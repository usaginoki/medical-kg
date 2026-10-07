"""Export the unified database as three flat tables (one row per dish / ingredient / claim).

Usage:
  uv run db/export.py                # reads db/unified.duckdb (or $UNIFIED_DB), writes db/export/

  dishes       one row per dish: culture labels, recipe text, its ingredient lines and lab-measured nutrients
  ingredients  one row per canonical ingredient: names, ids in other databases, cultural properties, compounds
  effects      one row per claim: ingredient → condition (direct, or via a compound) and ingredient × drug

The tables join on `ingredient_id`. Nested columns (lists of structs) are kept in the Parquet files; the CSV files
hold the same data with nested columns as JSON strings. Nothing is added or dropped relative to the database:
`effects` has every path of v_ingredient_condition_all plus every ingredient_drug row, and flags the
characteristic ("salient") paths with the rule of views.sql.
"""
import os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DB_PATH  # noqa: E402

import duckdb

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "export")

DISHES = """
SELECT d.dish_id,
       s.dataset_note                       AS source,
       d.name, d.name_local, d.lang,
       d.country_iso2, d.subregion, d.cuisine_label,
       d.servings,
       d.steps_text                          AS recipe_text,
       d.has_amounts,
       (SELECT list({'raw_text': di.raw_text, 'ingredient_id': di.ingredient_id, 'ingredient': i.canonical_name,
                     'quantity': di.quantity, 'unit': di.unit, 'grams': di.grams,
                     'match_method': di.match_method, 'match_score': di.match_score})
        FROM dish_ingredient di LEFT JOIN ingredient i USING (ingredient_id)
        WHERE di.dish_id = d.dish_id)        AS ingredients,
       (SELECT list({'nutrient': c.name, 'compound_id': dn.nutrient_compound_id,
                     'amount_per_100g': dn.amount_per_100g, 'unit': dn.unit})
        FROM dish_nutrient dn LEFT JOIN compound c ON c.compound_id = dn.nutrient_compound_id
        WHERE dn.dish_id = d.dish_id)        AS nutrients_per_100g,
       s.license
FROM dish d
LEFT JOIN source s USING (source_id)
ORDER BY d.dish_id
"""

INGREDIENTS = """
SELECT i.ingredient_id, i.canonical_name, i.category, i.scientific_name, i.ncbi_taxon_id, i.foodon_id, i.is_herb,
       (SELECT list({'name': a.alias, 'lang': a.lang, 'type': a.alias_type, 'source': a.source_id})
        FROM ingredient_alias a WHERE a.ingredient_id = i.ingredient_id)     AS names,
       (SELECT list({'db': x.db, 'id': x.xref_id})
        FROM ingredient_xref x WHERE x.ingredient_id = i.ingredient_id)      AS xrefs,
       (SELECT list({'system': p.system, 'property': p.property, 'value': p.value, 'source': p.source_id})
        FROM ingredient_property p WHERE p.ingredient_id = i.ingredient_id)  AS cultural_properties,
       (SELECT list({'compound_id': ic.compound_id, 'compound': c.name, 'amount': ic.amount, 'unit': ic.unit,
                     'mg_per_100g': ic.mg_per_100g, 'plant_part': ic.plant_part,
                     'evidence_type': ic.evidence_type, 'source': ic.source_id, 'citation': ic.citation}
                    ORDER BY ic.mg_per_100g DESC NULLS LAST)
        FROM ingredient_compound ic LEFT JOIN compound c USING (compound_id)
        WHERE ic.ingredient_id = i.ingredient_id)                            AS compounds
FROM ingredient i
ORDER BY i.ingredient_id
"""

EFFECTS = """
WITH paths AS (
  SELECT v.*,
         coalesce(v.path_kind = 'direct'
                  OR (v.compound_mg_per_100g >= 1
                      AND (cp.n_ingredients <= 20 OR v.compound_mg_per_100g >= 0.1 * cp.max_mg_per_100g)),
                  false) AS characteristic  -- no measured amount → not characteristic
  FROM v_ingredient_condition_all v
  LEFT JOIN compound_profile cp USING (compound_id)
)
SELECT p.ingredient_id, i.canonical_name AS ingredient,
       'condition'             AS target_type,
       p.condition_id          AS target_id,
       c.name                  AS target,
       c.type                  AS target_kind,
       p.direction,
       NULL::VARCHAR           AS drug_effect,
       p.evidence_type, p.evidence_rank,
       p.path_kind             AS path,
       p.compound_id           AS via_compound_id,
       cpd.name                AS via_compound,
       p.compound_mg_per_100g,
       p.link_source           AS source,
       p.content_source        AS compound_amount_source,
       p.tradition,
       NULL::VARCHAR           AS mechanism,
       p.pmids,
       p.note,
       p.characteristic
FROM paths p
LEFT JOIN ingredient i USING (ingredient_id)
LEFT JOIN condition c USING (condition_id)
LEFT JOIN compound cpd ON cpd.compound_id = p.compound_id
UNION ALL
SELECT idr.ingredient_id, i.canonical_name,
       'drug', idr.drug_id, dr.name, 'drug',
       NULL, idr.effect,
       idr.evidence_type, e.rank,
       'drug_interaction',
       NULL, NULL, NULL,
       idr.source_id, NULL, NULL,
       idr.mechanism, idr.pmid, idr.note,
       true
FROM ingredient_drug idr
LEFT JOIN ingredient i USING (ingredient_id)
LEFT JOIN drug dr USING (drug_id)
LEFT JOIN evidence_type e ON e.code = idr.evidence_type
"""


def add_bom(src, dst):
    """UTF-8 byte-order mark first, so Excel/Numbers read the CSV as UTF-8 (Japanese, Chinese, Arabic text)."""
    import shutil
    with open(dst, "wb") as fo, open(src, "rb") as fi:
        fo.write(b"\xef\xbb\xbf")
        shutil.copyfileobj(fi, fo, 1 << 24)
    os.remove(src)


def main():
    os.makedirs(OUT, exist_ok=True)
    con = duckdb.connect(DB_PATH, read_only=True)
    for name, sql in [("dishes", DISHES), ("ingredients", INGREDIENTS), ("effects", EFFECTS)]:
        t = time.time()
        con.execute(f"CREATE OR REPLACE TEMP TABLE t_{name} AS {sql}")
        n = con.execute(f"SELECT count(*) FROM t_{name}").fetchone()[0]
        con.execute(f"COPY t_{name} TO '{OUT}/{name}.parquet' (FORMAT parquet, COMPRESSION zstd)")
        nested = [c for c, typ in con.execute(f"SELECT column_name, column_type FROM (DESCRIBE t_{name})").fetchall()
                  if typ.endswith("[]")]
        cols = ", ".join(f"to_json({c}) AS {c}" if c in nested else c
                         for c, in con.execute(f"SELECT column_name FROM (DESCRIBE t_{name})").fetchall())
        con.execute(f"COPY (SELECT {cols} FROM t_{name}) TO '{OUT}/{name}.csv.tmp' (HEADER)")
        add_bom(f"{OUT}/{name}.csv.tmp", f"{OUT}/{name}.csv")
        mb = sum(os.path.getsize(f"{OUT}/{name}.{x}") for x in ("parquet", "csv")) / 1e6
        print(f"{name}: {n:,} rows ({time.time() - t:.0f}s, {mb:,.0f} MB)", flush=True)
    print(f"written to {OUT}/")


if __name__ == "__main__":
    main()
