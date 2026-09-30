"""links stage, part 1: `ingredient_compound` (food/herb -> compound) and `dish_nutrient`.

Sources: FooDB Content, Phenol-Explorer, CMAUP, NPASS (+ scraped amounts), FlavorDB2, IMPPAT, TM-MC, HERB and
SymMap scraped herb->ingredient. Rows are staged in TEMP TABLE stg_ic and deduplicated on
(ingredient, compound, source): median mg/100 g, best evidence, distinct plant parts and citations.
"""
import re

import pandas as pd

from common import data
from build.links_common import log, lookup_table, df_to_temp, s

STG = """CREATE OR REPLACE TEMP TABLE stg_ic (ingredient_id VARCHAR, compound_id VARCHAR, amount DOUBLE, unit VARCHAR,
         mg_per_100g DOUBLE, plant_part VARCHAR, evidence_type VARCHAR, source_id VARCHAR, citation VARCHAR)"""

# unit (lower-cased, trimmed) -> factor to mg/100 g (fresh weight / as eaten); dry-weight and molar units stay NULL
UNIT_FACTOR = {
    "mg/100g": 1, "mg/100 g": 1, "mg/100 g fresh weight": 1, "mg/100 g freshweight": 1, "mg/100g of fw": 1,
    "mg/kg": 0.1, "mg/kg fresh weight": 0.1, "mg/kg fresh sample": 0.1, "mg/kg puree": 0.1, "ppm": 0.1,
    "ug/g": 0.1, "ug/g fresh weight": 0.1, "µg/g": 0.1, "μg/g": 0.1, "µg/g of fw": 0.1, "ng/mg": 0.1,
    "g/100g": 1000, "g/100 g": 1000, "g/kg": 100, "g/kg fresh weight": 100, "mg/g": 100,
    "ug/100g": 0.001, "ug/ 100g fresh weight": 0.001, "µg/100g": 0.001, "µg/100 g": 0.001, "μg/100g": 0.001,
    "ppb": 0.0001, "ug/kg": 0.0001, "ug/kg fresh weight": 0.0001,
}
MAX_MG = 100_000  # > 100 g per 100 g is impossible: keep the raw amount, drop the normalised value


def unit_case(col):
    """SQL CASE giving the mg/100 g factor for a unit column."""
    whens = " ".join(f"WHEN '{u}' THEN {f}" for u, f in UNIT_FACTOR.items())
    return f"(CASE lower(trim({col})) {whens} ELSE NULL END)"


def _fix_mojibake(u):
    return None if u is None else u.replace("Âµ", "µ").replace("Î¼", "μ")


