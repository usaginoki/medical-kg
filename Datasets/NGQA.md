---
title: "NGQA"
slug: ngqa
kind: [case]
version: "NGQA_benchmark.csv from the README's Google Drive link (file dated 2024-12-10) + code at Yiyang-Ian-Li/NGQA commit 364b53e (2026-02-02)"
previous_versions: ""
papers: ["[[Zhang2024 - NGQA nutritional graph QA benchmark]]"]
url: "https://github.com/Yiyang-Ian-Li/NGQA"
license: "None stated: no LICENSE file, the GitHub API reports none, and neither the README nor the paper gives a data licence. The inputs are US federal public-domain data (CDC NHANES 2003–2020, USDA FNDDS/WWEIA)."
availability: open-download
access_link: "https://drive.google.com/file/d/1CpFbd5WWjZhu20utl0X5Tsoemc1pSmgF/view"
accessed: true
access_method: [github, website-download]
access_date: 2026-10-07
access_notes: "git clone --depth 1 of the repo (commit 364b53e) gives code and notebooks only. The ready-made benchmark NGQA_benchmark.csv (41.3 MB, 13,802 rows) came from the README's Google Drive link with `uv run --with gdown gdown 1CpFbd5WWjZhu20utl0X5Tsoemc1pSmgF`; it worked with no login. From the raw-data Drive folder we took only fndds_ingredients.csv (4.8 MB, the FNDDS food → ingredient table used to build the ingredient nodes), with the same gdown method. Not downloaded: the per-cycle NHANES XPT folders (0102…1720, 9900) and the FNDDS 2015–2020 xlsx files; they are public CDC/USDA files, needed only to rebuild the benchmark. Code (benchmark_pipeline/, experiments/, requirements.txt) was zipped into code.zip so that the profiler does not read requirements.txt as a table. .git and the repo's .gitignore were dropped."
countries: ["[[United States]]"]
regions: ["[[North America]]"]
n_records: "13,802 user × food items (8,490 sparse / 3,622 standard / 1,690 complex), each in 3 task forms; 5,644 NHANES adults; 849 FNDDS foods; 954 ingredient descriptions"
size: "46 MB on disk (benchmark CSV 41.3 MB)"
formats: [csv]
has_ingredients: true
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: true
body_effect: ""
body_effect_how: ""
join_keys: [NHANES SEQN (respondent id), FNDDS food code, FNDDS/SR Legacy ingredient description (+ ingredient code in fndds_ingredients.csv), WWEIA category]
case_type: [diet]
conclusion_type: [suitability, nutrient-rationale, advice]
languages: [en]
n_cases: "13,802 user-profile × food items (5,644 NHANES adults × 849 foods). Each is answered three ways: yes/no, the deciding nutrient tags, and a one-sentence explanation"
diet_relevance: central
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases, search/evaluation]
tags:
  - type/dataset
  - kind/case
  - case/diet
  - q/4
  - access/accessed
  - access/open
  - region/americas
---
# NGQA

> [!abstract] TL;DR
> NGQA (Nutritional Graph QA) asks whether a given food is healthy for a given person and which nutrients decide it ([[Zhang2024 - NGQA nutritional graph QA benchmark|Zhang et al., ACL 2025]]). It was built by Notre Dame, IBM Research, UConn and Brandeis.
> - **The person:** a real **NHANES 2003–2020** respondent (5,644 adults). The graph gives their health statuses (obesity, hypertension, diabetes, opioid misuse, 9 self-reported special diets) and dietary-habit nodes.
> - **The food:** one of 849 **FNDDS** foods, mostly US mixed dishes and desserts, with ingredients and high/low nutrient tags.
> - **The gold:** derived by rule from nutrient thresholds (EU / Codex claims) and a status → needed-nutrient map.
> - **Size and tasks:** 13,802 items at three difficulty levels; each is asked as yes/no, as nutrient tags, and as a short explanation.
> - **Diet is the whole dataset;** there are no drugs.
> - **Main caveat:** the item's own graph already contains `match` / `contradict` edges between the user's status and the food's tags. So the released task tests reading a graph, not knowing nutrition.
> - **Use for us:** strip those edges and NGQA becomes a clean test of whether our dish → ingredient → compound → condition KG supplies the missing knowledge.

