---
title: "ISSAI Dietary Recommendation profiles"
slug: issai-dietary-recommendation
kind: [case]
version: "Hugging Face issai/LLM_for_Dietary_Recommendation_System, commit 1b33b856 (uploaded 2025-02-19); same files as GitHub IS2AI/LLM_for_Dietary_Recommendation_System (last push 2023-08-23)"
previous_versions: "GitHub repo first published as IS2AI/Chat_GPT_for_Nutritional_Recommendation_System (now redirects); GPT-4 outputs generated May–Aug 2023"
papers: ["[[Adilmetova2024 - ChatGPT multilingual clinical nutrition advice]]"]
url: "https://huggingface.co/datasets/issai/LLM_for_Dietary_Recommendation_System"
license: "MIT (dataset card `license: mit`; LICENSE file 'MIT License, Copyright (c) 2023 ISSAI'). Paper: CC BY 4.0."
availability: open-download
access_link: "https://huggingface.co/datasets/issai/LLM_for_Dietary_Recommendation_System"
accessed: true
access_method: [huggingface]
access_date: 2026-10-07
access_notes: "`uv run hf download issai/LLM_for_Dietary_Recommendation_System --repo-type dataset` worked without login (not gated): 5 zips (≈820 KB), README, LICENSE, gpt_response_extraction.py. Each zip holds 50 plain-text files (prompt + profile + GPT-4 answers), no table. We parsed them into `derived/cases_responses.csv` (250 rows) and `derived/profiles.csv` (50 rows). The parser (`db/prep_issai.py`, run by `uv run db/prep.py issai`) splits profile from answer heuristically (≥2-space separator; for RU/KK the common prefix of the direct and translated files). All 250 rows split, but spot-check boundaries. The expert Likert ratings from the paper are NOT in the repo. The paper full text was blocked (ScienceDirect HTTP 403), so the notes on scoring come from the abstract."
countries: ["[[Kazakhstan]]"]
regions: ["[[Central Asia]]"]
n_records: "50 patient profiles × 3 languages (EN/RU/KK) = 150 profile texts; 250 GPT-4 answer files (EN direct, RU direct, RU via English, KK direct, KK via English)"
size: "0.8 MB zipped; 2.6 MB derived CSV"
formats: [txt, zip, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: ""
body_effect_how: ""
join_keys: [case_id (1–50), dish names (English/Russian/Kazakh), diagnosis (free text), drug names (free text)]
case_type: [synthetic, diet]
conclusion_type: [advice]
languages: [en, ru, kk]
n_cases: "50 mock patient profiles (10 lifestyle/sport goals + 40 clinical conditions), each in English, Russian and Kazakh"
diet_relevance: central
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
tags:
  - type/dataset
  - kind/case
  - case/synthetic
  - case/diet
  - q/4
  - access/accessed
  - access/open
  - region/central-asia
---
# ISSAI Dietary Recommendation profiles

> [!abstract] TL;DR
> ISSAI and the Nazarbayev University School of Medicine (Astana) wrote **50 mock patient profiles set in Kazakhstan**, each in **English, Russian and Kazakh** ([[Adilmetova2024 - ChatGPT multilingual clinical nutrition advice]]).
> - **Cases:** 10 lifestyle/sport goals and 40 clinical conditions: anaemias, thyroid disease, TB, hepatitis B, diabetes types, pregnancy, IBD, NAFLD, CKD/AKI…
> - **Each profile has:** demographics and ethnicity, diagnosis, medications, labs, anthropometry and a **diet history full of Kazakh dishes** (baursak, beshbarmak, plov, kazy, kumys, shelpek…).
> - **The "conclusion" is GPT-4's answer (2023)** to "Provide dietary recommendation for this patient profile" and "Give a specific diet plan for the day … using Central Asian food". **It is not an expert gold standard.**
> - **Rater scores:** the paper's Likert ratings were moderate for EN/RU (≈3.2–3.5 / 5), and the Kazakh outputs were unusable (≈1 / 5). The abstract does not say who the raters were, and the ratings are not released.
>
> It is the only case → diet-advice set built on Central Asian cuisine and patients. 29 of the 50 profiles list current drugs (warfarin, isoniazid, statins, levothyroxine, cholestyramine…), so it can test **food–drug** advice. Use the profiles as inputs and score answers with a rubric; do not treat the GPT-4 text as the reference.

## Access
| | |
|---|---|
| Availability | open-download (Hugging Face, MIT; also on GitHub IS2AI/LLM_for_Dietary_Recommendation_System) |
| Link | https://huggingface.co/datasets/issai/LLM_for_Dietary_Recommendation_System |
| Accessed? | true (not gated, no login needed) |
| How | `uv run hf download issai/LLM_for_Dietary_Recommendation_System --repo-type dataset --local-dir Data/issai-dietary-recommendation`, then the text files were parsed to CSV |
| Downloaded | `Data/issai-dietary-recommendation/Cases_and_Responses/*.zip` (originals) + `derived/cases_responses.csv`, `derived/profiles.csv` (written by `uv run db/prep.py issai`) |

## Tables & columns
### Original files: `Cases_and_Responses/*.zip` (5 zips × 50 `.txt`)
| zip | language of the profile | pipeline (from README and `gpt_response_extraction.py`) | file timestamps |
|---|---|---|---|
| `cases_results.zip` (`N_0_gpt.txt`) | English | prompt sent to GPT-4 as is | 2023-05-31 |
| `cases_results_1.zip` (`N_1_gpt.txt`) | Russian | Russian prompt; Russian follow-up "Предложите конкретный план питания на день…" | 2023-05-31 |
| `cases_results_1_tr.zip` | Russian | prompt machine-translated RU→EN (deep_translator / Google), GPT-4 answered in English, answer back-translated EN→RU | 2023-06-10 |
| `cases_results_2.zip` (`N_2.txt`) | Kazakh | Kazakh prompt; the file holds one combined answer ("1. Тамақтану кеңесі … 2. … күндік тамақтанудың жоспары"); the follow-up prompt is not in the file | 2023-08-23 |
| `cases_results_2_tr.zip` | Kazakh | KK→EN→GPT-4→KK as for `_1_tr` | 2023-06-10 |

- Each file contains: the prompt "Provide dietary recommendation for this patient profile." (or its RU/KK version), then the profile on one line, the first GPT-4 answer, the follow-up "Give a specific diet plan for the day based on the patient profile using Central Asian food.", and the second answer.
- The extraction script calls `model="gpt-4"` with `max_tokens=800` per turn.

### `derived/cases_responses.csv` (250 rows): one row per answer file
| column | type | meaning | example |
|---|---|---|---|
| `case_id` | int | profile number 1–50 (same across languages) | `17` |
| `language` | str | `en` / `ru` / `kk`: language of the profile and stored answer | `kk` |
| `pipeline` | str | `direct` (asked in that language) or `translated` (via English, answer back-translated) | `translated` |
| `source` | str | zip:file | `cases_results_2_tr.zip:17_2_gpt.txt` |
| `profile` | str | the patient profile text (case) | `Tuberculosis Name: Nursultan Age: 55…` |
| `gpt4_recommendations` | str | GPT-4 answer to "Provide dietary recommendation…" | `Dietary Recommendations for Nursultan: 1. Energy Intake…` |
| `gpt4_meal_plan` | str | GPT-4 answer to "Give a specific diet plan … using Central Asian food". Empty for the 50 KK-direct rows, whose answer is all in `gpt4_recommendations`. | `Breakfast: - Oatmeal (Kasha) with milk… kazy…` |

### `derived/profiles.csv` (50 rows): one row per case
| column | type | meaning | example |
|---|---|---|---|
| `case_id` | int | 1–50 | `27` |
| `case_label_en` | str | the case title the authors put before "Name:" | `Stroke` |
| `diagnosis_en` | str | text after "Diagnosis:" (regex, may be empty or overlong) | `Hemorrhagic Stroke Date of stroke: 1 year ago` |
| `medications_en` | str | text after "Medication(s):" (regex) | `Anticoagulants (Warfarin) - prescribed to prevent blood clots` |
| `profile_en`, `profile_ru`, `profile_kk` | str | the profile in each language (from the direct files) | — |

**Profile fields** (English headings; the order varies by author):
- Name, Gender, Age, Nationality/Ethnicity, Location, Marital status, Occupation, Cultural background.
- Medical information: diagnosis, date of diagnosis, symptoms, medical and family history, current medication.
- **Diet / Diet history:** breakfast/lunch/dinner/snacks, often weekday vs weekend, or a 24-h recall.
- Environmental, behavioural & social factors; anthropometry & body composition; biochemical & haematological markers; clinical; additional information (the patient's goal).

These follow the dietetic ABCD assessment (inferred). EN profiles are 959–2,891 characters long.

Sample: `Data/issai-dietary-recommendation/sample.csv` (first 50 answer rows) · `sample_derived_profiles_csv.csv` (all 50 profiles) · full profile: `Data/issai-dietary-recommendation/schema.md`

## Countries & cultures covered
- **[[Kazakhstan]]**: every profile lives in a Kazakh city: Almaty 9, Pavlodar 5, Astana 4, Kyzylorda, Taraz, Shymkent, Aktobe 3 each, Aktau, Atyrau, Semey, Karaganda 2 each…
- **Ethnicities** (Nationality/Ethnicity field) mirror Kazakhstan's mix: "Kazakhstani" 14, Kazakh 8, Russian 3, Uzbek 3, Karakalpak 2, Korean-Kazakh 2, Chinese-Kazakh 2, German-Kazakh 2, Kazakh-Russian 2, and one each Kyrgyz, Tatar, Uyghur, Turkish, Ukrainian…
- **Diet histories reflect each background:**
  - Kazakh dishes for most.
  - Russian cuisine (borscht, pelmeni) for case 3.
  - Korean + Kazakh for case 4.
  - Chinese dishes for case 24.
  - Turkish dishes for case 21.
- **Religion or religious food rules** (Islam, halal, no pork) appear in 17 profiles (regex `halal|pork|islamic|ramadan|religio|muslim`).
- The meal-plan prompt asks explicitly for **Central Asian food**, so the conclusions are culture-specific by design ([[Central Asia]]).

## Cases & conclusions
**One case** (case 17, English profile, abridged):
> *Tuberculosis.* Nursultan, 55, male, Kazakh, Karagandy, retired soldier. TB diagnosed 2 months ago; chronic cough, night sweats, weight loss. **Current medication: isoniazid 300 mg, rifampicin 450 mg, pyrazinamide 1,200 mg, ethambutol 800 mg daily.** 178 cm, 70 kg, BMI 22.1; lung infiltrates; sputum positive for *M. tuberculosis*. Diet before diagnosis: kasha with milk, bread with butter, tea; **beshbarmak**, shalgam drink, salad; shashlik, **pilaf, kumys**; snacks **baursak**, nuts, dried fruit. Lives alone, gardens and reads.

**Reference conclusion** (GPT-4, EN direct, abridged):
- Energy-dense diet in 5–6 small meals; lean protein (fish, poultry, eggs, low-fat dairy); ≥5 servings of fruit and vegetables; whole grains.
- Iron-rich foods with vitamin C; 8–10 glasses of water.
- "Avoid alcohol … as it can interfere with the effectiveness of the tuberculosis medication."
- **Central Asian day plan:** oatmeal kasha with apricots and walnuts + whole-wheat bread with **kazy**; ayran; **laghman**; chicken **shashlik** with Dungan-style rice **pilaf**; **kumys**.
- Note that it recommends kumys, a mildly alcoholic fermented drink, and fish to a patient on isoniazid, without the known isoniazid–histamine/tyramine food warning. This is why the GPT-4 text cannot serve as gold.

**How it was scored (paper):**
- Raters scored each answer on a **5-point Likert scale** for **personalisation**, **consistency with evidence-based guidelines** and **practicality**.
- Mean ± SD:

| | personalisation | consistency | practicality |
|---|---|---|---|
| English | 3.32 ± 0.46 | 3.48 ± 0.43 | 3.25 ± 0.41 |
| Russian | 3.18 ± 0.38 | 3.38 ± 0.39 | 3.37 ± 0.38 |
| Kazakh | 1.01 ± 0.06 | 1.09 ± 0.18 | 1.07 ± 0.15 |

- Kruskal–Wallis P < 0.001; EN and RU each differ from KK (Dunn's test).
- The per-item ratings are not in the dataset. For our eval, reuse the three criteria as a rubric (LLM-judge or dietitian) and add a food–drug-safety criterion.

**Diet / food / food–drug content** (regex counts, 2026-10-07):
- **Diet is central by construction:**
  - 50/50 EN profiles have a `Diet` field.
  - 50/50 RU profiles match `диет|питани`.
  - 50/50 KK profiles match `диета|тамақ|тағам`.
  - Every conclusion is diet advice plus a meal plan.
- **Central Asian dishes in profiles:** 25/50 EN profiles name ≥1.
  - Keywords: baursak/bauyrsak 13 · plov/pilaf/palov 12 · beshbarmak 9 · ayran/katyk 8 · manti/manty 8 · lagman 7 · sorpa/shorpo/shurpa 7 · shelpek 7 · kumys/koumiss/shubat 6 · kazy 6 · shashlik 5 · samsa 5 · kurt/irimshik 2 · naryn 1 · zhent/talkan 1.
- **Central Asian dishes in GPT-4 meal plans** (same keywords, plus Russian/Kazakh spellings `плов|палау|бешбармак|бауырсақ|лагман|қазы|қымыз|айран|сорпа…`):
  - EN 47/50 · RU direct 41/50 · RU via EN 45/50 · KK direct 49/50 (the text is mostly garbled) · KK via EN 46/50.
  - EN plans most often name plov/pilaf (36), ayran/katyk (22), lagman (9), sorpa/shorpo (8), beshbarmak (6), shashlik (6).
- **Medications:** 29/50 profiles list ≥1 current drug or supplement: cases 12–14, 17–20, 22, 23, 26–32, 34, 37, 39–41, 43–50.
  - Examples: levothyroxine, methimazole, ferrous sulfate, the 4 TB drugs, UDCA, tenofovir, donepezil, atorvastatin (3 cases), warfarin, theophylline, PPIs, ACE inhibitors / losartan (7 cases), sitagliptin, metformin + glimepiride, insulin, aspirin + clopidogrel + metoprolol, mesalamine, adalimumab + azathioprine, cholestyramine.
- **Food–drug advice in the GPT-4 answers:**
  - The word "interact" appears in 0 EN answers. Only **4 of the 29** EN answers for medicated cases give an explicit food/alcohol–drug statement:
    - warfarin → keep vitamin K intake consistent (case 27);
    - alcohol × TB drugs (17);
    - alcohol × antivirals (19);
    - potassium × losartan (50).
  - Missing: no grapefruit warning for the 3 atorvastatin cases; no levothyroxine–food timing (12); no cholestyramine–fat-soluble-vitamin note (47).
  - In Russian, `взаимодейств*` appears in 3 RU-direct answers.
- **Food allergy:** 1 profile (case 36: nut allergy plus new reactions to vegetables).

## Linking to the vault's KG
- **Dishes:** the Kazakh dish names in profiles and plans map to the cooked dishes of [[Kyrgyzstan Food Composition Table]] (beshbarmak, plov with barberry, manty, lagman, shorpo, oromo, mastava) and its koumiss row for per-100 g nutrients.
  - They also map to [[Central Asian Digital Visual Food Atlas]] items (pilaf 192/385/580 g, beshbarmak 194/365/541 g, lagman 173/343/515 g, bauyrsak, samsa, kuyrdak, naryn, sorpa, kespe, qurt, irimshik, zhent, kymyz, shubat) for portion grams.
  - Atlas grams × FCT per-100 g gives nutrients per plate, so a plan's sodium or energy can be checked against the case's condition.
  - Only the 11 Kyrgyz dishes are in the unified DB today. Kazakh-only items (baursak, kazy, shelpek, kurt, shubat) need new dish/ingredient rows.
- **Conditions:** the diagnoses are English free text, so use `ConditionResolver.by_text`. Checked 2026-10-07:
  - "Iron Deficiency Anemia" → `MESH:D018798`
  - "Irritable Bowel Syndrome" → `MESH:D043183`
  - "Type 2 diabetes" → `MESH:D003924`
  - "Non-alcoholic Fatty Liver Disease" → `MESH:D065626`
  - "Tuberculosis" → `MESH:D014376`
  - "Hypothyroidism" → `MESH:D007037`
  - **Check ambiguous aliases:** "Gastroesophageal Reflux Disease" resolves to `MESH:D004942` *Esophagitis, Peptic* (a HERB alias), not `MESH:D005764` *Gastroesophageal Reflux* (ICD K21.9).
- **Drugs:** the drug names → the DB `drug` table and [[DrugBank]], [[DDID]], [[FooDrugs]] for food–drug interactions. Checkable examples: warfarin–vitamin K foods, statins–grapefruit, isoniazid–histamine/tyramine foods, levothyroxine–soy/coffee timing, cholestyramine–fat-soluble vitamins, ACE inhibitors / losartan–potassium.
  - This is where a KG-augmented model should beat the GPT-4 answers stored here.

## Versions
- **GitHub:** IS2AI/LLM_for_Dietary_Recommendation_System (MIT, last push 2023-08-23; the old name Chat_GPT_for_Nutritional_Recommendation_System redirects).
- **Hugging Face:** issai/LLM_for_Dietary_Recommendation_System, created and last modified 2025-02-19 (commit 1b33b856). The same 5 zips. Single version.
- The Hugging Face card tags the language as `en` only, but the data is EN/RU/KK.

## Caveats
- **No expert gold.**
  - The answers are GPT-4 (2023) outputs, rated only moderate (≈3.3/5) in EN/RU.
  - The Kazakh direct answers are near-unreadable (rated ≈1/5).
  - The back-translated `_tr` answers carry machine-translation errors.
  - The per-answer ratings were not released.
- **Mock profiles:** written by the study team, not real patients. Formats vary between authors, so structured fields need regex or LLM extraction (`diagnosis_en` / `medications_en` are best-effort).
- **Small:** 50 cases. Only 40 are clinical.
- **Truncation:** `max_tokens=800` per turn may have cut some answers.
- **Split heuristic:** profile/answer boundaries in `derived/` come from text separators. For KK direct rows the plan is inside `gpt4_recommendations`.
- **Duplicate entry:** an older candidate [[ISSAI LLM for Dietary Recommendation System]] (topic `cultural-food-health`) points to the same Hugging Face repo.
