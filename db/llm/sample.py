"""Draw the stratified reference samples for the LLM experiments into .cache/llm/refs/ (git-ignored).

  uv run db/llm/sample.py w1     # ~145 cases across datasets and screen outcomes -> refs/w1_sample.jsonl

MedArabiQ is left out of everything sent to the API (its licence allows internal research only).
"""
import json, os, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from export import OUT  # noqa: E402

REFS = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".cache", "llm", "refs"))
SEED = 7


def screen(df):
    """The keyword screen outcome of each case row: strong / weak / diet / negated / none."""
    return df.apply(lambda r: "strong" if r.cue_strength == "strong" else "weak" if r.cue_strength == "weak"
                    else "diet" if r.diet else "negated" if r.cues_negated else "none", axis=1)


def take(df, n, **eq):
    sub = df
    for k, v in eq.items():
        sub = sub[sub[k].isin(v if isinstance(v, list) else [v])]
    return sub.sample(min(n, len(sub)), random_state=SEED)


def w1():
    df = pd.read_parquet(f"{OUT}/cases.parquet")
    df = df[df.source != "MedArabiQ"]
    df["screen"] = screen(df)
    parts = [
        take(df, 20, source="MedCaseReasoning", screen="strong"),
        take(df, 12, source="MedCaseReasoning", screen="weak"),
        take(df, 8, source="MedCaseReasoning", screen="diet"),
        take(df, 5, source="MedCaseReasoning", screen="negated"),
        take(df, 8, source="MedCaseReasoning", screen="none"),
        take(df, 10, source="RuMedBench", screen=["strong", "weak"]),
        take(df, 6, source="RuMedBench", screen="diet"),
        take(df, 4, source="RuMedBench", screen="negated"),
        take(df, 4, source="RuMedBench", screen="none"),
        take(df, 15, source="MTCMB"),
        take(df, 10, source="TCM-BEST4SDT"),
        take(df, 4, source="FAM-Bench", screen="strong"),
        take(df, 4, source="FAM-Bench", screen=["diet", "none", "negated"]),
        take(df, 4, source="NGQA", screen="strong"),
        take(df, 4, source="NGQA", screen=["diet", "none", "negated"]),
        take(df, 3, source="ISSAI Dietary Recommendation profiles", lang="ru"),
        take(df, 3, source="ISSAI Dietary Recommendation profiles", lang="kk"),
        take(df, 3, source="ISSAI Dietary Recommendation profiles", lang="en"),
        take(df, 5, source="PerMedCQA"),
        take(df, 5, source="Rezaei2026"),
        take(df, 3, source="MedicationQA", screen=["diet", "strong"]),
        take(df, 3, source="MedicationQA", screen="none"),
    ]
    s = pd.concat(parts).drop_duplicates("case_id")
    os.makedirs(REFS, exist_ok=True)
    path = f"{REFS}/w1_sample.jsonl"
    cols = ["case_id", "source", "part", "lang", "origin", "screen", "cue_strength", "cue_hits", "cues_negated", "diet",
            "relevance", "case", "conclusion"]
    with open(path, "w", encoding="utf-8") as f:
        for r in s[cols].to_dict("records"):
            f.write(json.dumps(r, ensure_ascii=False, default=bool) + "\n")
    print(f"{len(s)} cases -> {path}")
    print(s.groupby(["source", "screen"]).size().to_string())


if __name__ == "__main__":
    {"w1": w1}[sys.argv[1]]()