def build_ingredient_compound(con, ir, cr):
    con.execute(STG)
    ins = "INSERT INTO stg_ic "

    # ---- FooDB Content ------------------------------------------------------------------------------------
    con.execute(f"""CREATE OR REPLACE TEMP TABLE fc AS
        SELECT food_id, source_id, nullif(trim(orig_food_part), '') AS part, orig_unit AS unit, citation, citation_type,
               coalesce(try_cast(orig_content AS DOUBLE),
                        (try_cast(orig_min AS DOUBLE) + try_cast(orig_max AS DOUBLE)) / 2) AS amount
        FROM read_csv(?, all_varchar=true) WHERE source_type = 'Compound'""", [data("foodb", "Content.csv")])
    n_all = con.execute("SELECT count(*) FROM fc").fetchone()[0]
    lookup_table(con, "lk_ffood", [r[0] for r in con.execute("SELECT DISTINCT food_id FROM fc").fetchall()],
                 lambda k: ir.by_xref("foodb_food", k))
    lookup_table(con, "lk_fcmp", [r[0] for r in con.execute("SELECT DISTINCT source_id FROM fc").fetchall()],
                 lambda k: cr.by_xref("foodb", k))
    con.execute(ins + f"""
        SELECT f.v, c.v, fc.amount, fc.unit,
               CASE WHEN fc.amount * {unit_case('fc.unit')} <= {MAX_MG} THEN fc.amount * {unit_case('fc.unit')} END,
               fc.part,
               CASE WHEN fc.citation_type IN ('DATABASE', 'EXPERIMENTAL', 'ARTICLE', 'TEXTBOOK') THEN 'curated_literature'
                    WHEN fc.citation_type = 'UNKNOWN' AND fc.amount IS NOT NULL THEN 'curated_literature'
                    ELSE 'predicted' END AS ev,
               'foodb', fc.citation
        FROM fc JOIN lk_ffood f ON f.k = fc.food_id JOIN lk_fcmp c ON c.k = fc.source_id
        -- predicted rows (PathBank/HMDB expected, UNKNOWN) without an amount are useless and huge
        WHERE NOT (fc.amount IS NULL AND (fc.citation_type IN ('PREDICTED', 'UNKNOWN') OR fc.citation_type IS NULL))""")
    n = con.execute("SELECT count(*) FROM stg_ic WHERE source_id='foodb'").fetchone()[0]
    log(f"FooDB Content: {n_all:,} compound rows -> {n:,} staged")
    con.execute("DROP TABLE fc")

    # ---- Phenol-Explorer ----------------------------------------------------------------------------------
    pe = pd.read_excel(data("phenol-explorer", "composition-data.xlsx"),
                       usecols=["food", "compound", "units", "mean", "pubmed_ids"], dtype={"pubmed_ids": str})
    foods = pd.read_csv(data("phenol-explorer", "foods.csv"), dtype=str, keep_default_na=False)
    sci = dict(zip(foods.name, foods.food_source_scientific_name))
    pcomp = pd.read_csv(data("phenol-explorer", "compounds.csv"), dtype=str, keep_default_na=False)
    pid = dict(zip(pcomp.name, pcomp.id))

    def pe_food(name):
        hit = ir.by_scientific(sci[name]) if s(sci.get(name)) else None
        if hit:
            return hit
        base = re.sub(r"\[[^\]]*\]", " ", name).split(",")[0].strip()
        return ir.by_text(base, "en", fuzzy=False)

    fmap = {k: v for k in pe.food.unique() if (v := pe_food(k))}
    cmap = {k: v for k in pe.compound.unique()
            if (v := (cr.by_xref("phenol_explorer", pid[k]) if k in pid else None) or cr.by_name(k))}
    rows = []
    for r in pe.itertuples(index=False):
        ing, cmp_ = fmap.get(r.food), cmap.get(r.compound)
        if not ing or not cmp_:
            continue
        mean = float(r.mean) if pd.notna(r.mean) else None
        mg = mean if (mean is not None and str(r.units).startswith("mg/100 g")) else None
        cit = "PMID:" + str(r.pubmed_ids).replace("; ", "|PMID:") if s(r.pubmed_ids) else None
        rows.append((ing[0], cmp_, mean, r.units, mg, None, "curated_literature", "phenol", cit))
    df_to_temp(con, "pe_rows", pd.DataFrame(rows, columns=["i", "c", "a", "u", "m", "p", "e", "s", "ci"]))
    con.execute(ins + "SELECT * FROM pe_rows")
    log(f"Phenol-Explorer: {len(pe):,} rows, foods matched {len(fmap)}/{pe.food.nunique()}, "
        f"compounds {len(cmap)}/{pe.compound.nunique()} -> {len(rows):,} staged")

    # ---- CMAUP plant -> ingredient ------------------------------------------------------------------------
    # mixed LF / CRLF line endings: DuckDB's sniffer rejects the file, pandas copes
    cm = pd.read_csv(data("cmaup", "CMAUPv2.0_download_Plant_Ingredient_Associations_allIngredients.txt"), sep="\t",
                     dtype=str).rename(columns={"Plant_ID": "p", "Ingredient_ID": "c"})
    cm["c"] = cm.c.str.strip()
    df_to_temp(con, "cm", cm)
    plant = lambda k: ir.by_xref("cmaup", k) or ir.by_xref("npass", k)
    npc = lambda k: cr.by_xref("cmaup", k) or cr.by_xref("npass", k)
    lookup_table(con, "lk_cmp_plant", [r[0] for r in con.execute("SELECT DISTINCT p FROM cm").fetchall()], plant)
    lookup_table(con, "lk_cmp_np", [r[0] for r in con.execute(
        "SELECT DISTINCT c FROM cm WHERE p IN (SELECT k FROM lk_cmp_plant)").fetchall()], npc)
    con.execute(ins + """SELECT p.v, c.v, NULL, NULL, NULL, NULL, 'curated_literature', 'cmaup', NULL
                         FROM cm JOIN lk_cmp_plant p ON p.k = cm.p JOIN lk_cmp_np c ON c.k = cm.c""")
    log(f"CMAUP: {con.execute('SELECT count(*) FROM stg_ic WHERE source_id=?', ['cmaup']).fetchone()[0]:,} staged "
        f"({con.execute('SELECT count(*) FROM lk_cmp_plant').fetchone()[0]} plants)")

    # ---- NPASS species pairs + scraped amounts ------------------------------------------------------------
    con.execute("""CREATE OR REPLACE TEMP TABLE np AS SELECT org_id, np_id, org_isolation_part AS part, ref_id, ref_id_type
                   FROM read_csv(?, delim='\t', all_varchar=true, quote='')""",
                [data("npass", "NPASS3.0_naturalproducts_species_pair.txt")])
    lookup_table(con, "lk_np_org", [r[0] for r in con.execute("SELECT DISTINCT org_id FROM np").fetchall()],
                 lambda k: ir.by_xref("npass", k) or ir.by_xref("cmaup", k))
    lookup_table(con, "lk_np_c", [r[0] for r in con.execute(
        "SELECT DISTINCT np_id FROM np WHERE org_id IN (SELECT k FROM lk_np_org)").fetchall()], npc)
    con.execute(ins + """SELECT o.v, c.v, NULL, NULL, NULL,
                                CASE WHEN np.part NOT IN ('n.a.', '') THEN np.part END, 'curated_literature', 'npass',
                                CASE WHEN np.ref_id_type = 'PMID' THEN 'PMID:' || np.ref_id
                                     WHEN np.ref_id NOT IN ('n.a.', '') THEN np.ref_id END
                         FROM np JOIN lk_np_org o ON o.k = np.org_id JOIN lk_np_c c ON c.k = np.np_id""")
    q = pd.read_csv(data("npass", "scraped_np_quantity_sample.csv"), dtype=str, keep_default_na=False, encoding="utf-8")
    rows = []
    for r in q.itertuples(index=False):
        ing = ir.by_xref("npass", r.org_id) or ir.by_xref("cmaup", r.org_id)
        c = npc(r.np_id)
        if not ing or not c:
            continue
        try:
            v = float(r.quantity_standard)
        except ValueError:
            try:
                v = (float(r.quantity_min) + float(r.quantity_max)) / 2
            except ValueError:
                continue
        unit = _fix_mojibake(r.quantity_unit)
        f = UNIT_FACTOR.get(unit.lower().strip())
        mg = v * f if f is not None and v * f <= MAX_MG else None
        rows.append((ing[0], c, v, unit, mg, s(r.org_part), "curated_literature", "npass", s(r.reference)))
    if rows:
        df_to_temp(con, "npq", pd.DataFrame(rows, columns=["i", "c", "a", "u", "m", "p", "e", "s", "ci"]))
        con.execute(ins + "SELECT * FROM npq")
    log(f"NPASS: {con.execute('SELECT count(*) FROM stg_ic WHERE source_id=?', ['npass']).fetchone()[0]:,} staged "
        f"(scraped amounts usable: {len(rows)} of {len(q)})")
    con.execute("DROP TABLE np; DROP TABLE cm")

    # ---- FlavorDB2 ----------------------------------------------------------------------------------------
    em = pd.read_csv(data("flavordb2", "entity_molecules.csv"), dtype=str)
    rows = []
    for e, p in zip(em.entity_id, em.pubchem_id):
        ing, c = ir.by_xref("flavordb", e), cr.by_xref("flavordb", p)
        if ing and c:
            rows.append((ing[0], c, None, None, None, None, "curated_literature", "flavordb", None))
    df_to_temp(con, "fl", pd.DataFrame(rows, columns=["i", "c", "a", "u", "m", "p", "e", "s", "ci"]))
    con.execute(ins + "SELECT * FROM fl")
    log(f"FlavorDB: {len(em):,} pairs -> {len(rows):,} staged")

    # ---- IMPPAT phytochemical-plant association -----------------------------------------------------------
    con.execute("""CREATE OR REPLACE TEMP TABLE im AS SELECT Plant_identifier AS p, IMPPAT_Phytochemical_identifier AS c,
                          nullif(trim(Plant_part), '') AS part, Reference_identifier AS ref
                   FROM read_csv(?, delim='\t', all_varchar=true, quote='')""",
                [data("imppat", "IMPPAT_Phytochemical_Plant_Association.tsv")])
    lookup_table(con, "lk_im_p", [r[0] for r in con.execute("SELECT DISTINCT p FROM im").fetchall()],
                 lambda k: ir.by_xref("imppat", k))
    lookup_table(con, "lk_im_c", [r[0] for r in con.execute("SELECT DISTINCT c FROM im").fetchall()],
                 lambda k: cr.by_xref("imppat", k))
    con.execute(ins + """SELECT p.v, c.v, NULL, NULL, NULL, im.part, 'curated_literature', 'imppat', im.ref
                         FROM im JOIN lk_im_p p ON p.k = im.p JOIN lk_im_c c ON c.k = im.c""")
    log(f"IMPPAT: {con.execute('SELECT count(*) FROM stg_ic WHERE source_id=?', ['imppat']).fetchone()[0]:,} staged")

    # ---- TM-MC material -> compound (PMID) ----------------------------------------------------------------
    mc = pd.read_excel(data("tm-mc", "medicinal_compound.xlsx"), dtype=str)
    rows = []
    mats = {m: ir.by_xref("tmmc", m) for m in mc.LATIN.unique()}
    cids = {i: cr.by_xref("tmmc", i) for i in mc.ID.unique()}
    for r in mc.itertuples(index=False):
        ing, c = mats.get(r.LATIN), cids.get(r.ID)
        if ing and c:
            rows.append((ing[0], c, None, None, None, None, "curated_literature", "tmmc",
                         "PMID:" + r.PMID if s(r.PMID) else None))
    df_to_temp(con, "tm", pd.DataFrame(rows, columns=["i", "c", "a", "u", "m", "p", "e", "s", "ci"]))
    con.execute(ins + "SELECT * FROM tm")
    log(f"TM-MC: {len(mc):,} rows, materials matched {sum(1 for v in mats.values() if v)}/{len(mats)} -> {len(rows):,} staged")

    # ---- HERB / SymMap scraped herb -> ingredient ---------------------------------------------------------
    rows = []
    hi = pd.read_csv(data("herb", "scrape", "herb_ingredient.csv"), dtype=str)
    for h, i in zip(hi.source_herb_id, hi["Ingredient id"]):
        ing, c = ir.by_xref("herb", h), cr.by_xref("herb", i)
        if ing and c:
            rows.append((ing[0], c, None, None, None, None, "traditional", "herb", None))
    sm = pd.read_csv(data("symmap", "scrape", "herb_ingredient_relations.csv"), dtype=str)
    for h, i in zip(sm.source_herb_id, sm.MOL_id):
        ing, c = ir.by_xref("symmap", h), cr.by_xref("symmap", i)
        if ing and c:
            rows.append((ing[0], c, None, None, None, None, "traditional", "symmap", None))
    df_to_temp(con, "hs", pd.DataFrame(rows, columns=["i", "c", "a", "u", "m", "p", "e", "s", "ci"]))
    con.execute(ins + "SELECT * FROM hs")
    log(f"HERB/SymMap scraped herb->ingredient: {len(hi) + len(sm):,} rows -> {len(rows):,} staged")

    # ---- dedupe on (ingredient, compound, source) ---------------------------------------------------------
    con.execute("DELETE FROM ingredient_compound")
    con.execute("""
        INSERT INTO ingredient_compound
        SELECT s.ingredient_id, s.compound_id,
               arg_min(s.amount, (s.mg_per_100g IS NULL)::INT * 10 + e.rank) FILTER (WHERE s.amount IS NOT NULL),
               arg_min(s.unit, (s.mg_per_100g IS NULL)::INT * 10 + e.rank) FILTER (WHERE s.amount IS NOT NULL),
               median(s.mg_per_100g),
               left(string_agg(DISTINCT s.plant_part, '|'), 200),
               arg_min(s.evidence_type, e.rank),
               s.source_id,
               left(string_agg(DISTINCT s.citation, '|'), 500)
        FROM stg_ic s JOIN evidence_type e ON e.code = s.evidence_type
        WHERE s.ingredient_id IN (SELECT ingredient_id FROM ingredient)
          AND s.compound_id IN (SELECT compound_id FROM compound)
        GROUP BY s.ingredient_id, s.compound_id, s.source_id""")
    log("ingredient_compound: " + ", ".join(f"{a} {b:,}" for a, b in con.execute(
        "SELECT source_id, count(*) FROM ingredient_compound GROUP BY 1 ORDER BY 2 DESC").fetchall()))
    con.execute("DROP TABLE stg_ic")


