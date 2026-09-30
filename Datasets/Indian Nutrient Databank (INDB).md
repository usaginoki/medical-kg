---
title: "Indian Nutrient Databank (INDB)"
slug: indian-nutrient-databank-indb
kind: [food, ingredient]
version: "GitHub main, last commit 2025-04-08"
previous_versions: ""
papers: ["[[Vijayakumar2024 - Development of an Indian food composition database]]"]
url: "https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-"
license: "not stated in the repository (paper is CC BY; IFCT 2017/2004 source tables must be requested from ICMR-NIN)"
availability: open-download
access_link: "https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-"
accessed: true
access_method: [github]
access_date: 2026-09-30
access_notes: "git clone of the full repository: 9 xlsx files plus the Stata do-file. The ICMR-NIN IFCT 2017 and 2004 ingredient tables that INDB.do needs are NOT included (they must be requested from NIN), so the recipe→nutrient pipeline cannot be re-run. The finished recipe nutrient table INDB.xlsx is included."
countries: ["[[India]]"]
regions: ["[[South Asia]]"]
n_records: "1,014 recipes; 10,271 recipe–ingredient rows; 332 distinct ingredient food codes"
size: "2.4 MB"
formats: [xlsx, do]
has_ingredients: true
has_amounts: yes
has_cooking_method: no
has_nutrition: true
body_effect: no
body_effect_how: "Nutrient composition only (energy, macro- and micronutrients). Health effects come only from general nutrition knowledge or by linking ingredients to compound resources."
join_keys: [IFCT 2017 food code, IFCT 2004 food code, UK CoFID food code, USDA FDC id, recipe name]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - kind/ingredient
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# Indian Nutrient Databank (INDB)

> [!abstract] TL;DR
> INDB is an open recipe nutrient database built by Vijayakumar, Dubasi, Awasthi and Jaacks (University of
> Edinburgh / Public Health Foundation of India, *Curr Dev Nutr* 2024). It covers **1,014 commonly eaten Indian
> recipes**. Each recipe has gram/ml/tsp ingredient amounts linked to Indian Food Composition Table codes and
> a nutrient panel of about 40 nutrients, per 100 g and per serving. USDA retention factors are applied.
> Recipes come from two Indian home-science cookbooks (*The Art & Science of Cooking*, *Basic Food
> Preparation*) and 148 recipes from food blogs. For the agent it is a small but carefully built table of
> Indian dishes with real amounts and nutrients (Q1, Q2). It has **no regional or state labels**.

## Access
| | |
|---|---|
| Availability | open download (GitHub) |
| Link | https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB- |
| Accessed? | yes |
| How | `git clone --depth 1` |
| Downloaded | `Data/indian-nutrient-databank-indb/`: all 9 xlsx files, `INDB.do` and the README (2.4 MB) |

The raw ingredient composition tables (ICMR-NIN IFCT 2017 and 2004) are **not** in the repository and must be
requested from NIN, see [[Indian Food Composition Tables (IFCT 2017)]]. Without them `INDB.do` cannot rebuild
the table, but `INDB.xlsx` already holds the computed values.

## Tables & columns
### `INDB.xlsx` › `Nutrient Data` (1,014 rows × 82 columns)
One row per recipe. 41 nutrients per 100 g, then the same 41 per serving (`unit_serving_*`).
| column | type | meaning | example |
|---|---|---|---|
| `food_code` | str | recipe code; prefix = source: `ASC` Art & Science of Cooking, `BFP` Basic Food Preparation, `OSR` open-source (web) recipe | ASC001 |
| `food_name` | str | English name + local/Hindi name in brackets | Hot tea (Garam Chai) |
| `primarysource` | str | asc_manual 490 · bfp_manual 376 · open_source_recipes 148 | asc_manual |
| `energy_kj`, `energy_kcal` | float | energy per 100 g | 16.14 |
| `carb_g`, `protein_g`, `fat_g`, `freesugar_g`, `fibre_g` | float | macronutrients per 100 g | 2.58 |
| `sfa_mg`, `mufa_mg`, `pufa_mg`, `cholesterol_mg` | float | fatty acids, cholesterol | 321.5 |
| `calcium_mg` … `zinc_mg` (12 minerals) | float | Ca, P, Mg, Na, K, Fe, Cu, Se, Cr, Mn, Mo, Zn | |
| `vita_ug` … `carotenoids_ug` (18 vitamins) | float | A, E, D2, D3, K1, K2, folate, B1–B7, B9, C, carotenoids | |
| `servings_unit` | str | household serving unit | tea cup |
| `unit_serving_<nutrient>` (41 cols) | float | nutrient per serving | |

