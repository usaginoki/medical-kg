"""Combine the downloaded patient-case datasets into one flat table: a case and its gold conclusion.

Usage:
  uv run db/fetch.py medicationqa ngqa tcm_best4sdt mtcmb medcasereasoning rumedbench medarabiq fam_bench
  uv run db/cases.py                 # writes db/export/cases.parquet + cases.csv

  case_id     <dataset>:[<part>:]<id in the source file>, unique
  source      dataset note name (Datasets/<source>.md)
  case        what is put to the model: patient text, profile or dish + question, in the dataset's own language
  conclusion  the dataset's gold answer: diagnosis, ICD-10 code, TCM syndrome / formula, doctor's answer, decision

Only datasets with a gold conclusion are read (Questions/Q4 Patient case-conclusion datasets.md); the ISSAI profiles
are left out because their answers are GPT-4 outputs. Texts are copied as they are (50 TCM-BEST4SDT cases contain a
literal '\\n', as in the source file). Where a source stores the case or the answer as fields, the fields are written
one per line as "field: value" with the source's own field names; every choice of fields is listed per source below. Some rows are not redistributable (MedArabiQ licence: internal research
only), so the export stays out of git.
"""
import ast, json, os, re, sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
from export import OUT, add_bom  # noqa: E402

READERS = {}


def reader(fn):
    READERS[fn.__name__] = fn
    return fn


def jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def fields(d, sep="："):
    """Dict as 'key：value' lines (Chinese full-width colon for the TCM sets, as in their own files)."""
    return "\n".join(f"{k}{sep}{v}" for k, v in d.items() if v not in (None, "", [], {}))


@reader
def rumedbench():
    """RuMedTop3: real outpatient complaints (Russian) -> the doctor's ICD-10 code. All splits have the code."""
    rows = []
    for split in ("train", "dev", "test"):
        for r in jsonl(f"{DATA}/rumedbench/medbench/data/RuMedTop3/{split}_v1.jsonl"):
            rows.append((f"rumedbench:top3-{split}:{r['idx']}", "RuMedBench", r["symptoms"], f"ICD-10: {r['code']}"))
    return rows


@reader
def medcasereasoning():
    """PMC case reports: case_prompt -> final_diagnosis (the reasoning column is left out)."""
    rows = []
    for split in ("train", "val", "test"):
        df = pd.read_parquet(f"{DATA}/medcasereasoning/data/{split}-00000-of-00001.parquet",
                             columns=["pmcid", "case_prompt", "final_diagnosis"])
        rows += [(f"medcasereasoning:{split}:{r.pmcid}", "MedCaseReasoning", r.case_prompt, r.final_diagnosis)
                 for r in df.itertuples()]
    return rows


@reader
def tcm_best4sdt():
    """The 300 open TCM cases (ids 201-500): instruction -> 中医疾病诊断 + the output lines, without the
    multiple-choice key lines (…答案 / …选项). The other 300 items are exam questions, not cases."""
    rows = []
    for r in json.load(open(f"{DATA}/tcm-best4sdt/TCM-BEST4SDT.json", encoding="utf-8")):
        if "instruction" not in r:
            continue
        lines = [f"中医疾病诊断：{r['中医疾病诊断']}"] if r.get("中医疾病诊断") else []
        lines += [x for x in r["output"] if not re.match(r"^[^：]*(答案|选项)：", x)]
        rows.append((f"tcm-best4sdt:{r['id']}", "TCM-BEST4SDT", r["instruction"], "\n".join(lines)))
    return rows


@reader
def mtcmb():
    """MSDD (case record -> 证型 + 疾病), PR (case record -> prescribed herbs) and Diagnosis + FRD (same 200 symptom
    lists by id -> disease, syndrome elements, treatment, formula, herbs; merged into one case)."""
    base = f"{DATA}/mtcmb/data"
    rows = []
    for r in jsonl(f"{base}/TCM-MSDD.jsonl"):
        rows.append((f"mtcmb:msdd:{r['id']}", "MTCMB", fields(r["disease_case"]), fields(r["answer"])))
    for r in jsonl(f"{base}/TCM-PR.jsonl"):
        herbs = r["answer"]
        herbs = ast.literal_eval(herbs) if isinstance(herbs, str) else herbs
        rows.append((f"mtcmb:pr:{r['id']}", "MTCMB", fields(r["disease_case"]), "、".join(herbs)))
    frd = {r["id"]: r for r in jsonl(f"{base}/TCM-FRD.jsonl")}
    for r in jsonl(f"{base}/TCM-Diagnosis.jsonl"):
        f = frd.get(r["id"])
        if f is not None and f["question"] != r["question"]:
            raise ValueError(f"MTCMB Diagnosis/FRD id {r['id']}: different questions")
        answer = {**r["answer"], **(f["answer"] if f else {})}
        rows.append((f"mtcmb:diagnosis-frd:{r['id']}", "MTCMB", r["question"], fields(answer)))
    return rows