## Access
| | |
|---|---|
| Availability | open-download (GitHub code + Google Drive data; no licence stated) |
| Link | https://github.com/Yiyang-Ian-Li/NGQA · benchmark: https://drive.google.com/file/d/1CpFbd5WWjZhu20utl0X5Tsoemc1pSmgF/view · raw data: https://drive.google.com/drive/folders/1bR_ZGGxet19GC7rbqB5y7oor4WsaGylJ |
| Accessed? | true |
| How | `git clone --depth 1` (commit `364b53e`) · `uv run --with gdown gdown <file id>` for the benchmark and for `fndds_ingredients.csv` |
| Downloaded | `Data/ngqa/processed_data/NGQA_benchmark.csv` (41.3 MB), `Data/ngqa/data/fndds_ingredients.csv` (4.8 MB), `code.zip` (pipeline notebooks + experiment code), `README.md`, `overview.jpg` |

## Tables & columns
Meanings come from the paper (§3–4, App. B), the notebooks `0_raw_data_aggregation`, `1_food_lists_creation` and `2_benchmark_construction`, and `benchmark_pipeline/utils.py` (`generate_pairs`, `generate_answer`, `generate_graph`). "(ours)" marks counts we computed.

### `processed_data/NGQA_benchmark.csv` (13,802 rows)
| column | type | meaning | example |
|---|---|---|---|
| `difficulty` | str | **question level** (not task level): `easy` = *Sparse* (one status ↔ one food tag; 8,490), `medium` = *Standard* (several links, all match or all contradict; 3,622), `hard` = *Complex* (mixed match and contradict; 1,690) | `medium` |
| `question_easy` | str | the **binary task (-B)** prompt: "Based on the nutrients the food provides and the user needs, please answer whether the food "X" is healthy for the user? Please answer with yes or no." The user appears only in the graph | |
| `answer_easy` | str | gold `Yes` / `No`: Yes 6,616 / No 7,186 overall; sparse 4,087 / 4,403, standard 1,916 / 1,706, complex 613 / 1,077 (ours) | `Yes` |
| `question_medium` | str | the **multi-label task (-ML)** prompt: "…what nutrient tags are used to determine whether the food "X" is healthy or unhealthy for the user?" | |
| `answer_medium` | str | gold: comma-separated food tags that bear on the user's needs, from 14 labels (`low_/high_` × carb, sugar, sodium, calorie, protein, cholesterol, saturated_fat); 433 distinct combinations | `low_carb, low_sugar` |
| `question_hard` | str | the **text-generation task (-TG)** prompt: "…whether the food "X" is healthy for the user? Please answer with a short sentence explaining why." | |
| `answer_hard` | str | gold template sentence "Yes/No, because the food is <level> in <nutrient>, …" listing the winning side's reasons; 168 distinct | `Yes, because the food is low in carb, low in sugar.` |
| `node_list` | str (Python literal) | the item's graph nodes `[id, {name, attr}]`. Node 0 = user (`name` = NHANES SEQN, `attr` = `user`). Node 1 = food (`name` = FNDDS food code, `attr` = description). Other types by `name`: `category` (WWEIA), `ingredient` (FNDDS ingredient description), `food_nutrition_tag`, `dietary habit`, `status`, `user_nutrition_tag` (a need with no matching food tag). Mean 27.1 nodes (ours) | `[1, {'name': 58105100, 'attr': 'Pupusa, cheese only'}]` |
| `edge_list` | str (Python literal) | `[source, relation, target]`. Relations: `belongs to` (food → category and food → nutrient tag; the current code writes `contains` for the latter), `has` (food → ingredient, user → habit / status), **`match` / `contradict`** (status → food tag), `need` (status → user_nutrition_tag). Totals: has 249,261; belongs to 88,637; match 14,110; contradict 13,429; need 8,145 (ours) | `[26, 'contradict', 13]` |

