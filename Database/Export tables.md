---
title: "Export tables: dishes, ingredients, effects, cases"
topics: [cultural-food-health, kg-medical-eval]
questions: [Q1, Q2, Q3, Q4, Q5]
updated: 2026-10-07
tags:
  - type/database
  - q/1
  - q/2
  - q/3
  - q/4
  - q/5
---
# Export tables: dishes, ingredients, effects, cases

> [!abstract] What it is
> The [[Unified database]] flattened into three tables that join on `ingredient_id`, written by `uv run db/export.py`
> to `db/export/` (Parquet with nested lists + CSV with the lists as JSON; git-ignored):
> - **`dishes`**: one row per dish, with its culture labels, recipe text, ingredient lines and lab nutrients;
> - **`ingredients`**: one row per food or herb, with its names, ids, cultural properties and compounds;
> - **`effects`**: one row per claim, ingredient → condition (direct or via a compound) or ingredient × drug.
>
> A fourth table, **`cases`** (one row per patient case with its gold conclusion), is written separately by
> `uv run db/cases.py` from the case datasets of [[Q4 Patient case-conclusion datasets|Q4]]; it is not linked to
> the other three yet (last section below).
>
> Browse them with the viewer: `uv run python -m http.server 8765 -d db` → http://localhost:8765/viewer/
> (filters by dataset, country, "has recipe / ingredients / nutrients…", random samples, expandable rows; a Cases
> tab when `cases.parquet` exists).

> [!warning] Build of 2026-10-01 without HMDB
> HMDB access is pending, so this build skips it. That costs about 32k compounds and 23k compound → condition
> links, including ~17k CTD links that HMDB used to bridge to food compounds. Everything else matches the
> [[Unified database]] build of 2026-09-30 (see `db/build_report.md`).

## `dishes`: 46,252 dishes · 23 countries · 482,389 ingredient lines
| Dataset | Dishes | Countries | Ingredient lines | With recipe text | With grams | With lab nutrients | Language |
|---|---|---|---|---|---|---|---|
| [[IndicRecipeNutri]] | 20,415 | 1 (IN) | 235,320 | – | 20,358 | – | mostly en |
| [[Food.com Recipes and Interactions\|Food.com]] | 10,095 | 21 | 108,653 | 10,095 | – | – | en |
| [[CulinaryDB]] | 8,151 | 5 (CN IN JP KR TH) | 79,568 | – | 5,507 | – | en |
| [[XiaChuFang Recipe Corpus\|XiaChuFang]] | 5,000 | 1 (CN) | 36,105 | 5,000 | 2,476 | – | zh |
| [[Our Regional Cuisines (Japan MAFF)\|Japan MAFF]] | 1,355 | 1 (JP) | 11,200 | 1,340 | 1,253 | – | ja |
| [[Indian Nutrient Databank (INDB)\|INDB]] | 1,014 | 1 (IN) | 10,271 | – | 1,014 | 1,014 | en |
| [[Saudi Food Composition Tables\|Saudi FCT]] | 130 | 1 (SA) | 1,156 | 130 | 129 | 130 | en |
| [[Bahrain Food Composition Tables\|Bahrain FCT]] | 81 | 1 (BH) | – | – | – | 81 | ar |
| [[Kyrgyzstan Food Composition Table\|Kyrgyz FCT]] | 11 | 1 (KG) | 116 | – | 11 | 11 | en |

- **Top countries:** India 26,730 · China 7,906 · Japan 2,736 · Thailand 1,831 · Korea 534 · Vietnam 320 ·
  Lebanon 249 · Turkey 233 · Iran 230 · Saudi Arabia 210.
- **No country:** 4,089 dishes have only a region label (e.g. CulinaryDB "Middle East").
- **Bahrain has 81, not 82, dishes:** the book prints codes 7.1 and 8.19 twice each, and the codes are kept as
  printed, so one dish of each pair is merged away (Fatira with zaatar, Rangina).

## `ingredients`: 1,688 ingredients
| | Count |
|---|---|
| With scientific name | 677 |
| Medicinal herbs | 331 |
| With compounds | 935 (248,799 compound amounts) |
| Names (all languages) | 11,005 |
| Cultural properties | KNApSAcK edible/medicinal use 396 · TCM 168 · Persian Mizaj 35 |

