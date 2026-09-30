---
title: "ArabCulture"
slug: arabculture
kind: [food]
version: "HF MBZUAI/ArabCulture (last update 2025-05-23)"
previous_versions: ""
papers: ["[[Sadallah2025 - Commonsense Reasoning in Arab Culture]]"]
url: "https://huggingface.co/datasets/MBZUAI/ArabCulture"
license: "CC-BY-NC-SA-4.0"
availability: open-download
access_link: "https://huggingface.co/datasets/MBZUAI/ArabCulture"
accessed: true
access_method: [huggingface]
access_date: 2026-09-30
access_notes: "Full dataset (13 per-country parquet test splits) downloaded without login; not gated. Only main_fig.png skipped."
countries:
  - "[[Algeria]]"
  - "[[Egypt]]"
  - "[[Jordan]]"
  - "[[Lebanon]]"
  - "[[Libya]]"
  - "[[Morocco]]"
  - "[[Palestine]]"
  - "[[Saudi Arabia]]"
  - "[[Sudan]]"
  - "[[Syria]]"
  - "[[Tunisia]]"
  - "[[United Arab Emirates]]"
  - "[[Yemen]]"
regions: ["[[Middle East]]", "[[North Africa]]"]
n_records: "3,482 MCQ items (724 in the Food topic)"
size: "0.7 MB"
formats: [parquet, csv]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [country, sub-topic (meal slot), dish names in Arabic free text]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
---
# ArabCulture

> [!abstract] TL;DR
> ArabCulture (Sadallah et al., MBZUAI, ACL 2025) is a 3,482-item cultural commonsense benchmark written from scratch
> in Modern Standard Arabic by 26 native annotators (2 per country) from **13 Arab countries** in the Gulf (Saudi
> Arabia, UAE, Yemen), Levant, North Africa and Nile Valley. Each item is a one-sentence everyday scenario with three
> completions, only one culturally right for that country. The **Food** topic (724 items: breakfast, lunch, dinner,
> Ramadan iftar and sahoor, dessert, fruits, snacks) is a country-labelled record of typical meals — e.g. that a
> Saudi breakfast after Fajr is ful with bread, or that Emiratis break the fast with dates and coffee — which is
> exactly the GCC meal-pattern knowledge the agent needs, though only as short Arabic sentences, not recipes.

## Access
| | |
|---|---|
| Availability | open-download (HF, CC-BY-NC-SA-4.0) |
| Link | https://huggingface.co/datasets/MBZUAI/ArabCulture |
| Accessed? | yes |
| How | `hf download MBZUAI/ArabCulture --repo-type dataset` |
| Downloaded | `Data/arabculture/<Country>/test-00000-of-00001.parquet` × 13 (3,482 rows) + README; derived `Data/arabculture/food_subset.csv` (724 food rows, options flattened, English sub-topic added) |

## Tables & columns
### `<Country>/test-00000-of-00001.parquet` (13 files, 239–290 rows each, 3,482 total × 11)
| column | type | meaning | example |
|---|---|---|---|
| `worker_id` | str | annotator (2 per country) | `Jordan-1` |
| `sample_id` | str | `<n> \| <English sub-topic>` | `1 \| Breakfast` |
| `sub_topic` | str | sub-topic in Arabic (54 sub-topics, 12 topics) | `الافطار` |
| `first_statement` | str | scenario premise (MSA) | `يتناول محمد وجبة الإفطار بعد صلاة الفجر` ("Muhammad eats breakfast after Fajr prayer", our translation) |
| `options` | struct | `arabic_keys` (أ ب ج), `english_keys` (A B C), `text` (3 candidate completions) | `['يشمل الإفطار الفول مع الخبز', 'يشمل الإفطار البرجر مع البيض', 'يشمل الإفطار البيتزا مع البطاطس']` |
| `answer_key` | struct | `arabic_answer_key`, `english_answer_key` | `A` |
| `relevant_to_this_country` | str | validator: fits this country | `Yes` |
| `relevant_to_other_countries` | str | validator: also true elsewhere; `No` = country-specific (CS) | `No` |
| `should_discard` | str | QC flag (all `No` in the release) | `No` |
| `country` | str | country (`KSA`, `UAE` abbreviations) | `Jordan` |
| `region` | str | Gulf / Levant / North Africa / Nile Valley | `Levant` |

### `food_subset.csv` (724 rows × 12) — derived by us
Rows whose English sub-topic is in the paper's **Food** topic (Table 8): Breakfast, Lunch, Dinner, Sahoor (Ramadan),
Iftar (Ramadan), Dessert, Fruits, Snacks. Same columns plus `en_sub` (English sub-topic), `options` as
`A || B || C` text and `answer` (A/B/C).

