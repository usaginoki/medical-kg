"""Export data for the interactive presentation of the unified database and build the HTML.

Usage: uv run db/presentation/export.py

Reads db/unified.duckdb (every number and example row comes from the DB), the curated dataset text in
db/presentation/content.py, and writes
  db/presentation/data.json            the data bundle
  db/presentation/artifact.html        page fragment (for publishing as an Artifact)
  Database/presentation/index.html     stand-alone page for the repo (opens offline in any browser)
"""
import datetime, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
from common import VAULT, connect  # noqa: E402

try:
    import content  # curated dataset descriptions (db/presentation/content.py)
except ImportError:
    content = None

con = connect(read_only=True)


def rows(sql, params=None):
    cur = con.execute(sql, params or [])
    cols = [d[0] for d in cur.description]
    out = []
    for r in cur.fetchall():
        d = {}
        for c, v in zip(cols, r):
            if isinstance(v, float):
                v = round(v, 2)
            elif isinstance(v, (datetime.date, datetime.datetime)):
                v = str(v)
            d[c] = v
        out.append(d)
    return out


def one(sql, params=None):
    return con.execute(sql, params or []).fetchone()[0]


def breakdown(sql, label, top=8):
    items = [{"k": str(r[0]), "v": int(r[1])} for r in con.execute(sql).fetchall()]
    items.sort(key=lambda x: -x["v"])
    rest = sum(i["v"] for i in items[top:])
    items = items[:top] + ([{"k": "other", "v": rest}] if rest else [])
    return {"label": label, "items": items}


def must(r, what):
    if not r:
        sys.exit(f"export: trace row not found: {what}")
    return r


# ---------------------------------------------------------------------------------------------------------------
# Trace rows (asserted: the presentation must show real rows)
T = {}
T["dish"] = must(rows("""SELECT dish_id, name, country_iso2, subregion, cuisine_label, servings, source_id
                         FROM dish WHERE dish_id = 'sfct:68'"""), "dish sfct:68")
T["dish_ingredient"] = must(rows("""SELECT dish_id, raw_text, grams, match_method, match_score, ingredient_id, source_id
                                    FROM dish_ingredient WHERE dish_id = 'sfct:68' AND ingredient_id = 'ING:turmeric'"""),
                            "turmeric line")
T["ingredient"] = must(rows("""SELECT ingredient_id, canonical_name, scientific_name, ncbi_taxon_id, foodon_id, category,
                                      is_herb FROM ingredient WHERE ingredient_id = 'ING:turmeric'"""), "turmeric")
T["ingredient_compound"] = must(rows("""
    SELECT ic.ingredient_id, ic.compound_id, ic.amount, ic.unit, ic.mg_per_100g, ic.evidence_type, ic.source_id
    FROM ingredient_compound ic
    WHERE ic.ingredient_id = 'ING:turmeric' AND ic.compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N'
      AND ic.source_id IN ('foodb', 'phenol') ORDER BY ic.source_id"""), "turmeric→curcumin")
T["compound"] = must(rows("""SELECT compound_id, name, pubchem_cid, mesh_id, inchikey, is_nutrient FROM compound
                             WHERE compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N' AND pubchem_cid = 969516"""), "curcumin")
T["compound_condition"] = must(rows("""
    SELECT compound_id, condition_id, direction, evidence_type, source_id, pmids, score FROM compound_condition
    WHERE compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N' AND condition_id = 'MESH:D003924'
      AND source_id = 'ctd' AND pmids LIKE '%18403477%'"""), "CTD curcumin→T2D")
T["condition"] = must(rows("""SELECT condition_id, name, type, mesh_tree, umls_cui, source_vocab FROM condition
                              WHERE condition_id IN ('MESH:D003924', 'MESH:D003920') ORDER BY condition_id DESC"""),
                      "T2D / DM")
T["ingredient_condition"] = must(rows("""
    SELECT ingredient_id, condition_id, direction, evidence_type, tradition, n_pos, n_neg, left(pmids, 34) AS pmids,
           source_id, note FROM ingredient_condition
    WHERE ingredient_id = 'ING:turmeric' AND condition_id = 'MESH:D003920' AND source_id IN ('spicerx', 'imppat')
    ORDER BY source_id DESC"""), "turmeric→DM direct")
T["ingredient_drug"] = must(rows("""
    SELECT DISTINCT ingredient_id, drug_id, effect, evidence_type, pmid, source_id, left(note, 110) AS note
    FROM ingredient_drug WHERE ingredient_id = 'ING:turmeric' AND drug_id = 'DB:DB00682' AND pmid = '34062109'"""),
                             "turmeric×warfarin")[:1]
T["drug"] = must(rows("SELECT drug_id, name, drugbank_id, inchikey FROM drug WHERE drug_id = 'DB:DB00682'"), "warfarin")
T["dish_nutrient"] = must(rows("""
    SELECT dn.dish_id, dn.nutrient_compound_id, c.name AS nutrient, dn.amount_per_100g, dn.unit, dn.source_id
    FROM dish_nutrient dn JOIN compound c ON c.compound_id = dn.nutrient_compound_id
    WHERE dn.dish_id = 'sfct:68' AND (c.mesh_id IN ('MESH:D012964', 'MESH:D000073417')
          OR c.name LIKE '2-Methyl-3-[(E)-3,7,11,15%')
    ORDER BY c.name DESC"""), "Timman nutrients")
