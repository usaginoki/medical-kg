"""Print dish → condition and condition → dish traces from the unified database, as Markdown.

  uv run db/trace.py dish "kabsa" [--country SA] [--type symptom] [--top 12] [--drug warfarin]
  uv run db/trace.py condition "nausea" [--country IN] [--top 15] [--drug warfarin]
  uv run db/trace.py sql "SELECT …"      # ad-hoc query, printed as a table

Every hop shows its source (vault dataset note) and evidence grade, so a trace can be pasted into a vault note.
"""
import argparse, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import connect  # noqa: E402

RANK = {1: "clinical", 2: "curated", 3: "epidemiological", 4: "traditional", 5: "text-mined", 6: "predicted"}
DIRS = [("beneficial", "May help"), ("harmful", "May aggravate / harmful"),
        ("marker", "Associated (marker / mechanism)"), ("association", "Associated")]


def inlist(values):
    """'(?,?,…)' placeholder list. Bound constants let DuckDB push the filter into the views; a
    `IN (SELECT unnest(?))` semi-join does not, and then v_dish_condition is computed for every dish."""
    return "(" + ",".join("?" * max(len(values), 1)) + ")"


_VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_NOTES = {os.path.basename(f)[:-3] for d in ("Datasets", "Countries", "Regions", "Questions", "Papers", "Database")
          for f in __import__("glob").glob(os.path.join(_VAULT, d, "*.md"))} | {"Access requests"}
_WIKI = re.compile(r"\[\[([^\]|]+)(\|[^\]]*)?\]\]")


def _safe(text):
    """Escape [[…]] that is not a vault note (chemical names such as 5-[[Amino(…)]]… would become links)."""
    out, i = [], 0
    while (j := text.find("[[", i)) >= 0:
        m = _WIKI.match(text, j)
        keep = m is not None and m.group(1) in _NOTES
        out.append(text[i:j] + ("[[" if keep else "[\u200b["))
        i = j + 2
    return "".join(out) + text[i:]


def table(rows, header):
    if not rows:
        return "_none_\n"
    fmt = lambda v: "" if v is None else (f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v))
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join(_safe(fmt(v)).replace("|", "\\|") for v in r) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def note_of(con, source_id):
    r = con.execute("SELECT dataset_note FROM source WHERE source_id = ?", [source_id]).fetchone()
    return f"[[{r[0]}]]" if r and r[0] else source_id


def notes(con, ids):
    return ", ".join(sorted({note_of(con, s) for s in (ids or "").split(",") if s})) if ids else ""


def expand_condition(con, root):
    """Root condition + narrower terms (is_a), direct parents, TCM equivalents, same_as and actions targeting it."""
    return [r[0] for r in con.execute("""
        WITH RECURSIVE x(id, depth) AS (
          SELECT ?::VARCHAR, 0
          UNION
          SELECT CASE WHEN r.to_id = x.id THEN r.from_id ELSE r.to_id END, x.depth + 1
          FROM condition_relation r JOIN x ON (
               (r.rel = 'is_a' AND r.to_id = x.id)                                   -- children
            OR (r.rel IN ('tcm_maps_to', 'same_as') AND (r.from_id = x.id OR r.to_id = x.id))
            OR (r.rel = 'action_targets' AND r.to_id = x.id))                        -- actions aimed at it
          WHERE x.depth < 3)
        SELECT DISTINCT id FROM x
        UNION   -- plus the direct parents: traditional sources often use the broader term ("diabetes")
        SELECT to_id FROM condition_relation WHERE rel = 'is_a' AND from_id = ?""", [root, root]).fetchall()]


def find_condition(con, term):
    try:
        from build.resolve import ConditionResolver
        cid = ConditionResolver(con).by_text(term)
        if cid:
            return cid
    except Exception:
        pass
    r = con.execute("""SELECT condition_id FROM condition_alias WHERE lower(alias) = lower(?)
                       UNION ALL SELECT condition_id FROM condition WHERE name ILIKE ? LIMIT 1""",
                    [term, f"%{term}%"]).fetchone()
    return r[0] if r else None


