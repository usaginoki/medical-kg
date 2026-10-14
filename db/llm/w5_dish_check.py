"""W5: check a dish row: is it a dish, a clean English name, the cuisine's country, and traditional vs fusion.

  UNIFIED_DB=<db> uv run db/llm/w5_dish_check.py sample | run [--models ...] | score
"""
import argparse, asyncio, glob, json, os, sys
from typing import Literal

from pydantic import BaseModel, Field

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
from client import LLM, PRICES, summary  # noqa: E402
from w1_run import BASE, RUNS, load  # noqa: E402

VERSION = "w5-v1"
MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite"]


class DishCheck(BaseModel):
    kind: Literal["dish", "drink", "component_or_mix", "category", "not_food"]
    name_en: str = Field(description="clean English dish name, no website text")
    cuisine_country: str | None = Field(description="ISO 3166-1 alpha-2 code of the cuisine the dish comes from, "
                                                    "or null if international / unclear")
    style: Literal["traditional", "adapted", "fusion", "generic_international"]


SYSTEM = """You check dish records from recipe datasets (Food.com, CulinaryDB, XiaChuFang, IndicRecipeNutri, Japan MAFF,
Indian INDB). Each item gives the source, the stored name (may contain website text such as "Recipe | How to make"),
a local-language name, the cuisine label and country stored by the dataset, and some ingredients.
kind: dish (a prepared dish) | drink | component_or_mix (spice mix, premix, batter, sauce, stock made to be used in
  other dishes) | category (a group such as "汤菜" soups, "东北名菜") | not_food.
name_en: a clean English name ("Kozhukattai (steamed rice dumplings)" style only when the name is not English).
cuisine_country: ISO alpha-2 country the dish belongs to by origin (biryani -> IN, plov -> UZ only when the record is
  Uzbek-style; a dish shared by a region -> the country the record's label points to); null for international dishes
  (pasta salad, brownies) or when unclear. The stored label can be wrong: judge from the dish itself.
style: traditional (a recognised dish of that cuisine) | adapted (a home or Western-kitchen version of one, e.g.
  slow-cooker biryani) | fusion (mixes cuisines: "Thai pizza", "kimchi quesadilla") | generic_international (no
  particular cuisine)."""


def render(r):
    return (f"SOURCE: {r['source_id']}\nNAME: {r['name']}\nLOCAL NAME: {r['name_local'] or ''}\n"
            f"CUISINE LABEL: {r['cuisine_label'] or ''}\nSTORED COUNTRY: {r['country_iso2'] or ''}\n"
            f"SUBREGION: {r['subregion'] or ''}\nINGREDIENTS: {r['ingredients']}")


def sample():
    import duckdb
    from common import DB_PATH
    con = duckdb.connect(DB_PATH, read_only=True)
    q = """SELECT d.dish_id, d.name, d.name_local, d.cuisine_label, d.country_iso2, d.subregion, d.source_id,
                  (SELECT string_agg(raw_text, '; ') FROM (SELECT raw_text FROM dish_ingredient i
                   WHERE i.dish_id = d.dish_id LIMIT 12)) AS ingredients
           FROM dish d WHERE {w} ORDER BY hash(d.dish_id || 'w5') LIMIT {n}"""
    parts = [("source_id='foodcom' AND country_iso2 IS NULL", 10), ("source_id='foodcom' AND country_iso2 IS NOT NULL", 20),
             ("source_id='culinarydb' AND country_iso2 IS NULL", 15), ("source_id='xiachufang'", 15),
             ("source_id='indicrecipenutri'", 15), ("source_id='maff'", 5)]
    rows = []
    for w, n in parts:
        rows += con.sql(q.format(w=w, n=n)).df().to_dict("records")
    with open(f"{BASE}/refs/w5_sample.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            r["ingredients"] = (r["ingredients"] or "")[:400]
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{len(rows)} dishes -> refs/w5_sample.jsonl")


async def run(models):
    rows = load(f"{BASE}/refs/w5_sample.jsonl")

    async def one(m):
        llm = LLM(m, workers=24)
        res = await llm.map(SYSTEM, [render(r) for r in rows], DishCheck, VERSION, progress=False)
        with open(f"{RUNS}/w5_{m}.jsonl", "w", encoding="utf-8") as f:
            for r, x in zip(rows, res):
                f.write(json.dumps({"dish_id": r["dish_id"], "data": x.data, "error": x.error,
                                    "tokens_in": x.tokens_in, "tokens_out": x.tokens_out}, ensure_ascii=False) + "\n")
        print(f"w5_{m}: {summary(res)}", flush=True)

    await asyncio.gather(*(one(m) for m in models))


def score():
    rows = {r["dish_id"]: r for r in load(f"{BASE}/refs/w5_sample.jsonl")}
    gold = {}
    for p in glob.glob(f"{BASE}/refs/w5_labels_*.jsonl"):
        for x in load(p):
            gold[x["dish_id"]] = x["label"]
    rp = f"{BASE}/refs/w5_review.json"
    alts = {r["id"]: set(r["also_ok"]) for r in (json.load(open(rp)) if os.path.exists(rp) else [])}
    okc = lambda k, c: c == gold[k]["cuisine_country"] or c in alts.get(k, set())  # noqa: E731
    cols = ["n", "kind_acc", "country_acc", "country_acc_stored_missing", "style_acc", "fusion_or_generic_F1",
            "usd_per_1k"]
    lines = ["| run | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    preds = {"stored country": {k: {"cuisine_country": r["country_iso2"]} for k, r in rows.items()}}
    costs = {}
    for path in sorted(glob.glob(f"{RUNS}/w5_*.jsonl")):
        m = os.path.basename(path)[3:-6]
        recs = load(path)
        preds[m] = {x["dish_id"]: x["data"] for x in recs if x["data"]}
        pin, pout = PRICES.get(m, (0, 0))
        costs[m] = sum(x["tokens_in"] * pin + x["tokens_out"] * pout for x in recs) / 1e6 / len(recs) * 1000
    from w1_run import binary
    for name, pred in preds.items():
        ks = [k for k in gold if k in pred]
        out = {"n": len(ks), "usd_per_1k": costs.get(name, "")}
        out["country_acc"] = sum(okc(k, pred[k]["cuisine_country"]) for k in ks) / len(ks)
        miss = [k for k in ks if not rows[k]["country_iso2"]]
        out["country_acc_stored_missing"] = sum(okc(k, pred[k]["cuisine_country"]) for k in miss) / max(1, len(miss))
        if "kind" in pred[ks[0]]:
            out["kind_acc"] = sum(gold[k]["kind"] == pred[k]["kind"] for k in ks) / len(ks)
            out["style_acc"] = sum(gold[k]["style"] == pred[k]["style"] for k in ks) / len(ks)
            fg = lambda x: x["style"] in ("fusion", "generic_international")  # noqa: E731
            out["fusion_or_generic_F1"] = binary([fg(gold[k]) for k in ks], [fg(pred[k]) for k in ks])[2]
        lines.append(f"| {name} | " + " | ".join(f"{out[c]:.3f}" if isinstance(out.get(c), float) else str(out.get(c, ""))
                                                for c in cols) + " |")
    text = "\n".join(lines)
    print(text)
    open(f"{RUNS}/w5_scores.md", "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "run", "score"])
    ap.add_argument("--models", nargs="*", default=MODELS)
    a = ap.parse_args()
    {"sample": sample, "run": lambda: asyncio.run(run(a.models)), "score": score}[a.cmd]()


if __name__ == "__main__":
    main()
