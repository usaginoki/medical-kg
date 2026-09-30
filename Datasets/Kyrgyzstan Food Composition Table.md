---
title: "Kyrgyzstan Food Composition Table"
slug: kyrgyzstan-food-composition-table
kind: [ingredient, food]
version: "1st edition (2022), figshare item 20237163 v2 (DOI 10.6084/m9.figshare.20237163.v2); file 'Kyrgyzstan FCT 06072022.docx.pdf'"
previous_versions: "figshare v1 (same PDF, same md5 385fd60b…). No earlier national Kyrgyz FCT existed."
papers: ["[[Smanalieva2025 - Development of Kyrgyz food composition tables]]"]
url: "https://doi.org/10.6084/m9.figshare.20237163.v2"
license: "CC BY 4.0 (figshare). The PDF itself says free copying for public-health research/service, no commercial use without permission."
availability: open-download
access_link: "https://figshare.com/articles/book/Kyrgyzstan_s_Food_Composition_Table/20237163"
accessed: true
access_method: [figshare]
access_date: 2026-09-30
access_notes: "The figshare API lists no files for v2, but v1 lists file 36169554. figshare.com/ndownloader returned an AWS-WAF 202 challenge with a browser UA; ndownloader.figshare.com/files/36169554 with a curl UA returned the 3.3 MB, 85-page PDF (md5 matches). We extracted all composition tables (pp. 55–72), the 11 recipes (pp. 15–26) and the Annex 1 food index to CSV. Not converted: the amino-acid (3 foods) and fatty-acid (4 foods) tables on pp. 72–73."
countries: ["[[Kyrgyzstan]]"]
regions: ["[[Central Asia]]"]
n_records: "41 raw foods (40 in the proximate table) + 11 cooked national dishes; 162 recipe ingredient lines"
size: "3.3 MB PDF; ~40 KB CSV"
formats: [pdf, csv]
has_ingredients: true
has_amounts: "yes"
has_cooking_method: steps
has_nutrition: true
body_effect: linkable
body_effect_how: "Per-100 g nutrients (INFOODS tagnames ENERC, PROT, FAT, CHO, FIBT, CA, FE, NA, VITA, CARTB, VITC, FOL…) plus scientific names (Malus sieversii, Hippophae rhamnoides, Berberis oblonga, Rosa canina…) that link to FooDB/NCBI taxonomy for bioactive compounds. No health fields."
join_keys: [Kyrgyz food code (group_code + 5-digit code), INFOODS tagname, scientific name, food name (Kyrgyz/English)]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/regions, search/ingredients]
tags:
  - type/dataset
  - kind/ingredient
  - kind/food
  - q/1
  - q/2
  - access/accessed
  - access/open
  - region/central-asia
---
# Kyrgyzstan Food Composition Table

> [!abstract] TL;DR
> This is Kyrgyzstan's first national food composition table (2022), compiled by Kyrgyz State Technical University, Kyrgyz-Turkish Manas University and the Slovak National Agricultural and Food Centre with EuroFIR-standard documentation. It covers:
> - **41 raw foods**, strongly local: koumiss, dried koumiss, mare/yak/hainak milk, yak meat and fat, horse fat, chuchuk horse sausage, bozo and bozodoy drinks, Ozgon rice, badyrak, and wild fruits such as *Malus sieversii* apple, sea buckthorn, barberry, cherry plum, hawthorn and dog rose.
> - **11 traditional cooked dishes** with standardized recipes and calculated composition: beshbarmak, dymdama, plov with barberry, 3 manty variants, oromo, lagman, shorpo, mastava, soup with kidney beans.
>
> Labels are bilingual Kyrgyz/English, with scientific names. It is the **only national FCT for Central Asia** in the vault, and it pairs with the [[Central Asian Digital Visual Food Atlas]] portion weights.

## Access
| | |
|---|---|
| Availability | open-download (figshare, CC BY 4.0) |
| Link | https://figshare.com/articles/book/Kyrgyzstan_s_Food_Composition_Table/20237163 |
| Accessed? | true |
| How | `curl -L -A curl/8.0 https://ndownloader.figshare.com/files/36169554`. Tables were parsed with pdfplumber, assigning each value to a column by x-position; dense dish tables were parsed by token order. |
| Downloaded | `Data/kyrgyzstan-food-composition-table/Kyrgyzstan_FCT_06072022.pdf` + `extracted/` (9 CSVs) |