Sample: `Data/arabculture/sample.csv` (food subset) · full profile: `Data/arabculture/schema.md`

## Countries & cultures covered
13 countries, 4 regions. "Food" = the 8 food sub-topics above; "food-adjacent" = `wedding food` + `eating habits`
(topics Wedding and Habits). "Country-specific" = `relevant_to_other_countries == No`.

| region | country | all items | Food items | of which country-specific | food-adjacent |
|---|---|---|---|---|---|
| Gulf | [[Saudi Arabia]] (`KSA`) | 261 | 53 | 21 | 8 |
| Gulf | [[United Arab Emirates]] (`UAE`) | 283 | 59 | 28 | 8 |
| Gulf | [[Yemen]] | 273 | 57 | 36 | 7 |
| Levant | [[Jordan]] | 290 | 59 | 1 | 7 |
| Levant | [[Lebanon]] | 255 | 55 | 27 | 8 |
| Levant | [[Palestine]] | 273 | 58 | 7 | 8 |
| Levant | [[Syria]] | 279 | 58 | 13 | 8 |
| Nile Valley | [[Egypt]] | 265 | 56 | 40 | 7 |
| Nile Valley | [[Sudan]] | 256 | 57 | 50 | 4 |
| North Africa | [[Algeria]] | 271 | 56 | 28 | 7 |
| North Africa | [[Libya]] | 239 | 49 | 21 | 7 |
| North Africa | [[Morocco]] | 276 | 54 | 33 | 8 |
| North Africa | [[Tunisia]] | 261 | 53 | 27 | 6 |
| | **total** | **3,482** | **724** | **332** | **93** |

Food items per sub-topic are nearly uniform across countries (Breakfast 8–10, Lunch 8–10, Iftar 7–10, Sahoor 8–10,
Dessert 6, Fruits 4–6, Dinner 2–4, Snacks 2–4). Priority-region coverage: GCC = Saudi Arabia and UAE only (no
Qatar, Kuwait, Bahrain, Oman); plus Yemen and the Levant. No Central/South/East Asia.

## Ingredients, amounts, cooking method
Not a recipe dataset. The correct completion usually names the typical dish or components of a meal, so dishes
and some ingredients can be extracted (Arabic NER/LLM needed). Examples (our translations):
- Saudi Arabia, Breakfast — "Muhammad eats breakfast after Fajr prayer" → **ful (fava beans) with bread** (vs
  burger with eggs / pizza with fries).
- UAE, Iftar — "Ahmad drinks coffee at iftar" → **breaks his fast with dates and coffee** (vs croissant / donuts).
- Yemen, Lunch — saltah (سلتة) → **with more meat** (vs fish / flour).
- Syria, Dessert — Nabulsiyeh from kunafa dough → **spread on a tray with cheese and baked until the cheese melts**
  (this one is a preparation step).
- Sudan, Sahoor — ruqaq → **layered like kisra**.
No amounts or nutrition.

## Linking to other datasets
- Dish names are Arabic free text; match to [[WorldCuisines]] (its `location_and_cuisines.csv` and `Alias` give Arabic
  names) or [[World Wide Dishes]] (Arabic `local_name`s) by transliteration/fuzzy matching.
- [[BLEnD]] (SemEval-2026) covers Saudi Arabia, Egypt and Morocco with open-ended food questions — complementary to
  ArabCulture's MCQ scenarios.

## Versions
One release (Dec 2024 HF repo, updated May 2025; arXiv Feb 2025 → ACL 2025). Derivatives on HF (not processed):
`Almheiri/ArabCulture-Dialogue` (ACL 2026; 3,471 parallel MSA–dialect dialogue pairs, same 13 countries and 54
sub-topics, CC-BY-SA-4.0), `go-inoue/ArabCulture_undiac`, `go-inoue/ArabCulture_full`, `qimma/MCQ_ArabCulture`.

## Caveats
- Non-commercial licence (CC-BY-NC-SA-4.0).
- Two annotators per country: scenarios reflect their knowledge. The paper labels 46% of items country-specific; in the released `relevant_to_other_countries` column only 1,310/3,482 (38%) are `No`, so the column is not identical to the paper's CS label.
- MCQ format: the wrong options are deliberately plausible-but-foreign, so only the correct completion is data.
- Text is MSA only (dialect dish names are often transliterated inconsistently).