def trace_dish(con, a):
    rows = con.execute("""SELECT dish_id, name, name_local, country_iso2, subregion, cuisine_label, source_id
                          FROM dish WHERE (name ILIKE ? OR name_local ILIKE ?) AND (? IS NULL OR country_iso2 = ?)
                          ORDER BY length(name) LIMIT 10""",
                       [f"%{a.query}%", f"%{a.query}%", a.country, a.country]).fetchall()
    if not rows:
        sys.exit(f"no dish matching {a.query!r}")
    dish = rows[0]
    print(f"## Dish → conditions: {dish[1]}" + (f" ({dish[2]})" if dish[2] and dish[2] != dish[1] else ""))
    print(f"\n`{dish[0]}` · {dish[3] or ''} {('· ' + dish[4]) if dish[4] else ''} · cuisine: {dish[5] or '—'} · "
          f"source: {note_of(con, dish[6])}")
    if len(rows) > 1:
        print("\nOther matches: " + "; ".join(f"`{r[0]}` {r[1]}" for r in rows[1:]))
    print("\n### Ingredients\n")
    print(table(con.execute("""SELECT di.raw_text, di.ingredient_id, di.grams, di.match_method, di.match_score
                               FROM dish_ingredient di WHERE dish_id = ? ORDER BY di.grams DESC NULLS LAST""",
                            [dish[0]]).fetchall(), ["line", "ingredient", "g", "match", "score"]))
    tfilter = "AND c.type = ?" if a.type else "AND c.type IN ('symptom','disease','finding')"
    for d, label in DIRS:
        sal = "" if a.all else "AND (v.n_salient_ingredients > 0 OR v.via_high_nutrient)"
        res = con.execute(f"""SELECT c.name, c.type, coalesce(v.best_salient_rank, v.best_evidence_rank),
                                     v.max_salient_sources, v.n_salient_ingredients,
                                     coalesce(v.salient_ingredients, v.ingredients), v.via_high_nutrient,
                                     v.condition_id
                              FROM v_dish_condition v JOIN condition c USING (condition_id)
                              WHERE v.dish_id = ? AND v.direction = ? {tfilter} {sal}
                              -- strongest single-ingredient support (independent sources) first, then evidence
                              -- grade, then how many characteristic ingredients agree
                              ORDER BY v.max_salient_sources DESC, v.best_salient_rank,
                                       v.n_salient_ingredients DESC LIMIT ?""",
                          [dish[0], d] + ([a.type] if a.type else []) + [a.top]).fetchall()
        if not res:
            continue
        print(f"### {label}\n")
        print(table([(r[0], r[1], RANK.get(r[2]), r[3], r[4], r[5], "high" if r[6] else "") for r in res],
                    ["condition", "type", "best evidence", "sources", "characteristic ingredients",
                     "via", "lab nutrient"]))
        print(hop_details(con, dish[0], [r[7] for r in res[:4]], d))
    high_nutrients(con, dish[0])
    drug_warnings(con, dish_ids=[dish[0]], drug=a.drug)


def high_nutrients(con, dish_id):
    rows = con.execute("""
        SELECT t.label, round(dn.amount_per_100g, 1), dn.unit, t.high_mg_per_100g,
               (SELECT string_agg(DISTINCT c.name, '; ') FROM compound_condition cc JOIN condition c USING (condition_id)
                WHERE cc.compound_id = dn.nutrient_compound_id AND c.type IN ('symptom', 'disease') LIMIT 1) AS conds,
               dn.source_id
        FROM dish_nutrient dn JOIN compound cp ON cp.compound_id = dn.nutrient_compound_id
        JOIN nutrient_high_threshold t ON t.mesh_id = cp.mesh_id
        WHERE dn.dish_id = ?
          AND dn.amount_per_100g * CASE lower(dn.unit) WHEN 'g' THEN 1000 ELSE 1 END >= t.high_mg_per_100g""",
                       [dish_id]).fetchall()
    if rows:
        print("### Lab-measured nutrients above the FSA \"high\" threshold\n")
        print(table([(r[0], r[1], r[2], r[3], (r[4] or "")[:160], note_of(con, r[5])) for r in rows],
                    ["nutrient", "per 100 g", "unit", "high ≥ (mg)", "CTD conditions (sample)", "source"]))


