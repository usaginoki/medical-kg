---
title: "RuMedBench"
slug: rumedbench
kind: [case]
version: "v1 task files (`*_v1.jsonl`) in sb-ai-lab/MedBench, commit dd57f4f (2026-02-02); RuMedPrime source data v1.0 (Zenodo 5765873, 2021-12-01)"
previous_versions: "pavel-blinov/RuMedBench (archived; last commit dd56a60, 2024-04-09; README 'The repository is closed'), with an identical data/ folder"
papers: ["[[Blinov2022 - RuMedBench]]"]
url: "https://github.com/sb-ai-lab/MedBench"
license: "MedBench repo: Apache License 2.0 (LICENSE file). RuMedPrime source data (Zenodo 5765873): CC BY 3.0. RuMedNLI: PhysioNet Credentialed Health Data License 1.5.0 (MIMIC-III derived). RuDReC (source of RuMedNER): no licence file in cimm-kzn/RuDReC. The original pavel-blinov/RuMedBench repo has no licence file."
availability: open-download
access_link: "https://github.com/sb-ai-lab/MedBench"
accessed: true
access_method: [github, zenodo]
access_date: 2026-10-07
access_notes: "git clone --depth 1 of pavel-blinov/RuMedBench showed it is archived ('closed') and points to sb-ai-lab/MedBench, so we cloned that too (6.4 MB repo). The data/ folders of both are byte-identical (diff -rq), so we kept MedBench only and removed .git. RuMedPrimeData.zip from Zenodo (2.0 MB, md5 6aa7fade…) unzips to the same TSV as data/raw/RuMedPrimeData.tsv (md5 abc73e2b…, matching the md5 on the Zenodo page). Nothing was gated. To keep schema.md and the committed samples to case data with redistributable licences, we zipped RuMedNLI (PhysioNet credentialed data that the repo re-hosts), RuMedNER + RuDReC.csv (no source licence), and code/ + lb_submissions/ (baselines, human and LLM outputs). They are kept locally but not profiled. RuMedTest and the RuMedDaNet private test have no answer keys (scored on medbench.ru). ECG2Pathology (PTB-XL signals) was not downloaded."
countries: ["[[Russia]]"]
regions: ["[[Europe]]"]
n_records: "RuMedPrime 7,625 outpatient visits (4,480 patients) → RuMedTop3 6,360 (4,690/848/822) · RuMedSymptomRec 3,300 (2,470/415/415) · RuMedDaNet 1,564 + 512 private · RuMedTest 397 MCQs · RuMedNLI 14,049 + 1,536 private · RuMedNER 4,809 sentences"
size: "19 MB on disk (data/ 15 MB)"
formats: [jsonl, tsv, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: ""
body_effect_how: ""
join_keys: [ICD-10 code (3-character in RuMedTop3; full code in RuMedPrime), new_event_id / idx, new_patient_id]
case_type: [real]
conclusion_type: [diagnosis]
languages: [ru]
n_cases: "6,360 real outpatient visits with an ICD-10 gold code (RuMedTop3; test split 822), drawn from 7,625 RuMedPrime visits that also carry the anamnesis"
diet_relevance: subset
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
tags:
  - type/dataset
  - kind/case
  - case/real
  - q/4
  - access/accessed
  - access/open
  - region/europe
---
# RuMedBench

> [!abstract] TL;DR
> RuMedBench is the open **Russian medical language-understanding benchmark** from Sber AI Lab, presented at AIME 2022 ([[Blinov2022 - RuMedBench]]). Its Q4 core is **RuMedTop3**:
> - **6,360 real outpatient visits** from the Siberian State Medical University hospital (Tomsk).
> - Each visit is the doctor's free-text record of the patient's complaints (*symptoms*) plus **one gold ICD-10 code**, cut to 3 characters (105 codes).
> - Scored by Hit@1 / Hit@3 over a ranked list of 3 codes.
>
> The source corpus, **RuMedPrime** (7,625 visits, CC BY 3.0), also has a free-text **anamnesis** that RuMedTop3 drops. It is the only open set of real Russian case → diagnosis pairs. Russian is the main clinical language in Kazakhstan and Kyrgyzstan, so it is the closest real-case test set for the Central Asian setting. Diet is a minor theme:
> - 3.7% of RuMedTop3 inputs mention food or diet keywords.
> - About 18% of visits have a diet-modifiable gold code (gastritis, obesity, T2DM, GERD, cholecystitis, goitre…).
> - 159 RuMedPrime visits mention **opisthorchiasis**, a liver fluke caught from river fish: a regional food–disease signal.

## Access
| | |
|---|---|
| Availability | open-download (GitHub, Apache-2.0; source corpus on Zenodo, CC BY 3.0) |
| Link | https://github.com/sb-ai-lab/MedBench (continuation of https://github.com/pavel-blinov/RuMedBench) · https://zenodo.org/records/5765873 |
| Accessed? | true |
| How | `git clone --depth 1` of both repos (data identical) · `curl -L https://zenodo.org/api/records/5765873/files/RuMedPrimeData.zip/content` (md5 checked) |
| Downloaded | `Data/rumedbench/medbench/` (task files, 15 MB data), `Data/rumedbench/zenodo/RuMedPrimeData.zip`. Zipped, not profiled: `data/RuMedNLI.zip`, `data/RuMedNER_RuDReC.zip`, `code_and_lb_submissions.zip` |

## Tables & columns
Column meanings come from `data/README.md`, the Zenodo record and the paper. All text is Russian. Personal data is masked with templates (`*ДАТА*` date, `*ИМЯ*` name, `*МО*` medical organisation).

### `medbench/data/raw/RuMedPrimeData.tsv` (7,625 rows): the RuMedPrime source corpus
| column | type | meaning | example |
|---|---|---|---|
| `symptoms` | str | patient complaints as registered by the doctor (Zenodo) | `Сухость кожи, мышечная слабость…` |
| `anamnesis` | str | the patient's history (Zenodo). **Not** part of the RuMedTop3 input. | `Месяц назад сильный стресс…` |
| `icd10` | str | ICD-10 code assigned at the visit, full precision. 992 distinct codes, 479 distinct at 3 characters. | `K29.6` |
| `new_patient_id` | str | anonymised patient id (4,480 patients) | `qf156c36` |
| `new_event_id` | str | visit id; equals `idx` in RuMedTop3 / RuMedSymptomRec | `q5fc2cb1` |
| `new_event_time` | date | visit date, **randomised per patient** (Zenodo). The file spans 2020-10-27 to 2030-12-16, so these are not real dates. | `2027-05-19` |

### `medbench/data/RuMedTop3/{train,dev,test}_v1.jsonl` (4,690 / 848 / 822 rows): diagnosis prediction
| column | type | meaning | example |
|---|---|---|---|
| `idx` | str | = RuMedPrime `new_event_id` (all 6,360 are found there) | `qaf1454f` |
| `symptoms` | str | model input: the RuMedPrime `symptoms` field only. Median 118 characters, max 3,627. | `Головную боль, "мелькание мушек перед глазами" на фоне повышения цифр АД до 150\100…` |
| `code` | str | gold label: ICD-10 code at the "second level of the hierarchy" (3 characters). Visits with codes seen fewer than 10 times were dropped (paper), leaving 105 codes. | `I11` |

Most frequent gold codes: M54 dorsalgia 734 · I11 hypertensive heart disease 360 · G54 nerve root/plexus disorders 304 · E06 thyroiditis 220 · G90 autonomic disorders 215 · G44 other headache 171 · J06 acute URTI 162 · G20 Parkinson's 151 · E66 obesity 136.

### `medbench/data/RuMedSymptomRec/{train,dev,test}_v1.jsonl` (2,470 / 415 / 415 rows): symptom recommendation
| column | type | meaning | example |
|---|---|---|---|
| `idx` | str | RuMedPrime visit id | `q6fb3825` |
| `symptoms` | str | complaints text with one symptom cut out | `Жалобы осиплость голоса, повышение температуры до 38 кашель…` |
| `code` | str | the removed symptom to predict: one of 141 symptom codes (UMLS-concept-based, Russian phrase) | `сухой кашель` |

### `medbench/data/raw/rec_markup.csv` (7,625 rows): markup used to build RuMedSymptomRec
- `new_event_id`: the visit.
- `code`: the target symptom. Filled for 55% of rows; 219 distinct.
- `keep_spans`: list of `(start, end)` character spans of `symptoms` to keep, so that the target symptom is removed, e.g. `[(0, 138), (151, 279)]`.

### `medbench/data/RuMedDaNet/{train,dev,test}_v1.jsonl` (1,052 / 256 / 256) + `private_test_v1.jsonl` (512, no answers)
- `pairID`: item id.
- `context`: a medical text excerpt of up to 300 words (therapeutics, physiology, anatomy, pharmacology, biochemistry).
- `question`: a yes/no question written by an assessor.
- `answer`: `да` / `нет`, balanced.
- Not a patient case (knowledge QA).

### `medbench/data/RuMedTest/private_test_v1.jsonl` (397 rows, no answer key)
- `idx`: item id.
- `question`: a 4-option MCQ from the specialty "General medical practice" (medbench.ru).
- `1`–`4`: the answer options.
- Test-only and scored on medbench.ru, so it is unusable offline without an answer key.

### Kept zipped (not profiled)
- `data/RuMedNLI.zip`: MedNLI (MIMIC-III past-medical-history premises) translated into Russian by two MT services plus human correction (paper).
  - Columns `pairID`, `ru_sentence1`, `ru_sentence2`, `gold_label`.
  - 11,232 / 1,395 / 1,422 rows + 1,536 private.
  - The official copy is PhysioNet credentialed access (DOI 10.13026/gxzd-cf80); **do not commit samples**.
- `data/RuMedNER_RuDReC.zip`: RuMedNER, 3,440 / 676 / 693 sentences with columns `idx`, `tokens`, `ner_tags`.
  - IOB tags: Drugname, Drugclass, Drugform, ADR, DI (drug indication/symptom), Finding.
  - Built from `RuDReC.csv`: 68,041 tokens in 4,809 sentences of drug user reviews.

Sample: `Data/rumedbench/sample.csv` (RuMedPrime) + `sample_medbench_data_RuMedTop3_test_v1_jsonl.csv` etc. · full profile: `Data/rumedbench/schema.md`

## Countries & cultures covered
- **[[Russia]]**: one outpatient unit of the Siberian State Medical University hospital, Tomsk (Western Siberia). The text is real Russian clinical shorthand with typos and abbreviations, e.g. `АД` blood pressure, `ГБ` hypertension/headache, `пр п/реберье` right hypochondrium.
- **Region-specific signals:**
  - **Opisthorchiasis** (`описторх*`) appears in **159 RuMedPrime visits, 118 of them in RuMedTop3**. Gold codes are mostly K81 cholecystitis, K29 gastritis, K58 IBS, K83 biliary and B66. Anamneses mention eating river fish.
  - The *Opisthorchis felineus* fluke is endemic in the Ob–Irtysh basin, which also covers northern and eastern Kazakhstan. This is general epidemiology, not something the dataset states.
  - Iodine-deficiency thyroid disease (E01, 65 visits) and goitre (E04, 95) are frequent.
- **Relevance for Central Asia:** no Central Asian patients. But Russian-language outpatient notes and ICD-10 coding are the norm in Kazakhstan and Kyrgyzstan clinics, so this is the closest open real-case proxy (`regions` follows the vault's Russia → Europe assignment).

## Cases & conclusions
**One real case** (RuMedTop3 test, `idx q9b233e6`), translated from Russian:
- *Input (`symptoms`):* "Periodic pressing pains in the right hypochondrium, on an empty stomach, sometimes after eating. Nausea, decreased appetite."
- *Gold conclusion (`code`):* **K29**, gastritis and duodenitis. RuMedPrime has the full code `K29.6`, other gastritis.
- *Hidden context in RuMedPrime `anamnesis`:* "Epigastric pain since childhood. Ate river fish. Deworming for opisthorchiasis with Biltricide [praziquantel] in *DATE* and *DATE*. Continued to eat river fish. Nausea and decreased appetite since *DATE*. Constantly takes thyroid hormones."
  - Here a diet exposure, raw river fish, plus a drug, levothyroxine, sit in the history, not in the benchmark input.

**Scoring** (`code/eval.py`): the model returns a ranked list of 3 ICD-10 codes per test visit.
- **Hit@1** (= accuracy): the top code equals the gold code.
- **Hit@3**: the gold code is among the 3.
- The benchmark "overall" score averages these with the other tasks.
- Test results from the paper and README (Hit@1 / Hit@3):

| model | RuMedTop3 | RuMedSymptomRec |
|---|---|---|
| naive (most frequent codes) | 10.58 / 22.02 | 1.93 / 5.30 |
| tf-idf char n-grams + logistic regression | **49.76 / 72.75** | 32.05 / 49.40 |
| RuPoolBERT | 47.45 / 70.44 | 34.94 / 52.05 |
| RuBioRoBERTa | 46.72 / 72.87 | **44.01 / 58.95** |
| clinicians (human baseline) | 25.06 / 48.54 | 7.23 / 12.53 |

- Clinicians did worse than models because the symptoms field lacks sex, age, examination and anamnesis (paper). For an LLM test set, **pair `symptoms` + `anamnesis` from RuMedPrime with the gold code** (join on `idx` = `new_event_id`).

**Diet / food relevance** (case-insensitive regex over the Russian text, stems as listed; counted 2026-10-07):

| keyword group (stems) | RuMedTop3 all (n=6,360) | RuMedTop3 test (n=822) | RuMedPrime symptoms+anamnesis (n=7,625) |
|---|---|---|---|
| `диет*` diet | 31 | 1 | 103 |
| `питани*` nutrition/eating | 14 | 5 | 174 |
| `пищ*` food (excl. `пищевод`, `пищеварен`) | 90 | 16 | 218 |
| `еда/еды/еду/едой` food, meal | 61 | 7 | 165 |
| `продукт*` (excl. `продуктивн`) | 5 | 3 | 50 |
| `голод*` hunger | 27 | 4 | 45 |
| `аппетит*` appetite | 37 | 6 | 75 |
| `переед*` overeating | 1 | 0 | 3 |
| **any of the above** | **236 (3.7%)** | **36 (4.4%)** | **639 (8.4%)** |
| alcohol (`алкогол*`, `спиртн*`) | 6 | 0 | 42 |
| herbs/supplements (`трав*` excl. `травм*`, `фито*`, `настой`, `отвар`, `БАД`) | 11 | 2 | 51 |
| named foods (`кофе`, `чай`, `молок*`, `мяс*`, `жирн*`, `сладк*`, `шоколад`) | 168 | 25 | 376 |
| food–drug (`взаимодейств*`, `грейпфрут`, `несовмест*`) | 0 | 0 | 1 (a grapefruit *allergy*, not an interaction) |

- Gold codes for conditions where diet is part of management (our grouping), RuMedTop3 all / test:
  - I11 360 / 56 · E66 obesity 136 / 10 · K29 gastritis 107 / 16 · E04 goitre 95 / 19 · K81 cholecystitis 75 / 15
  - K21 GERD 72 / 6 · E11 T2DM 70 / 6 · E01 iodine-deficiency thyroid 65 / 8 · I10 56 / 6 · D50 iron-deficiency anaemia 41 / 5
  - K80 gallstones 38 / 4 · K58 IBS 34 / 6 · M10 gout 22 / 1
  - **Total 1,171 / 6,360 (18.4%)**; test 158 / 822.
- Many inputs are diet-*triggered* complaints (pain "after eating", "after a dietary error"), but **no item has a diet or food–drug conclusion**: the label is always a diagnosis. Hence `diet_relevance: subset`.

## Linking to the vault's KG
- **ICD-10 → conditions.** The unified DB's `condition.icd10cm` is filled for 3,222 conditions (2,748 from CTD's MEDIC vocabulary, 474 from SymMap).
  - A 3-character prefix match maps **90 of the 105 RuMedTop3 codes (5,457 / 6,360 visits, 85.8%)** to ≥1 condition, e.g. K29 → `MESH:D005756` Gastritis, E66 → `MESH:D009765` Obesity, E11 → `MESH:D003924` Diabetes Mellitus Type 2, K21 → `MESH:D005764`, D50 → `MESH:D018798`, M10 → `MESH:D006073`.
  - **Unmapped:** I11 (the 2nd most frequent code), E01, E89, J01, J02, J31, J41, M13, M15, M51, M75, N84, N86, N93, Z00. Map these by MeSH name (e.g. I11 → Hypertension), or through the ICD-10 → MeSH crosswalk in UMLS.
  - The MeSH disease ids then join to [[CTD]] curated chemical–disease rows (`DiseaseID`).
- **Conditions → dishes.** Through `v_condition_dish`, 87 codes reach ≥1 dish, and **73 codes (4,569 visits) reach ≥1 of the 11 Kyrgyz dishes**, the only Central Asian dishes in the DB, from [[Kyrgyzstan Food Composition Table]].
  - Paths are dense (about 45,800 dishes per common code), so an eval must filter by `best_evidence_rank` / salient ingredients.
- **Opisthorchiasis** has a condition (`MESH:D009889`, ICD B66), but the KG has no "raw river fish → fluke" exposure edge. This is a gap that the RuMedPrime anamneses expose.
- **Medications** in anamneses (free text, e.g. levothyroxine, azilsartan) could be matched to the `drug` table for food–drug checks. No structured drug field exists.

## Versions
- **Paper:** arXiv v1 2022-01-17, v2 2022-05-24; AIME 2022 (LNCS, pp. 383–392).
- **Code + data:** pavel-blinov/RuMedBench was archived ("The repository is closed"). The live repo is sb-ai-lab/MedBench (Apache-2.0); its last commit, 2026-02-02, adds a MedGemma-4B leaderboard submission. Task files are still `v1`.
- **MedBench platform** (https://medbench.ru): a leaderboard with closed tests for RuMedDaNet, RuMedNLI, RuMedTest and ECG2Pathology. RuMedTop3 / RuMedSymptomRec are *not* on it.
  - Leaderboard on 2026-10-07: Human, RuMedTest 85 / DaNet 92.97 / NLI 85.67 · GigaChat 72.04 / 92.58 / 65.17 · MedGemma-4B 49.87 / 89.45 / 53.58 · text-davinci-003 35.01 / 89.26 / 61.33.
  - The site offers `MedBench_data.zip`; not downloaded.
- **RuMedPrime:** Zenodo v1.0 (2021-12-01) is the only version.

## Caveats
- **Thin inputs:** RuMedTop3 gives only the complaints field (median 118 characters, noisy, typos). Clinicians scored Hit@1 25%. Use RuMedPrime's anamnesis for a fairer LLM case.
- **One gold code per visit**, truncated to 3 characters and assigned in routine outpatient coding. There is no differential and no adjudication, and rare codes (<10 visits) are removed.
- **Skewed mix:** one Tomsk clinic dominated by neurology (M54, G54, G90, G44, G20), cardiology (I11), thyroid (E04–E06) and gynaecology/urology. M54 alone is 11.5% of items.
- **Contamination risk:** the test labels have been public on GitHub since 2022.
- **Licences differ by task:**
  - RuMedTop3 / SymptomRec / RuMedPrime: CC BY 3.0 + Apache-2.0, fine with attribution.
  - RuMedNLI: PhysioNet credentialed; the MedBench repo re-hosts it, which we do not rely on.
  - RuDReC: no licence file.
  - We committed samples only of the first group plus RuMedDaNet / RuMedTest (Apache-2.0).
- **Dates** in RuMedPrime are randomised per patient. Do not use them for temporal reasoning.
- The diet keyword counts are regex counts: they include mentions such as "appetite decreased", and a few false positives may remain.
