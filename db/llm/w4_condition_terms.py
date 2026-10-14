"""W4: map a source's indication / activity term (Dr. Duke, IMPPAT, FooDB health effects) to conditions in the graph,
or say what kind of term it is when it is not a condition.

Generate-then-ground: the model names the conditions in standard (MeSH-style) English; `ground()` maps the names to
condition ids with the build's ConditionResolver, so the model never invents ids.

  UNIFIED_DB=<db> uv run db/llm/w4_condition_terms.py sample     # -> .cache/llm/refs/w4_sample.jsonl
  UNIFIED_DB=<db> uv run db/llm/w4_condition_terms.py run [--models ...]
  UNIFIED_DB=<db> uv run db/llm/w4_condition_terms.py score      # needs refs/w4_labels_*.jsonl
"""
import argparse, asyncio, collections, glob, json, os, random, sys
from typing import Literal

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(HERE, "..", "build"))
from client import LLM, PRICES, summary  # noqa: E402
from w1_run import BASE, RUNS, binary, load, prf  # noqa: E402

VERSION = "w4-v1"
MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-flash-lite"]


class Cond(BaseModel):
    name: str = Field(description="standard English disease / symptom name, MeSH style (e.g. 'Hypertension')")
    relation: Literal["treats_or_prevents", "causes_or_worsens", "marker"]


class TermMap(BaseModel):
    meaning: str = Field(description="short English gloss of the term")
    kind: Literal["condition", "symptom", "pharmacological_action", "body_part_or_organ", "property_or_use",
                  "tcm_or_ayurveda_concept", "not_medical"]
    conditions: list[Cond] = Field(description="0-3 conditions the term points to; [] if none fits")
    evidence_level: Literal["traditional_use", "in_vitro_or_animal", "human_clinical", "unclear"]


SYSTEM = """You normalise terms from food / herb / phytochemical databases for a knowledge graph of conditions
(diseases and symptoms, MeSH vocabulary). Each item gives the SOURCE, the TERM, and how often it occurs.
Return:
meaning: a short English gloss (expand abbreviations; translate Latin / Sanskrit / Indonesian).
kind: condition (a disease) | symptom | pharmacological_action (antihypertensive, ACE-inhibitor, emetic, sedative,
  hepatoprotective) | body_part_or_organ (Liver, Chest: an ethnobotanical use "for the liver") | property_or_use
  (tonic, antioxidant, pesticide, astringent, food use, flavour, poison as a use) | tcm_or_ayurveda_concept (qi
  deficiency, vata dosha) | not_medical.
conditions: the condition(s) the term implies, as standard MeSH-style English names, most specific first, at most 3:
  a disease or symptom term -> itself in standard wording ('Piles' -> 'Hemorrhoids', 'Ache(Head)' -> 'Headache');
  an action -> the condition it acts on ('Antihypertensive' -> Hypertension treats_or_prevents; 'Hepatotoxic' ->
  'Chemical and Drug Induced Liver Injury' causes_or_worsens; 'Emetic' -> 'Vomiting' causes_or_worsens);
  an organ use -> [] unless the source clearly means one disease; a vague property (tonic, antioxidant) -> [].
  relation: treats_or_prevents / causes_or_worsens / marker (the substance is a biomarker of the condition).
evidence_level: what kind of claim such a term usually is in this SOURCE: traditional_use (ethnobotanical,
  Ayurvedic), in_vitro_or_animal (a pharmacological activity measured in the lab), human_clinical, unclear.
Do not invent conditions for terms that do not name one."""


def render(r):
    return f"SOURCE: {r['source']}\nTERM: {r['term']}\nROWS WITH THIS TERM: {r['rows']}"


def resolver():
    import duckdb
    from common import DB_PATH
    from resolve import ConditionResolver
    from links_common import CondText
    con = duckdb.connect(DB_PATH, read_only=True)
    cr = ConditionResolver(con)
    return con, cr, CondText(cr)


def ground(cr, names):
    """Condition ids for model-proposed names (None for a name that does not resolve)."""
    out = []
    for n in names:
        r = cr.by_text_scored(n)
        if r and r[0].startswith("ACT:"):
            out += list(cr.action_targets(r[0]))
        elif r:
            out.append(r[0])
        else:
            out.append(None)
    return out