**Users (statuses, from `0_raw_data_aggregation`):**
- *Conditions:*
  - **obesity**: BMI ≥ 30 *and* waist ≥ 102 cm (men) / 88 cm (women) in the code; the paper says BMI ≥ 30 only.
  - **hypertension**: mean systolic ≥ 140 or diastolic ≥ 90 mmHg.
  - **diabetes**: serum glucose ≥ 7.0 mmol/L *and* HbA1c ≥ 6.5%.
  - **opioid misuse**: heroin, cocaine or meth use within a year, or a prescription opioid taken for > 90 days (Multum classes 57/58/60 or 191).
- *Special diets:* 9 self-reported diets from the NHANES 24-h recall (`DR1TOT` `DRQSDT*`): weight loss / low calorie, low fat / low cholesterol, low salt, sugar-free, diabetic, weight gain / muscle building, low carbohydrate, high protein, renal / kidney.
- *Status → needed tags* (`reference_dict`):
  - obesity → low_calorie
  - hypertension → low_sodium
  - diabetes → low_sugar + low_carb
  - opioid misuse → high_protein + low_sugar + low_sodium
  - low-fat diet → low_cholesterol + low_saturated_fat
  - renal diet → low_protein
  - weight-gain diet → high_calorie + high_protein
  - the other diets map one-to-one.
- *Status counts (rows, ours):* obesity 4,689 · hypertension 3,285 · low fat 3,237 · low carb 2,527 · sugar-free 2,422 · diabetes 1,925 · high protein 1,736 · weight loss 1,453 · low salt 1,249 · diabetic diet 1,130 · opioid misuse 1,079 · weight gain 882 · renal 738.
- *Statuses per item:* 1 in 7,049 items; up to 9.
- *Dietary habits:* 47 distinct labels in the file (the paper says 54). Examples: "Adds lots of salt at table", "Drinks Alcohol more than average", "Takes more supplements", "Eats lots of fast food". They come from the NHANES diet-behaviour questionnaires (top / bottom 10%). They are **distractors**: the gold never uses them.

**Foods (from `1_food_lists_creation`):**
- *Nutrient values:* per-100 g nutrient values are averaged over all NHANES 2003–2020 24-h recall records of that food code (`DR1IFF` / `DR2IFF`).
- *Tags (low ≤ / high > per 100 g):*
  - calorie 40 / 225 kcal
  - protein 10 / 15 g
  - carbohydrate 55 / 75 g
  - sugar 5 / 22.5 g
  - saturated fat 1.5 / 5 g
  - cholesterol 20 / 40 mg
  - sodium 120 / 200 mg
  - fibre 3 / 6 g and 8 micronutrients are tagged too, but not used in the graphs.
- *Selection:* FNDDS "mixed dishes" plus bakery, desserts and other categories. Near-duplicates are removed by name (keep the most-tagged one per first-2/3-words group), which leaves 849 foods in 35 WWEIA categories.
- *Top categories:* Soups 119 · Cakes and pies 109 · Meat mixed dishes 99 · Seafood mixed dishes 65 · Doughnuts/pastries 46 · Cookies and brownies 45.

**Gold rule (`generate_answer`):** for each nutrient the user needs, if the food carries a tag on that nutrient:
- the same direction is a reason for *yes*;
- the opposite direction is a reason for *no*;
- **Yes iff yes-reasons > no-reasons** (a tie is No).
- `answer_medium` lists all tags involved; `answer_hard` lists the winning side's reasons.
- Food tags that no user status refers to are ignored.

