"""Combine the downloaded patient-case datasets into one flat table: a case, its conclusion, where both come from
and how relevant the case is for testing a culturally aware medical agent.

Usage:
  uv run db/fetch.py medicationqa ngqa tcm_best4sdt mtcmb medcasereasoning rumedbench medarabiq fam_bench \\
                     issai_diet permedcqa rezaei2026
  uv run db/prep.py issai
  uv run db/cases.py                 # writes db/export/cases.parquet + cases.csv

  case_id      <dataset>:[<part>:]<id in the source file>, unique
  source       dataset note name (Datasets/<source>.md; PerMedCQA and Rezaei2026 have Backlog / Papers notes only)
  part         dataset part, the key of PARTS below
  lang         language of the case text
  origin       where the case comes from (one phrase per part)
  case_ai      is the case text AI-written: no | ai-rewritten | ai-generated | not stated
  conclusion_ai  is the conclusion AI-made: no | ai-extracted | ai-proposed, expert-checked | rule-derived | ai-generated
  gold         gold | weak gold | ai-generated  (summary of conclusion_ai for filtering)
  relevance    high | medium | low for a culturally aware evaluation, with the reason in relevance_why (see relevance())
  cue_*, culture_by_construction, diet   the flags the relevance is built from (db/cues.py)
  case         what is put to the model: patient text, profile or dish + question, in the dataset's own language
  conclusion   the dataset's answer: diagnosis, ICD-10 code, TCM syndrome / formula, doctor's answer, decision

Datasets without a gold conclusion are included and flagged (`gold`): the ISSAI answers are GPT-4 outputs. Texts are
copied as they are (50 TCM-BEST4SDT cases contain a literal '\\n', as in the source file). Where a source stores the
case or the answer as fields, the fields are written one per line as "field: value" with the source's own field
names; every choice of fields is listed per source below. Some rows are not redistributable (MedArabiQ licence:
internal research only; the Rezaei repository has no licence), so the export stays out of git.
"""
import ast, csv, io, json, os, random, re, sys, zipfile

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402
from export import OUT, add_bom  # noqa: E402
import cues  # noqa: E402

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
    """RuMedTop3: real outpatient visits (Russian) -> the doctor's ICD-10 code. All splits have the code.

    RuMedTop3 keeps only the complaints (`symptoms`) and the code cut to 3 characters. The parent set RuMedPrime
    (Zenodo) has the same visits (idx = new_event_id) with the anamnesis and the full code, so both are added: the
    case is complaints + anamnesis, the conclusion is the 3-character code with its WHO ICD-10 title plus the full
    code. Without the RuMedPrime zip the case is the complaints alone. Titles: maps/icd10_titles.csv."""
    titles = dict(csv.reader(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "maps", "icd10_titles.csv"),
                              encoding="utf-8")))
    named = lambda c: f"{c} ({titles[c]})" if c in titles else c  # noqa: E731
    prime = {}
    zpath = f"{DATA}/rumedbench/zenodo/RuMedPrimeData.zip"
    if os.path.exists(zpath):
        with zipfile.ZipFile(zpath) as z:
            p = pd.read_csv(io.BytesIO(z.read("RuMedPrimeData.tsv")), sep="\t").fillna("")
        prime = {r.new_event_id: r for r in p.itertuples()}
    else:
        print("  rumedbench: RuMedPrimeData.zip missing, cases are complaints only (uv run db/fetch.py rumedbench)")
    rows = []
    for split in ("train", "dev", "test"):
        for r in jsonl(f"{DATA}/rumedbench/medbench/data/RuMedTop3/{split}_v1.jsonl"):
            p = prime.get(r["idx"])
            case, answer = r["symptoms"], f"ICD-10: {named(r['code'])}"
            if p is not None:
                if p.icd10[:3] != r["code"]:
                    raise ValueError(f"RuMedPrime {r['idx']}: code {p.icd10} does not start with {r['code']}")
                case = fields({"Жалобы": r["symptoms"], "Анамнез": p.anamnesis}, ": ")
                if p.icd10 != r["code"]:
                    answer += f"\nfull code: {named(p.icd10)}"
            rows.append((f"rumedbench:top3-{split}:{r['idx']}", "RuMedBench", case, answer, "rumedbench:top3"))
    return rows