for r in T["dish_nutrient"]:
    if r["nutrient"].startswith("2-Methyl-3-"):
        r["nutrient"] = "Vitamin K₁ (phylloquinone)"

trace_extra = {
    "is_a": rows("""SELECT from_id, to_id, rel FROM condition_relation
                    WHERE from_id = 'MESH:D003924' AND to_id = 'MESH:D003920' AND rel = 'is_a'"""),
    "aliases": rows("""SELECT lang, string_agg(DISTINCT alias, ' · ') AS aliases FROM ingredient_alias
                       WHERE ingredient_id = 'ING:turmeric' AND lang IN ('zh','ja','ko','fa','zh-Latn','la')
                       GROUP BY lang ORDER BY lang"""),
    "xref_dbs": one("SELECT count(DISTINCT db) FROM ingredient_xref WHERE ingredient_id = 'ING:turmeric'"),
    "compound_xrefs": rows("""SELECT db, count(*) AS n FROM compound_xref
                              WHERE compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N'
                                AND db NOT IN ('synonym','pubchem','cas','chebi','ctd_match') GROUP BY db ORDER BY n DESC"""),
    "curcumin_conditions": one("""SELECT count(DISTINCT condition_id) FROM compound_condition
                                  WHERE compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N'"""),
    "turmeric_paths_t2d": one("""SELECT count(*) FROM v_ingredient_condition_all
                                 WHERE ingredient_id = 'ING:turmeric' AND condition_id IN ('MESH:D003924', 'MESH:D003920')"""),
    "warfarin_ing": one("SELECT count(DISTINCT ingredient_id) FROM ingredient_drug WHERE drug_id = 'DB:DB00682'"),
}

# ---------------------------------------------------------------------------------------------------------------
# Per-table stats and examples. `trace` marks the row(s) used by the patient trace.
EX = {}
EX["dish"] = rows("""SELECT dish_id, name, name_local, country_iso2, subregion, source_id FROM dish
    WHERE dish_id IN ('sfct:68','kfct:13001','maff:758','xiachufang:59932','indicrecipenutri:15191','culinarydb:4782')""")
EX["dish_ingredient"] = rows("""
    SELECT * FROM (
      SELECT dish_id, raw_text, grams, match_method, match_score, ingredient_id, source_id,
             row_number() OVER (PARTITION BY dish_id ORDER BY grams DESC NULLS LAST) AS rk
      FROM dish_ingredient
      WHERE dish_id IN ('kfct:13001','maff:758','xiachufang:59932','indicrecipenutri:15191','culinarydb:4782')
        AND ingredient_id IS NOT NULL)
    WHERE rk = 1""")
EX["dish_nutrient"] = rows("""
    SELECT dn.dish_id, c.name AS nutrient, dn.amount_per_100g, dn.unit, dn.source_id
    FROM dish_nutrient dn JOIN compound c ON c.compound_id = dn.nutrient_compound_id
    WHERE (dn.dish_id, c.mesh_id) IN (('sfct:96','MESH:D012964'), ('kfct:13001','MESH:D012964'),
                                      ('indb:ASC001','MESH:D004041'), ('bfct:1','MESH:D000073417'))""")
EX["ingredient"] = rows("""SELECT ingredient_id, canonical_name, scientific_name, ncbi_taxon_id, category FROM ingredient
    WHERE ingredient_id IN ('ING:ginger','ING:dried-lime','ING:burdock','ING:soy-sauce','ING:camel-meat','ING:nigella')""")
EX["ingredient_compound"] = rows("""
    SELECT ic.ingredient_id, c.name AS compound, ic.mg_per_100g, ic.evidence_type, ic.source_id
    FROM ingredient_compound ic JOIN compound c USING (compound_id)
    WHERE (ic.ingredient_id, c.name, ic.source_id) IN (('ING:black-pepper','Piperine','foodb'),
          ('ING:soy-sauce','Sodium','foodb'), ('ING:garlic','Allicin','foodb'), ('ING:green-tea','Epigallocatechin gallate','phenol'),
          ('ING:nigella','Thymoquinone','npass'))""")
EX["compound"] = rows("""SELECT compound_id, name, pubchem_cid, mesh_id FROM compound
    WHERE (name, pubchem_cid) IN (('Piperine', 638024), ('Sodium', 5360545), ('Thymoquinone', 10281),
                                  ('Epigallocatechin gallate', 65064), ('Trigonelline', 5570))""")
