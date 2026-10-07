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

## `cases`: 37,631 patient cases · 8 datasets
Four columns: `case_id`, `source`, `case` (what is put to the model), `conclusion` (the dataset's gold answer). The
test for [[Q5 Evaluating KG-augmented medical LLMs|Q5]]: ask a model each `case` with and without the graph and
compare its answer with `conclusion`. Built on 2026-10-07; rules per source are in `db/cases.py` and `db/README.md`.

| Dataset | Cases | Parts | Case | Conclusion | Lang. | Diet relevance |
|---|---|---|---|---|---|---|
| [[MedCaseReasoning]] | 14,489 | train 13,092 · val 500 · test 897 | published case report (`case_prompt`) | final diagnosis (8,861 distinct) | en | subset |
| [[NGQA]] | 13,802 | – | NHANES user (status, dietary habits) + food (category, ingredients) + question | yes/no with a one-sentence reason (No 7,186 · Yes 6,616) | en | central |
| [[RuMedBench]] | 6,360 | RuMedTop3 train 4,690 · dev 848 · test 822 | real outpatient complaints | ICD-10 code, 3 characters (105 distinct) | ru | subset |
| [[FAM-Bench]] | 1,500 | Task 1 | dish (title, ingredients, nutrition, tags) + condition question | recommend 775 · not recommend 725, with ingredients and reasoning per condition | en | central |
| [[MedicationQA]] | 680 | – | consumer medication question | answer passage from a trusted website | en | subset |
| [[MTCMB]] | 400 | MSDD 100 · PR 100 · Diagnosis + FRD 200 | EMR case record or symptom list | syndrome + disease · prescribed herbs · disease, syndrome elements, treatment, formula, herbs | zh | subset |
| [[TCM-BEST4SDT]] | 300 | – | patient narrative | 中医疾病诊断 + 12 fields: syndrome, cause, mechanism, treatment, formula with doses, decoction, cautions… | zh | central |
| [[MedArabiQ]] | 100 | patient–doctor QA | patient question | doctor's answer | ar | subset |

- **Median length (characters), case / conclusion:** MedCaseReasoning 1,255 / 22 · FAM-Bench 1,083 / 199 ·
  NGQA 829 / 40 · MTCMB 366 / 71 · MedArabiQ 152 / 113 · RuMedBench 118 / 11 · TCM-BEST4SDT 116 / 571 ·
  MedicationQA 38 / 259.
- **Left out:** [[ISSAI Dietary Recommendation profiles]] (the answers are GPT-4 outputs, not gold); multiple-choice
  exam items (MTCMB exam sets, the TCM-BEST4SDT knowledge questions, the other six MedArabiQ files); FAM-Bench Task 2
  (comparisons between dishes); NGQA's nutrition tags and match/contradict/need edges (what the answer is checked
  against); MedCaseReasoning's `diagnostic_reasoning`; the 10 MedicationQA rows marked `No answers`.
- **Licences:** MedArabiQ allows internal research only, so `db/export/` must not be committed or shared.
  MedicationQA and FAM-Bench answers quote third-party websites.
- **Not linked to the graph yet:** the next step is to match cases to graph ids (ICD-10 → conditions, dish and
  ingredient names → `ingredient_id`), so that the graph-covered cases can be scored separately.