def build_dish_nutrient(con, cr):
    from build.dishes import iter_dish_nutrients
    rows, skipped = [], 0
    cache = {}

    def nutrient(key, src, unit):
        """The dishes stage yields bare analyte labels; nutrient_map.csv keys carry the unit in each source's own
        header style ('Magnesium [mg]', 'Na (mg/100g)', 'sodium_mg'). Try the bare key, then those forms."""
        ck = (key, src, unit)
        if ck not in cache:
            u = (unit or "").strip()
            cands = [key, f"{key} [{u}]", f"{key} ({u}/100g)", f"{key} ({u}/100g as printed)", f"{key} ({u})",
                     f"{key}_{u.lower().replace('µ', 'u').replace('μ', 'u').replace('mcg', 'ug')}"]
            cache[ck] = next((c for c in (cr.nutrient(k, src) for k in cands) if c), None)
        return cache[ck]

    for dish_id, key, src, amt, unit in iter_dish_nutrients():
        if src == "indb" and str(key).startswith("unit_serving_"):  # per-serving values, not per 100 g
            skipped += 1
            continue
        c = nutrient(key, src, unit)
        if c is None:
            skipped += 1
            continue
        rows.append((dish_id, c, amt, unit, src))
    df = pd.DataFrame(rows, columns=["dish_id", "c", "a", "u", "s"])
    con.execute("DELETE FROM dish_nutrient")
    df_to_temp(con, "dn", df)
    con.execute("""INSERT INTO dish_nutrient SELECT dish_id, c, a, u, s FROM dn
                   WHERE dish_id IN (SELECT dish_id FROM dish) AND c IN (SELECT compound_id FROM compound)""")
    n = con.execute("SELECT count(*) FROM dish_nutrient").fetchone()[0]
    log(f"dish_nutrient: {n:,} rows ({skipped:,} values skipped: energy/water/unmapped keys)")
    con.execute("DROP TABLE dn")