### `data/fndds_ingredients.csv` (36,718 rows)
The FNDDS food → ingredient table that `2_benchmark_construction` uses to add ingredient nodes. The FNDDS release is not stated; we infer one of 2015–2020.

| column | type | meaning | example |
|---|---|---|---|
| `Food code` | int | FNDDS 8-digit food code (= the food node's `name`); 9,260 foods | `58105100` |
| `Main food description` | str | FNDDS food name | `Pupusa, cheese only` |
| `WWEIA Category number` / `description` | int / str | What We Eat in America food category (174 numbers) | `Other Mexican mixed dishes` |
| `Ingredient code` | int | the ingredient's code: an SR Legacy NDB number (< 10⁵), or an FNDDS food code (≥ 10⁷) for sub-recipes. Of the codes used in the benchmark, 173 of 959 are sub-recipe codes (ours) | `1107` |
| `Ingredient description` | str | SR Legacy / FNDDS ingredient name (= the ingredient node's `attr`) | `Restaurant, Latino, pupusas con queso` |

Samples: `Data/ngqa/sample.csv` (fndds_ingredients), `Data/ngqa/sample_processed_data_NGQA_benchmark_csv.csv` · full profile: `Data/ngqa/schema.md`

## Countries & cultures covered
- **[[United States]].**
  - *Users:* NHANES is a national US sample. By SEQN, the users come from every cycle 2003–04 to 2017–18 (492–660 each) plus 1,013 from the 2017–March 2020 pre-pandemic files (ours).
  - Race/ethnicity is **not** in the graph. SEQN joins back to NHANES `DEMO` (`RIDRETH1`: Mexican American, Other Hispanic, Non-Hispanic White, Non-Hispanic Black, Other), so ethnic subgroups could be added.
- **Foods are US-consumed foods, some with an ethnic origin in the name** (regex over food names, ours):

| group | foods | items |
|---|---|---|
| "Puerto Rican style" / Caribbean | 58 | 941 |
| Mexican / Central American (taco, burrito, enchilada, tamale, pupusa, empanada…) | 71 | 1,162 |
| Asian (sushi, chow mein, pho, bibimbap, tteokbokki, biryani, dosa, curry, teriyaki…) | 41 | 654 |

  - There is no cuisine label. WWEIA categories mix origins: the Salvadoran pupusa sits in "Other Mexican mixed dishes".
  - The nutrient thresholds come from the EU Nutrition & Health Claims Regulation and Codex; the status definitions are AHA / WHO style.

## Cases & conclusions
**One case** (CSV row 6,586; standard level). The question names only the food. The model gets the item graph as triples:
- *Graph:*
  - **Food:** Pupusa, cheese only [58105100]
    - belongs to → Other Mexican mixed dishes
    - has → "Restaurant, Latino, pupusas con queso"
    - nutrient tags → low_carb, low_sugar, high_sodium, high_calorie, high_saturated_fat
  - **User:** NHANES SEQN 26009
    - has habits → drinks lots of milk, eats little or no fish or shellfish, drinks alcohol less than average, takes few or no supplements, uses lots of salt in preparation, ate more food than usual
    - has status → **diabetes**
  - **Links:** diabetes → *match* → low_sugar; diabetes → *match* → low_carb.
- *Gold:*
  - -B **Yes**
  - -ML `low_carb, low_sugar`
  - -TG "Yes, because the food is low in carb, low in sugar."
- *Note:* the high-sodium, high-saturated-fat, high-calorie tags do not count, because the user's statuses do not mention them. This shows how narrow the rule is.

**Scoring** (`experiments/evaluate.py`):
- *-B:* accuracy, precision, recall and F1. An output that is neither Yes nor No counts as wrong.
- *-ML:* instance Jaccard "accuracy", plus weighted precision, recall and F1 over the 14 tags.
- *-TG:* ROUGE-1/2/L, BLEU and BERTScore against the template sentence.
- *Published results* (GPT-4o-mini, -B accuracy, sparse / standard / complex):
  - plain graph-RAG: 0.597 / 0.576 / 0.660
  - CoT-Zero: 0.660 / 0.657 / 0.663
  - **ToG: 0.773 / 0.863 / 0.747**
  - Recall is low everywhere: the models over-answer "No".
  - Llama-3.1-70B with ToG: 0.848 / 0.865 / 0.722.

**Food, diet, herbs, food–drug.**
- All 13,802 items are diet suitability (**diet_relevance: central**).
- There are no herbs, no traditional medicine and no drug nodes.
- Drugs touch the data only indirectly: "opioid misuse" is partly defined from prescription-opioid use, and the habit nodes "Takes more supplements" (4,487 rows) and "Takes few or no supplements" (5,853) carry no interaction content.

## Linking to the vault's KG
Here "KG" is the [[Unified database]], specifically its `ingredient`, `compound` and `condition` tables ([[Export tables]]). All numbers below are ours, from `db/unified.duckdb`.
- **Foods → dishes.** The 849 FNDDS foods, with their FNDDS ingredient lists, could enter the `dish` table as US dishes. No FNDDS dishes are loaded yet.
- **Ingredients → `ingredient`.**
  - `IngredientResolver.by_text(fuzzy=False)` resolves **857 of 954 ingredient descriptions (90%; 4,975 of 5,156 food–ingredient mentions) to 216 ingredient ids**. 594 of the 849 foods resolve completely.
  - The match works on the first comma segment of SR-style names, so it is coarse: "Crustaceans, lobster" → `crustaceans`, "Pie, coconut creme" → `pie`.
  - Unresolved examples: hot-dog rolls, water chestnuts, doughnuts, frostings, "Restaurant, Chinese…".
  - Of the 216, **157 have compounds and 66 have [[DDID]] drug edges**.
  - The exact route would be ingredient code (SR NDB number) → [[USDA FoodData Central]] SR Legacy `NDB_number` → `fdc_id`. But the KG's `ingredient_xref` has **no `usda_ndb` rows and only 38 `usda_fdc` rows**, so today it yields 0 matches; adding an NDB xref would fix that.
- **Nutrient tags → `compound` (`is_nutrient`):**

| NGQA tag | compound |
|---|---|
| sodium | `IK:KEAYESYHFKHZAL-UHFFFAOYSA-N` Sodium |
| carb | `MESH:D004040` Dietary Carbohydrates |
| sugar | `MESH:D000073417` Dietary Sugars |
| protein | `MESH:D004044` Dietary Proteins |
| cholesterol | `MESH:D002791` Cholesterol, Dietary |
| saturated fat | `NAME:saturated-fatty-acids` (not flagged as a nutrient) |
| calorie | **none: the KG has no energy node** |

- **Statuses → `condition`:**
  - obesity `MESH:D009765`
  - hypertension `MESH:D006973`
  - diabetes `MESH:D003920` (or T2D `MESH:D003924`)
  - opioid misuse `MESH:D009293` Opioid-Related Disorders
  - renal diet → `MESH:D051436` / `MESH:D007674`
  - low-fat diet → `MESH:D006949` Hyperlipidemias (proxy, our choice)
  - The other diets are not conditions.
- **Does the KG know NGQA's rules?** Partly. `compound_condition` has:
  - sodium → hypertension ([[FooDB]] and [[Dr. Duke's Phytochemical and Ethnobotanical Databases|Duke]] "harmful", [[CTD]] "marker");
  - dietary sugars → obesity and T2D; carbohydrates → obesity; dietary cholesterol → hyperlipidaemia (all CTD "marker").
  - There is no protein → CKD edge and no nutrient edge to opioid-related disorders.
  - Most links are associations ("marker"), not "limit this nutrient" guidance. That guideline layer is exactly what NGQA's `reference_dict` encodes and our KG lacks; [[FAM-Bench]]'s condition rules are a similar source.
- **KG test design:**
  1. Keep the profile (statuses, optionally habits) and the food name, plus ingredients for an ingredient-level variant.
  2. Delete the `food_nutrition_tag`, `user_nutrition_tag`, `match`, `contradict` and `need` nodes and edges, which give the answer away.
  3. Ask -B / -ML / -TG with no context, then with our KG paths: dish → ingredients → nutrient compounds (amounts per 100 g from [[USDA FoodData Central]] / FooDB) → conditions.
  - The ~170 Puerto Rican, Mexican / Central American and Asian-named foods give a small cultural slice.

## Versions
- **Paper:** arXiv v1 2024-12-20 (the only version); ACL 2025 main conference, long paper (Vienna), pp. 5934–5966, DOI 10.18653/v1/2025.acl-long.296.
- **Data and code:** one benchmark file, on Drive and dated 2024-12-10. The repo was cleaned up and released in December 2024 (`add file links`, 2024-12-14); the 2026-02 commits only add the ACL citation to the README.
- **Release drift:**
  - The current `generate_graph` writes food → tag edges as `contains`, while the released CSV has `belongs to`. So the CSV comes from an earlier code state (inferred).
  - The paper reports 54 habit tags; the file has 47.

## Caveats
- **Answer leakage:** each item's graph contains the status → tag `match` / `contradict` edges that decide the label. The published scores therefore measure graph reading and retrieval (ToG prunes noise), not nutrition knowledge.
- **Rule-made gold.** Labels follow from thresholds and the status map by counting. Ties → No. Food tags that no status refers to are ignored (see the pupusa). Habits never matter. "Three human annotators" validated the scheme (paper), but there is no per-item clinical judgement.
- **136 complex items (ours)** where counting `match` vs `contradict` edges in the graph gives the opposite of the gold. The gold counts distinct user tags; the graph repeats a tag when two statuses need it.
- **Diet-habit labels look misassigned (ours).** Eight special-diet statuses each co-occur in 100% of their rows with a *different* diet habit:

| status | habit always present | rows |
|---|---|---|
| Low fat/Low cholesterol diet | "Eats weight loss diet" | 3,237 |
| Low carbohydrate diet | "Eats high protein diet" | 2,527 |
| Sugar free/Low sugar diet | "Eats low salt diet" | 2,422 |
| High protein diet | "Eats gluten free diet" | 1,736 |
| Low salt/Low sodium diet | "Eats low fat diet" | 1,249 |
| Diabetic diet | "Eats high fiber diet" | 1,130 |
| Weight gain/Muscle building diet | "Eats diabetic diet" | 882 |
| Renal/Kidney diet | "Eats low carb diet" | 738 |

  - In 7 of the 8 pairs the habit label names the diet next to the status in NHANES's `DRQSDT` code list (e.g. low fat = DRQSDT2 → "weight loss" = DRQSDT1), so the habit labels look misassigned against the codes.
  - These habit nodes contradict the status nodes and can mislead a model.
- **Definitions.**
  - Obesity in the code needs BMI ≥ 30 and a high waist circumference; the paper says only BMI.
  - Diabetes in the code uses only lab values (glucose ≥ 7.0 mmol/L and HbA1c ≥ 6.5%), although the paper also mentions the NHANES diabetes questionnaire.
  - "Opioid misuse" mixes illicit use with long-term prescription opioid use.
- **Users:** adults only. SEQN is real NHANES respondent ids from public files. The 2017–18 and 2017–March 2020 (P) files overlap in time, so one person may appear under two SEQNs (not checked).
- **Food values:** averaged over 24-h recall records per 100 g, not taken from FNDDS nutrient tables. Portion size is ignored. Only US foods, and no cuisine labels.
- **Licence:** none stated. We committed 50-row samples of both files (no licence forbids it, and the content derives from US public-domain data). Delete them if a stricter reading is wanted.