EX["compound_condition"] = rows("""
    SELECT c.name AS compound, k.name AS condition, cc.direction, cc.evidence_type, cc.source_id, left(cc.pmids, 24) AS pmids
    FROM compound_condition cc JOIN compound c USING (compound_id) JOIN condition k USING (condition_id)
    WHERE (c.name, k.name, cc.source_id) IN (('Piperine','Neoplasms','ctd'), ('Sodium','Hypertension','ctd'),
          ('Caffeine','Hypertension','duke'), ('Epigallocatechin gallate','Breast Neoplasms','exposome'))
    QUALIFY row_number() OVER (PARTITION BY c.name, k.name, cc.source_id ORDER BY cc.compound_id) = 1""")
EX["condition"] = rows("""SELECT condition_id, name, type, source_vocab FROM condition
    WHERE condition_id IN ('MESH:D009325', 'TCM:SMTS00755', 'ICD11:MD12', 'ACT:antiemetic', 'MESH:D006973')""")
EX["ingredient_condition"] = rows("""
    SELECT ic.ingredient_id, k.name AS condition, ic.direction, ic.evidence_type, ic.tradition, ic.n_pos, ic.n_neg, ic.source_id
    FROM ingredient_condition ic JOIN condition k USING (condition_id)
    WHERE (ic.ingredient_id, k.name, ic.source_id) IN (('ING:licorice','Hypertension','spicerx'),
          ('ING:licorice','Hypertension','imppat'), ('ING:ginger','Vomiting','symmap'), ('ING:clove','Nausea','unaprod'),
          ('ING:licorice','Hypokalemia','cmaup'))
    QUALIFY row_number() OVER (PARTITION BY ic.ingredient_id, k.name, ic.source_id ORDER BY ic.evidence_type) = 1""")
EX["ingredient_drug"] = rows("""
    SELECT DISTINCT idr.ingredient_id, d.name AS drug, idr.effect, idr.evidence_type, idr.pmid, idr.source_id
    FROM ingredient_drug idr JOIN drug d USING (drug_id)
    WHERE (idr.ingredient_id, d.name, idr.effect) IN (('ING:coconut','Warfarin','Harmful'), ('ING:honey','Warfarin','Harmful'),
          ('ING:grapefruit','Cyclosporine','Positive'), ('ING:licorice','Omeprazole','Negative'), ('ING:ginger','Warfarin','No Effect'))
    LIMIT 5""")
EX["drug"] = rows("""SELECT drug_id, name, drugbank_id FROM drug
    WHERE name IN ('Metformin','Cyclosporine','Omeprazole','Spironolactone','Tacrolimus') ORDER BY name""")

# supporting (grayed) tables: a few rows each, preferably ones this trace touches
EX["ingredient_alias"] = rows("""SELECT ingredient_id, alias, lang, alias_type FROM ingredient_alias
    WHERE ingredient_id = 'ING:turmeric' AND lang IN ('zh','ja','ko','fa','zh-Latn','la')
    QUALIFY row_number() OVER (PARTITION BY lang ORDER BY alias) = 1""")
EX["ingredient_xref"] = rows("""SELECT ingredient_id, db, xref_id FROM ingredient_xref WHERE ingredient_id = 'ING:turmeric'
    AND db IN ('foodb_food','spicerx','ddid_food','symmap','imppat','flavordb')
    QUALIFY row_number() OVER (PARTITION BY db ORDER BY xref_id) = 1""")
EX["ingredient_property"] = rows("""SELECT ingredient_id, system, property, value, source_id FROM ingredient_property
    WHERE ingredient_id IN ('ING:turmeric','ING:ginger','ING:saffron')
    QUALIFY row_number() OVER (PARTITION BY ingredient_id, system ORDER BY property) = 1 LIMIT 6""")
EX["compound_xref"] = rows("""SELECT compound_id, db, xref_id FROM compound_xref
    WHERE compound_id = 'IK:VFLDPWHFBUODDF-FCXRPNKRSA-N' AND db IN ('foodb','hmdb','npass','ctd','imppat','phenol_explorer')
    QUALIFY row_number() OVER (PARTITION BY db ORDER BY xref_id) = 1""")
EX["condition_alias"] = rows("""SELECT condition_id, alias, lang, source_id FROM condition_alias
    WHERE condition_id = 'MESH:D003924' QUALIFY row_number() OVER (PARTITION BY lang ORDER BY length(alias)) <= 2 LIMIT 6""")
EX["condition_relation"] = rows("""SELECT * FROM condition_relation
    WHERE (from_id = 'MESH:D003924' AND rel = 'is_a') OR (from_id = 'ACT:antiemetic') OR (rel = 'same_as' AND from_id = 'ICD11:MD12')""")
EX["drug_condition"] = rows("""SELECT dc.drug_id, d.name AS drug, c.name AS condition FROM drug_condition dc
    JOIN drug d USING (drug_id) JOIN condition c USING (condition_id) WHERE d.name IN ('Warfarin','Metformin') LIMIT 5""")
EX["evidence_type"] = rows("SELECT * FROM evidence_type ORDER BY rank")
EX["source"] = rows("""SELECT source_id, dataset_note, version, license FROM source
    WHERE source_id IN ('sfct','foodb','ctd','spicerx','ddid','manual')""")