### `recipes.xlsx` (10,271 rows × 13 columns): recipe → ingredient with amount
| column | type | meaning | example |
|---|---|---|---|
| `recipe_code_org`, `recipe_code` | str | recipe number in the cookbook; INDB code | 5.1, ASC001 |
| `recipe_name_org`, `recipe_name` | str | original and standardised name | Hot Tea → Hot tea (Garam Chai) |
| `ingredient_name_org` | str | ingredient as written | Washed moong dal |
| `amount_org`, `unit_org` | str | amount as written | 2, tsp (to taste) |
| `food_code_org`, `food_name_org` | str | matched source-FCT code (IFCT, `UK-…`, `US-…`) | UK-17-063, Sugar, white |
| `food_code`, `food_name` | str | INDB ingredient code and name (332 distinct) | B010, Green gram, dal (Vigna radiata) |
| `amount`, `unit` | float, str | cleaned amount; units g 4,759 · tsp 3,660 · tbsp 844 · ml 473 · C (cup) 275 · sprig 247 | 10.0 g |

### `recipes_names.xlsx` (1,014) · `recipes_servingsize.xlsx` (1,014 × 13) · `recipe_links.xlsx` (150)
Recipe names with `primarysource`. Serving data: `no_of_servings`, `size_of_servings`, `servings_unit` (for
example 2 × 1 tea cup), plus remarks. `recipe_links` gives the URL of each `OSR` recipe (`Food Names`,
`Food Code`, `Link`).

### Ingredient composition supplements: `UK_fct.xlsx` (144 × 44) · `US_fct.xlsx` (54 × 44)
Ingredients missing from IFCT, taken from UK CoFID 2021 and USDA FoodData Central. Columns: `retention_factor`,
`food_code_org` (`UK-13-146`, `US-806341`), `food_code`, `food_name`, `primarysource`, then the same 39
nutrient columns per 100 g. `Tr` = trace, `N` = present but unknown.

### `USDA_nrf.xlsx` (270 × 28) · `Units.xlsx` (345 × 5)
USDA Nutrient Retention Factors Release 6: `retention_factor` code, `Retention Description` (e.g.
CHEESE,BAKED) and `usda_rf_<nutrient>` % retained. `Units` holds household-measure conversions (1 cup = 240 ml
= 240 g…).

Sample: `Data/indian-nutrient-databank-indb/sample.csv` · full profile: `Data/indian-nutrient-databank-indb/schema.md`

## Countries & cultures covered
- **[[India]]**: all 1,014 recipes. There is **no state, region or cuisine column**, so no per-state counts are
  possible.
- Regional identity shows only in some names (e.g. "Kashmiri masala", idli/dosa-type South Indian dishes,
  "Rice flakes (Chiwda/Aval)"). The cookbooks are Delhi home-science manuals, so the set leans North Indian and
  pan-Indian.
- The set also includes Western and continental dishes as eaten in India (e.g. "Charlotte rousse", "Beans and
  macaroni", omelettes, cakes).

## Ingredients, amounts, cooking method
- **Ingredients + amounts: yes.** Example: *Vegetable khichdi/khichri* = parboiled rice 20 g, washed
  moong dal 10 g, spinach 25 g, carrot 25 g, curds 50 g, salt 0.25 tsp, unsalted butter 5 g. Result per 100 g:
  143 kcal, 5.6 g protein, 19.6 g carbohydrate, 4.5 g fat, 2.5 g fibre, 1.09 mg iron.
- **Cooking method: no** steps or tags in the tables. Cooking only enters through the USDA retention-factor
  code attached to each ingredient (e.g. boiled, baked).
- **Nutrition: yes**, 41 nutrients per 100 g and per serving.

## Linking to other datasets
- `food_code` (IFCT 2017/2004 codes such as `A014`, `B010`) → [[Indian Food Composition Tables (IFCT 2017)]].
- `US-<fdc_id>` codes → [[USDA FoodData Central]]. `UK-…` codes → UK CoFID.
- [[IndicRecipeNutri]] reuses INDB's 198 US/UK composition rows in its nutrition layer (per its README).
- Ingredient botanical names in `food_name` (e.g. *Vigna radiata*, *Spinacia oleracea*) → [[IMPPAT]] and
  [[FooDB]] by scientific name, which leads on to compounds.

## Versions
One version only. The repository was last updated on 2025-04-08. The paper (June 2024) describes the same
1,014 recipes.

## Caveats
- Small: 1,014 recipes, from textbook "standard recipes" rather than household-observed ones.
- No regional labels.
- Counts differ slightly between sources: the README says 378 BFP recipes and 150 web links, the data has 376
  BFP recipes and 148 `open_source_recipes`.
- The paper reports that only 42.6% of ingredients got a retention factor, so some cooking losses are ignored.
- There is no licence file in the repository; the IFCT source data is restricted.