@reader
def medcasereasoning():
    """PMC case reports: case_prompt -> final_diagnosis (the reasoning column is left out)."""
    rows = []
    for split in ("train", "val", "test"):
        df = pd.read_parquet(f"{DATA}/medcasereasoning/data/{split}-00000-of-00001.parquet",
                             columns=["pmcid", "case_prompt", "final_diagnosis"])
        rows += [(f"medcasereasoning:{split}:{r.pmcid}", "MedCaseReasoning", r.case_prompt, r.final_diagnosis,
                  "medcasereasoning") for r in df.itertuples()]
    return rows


@reader
def tcm_best4sdt():
    """The 300 open TCM cases (ids 201-500): instruction -> 中医疾病诊断 + the output lines, without the
    multiple-choice key lines (…答案 / …选项). The other 300 items are exam questions, not cases. The three parts
    follow the id ranges of the dataset note (inferred from the text; the paper gives no split)."""
    rows = []
    for r in json.load(open(f"{DATA}/tcm-best4sdt/TCM-BEST4SDT.json", encoding="utf-8")):
        if "instruction" not in r:
            continue
        lines = [f"中医疾病诊断：{r['中医疾病诊断']}"] if r.get("中医疾病诊断") else []
        lines += [x for x in r["output"] if not re.match(r"^[^：]*(答案|选项)：", x)]
        part = "classical" if r["id"] <= 350 else "clinical" if r["id"] <= 400 else "vignette"
        rows.append((f"tcm-best4sdt:{r['id']}", "TCM-BEST4SDT", r["instruction"], "\n".join(lines),
                     f"tcm-best4sdt:{part}"))
    return rows


@reader
def mtcmb():
    """MSDD (case record -> 证型 + 疾病), PR (case record -> prescribed herbs) and Diagnosis + FRD (same 200 symptom
    lists by id -> disease, syndrome elements, treatment, formula, herbs; merged into one case). CHGD (doctor–patient
    dialogue written by DeepSeek-R1 -> structured record) and TCMeEE (case record -> extracted entities, an
    LLM-written reference) are the two parts with AI-made text."""
    base = f"{DATA}/mtcmb/data"
    rows = []
    for r in jsonl(f"{base}/TCM-MSDD.jsonl"):
        rows.append((f"mtcmb:msdd:{r['id']}", "MTCMB", fields(r["disease_case"]), fields(r["answer"]), "mtcmb:msdd"))
    for r in jsonl(f"{base}/TCM-PR.jsonl"):
        herbs = r["answer"]
        herbs = ast.literal_eval(herbs) if isinstance(herbs, str) else herbs
        rows.append((f"mtcmb:pr:{r['id']}", "MTCMB", fields(r["disease_case"]), "、".join(herbs), "mtcmb:pr"))
    frd = {r["id"]: r for r in jsonl(f"{base}/TCM-FRD.jsonl")}
    for r in jsonl(f"{base}/TCM-Diagnosis.jsonl"):
        f = frd.get(r["id"])
        if f is not None and f["question"] != r["question"]:
            raise ValueError(f"MTCMB Diagnosis/FRD id {r['id']}: different questions")
        answer = {**r["answer"], **(f["answer"] if f else {})}
        rows.append((f"mtcmb:diagnosis-frd:{r['id']}", "MTCMB", r["question"], fields(answer), "mtcmb:diagnosis-frd"))
    for r in jsonl(f"{base}/TCM-CHGD.jsonl"):
        rows.append((f"mtcmb:chgd:{r['id']}", "MTCMB", r["dialogue"], r["answer"], "mtcmb:chgd"))
    for r in jsonl(f"{base}/TCMeEE.jsonl"):
        answer = r["answer"]
        try:
            answer = fields(json.loads(answer), ": ")
        except (TypeError, ValueError):
            pass  # keep the source string when it is not valid JSON
        rows.append((f"mtcmb:tcmeee:{r['id']}", "MTCMB", r["Medical_case"], answer, "mtcmb:tcmeee"))
    return rows


@reader
def medarabiq():
    """The patient–doctor QA set (Arabic), 100 questions in three versions with the same row order: original
    (Question_description -> Answer_details), machine grammar-corrected (-gec: question and answer) and GPT-4o
    paraphrase of the question (-llm: answer unchanged). The other four MedArabiQ files are exam items.
    Licence: no redistribution."""
    rows = []
    for name, qcol, acol in (("patient-doctor-qa", "Question_description", "Answer_details"),
                             ("patient-doctor-qa-gec", "GEC Question description", "GEC Answer details"),
                             ("patient-doctor-qa-llm", "Modified question description", "Unmodified answer")):
        df = pd.read_csv(f"{DATA}/medarabiq/datasets/{name}.csv")
        rows += [(f"medarabiq:{name}:{i}", "MedArabiQ", q, a, f"medarabiq:{name}")
                 for i, (q, a) in enumerate(zip(df[qcol], df[acol]))]
    return rows


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
        rows.append((f"fam-bench:task1:{i}", "FAM-Bench", case, "\n".join(lines), "fam-bench:task1"))
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
        rows.append((f"ngqa:{i}", "NGQA", case, r.answer_hard.strip(), "ngqa"))
    return rows


