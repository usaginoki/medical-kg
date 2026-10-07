---
title: "MedArabiQ"
slug: medarabiq
kind: [case]
version: "GitHub main @ 1d3d77a (2025-06-17)"
previous_versions: ""
papers: ["[[AbuDaoud2025 - MedArabiQ Arabic medical benchmark]]"]
url: "https://github.com/nyuad-cai/MedArabiQ"
license: "Custom NYU licence (LICENSE): internal non-commercial research and evaluation only; no rights to sublicense, further distribute or modify. (CC BY-NC-SA 4.0 is the licence of the arXiv paper, not of the data.)"
availability: open-download
access_link: "https://github.com/nyuad-cai/MedArabiQ"
accessed: true
access_method: [github]
access_date: 2026-10-07
access_notes: "git clone --depth 1 (commit 1d3d77a, 2025-06-17) worked without login: all 7 CSVs (7 × 100 rows) + LICENSE + README. Licence forbids further distribution, so Data/medarabiq/sample*.csv were deleted after profiling and example values in schema.md redacted (nothing from the data may go into the public vault repo). Third-party HF copies exist (qimma/MCQ_MedArabiQ, qimma/QA_MedArabiQ, 2026) but were not used."
countries: []
regions: ["[[Middle East]]", "[[North Africa]]"]
n_records: "700 items in 7 CSVs (100 each)"
size: "0.9 MB"
formats: [csv]
join_keys: [Category (specialty), free-text Arabic symptoms/drugs/foods]
case_type: [real]
conclusion_type: [advice, mcq-answer, fill-in]
languages: [ar, en]
n_cases: "100 real patient questions → doctor answers (each in 3 variants: original, grammar-corrected, GPT-4o paraphrase); plus 400 exam/lecture items (200 MCQ, 200 fill-in-the-blank) that are knowledge questions, not cases"
diet_relevance: subset
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases, search/global-cases]
tags:
  - type/dataset
  - kind/case
  - q/4
  - case/real
  - region/middle-east
  - access/accessed
  - access/open
---
# MedArabiQ

> [!abstract] TL;DR
> MedArabiQ (Abu Daoud et al., NYU Abu Dhabi, MLHC 2025) is a small Arabic medical benchmark of **7 × 100 items**:
> 100 MCQs and 100 bias-injected MCQs from past exams of (unnamed) Arab medical schools, 2 × 100 fill-in-the-blank
> items from lecture notes (Arabic + English), and **100 real patient questions from the Altibbi telehealth forum
> (via [[AraMed]]) with the doctor's answer as reference**, in three versions (original, grammar-corrected,
> GPT-4o-paraphrased). Only the patient Q&A is a case → conclusion set (conclusion = advice/triage, scored with
> BERTScore). 18 of the 100 patient cases mention food or diet. **The NYU licence forbids redistribution**, so nothing
> from it may be committed to this public vault.

## Access
| | |
|---|---|
| Availability | open-download (GitHub), but under a restrictive NYU licence |
| Link | https://github.com/nyuad-cai/MedArabiQ |
| Accessed? | yes (complete) |
| How | `git clone --depth 1` (commit `1d3d77a`, 2025-06-17); no login |
| Downloaded | `Data/medarabiq/datasets/*.csv` (7 files, 700 rows), `LICENSE`, `README.md`; `.git`, `.DS_Store` dropped. `sample*.csv` **deleted** and `schema.md` examples **redacted** (licence) |

### Licence (exact text of `LICENSE`)
> Copyright 2025 New York University. All Rights Reserved.
>
> A license to use and copy this software and its documentation solely for your internal non-commercial research and
> evaluation purposes, without fee and without a signed licensing agreement, is hereby granted upon your download of
> the software, through which you agree to the following: 1) the above copyright notice, this paragraph and the
> following three paragraphs will prominently appear in all internal copies and modifications; 2) no rights to
> sublicense or further distribute this software are granted; 3) no rights to modify this software are granted; and
> 4) no rights to assign this license are granted. Please contact the NYU Office of Technology Opportunities and
> Ventures at TOVCommunications@nyulangone.org for commercial licensing opportunities, or for further distribution,
> modification, or license rights.

