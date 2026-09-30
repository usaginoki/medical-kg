---
title: "Food.com Recipes and Interactions"
slug: food-com-recipes-and-interactions
kind: [food]
version: "Kaggle v2 (last updated 2019-11-08)"
previous_versions: "Kaggle v1 (2019)"
papers: ["[[Majumder2019 - Personalized recipe generation]]"]
url: "https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions"
license: "Kaggle: 'Data files © Original Authors' (no open licence; recipes scraped from Food.com)"
availability: open-download
access_link: "https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions"
accessed: true
access_method: [kaggle]
access_date: 2026-09-30
access_notes: "kagglehub download without login (852 MB). Kept RAW_recipes.csv + interactions_train/validation/test.csv (~323 MB); skipped RAW_interactions.csv (349 MB, review text) and the tokenised PP_recipes/PP_users/ingr_map.pkl to stay within budget. Cuisine counts derived by us from the tags column (cuisine_tag_counts.csv, country_recipe_counts.csv)."
countries: ["[[United States]]", "[[Italy]]", "[[Mexico]]", "[[Canada]]", "[[Australia]]", "[[India]]", "[[Greece]]", "[[France]]", "[[United Kingdom]]", "[[China]]", "[[Germany]]", "[[Thailand]]", "[[Spain]]", "[[Morocco]]", "[[Japan]]", "[[Ireland]]", "[[New Zealand]]", "[[Poland]]", "[[Russia]]", "[[Switzerland]]", "[[Sweden]]", "[[Portugal]]", "[[Vietnam]]", "[[South Africa]]", "[[Hungary]]", "[[Lebanon]]", "[[Turkey]]", "[[Cuba]]", "[[South Korea]]", "[[Iran]]", "[[Brazil]]", "[[Denmark]]", "[[Netherlands]]", "[[Indonesia]]", "[[Philippines]]", "[[Egypt]]", "[[Norway]]", "[[Finland]]", "[[Austria]]", "[[Belgium]]", "[[Pakistan]]", "[[Czech Republic]]", "[[Argentina]]", "[[Peru]]", "[[Malaysia]]", "[[Puerto Rico]]", "[[Saudi Arabia]]", "[[Iraq]]", "[[Palestine]]", "[[Ethiopia]]", "[[Chile]]", "[[Colombia]]", "[[Nepal]]", "[[Costa Rica]]", "[[Venezuela]]", "[[Cambodia]]", "[[Iceland]]", "[[Libya]]", "[[Nigeria]]", "[[Ecuador]]", "[[Guatemala]]", "[[Honduras]]", "[[Georgia]]", "[[Laos]]", "[[Sudan]]", "[[Angola]]", "[[Mongolia]]", "[[Somalia]]", "[[Namibia]]"]
regions: ["[[North America]]", "[[Europe]]", "[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "231,637 recipes; 718,379 interactions in the train/val/test splits (1.1M+ raw reviews not downloaded)"
size: "852 MB full; 309 MB downloaded"
formats: [csv, pkl]
has_ingredients: true
has_amounts: no
has_cooking_method: steps
has_nutrition: true
body_effect: no
body_effect_how: "Recipe dataset; no compound or health fields (nutrition %DV only)"
join_keys: [Food.com recipe id, ingredient name (free text)]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
  - region/global
---
# Food.com Recipes and Interactions

> [!abstract] TL;DR
> 231,637 English recipes scraped from Food.com (1999–2018) with ingredient lists (no quantities), step-by-step
> instructions, a 7-value nutrition vector and ~550 user tags, plus user ratings. Released by UCSD (McAuley lab) for
> personalised recipe generation. Culture enters only via **cuisine tags**: 72,837 recipes carry a tag that we
> map to one of 69 countries, and 91,102 carry a country- or region-level cuisine tag. It is heavily
> US-centric (31.6k US-tagged recipes), but it does have small, usable sets for the priority regions
> (India 2,708, China 2,008, Thailand 1,208, Japan 851, Lebanon 308, Turkey 286, Iran 252, Saudi Arabia 102).

## Access
| | |
|---|---|
| Availability | open-download (Kaggle, no login needed through `kagglehub`) |
| Link | https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions |
| Accessed? | yes (a subset of the files) |
| How | `uv run python -c "import kagglehub; print(kagglehub.dataset_download('shuyangli94/food-com-recipes-and-user-interactions'))"`, then copied files |
| Downloaded | `Data/food-com-recipes-and-interactions/`: `RAW_recipes.csv` (295 MB), `interactions_{train,validation,test}.csv` (29 MB), plus our derived `cuisine_tag_counts.csv`, `country_recipe_counts.csv`. Not copied: `RAW_interactions.csv` (349 MB, full reviews with text), `PP_recipes.csv`/`PP_users.csv`/`ingr_map.pkl` (BPE-tokenised versions for the paper's model) |

## Tables & columns
### `RAW_recipes.csv` (231,637 recipes; schema.md reports 267,782 lines because descriptions contain newlines)
| column | type | meaning | example |
|---|---|---|---|
| `name` | str | recipe name (lower-cased) | `aab goosht e baadenjaan` |
| `id` | int | Food.com recipe id | `213132` |
| `minutes` | int | minutes to prepare | `135` |
| `contributor_id` | int | user who submitted the recipe | `47892` |
| `submitted` | date | submission date (1999-08-06 … 2018-12-04) | `2005-09-16` |
| `tags` | list[str] | Food.com tags (552 distinct): course, time, diet, occasion, **cuisine** (country/region) | `['…', 'cuisine', 'middle-eastern', 'iranian-persian', …]` |
| `nutrition` | list[float] | [calories (#), total fat (PDV), sugar (PDV), sodium (PDV), protein (PDV), saturated fat (PDV), carbohydrates (PDV)] per serving (Kaggle docs; PDV = % daily value) | `[924.1, 52.0, 109.0, 8.0, 88.0, 71.0, 39.0]` |
| `n_steps` | int | number of steps | `18` |
| `steps` | list[str] | ordered instruction steps | `['peel and thinly slice onions', 'fry in oil until slightly golden', …]` |
| `description` | str | free-text description by the author | `autumn is my favorite time of year…` |
| `ingredients` | list[str] | ingredient names, no amounts (14,942 distinct strings) | `['lamb shoulder', 'split peas', 'eggplants', …, 'turmeric']` |
| `n_ingredients` | int | number of ingredients | `10` |

### `interactions_{train,validation,test}.csv` (698,901 / 7,023 / 12,455 rows)
The paper's sequential leave-one-out splits (most recent review per user → test, second most recent → validation).

| column | type | meaning | example |
|---|---|---|---|
| `user_id` | int | Food.com user id | `2046` |
| `recipe_id` | int | Food.com recipe id (→ `RAW_recipes.id`) | `4684` |
| `date` | date | review date | `2000-02-25` |
| `rating` | float | 0–5 star rating | `5.0` |
| `u` | int | contiguous user index used by the model (inferred) | `22095` |
| `i` | int | contiguous recipe index used by the model (inferred) | `44367` |

### Derived by us: `cuisine_tag_counts.csv`, `country_recipe_counts.csv`
`tag, level, maps_to, n_recipes` for every cuisine-like tag (94 country-level and 15 region/culture tags), and
`country, n_recipes` after merging sub-national tags (e.g. `szechuan`/`cantonese`/`hunan`/`beijing` → China,
`cajun`/`tex-mex`/`southern-united-states` → United States, `baja`/`oaxacan` → Mexico, `quebec`/`ontario` → Canada).

Sample: `Data/food-com-recipes-and-interactions/sample.csv` · full profile: `Data/food-com-recipes-and-interactions/schema.md`

## Countries & cultures covered
Recipes per country (a recipe with tags for two countries counts once for each), from `country_recipe_counts.csv`:

United States 31,596 · Italy 7,410 · Mexico 6,694 · Canada 4,572 · Australia 2,845 · **India 2,708** · Greece 2,391 ·
France 2,268 · United Kingdom 2,249 · **China 2,008** · Germany 1,377 · **Thailand 1,208** · Spain 1,072 · Morocco 897 ·
**Japan 851** · Ireland 658 · New Zealand 645 · Poland 407 · Russia 381 · Switzerland 375 · Sweden 373 · Portugal 358 ·
**Vietnam 351** · South Africa 324 · Hungary 317 · **Lebanon 308** · **Turkey 286** · Cuba 255 · **South Korea 253** ·
**Iran 252** · Brazil 247 · Denmark 230 · Netherlands 224 · **Indonesia 218** · **Philippines 206** · Egypt 200 ·
Norway 199 · Finland 171 · Austria 170 · Belgium 165 · **Pakistan 141** · Czech Republic 136 · Argentina 124 · Peru 121 ·
**Malaysia 119** · Puerto Rico 106 · **Saudi Arabia 102** · **Iraq 98** · **Palestine 92** · Ethiopia 88 · Chile 76 ·
Colombia 73 · **Nepal 53** · Costa Rica 48 · Venezuela 48 · **Cambodia 46** · Iceland 44 · Libya 40 · Nigeria 38 ·
Ecuador 37 · Guatemala 34 · Honduras 21 · Georgia 17 · **Laos 16** · Sudan 15 · Angola 13 · **Mongolia 13** · Somalia 9 · Namibia 6

Region-level tags: `north-american` 48,479 · `european` 24,912 · `asian` 13,485 · `south-west-pacific` 3,934 ·
`african` 2,851 · `middle-eastern` 2,067 · `central-american` 1,818 · `caribbean` 1,709 · `scandinavian` 1,294 ·
`south-american` 1,255 · `polynesian` 203 · `micro-melanesia` 49. Cultural/religious tags: `jewish-ashkenazi` 612,
`jewish-sephardi` 185, `kosher` 4,446, `ramadan` 279. `congolese` (11) is ambiguous (DRC or Republic of the Congo) and is
not in `countries`. No Central Asian or GCC-other (UAE, Qatar, Kuwait, Oman, Bahrain) tags exist.

> [!warning] Tags are user-assigned on an American site
> "indian" or "iranian-persian" means the uploader labelled it so; many are Americanised adaptations. The tag vocabulary is
> Food.com's (`georgian` is the Caucasus country in Food.com's world-cuisine tree, inferred).

## Ingredients, amounts, cooking method
- **Ingredients**: yes, as normalised names without quantities (`['rice vermicelli', 'sugar', 'ground cardamom', 'rose water', 'olive oil', 'saffron', 'water']`
  for the Saudi *balalit*, id 361328). 14,942 distinct strings; most frequent: salt (85,746 recipes), butter, sugar, onion.
- **Amounts**: no (the original Food.com pages have them; the release strips them).
- **Cooking method**: full ordered `steps` (e.g. Iranian *aab goosht e baadenjaan*, id 213132, 18 steps: "peel and thinly
  slice onions", "fry in oil until slightly golden", … "add salt, black pepper, and turmeric") plus `minutes` and
  technique-ish tags (`oven`, `stove-top`, `deep-fry`, `crock-pot-slow-cooker`, `grilling`).
- **Nutrition**: per-serving calories and six %DV values, computed by Food.com (not lab data).
- Example cultural signal from the data: **turmeric** appears in 3,045 recipes: 44.0 % of `pakistani`, 37.3 % of `indian`,
  22.6 % of `iranian-persian`, 12.7 % of `saudi-arabian`, 8.8 % of `middle-eastern` and 0.3 % of `american` recipes.

## Linking to other datasets
- Ingredient names are free text: they need string/embedding matching to [[USDA FoodData Central]] descriptions or
  [[FooDB]] / [[Phenol-Explorer]] food names (e.g. `turmeric` → FooDB FOOD00068 → curcumin; Phenol-Explorer "Turmeric,
  dried" → curcumin 2,213.57 mg/100 g).
- The `nutrition` vector can be checked against USDA values after ingredient matching (amounts are missing, so only roughly).

## Versions
Kaggle v2 (2019-11-08) is current; v1 was the initial 2019 upload. The paper describes the same crawl (230K+ recipes,
1M+ interactions, 2000–2018).

## Caveats
- Culture labels cover only 39 % of recipes (91,102 / 231,637) and are self-reported tags.
- No quantities, so no reliable per-dish nutrient intake; nutrition is Food.com's computed %DV.
- Licence is "© original authors": fine for research, redistribution unclear.
