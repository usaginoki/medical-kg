"""Stage `llm`: load the stored LLM results (db/llm/store.py -> db/export/llm/*.parquet) into tables of the same
names. The stage owns the llm_* tables and nothing else: the graph tables are not changed. Missing files are skipped
(the full LLM pass is optional and its files are git-ignored)."""
import os

from common import DB_DIR

TABLES = ["llm_case_tags", "llm_case_facts", "llm_ingredient_lines", "llm_condition_terms", "llm_dishes"]


def build(con):
    for t in TABLES:
        path = os.path.join(DB_DIR, "export", "llm", f"{t}.parquet")
        con.execute(f"DROP TABLE IF EXISTS {t}")
        if os.path.exists(path):
            con.execute(f"CREATE TABLE {t} AS SELECT * FROM read_parquet(?)", [path])
            print(f"  {t}: {con.execute(f'SELECT count(*) FROM {t}').fetchone()[0]:,} rows")
        else:
            print(f"  {t}: no {os.path.relpath(path)} (uv run db/llm/store.py)")