TABLE_SQL = {  # breakdowns per table
    "dish": [("SELECT source_id, count(*) FROM dish GROUP BY 1", "by source"),
             ("SELECT coalesce(country_iso2, 'region only'), count(*) FROM dish GROUP BY 1", "by country")],
    "dish_ingredient": [("SELECT match_method, count(*) FROM dish_ingredient GROUP BY 1", "by match method"),
                        ("SELECT CASE WHEN grams IS NULL THEN 'no grams' ELSE 'with grams' END, count(*) FROM dish_ingredient GROUP BY 1", "amounts")],
    "dish_nutrient": [("SELECT source_id, count(*) FROM dish_nutrient GROUP BY 1", "by source")],
    "ingredient": [("SELECT coalesce(category, '—'), count(*) FROM ingredient GROUP BY 1", "by category"),
                   ("SELECT CASE WHEN ncbi_taxon_id IS NOT NULL THEN 'NCBI taxon' WHEN scientific_name IS NOT NULL THEN 'scientific name only' ELSE 'name only' END, count(*) FROM ingredient GROUP BY 1", "identity")],
    "ingredient_compound": [("SELECT source_id, count(*) FROM ingredient_compound GROUP BY 1", "by source"),
                            ("SELECT CASE WHEN mg_per_100g IS NULL THEN 'presence only' ELSE 'measured amount' END, count(*) FROM ingredient_compound GROUP BY 1", "amounts")],
    "compound": [("SELECT split_part(compound_id, ':', 1), count(*) FROM compound GROUP BY 1", "id type"),
                 ("SELECT CASE WHEN mesh_id IS NOT NULL THEN 'linked to CTD' ELSE 'not in CTD' END, count(*) FROM compound GROUP BY 1", "CTD link")],
    "compound_condition": [("SELECT source_id, count(*) FROM compound_condition GROUP BY 1", "by source"),
                           ("SELECT direction, count(*) FROM compound_condition GROUP BY 1", "by direction")],
    "condition": [("SELECT type, count(*) FROM condition GROUP BY 1", "by type"),
                  ("SELECT source_vocab, count(*) FROM condition GROUP BY 1", "by vocabulary")],
    "ingredient_condition": [("SELECT source_id, count(*) FROM ingredient_condition GROUP BY 1", "by source"),
                             ("SELECT evidence_type, count(*) FROM ingredient_condition GROUP BY 1", "by evidence")],
    "ingredient_drug": [("SELECT effect, count(*) FROM ingredient_drug GROUP BY 1", "by effect"),
                        ("SELECT source_id, count(*) FROM ingredient_drug GROUP BY 1", "by source")],
    "drug": [("SELECT CASE WHEN drugbank_id IS NOT NULL THEN 'DrugBank id' ELSE 'name only' END, count(*) FROM drug GROUP BY 1", "identity")],
    # grayed tables (not on the trace path)
    "source": [("SELECT CASE WHEN dataset_note IS NULL THEN 'curated maps' ELSE 'dataset' END, count(*) FROM source GROUP BY 1", "kind")],
    "evidence_type": [("SELECT rank || ' ' || code, 1 FROM evidence_type", "ranks")],
    "ingredient_alias": [("SELECT lang, count(*) FROM ingredient_alias GROUP BY 1", "by language")],
    "ingredient_xref": [("SELECT db, count(*) FROM ingredient_xref GROUP BY 1", "by database")],
    "ingredient_property": [("SELECT system, count(*) FROM ingredient_property GROUP BY 1", "by system")],
    "compound_xref": [("SELECT db, count(*) FROM compound_xref GROUP BY 1", "by database")],
    "condition_alias": [("SELECT CASE WHEN lang = 'xref' THEN 'id cross-reference' ELSE 'text (' || lang || ')' END, count(*) FROM condition_alias GROUP BY 1", "kind")],
    "condition_relation": [("SELECT rel, count(*) FROM condition_relation GROUP BY 1", "by relation")],
    "drug_condition": [("SELECT source_id, count(*) FROM drug_condition GROUP BY 1", "by source")],
}
GRAY = ["source", "evidence_type", "ingredient_alias", "ingredient_xref", "ingredient_property", "compound_xref",
        "condition_alias", "condition_relation", "drug_condition"]

SOURCES_OF = {  # which source_ids feed each table (from the build); used for the dataset badges
    t: [r[0] for r in con.execute(f"SELECT DISTINCT source_id FROM {t} WHERE source_id IS NOT NULL").fetchall()]
    for t in ["dish", "dish_ingredient", "dish_nutrient", "ingredient_compound", "compound_condition",
              "ingredient_condition", "ingredient_drug", "drug_condition"]}
SOURCE_ROWS = {
    t: {r[0]: int(r[1]) for r in con.execute(f"SELECT source_id, count(*) FROM {t} GROUP BY 1").fetchall()}
    for t in SOURCES_OF}