@reader
def medarabiq():
    """The original patient–doctor QA set (Arabic): Question_description -> Answer_details. The other six MedArabiQ
    files are exam MCQs or LLM-modified copies. Licence: no redistribution."""
    df = pd.read_csv(f"{DATA}/medarabiq/datasets/patient-doctor-qa.csv")
    return [(f"medarabiq:patient-doctor-qa:{i}", "MedArabiQ", r.Question_description, r.Answer_details)
            for i, r in enumerate(df.itertuples())]


@reader
def fam_bench():
    """Task 1 (dish suitability): the fields the official runner sends to the model (run_q2._build_prompt_payload:
    title, question, ingredients, nutrition, dietary_tags, meal_type, notes) -> the standard answer's decision and
    per-condition rationale. Task 2 (comparisons between dishes) is not a case set."""
    rows = []
    for i, r in enumerate(json.load(open(f"{DATA}/fam-bench/dataset/task1_dish_suitability.json", encoding="utf-8"))):
        nutrition = ", ".join(f"{k} {v}" for k, v in (r.get("nutrition") or {}).items() if v is not None)
        case = fields({"title": r.get("title"), "question": r.get("question"),
                       "ingredients": "; ".join(r.get("ingredients") or []), "nutrition": nutrition,
                       "dietary_tags": ", ".join(r.get("dietary_tags") or []),
                       "meal_type": ", ".join(r.get("meal_type") or []), "notes": r.get("notes")}, ": ")
        a = r["standard answer"]
        lines = [f"decision: {a['decision']}"]
        lines += [f"{x['condition']} ({', '.join(x.get('ingredients') or [])}): {x.get('reasoning', '')}".rstrip(": ")
                  for x in a.get("rationale_ingredients") or []]
        rows.append((f"fam-bench:task1:{i}", "FAM-Bench", case, "\n".join(lines)))
    return rows


@reader
def ngqa():
    """NHANES user + FNDDS food graph: the user's status and dietary-habit nodes, the food with its category and
    ingredients, and question_hard -> answer_hard. The nutrition-tag nodes and match/contradict/need edges are left
    out: they are the reasoning the answer is checked against."""
    df = pd.read_csv(f"{DATA}/ngqa/processed_data/NGQA_benchmark.csv",
                     usecols=["node_list", "question_hard", "answer_hard"])
    rows = []
    for i, r in enumerate(df.itertuples()):
        nodes = dict(ast.literal_eval(r.node_list))
        by = lambda kind: [v["attr"] for v in nodes.values() if v["name"] == kind]  # noqa: E731
        case = fields({"food": nodes[1]["attr"], "category": "; ".join(by("category")),
                       "ingredients": "; ".join(by("ingredient")), "user status": "; ".join(by("status")),
                       "user dietary habits": "; ".join(by("dietary habit")), "question": r.question_hard}, ": ")
        rows.append((f"ngqa:{i}", "NGQA", case, r.answer_hard.strip()))
    return rows


@reader
def medicationqa():
    """Consumer medication questions -> answer passage from a trusted website. The id is the row's 1-based position,
    the `#n` of the dataset note. The 10 rows without an answer ('No answers', one empty) are skipped; the 3
    'Unanswerable' rows are the source's gold answer and are kept."""
    df = pd.read_excel(f"{DATA}/medicationqa/MedInfo2019-QA-Medications.xlsx")
    return [(f"medicationqa:{i}", "MedicationQA", r.Question, r.Answer)
            for i, r in enumerate(df.itertuples(), start=1)
            if isinstance(r.Answer, str) and r.Answer.strip().lower() not in ("", "no answers")]


def main():
    frames = []
    for name, fn in READERS.items():
        df = pd.DataFrame(fn(), columns=["case_id", "source", "case", "conclusion"])
        df = df[df.case.astype(str).str.strip().ne("") & df.conclusion.astype(str).str.strip().ne("")]
        print(f"  {name:18} {len(df):>6,}")
        frames.append(df)
    cases = pd.concat(frames, ignore_index=True)
    dup = cases.case_id[cases.case_id.duplicated()]
    if len(dup):
        raise ValueError(f"duplicate case_id: {dup.head().tolist()}")
    os.makedirs(OUT, exist_ok=True)
    cases.to_parquet(f"{OUT}/cases.parquet", index=False)
    cases.to_csv(f"{OUT}/cases.tmp.csv", index=False)
    add_bom(f"{OUT}/cases.tmp.csv", f"{OUT}/cases.csv")
    print(f"  {'total':18} {len(cases):>6,}  -> {os.path.relpath(OUT)}/cases.parquet, cases.csv")


if __name__ == "__main__":
    main()
