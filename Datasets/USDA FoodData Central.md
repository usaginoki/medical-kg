---
title: "USDA FoodData Central"
slug: usda-fooddata-central
kind: [ingredient]
version: "Foundation Foods 2026-04-30 (+ SR Legacy 2018-04, frozen)"
previous_versions: "Foundation Foods releases 2019-04-02 … 2025-12-18 (twice yearly); SR Legacy replaces SR28 (2016)"
papers: ["[[Fukagawa2022 - USDA FoodData Central]]"]
url: "https://fdc.nal.usda.gov/"
license: "CC0 1.0 (public domain)"
availability: open-download
access_link: "https://fdc.nal.usda.gov/download-datasets"
accessed: true
access_method: [website-download, api]
access_date: 2026-09-30
access_notes: "Direct curl of FoodData_Central_foundation_food_csv_2026-04-30.zip (3.8 MB) and FoodData_Central_sr_legacy_food_csv_2018-04.zip (6.1 MB), unzipped (70 MB). Branded (~450k products), FNDDS/Survey (2024-10-31) and Experimental not downloaded, as instructed. A free REST API (api.data.gov key) also exists but was not needed."
countries: ["[[United States]]"]
regions: ["[[North America]]"]
n_records: "Foundation: 469 foundation foods (+ 87,521 sample/acquisition/sub-sample records), 170,469 nutrient values; SR Legacy: 7,793 foods, 644,125 nutrient values"
size: "10 MB zipped / 70 MB unzipped (these two data types)"
formats: [csv, xlsx]
has_ingredients: false
has_amounts: no
has_cooking_method: no
has_nutrition: true
body_effect: linkable
body_effect_how: "No health fields. Nutrients (474–477 components incl. vitamins, minerals, carotenoids, choline, ergothioneine, some SR flavan-3-ols) have well-known physiological roles/DRIs; foods carry FoodOn and NCBI Taxon ids (Foundation food_attribute) that join to FooDB / CTD-style compound→effect resources."
join_keys: [USDA FDC id, NDB number, FoodOn id, NCBI taxon, INFOODS nutrient number]
topics: [cultural-food-health]
questions: [Q2]
relevance: core
found_by: [search/ingredients]
tags:
  - type/dataset
  - kind/ingredient
  - q/2
  - access/accessed
  - access/open
  - region/americas
---
# USDA FoodData Central

> [!abstract] TL;DR
> USDA's integrated food-composition system (CC0). **Foundation Foods** (469 minimally processed foods with
> sample-level analytical data, lab methods, FoodOn/NCBI-taxon metadata; updated twice a year, latest 2026-04-30) and
> **SR Legacy** (7,793 foods × up to 149 nutrients, the frozen 2018 successor of SR28) are the reference nutrient
> tables that most national food-composition tables (FCTs) crosswalk to. It covers the US only, but it is the practical hub
> for turning ingredient names from cultural recipe datasets into nutrient profiles. It has a few culture-tagged
> items (SR Legacy: 15 "Restaurant, Chinese", 15 "Restaurant, Latino", 6 "Mexican", 165 American Indian/Alaska Native foods)
> and common Middle-East/Asian staples (hummus, tahini, falafel, naan, chapati, kimchi, miso, medjool dates).

## Access
| | |
|---|---|
| Availability | open-download (CSV/JSON zips) + open REST API (free api.data.gov key) |
| Link | https://fdc.nal.usda.gov/download-datasets |
| Accessed? | yes |
| How | `curl -L -O https://fdc.nal.usda.gov/fdc-datasets/FoodData_Central_foundation_food_csv_2026-04-30.zip` and `…sr_legacy_food_csv_2018-04.zip`, unzip |
| Downloaded | `Data/usda-fooddata-central/FoodData_Central_foundation_food_csv_2026-04-30/` (26 CSV + field-description xlsx) and `…/FoodData_Central_sr_legacy_food_csv_2018-04/` (19 CSV + xlsx) |

## Tables & columns
Both data types share one relational schema (field descriptions ship as `Download API Field Descriptions.xlsx`).
Key tables:

### `food.csv` (Foundation 87,990 rows · SR Legacy 7,793)
| column | type | meaning | example |
|---|---|---|---|
| `fdc_id` | int | FoodData Central id, unique per food record | `323505` |
| `data_type` | str | `foundation_food` (469), `sample_food` (4,079), `market_acquisition` (7,577), `sub_sample_food` (75,055), `agricultural_acquisition` (810); `sr_legacy_food` in SR | `foundation_food` |
| `description` | str | food name | `Kale, raw` |
| `food_category_id` | int | → `food_category.csv` (28 SR-style groups, e.g. 2 = Spices and Herbs, 24 = American Indian/Alaska Native Foods, 25 = Restaurant Foods) | `11` |
| `publication_date` | date | release date of the record | `2019-04-01` |

### `food_nutrient.csv` (Foundation 170,469 · SR Legacy 644,125)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | row id | `1283674` |
| `fdc_id` | int | food | `172231` |
| `nutrient_id` | int | → `nutrient.csv` | `1003` |
| `amount` | float | amount per 100 g edible portion, unit in `nutrient.unit_name` | `3.25` |
| `data_points` | int | number of analyses behind the value | `3` |
| `derivation_id` | int | how derived (analysed, calculated, imputed…) → `food_nutrient_derivation.csv` (SR) | `46` |
| `min`, `max`, `median` | float | range across samples (Foundation; SR partly) | `4460 / 8560` |
| `footnote` | str | free-text note | `Samples were obtained from 12 retail st…` |
| `min_year_acquired` | int | earliest sample year | |