# entity tables: contributions from xrefs / vocabularies
XREF2SRC = {"foodb_food": "foodb", "flavordb": "flavordb", "culinarydb": "culinarydb", "indicrecipenutri": "indicrecipenutri",
            "symmap": "symmap", "herb": "herb", "tmmc": "tmmc", "imppat": "imppat", "cmaup": "cmaup", "npass": "npass",
            "ddid_food": "ddid", "ddid_herb": "ddid", "spicerx": "spicerx", "unaprod": "unaprod", "duke": "duke",
            "knapsack": "knapsack", "foodb": "foodb", "hmdb": "hmdb", "phenol_explorer": "phenol", "ctd": "ctd"}
ing_src = {}
for db, n in con.execute("SELECT db, count(DISTINCT ingredient_id) FROM ingredient_xref GROUP BY 1").fetchall():
    if db in XREF2SRC:
        s = XREF2SRC[db]
        ing_src[s] = max(ing_src.get(s, 0), int(n))
cmp_src = {}
for db, n in con.execute("SELECT db, count(DISTINCT compound_id) FROM compound_xref GROUP BY 1").fetchall():
    if db in XREF2SRC:
        cmp_src[XREF2SRC[db]] = int(n)
cond_src = {"medic" if v == "medic" else v: int(n) for v, n in
            con.execute("SELECT source_vocab, count(*) FROM condition GROUP BY 1").fetchall()}
cond_src = {{"action_map": "manual", "icd11": "cmaup"}.get(k, k): v for k, v in cond_src.items()}
drug_src = {"ddid": one("SELECT count(*) FROM drug")}
SOURCE_ROWS.update({"ingredient": ing_src, "compound": cmp_src, "condition": cond_src, "drug": drug_src})
SOURCES_OF.update({t: list(v) for t, v in [("ingredient", ing_src), ("compound", cmp_src), ("condition", cond_src),
                                            ("drug", drug_src)]})

tables = {}
for t, specs in TABLE_SQL.items():
    tables[t] = {
        "count": one(f"SELECT count(*) FROM {t}"),
        "columns": [r[0] for r in con.execute(f"DESCRIBE {t}").fetchall()],
        "breakdowns": [breakdown(sql, label) for sql, label in specs],
        "examples": EX.get(t, []),
        "trace": T.get(t, []),
        "sources": dict(sorted(SOURCE_ROWS.get(t, {}).items(), key=lambda kv: -kv[1])),
        "gray": t in GRAY,
    }
if content:
    for t, meta in getattr(content, "TABLES", {}).items():
        if t in tables:
            tables[t].update({k: v for k, v in meta.items() if k in ("title", "role", "why")})

sources = {r["source_id"]: r for r in rows("SELECT source_id, dataset_note, name, version, license FROM source")}
datasets = {}
for sid, s in sources.items():
    c = (getattr(content, "DATASETS", {}) or {}).get(sid, {}) if content else {}
    datasets[sid] = {"name": c.get("name") or s["name"], "note": c.get("note") or s["dataset_note"],
                     "what": c.get("what", ""), "origin": c.get("origin", s["version"] or ""),
                     "access": c.get("access", ""), "license": s["license"], "tables": c.get("tables", {})}

# ---------------------------------------------------------------------------------------------------------------
# The trace graph. `key` = column that carries the path to the next node; `in` = column matched from the previous.
NODES = [
    {"id": "dish", "table": "dish", "x": 0, "y": 330, "in": None, "key": ["dish_id"],
     "show": ["dish_id", "name", "country_iso2", "subregion", "servings", "source_id"],
     "caption": "The patient's dish: a lab-analysed Saudi recipe"},
    {"id": "dish_ingredient", "table": "dish_ingredient", "x": 460, "y": 330, "in": ["dish_id"], "key": ["ingredient_id"],
     "show": ["dish_id", "raw_text", "grams", "match_method", "match_score", "ingredient_id"],
     "caption": "One of 20 recipe lines: 5 g ground turmeric"},
    {"id": "ingredient", "table": "ingredient", "x": 920, "y": 330, "in": ["ingredient_id"], "key": ["ingredient_id"],
     "show": ["ingredient_id", "canonical_name", "scientific_name", "ncbi_taxon_id", "foodon_id", "category"],
     "caption": "Canonical turmeric, known to 20 databases"},
    {"id": "ingredient_compound", "table": "ingredient_compound", "x": 1380, "y": 0, "in": ["ingredient_id"],
     "key": ["compound_id"], "show": ["ingredient_id", "compound_id", "mg_per_100g", "evidence_type", "source_id"],
     "caption": "Turmeric contains curcumin, measured"},
    {"id": "compound", "table": "compound", "x": 1840, "y": 0, "in": ["compound_id"], "key": ["compound_id"],
     "show": ["compound_id", "name", "pubchem_cid", "mesh_id"], "caption": "Curcumin, merged from 11 sources"},
    {"id": "compound_condition", "table": "compound_condition", "x": 2300, "y": 0, "in": ["compound_id"],
     "key": ["condition_id"], "show": ["compound_id", "condition_id", "direction", "evidence_type", "source_id", "pmids"],
     "caption": "CTD: curcumin studied as a T2D treatment"},
    {"id": "ingredient_condition", "table": "ingredient_condition", "x": 1380, "y": 460, "in": ["ingredient_id"],
     "key": ["condition_id"], "show": ["ingredient_id", "condition_id", "direction", "evidence_type", "tradition",
                                       "n_pos", "n_neg", "source_id"],
     "caption": "Direct claims: literature mining and Ayurveda"},
    {"id": "condition", "table": "condition", "x": 2760, "y": 300, "in": ["condition_id"], "key": [],
     "show": ["condition_id", "name", "type", "mesh_tree"], "caption": "The patient's condition, and its parent"},
    {"id": "ingredient_drug", "table": "ingredient_drug", "x": 1380, "y": 980, "in": ["ingredient_id"], "key": ["drug_id"],
     "show": ["ingredient_id", "drug_id", "effect", "evidence_type", "pmid", "source_id"],
     "caption": "Food–drug check · source label needs verifying"},
    {"id": "drug", "table": "drug", "x": 1840, "y": 980, "in": ["drug_id"], "key": [],
     "show": ["drug_id", "name", "drugbank_id"], "caption": "Warfarin (anticoagulant)"},
    {"id": "dish_nutrient", "table": "dish_nutrient", "x": 460, "y": 760, "in": ["dish_id"], "key": [],
     "show": ["dish_id", "nutrient", "amount_per_100g", "unit"], "caption": "Lab values of the whole cooked dish"},
]