@reader
def medicationqa():
    """Consumer medication questions -> answer passage from a trusted website. The id is the row's 1-based position,
    the `#n` of the dataset note. The 10 rows without an answer ('No answers', one empty) are skipped; the 3
    'Unanswerable' rows are the source's gold answer and are kept."""
    df = pd.read_excel(f"{DATA}/medicationqa/MedInfo2019-QA-Medications.xlsx")
    return [(f"medicationqa:{i}", "MedicationQA", r.Question, r.Answer, "medicationqa")
            for i, r in enumerate(df.itertuples(), start=1)
            if isinstance(r.Answer, str) and r.Answer.strip().lower() not in ("", "no answers")]


@reader
def issai():
    """50 mock Kazakh patient profiles in five language pipelines (derived/cases_responses.csv, db/prep_issai.py):
    profile -> GPT-4's recommendations + one-day meal plan. The conclusion is a model output, not gold."""
    df = pd.read_csv(f"{DATA}/issai-dietary-recommendation/derived/cases_responses.csv").fillna("")
    rows = []
    for r in df.itertuples():
        answer = "\n\n".join(x for x in (r.gpt4_recommendations, r.gpt4_meal_plan) if x.strip())
        rows.append((f"issai:{r.language}-{r.pipeline}:{r.case_id}", "ISSAI Dietary Recommendation profiles",
                     r.profile, answer, f"issai:{r.language}-{r.pipeline}"))
    return rows


@reader
def permedcqa(n=10, seed=0):
    """A sample of n real Iranian patient questions (Persian) -> physician answer, drawn with a fixed seed from the
    questions whose text carries a religion, food, habit or traditional-medicine cue (db/cues.py)."""
    recs = []
    for split in ("train", "test"):
        recs += json.load(open(f"{DATA}/permedcqa/Data/{split}.json", encoding="utf-8"))
    df = pd.DataFrame(recs).fillna("")
    df = df[df.Question.astype(str).str.strip().ne("") & df.Expert_Answer.astype(str).str.strip().ne("")]
    probe = cues.tag(pd.DataFrame({"source": "PerMedCQA", "lang": "fa", "case": df.Question.astype(str)}))
    keep = probe[["cue_religion", "cue_food", "cue_habit", "cue_tradmed"]].any(axis=1).to_numpy()
    df = df[keep].sort_values("instance_id").sample(n, random_state=seed).sort_values("instance_id")
    return [(f"permedcqa:{r['instance_id']}", "PerMedCQA",
             fields({"Sex": r["Sex"], "Age": r["Age"], "Specialty": r["Specialty"], "Question": r["Question"]}, ": "),
             r["Expert_Answer"], "permedcqa") for r in df.to_dict("records")]


REZAEI_SKIP = {3, 20, 80, 90, 134, 141}  # items whose variants lose a decisive cue or leak the answer (paper note)


@reader
def rezaei2026(n=10, seed=0):
    """A sample of n culturally augmented MedQA items (Rezaei & Shakeri 2026): one variant each from n different
    items, cycling through the three groups (t1 Indigenous Canadian, t2 Middle-Eastern Muslim, t3 Southeast Asian)
    and the three cue types (i identifier, c context, ic both). Case = variant stem + options; conclusion = the
    MedQA key. Items are numbered from 1 in file order."""
    data = json.load(open(f"{DATA}/rezaei2026/final_augment_test_questions.json", encoding="utf-8"))
    items = [i for i in range(1, len(data) + 1) if i not in REZAEI_SKIP and i - 1 not in REZAEI_SKIP]
    combos = [(t, c) for c in ("ic", "c", "i") for t in ("t2", "t3", "t1")]
    rows = []
    for k, i in enumerate(sorted(random.Random(seed).sample(items, n))):
        r = data[i - 1]
        t, c = combos[k % len(combos)]
        case = r[f"{t}_question"][c] + "\n" + "\n".join(f"{o}. {v}" for o, v in r["options"].items())
        rows.append((f"rezaei2026:{i}:{t}-{c}", "Rezaei2026", case, f"{r['answer_idx']}. {r['answer']}", "rezaei2026"))
    return rows


