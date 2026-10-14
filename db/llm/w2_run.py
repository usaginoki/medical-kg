"""Run and score W2 (structured case facts) and measure how much of the output links to graph ids.

  uv run db/llm/w2_run.py run   [--models ...]      # on .cache/llm/refs/w2_sample.jsonl (64 cases)
  uv run db/llm/w2_run.py score                     # needs refs/w2_labels_*.jsonl
  UNIFIED_DB=<db> uv run db/llm/w2_run.py link      # link rates of foods / diagnosis / symptoms via the resolvers
"""
import argparse, asyncio, glob, json, os, sys

from rapidfuzz import fuzz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from client import LLM, PRICES, summary  # noqa: E402
from w1_run import BASE, RUNS, load, prf  # noqa: E402
import w2_case_facts as W  # noqa: E402

MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite", "gemma-4-26b-a4b-it",
          "gemma-4-31b-it"]


async def run_one(model, rows):
    llm = LLM(model, workers=3 if model.startswith("gemma") else 24)
    res = await llm.map(W.SYSTEM, [W.render(r) for r in rows], W.CaseFacts, W.VERSION, progress=False)
    os.makedirs(RUNS, exist_ok=True)
    with open(f"{RUNS}/w2_{model}.jsonl", "w", encoding="utf-8") as f:
        for r, x in zip(rows, res):
            f.write(json.dumps({"case_id": r["case_id"], "data": x.data, "error": x.error, "tokens_in": x.tokens_in,
                                "tokens_out": x.tokens_out, "latency": x.latency}, ensure_ascii=False) + "\n")
    print(f"w2_{model}: {summary(res)}", flush=True)


def soft_f1(gold, pred, cut=85):
    """Set F1 with fuzzy string matching (token_set_ratio >= cut), greedy one-to-one."""
    gold = [g.lower().strip() for g in gold]
    pred = [p.lower().strip() for p in pred]
    used, tp = set(), 0
    for p in pred:
        best = max(((fuzz.token_set_ratio(p, g), j) for j, g in enumerate(gold) if j not in used), default=(0, None))
        if best[0] >= cut:
            used.add(best[1])
            tp += 1
    return tp, len(pred) - tp, len(gold) - tp


def score():
    gold = {}
    for p in glob.glob(f"{BASE}/refs/w2_labels_*.jsonl"):
        for x in load(p):
            gold[x["case_id"]] = x["label"]
    print(f"gold labels: {len(gold)}")
    cols = ["valid", "age_acc", "sex_acc", "country_acc", "foods_P", "foods_R", "foods_F1", "symptoms_F1",
            "diagnosis_sim", "usd_per_1k"]
    lines = ["| model | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    for path in sorted(glob.glob(f"{RUNS}/w2_*.jsonl")):
        model = os.path.basename(path)[3:-6]
        recs = load(path)
        pred = {x["case_id"]: x["data"] for x in recs if x["data"]}
        ids = [i for i in gold if i in pred]
        g, p = [gold[i] for i in ids], [pred[i] for i in ids]
        m = {"valid": f"{len(pred)}/{len(recs)}"}
        age = lambda a, b: (a is None and b is None) or (a is not None and b is not None and abs(a - b) <= 1)  # noqa: E731
        m["age_acc"] = sum(age(a["age_years"], b["age_years"]) for a, b in zip(g, p)) / len(ids)
        m["sex_acc"] = sum(a["sex"] == b["sex"] for a, b in zip(g, p)) / len(ids)
        norm = lambda c: (c or "").lower().strip()  # noqa: E731
        m["country_acc"] = sum(norm(a["country"]) == norm(b["country"]) for a, b in zip(g, p)) / len(ids)
        t = [soft_f1([f["name_en"] for f in a["foods"] if not f["negated"]],
                     [f["name_en"] for f in b["foods"] if not f["negated"]]) for a, b in zip(g, p)]
        m["foods_P"], m["foods_R"], m["foods_F1"] = prf(*map(sum, zip(*t)))
        t = [soft_f1(a["symptoms"], b["symptoms"], 80) for a, b in zip(g, p)]
        m["symptoms_F1"] = prf(*map(sum, zip(*t)))[2]
        m["diagnosis_sim"] = sum(fuzz.token_set_ratio(norm(a["diagnosis_en"]), norm(b["diagnosis_en"])) >= 85
                                 for a, b in zip(g, p)) / len(ids)
        pin, pout = PRICES.get(model, (0, 0))
        m["usd_per_1k"] = sum(x["tokens_in"] * pin + x["tokens_out"] * pout for x in recs) / 1e6 / len(recs) * 1000
        lines.append(f"| {model} | " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in
                                                  (m[c] for c in cols)) + " |")
    text = "\n".join(lines)
    print(text)
    open(f"{RUNS}/w2_scores.md", "w").write(text + "\n")


def link():
    """Share of extracted names that resolve to a graph id (foods -> ingredient, diagnosis / symptoms -> condition),
    for the reference labels and for each model."""
    sys.path.insert(0, os.path.join(HERE, ".."))
    sys.path.insert(0, os.path.join(HERE, "..", "build"))
    import duckdb
    from common import DB_PATH
    from resolve import ConditionResolver, IngredientResolver
    con = duckdb.connect(DB_PATH, read_only=True)
    cr, ir = ConditionResolver(con), IngredientResolver(con)
    sets = {"reference": {}}
    for p in glob.glob(f"{BASE}/refs/w2_labels_*.jsonl"):
        for x in load(p):
            sets["reference"][x["case_id"]] = x["label"]
    for path in sorted(glob.glob(f"{RUNS}/w2_*.jsonl")):
        sets[os.path.basename(path)[3:-6]] = {x["case_id"]: x["data"] for x in load(path) if x["data"]}
    print(f"database: {DB_PATH}")
    print("| set | foods linked | diagnosis linked | symptoms linked | history linked |\n|---|---|---|---|---|")
    examples = []
    for name, d in sets.items():
        foods = [f["name_en"] for v in d.values() for f in v["foods"] if not f["negated"]]
        fl = [ir.by_text(f, "en") for f in foods]
        dx = [v["diagnosis_en"] for v in d.values() if v["diagnosis_en"]]
        dl = [cr.by_text(x) for x in dx]
        sy = [s for v in d.values() for s in v["symptoms"]]
        hi = [s for v in d.values() for s in v["history"]]
        rate = lambda xs: f"{sum(x is not None for x in xs)}/{len(xs)} ({sum(x is not None for x in xs) / max(1, len(xs)):.0%})"  # noqa: E731
        print(f"| {name} | {rate(fl)} | {rate(dl)} | {rate([cr.by_text(s) for s in sy])} | "
              f"{rate([cr.by_text(s) for s in hi])} |")
        if name == "reference":
            examples = [(f, r) for f, r in zip(foods, fl)][:25] + [(x, r) for x, r in zip(dx, dl)][:25]
    print("\nreference examples (name -> id):")
    for n, r in examples:
        print(f"  {n!r} -> {r}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "score", "link"])
    ap.add_argument("--models", nargs="*", default=MODELS)
    a = ap.parse_args()
    if a.cmd == "run":
        rows = load(f"{BASE}/refs/w2_sample.jsonl")

        async def go():
            await asyncio.gather(*(run_one(m, rows) for m in a.models))
        asyncio.run(go())
    elif a.cmd == "score":
        score()
    else:
        link()


if __name__ == "__main__":
    main()