- **Compound amounts by source:** [[FooDB]] 105,227 · [[NPASS]] 56,402 · [[CMAUP]] 37,411 · [[IMPPAT]] 27,515 ·
  [[TM-MC]] 7,650 · [[FlavorDB2]] 6,607 · [[Phenol-Explorer]] 4,542 · [[SymMap]] 2,042 · [[HERB]] 1,403.
- **Cultural properties from:** [[KNApSAcK Family]] (use per country), [[SymMap]] and [[HERB]] (TCM),
  [[UNaProd]] (Persian Mizaj).

## `effects`: 5,231,893 claims · 258,234 characteristic · 949 ingredients
| Source | Claims | Characteristic | Ingredients | Conditions / drugs | Path |
|---|---|---|---|---|---|
| [[CTD]] | 3,461,555 | 124,729 | 928 | 2,268 | via compound |
| [[Dr. Duke's Phytochemical and Ethnobotanical Databases\|Duke]] | 810,841 | 32,851 | 928 | 390 | via compound + direct |
| [[FooDB]] | 809,468 | 33,851 | 922 | 148 | via compound |
| [[Exposome-Explorer]] | 84,279 | 1,053 | 881 | 14 | via compound |
| [[CMAUP]] | 42,704 | 42,704 | 254 | 532 | direct |
| [[SymMap]] | 9,908 | 9,908 | 13 | 5,063 | direct |
| [[IMPPAT]] | 7,560 | 7,560 | 247 | 513 | direct |
| [[DDID]] | 4,893 | 4,893 | 241 | 536 drugs | drug interaction |
| [[UNaProd]] | 292 | 292 | 17 | 98 | direct |
| [[SpiceRx]] | 246 | 246 | 26 | 99 | direct |
| [[DrugBank]] (via DDID) | 121 | 121 | 22 | 60 drugs | drug interaction |
| [[HERB]] | 18 | 18 | 2 | 18 | direct |
| [[KNApSAcK Family\|KNApSAcK]] Jamu | 8 | 8 | 6 | 3 | direct |

- **Conditions:** 5,226,879 claims over 6,325 conditions. **Drugs:** 5,014 claims over 539 drugs.
- **Characteristic** is the salience rule of [[Unified database#Ranking]]: direct claims always count; a compound path
  counts only when the ingredient has ≥ 1 mg/100 g of a rare compound or is a major source of it. So direct-only
  sources are 100% characteristic, while most CTD/FooDB/Duke compound paths are not.
- Evidence grades and directions are those of [[Unified database#Evidence grading and direction]].

## `cases`: 38,301 patient cases · 11 datasets
The core columns are `case_id`, `source`, `case` (what is put to the model) and `conclusion` (the dataset's answer);
provenance, AI flags and relevance columns are described under *Provenance and relevance* below. The
test for [[Q5 Evaluating KG-augmented medical LLMs|Q5]]: ask a model each `case` with and without the graph and
compare its answer with `conclusion`. Built on 2026-10-07; rules per source are in `db/cases.py` and `db/README.md`.

| Dataset | Cases | Parts | Case | Conclusion | Lang. | Diet relevance |
|---|---|---|---|---|---|---|
| [[MedCaseReasoning]] | 14,489 | train 13,092 · val 500 · test 897 | published case report (`case_prompt`) | final diagnosis (8,861 distinct) | en | subset |
| [[NGQA]] | 13,802 | – | NHANES user (status, dietary habits) + food (category, ingredients) + question | yes/no with a one-sentence reason (No 7,186 · Yes 6,616) | en | central |
| [[RuMedBench]] | 6,360 | RuMedTop3 train 4,690 · dev 848 · test 822 | real outpatient complaints | ICD-10 code, 3 characters (105 distinct) | ru | subset |
| [[FAM-Bench]] | 1,500 | Task 1 | dish (title, ingredients, nutrition, tags) + condition question | recommend 775 · not recommend 725, with ingredients and reasoning per condition | en | central |
| [[MedicationQA]] | 680 | – | consumer medication question | answer passage from a trusted website | en | subset |
| [[MTCMB]] | 600 | MSDD 100 · PR 100 · Diagnosis + FRD 200 · CHGD 100 · TCMeEE 100 | EMR case record, symptom list, LLM-written dialogue or classical case record | syndrome + disease · prescribed herbs · disease, syndrome elements, treatment, formula, herbs · structured record · extracted entities | zh | subset |
| [[TCM-BEST4SDT]] | 300 | – | patient narrative | 中医疾病诊断 + 12 fields: syndrome, cause, mechanism, treatment, formula with doses, decoction, cautions… | zh | central |
| [[MedArabiQ]] | 300 | patient–doctor QA: original 100 · grammar-corrected 100 · GPT-4o paraphrase 100 (the same 100 questions) | patient question | doctor's answer | ar | subset |
| [[ISSAI Dietary Recommendation profiles]] | 250 | 50 profiles × 5 pipelines (EN, RU, KK direct; RU, KK via translation) | mock Kazakh patient profile | GPT-4 diet advice + meal plan (**not gold**) | en, ru, kk | central |
| [[PerMedCQA]] | 10 | sample of 67,791 | real Iranian patient question | physician's answer | fa | sample chosen for cues |
| [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA\|Rezaei & Shakeri 2026]] | 10 | sample of 1,350 variants | MedQA vignette with an injected cultural cue + options | MedQA key | en | none |

- **Median length (characters), case / conclusion:** MedCaseReasoning 1,255 / 22 · FAM-Bench 1,083 / 199 ·
  NGQA 829 / 40 · MTCMB 366 / 71 · MedArabiQ 152 / 113 · RuMedBench 118 / 11 · TCM-BEST4SDT 116 / 571 ·
  MedicationQA 38 / 259.
- **Left out:** multiple-choice
  exam items (MTCMB exam sets, the TCM-BEST4SDT knowledge questions, the other four MedArabiQ files); FAM-Bench Task 2
  (comparisons between dishes); NGQA's nutrition tags and match/contradict/need edges (what the answer is checked
  against); MedCaseReasoning's `diagnostic_reasoning`; the 10 MedicationQA rows marked `No answers`.
- **Licences:** MedArabiQ allows internal research only and the Rezaei repository has no licence, so `db/export/`
  must not be committed or shared.
  MedicationQA and FAM-Bench answers quote third-party websites.
- **Cultural cues:** `uv run db/cues.py` counts the cases that state a place, an ethnicity, a religion, a
  culture-linked habit or food, or traditional medicine: 8,238 of 38,301 (21.5%), mostly nationality words in
  MedCaseReasoning and cuisine names on NGQA and FAM-Bench dishes. Table and reading (for the first 8 datasets):
  [[Q7 Cultural cues in evaluation datasets|Q7]].
- **Not linked to the graph yet:** the next step is to match cases to graph ids (ICD-10 → conditions, dish and
  ingredient names → `ingredient_id`), so that the graph-covered cases can be scored separately.

### Provenance and relevance
Every case carries where it comes from, whether AI wrote any of it, and how relevant it is for testing a culturally
aware medical agent. The Cases tab of the viewer (`db/viewer/index.html`) has a filter for each column.

| Column | Values |
|---|---|
| `part` | dataset part, e.g. `mtcmb:chgd`, `issai:kk-direct` |
| `lang` | language of the case text: en, ru, kk, zh, ar, fa |
| `origin` | where the case comes from, one phrase per part |
| `case_ai` | is the case text AI-written: `no` · `ai-rewritten` (a real or human source reworded by a model) · `ai-generated` · `not stated` |
| `conclusion_ai` | is the conclusion AI-made: `no` · `ai-extracted` (copied from a human source by a model) · `ai-proposed, expert-checked` · `rule-derived` · `ai-generated` |
| `gold` | summary for filtering: `gold` (24,249) · `weak gold` (13,802, rule-derived) · `ai-generated` (250) |
| `cue_place`, `cue_ethnicity`, `cue_religion`, `cue_habit`, `cue_food`, `cue_tradmed` | keyword flags on the case text (`db/cues.py`; a lower bound) |
| `culture_by_construction` | the whole part is tied to a culture: TCM sets, ISSAI Kazakh profiles, Rezaei's injected cues |
| `diet` | a food, diet, supplement or herb word in the case text; always true for FAM-Bench, NGQA and ISSAI |
| `relevance`, `relevance_why` | `high` (1,858) · `medium` (8,716) · `low` (27,727), and the reason with the matched words |

**Relevance rule** (`relevance()` in `db/cases.py`): *cue* = any cue flag or culture by construction; *actionable* =
food, diet or herb content the graph can act on (`diet`, `cue_tradmed`, or a diet / traditional-medicine dataset).
- **high:** cue and actionable and a gold conclusion.
- **medium:** exactly one of the two with a gold conclusion, or both without one (weak gold or AI-generated).
- **low:** the rest.

The labels come from keywords and part-level facts, not from reading each case: a place name that looks like a
keyword (a town called "Kampo") is counted, and a cue is not checked for whether the answer depends on it.

| Part | Cases | Origin | Case by AI | Conclusion by AI | Gold | High / medium / low |
|---|---|---|---|---|---|---|
| `medcasereasoning` | 14,489 | published case report (PMC) | ai-rewritten (o4-mini wrote the prompt from the article) | ai-extracted (the report's diagnosis; 100 physician-checked) | gold | 361 / 3,383 / 10,745 |
| `ngqa` | 13,802 | real NHANES participant + a food, templated | no | rule-derived | weak gold | 0 / 3,814 / 9,988 |
| `rumedbench:top3` | 6,360 | real outpatient visit, Tomsk | no | no | gold | 4 / 279 / 6,077 |
| `fam-bench:task1` | 1,500 | web recipe + templated question | no | ai-proposed (GPT-5.5), expert-checked | gold | 576 / 924 / 0 |
| `medicationqa` | 680 | real consumer question to MedlinePlus | no | no | gold | 1 / 27 / 652 |
| `mtcmb:msdd`, `mtcmb:pr` | 200 | real TCM medical records | no | no | gold | 200 / 0 / 0 |
| `mtcmb:diagnosis-frd` | 200 | TCM textbook cases | no | no | gold | 200 / 0 / 0 |
| `mtcmb:chgd` | 100 | dialogue written by DeepSeek-R1 from an exam case | ai-generated | no (exam-bank record) | gold | 100 / 0 / 0 |
| `mtcmb:tcmeee` | 100 | classical or modern TCM case record | no | ai-proposed (DeepSeek-R1), expert-checked | gold | 100 / 0 / 0 |
| `tcm-best4sdt:classical` | 150 | classical case record retold in modern Chinese | not stated | no (expert-annotated) | gold | 150 / 0 / 0 |
| `tcm-best4sdt:clinical` | 50 | modern clinical record | no | no | gold | 50 / 0 / 0 |
| `tcm-best4sdt:vignette` | 100 | short modern vignette, author not stated | not stated | no | gold | 100 / 0 / 0 |
| `medarabiq:patient-doctor-qa` | 100 | real Altibbi patient question | no | no | gold | 2 / 11 / 87 |
| `medarabiq:patient-doctor-qa-gec` | 100 | the same questions, machine grammar-corrected | ai-rewritten | no | gold | 2 / 11 / 87 |
| `medarabiq:patient-doctor-qa-llm` | 100 | the same questions, paraphrased by GPT-4o | ai-rewritten | no | gold | 3 / 6 / 91 |
| `issai:*` (5 parts) | 250 | mock Kazakh profile written by the study team | no | ai-generated (GPT-4) | ai-generated | 0 / 250 / 0 |
| `permedcqa` | 10 | real Iranian patient question (sample with cues) | no | no | gold | 9 / 1 / 0 |
| `rezaei2026` | 10 | MedQA vignette with an LLM-injected cultural cue | ai-rewritten | no (MedQA key) | gold | 0 / 10 / 0 |

- The three MedArabiQ parts and the five ISSAI parts repeat the same 100 questions and 50 profiles; filter on `part`
  to avoid counting them more than once.
- All 900 TCM cases are high because they are traditional medicine by construction with a gold answer; within them,
  the cue and `diet` flags show which ones mention food or habits.
- PerMedCQA and the Rezaei set are 10-row samples (fixed seed) of much larger open sets; they have no dataset note yet.
