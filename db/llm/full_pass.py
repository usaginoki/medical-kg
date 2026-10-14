"""Full LLM pass over what the rule screens hand off, through the Gemini Batch API (db/llm/batch.py).

  uv run db/llm/full_pass.py items             # build and count the items per workflow (-> .cache/llm/full/<w>.jsonl)
  uv run db/llm/full_pass.py submit w4 w5      # submit batch jobs (skips cached items; refused above the $ cap)
  uv run db/llm/full_pass.py status            # job states and spend
  uv run db/llm/full_pass.py collect           # finished jobs -> cache; invalid answers repaired with the standard API
  uv run db/llm/full_pass.py costs             # spend per workflow

Workflows and hand-off (Database/LLM tagging experiments.md). MedArabiQ is never sent (licence; see the issue).
  w1   cultural tags + reason for the culture role   screen-passing cases   gemini-3.1-flash-lite  (w1_case_tags)
  w2   case facts           screen-passing cases            gemini-3.1-flash-lite  (w2_case_facts)
  w3   ingredient lines     weak + unmatched distinct lines gemini-3.1-flash-lite  (w3_ingredient_lines)
  w4   condition terms      unmatched distinct terms        gemini-3.5-flash-lite  (w4_condition_terms)
  w5   dish check           dishes without a country + Food.com dishes   gemini-3.5-flash-lite (w5_dish_check)
"""
import asyncio, json, os, re, sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import batch  # noqa: E402
from client import LLM  # noqa: E402
from w1_run import BASE, load  # noqa: E402
from export import OUT  # noqa: E402
import w1_case_tags as W1, w2_case_facts as W2  # noqa: E402,E401
import w3_ingredient_lines as W3, w4_condition_terms as W4, w5_dish_check as W5  # noqa: E402,E401

FULL = f"{BASE}/full"
# The answer-leak check (w1b_leak.py) was dropped from the full pass on 2026-10-15: not needed for the evaluation.
EXCLUDED_SOURCES = {"MedArabiQ"}
CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")


def est_tokens(text):
    """Rough input tokens for a text (for the cost estimate before submission): CJK about 1 token per character,
    other scripts about 0.3."""
    n = len(CJK.findall(text))
    return n + (len(text) - n) * 0.3


TASKS = {
    "w1": dict(model="gemini-3.1-flash-lite", version=f"{W1.VERSION}-0shot", system=W1.SYSTEM, schema=W1.CaseTags,
               est_out=130),
    "w2": dict(model="gemini-3.1-flash-lite", version=W2.VERSION, system=W2.SYSTEM, schema=W2.CaseFacts, est_out=480),
    "w3": dict(model="gemini-3.1-flash-lite", version=W3.VERSION, system=W3.SYSTEM, schema=W3.IngMatch, est_out=60),
    "w4": dict(model="gemini-3.5-flash-lite", version=W4.VERSION, system=W4.SYSTEM, schema=W4.TermMap, est_out=100),
    "w5": dict(model="gemini-3.5-flash-lite", version=W5.VERSION, system=W5.SYSTEM, schema=W5.DishCheck, est_out=60),
}
for _n, _t in TASKS.items():
    _t["name"] = _n
    _t["est_in_per_char"] = 0.0  # batch.submit uses est_tokens through est_in below


def screened_cases():
    d = pd.read_parquet(f"{OUT}/cases.parquet")
    d = d[~d.source.isin(EXCLUDED_SOURCES)]
    keep = (d.cue_strength != "none") | d.diet | d.cues_negated.ne("") | d.culture_by_construction
    return d[keep]