def hop_details(con, dish_id, condition_ids, direction):
    """Hop-by-hop evidence for the strongest characteristic paths to the given conditions.

    One row per (condition, ingredient, compound); the food→compound and compound→condition sources are merged.
    """
    rows = con.execute(f"""
        WITH p AS (
          SELECT c.name AS cond, di.ingredient_id AS ing, coalesce(cp.name, '(direct)') AS comp,
                 v.compound_mg_per_100g AS mg, v.evidence_rank AS r, v.link_source, v.content_source,
                 v.tradition, v.pmids, v.note
          FROM dish_ingredient di
          JOIN v_ingredient_condition_all v USING (ingredient_id)
          JOIN condition c ON c.condition_id = v.condition_id
          LEFT JOIN compound cp ON cp.compound_id = v.compound_id
          LEFT JOIN compound_profile pr ON pr.compound_id = v.compound_id
          WHERE di.dish_id = ? AND v.direction = ? AND v.condition_id IN {inlist(condition_ids)}
            AND (v.path_kind = 'direct'
                 OR (v.compound_mg_per_100g >= 1
                     AND (pr.n_ingredients <= 20 OR v.compound_mg_per_100g >= 0.1 * pr.max_mg_per_100g))))
        SELECT cond, ing, comp, max(mg), min(r),
               string_agg(DISTINCT content_source, ','), string_agg(DISTINCT link_source, ','),
               string_agg(DISTINCT tradition, ','), left(max(pmids), 40), left(max(note), 60)
        FROM p GROUP BY cond, ing, comp
        QUALIFY row_number() OVER (PARTITION BY cond ORDER BY min(r), max(mg) DESC NULLS LAST) <= 3
        ORDER BY cond, min(r), max(mg) DESC NULLS LAST""", [dish_id, direction] + list(condition_ids)).fetchall()
    out = [(r[0], r[1].removeprefix("ING:"), r[2], r[3], RANK.get(r[4]),
            notes(con, ",".join(x for x in (r[5], r[6]) if x)), r[7], r[8], r[9]) for r in rows]
    return "Strongest characteristic paths:\n\n" + table(
        out, ["condition", "ingredient", "compound", "mg/100 g", "evidence", "sources", "tradition", "PMIDs", "note"])


def drug_warnings(con, dish_ids=None, drug=None):
    """Food–drug interactions for the ingredients of the given dishes, one row per (ingredient, drug, effect)."""
    sql = f"""SELECT replace(di.ingredient_id, 'ING:', '') AS ing, dr.name AS drug, idr.effect AS eff,
                     string_agg(DISTINCT idr.mechanism, '; '), string_agg(DISTINCT idr.pmid, ', '),
                     string_agg(DISTINCT idr.source_id, ','), count(DISTINCT idr.pmid)
              FROM dish_ingredient di JOIN ingredient_drug idr USING (ingredient_id) JOIN drug dr USING (drug_id)
              WHERE di.dish_id IN {inlist(dish_ids)} AND """
    sql += "dr.name ILIKE ?" if drug else "idr.effect IN ('Harmful', 'Negative')"
    sql += """ GROUP BY ing, drug, eff ORDER BY CASE eff WHEN 'Harmful' THEN 1 WHEN 'Negative' THEN 2
               WHEN 'Positive' THEN 3 WHEN 'Possible' THEN 4 ELSE 5 END, ing LIMIT 20"""
    rows = con.execute(sql, list(dish_ids) + ([f"%{drug}%"] if drug else [])).fetchall()
    if rows:
        print(f"### Food–drug interactions{' with ' + drug if drug else ' (harmful / negative)'}\n")
        print(table([(r[0], r[1], r[2], r[3], r[4], notes(con, r[5])) for r in rows],
                    ["ingredient", "drug", "effect", "mechanism", "PMIDs", "source"]))


