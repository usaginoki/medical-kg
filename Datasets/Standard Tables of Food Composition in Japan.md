---
title: "Standard Tables of Food Composition in Japan"
slug: standard-tables-of-food-composition-in-japan
kind: [ingredient]
version: "8th Revised Edition, 2023 Supplement (日本食品標準成分表（八訂）増補2023年), data updated 2026-03-27 (errata)"
previous_versions: "2020 (8th rev.) · 2015 (7th rev.) and its 2016–2019 supplements · earlier editions since 1950"
papers: []
url: "https://www.mext.go.jp/a_menu/syokuhinseibun/mext_00001.html"
license: "Free to use with citation: 「日本食品標準成分表（八訂）増補2023年から引用」 (MEXT)"
availability: open-download
access_link: "https://www.mext.go.jp/a_menu/syokuhinseibun/mext_00001.html"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "All 12 Excel files downloaded directly (curl, browser UA): main table, amino-acid tables 1–4, fatty-acid tables 1–3, carbohydrate table plus 2 annexes, and the 2026-03-27 errata. The Japanese Excel files have multi-row merged headers. We converted the main, amino-acid table 1, fatty-acid table 1 and carbohydrate main tables to tidy CSVs keyed by INFOODS tagnames. English food names do not exist for the 8th edition. We joined them by food number from the MEXT English 7th edition (2015) table; 2,184/2,538 foods matched."
countries: ["[[Japan]]"]
regions: ["[[East Asia]]"]
n_records: "2,538 foods (main table); 1,999 (amino acids); 1,967 (fatty acids); 1,101 (carbohydrates)"
size: "8.8 MB Excel (zipped) + 2.3 MB tidy CSV"
formats: [xlsx, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: true
body_effect: linkable
body_effect_how: "Per-100 g nutrient values (energy, macros, 15 minerals, vitamins, 20 amino acids, ~50 fatty acids incl. EPA/DHA, sugars, sugar alcohols) keyed by INFOODS tagnames; effects on the body come by linking nutrients to dietary reference intakes / nutrient–health evidence, not from this table. Ingredient names → FooDB/USDA for non-nutrient compounds."
join_keys: [MEXT food number (5-digit), INFOODS tagname, food name (JP), food name (EN, 2015)]
topics: [cultural-food-health]
questions: [Q2]
relevance: core
found_by: [search/ingredients, search/regions]
tags:
  - type/dataset
  - kind/ingredient
  - q/2
  - access/accessed
  - access/open
---
# Standard Tables of Food Composition in Japan

> [!abstract] TL;DR
> Japan's official national food composition table, published by **MEXT**. The 8th revised edition's 2023 supplement is the latest; its data was corrected on 2026-03-27. It gives per-100 g edible-portion nutrient values for **2,538 foods in 18 groups**, covering raw ingredients, cooked forms (boiled, grilled, fried) and Japanese-specific items such as natto, miso, pickles, seaweeds, fish and wagashi. Companion tables cover amino acids, fatty acids and carbohydrates. It is the reference for turning Japanese ingredients and recipes into nutrients (Q2).

## Access
| | |
|---|---|
| Availability | open-download (Excel + PDF) |
| Link | <https://www.mext.go.jp/a_menu/syokuhinseibun/mext_00001.html> · English (7th ed. 2015 only): <https://www.mext.go.jp/en/policy/science_technology/policy/title01/detail01/1374030.htm> |
| Accessed? | true |
| How | `curl -A <browser UA>` on each `/content/20260327-mxt_kagsei-mext-000029402_NN.xlsx`, then conversion to CSV (script in the session scratchpad) |
| Downloaded | `Data/standard-tables-of-food-composition-in-japan/`: 4 tidy CSVs; `raw_mext_excel_files.zip` holds all 12 original xlsx plus `english_7th_ed_2015_main_table.xlsx` |

Raw files in the zip:
- `main_composition_table.xlsx` (本表). Sheet `表全体` has all foods; the other 18 sheets hold one food group each.
- Amino-acid tables (アミノ酸成分表編): `amino_acid_table1_per100g_edible`, `…table2_per_g_nitrogen`, `…table3_per_g_protein_by_aa`, `…table4_per_g_protein`.
- Fatty-acid tables (脂肪酸成分表編): `fatty_acid_table1_per100g_edible`, `…table2_per100g_total_fa`, `…table3_per_g_lipid`.
- Carbohydrate tables (炭水化物成分表編): `carbohydrate_main_table` (available carbohydrates and sugar alcohols), `…annex1_dietary_fiber`, `…annex2_organic_acids`.
- `errata_2026-03-27.xlsx` (正誤表).

> [!note] English names
> MEXT has **not** published an English edition of the 8th edition (2020/2023); the latest English tables are for the 7th edition (2015). We added `food_name_en_2015` by joining on the 5-digit food number, which is stable across editions. 354 foods added in 2020/2023 have no English name, e.g. 01167 キヌア (quinoa) and 01174 角形食パン 焼き.

## Tables & columns
Value conventions from the MEXT notes:
- `-` = not analysed.
- `0` = below 1/10 of the minimum reportable value.
- `Tr` = trace.
- `(0)` = estimated zero.
- Numbers in `( )` are estimates, e.g. computed from similar foods or borrowed from the US table.
- `*` in the `*_energy_calc_flag` columns marks which available-carbohydrate value was used for the energy calculation.

Values are kept as strings to preserve these markers.

### `main_composition_table.csv` (2,538 rows × 62 columns)
Translated headers:

| column | type | meaning (JP header → EN) | unit | example (01001 amaranth) |
|---|---|---|---|---|
| `food_group` | str | 食品群, food group 01–18 (see below) | | 01 |
| `food_number` | str | 食品番号, food number (stable id) | | 01001 |
| `index_number` | str | 索引番号, index number | | 0001 |
| `food_name_ja` | str | 食品名, food name | | アマランサス 玄穀 |
| `food_name_en_2015` | str | English name from the 2015 edition (our join) | | Amaranth, whole grain, raw |
| `REFUSE` | str | 廃棄率, refuse (inedible share) | % | 0 |
| `ENERC` / `ENERC_KCAL` | str | エネルギー, energy | kJ / kcal | 1452 / 343 |
| `WATER` | str | 水分, water | g | 13.5 |
| `PROTCAA` | str | アミノ酸組成によるたんぱく質, protein as the sum of amino-acid residues | g | (11.3) |
| `PROT-` | str | たんぱく質, protein (N × factor) | g | 12.7 |
| `FATNLEA` | str | 脂肪酸のトリアシルグリセロール当量, fat as triacylglycerol equivalents | g | 5.0 |
| `CHOLE` | str | コレステロール, cholesterol | mg | (0) |
| `FAT-` | str | 脂質, lipid (total) | g | 6.0 |
| `CHOAVLM` | str | 利用可能炭水化物（単糖当量）, available carbohydrate, monosaccharide equivalents | g | 63.5 |
| `CHOAVL` | str | 利用可能炭水化物（質量計）, available carbohydrate by mass | g | 57.8 |
| `CHOAVLDF-` | str | 差引き法による利用可能炭水化物, available carbohydrate by difference | g | 59.9 |
| `FIB-` | str | 食物繊維総量, total dietary fibre | g | 7.4 |
| `POLYL` | str | 糖アルコール, sugar alcohols | g | - |
| `CHOCDF-` | str | 炭水化物, carbohydrate (total, by difference) | g | 64.9 |
| `OA` | str | 有機酸, organic acids | g | - |
| `ASH` | str | 灰分, ash | g | 2.9 |
| `NA`, `K`, `CA`, `MG`, `P`, `FE`, `ZN`, `CU`, `MN` | str | 無機質, minerals: sodium, potassium, calcium, magnesium, phosphorus, iron, zinc, copper, manganese | mg | 1, 600, 160, 270, 540, 9.4, 5.8, 0.92, 6.14 |
| `ID`, `SE`, `CR`, `MO` | str | iodine, selenium, chromium, molybdenum | µg | 1, 13, 7, 59 |
| `RETOL`, `CARTA`, `CARTB`, `CRYPXB`, `CARTBEQ`, `VITA_RAE` | str | vitamin A: retinol, α-carotene, β-carotene, β-cryptoxanthin, β-carotene equivalents, retinol activity equivalents | µg | (0), 0, 2, 0, 2, Tr |
| `VITD` | str | vitamin D | µg | (0) |
| `TOCPHA`–`TOCPHD` | str | vitamin E: α-, β-, γ-, δ-tocopherol | mg | 1.3, 2.3, 0.2, 0.7 |
| `VITK` | str | vitamin K | µg | (0) |
| `THIA`, `RIBF`, `NIA`, `NE`, `VITB6A` | str | vitamin B1, vitamin B2, niacin, niacin equivalents, vitamin B6 | mg | 0.04, 0.14, 1.0, (3.8), 0.58 |
| `VITB12`, `FOL` | str | vitamin B12, folate | µg | (0), 130 |
| `PANTAC` | str | pantothenic acid | mg | 1.69 |
| `BIOT` | str | biotin | µg | 16.0 |
| `VITC` | str | vitamin C | mg | (0) |
| `ALC` | str | アルコール, alcohol | g | - |
| `NACL_EQ` | str | 食塩相当量, salt equivalent | g | 0 |
| `CHOAVLM_energy_calc_flag`, `CHOAVLDF-_energy_calc_flag` | str | `*` = value used for energy (inferred from the MEXT notes) | | * |
| `remarks_ja` | str | 備考, remarks: synonyms (別名), refuse parts (廃棄部位), yields, recipe ratios, nitrate, etc. | | 別名： オート、オーツ |

**Food groups** (`food_group`, rows): 01 cereals 208 · 02 potatoes & starches 70 · 03 sugars & sweeteners 31 · 04 pulses 113 · 05 nuts & seeds 46 · 06 vegetables 413 · 07 fruits 185 · 08 mushrooms 56 · 09 algae 58 · 10 fish & shellfish 471 · 11 meat 317 · 12 eggs 23 · 13 milk 59 · 14 fats & oils 34 · 15 confectionery 187 · 16 beverages 64 · 17 seasonings & spices 148 · 18 prepared foods 55.

### `amino_acid_table1_per100g_edible.csv` (1,999 rows × 32 columns)
- Ids and name: `food_group`, `food_number`, `index_number`, `food_name_ja`.
- Protein context: `WATER`, `PROTCAA`, `PROT-`.
- 18 amino acids in mg/100 g: `ILE` isoleucine, `LEU` leucine, `LYS` lysine, `MET` methionine, `CYS` cystine, `AAS` sulfur AA total, `PHE` phenylalanine, `TYR` tyrosine, `AAA` aromatic AA total, `THR` threonine, `TRP` tryptophan, `VAL` valine, `HIS` histidine, `ARG` arginine, `ALA` alanine, `ASP` aspartic acid, `GLU` glutamic acid, `GLY` glycine, `PRO` proline, `SER` serine, `HYP` hydroxyproline.
- Totals: `AAT` amino-acid total, `AMMON` ammonia, `AMMON-E` excess ammonia.
- `remarks_ja`.

### `fatty_acid_table1_per100g_edible.csv` (1,967 rows × 63 columns)
- Summary columns in g/100 g: `FATNLEA`, `FAT-`, `FACID` total fatty acids, `FASAT` saturated, `FAMS` monounsaturated, `FAPU` polyunsaturated, `FAPUN3` n-3, `FAPUN6` n-6.
- ~45 individual fatty acids in mg/100 g, named `F<carbons>D<double bonds>[N3|N6|CN9…]`. Examples: `F16D0` palmitic, `F18D1CN9` oleic, `F18D2N6` linoleic, `F18D3N3` α-linolenic, `F20D4N6` arachidonic, `F20D5N3` **EPA**, `F22D6N3` **DHA**.
- `FAUN` unidentified fatty acids.
- Example: 10003 まあじ 皮つき 生 (Japanese horse mackerel, raw) has EPA 300 and DHA 570 mg/100 g.

### `carbohydrate_main_table.csv` (1,101 rows × 18 columns)
Columns, all g/100 g:
- `WATER`, `CHOAVLM` available carbohydrate (monosaccharide equivalents), `CHOAVL` total available carbohydrate (sum)
- `STARCH` starch
- sugars: `GLUS` glucose, `FRUS` fructose, `GALS` galactose, `SUCS` sucrose, `MALS` maltose, `LACS` lactose, `TRES` trehalose
- sugar alcohols: `SORTL` sorbitol, `MANTL` mannitol

Sample: `Data/standard-tables-of-food-composition-in-japan/sample.csv` · full profile: `Data/standard-tables-of-food-composition-in-japan/schema.md`

## Countries & cultures covered
- **[[Japan]]**: all 2,538 foods are foods commonly eaten in Japan.
- It includes foods of foreign origin (quinoa, bagels, kimchi) but there is no country-of-origin field.
- Strong coverage of Japanese staples: 471 fish and shellfish, 58 algae, soy products, miso and soy sauce variants, tsukemono, wagashi.

## Inferring effects on the body
- **Direct health fields:** none. The table is purely compositional.
- **Linkable:** nutrient columns use FAO/INFOODS tagnames, so they map to nutrient ontologies and to Japan's Dietary Reference Intakes (食事摂取基準) and other nutrient–health evidence.
- Examples:
  - 04046 糸引き納豆 (natto): VITK 600 µg/100 g, which the remarks note includes menaquinone-7. That is relevant to warfarin interaction and bone health.
  - 17045 淡色辛みそ (light miso): NA 4,900 mg, NACL_EQ 12.4 g/100 g. Relevant to hypertension advice.
  - Horse-mackerel EPA/DHA values support omega-3 advice.
- Evidence type: laboratory analysis (compositional). Health effects need an external nutrient→outcome resource.
- Non-nutrient bioactives (catechins, isoflavones, curcumin) are **not** in the table. Link foods via English names to FooDB for those.

## Linking to other datasets
- `food_number` is the join key across all MEXT tables and editions, and it is also used by Japanese nutrition software and dietary surveys.
- `food_name_ja` → ingredient strings in [[Our Regional Cuisines (Japan MAFF)]] and [[NII Cookpad Dataset]] recipes, for recipe-level nutrient estimates.
- `food_name_en_2015` → [[FooDB]] / [[USDA FoodData Central]] by name, for compounds.
- INFOODS tagnames align with [[Korean Food Composition Table]] (`nutrient_dictionary.csv` tagname column), so the same nutrient can be compared across Japan and Korea.

## Versions
- **Latest: 8th revised edition, 2023 supplement** (八訂 増補2023年), with errata applied 2026-03-27.
  - It updates part of the 2020 data and adds foods: 2,538 in the main table vs 2,478 in 2020.
  - The 2020 8th edition changed energy calculation to use component-based factors (available carbohydrate, fatty-acid TAG, amino-acid protein) instead of Atwater-type factors, so energy values are not comparable with the 7th edition.
- Previous: 2020 (8th), 2015 (7th, 2,191 foods, with English tables) and its annual supplements 2016–2019, back to the 1st edition in 1950.

## Caveats
- The raw Excel files have merged multi-row headers. Use the tidy CSVs, which keep all value markers as strings; convert `Tr`, `(…)` and `-` before any maths.
- English names are available only for foods that existed in 2015, and the 2015 descriptions may differ slightly from the 2023 Japanese names.
- Amino-acid table 2 (per g nitrogen) and table 3, fatty-acid tables 2–3, and the carbohydrate annexes (dietary fibre by method, organic acids) are only in the raw zip.