def build_items():
    """{workflow: [record]}; each record has item_id, text and the fields store.py keeps next to the answer."""
    os.makedirs(FULL, exist_ok=True)
    out = {}
    cases = screened_cases()
    rows = cases.to_dict("records")
    out["w1"] = [{"item_id": r["case_id"], "text": W1.render(r)} for r in rows]
    out["w2"] = [{"item_id": r["case_id"], "text": W2.render(r)} for r in rows]
    con = W3.con_db()
    pop = W3.population(con)
    cands = W3.Candidates(con)
    recs = []
    for r in pop.to_dict("records"):
        if not isinstance(r["raw_text"], str) or not r["raw_text"].strip():
            continue
        r["candidates"] = cands(r["raw_text"], r["ingredient_id"])
        r["match_score"] = None if pd.isna(r["match_score"]) else r["match_score"]
        r["ingredient_id"] = r["ingredient_id"] if isinstance(r["ingredient_id"], str) else None
        recs.append({"item_id": r["raw_text"], "text": W3.render(r, cands), "meta": r})
    out["w3"] = recs
    pop4 = W4.population()
    un = pop4[pop4.current.map(len).eq(0)]
    out["w4"] = [{"item_id": f"{r['source']}|{r['term']}", "text": W4.render(r), "meta": r} for r in un.to_dict("records")]
    q = """SELECT d.dish_id, d.name, d.name_local, d.cuisine_label, d.country_iso2, d.subregion, d.source_id,
                  (SELECT string_agg(raw_text, '; ') FROM (SELECT raw_text FROM dish_ingredient i
                   WHERE i.dish_id = d.dish_id LIMIT 12)) AS ingredients
           FROM dish d WHERE d.country_iso2 IS NULL OR d.source_id = 'foodcom'"""
    dishes = con.sql(q).df().to_dict("records")
    for r in dishes:
        r["ingredients"] = (r["ingredients"] or "")[:400]
    out["w5"] = [{"item_id": r["dish_id"], "text": W5.render(r), "meta": r} for r in dishes]
    for w, items in out.items():
        with open(f"{FULL}/{w}.jsonl", "w", encoding="utf-8") as f:
            for it in items:
                f.write(json.dumps(it, ensure_ascii=False, default=str) + "\n")
        t = TASKS[w]
        pin, pout = batch.PRICES[t["model"]]
        est = sum((est_tokens(t["system"] + it["text"])) * pin + t["est_out"] * pout for it in items) / 1e6 / 2
        print(f"{w:4} {len(items):>7,} items  est ${est:.2f} (batch)  -> {os.path.relpath(FULL)}/{w}.jsonl")


def submit(names):
    for w in names:
        t = TASKS[w]
        items = load(f"{FULL}/{w}.jsonl")
        task = dict(t, est_in_per_char=0.0)
        # per-item estimate with est_tokens: pass it as an average per character over this workflow
        chars = sum(len(t["system"]) + len(it["text"]) for it in items)
        task["est_in_per_char"] = sum(est_tokens(t["system"] + it["text"]) for it in items) / max(1, chars)
        batch.submit(task, [(it["item_id"], it["text"]) for it in items])


def collect():
    failed = batch.collect({w: t["schema"] for w, t in TASKS.items()})
    for w, items in failed.items():
        if not items:
            continue
        t = TASKS[w]
        print(f"{w}: repairing {len(items):,} items with the standard API")
        res = asyncio.run(LLM(t["model"], workers=16).map(t["system"], [x["text"] for x in items], t["schema"],
                                                           t["version"], progress=False))
        print(f"{w}: repaired {sum(r.data is not None for r in res):,}/{len(items):,}")


def costs():
    led = batch.load_ledger()
    by = {}
    for j in led["jobs"]:
        b = by.setdefault(j["task"], {"jobs": 0, "n": 0, "est": 0.0, "actual": 0.0, "collected": 0})
        b["jobs"] += 1
        b["n"] += j["n"]
        b["est"] += j["est_usd"]
        if j.get("collected"):
            b["actual"] += j["actual_usd"]
            b["collected"] += j["n"]
    print("| workflow | jobs | items | collected | est $ | actual $ |\n|---|---|---|---|---|---|")
    for w, b in by.items():
        print(f"| {w} | {b['jobs']} | {b['n']:,} | {b['collected']:,} | {b['est']:.2f} | {b['actual']:.2f} |")
    print(f"committed (spent + pending estimates): ${batch.committed(led):.2f} of ${batch.MAX_USD:.0f}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    {"items": lambda: build_items(), "submit": lambda: submit(args or list(TASKS)), "status": lambda: batch.poll(),
     "collect": collect, "costs": costs}[cmd]()
