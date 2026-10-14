"""Write the full-pass LLM answers (from the cache, see db/llm/full_pass.py) as separate tables in db/export/llm/.

  uv run db/llm/store.py [w1 w2 ...]      # default: every workflow that has items; then `uv run db/build.py --only llm`

The tables sit next to the graph and the case table; nothing in the graph uses them yet (see the GitHub issue on
storing LLM results). Every row carries model, prompt_version and stored_at.

  llm_case_tags         case_id, culture_reason, culture_role, diet_relevant, graph_answerable, cues[]      (W1)
  llm_case_facts        case_id, demographics, place, symptoms, history, diagnosis, foods[], drugs, linked ids   (W2)
  llm_ingredient_lines  distinct weak / unmatched recipe line, current match, LLM kind, name, choice, final id    (W3)
  llm_condition_terms   source term, current ids (none), LLM kind, meaning, conditions[] with condition_id         (W4)
  llm_dishes            dish_id, stored country, LLM kind, clean English name, cuisine country, style              (W5)

db/export/ is git-ignored: case texts and answers of some datasets must not be redistributed.
"""
import datetime, json, os, sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "build"))
from client import LLM  # noqa: E402
from export import OUT  # noqa: E402
from full_pass import FULL, TASKS  # noqa: E402
from w1_run import load  # noqa: E402

DEST = f"{OUT}/llm"
TODAY = datetime.date.today().isoformat()


def answers(w):
    """[(item record, answer dict or None)] for a workflow, read from the cache."""
    t = TASKS[w]
    llm = LLM(t["model"])
    out = []
    for it in load(f"{FULL}/{w}.jsonl"):
        row = llm.get(llm.key(t["version"], t["system"], it["text"], t["schema"]))
        out.append((it, json.loads(row[0]) if row else None))
    return out


def prov(w):
    return {"model": TASKS[w]["model"], "prompt_version": TASKS[w]["version"], "stored_at": TODAY}


def write(name, rows):
    os.makedirs(DEST, exist_ok=True)
    df = pd.DataFrame(rows)
    df.to_parquet(f"{DEST}/{name}.parquet", index=False)
    print(f"{name}: {len(df):,} rows -> {os.path.relpath(DEST)}/{name}.parquet")
    return df


def resolvers():
    import duckdb
    from common import DB_PATH
    from resolve import ConditionResolver, IngredientResolver
    con = duckdb.connect(DB_PATH, read_only=True)
    dishes = {}
    for did, name, local in con.sql("SELECT dish_id, lower(name), lower(name_local) FROM dish").fetchall():
        for n in (name, local):
            if n:
                dishes.setdefault(n.strip(), []).append(did)
    return con, ConditionResolver(con), IngredientResolver(con), dishes


def case_tags():
    rows = []
    for it, a in answers("w1"):
        if a is None:
            continue
        rows.append({"case_id": it["item_id"], "culture_reason": a["culture_reason"], "culture_role": a["culture_role"],
                     "diet_relevant": a["diet_relevant"], "graph_answerable": a["graph_answerable"], "cues": a["cues"],
                     **prov("w1")})
    write("llm_case_tags", rows)


def case_facts():
    con, cr, ir, dishes = resolvers()
    rows = []
    cid = lambda x: cr.by_text(x) if x else None  # noqa: E731
    for it, a in answers("w2"):
        if a is None:
            continue
        foods = []
        for f in a["foods"]:
            hit = ir.by_text(f["name_en"], "en", fuzzy=False)
            ids = dishes.get(f["name_en"].lower().strip(), [])[:5] + dishes.get(f["original"].lower().strip(), [])[:5]
            foods.append({**f, "ingredient_id": hit[0] if hit else None, "dish_ids": list(dict.fromkeys(ids))})
        rows.append({"case_id": it["item_id"], **{k: a[k] for k in ("age_years", "sex", "country", "region_or_city",
                                                                    "ethnicity", "religious_practices", "symptoms",
                                                                    "history", "diagnosis_en", "drugs")},
                     "foods": foods, "diagnosis_condition_id": cid(a["diagnosis_en"]),
                     "symptom_condition_ids": [c for c in map(cid, a["symptoms"]) if c],
                     "history_condition_ids": [c for c in map(cid, a["history"]) if c], **prov("w2")})
    write("llm_case_facts", rows)


def ingredient_lines():
    import duckdb
    from common import DB_PATH
    from resolve import IngredientResolver
    ir = IngredientResolver(duckdb.connect(DB_PATH, read_only=True))
    rows = []
    for it, a in answers("w3"):
        m = it["meta"]
        if a is None:
            continue
        final = a["choice"] if a["choice"] in m["candidates"] else None
        if final is None and a["kind"] in ("ingredient", "several_ingredients") and a["name_en"]:
            g = ir.by_text(a["name_en"], "en", fuzzy=False)
            final = g[0] if g and g[1] in ("exact", "normalised", "manual") else None
        rows.append({"raw_text": m["raw_text"], "lang": m["lang"], "source_id": m["source_id"], "lines": m["lines"],
                     "current_ingredient_id": m["ingredient_id"], "current_method": m["match_method"],
                     "current_score": m["match_score"], "kind": a["kind"], "name_en": a["name_en"],
                     "choice": a["choice"], "fit": a["fit"], "llm_ingredient_id": final,
                     "agrees": final == m["ingredient_id"], **prov("w3")})
    write("llm_ingredient_lines", rows)


def condition_terms():
    from w4_condition_terms import ground, resolver
    _, cr, _ = resolver()
    rows = []
    for it, a in answers("w4"):
        m = it["meta"]
        if a is None:
            continue
        ids = ground(cr, [c["name"] for c in a["conditions"]])
        rows.append({"source": m["source"], "term": m["term"], "rows": m["rows"], "kind": a["kind"],
                     "meaning": a["meaning"], "evidence_level": a["evidence_level"],
                     "conditions": [{**c, "condition_id": i} for c, i in zip(a["conditions"], ids)], **prov("w4")})
    write("llm_condition_terms", rows)


def dishes():
    rows = []
    for it, a in answers("w5"):
        m = it["meta"]
        if a is None:
            continue
        rows.append({"dish_id": m["dish_id"], "source_id": m["source_id"], "stored_country": m["country_iso2"],
                     "kind": a["kind"], "name_en": a["name_en"], "cuisine_country": a["cuisine_country"],
                     "style": a["style"], "country_changed": a["cuisine_country"] != m["country_iso2"], **prov("w5")})
    write("llm_dishes", rows)


STEPS = {"w1": case_tags, "w2": case_facts, "w3": ingredient_lines, "w4": condition_terms, "w5": dishes}

if __name__ == "__main__":
    for w in sys.argv[1:] or list(STEPS):
        STEPS[w]()