(It continues with the creators' names, a liability disclaimer and a citation request.) The GitHub API reports the
licence as "Other / NOASSERTION". The **CC BY-NC-SA 4.0** reported by one search strand is the licence of the arXiv
paper (2505.03427), not of the dataset. In practice: we may use it internally for non-commercial evaluation, but may
not publish its items, samples or modified versions (e.g. translations) — keep it out of git.

## Tables & columns
All files are UTF-8 CSV with 100 rows; Arabic text is Modern Standard Arabic for exam items and largely
dialectal/colloquial for patient questions. Meanings from the paper (§4, Table F1) and the files.

### `multiple-choice-questions.csv` (100 rows)
| column | meaning |
|---|---|
| `Question` | Arabic stem with the options inline (أ ب ج د ه); average 24 words |
| `Answer` | correct option letter + its text |
| `Category` | subject: Physiology 15, Histology 15, Embryology 15, Microbiology 10, Biochemistry 10, and 5 each of Oncology, Ophthalmology, Pharmacology, Pulmonology, Pediatrics, Neurosurgery, OBGYN |

### `multiple-choice-withbias.csv` (100 rows)
| column | meaning |
|---|---|
| `Question`, `Answer`, `Category` | as above (same exam pool) |
| `Bias Category` | 1–7 = confirmation 16, recency 17, frequency 15, **cultural** 13, false-consensus 11, status quo 13, self-diagnosis 15 (mapping from the paper's order; checked on examples, e.g. code 4 adds "in some cultures a change of voice in women is attributed to age or smoking…") |
| `Question with Bias` | stem with an injected biasing sentence |
| `Bias Education` | biased stem prefixed with a warning to reason from evidence |
| `One-shot Demonstration`, `Few-shot Demonstration` | biased stem with one negative / negative+positive worked example |
| `Unnamed: 8` | stray column (1 non-empty cell) |

### `fill-in-the-blank-choices.csv`, `fill-in-the-blank-nochoices.csv` (100 rows each)
| column | meaning |
|---|---|
| `Question - Arabic` (header starts with a BOM) | cloze sentence (`______`), with options in the *choices* file |
| `Answer - Arabic` | correct filler (with option letter in the *choices* file) |
| `Question - English`, `Answer - English` | the same item in English (parallel) |
| `Category` | Neurology 15, Endocrinology 14, Cardiovascular System 14, OBGYN 12, Pulmonology 12, Gastroenterology 11, Pediatrics 9, Dermatology 8, Hematology 5 |

### `patient-doctor-qa.csv`, `patient-doctor-qa-gec.csv`, `patient-doctor-qa-llm.csv` (100 rows each, same order)
| file | columns | meaning |
|---|---|---|
| `patient-doctor-qa.csv` | `Question_description`, `Answer_details` | Altibbi patient question (sex and age prepended as "I am a [man/woman] aged X" when known; 87/100 have the prefix) and the physician's reply (reference). Mean 155 / 187 characters |
| `patient-doctor-qa-gec.csv` | `GEC Question description`, `GEC Answer details`, `Unnamed: 2–5` (empty) | question and answer after CAMeL Tools + BERT error detection + mBART grammatical error correction |
| `patient-doctor-qa-llm.csv` | `Modified question description`, `Unmodified answer` | question paraphrased by GPT-4o (anti-memorisation); answer unchanged (identical to the original in all 100 rows) |

No specialty column in the Q&A files; the paper says the 100 were chosen evenly over 14 specialties (cardiology,
OB/GYN, surgery, paediatrics, neurology, oncology, endocrinology, dentistry, ENT, public health, dermatology, primary
care, pulmonology, psychology).

Full profile (no examples): `Data/medarabiq/schema.md` · no sample file (licence)

## Countries & cultures covered
Arabic-speaking region, no country labels. Exams and notes come from "student-led social platforms of regional medical
schools" (countries not named); Altibbi is a pan-Arab telehealth platform. One patient question asks about Saudi
government hospitals. Culture appears through dialect, the patient framing, the "cultural bias" items, and folk
food remedies in doctors' answers (see below). Regions recorded: [[Middle East]], [[North Africa]]; `countries` left
empty because no item is tied to a country.

## Cases & conclusions
**One case** (`patient-doctor-qa.csv` row 0; our English translation, not the original text):
> *Patient:* "I am a woman, 24 years old. I have severe stomach pain, squeezing and cramps, nausea, loss of appetite,
> stabbing pains and heat inside the abdomen, and whatever I eat hurts my stomach afterwards."
> *Reference answer (doctor):* do a stool analysis and send us the result to decide the treatment; drink plenty of
> water, eat **fibre-rich foods**, and split meals into small, frequent ones.

**Gold conclusion and scoring.** The reference is a single, short, unverified forum reply (advice/triage, sometimes
"see a doctor"). Scored with BERTScore (XLM-RoBERTa-large) against it; the paper adds a GPT-4 judge (1–5 for
similarity, relevance, factuality, safety) because BERTScore rewarded hallucinating models (Falcon: high BERTScore,
judge score 1.1). Exam items: accuracy (MCQ, fill-in with choices) or BERTScore (fill-in without choices). Best
published: MCQ 57.5 (Gemini 1.5 Pro), fill-in with choices 79.7 (DeepSeek-V3); Q&A BERTScores all ≈ 81–86.

**Case vs knowledge items.** Only the 100 Altibbi questions are patient cases (`case/real`). The 400 exam/lecture
items are knowledge questions: our regex for a patient + age/complaint pattern finds 2 vignettes among the 100 MCQs
and 1 in each fill-in file.

**Food, diet, herbs, food–drug (keyword counts, our script, Arabic columns only, diacritics stripped, substring
match).** Keywords: غذاء, غذائ, أغذية/اغذية, تغذية/تغذيه, حمية/حميه, طعام, أطعمة/اطعمة, الأكل/الاكل, وجبة, وجبات,
رجيم/ريجيم, أعشاب/اعشاب, عشبي, صيام, الصوم, رمضان.
| set | hits |
|---|---|
| all 7 files | **66 / 700** (Q&A 18 original, 19 GEC, 16 paraphrased; MCQ 2, MCQ-bias 2, fill-in 5 + 4) |
| unique patient cases, excluding التمثيل الغذائي "metabolism" and clinical الصيام "fasting test" | **18 / 100** (food word in the question 7, only in the doctor's answer 11) |
| exam/lecture items, same exclusions | 3 / 400 (e.g. botulism after eating contaminated food) |
| herbs (أعشاب/عشبي), Ramadan/fasting (رمضان, الصوم) | 0 |

Diet-relevant cases worth keeping (row numbers): 16 foods for dialysis patients (limit salt, 50–100 g protein/day,
moderate potassium-rich fruit such as bananas, avoid preserved foods); 56 does cinnamon lower blood pressure ("not a
substitute for prescribed antihypertensives"); 53 metformin (Glucophage) for slimming in a 13-year-old, taken with a
fatty meal; 55 metformin and sweets/hypoglycaemia; 67 apple-cider vinegar and olive oil for slimming; 73 a folk list
of "strengthening" foods (garlic, onion, ginger, nigella seed, dates, fenugreek, saffron, honey, royal jelly).
Food–drug items: 3 (53, 55, 56). **diet_relevance: subset.**

## Linking to the vault's knowledge graph
- No structured ids: foods, herbs, drugs and conditions are free Arabic text. Linking needs Arabic NER or an LLM
  extraction step, then `IngredientResolver.by_text(..., lang='ar')` (the unified DB has only 7 Arabic ingredient
  aliases today) and `ConditionResolver.by_text`.
- The diet cases above map to KG paths we already have: potassium/phosphorus/sodium limits in CKD (dish nutrients),
  cinnamon → blood pressure (compound → condition), metformin and food ([[DDID]], [[FooDrugs]]), nigella seed and
  fenugreek (Persian/Unani properties via [[UNaProd]]).
- `Category` (specialty) of the exam items maps loosely to condition groups; not useful for diet.
- Better Arabic sources for KG testing: the full [[AraMed]] corpus (on request), and the larger [[MedAraBench]] by the
  same NYUAD group.

## Versions
One release (repo created 2025-02-08, last push 2025-06-17; arXiv v1 2025-05-06, v2 2025-08-22 = MLHC 2025 camera-ready).
Third-party Hugging Face re-uploads (`qimma/MCQ_MedArabiQ`, `qimma/QA_MedArabiQ`, 2026) were not checked and may
breach the licence.

## Caveats
- **Licence forbids redistribution and modification** — no samples, translations or derived files in git; ask NYU TOV
  for permission before publishing results that quote items.
- **Tiny**: 100 real cases; the GEC and paraphrased files are variants of the same 100, not new cases.
- **Weak reference answers**: single forum replies, sometimes generic or medically dubious (row 73 attributes poor
  eyesight to masturbation and lists folk foods); not expert-validated (medical students rated the Q&A set 4.88–4.99 / 5 for relevance, factuality, accuracy, clarity).
- **Contamination**: AraMed/Altibbi is public web text (hence the paraphrased variant); exams were digitised by hand
  but may be online.
- BERTScore on Arabic advice is a poor measure of correctness; plan an LLM-judge or rubric if used.