def P(lang, origin, case_ai, conclusion_ai, gold, gold_note, culture=None, diet=False):
    return dict(lang=lang, origin=origin, case_ai=case_ai, conclusion_ai=conclusion_ai, gold=gold,
                gold_note=gold_note, culture=culture, diet=diet, tradmed=culture == "TCM case")


# Provenance of every part, from the dataset notes in Datasets/ (and the paper notes for PerMedCQA and Rezaei2026).
# culture: why the whole part is tied to a culture even when no keyword matches; diet: the part is about food.
# TCM parts count as traditional-medicine content throughout (their conclusions are syndromes, formulas and herbs).
PARTS = {
    "rumedbench:top3": P("ru", "real outpatient visit record (complaints + anamnesis), university hospital in Tomsk (Russia)", "no", "no", "gold",
                         "the doctor's ICD-10 code (title added from the WHO ICD-10 list)"),
    "medcasereasoning": P("en", "published case report (PubMed Central, authors worldwide)", "ai-rewritten",
                          "ai-extracted", "gold",
                          "the report's final diagnosis, extracted by an LLM (100 cases physician-checked)"),
    "tcm-best4sdt:classical": P("zh", "classical TCM case record retold in modern Chinese", "not stated", "no", "gold",
                                "expert-annotated syndrome → prescription chain", culture="TCM case"),
    "tcm-best4sdt:clinical": P("zh", "modern dated clinical record, TCM hospital (China)", "no", "no", "gold",
                               "expert-annotated syndrome → prescription chain", culture="TCM case"),
    "tcm-best4sdt:vignette": P("zh", "short modern TCM vignette (China); who wrote it is not stated", "not stated", "no",
                               "gold", "expert-annotated syndrome → prescription chain", culture="TCM case"),
    "mtcmb:msdd": P("zh", "real TCM electronic medical record (China; CCL25-Eval Task 9)", "no", "no", "gold",
                    "syndrome and disease labels of the record", culture="TCM case"),
    "mtcmb:pr": P("zh", "real TCM electronic medical record (China; CCL25-Eval Task 9)", "no", "no", "gold",
                  "the herbs actually prescribed", culture="TCM case"),
    "mtcmb:diagnosis-frd": P("zh", "TCM textbook case (China, national textbooks)", "no", "no", "gold",
                             "the textbook's diagnosis and treatment", culture="TCM case"),
    "mtcmb:chgd": P("zh", "doctor–patient dialogue written by DeepSeek-R1 from a TCM licensing-exam case", "ai-generated",
                    "no", "gold", "the exam bank's structured record (expert-reviewed)", culture="TCM case"),
    "mtcmb:tcmeee": P("zh", "classical or modern TCM case record (医案) from zhongyigen.com or practitioners", "no",
                      "ai-proposed, expert-checked", "gold",
                      "entities extracted by DeepSeek-R1, expert-reviewed (the conclusion is already in the case text)",
                      culture="TCM case"),
    "medarabiq:patient-doctor-qa": P("ar", "real patient question, Altibbi telehealth forum (Arab region)", "no", "no",
                                     "gold", "the forum doctor's answer"),
    "medarabiq:patient-doctor-qa-gec": P("ar", "real Altibbi patient question, machine grammar-corrected (same 100 "
                                         "questions)", "ai-rewritten", "no", "gold",
                                         "the forum doctor's answer, machine grammar-corrected"),
    "medarabiq:patient-doctor-qa-llm": P("ar", "real Altibbi patient question, paraphrased by GPT-4o (same 100 questions)",
                                         "ai-rewritten", "no", "gold", "the forum doctor's answer (unchanged)"),
    "fam-bench:task1": P("en", "recipe from a health or recipe website (mostly US) + templated condition question", "no",
                         "ai-proposed, expert-checked", "gold",
                         "label proposed by GPT-5.5, rule-checked and confirmed by nutrition experts", diet=True),
    "ngqa": P("en", "real NHANES participant (US) + a food they could eat, in a template", "no", "rule-derived",
              "weak gold", "label computed by rule from nutrient thresholds, no per-item clinical judgement", diet=True),
    "medicationqa": P("en", "real consumer question sent to MedlinePlus (US)", "no", "no", "gold",
                      "reference passage chosen by annotators from trusted websites"),
    "permedcqa": P("fa", "real patient question, Iranian medical Q&A forums", "no", "no", "gold",
                   "the physician's answer"),
    "rezaei2026": P("en", "US licensing-exam vignette (MedQA) with a cultural cue injected by an LLM", "ai-rewritten", "no",
                    "gold", "the MedQA key; one clinician confirmed the cue does not change it",
                    culture="injected cultural cue"),
}
for _lang, _name in (("en", "English"), ("ru", "Russian"), ("kk", "Kazakh")):
    for _pipe in ("direct", "translated"):
        if (_lang, _pipe) == ("en", "translated"):
            continue
        how = "" if _pipe == "direct" else "; answered via machine translation to English and back"
        PARTS[f"issai:{_lang}-{_pipe}"] = P(
            _lang, f"mock patient profile set in Kazakhstan, written by the ISSAI study team ({_name}{how})", "no",
            "ai-generated", "ai-generated", "GPT-4's 2023 advice, not checked by an expert", culture="Kazakh profile",
            diet=True)