def population():
    """Every distinct term of the three sources with its current rule-based condition ids (DataFrame)."""
    from common import data
    con, cr, ct = resolver()
    duke = "dr-dukes-phytochemical-and-ethnobotanical-databases"
    terms = collections.Counter()
    for src, path, col, kw in (
            ("Dr. Duke ETHNOBOT (ethnobotanical uses)", data(duke, "ETHNOBOT.csv"), "ACTIVITY", {}),
            ("Dr. Duke AGGREGAC (chemical activities)", data(duke, "AGGREGAC.csv"), "ACTIVITY", {}),
            ("IMPPAT therapeutic uses (Indian medicinal plants)",
             data("imppat", "IMPPAT_TherapeuticUse_Plant_Association.tsv"), "Therapeutic_use", {"sep": "\t"})):
        df = pd.read_csv(path, dtype=str, keep_default_na=False, usecols=[col], **kw)
        for t, n in df[col].value_counts().items():
            if t.strip():
                terms[(src, t.strip())] += int(n)
    recs = []
    for (src, t), n in terms.items():
        h = ct.hits(t, "beneficial")
        recs.append({"source": src, "term": t, "rows": n, "current": sorted({x[0] for x in h}),
                     "current_method": h[0][2] if h else None})
    df = pd.DataFrame(recs)
    print(f"{len(df):,} distinct terms; unmatched {df.current.map(len).eq(0).sum():,} "
          f"({df[df.current.map(len).eq(0)].rows.sum():,} of {df.rows.sum():,} rows)")
    return df


def sample():
    df = population()
    rng = random.Random(5)
    un = df[df.current.map(len).eq(0)]
    ma = df[df.current.map(len).gt(0)]
    pick = []
    for part, n in ((un, 80), (ma, 70)):
        # frequent terms more likely (weight ~ sqrt of rows), so the sample reflects what the rows contain
        w = part.rows.astype(float) ** 0.5
        idx = np.random.default_rng(rng.randint(0, 10**6)).choice(len(part), n, replace=False, p=(w / w.sum()).to_numpy())
        pick.append(part.iloc[idx])
    s = pd.concat(pick)
    os.makedirs(f"{BASE}/refs", exist_ok=True)
    s.to_json(f"{BASE}/refs/w4_sample.jsonl", orient="records", lines=True, force_ascii=False)
    df.to_json(f"{BASE}/refs/w4_population.jsonl", orient="records", lines=True, force_ascii=False)
    print(f"{len(s)} terms -> refs/w4_sample.jsonl (population -> refs/w4_population.jsonl)")


async def run(models):
    rows = load(f"{BASE}/refs/w4_sample.jsonl")
    _, cr, _ = resolver()

    async def one(m):
        llm = LLM(m, workers=8 if m.startswith("gemma") else 24)
        res = await llm.map(SYSTEM, [render(r) for r in rows], TermMap, VERSION, progress=False)
        with open(f"{RUNS}/w4_{m}.jsonl", "w", encoding="utf-8") as f:
            for r, x in zip(rows, res):
                ids = ground(cr, [c["name"] for c in x.data["conditions"]]) if x.data else []
                f.write(json.dumps({"term": r["term"], "source": r["source"], "data": x.data, "grounded": ids,
                                    "error": x.error, "tokens_in": x.tokens_in, "tokens_out": x.tokens_out},
                                   ensure_ascii=False) + "\n")
        print(f"w4_{m}: {summary(res)}", flush=True)

    os.makedirs(RUNS, exist_ok=True)
    await asyncio.gather(*(one(m) for m in models))


