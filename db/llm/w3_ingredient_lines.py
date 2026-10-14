"""W3: map a recipe ingredient line that the rules matched weakly (fuzzy, substring, normalised < 0.8) or not at all
to an ingredient id, or say it is not an ingredient.

Retrieve-then-choose: rapidfuzz proposes up to K candidate ingredients from the alias table; the model picks one, or
NONE, and also names the ingredient in English. When it picks NONE but the English name resolves exactly with the
IngredientResolver, that id is used (generate-then-ground fallback).

  UNIFIED_DB=<db> uv run db/llm/w3_ingredient_lines.py sample | run [--models ...] | score
"""
import argparse, asyncio, glob, json, os, re, sys
from typing import Literal

from pydantic import BaseModel, Field
from rapidfuzz import fuzz, process

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "build"))
from client import LLM, PRICES, summary  # noqa: E402
from w1_run import BASE, RUNS, load  # noqa: E402

VERSION = "w3-v1"
MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite"]
K = 8
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af]")
WEAK = "match_method IN ('fuzzy','substring','unmatched') OR (match_method='normalised' AND match_score < 0.8)"


class IngMatch(BaseModel):
    kind: Literal["ingredient", "several_ingredients", "header_or_note", "non_food_item", "prepared_component"]
    name_en: str = Field(description="the main ingredient in plain English, generic, no quantity; '' if none")
    choice: str = Field(description="the id of the best candidate, or NONE")
    fit: Literal["exact", "close", "broader", "none"]


SYSTEM = """You match lines from recipe ingredient lists (English, Chinese, Japanese, Hindi-English) to a food
ingredient vocabulary. Each item gives the LINE, its language, the CURRENT match from a rule-based matcher (may be
wrong), and CANDIDATES (id: name; aliases) found by string similarity.
kind: ingredient | several_ingredients (the line lists more than one; choose the main one) | header_or_note (a
  section title, note, instruction, website text) | non_food_item (skewers, leaves for wrapping, a weight stone) |
  prepared_component (a sub-recipe such as 'idli batter', 'for the gravy').
name_en: the main ingredient in plain English (e.g. '牛肉片' -> 'beef', 'rajgiri atta' -> 'amaranth flour').
choice: the candidate id that names the same food. Prefer the exact food; accept a slightly broader one only when no
  exact one is offered (fit = broader). A different species, cut that changes the food (pork vs beef), a different
  product (oyster sauce is not oyster) or a different plant part with different use is NOT a match. Use NONE when no
  candidate fits or the line is not an ingredient.
fit: exact | close (spelling / form variant: 'red chilly' -> chili) | broader | none."""


def con_db():
    import duckdb
    from common import DB_PATH
    return duckdb.connect(DB_PATH, read_only=True)


class Candidates:
    """Top-K ingredient candidates for a line, by rapidfuzz WRatio over canonical names and aliases."""

    def __init__(self, con):
        al = con.sql("""SELECT a.ingredient_id, a.alias, a.lang FROM ingredient_alias a UNION
                        SELECT ingredient_id, canonical_name, 'en' FROM ingredient""").fetchall()
        self.names = dict(con.sql("SELECT ingredient_id, canonical_name FROM ingredient").fetchall())
        self.keys = [a.lower() for _, a, _ in al]
        self.ids = [i for i, _, _ in al]
        self.aliases = {}
        for i, a, _ in al:
            self.aliases.setdefault(i, []).append(a)
        self.cjk = {j: k for j, k in enumerate(self.keys) if CJK.search(k)}  # CJK aliases, for CJK lines

    def __call__(self, text, current=None):
        """Chinese / Japanese lines: aliases contained in the line first (longest first), then WRatio over CJK
        aliases; other lines: WRatio over all aliases."""
        text = text.lower()
        out = [current] if isinstance(current, str) else []
        if CJK.search(text):
            inside = sorted({(len(k), self.ids[j]) for j, k in self.cjk.items() if k in text}, reverse=True)
            for _, i in inside:
                if i not in out:
                    out.append(i)
            hits = process.extract(text, self.cjk, scorer=fuzz.WRatio, limit=60)
        else:
            hits = process.extract(text, self.keys, scorer=fuzz.WRatio, limit=60)
        for _, _, j in hits:
            if self.ids[j] not in out:
                out.append(self.ids[j])
            if len(out) >= K:
                break
        return out

    def show(self, i):
        al = [a for a in self.aliases.get(i, []) if a.lower() != (self.names.get(i) or "").lower()][:4]
        return f"{i}: {self.names.get(i)}" + (f"; {', '.join(al)}" if al else "")


def render(r, cands):
    cur = (f"{r['ingredient_id']} ({r['match_method']}, score {r['match_score']})" if r["ingredient_id"] else "none")
    return (f"LINE: {r['raw_text']}\nLANGUAGE: {r['lang']}\nSOURCE: {r['source_id']}\nCURRENT: {cur}\n"
            f"CANDIDATES:\n" + "\n".join(cands.show(i) for i in r["candidates"]))


def population(con):
    """Distinct weak or unmatched ingredient lines (lower-cased) with their current match and line count."""
    q = f"""SELECT lower(di.raw_text) raw_text, any_value(di.ingredient_id) ingredient_id,
                   any_value(di.match_method) match_method, round(any_value(di.match_score), 2) match_score,
                   any_value(d.lang) lang, any_value(di.source_id) source_id, count(*) lines
            FROM dish_ingredient di JOIN dish d USING (dish_id) WHERE {WEAK.replace('match_', 'di.match_')}
            GROUP BY 1"""
    pop = con.sql(q).df()
    print(f"population: {len(pop):,} distinct weak lines ({pop.lines.sum():,} lines); by method:")
    print(pop.groupby("match_method").lines.agg(["count", "sum"]).to_string())
    return pop