def relevance(r):
    """high / medium / low for a culturally aware evaluation, and why.

    cue        a cultural cue is stated in the case, or the part is tied to a culture by construction
    actionable food, diet or herb content the graph can act on (keyword, or a diet / traditional-medicine dataset)
    high   = cue and actionable and a gold conclusion
    medium = exactly one of the two with a gold conclusion, or both without one (weak gold or AI-generated)
    low    = the rest
    """
    p = PARTS[r["part"]]
    found = [f"{c} ({r['m_' + c]})" for c in cues.CUES if r[f"cue_{c}"]]
    cue = bool(found) or bool(p["culture"])
    actionable = bool(r["diet"] or r["cue_tradmed"] or p["diet"] or p["tradmed"])
    if cue and actionable and p["gold"] == "gold":
        level = "high"
    elif (cue != actionable and p["gold"] == "gold") or (cue and actionable):
        level = "medium"
    else:
        level = "low"
    why = ["cue: " + (", ".join(found) if found else "none in the text")
           + (f"; {p['culture']} by construction" if p["culture"] else ""),
           "food / diet / herb content: " + ("diet dataset" if p["diet"] else "traditional-medicine dataset" if p["tradmed"]
                                           else "yes" if actionable else "no"),
           f"{p['gold']}: {p['gold_note']}"]
    return level, "; ".join(why)


COLUMNS = ["case_id", "source", "part", "lang", "origin", "case_ai", "conclusion_ai", "gold", "relevance",
           "relevance_why"] + [f"cue_{c}" for c in cues.CUES] + ["culture_by_construction", "diet", "case", "conclusion"]


def main():
    frames = []
    for name, fn in READERS.items():
        df = pd.DataFrame(fn(), columns=["case_id", "source", "case", "conclusion", "part"])
        df = df[df.case.astype(str).str.strip().ne("") & df.conclusion.astype(str).str.strip().ne("")]
        print(f"  {name:18} {len(df):>6,}")
        frames.append(df)
    cases = pd.concat(frames, ignore_index=True)
    dup = cases.case_id[cases.case_id.duplicated()]
    if len(dup):
        raise ValueError(f"duplicate case_id: {dup.head().tolist()}")
    unknown = set(cases.part) - set(PARTS)
    if unknown:
        raise ValueError(f"parts without provenance: {sorted(unknown)}")
    for col in ("lang", "origin", "case_ai", "conclusion_ai", "gold"):
        cases[col] = cases.part.map(lambda k: PARTS[k][col])
    cases["culture_by_construction"] = cases.part.map(lambda k: bool(PARTS[k]["culture"]))
    cases = cues.tag(cases, keep_matches=True)
    cases["diet"] = cases.diet | cases.part.map(lambda k: PARTS[k]["diet"])
    rel = cases.apply(relevance, axis=1, result_type="expand")
    cases["relevance"], cases["relevance_why"] = rel[0], rel[1]
    cases = cases[COLUMNS]
    os.makedirs(OUT, exist_ok=True)
    cases.to_parquet(f"{OUT}/cases.parquet", index=False)
    cases.to_csv(f"{OUT}/cases.tmp.csv", index=False)
    add_bom(f"{OUT}/cases.tmp.csv", f"{OUT}/cases.csv")
    print(f"  {'total':18} {len(cases):>6,}  -> {os.path.relpath(OUT)}/cases.parquet, cases.csv\n")
    tab = cases.groupby(["source", "gold", "relevance"]).size().unstack(fill_value=0)
    print(tab.reindex(columns=["high", "medium", "low"], fill_value=0).to_string())


if __name__ == "__main__":
    main()
