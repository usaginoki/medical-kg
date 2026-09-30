"""Build the unified dish ↔ condition database (DuckDB).

Usage:
  uv run db/build.py                 # full rebuild into db/unified.duckdb (or $UNIFIED_DB)
  uv run db/build.py --only conditions compounds   # run selected stages on an existing file

Stages run in dependency order. Each stage is a module in db/build/ exposing `build(con)`; a stage must be
idempotent (it deletes the rows it owns before inserting). See db/README.md for the contract between stages.
"""
import argparse, importlib, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DB_PATH, connect, init_schema  # noqa: E402

STAGES = [
    "sources",       # source registry
    "conditions",    # condition, condition_alias, condition_relation (MEDIC, SymMap, HERB vocab, action map)
    "compounds",     # compound, compound_xref (CTD, FooDB, HMDB, NPASS/CMAUP, Phenol-Explorer, FlavorDB, nutrients)
    "ingredients",   # ingredient, ingredient_alias, ingredient_xref, ingredient_property
    "dishes",        # dish, dish_ingredient, dish_nutrient
    "links",         # ingredient_compound, compound_condition, ingredient_condition, drug*, ingredient_drug
    "views",         # db/views.sql
    "report",        # db/build_report.md
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*", choices=STAGES)
    ap.add_argument("--fresh", action="store_true", help="delete the DB file first")
    a = ap.parse_args()
    if a.fresh and os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    con = connect()
    init_schema(con)
    for stage in a.only or STAGES:
        t = time.time()
        importlib.import_module(f"build.{stage}").build(con)
        print(f"[{stage}] done in {time.time() - t:.1f}s", flush=True)
    con.close()
    print(f"database: {DB_PATH}")


if __name__ == "__main__":
    main()
