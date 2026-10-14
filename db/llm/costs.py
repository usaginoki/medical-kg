"""Extrapolate full-run costs of each workflow from the tokens measured on the reference samples.

  uv run db/llm/costs.py

Per workflow: the population the rule screen hands to the LLM, mean input / output tokens per item measured with the
same model (per dataset for the case workflows, since case length differs a lot), and the cost at standard and Batch
(half) prices.
"""
import collections, json, os, sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from client import PRICES  # noqa: E402
from w1_run import BASE, RUNS, load  # noqa: E402
from export import OUT  # noqa: E402

MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite"]


def per_source_tokens(run_file, sample_file, key="case_id"):
    src = {r[key]: r["source"] for r in load(sample_file)}
    acc = collections.defaultdict(lambda: [0, 0, 0])
    for x in load(run_file):
        a = acc[src[x[key]]]
        a[0] += x["tokens_in"]; a[1] += x["tokens_out"]; a[2] += 1
    return {s: (a[0] / a[2], a[1] / a[2]) for s, a in acc.items()}


def flat_tokens(run_file):
    recs = load(run_file)
    return sum(x["tokens_in"] for x in recs) / len(recs), sum(x["tokens_out"] for x in recs) / len(recs)


def main():
    cases = pd.read_parquet(f"{OUT}/cases.parquet", columns=["source", "cue_strength", "diet", "cues_negated",
                                                             "culture_by_construction", "gold"])
    cases = cases[cases.source != "MedArabiQ"]
    screened = cases[(cases.cue_strength != "none") | cases.diet | cases.cues_negated.ne("") | cases.culture_by_construction]
    pops = {"W1 case tags (screen-passing cases)": screened.source.value_counts().to_dict(),
            "W1 case tags (all cases)": cases.source.value_counts().to_dict()}
    rows = []
    for m in MODELS:
        pin, pout = PRICES[m]
        tok = per_source_tokens(f"{RUNS}/w1_{m}_0shot_off.jsonl", f"{BASE}/refs/w1_sample.jsonl")
        fallback = (sum(v[0] for v in tok.values()) / len(tok), sum(v[1] for v in tok.values()) / len(tok))
        for name, pop in pops.items():
            usd = sum(n * (tok.get(s, fallback)[0] * pin + tok.get(s, fallback)[1] * pout) / 1e6 for s, n in pop.items())
            rows.append((name, m, sum(pop.values()), usd))
        tok2 = per_source_tokens(f"{RUNS}/w2_{m}.jsonl", f"{BASE}/refs/w2_sample.jsonl")
        fb2 = (sum(v[0] for v in tok2.values()) / len(tok2), sum(v[1] for v in tok2.values()) / len(tok2))
        pop = pops["W1 case tags (screen-passing cases)"]
        usd = sum(n * (tok2.get(s, fb2)[0] * pin + tok2.get(s, fb2)[1] * pout) / 1e6 for s, n in pop.items())
        rows.append(("W2 case facts (screen-passing cases)", m, sum(pop.values()), usd))
        for name, f, n in (("W3 ingredient lines (weak + unmatched, distinct)", "w3", len(load(f"{BASE}/refs/w3_population.jsonl"))),
                           ("W4 condition terms (unmatched, distinct)", "w4",
                            sum(1 for r in load(f"{BASE}/refs/w4_population.jsonl") if not r["current"])),
                           ("W5 dish check (all dishes)", "w5", 46253)):
            ti, to = flat_tokens(f"{RUNS}/{f}_{m}.jsonl")
            rows.append((name, m, n, n * (ti * pin + to * pout) / 1e6))
    df = pd.DataFrame(rows, columns=["workflow", "model", "items", "usd"])
    df["usd_batch"] = df.usd / 2
    print("| workflow | model | items | USD standard | USD batch |\n|---|---|---|---|---|")
    for r in df.itertuples():
        print(f"| {r.workflow} | {r.model} | {r.items:,} | {r.usd:.2f} | {r.usd_batch:.2f} |")


if __name__ == "__main__":
    main()
