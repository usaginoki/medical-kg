---
title: "NII Cookpad Dataset"
slug: nii-cookpad-dataset
kind: [food]
version: "Cookpad recipe & meal data (recipes/meals up to 2014-09-30; distributed since 2015-02-24; page updated 2023-06-29)"
previous_versions: ""
papers: ["[[Harashima2016 - Cookpad recipe and meal data collection]]"]
url: "https://www.nii.ac.jp/dsc/idr/cookpad/"
license: "Cookpad data-provision terms + NII IDR service terms; academic research only; contract signed with official seal"
availability: on-request
access_link: "https://www.nii.ac.jp/dsc/idr/cookpad/"
accessed: false
access_method: []
access_date: 2026-09-30
access_notes: "Needs an institutional application. Researchers at universities or public research institutes send the application form (利用申請書, Word) by email to NII IDR (idr@nii.ac.jp); a person with contract authority signs and seals a written agreement (同意書); NII then provides a download. Others must ask Cookpad (recipe-corpus@cookpad.com). Not attempted, since it needs the user's institution. As context only, Data/nii-cookpad-dataset/ holds public term-frequency dictionaries that Kyoto University derived from the dataset's step texts."
countries: ["[[Japan]]"]
regions: ["[[East Asia]]"]
n_records: "~1,715,000 recipes (1,715,589 per Kyoto Univ. text extraction); ~36,000 meals; ~10M tsukurepo reviews; ~146,000 recipes in ~1,100 categories"
size: "1.8 GB 7z MySQL dump (~5.5 GB unpacked), 12 tables"
formats: [mysql-dump]
has_ingredients: true
has_amounts: yes
has_cooking_method: steps
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [recipe id, meal id, ingredient name (Japanese)]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/blocked
  - access/request
---
# NII Cookpad Dataset

> [!abstract] TL;DR
> All **~1.72M Japanese recipes and ~36k meals (献立)** posted on Cookpad, Japan's largest recipe site, up to Sept 2014. Records carry titles, descriptions, ingredients with quantities and servings, steps, tips, history, ~1,100 user categories and ~10M "tsukurepo" cook-reports. Meals link main and side dishes, so the data shows **how Japanese home meals are combined**. Cookpad distributes it through NII's IDR as a MySQL dump, only to academic researchers who apply as an institution. **We have not accessed it.**

> [!warning] Needs user action
> Applying is an institutional process, detailed under *Access* below.
> The terms also restrict **LLM use**: feeding the data to an external generative-AI service counts as prohibited third-party disclosure. The exception is a service that guarantees no training on inputs, such as OpenAI API business terms; consumer ChatGPT is not allowed. This matters for our agent pipeline.

## Access
| | |
|---|---|
| Availability | on-request (institutional application + signed contract) |
| Link | <https://www.nii.ac.jp/dsc/idr/cookpad/> |
| Accessed? | false |
| How | none. The only files downloaded are public derived term dictionaries (see below) |
| Downloaded | `Data/nii-cookpad-dataset/public_derived_kyoto_recipe_term_dictionaries/`: 3 TSVs (not the dataset itself) |

