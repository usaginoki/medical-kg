"""Run and score W1 (case cultural tagging) on the reference sample.

  uv run db/llm/w1_run.py run  [--models m1 m2 ...] [--shots 0 1] [--thinking off]
  uv run db/llm/w1_run.py score                      # needs .cache/llm/refs/w1_labels_*.jsonl

Outputs: .cache/llm/runs/w1_<model>_<shots>shot_<thinking>.jsonl and a Markdown score table on stdout
(also written to .cache/llm/runs/w1_scores.md).
"""
import argparse, asyncio, copy, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import LLM, PRICES, summary  # noqa: E402
import w1_case_tags as W  # noqa: E402

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".cache", "llm"))
RUNS = f"{BASE}/runs"
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash-lite", "gemma-4-26b-a4b-it",
          "gemma-4-31b-it"]
REAL = {"patient", "family", "other"}  # cues that are about a person (not a test name or a form line)


def load(path):
    return [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]


def run_name(model, shots, thinking):
    """Run file name; prompt versions after w1-v1 are suffixed so earlier runs stay comparable."""
    return f"w1_{model}_{shots}shot_{thinking}" + ("" if W.VERSION.startswith("w1-v1") else f"_{W.VERSION.split()[0]}")


async def run_one(model, shots, thinking, rows):
    llm = LLM(model, workers=3 if model.startswith("gemma") else 24, thinking=thinking)
    system = W.few_shot_system() if shots else W.SYSTEM
    res = await llm.map(system, [W.render(r) for r in rows], W.CaseTags, f"{W.VERSION}-{shots}shot")
    os.makedirs(RUNS, exist_ok=True)
    with open(f"{RUNS}/{run_name(model, shots, thinking)}.jsonl", "w", encoding="utf-8") as f:
        for r, x in zip(rows, res):
            f.write(json.dumps({"case_id": r["case_id"], "data": x.data, "error": x.error, "tokens_in": x.tokens_in,
                                "tokens_out": x.tokens_out, "latency": x.latency}, ensure_ascii=False) + "\n")
    s = summary(res)
    print(f"{run_name(model, shots, thinking)}: {s}", flush=True)
    return s


async def run(models, shots, thinking):
    rows = load(f"{BASE}/refs/w1_sample.jsonl")
    await asyncio.gather(*(run_one(m, k, t, rows) for m in models for k in shots for t in thinking))


# ---------- scoring ----------

def cue_types(label, merge_origin=False):
    """Non-negated cue types about a person. merge_origin: count place and ethnicity as one type ('origin'), since
    nationality words ('a Japanese man') fit both definitions."""
    t = {c["type"] for c in label["cues"] if not c["negated"] and c["about"] in REAL}
    return {"origin" if merge_origin and x in ("place", "ethnicity") else x for x in t}


def screen_types(row):
    """The keyword screen's cue types for a sample row (from cue_hits)."""
    return {part.split(":")[0].strip() for part in (row.get("cue_hits") or "").split(";") if part.strip()}


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def binary(gold, pred):
    tp = sum(g and p for g, p in zip(gold, pred))
    fp = sum(p and not g for g, p in zip(gold, pred))
    fn = sum(g and not p for g, p in zip(gold, pred))
    return prf(tp, fp, fn)


def score_pred(rows, gold, pred, skip=None):
    """Metrics for one prediction set. gold / pred: {case_id: label dict}; rows: sample rows. skip: {field: set of
    case_ids} left out of that field's score (items the manual review found ambiguous under the definitions)."""
    skip = skip or {}
    ids = [r["case_id"] for r in rows if r["case_id"] in gold and r["case_id"] in pred]
    out = {"n": len(ids)}
    keep = lambda f: [i for i in ids if i not in skip.get(f, ())]  # noqa: E731
    matters = lambda x: x["culture_role"] in ("decisive", "supportive")  # noqa: E731
    k = keep("matters")
    out["role_acc"] = sum(gold[i]["culture_role"] == pred[i]["culture_role"] for i in k) / len(k)
    out["matters_P"], out["matters_R"], out["matters_F1"] = binary([matters(gold[i]) for i in k], [matters(pred[i]) for i in k])
    out["decisive_F1"] = binary([gold[i]["culture_role"] == "decisive" for i in k],
                                [pred[i]["culture_role"] == "decisive" for i in k])[2]
    for f in ("diet_relevant", "graph_answerable", "answer_leak"):
        k = [i for i in keep(f) if f in pred[i]]  # w1-v3 no longer asks for answer_leak
        if not k:
            continue
        out[f + "_F1"] = binary([gold[i][f] for i in k], [pred[i][f] for i in k])[2]
        out[f + "_acc"] = sum(gold[i][f] == pred[i][f] for i in k) / len(k)
    for name, merge in (("cue", False), ("cue_origin", True)):
        tp = fp = fn = 0
        for i in keep("cue_types"):
            ga, pb = cue_types(gold[i], merge), cue_types(pred[i], merge)
            tp, fp, fn = tp + len(ga & pb), fp + len(pb - ga), fn + len(ga - pb)
        out[name + "_P"], out[name + "_R"], out[name + "_F1"] = prf(tp, fp, fn)
    return out