def sample():
    con = con_db()
    pop = population(con)
    import numpy as np
    rng = np.random.default_rng(9)
    parts = []
    for m, n in (("unmatched", 60), ("substring", 70), ("normalised", 20), ("fuzzy", 20)):
        sub = pop[pop.match_method == m].reset_index(drop=True)
        if sub.empty:
            continue
        w = sub.lines.to_numpy(dtype="float64") ** 0.5
        parts.append(sub.iloc[rng.choice(len(sub), min(n, len(sub)), replace=False, p=w / w.sum())])
    import pandas as pd
    s = pd.concat(parts)
    cands = Candidates(con)
    s["candidates"] = [cands(t, c) for t, c in zip(s.raw_text, s.ingredient_id)]
    s.to_json(f"{BASE}/refs/w3_sample.jsonl", orient="records", lines=True, force_ascii=False)
    pop.to_json(f"{BASE}/refs/w3_population.jsonl", orient="records", lines=True, force_ascii=False)
    print(f"{len(s)} lines -> refs/w3_sample.jsonl")


async def run(models):
    rows = load(f"{BASE}/refs/w3_sample.jsonl")
    con = con_db()
    cands = Candidates(con)
    from resolve import IngredientResolver
    ir = IngredientResolver(con)

    async def one(m):
        llm = LLM(m, workers=24)
        res = await llm.map(SYSTEM, [render(r, cands) for r in rows], IngMatch, VERSION, progress=False)
        with open(f"{RUNS}/w3_{m}.jsonl", "w", encoding="utf-8") as f:
            for r, x in zip(rows, res):
                d = x.data or {}
                final = d.get("choice") if d.get("choice") in r["candidates"] else None
                if final is None and d.get("kind") in ("ingredient", "several_ingredients") and d.get("name_en"):
                    g = ir.by_text(d["name_en"], "en", fuzzy=False)
                    final = g[0] if g and g[1] in ("exact", "normalised", "manual") else None
                f.write(json.dumps({"raw_text": r["raw_text"], "data": x.data, "final": final, "error": x.error,
                                    "tokens_in": x.tokens_in, "tokens_out": x.tokens_out}, ensure_ascii=False) + "\n")
        print(f"w3_{m}: {summary(res)}", flush=True)

    await asyncio.gather(*(one(m) for m in models))


def score():
    rows = {r["raw_text"]: r for r in load(f"{BASE}/refs/w3_sample.jsonl")}
    gold = {}
    for p in glob.glob(f"{BASE}/refs/w3_labels_*.jsonl"):
        for x in load(p):
            gold[x["raw_text"]] = x["label"]
    rp = f"{BASE}/refs/w3_review.json"
    alts = {r["id"]: set(r.get("also_ok", [])) for r in (json.load(open(rp)) if os.path.exists(rp) else [])}
    print(f"gold labels: {len(gold)}; {len(alts)} ambiguous lines accept an alternative id (refs/w3_review.json)")
    cols = ["n", "id_acc", "id_acc_food", "food_lines_wrong", "not_food_detect_F1", "kind_acc", "acc_unmatched",
            "acc_substring", "acc_normalised", "acc_fuzzy", "usd_per_1k"]
    lines = ["| run | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    preds = {"current matcher": {k: {"final": r["ingredient_id"]} for k, r in rows.items()}}
    costs = {}
    for path in sorted(glob.glob(f"{RUNS}/w3_*.jsonl")):
        m = os.path.basename(path)[3:-6]
        recs = load(path)
        preds[m] = {x["raw_text"]: {"final": x["final"], **(x["data"] or {})} for x in recs}
        pin, pout = PRICES.get(m, (0, 0))
        costs[m] = sum(x["tokens_in"] * pin + x["tokens_out"] * pout for x in recs) / 1e6 / len(recs) * 1000
    from w1_run import binary
    nf = lambda k: k in ("header_or_note", "non_food_item", "prepared_component")  # noqa: E731
    for name, pred in preds.items():
        ks = [k for k in gold if k in pred]
        ok = {k: (pred[k]["final"] or None) in ({gold[k]["ingredient_id"] or None} | alts.get(k, set())) for k in ks}
        out = {"n": len(ks), "usd_per_1k": costs.get(name, "")}
        out["id_acc"] = sum(ok.values()) / len(ks)
        food = [k for k in ks if gold[k]["ingredient_id"]]
        out["id_acc_food"] = sum(ok[k] for k in food) / len(food)
        out["food_lines_wrong"] = sum(1 for k in food if pred[k]["final"] and not ok[k])
        for m in ("unmatched", "substring", "normalised", "fuzzy"):
            km = [k for k in ks if rows[k]["match_method"] == m]
            out[f"acc_{m}"] = sum(ok[k] for k in km) / max(1, len(km))
        if "kind" in pred[ks[0]]:
            out["kind_acc"] = sum(gold[k]["kind"] == pred[k].get("kind") for k in ks) / len(ks)
            out["not_food_detect_F1"] = binary([nf(gold[k]["kind"]) for k in ks], [nf(pred[k].get("kind")) for k in ks])[2]
        lines.append(f"| {name} | " + " | ".join(f"{out[c]:.3f}" if isinstance(out.get(c), float) else str(out.get(c, ""))
                                                for c in cols) + " |")
    text = "\n".join(lines)
    print(text)
    open(f"{RUNS}/w3_scores.md", "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "run", "score"])
    ap.add_argument("--models", nargs="*", default=MODELS)
    a = ap.parse_args()
    {"sample": sample, "run": lambda: asyncio.run(run(a.models)), "score": score}[a.cmd]()


if __name__ == "__main__":
    main()