## Tables & columns
Common id columns in every table:
- `page`: PDF page
- `food_group_code`: EuroFIR-style group, e.g. `05` fruits, `10` milk, `13` cooked dishes
- `food_code`: 5-digit code, e.g. `00011`
- `name_kyrgyz`, `name_english`, e.g. `Кымыз` / `Koumiss`

Nutrient columns use INFOODS tagnames, all per 100 g edible portion. Values in parentheses are as printed, e.g. `(3.0)`, probably estimated.

### `extracted/raw_foods_proximates.csv` (40 rows)
| column | type | meaning | example (Koumiss) |
|---|---|---|---|
| `ENERC` / `ENERC_2` | num | energy kJ / kcal | `255` / `61` |
| `WATER` | g | water | `88.5` |
| `PROT` | g | protein | `2.78` |
| `FAT` | g | fat | `2.42` |
| `CHOT` | g | carbohydrate, total (by difference) | `4.42` |
| `CHO` | g | carbohydrate, available | `4.42` |

Pistachio (00019) is missing from the printed proximate table.

### `extracted/raw_foods_sugars_fibre.csv` (41 rows)
- Columns: `SUGAR` total sugars, `SUGRD` reducing sugars, `SUCS` sucrose, `LACS` lactose, `FIBT` fibre, `PECT` pectin, `ASH`, `ALC` alcohol, `OA` organic acids (g).
- Example: Honey SUGAR 78.56 · SUGRD 75.40 · SUCS 3.16.

### `extracted/raw_foods_minerals.csv` (41 rows)
- Columns: `CA`, `FE`, `MG`, `P`, `K`, `ZN`, `CU`, `NA` (mg).
- Example: Mare milk CA 87 · FE 0.1 · MG 8 · P 54 · K 63 · ZN 0.15 · CU 0.03 · NA 0.05.
- Many rows are blank: values are only given where literature data existed.

### `extracted/raw_foods_vitamins.csv` (41 rows)
- Columns: `VITA` (mcg), `CARTB` β-carotene (mcg), `CAROT` carotenoids (mcg), `VITE`, `THIA`, `RIBF`, `VITC` (mg).
- Examples: Sea buckthorn CARTB 14,200 · VITC 266. Barberry VITC 244.

### `extracted/dishes_proximates.csv` (11 rows, food group 13)
- Columns: `ENERC` kJ, `ENERC_2` kcal, `WATER`, `PROT`, `FAT`, `CHOT`, `CHO`, `GLUS` glucose, `FRU` fructose, `SUCS`, `FIBT` (g).
- Values are **calculated** from recipes with retention and yield factors.
- Example: Beshbarmak 519 kJ / 124 kcal · 55.0 water · 9.22 protein · 5.24 fat.

### `extracted/dishes_minerals.csv` (11 rows)
- Columns: `CA`, `FE`, `MG`, `P`, `K`, `ZN`, `CU`, `NA` (mg), `ASH`, `OA` (g).
- Example: Oromo NA 563 mg. Beshbarmak NA 326 mg, ZN 1.55 mg.

### `extracted/dishes_vitamins.csv` (11 rows)
- Columns: `VITA`, `CAROT`, `FOL` (mcg), `VITE`, `THIA`, `RIBF`, `VITC` (mg).
- Example: Plov with barberry VITA 480, CAROT 2,593.

### `extracted/dish_recipes_ingredients.csv` (162 rows)
| column | type | meaning | example |
|---|---|---|---|
| `recipe_no` / `food_code` | int / str | recipe 1–11 ↔ dish code 13001–13011 | `1` / `13001` |
| `dish_name` | str | dish | `Beshbarmak` |
| `ingredient` | str | ingredient, or an intermediate mass ("Meat cooked", "Mass of dough", "TOTAL COOKED WEIGHT") | `Lamb, horse or beef meat` |
| `raw_weight_g` | num | raw ingredient weight, g | `218` |
| `edible_weight_g` | num | edible-part weight, g | `156` |

### `extracted/annex1_food_index.csv` (41 rows)
- Columns: `code` (`05_00008`), `name_english`, `name_kyrgyz`, `scientific_name` (`Malus sieversii`), `biblio_ids` (`KG00005;KG00032` → Annex 2 bibliography).

