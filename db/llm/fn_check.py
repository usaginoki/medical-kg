"""False-negative check of the keyword screen: tag a sample of the cases the screen rejects (no cue, no diet word,
no negated hit, not cultural by construction) and of the weak-cue-only cases with W1, and list the cases a model
flags, for manual review.

  uv run db/llm/fn_check.py sample
  uv run db/llm/fn_check.py run
  uv run db/llm/fn_check.py flagged        # -> .cache/llm/review/fn_flagged.jsonl
"""
import asyncio, json, os, sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from client import LLM, summary  # noqa: E402
from w1_run import BASE, RUNS, load, cue_types  # noqa: E402
import w1_case_tags as W  # noqa: E402
from export import OUT  # noqa: E402

MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite"]
PLAN = [("rejected", "MedCaseReasoning", 250), ("rejected", "RuMedBench", 120), ("rejected", "MedicationQA", 50),
        ("weak", "MedCaseReasoning", 80)]


def sample():
    d = pd.read_parquet(f"{OUT}/cases.parquet")
    d = d[d.source != "MedArabiQ"]
    rejected = (d.cue_strength == "none") & ~d.diet & d.cues_negated.eq("") & ~d.culture_by_construction
    groups = {"rejected": d[rejected], "weak": d[d.cue_strength == "weak"]}
    parts = []
    for g, src, n in PLAN:
        sub = groups[g][groups[g].source == src]
        s = sub.sample(min(n, len(sub)), random_state=21).assign(stratum=g, stratum_size=len(sub))
        parts.append(s)
    s = pd.concat(parts)
    cols = ["case_id", "source", "origin", "lang", "stratum", "stratum_size", "cue_hits", "cues_negated", "case",
            "conclusion"]
    s[cols].to_json(f"{BASE}/refs/fn_sample.jsonl", orient="records", lines=True, force_ascii=False)
    print(s.groupby(["stratum", "source"]).size().to_string())


async def run():
    rows = load(f"{BASE}/refs/fn_sample.jsonl")

    async def one(m):
        res = await LLM(m, workers=24).map(W.SYSTEM, [W.render(r) for r in rows], W.CaseTags, f"{W.VERSION}-0shot",
                                           progress=False)
        with open(f"{RUNS}/fn_{m}.jsonl", "w", encoding="utf-8") as f:
            for r, x in zip(rows, res):
                f.write(json.dumps({"case_id": r["case_id"], "data": x.data, "error": x.error}, ensure_ascii=False) + "\n")
        print(f"fn_{m}: {summary(res)}")

    await asyncio.gather(*(one(m) for m in MODELS))


def flagged():
    rows = {r["case_id"]: r for r in load(f"{BASE}/refs/fn_sample.jsonl")}
    preds = {m: {x["case_id"]: x["data"] for x in load(f"{RUNS}/fn_{m}.jsonl") if x["data"]} for m in MODELS}
    out = []
    for cid, r in rows.items():
        flags = {}
        for m, p in preds.items():
            d = p.get(cid)
            if not d:
                continue
            f = []
            if d["culture_role"] in ("decisive", "supportive"):
                f.append(f"culture {d['culture_role']}")
            if d["diet_relevant"]:
                f.append("diet")
            if d["graph_answerable"]:
                f.append("graph")
            if f:
                flags[m] = f + [f"cues {sorted(cue_types(d))}"] + [f"{c['type']}:{c['text']}" for c in d["cues"]
                                                                   if not c["negated"] and c["about"] in ("patient", "family", "other")]
        if flags:
            out.append({"case_id": cid, "stratum": r["stratum"], "source": r["source"], "flags": flags})
    os.makedirs(f"{BASE}/review", exist_ok=True)
    with open(f"{BASE}/review/fn_flagged.jsonl", "w", encoding="utf-8") as f:
        for o in out:
            f.write(json.dumps(o, ensure_ascii=False) + "\n")
    tab = pd.DataFrame([{"stratum": rows[c]["stratum"], "source": rows[c]["source"],
                         "flagged": any(o["case_id"] == c for o in out)} for c in rows])
    print(tab.groupby(["stratum", "source"]).flagged.agg(["sum", "count"]).to_string())


if __name__ == "__main__":
    {"sample": sample, "run": lambda: asyncio.run(run()), "flagged": flagged}[sys.argv[1]]()