**Application procedure** (from the NII page, updated 2023-06-29):
1. Eligibility: researchers at universities or public research institutes, for **academic research only**. Others ask Cookpad directly at recipe-corpus@cookpad.com.
2. Download the application form `documents/application_ckpd_1_4.docx` from the page. Also read the Cookpad data terms (<https://cookpad.com/jp/terms_others#cookpad_data_academy>) and the IDR service terms.
   - One application per lab. The PI must be a full-time staff member.
   - The contracting person must have signing authority and an official seal, usually dean level.
   - Group members must belong to the same organisation.
3. Email the form to IDR (idr [at] nii.ac.jp) with the subject `クックパッドデータ利用申請（<University>）`.
4. IDR checks eligibility and forwards the application to Cookpad; this takes a few days.
5. IDR emails the agreement (同意書). Stamp it with the official seal and **post it** to NII, 2-1-2 Hitotsubashi, Chiyoda-ku, Tokyo.
6. Download from the IDR web server.

After access you must:
- notify Cookpad 30 days before any publication,
- state in publications that the data was used,
- file an annual usage report.

**Public derived resource we did download.** Kyoto University (Sasada, Mori lab) ran KyTea word segmentation and PWNER recipe-NER over the `steps` table of this dataset. They published term-frequency dictionaries at <https://www.lsta.media.kyoto-u.ac.jp/resource/data/recipe/cookpaddata.html> (dated 2015-07-03). We took the Food (F), Tool (T) and chef-Action (Ac) dictionaries.

## Tables & columns
### Dataset itself (not accessed; from docs)
The dump holds **12 MySQL tables: 6 for recipes and 6 for meals** (Harashima et al. 2016). We could not see the table names or columns. The one confirmed name is `steps`, which the Kyoto guide queries with `select * from steps`. The fields below come from the paper's description of the recipe and meal templates.

| entity | field | meaning |
|---|---|---|
| recipe | recipe id, author id, upload date | unique ids (author id anonymised) |
| recipe | title | ≤ 20 characters, e.g. 豚のにんにく醤油焼き |
| recipe | description | eye-catching summary shown as the search snippet |
| recipe | ingredients | ingredient names **with quantities**, plus the number of servings |
| recipe | steps | ordered cooking steps (8,849,850 sentences over 1,715,589 recipes per Kyoto Univ.) |
| recipe | advice / points to note | tips, e.g. substitutions |
| recipe | history | why and how the recipe was created |
| recipe-related | categories | ~146,000 recipes in ~1,100 user categories (meat, seafood, vegetable dishes …) |
| recipe-related | tsukurepo | ~10M cook-reports (reviews by people who made the recipe) |
| meal | meal id, author id, date, title | ~36,000 meals, e.g. ドライカレープレート |
| meal | noteworthy points, cooking time (minutes, from fixed options), advice | meal-level text |
| meal | main dishes, side dishes | links to recipe records |
| meal-related | categories, votes | e.g. Japanese style or Western style; user votes |

### `public_derived_kyoto_recipe_term_dictionaries/food_terms_F.tsv` (271,078 rows)
| column | type | meaning | example |
|---|---|---|---|
| `count` | int | occurrences of the term in the Cookpad step texts (auto-tagged) | 687308 |
| `percent` | float | share of all terms with this tag | 2.82 |
| `term` | str | surface form tagged as Food (F) by PWNER | 水 |
| `tag` | str | recipe-NE tag (F = food) | F |

`tool_terms_T.tsv` (26,535 rows, tag T = tool) and `chef_action_terms_Ac.tsv` (59,874 rows, tag Ac = chef action) have the same columns. Top foods: 水 (water), 塩 (salt), 油 (oil), 砂糖 (sugar). Top actions: 入れ (put in, 10.8%), 混ぜ (mix, 5.8%).

Sample: `Data/nii-cookpad-dataset/sample.csv` · full profile: `Data/nii-cookpad-dataset/schema.md`

## Countries & cultures covered
- **[[Japan]]**: all ~1.72M recipes and ~36k meals. The dataset is Japanese-language.
- There is no prefecture field. Meals carry style categories such as Japanese style or Western style.

## Ingredients, amounts, cooking method
- **Ingredients and amounts:** yes. Quantities and servings are template fields, so they are more structured than XiaChuFang's fused strings.
- **Cooking method:** ordered steps, plus tips.
- **Nutrition:** none. Ingredients can be mapped to [[Standard Tables of Food Composition in Japan]] by Japanese food name.
- **Meal composition** (main and side dishes) is unusual among recipe datasets and useful for whole-meal advice.

## Linking to other datasets
- Ingredient names (Japanese) → [[Standard Tables of Food Composition in Japan]] `food_name_ja` for nutrient estimates. Needs normalisation, e.g. 豚肉 → ぶた 肉類.
- Dishes → [[Our Regional Cuisines (Japan MAFF)]] dish names for regional or traditional context.
- Related Cookpad resources, which need separate applications: Cookpad Image Dataset (SIGIR 2017), the Kyoto flow-graph corpus (266 recipes), and the Cookpad/OSX cooking-video dataset.

## Versions
One release (Feb 2015), with data up to 2014-09-30. Later page updates only changed contacts and procedures.

## Caveats
- Access needs an institution with a seal-signed contract, and publications need 30-day pre-notification.
- LLM restriction as above.
- The data is from 2014 and reflects Cookpad's user base: home cooks, mostly women.
- The table layout here is reconstructed from the paper, not verified.