Sample: `Data/kyrgyzstan-food-composition-table/sample.csv` · full profile: `Data/kyrgyzstan-food-composition-table/schema.md`

## Countries & cultures covered
- **[[Kyrgyzstan]]**: all 52 foods (41 raw + 11 dishes).
- Raw foods by group:
  - 21 fruits (mostly wild or local varieties)
  - 6 milk and dairy: koumiss, dried koumiss, mare, cow, yak and hainak milk
  - 3 fats: beef, horse, yak
  - 2 each of cereals (badyrak, Ozgon rice), vegetables, nuts (walnut, pistachio), meat (chuchuk, yak calf) and beverages (bozo, bozodoy)
  - honey
- The book's chapter on traditional Kyrgyz cuisine notes that the cuisine fuses Uzbek, Uyghur, Russian and Ukrainian influences. The dishes (manty, lagman, plov, shorpo, mastava) are shared across Central Asia, so they are usable for [[Kazakhstan]] and [[Uzbekistan]] with care. The data itself is labelled Kyrgyz only.

## Ingredients, amounts, cooking method
- **Ingredients + amounts:** yes, per portion in grams, raw and edible.
  - *Beshbarmak*: lamb/horse/beef 218 g raw (156 g edible → 100 g cooked meat), egg 8 g, wheat flour type 405 62 g, water 15 g, salt 2 g, onion 36 g, black pepper 0.5 g, bouillon 150 g. Total cooked weight 430 g.
  - *Plov with barberry*: meat 150 g, oil 30 g, Uzgen rice 80 g, carrots 100 g, onion 36 g, barberry 2 g.
- **Cooking method:** a short prose method per recipe, e.g. Beshbarmak: boiled lamb cut into 0.5 × 5–7 cm slices, fresh noodles boiled in broth, onion rings on top, broth served separately (source: Ibraimova 1991).
- **Nutrition:** per 100 g. Raw foods are mostly analysed values from the literature. Dishes are calculated.

## Inferring effects on the body
- **Direct:** none.
- **Linkable:**
  - Nutrients (INFOODS tagnames) link to nutrient→outcome guidance, e.g. sodium in oromo (563 mg/100 g) and manty.
  - Scientific names reach compound databases: *Hippophae rhamnoides* (sea buckthorn: carotenoids, β-carotene 14,200 µg/100 g here) and *Berberis* (barberry, vitamin C 244 mg/100 g) → [[FooDB]] / [[Phenol-Explorer]] polyphenols. Koumiss and mare milk are traditional-medicine foods in the region.
- **Evidence type:** literature-compiled analytical data (EuroFIR documentation, BiblioIDs); dish values are recipe-calculated.

## Linking to other datasets
- `scientific_name` → [[FooDB]], [[Phenol-Explorer]], [[USDA FoodData Central]] (e.g. *Juglans regia*, *Prunus armeniaca*).
- Dish names ↔ [[Central Asian Food Dataset]] image classes (`beshbarmak-*`, `manty`, `lagman-*`, `plov`, `orama`, `shorpa`, `kymyz-kymyran`) and ↔ [[Central Asian Digital Visual Food Atlas]] portion weights (Beshbarmak 194/365/541 g; Lagman; Naryn). Portion × per-100 g gives nutrients per serving.
- INFOODS tagnames are shared with [[Korean Food Composition Table]] and [[Standard Tables of Food Composition in Japan]].

## Versions
- figshare v1 and v2 (2022-07-06) carry the same PDF, "first edition".
- The 2025 JFCA paper ([[Smanalieva2025 - Development of Kyrgyz food composition tables]]) describes this same first edition (41 raw + 11 cooked foods) and its limitations. No second edition was found.

## Caveats
- The data is extracted from a PDF.
  - The sparse raw-food tables (sugars, minerals, vitamins) were mapped to columns by x-position; spot-checked rows are correct, but verify single values against the PDF page.
  - The dense dish tables were checked row by row.
- Small coverage: 52 foods, and micronutrients are only present where literature data existed.
- Dish values are calculated, not analysed. Recipe amounts are per single portion (about 350–450 g cooked).
- The source has typos: "pumkin", "Kidey beans", and a total cooked weight of 45 g printed for dymdama.