def apply_review(gold, review):
    """Apply the manual review of the reference labels (refs/w1_review.json): corrected fields and cues for
    'gold_wrong' items; for 'ambiguous' items, the fields to leave out of the score. Returns (gold, skip)."""
    gold = copy.deepcopy(gold)
    skip = {}
    for r in review:
        g = gold.get(r["id"])
        if g is None:
            continue
        if r["verdict"] == "gold_wrong":
            g.update(r.get("set", {}))
            for c in g["cues"]:
                if c["text"] in r.get("cue_about", {}):
                    c["about"] = r["cue_about"][c["text"]]
            g["cues"] = [c for c in g["cues"] if c["text"] not in r.get("cue_drop", [])]
        elif r["verdict"] == "ambiguous":
            for f in r["fields"]:
                skip.setdefault(f, set()).add(r["id"])
        # 'gold_ok': the reference stands (a decision settled the question)
    return gold, skip


def screen_baseline(rows, gold):
    """The keyword screen scored the same way: cue types from cue_hits, 'matters' = strong cue, diet = diet flag."""
    pred = {}
    for r in rows:
        types = screen_types(r)
        pred[r["case_id"]] = {
            "cues": [{"type": t, "negated": False, "about": "patient"} for t in types],
            "culture_role": "supportive" if r["cue_strength"] == "strong" else "incidental" if types else "none",
            "diet_relevant": bool(r["diet"]), "graph_answerable": bool(r["diet"]), "answer_leak": False}
    return pred


def score():
    rows = load(f"{BASE}/refs/w1_sample.jsonl")
    raw = {}
    for path in sorted(glob.glob(f"{BASE}/refs/w1_labels_*.jsonl")):
        for x in load(path):
            raw[x["case_id"]] = x["label"]
    review_path = f"{BASE}/refs/w1_review.json"
    review = json.load(open(review_path)) if os.path.exists(review_path) else []
    reviewed, skip = apply_review(raw, review)
    print(f"gold labels: {len(raw)} / {len(rows)}; review: "
          f"{sum(r['verdict'] == 'gold_wrong' for r in review)} corrected, "
          f"{sum(r['verdict'] == 'ambiguous' for r in review)} ambiguous items left out of their field, "
          f"{sum(r['verdict'] == 'gold_ok' for r in review)} confirmed by a decision")
    cols = ["n", "valid", "role_acc", "matters_P", "matters_R", "matters_F1", "decisive_F1", "cue_F1", "cue_origin_F1",
            "diet_relevant_F1", "graph_answerable_F1", "answer_leak_F1", "usd_per_1k", "s_per_item"]
    runs = [("keyword screen", screen_baseline(rows, raw), None)]
    for path in sorted(glob.glob(f"{RUNS}/w1_*.jsonl")):
        recs = load(path)
        runs.append((os.path.basename(path)[3:-6], {x["case_id"]: x["data"] for x in recs if x["data"]}, recs))
    text = []
    for title, gold, sk in (("reference labels as written", raw, None), ("after manual review", reviewed, skip)):
        lines = [f"### {title}", "| run | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
        for name, pred, recs in runs:
            m = score_pred(rows, gold, pred, sk)
            if recs:
                pin, pout = PRICES.get(name.split("_")[0], (0, 0))
                m["valid"] = len(pred)
                m["usd_per_1k"] = sum(x["tokens_in"] * pin + x["tokens_out"] * pout for x in recs) / 1e6 / len(recs) * 1000
                m["s_per_item"] = sum(x["latency"] for x in recs) / len(recs)
            lines.append(f"| {name} | " + " | ".join(_fmt(m.get(c, "")) for c in cols) + " |")
        text.append("\n".join(lines))
    text = "\n\n".join(text)
    print(text)
    os.makedirs(RUNS, exist_ok=True)
    open(f"{RUNS}/w1_scores.md", "w").write(text + "\n")


def _fmt(v):
    return f"{v:.3f}" if isinstance(v, float) else str(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "score"])
    ap.add_argument("--models", nargs="*", default=MODELS)
    ap.add_argument("--shots", nargs="*", type=int, default=[0, 1])
    ap.add_argument("--thinking", nargs="*", default=["off"])
    a = ap.parse_args()
    if a.cmd == "run":
        asyncio.run(run(a.models, a.shots, a.thinking))
    else:
        score()


if __name__ == "__main__":
    main()