Of the Foundation rows, 21,459 belong to the 469 `foundation_food` records (235 distinct nutrients); the rest are
per-sample (`sub_sample_food` 134,436) and per-farm (`agricultural_acquisition` 14,574) analyses.

### `nutrient.csv` (Foundation 477 · SR Legacy 474)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | nutrient id | `1121` |
| `name` | str | nutrient/component | `Lutein` |
| `unit_name` | str | `G`, `MG`, `UG`, `KCAL`, `IU` | `UG` |
| `nutrient_nbr` | float | legacy SR / INFOODS-style number | `338.1` |
| `rank` | float | display order | `7562` |

Includes vitamins, minerals, amino acids, fatty-acid profiles, sugars, carotenoids, choline fractions, beta-glucans,
ergothioneine (2057) and flavan-3-ols (`Catechin`, `Epicatechin`, `Epigallocatechin-3-gallate`, `Quercetin`…; ids 1363–1398,
not populated for Foundation foods in this release).

### Other tables
- `food_portion.csv` (Foundation 10,951 · SR 14,449): household measures → `gram_weight` (e.g. ground turmeric: `modifier` "tbsp" = 9.4 g, "tsp" = 3.0 g).
- `food_attribute.csv` (Foundation 9,380 · SR 1,074): name/value metadata: `FoodOn Ontology ID For FDC Item`
  (1,010), `NCBI Taxon` (1,010), `Genotype`, `Organic`, `Growing Region`, `Country of Origin` (7, all "USA").
- `market_acquisition.csv` (7,577): store, city, `store_state` (MD 1,419, VA 878, CA 624, TX 317…), UPC, dates.
- `agricultural_samples.csv` (810), `acquisition_samples.csv`, `sample_food.csv`, `sub_sample_food.csv`, `sub_sample_result.csv` (134,267): sample provenance chain.
- `lab_method.csv` (305), `lab_method_code.csv`, `lab_method_nutrient.csv`: analytical methods (e.g. `AOAC 968.06 + 992.15`, Combustion).
- `food_component.csv` (3,066): refuse (bone, fat) as % weight. `input_food.csv` (6,038): which sample foods feed a Foundation food.
- Conversion factors: `food_calorie_conversion_factor`, `food_protein_conversion_factor`, `food_nutrient_conversion_factor`.
- SR only: `sr_legacy_food.csv` (fdc_id ↔ `NDB_number`), `retention_factor.csv` (270 cooking retention factors), `food_nutrient_source.csv`, `food_nutrient_derivation.csv`.

Sample: `Data/usda-fooddata-central/sample.csv` · full profile: `Data/usda-fooddata-central/schema.md`

## Countries & cultures covered
- [[United States]]: all records (Foundation samples bought in US stores/farms; 7 `Country of Origin` attributes = "USA").
- Culture-labelled items inside US data (SR Legacy descriptions): Restaurant, Chinese 15 · Restaurant, Latino 15 ·
  Restaurant, family style 13 · Restaurant, Mexican 6 · Restaurant, Italian 5 · American Indian/Alaska Native Foods
  category 165 (e.g. "Seal, bearded (Oogruk), meat, raw (Alaska Native)"). Foundation: Restaurant, Chinese 3 · Latino 2.
- Ethnic staples present as plain foods: hummus (2), tahini (4), falafel, naan (2), chapati/roti (2), couscous (2),
  kimchi, miso, tofu (34), medjool/deglet noor dates. These are useful anchors for Middle East / South & East Asia recipes.

## Inferring effects on the body
- **No health/effect fields.** Effect inference is *linkable*: nutrient amounts per 100 g → dietary reference intakes
  (DRIs), or FoodOn/NCBI Taxon ids → [[FooDB]] (compound → health effect) and [[Phenol-Explorer]] (polyphenols).
- Example row: `Spices, turmeric, ground` (SR Legacy, fdc_id 172231, category 2 Spices and Herbs): water 12.85 g,
  total fat 3.25 g, sugars 3.21 g, vitamin K 13.4 µg per 100 g. Curcuminoids are **not** in FDC. For them go to
  Phenol-Explorer (curcumin 2,213.57 mg/100 g in "Turmeric, dried") or FooDB (turmeric FOOD00068 → curcumin → anti-inflammatory).
- Evidence type: analytical measurements (Foundation: per-sample lab data with methods; SR: compiled/analysed/imputed per `derivation_id`).

## Linking to other datasets
- `fdc_id` / `NDB_number`: the standard key used by FNDDS, many national FCT crosswalks, and recipe-nutrition work.
- `FoodOn` and `NCBI Taxon` (Foundation `food_attribute`): join to [[FooDB]] (`ncbi_taxonomy_id` in its Food table) and ontology-based KGs.
- Free-text `description` ↔ ingredient names in [[Food.com Recipes and Interactions]] (fuzzy matching).

## Versions
- Foundation Foods is released twice a year (2019-04-02 → … 2025-04-24, 2025-12-18, **2026-04-30**); each release adds
  foods and nutrients and revises values. We took the latest.
- SR Legacy (2018-04) is final (it replaced SR28 and is no longer updated).
- Other FDC data types not downloaded: Branded Foods (2026-04-30), FNDDS/Survey Foods (2024-10-31), Experimental Foods.

## Caveats
- US food supply only; Foundation covers just 469 foods and needs the sample tables to interpret.
- Flavonoid/phytochemical columns are sparse (the USDA flavonoid/isoflavone databases are separate products).
- `food.csv` in Foundation mixes aggregate foods with tens of thousands of sample records: filter on `data_type`.