S = {  # code excerpts shown on the arrows (trimmed, with file references)
    "match": '''# db/build/resolve_ingredients.py · IngredientResolver.by_text
raw = unicodedata.normalize("NFKC", text).lower().strip()
hit = self._lookup(self.exact, raw, lang)          # 1. exact alias
# 2. normalised alias: norm_text("Ground turmeric") -> "turmeric"
# 3. rapidfuzz token_sort_ratio >= 90 within the language
# 4. db/maps/ingredient_map_manual.csv (849 zh/ja/en strings)
-> ("ING:turmeric", "normalised", 0.92)''',
    "foodb": '''-- db/build/links_compounds.py · FooDB Content
SELECT f.v AS ingredient_id, c.v AS compound_id, fc.amount, fc.unit, …,
  CASE WHEN fc.citation_type IN ('DATABASE','EXPERIMENTAL','ARTICLE','TEXTBOOK')
       THEN 'curated_literature' … ELSE 'predicted' END
FROM fc JOIN lk_ffood f ON f.k = fc.food_id        -- by_xref('foodb_food', 68)
        JOIN lk_fcmp  c ON c.k = fc.source_id      -- by_xref('foodb', compound id)
WHERE NOT (fc.amount IS NULL AND fc.citation_type IN ('PREDICTED','UNKNOWN'))''',
    "merge": '''# db/build/compounds.py · union–find merge of 395,833 candidates
1. same InChIKey                      -> merge
2. same PubChem CID (no InChIKey conflict)
3. explicit cross-ids (HMDB.foodb_id, NPASS/CMAUP np_id, …)
4. same CAS (check digit valid)
compound_id = 'IK:' || inchikey  ->  IK:VFLDPWHFBUODDF-FCXRPNKRSA-N''',
    "ctd": '''# db/build/links_conditions.py · CTD curated chemical–disease
own = cr.by_mesh(m)                 # MESH:D003474 -> Curcumin
for c in cr.all_by_mesh(m):         # stereo / tautomer variants in food paths
    ...
SELECT c.compound_id, d.v,
  CASE WHEN ctd.de = 'therapeutic' THEN 'beneficial' ELSE 'marker' END,
  'curated_literature', 'ctd', ctd.pm, c.score
FROM ctd JOIN lk_ctd_c c USING (mesh) JOIN lk_ctd_d d ON d.k = ctd.did''',
    "medic": '''-- condition ids are MEDIC DiseaseIDs (Data/ctd/CTD_diseases.tsv.gz)
MESH:D003924  Diabetes Mellitus, Type 2   tree C18.452.394.750.149 …
  is_a -> MESH:D003920  Diabetes Mellitus  (from ParentIDs)
type = 'symptom' only for C23.888 (Signs and Symptoms)''',
    "spicerx": '''# db/build/links_ingredients.py · SpiceRx
ing  = ir.by_xref("spicerx", r.tax_id)       # 136217 -> ING:turmeric
cond = kr.by_mesh(r.mesh_id)                 # D003920 -> Diabetes Mellitus
p, n = int(r.n_positive), int(r.n_negative)  # 45, 0
direction = "beneficial" if p > n else "harmful" if n > p else "association"''',
    "isa": '''-- db/trace.py · expand_condition(): the query term, narrower terms,
-- and its direct parents (traditional sources say just "diabetes")
SELECT to_id FROM condition_relation
WHERE rel = 'is_a' AND from_id = 'MESH:D003924'   -- -> MESH:D003920''',
    "ddid": '''# db/build/links_drugs.py · DDID interactions
ing  = ir.by_xref("ddid_food", "F00015")      # -> ING:turmeric
drug = fhdi.get(r["Drug_ID"])                 # -> DB:DB00682 Warfarin
eff  = r["Effect"]                            # "Possible"
ev   = "curated_literature" if pm else "predicted"''',
    "nutrient": '''-- db/views.sql · a lab nutrient counts only when "high" (UK FSA, per 100 g)
('MESH:D012964','sodium', 600.0), ('MESH:D000073417','sugars', 22500.0), …
-- Timman Rice: sodium 162 mg < 600  ->  no high-sodium flag''',
    "dish": '''-- dish lines share the dish id
SELECT * FROM dish_ingredient WHERE dish_id = 'sfct:68'   -- 20 lines, all with grams''',
    "drugid": '''-- drug ids are DrugBank ids carried by DDID
SELECT * FROM drug WHERE drug_id = 'DB:DB00682'   -- Warfarin''',
}