def trace_condition(con, a):
    root = find_condition(con, a.query)
    if not root:
        sys.exit(f"no condition matching {a.query!r}")
    ids = expand_condition(con, root)
    name = con.execute("SELECT name, type FROM condition WHERE condition_id = ?", [root]).fetchone()
    print(f"## Condition → dishes: {name[0]} (`{root}`, {name[1]})\n")
    others = con.execute(f"SELECT name, type FROM condition WHERE condition_id IN {inlist(ids)} AND condition_id <> ?",
                         ids + [root]).fetchall()
    if others:
        print("Expanded to: " + "; ".join(f"{n} ({t})" for n, t in others[:20]) + "\n")
    for d, label in DIRS[:3]:   # may help · may aggravate · associated (CTD marker/mechanism, e.g. sodium)
        sal = "" if a.all else """AND (v.path_kind = 'direct'
               OR (v.compound_mg_per_100g >= 1
                   AND (pr.n_ingredients <= 20 OR v.compound_mg_per_100g >= 0.1 * pr.max_mg_per_100g)))"""
        ing = con.execute(f"""SELECT i.canonical_name, v.ingredient_id, min(v.evidence_rank) r, count(*) n,
                                    count(DISTINCT v.link_source) ns,
                                    string_agg(DISTINCT v.link_source, ',') src, string_agg(DISTINCT v.tradition, ',') trad,
                                    string_agg(DISTINCT coalesce(cp.name, '(direct)'), '; ') via
                             FROM v_ingredient_condition_all v JOIN ingredient i USING (ingredient_id)
                             LEFT JOIN compound cp ON cp.compound_id = v.compound_id
                             LEFT JOIN compound_profile pr ON pr.compound_id = v.compound_id
                             WHERE v.condition_id IN {inlist(ids)} AND v.direction = ? {sal}
                             GROUP BY 1, 2
                             ORDER BY ns + 2 * (r <= 2)::INT + bool_or(v.path_kind = 'direct')::INT DESC, r, n DESC
                             LIMIT ?""", ids + [d, a.top]).fetchall()
        if not ing:
            continue
        print(f"### {label}: ingredients\n")
        print(table([(r[0], RANK.get(r[2]), r[3], notes(con, r[5]), r[6], (r[7] or "")[:80]) for r in ing],
                    ["ingredient", "best evidence", "paths", "sources", "tradition", "via"]))
        # Dose-aware dish score: Σ over the dish's helpful/harmful ingredients of (ingredient score² × weight share),
        # where ingredient score = number of independent sources behind its characteristic paths. A ginger tea should
        # outrank a curry that merely contains a pinch of ginger.
        # ingredient score = independent sources + 2 if clinical/curated evidence + 1 if a direct link exists
        top_ing = con.execute(f"""SELECT v.ingredient_id,
                                    count(DISTINCT v.link_source)
                                    + 2 * bool_or(v.evidence_rank <= 2)::INT
                                    + bool_or(v.path_kind = 'direct')::INT AS score
                             FROM v_ingredient_condition_all v
                             LEFT JOIN compound_profile pr ON pr.compound_id = v.compound_id
                             WHERE v.condition_id IN {inlist(ids)} AND v.direction = ? {sal}
                             GROUP BY 1 ORDER BY score DESC LIMIT 40""", ids + [d]).fetchall()
        if not top_ing:
            continue
        con.execute("CREATE OR REPLACE TEMP TABLE _ing_score (ingredient_id VARCHAR, score DOUBLE)")
        con.executemany("INSERT INTO _ing_score VALUES (?, ?)", top_ing)
        dishes = con.execute("""
            WITH lines AS (   -- distrust lowest-confidence weights (IndicRecipeNutri tier E) and spices > 30 g
              SELECT di.dish_id, di.ingredient_id,
                     CASE WHEN di.raw_text LIKE '%[weight tier E]%' OR (i.category = 'spice' AND di.grams > 30)
                          THEN NULL ELSE di.grams END AS g
              FROM dish_ingredient di LEFT JOIN ingredient i USING (ingredient_id)),
            tot AS (SELECT l.dish_id, sum(l.g) g, count(*) n, avg((l.g IS NOT NULL)::INT) cov,
                           avg((i.category IN ('spice', 'herb'))::INT) spice_share
                    FROM lines l LEFT JOIN ingredient i USING (ingredient_id) GROUP BY l.dish_id),
            hit AS (   -- weight share when ≥ 80% of the dish's lines have usable grams, else 1 / number of lines
              SELECT l.dish_id, l.ingredient_id, s.score,
                     CASE WHEN any_value(t.cov) >= 0.8 AND any_value(t.g) > 0
                          THEN coalesce(sum(l.g), 0) / any_value(t.g)
                          ELSE count(*) / any_value(t.n) END AS share
              FROM lines l JOIN _ing_score s USING (ingredient_id) JOIN tot t USING (dish_id)
              GROUP BY l.dish_id, l.ingredient_id, s.score)
            SELECT d.name, d.country_iso2, d.subregion, d.source_id, sum(h.score * h.score * h.share) AS dish_score,
                   string_agg(replace(h.ingredient_id, 'ING:', '') || ' ' || round(100 * h.share)::INT || '%', ', '
                              ORDER BY h.score * h.score * h.share DESC) AS contributions,
                   d.dish_id
            FROM hit h JOIN dish d USING (dish_id)
            JOIN tot t ON t.dish_id = d.dish_id
            WHERE (? IS NULL OR d.country_iso2 = ?)
              AND t.n >= 4   -- skip truncated records (e.g. XiaChuFang/CulinaryDB/IndicRecipeNutri rows with 1–3 lines)
              AND (? OR coalesce(t.spice_share, 0) < 0.75)   -- spice blends (garam masala, rasam powder) are not meals
            GROUP BY d.name, d.country_iso2, d.subregion, d.source_id, d.dish_id
            ORDER BY dish_score DESC LIMIT ?""", [a.country, a.country, a.blends, a.top]).fetchall()
        print(f"### {label}: dishes{' in ' + a.country if a.country else ''} (dose-aware)\n")
        print(table([(r[0], r[1], r[2], note_of(con, r[3]), round(r[4], 2), r[5]) for r in dishes],
                    ["dish", "country", "subregion", "source", "score", "contributing ingredients (weight share)"]))
        dishes = [(None,) * 7 + (r[6],) for r in dishes]
        if a.drug and dishes:
            drug_warnings(con, dish_ids=[r[7] for r in dishes], drug=a.drug)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["dish", "condition", "sql"])
    ap.add_argument("query")
    ap.add_argument("--country", help="ISO 3166-1 alpha-2, e.g. SA, IN, JP")
    ap.add_argument("--type", choices=["symptom", "disease", "finding"])
    ap.add_argument("--drug")
    ap.add_argument("--top", type=int, default=12)
    ap.add_argument("--all", action="store_true", help="include non-characteristic (ubiquitous-compound) paths")
    ap.add_argument("--blends", action="store_true", help="include spice blends (≥ 75%% spice lines) in dish lists")
    a = ap.parse_args()
    con = connect(read_only=True)
    if a.mode == "sql":
        cur = con.execute(a.query)
        print(table(cur.fetchall(), [d[0] for d in cur.description]))
    elif a.mode == "dish":
        trace_dish(con, a)
    else:
        trace_condition(con, a)


if __name__ == "__main__":
    main()
