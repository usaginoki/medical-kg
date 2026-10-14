"""List reference items that two or more models answer differently from the reference label, per workflow and
field, for manual review. Writes .cache/llm/review/<workflow>.jsonl.

  uv run db/llm/disagree.py
"""
import glob, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from w1_run import BASE, RUNS, load, cue_types  # noqa: E402

OUT = f"{BASE}/review"
W1_RUNS = ["gemini-3.1-flash-lite_0shot_off", "gemini-3.5-flash-lite_0shot_off", "gemini-2.5-flash-lite_0shot_off",
           "gemma-4-31b-it_0shot_off"]
MODELS3 = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite"]


def gold_of(pattern, key):
    g = {}
    for p in glob.glob(f"{BASE}/refs/{pattern}"):
        for x in load(p):
            g[key(x)] = x
    return g


def write(name, items):
    os.makedirs(OUT, exist_ok=True)
    with open(f"{OUT}/{name}.jsonl", "w", encoding="utf-8") as f:
        for it in items:
            f.write(json.dumps(it, ensure_ascii=False) + "\n")
    print(f"{name}: {len(items)} items")


def w1():
    gold = gold_of("w1_labels_*.jsonl", lambda x: x["case_id"])
    preds = {r: {x["case_id"]: x["data"] for x in load(f"{RUNS}/w1_{r}.jsonl") if x["data"]} for r in W1_RUNS}
    matters = lambda d: d["culture_role"] in ("decisive", "supportive")  # noqa: E731
    fields = {"matters": matters, "diet_relevant": lambda d: d["diet_relevant"],
              "graph_answerable": lambda d: d["graph_answerable"], "cue_types": lambda d: sorted(cue_types(d))}
    items = []
    for cid, g in gold.items():
        for f, fn in fields.items():
            gv = fn(g["label"])
            wrong = {r: fn(p[cid]) for r, p in preds.items() if cid in p and fn(p[cid]) != gv}
            if len(wrong) >= 2:
                items.append({"case_id": cid, "field": f, "gold": gv, "models": wrong, "note": g.get("note"),
                              "confidence": g.get("confidence")})
    write("w1", items)


def simple(name, gfile, key, rfile_key, gval, pval):
    gold = gold_of(gfile, key)
    items = []
    preds = {m: {rfile_key(x): x for x in load(f"{RUNS}/{name}_{m}.jsonl")} for m in MODELS3
             if os.path.exists(f"{RUNS}/{name}_{m}.jsonl")}
    for k, g in gold.items():
        gv = gval(g)
        wrong = {m: pval(p[k]) for m, p in preds.items() if k in p and pval(p[k]) != gv}
        if len(wrong) >= 2:
            items.append({"key": k, "gold": gv, "models": wrong, "confidence": g.get("confidence")})
    write(name, items)


if __name__ == "__main__":
    w1()
    simple("w3", "w3_labels_*.jsonl", lambda x: x["raw_text"], lambda x: x["raw_text"],
           lambda g: g["label"]["ingredient_id"], lambda p: p["final"])
    from w4_condition_terms import resolver, ground  # compare grounded ids: names differ, ids may not
    _, cr, _ = resolver()
    simple("w4", "w4_labels_*.jsonl", lambda x: (x["source"], x["term"]), lambda x: (x["source"], x["term"]),
           lambda g: sorted(i for i in ground(cr, [c["name"] for c in g["label"]["conditions"]]) if i),
           lambda p: sorted(i for i in p["grounded"] if i))
    simple("w5", "w5_labels_*.jsonl", lambda x: x["dish_id"], lambda x: x["dish_id"],
           lambda g: g["label"]["cuisine_country"], lambda p: (p["data"] or {}).get("cuisine_country"))