EDGES = [
    {"from": "dish", "to": "dish_ingredient", "col": "dish_id", "label": "dish_id",
     "bullets": ["Recipe lines carry the dish id of their dish", "Saudi table: 1,154 lines for 130 dishes; Timman Rice has 20",
                 "Quantities parsed from text (\"5 g\") into grams"], "code": S["dish"]},
    {"from": "dish_ingredient", "to": "ingredient", "col": "ingredient_id", "label": "ingredient_id",
     "bullets": ["Free-text line \"Ground turmeric\" matched to a canonical ingredient",
                 "Resolver order: exact alias → normalised text → fuzzy → manual map",
                 "Here: descriptor \"ground\" stripped, normalised match, score 0.92",
                 "97.8% of all 482k lines are matched"], "code": S["match"]},
    {"from": "ingredient", "to": "ingredient_compound", "col": "ingredient_id", "label": "ingredient_id",
     "bullets": ["Turmeric's FooDB food id (FOOD00068) and taxon link it to composition data",
                 "Phenol-Explorer: curcumin 2,213.57 mg/100 g dried turmeric (measured)",
                 "FooDB mg_per_100g 2,507 = median of its sources (Duke 2,800; Phenol-Explorer 2,214)",
                 "Predicted FooDB rows without an amount are dropped"], "code": S["foodb"]},
    {"from": "ingredient_compound", "to": "compound", "col": "compound_id", "label": "compound_id",
     "bullets": ["Compounds from 11 sources merged by InChIKey, then CID, cross-ids, CAS",
                 "Curcumin's id is its InChIKey: IK:VFLDPWHFBUODDF-FCXRPNKRSA-N",
                 "The merge also gives it CTD's MeSH id D003474"], "code": S["merge"]},
    {"from": "compound", "to": "compound_condition", "col": "compound_id", "label": "compound_id",
     "bullets": ["CTD lists chemicals by MeSH id; resolver maps MESH:D003474 → curcumin",
                 "CTD 'therapeutic' → beneficial; 'marker/mechanism' → marker",
                 "Evidence: curated literature (mostly lab / animal studies)"], "code": S["ctd"]},
    {"from": "compound_condition", "to": "condition", "col": "condition_id", "label": "condition_id",
     "bullets": ["Condition ids are MEDIC (MeSH/OMIM) ids, as used by CTD",
                 "MESH:D003924 Diabetes Mellitus, Type 2 — the patient's condition",
                 "MeSH tree gives the hierarchy (is_a → Diabetes Mellitus)"], "code": S["medic"]},
    {"from": "ingredient", "to": "ingredient_condition", "col": "ingredient_id", "label": "ingredient_id",
     "bullets": ["Direct ingredient → condition claims, no compound needed",
                 "SpiceRx joins by NCBI taxon 136217; IMPPAT by plant id",
                 "Direction from paper counts: 45 positive vs 0 negative → beneficial"], "code": S["spicerx"]},
    {"from": "ingredient_condition", "to": "condition", "col": "condition_id", "label": "is_a",
     "bullets": ["These sources say just \"diabetes\" (MESH:D003920)",
                 "Query expansion adds the direct parent of the patient's T2D",
                 "So traditional and text-mined claims reach the patient's condition"], "code": S["isa"]},
    {"from": "ingredient", "to": "ingredient_drug", "col": "ingredient_id", "label": "ingredient_id",
     "bullets": ["DDID food id F00015 (\"Turmeric\") was mapped to turmeric at build time",
                 "⚠ The underlying study used Curcuma xanthorrhiza (Javanese turmeric) in rats, not C. longa",
                 "Provenance at every hop is what makes this visible",
                 f"Warfarin has DDID records with {trace_extra['warfarin_ing']} ingredients in the DB"], "code": S["ddid"]},
    {"from": "ingredient_drug", "to": "drug", "col": "drug_id", "label": "drug_id",
     "bullets": ["DrugBank id DB00682 identifies warfarin",
                 "Effect 'Possible': higher doses of C. xanthorrhiza extract raised warfarin exposure (AUC) in rats",
                 "PMID 34062109 · evidence for culinary C. longa is not shown by this record"],
     "code": S["drugid"]},
    {"from": "dish", "to": "dish_nutrient", "col": "dish_id", "label": "dish_id",
     "bullets": ["Only composition tables have lab values for whole dishes",
                 "Sodium 162 mg/100 g: below the FSA 'high' line (600)",
                 "Sugars 0 g; vitamin K₁ 5.6 µg (relevant for warfarin)"], "code": S["nutrient"]},
]

