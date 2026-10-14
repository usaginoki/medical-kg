"""W1b: does the case text already give away the conclusion? A narrow follow-up to W1, whose `answer_leak` field
is rarely set by the small models.

  uv run db/llm/w1b_leak.py [--models ...]     # runs on the W1 sample and scores against the W1 reference labels
"""
import argparse, asyncio, glob, json, os, sys
from typing import Literal

from pydantic import BaseModel, Field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import LLM, PRICES  # noqa: E402
from w1_run import BASE, binary, load  # noqa: E402

VERSION = "w1b-v1"


class Leak(BaseModel):
    evidence: str = Field(description="the words in the case that state or nearly state the conclusion, or ''")
    leak: Literal["explicit", "partial", "none"]


SYSTEM = """You check benchmark items for answer leakage. Given a CASE (shown to the model under test) and the gold
CONCLUSION, decide whether the CASE already states the conclusion's main answer (diagnosis, disease name, ICD
category, TCM disease / syndrome name, formula or decision), in any language or abbreviation.
explicit = the case names the same diagnosis / syndrome / formula (e.g. the history says "СД 2 типа" and the answer
           is E11 Type 2 diabetes; a TCM record that already names the syndrome or formula; "biopsy showed
           keratoacanthoma").
partial  = the case names it one step away (the parent category, the organism genus, the disease without its
           subtype, a prior diagnosis of the same condition) so the item becomes much easier.
none     = the conclusion has to be inferred.
Symptoms that happen to share a word with a TCM disease name (便秘, 咳嗽) do not count as a leak unless the case calls
it the diagnosis. Quote the evidence first, then decide."""


def render(r):
    return f"CASE:\n{r['case']}\n\nCONCLUSION:\n{r['conclusion']}"


async def main_async(models):
    rows = load(f"{BASE}/refs/w1_sample.jsonl")
    gold = {}
    for p in glob.glob(f"{BASE}/refs/w1_labels_*.jsonl"):
        for x in load(p):
            gold[x["case_id"]] = x["label"]["answer_leak"]
    for m in models:
        llm = LLM(m, workers=8 if m.startswith("gemma") else 24)
        res = await llm.map(SYSTEM, [render(r) for r in rows], Leak, VERSION, progress=False)
        pin, pout = PRICES.get(m, (0, 0))
        ids = [r["case_id"] for r in rows]
        for name, pos in (("explicit+partial", {"explicit", "partial"}), ("explicit", {"explicit"})):
            pred = [bool(x.data and x.data["leak"] in pos) for x in res]
            p, r, f = binary([gold[i] for i in ids], pred)
            print(f"{m} [{name}]: P={p:.2f} R={r:.2f} F1={f:.2f}  (pred {sum(pred)}, gold {sum(gold.values())})")
        usd = sum(x.tokens_in * pin + x.tokens_out * pout for x in res) / 1e6
        print(f"  valid {sum(x.data is not None for x in res)}/{len(res)}, ${usd / len(res) * 1000:.3f} per 1k")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=["gemini-3.1-flash-lite", "gemini-3.5-flash-lite"])
    asyncio.run(main_async(ap.parse_args().models))