def score():
    rows = {(r["source"], r["term"]): r for r in load(f"{BASE}/refs/w4_sample.jsonl")}
    _, cr, _ = resolver()
    gold = {}
    for p in glob.glob(f"{BASE}/refs/w4_labels_*.jsonl"):
        for x in load(p):
            lab = x["label"]
            lab["ids"] = {i for i in ground(cr, [c["name"] for c in lab["conditions"]]) if i}
            gold[(x["source"], x["term"])] = lab
    rp = f"{BASE}/refs/w4_review.json"
    alts = {}
    for r in (json.load(open(rp)) if os.path.exists(rp) else []):
        k = tuple(r["id"])
        if k not in gold:
            continue
        if r["verdict"] == "gold_wrong":
            gold[k]["ids"] = {i for i in ground(cr, r["set_names"]) if i}
        else:
            alts[k] = [set(a) for a in r["also_ok"]]
    print(f"review: {len(alts)} ambiguous terms accept an alternative id set (refs/w4_review.json)")
    print(f"gold labels: {len(gold)}; gold names that do not ground: "
          f"{sum(1 for g in gold.values() for i in ground(cr, [c['name'] for c in g['conditions']]) if i is None)}")
    cols = ["n", "kind_acc", "has_cond_F1", "ids_P", "ids_R", "ids_F1", "unmatched_recovered", "matched_agree",
            "evidence_acc", "usd_per_1k"]
    lines = ["| run | " + " | ".join(cols) + " |", "|---|" + "---|" * len(cols)]
    # the current rule-based resolver as a baseline
    preds = {"current resolver": {k: {"ids": set(r["current"]), "kind": None, "evidence_level": None}
                                  for k, r in rows.items()}}
    costs = {}
    for path in sorted(glob.glob(f"{RUNS}/w4_*.jsonl")):
        m = os.path.basename(path)[3:-6]
        recs = load(path)
        preds[m] = {(x["source"], x["term"]): {"ids": {i for i in x["grounded"] if i}, **(x["data"] or {})}
                    for x in recs}
        pin, pout = PRICES.get(m, (0, 0))
        costs[m] = sum(x["tokens_in"] * pin + x["tokens_out"] * pout for x in recs) / 1e6 / len(recs) * 1000
    for m in [m for m in list(preds) if m != "current resolver"]:  # resolver first, the model only for its misses
        preds[f"resolver + {m} on misses"] = {k: ({"ids": set(rows[k]["current"])} if rows[k]["current"] else preds[m][k])
                                              for k in preds[m]}
        costs[f"resolver + {m} on misses"] = costs[m]
    for name, pred in preds.items():
        ks = [k for k in gold if k in pred]
        tp = fp = fn = 0
        best = {}
        for k in ks:
            p = pred[k]["ids"]
            # the acceptable id set closest to the prediction (fewest errors)
            g = min([gold[k]["ids"]] + alts.get(k, []), key=lambda a: len(a ^ p))
            best[k] = g
            tp, fp, fn = tp + len(g & p), fp + len(p - g), fn + len(g - p)
        out = {"n": len(ks)}
        out["ids_P"], out["ids_R"], out["ids_F1"] = prf(tp, fp, fn)
        out["has_cond_F1"] = binary([bool(best[k]) for k in ks], [bool(pred[k]["ids"]) for k in ks])[2]
        if all(pred[k].get("kind") for k in ks):
            out["kind_acc"] = sum(gold[k]["kind"] == pred[k]["kind"] for k in ks) / len(ks)
            out["evidence_acc"] = sum(gold[k]["evidence_level"] == pred[k]["evidence_level"] for k in ks) / len(ks)
        un = [k for k in ks if not rows[k]["current"] and gold[k]["ids"]]
        out["unmatched_recovered"] = (f"{sum(bool(best[k] & pred[k]['ids']) for k in un)}/{len(un)}")
        ma = [k for k in ks if rows[k]["current"]]
        out["matched_agree"] = f"{sum(best[k] == pred[k]['ids'] for k in ma)}/{len(ma)}"
        out["usd_per_1k"] = costs.get(name, "")
        lines.append(f"| {name} | " + " | ".join(f"{out[c]:.3f}" if isinstance(out.get(c), float) else str(out.get(c, ""))
                                                for c in cols) + " |")
    text = "\n".join(lines)
    print(text)
    open(f"{RUNS}/w4_scores.md", "w").write(text + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["sample", "run", "score"])
    ap.add_argument("--models", nargs="*", default=MODELS)
    a = ap.parse_args()
    if a.cmd == "sample":
        sample()
    elif a.cmd == "run":
        asyncio.run(run(a.models))
    else:
        score()


if __name__ == "__main__":
    main()