PATIENT = {  # a fictional, illustrative patient
    "name": "Fatimah, 58", "place": "Hail, Saudi Arabia",
    "facts": ["Type 2 diabetes", "Atrial fibrillation → on warfarin", "Eats Timman Rice every week"],
    "question": "Is my Timman Rice OK? Does anything in it matter for my diabetes or my medicine?",
}
OUTCOME = [
    {"tone": "good", "text": "Dish fits a T2D diet: sugars 0 g, sodium 162 mg per 100 g (lab-measured)", "grade": "measured"},
    {"tone": "good", "text": "Turmeric (5 g ≈ 125 mg curcumin): curcumin studied as T2D treatment",
     "grade": "curated · lab/animal"},
    {"tone": "good", "text": "Turmeric for diabetes: 45 supporting papers, 0 against; Ayurvedic use",
     "grade": "text-mined · traditional"},
    {"tone": "warn", "text": "Warfarin: DDID flags turmeric as 'Possible', but the study is Javanese turmeric (C. xanthorrhiza) in rats → verify before advising",
     "grade": "curated · rat study · PMID 34062109 · data-quality flag"},
    {"tone": "info", "text": "Vitamin K₁ only 5.6 µg per 100 g: no concern for warfarin", "grade": "measured"},
]
CAVEATS = [
    ("Status", ["Proof of concept: shows that the sources can be joined and traced end to end",
                "Not validated against clinical guidelines or expert review",
                "Outputs illustrate the reasoning an agent could show, not advice to a patient"]),
    ("Evidence", ["CTD links are mostly lab and animal studies; 'therapeutic' ≠ proven in humans",
                  "Traditional claims stored as stated, with the tradition named; not validated",
                  "Conflicts kept side by side (e.g. licorice & hypertension: Ayurveda vs 57 negative papers)"]),
    ("Ranking", ["Salience and dose-aware scores are transparent heuristics, not validated",
                 "Sodium → hypertension is a CTD 'marker', not flagged 'harmful'"]),
    ("Data", ["Source labels can be wrong: DDID files a C. xanthorrhiza (rat) study under 'Turmeric'",
              "Some nutrient mappings are wrong (unsaturated fat → 'Formic acid' via MeSH D005231)",
              "Some free-text matches are too specific (e.g. 'breast cancer' → 'Breast Cancer, Familial')",
              "Grams approximate (density 1; pieces have no grams); default weights for 'a pinch'",
              "Compound merge: stereo variants share MeSH ids; a few wrong CAS merges from FooDB",
              "FooDB content is 64% predicted; only rows with amounts are used"]),
    ("Coverage", ["Lab-measured dish nutrients only for Saudi, Bahrain, Kyrgyz and INDB tables",
                  "SymMap, HERB, SpiceRx, UNaProd, KNApSAcK are local samples",
                  "FoodAtlas, RecipeDB2, GRAYU, DrugBank pending access requests",
                  "No local TCM-symptom → modern-symptom mapping"]),
    ("Use", ["Several licences are non-commercial; CTD requires notification",
             "GRAYU excluded (terms forbid medical advice); NII Cookpad forbids external LLMs",
             "A decision-support aid, not medical advice"]),
]

data = {
    "built": str(datetime.date.today()),
    "totals": {"dishes": one("SELECT count(*) FROM dish"), "ingredients": one("SELECT count(*) FROM ingredient"),
               "compounds": one("SELECT count(*) FROM compound"), "conditions": one("SELECT count(*) FROM condition"),
               "drugs": one("SELECT count(*) FROM drug"),
               "datasets": one("SELECT count(DISTINCT dataset_note) FROM source WHERE dataset_note IS NOT NULL")},
    "poc": {"label": "Proof of concept",
            "note": "Illustrative case · real database rows · not medical advice"},
    "patient": PATIENT, "outcome": OUTCOME, "caveats": [{"title": t, "items": i} for t, i in CAVEATS],
    "nodes": NODES, "edges": EDGES, "tables": tables, "gray": GRAY, "datasets": datasets, "trace_extra": trace_extra,
}

out_json = os.path.join(HERE, "data.json")
json.dump(data, open(out_json, "w"), ensure_ascii=False, indent=1, default=str)
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
payload = json.dumps(data, ensure_ascii=False, default=str).replace("</", "<\\/")
fragment = tpl.replace("/*__DATA__*/null", payload)
open(os.path.join(HERE, "artifact.html"), "w", encoding="utf-8").write(fragment)
os.makedirs(os.path.join(VAULT, "Database", "presentation"), exist_ok=True)
page = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n</head>\n<body>\n'
        + fragment + "\n</body>\n</html>\n")
open(os.path.join(VAULT, "Database", "presentation", "index.html"), "w", encoding="utf-8").write(page)
print(f"data.json {os.path.getsize(out_json) / 1e3:.0f} kB · datasets with curated text: "
      f"{sum(1 for d in datasets.values() if d['tables'])}/{len(datasets)} · wrote Database/presentation/index.html")
