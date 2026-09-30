---
title: "Korean Food Composition Table"
slug: korean-food-composition-table
kind: [ingredient]
version: "National Standard Food Composition DB 10.4 (국가표준식품성분 DB 10.4; 10th revision series)"
previous_versions: "DB 10.0, 10.1, 10.2, 10.3 (sheets in the same workbook) · 9th revision (2016) and earlier printed editions since 1970"
papers: []
url: "https://koreanfood.rda.go.kr/kfi/fct/fctIntro/list?menuId=PS03562"
license: "KOGL Type 1 (attribution) for the annual DB Excel; KOGL Type 2 (attribution, non-commercial) for the printed book PDF"
availability: open-download
access_link: "https://www.nics.go.kr/food/kfi/fct/fctIntro/list?menuId=PS03562"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "The Excel download sits behind a short anonymous usage survey: a pop-up asks for purpose and occupation, with no account. We selected 'academic research' and 'academic research staff' and POSTed to /food/kfi/fct/fctIntro/downloadImg.do (gubun=EXCEL), which returned 식품성분표(10개정판).xlsx (13.3 MB, sheets DB 10.0–10.4 + appendices). The site redirects koreanfood.rda.go.kr → www.nics.go.kr/food. The same DB is also on data.go.kr as an Open API."
countries: ["[[South Korea]]"]
regions: ["[[East Asia]]"]
n_records: "3,366 foods (DB 10.4) × 132 components"
size: "13.3 MB xlsx (zipped 12 MB) + 3.5 MB tidy CSV"
formats: [xlsx, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: true
body_effect: linkable
body_effect_how: "Per-100 g values for 132 components (proximates, sugars, fibre, 12 minerals, vitamins incl. K1/K2 and tocotrienols, 19 amino acids incl. taurine, ~40 fatty acids incl. EPA/DHA/trans) with INFOODS tagnames; scientific names (2,090 foods) link to FooDB/NCBI taxonomy for bioactive compounds; health effects via external nutrient→outcome evidence."
join_keys: [RDA food code (12-char), DB index, INFOODS tagname, scientific name, food name (KO/EN)]
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
# Korean Food Composition Table

> [!abstract] TL;DR
> South Korea's national food composition database (국가표준식품성분 DB), maintained by the **Rural Development Administration (RDA/NICS)**. The latest is **DB 10.4**, the 4th yearly update of the 10th revision. It gives per-100 g edible-portion values for **3,366 foods × 132 components**. It includes **official English food names and scientific names** plus a Korean-English nutrient dictionary. Coverage of Korean foods is strong: 18 kinds of kimchi, jang (fermented pastes), namul, ginseng, seaweeds and 683 seafood items.

## Access
| | |
|---|---|
| Availability | open-download (Excel after a 2-question anonymous survey; also Open API on data.go.kr) |
| Link | <https://www.nics.go.kr/food/kfi/fct/fctIntro/list?menuId=PS03562> (old: koreanfood.rda.go.kr) · English search UI: `/food/eng/fctFoodSrchEng/main` |
| Accessed? | true |
| How | `curl` POST `gubun=EXCEL&usepurps=704010&occpgrupp=704017` (academic research / academic staff) to `/food/kfi/fct/fctIntro/downloadImg.do` with a session cookie |
| Downloaded | `Data/korean-food-composition-table/`: `raw_kfct_10th_rev_db10.0-10.4.zip` (original xlsx) plus tidy CSVs `kfct_db10_4_per100g.csv`, `food_names_ko_en_scientific.csv`, `nutrient_dictionary.csv` |

Original workbook sheets:
- `DB 설명` (description)
- `국가표준식품성분 Database 10.0` … `10.4` (one sheet per yearly version, 137 columns)
- `DB 10.4 신규,교체,삭제 식품목록`: foods new, replaced or deleted in 10.4 (188 rows)
- `부록1)식품코드 연계표`: food-code crosswalk across DB 10.0–10.4
- `부록2)식품코드,국문명,영문명,학명 정보`: food code, Korean name, English name, scientific name
- `부록3)영양성분표기및단위`: nutrient code, Korean and English name, tagname, unit

## Tables & columns
### `kfct_db10_4_per100g.csv` (3,366 rows × 140 columns)
Built from sheet DB 10.4, with codes, English names and scientific names joined from 부록2 by DB index. Nutrient columns are named `<TAGNAME>__<english_name>_<unit>`, taken from 부록3.

| column | type | meaning (Korean header → English) | example |
|---|---|---|---|
| `db_index` | int | DB10.4 색인, row index (stable within 10.x; crosswalk in 부록1) | 795 |
| `book_index_10th` | int | 10개정 책자 색인, index in the printed 10th-revision book (blank = DB-only food; 1,215 foods are in the book) | |
| `food_group_ko` | str | 식품군, food group (20 groups, see below) | 채소류 (vegetables) |
| `food_name_ko` | str | 식품명, food name, comma-faceted: food, variety/part, processing, state | 김치, 배추 김치 |
| `source` | str | 출처, data source and year: 농진청 = RDA analysis; USDA('18) = borrowed from the US table (207 foods); JAPAN('20) = borrowed from the Japanese table (204); 식약 = MFDS; 수('09) = meaning not stated in the file (inferred: compiled from earlier or literature values), 533 foods | 농진청('22) |
| `food_code` | str | 식품코드, 12-character RDA food code | F2050070009a |
| `food_name_en` | str | 식품명_영문명, official English name | Kimchi, Baechukimchi, Prepared with Kimchi cabbage |
| `scientific_name` | str | 학명, scientific name (2,090 / 3,366 filled) | Panax ginseng C. A. Meyer |
| `ENERC__energy_kcal` | str | 에너지, energy (kcal) | 38 |
| `WATER__water_g`, `PROT__protein_g`, `FATCE__fat_g`, `ASH__ash_g`, `CHOCDF__carbohydrate_g` | str | 수분 water, 단백질 protein, 지방 fat, 회분 ash, 탄수화물 carbohydrate (g) | |
| `SUGAR__total_sugars_g` … `GALS__galactose_g` | str | 당류 total sugars, 자당 sucrose, 포도당 glucose, 과당 fructose, 유당 lactose, 맥아당 maltose, 갈락토오스 galactose (g) | |
| `FIBTG`, `FIBSOL`, `FIBINS` | str | 총, 수용성, 불용성 식이섬유: total, soluble, insoluble fibre (g) | |
| `CA` … `MN` (mg), `SE`, `MO`, `ID` (µg) | str | 칼슘 calcium, 철 iron, 마그네슘 magnesium, 인 phosphorus, 칼륨 potassium, 나트륨 sodium, 아연 zinc, 구리 copper, 망간 manganese, 셀레늄 selenium, 몰리브덴 molybdenum, 요오드 iodine | NA 551 mg |
| vitamins | str | 비타민 A (RAE), 레티놀 retinol, 베타카로틴 β-carotene, 티아민 thiamin, 리보플라빈 riboflavin, 니아신 niacin (+NE, nicotinic acid, nicotinamide), 판토텐산 pantothenic acid, B6 (+pyridoxine), 비오틴 biotin, 엽산 folate (DFE, food folate, folic acid), B12, C, D (D2, D3), E (α/β/γ/δ-tocopherol, α/β/γ/δ-tocotrienol), K (K1 phylloquinone, K2 menaquinone) | |
| amino acids (mg) | str | 총 아미노산 total, 총 필수아미노산 total essential; Ile, Leu, Lys, Met, Phe, Thr, Trp, Val, His, Arg, Tyr, Cys, Ala, Asp, Glu, Gly, Pro, Ser, 타우린 taurine | |
| `CHOLE__cholesterol_mg` | str | 콜레스테롤, cholesterol | |
| fatty acids | str | total, essential, saturated (4:0–24:0), MUFA (14:1–24:1), PUFA (18:2n-6, 18:3n-3, 18:3n-6, 20:2–22:6, incl. EPA `F20D5N3`, DPA `F22D5N3`, DHA `F22D6N3`), n-3, n-6, trans (total, 18:1t, 18:2t, 18:3t); g for totals, mg for individual acids | |
| `NACL_EQ__salt_equivalent_g` | str | 식염상당량, salt equivalent | |
| `REFUSE__refuse_%` | str | 폐기율, refuse | |

`-` = not analysed. Some nutrient columns lack a tagname in 부록3; those carry only the English name, e.g. `riboflavin_mg`, `total_amino_acids_mg`.

### `food_names_ko_en_scientific.csv` (3,366 rows)
`db_index`, `food_code`, `food_name_ko`, `food_name_en`, `scientific_name`, straight from sheet 부록2. Example: `R0720000005a` 강황, 가루 / Turmeric, Powder / *Curcuma aromatica*.

### `nutrient_dictionary.csv` (132 rows)
`nutrient_code` (RDA code, e.g. A10100), `name_ko`, `name_en`, `tagname` (FAO/INFOODS), `unit`. This is the Korean→English translation of every column header.

Sample: `Data/korean-food-composition-table/sample.csv` · full profile: `Data/korean-food-composition-table/schema.md`

## Countries & cultures covered
- **[[South Korea]]**: 3,366 foods commonly eaten in Korea.
- About 12% of foods (411) have values borrowed from foreign tables: USDA 207, Japan 204.

Food groups (rows): seafood 어패류 683 · vegetables 채소류 613 · cereals 곡류 446 · meat 육류 436 · fruits 과일류 265 · seasonings 조미료류 135 · mushrooms 버섯류 95 · pulses 두류 88 · nuts & seeds 견과류 및 종실류 78 · potatoes & starches 감자류 및 전분류 77 · teas 차류 68 · milk 우유 58 · sugars 당류 55 · prepared/processed foods 조리가공식품류 54 · seaweeds 해조류 53 · beverages 음료류 37 · eggs 난류 34 · other 기타 34 · fats & oils 유지류 32 · alcoholic drinks 주류 25.

Korean-specific items include:
- 18 kimchi types: 배추김치 by growing season, 깍두기, 동치미, 백김치 …
- red and white ginseng (인삼/홍삼) and extracts
- jang: 된장, 고추장, 간장
- many regional rice varieties

## Inferring effects on the body
- **Direct:** none. The table is compositional only.
- **Linkable:**
  - INFOODS tagnames → nutrient reference intakes (KDRIs) and nutrient–disease evidence.
  - `scientific_name` → NCBI Taxonomy / FooDB for non-nutrient bioactives such as ginsenosides and curcuminoids.
- Examples:
  - 배추김치 (baechu kimchi) has NA 551 mg/100 g, relevant to sodium and hypertension advice for Korean diets.
  - 강황 가루 (turmeric powder), *Curcuma aromatica*: link via the species name to FooDB/PubChem for curcumin. Note that the species differs from the usual *C. longa*.
  - 인삼 (ginseng), *Panax ginseng*: link to ginsenoside compounds.
- Evidence type: laboratory analysis (RDA), plus values borrowed from USDA and Japan.

## Linking to other datasets
- Tagnames align with [[Standard Tables of Food Composition in Japan]] (same INFOODS system), which allows Japan–Korea comparison. Note that 204 Korean values are taken from the Japanese table.
- `scientific_name` and `food_name_en` → [[FooDB]] / [[USDA FoodData Central]].
- `food_code` → Korean dietary-survey (KNHANES) food codes via RDA (inferred).

## Versions
- **Latest: DB 10.4.** It adds, replaces or deletes 188 foods relative to 10.3 (sheet `DB 10.4 신규,교체,삭제 식품목록`), e.g. new rice cultivars 바로미3 and 새청무.
- The yearly DB updates 10.0, 10.1, 10.2, 10.3 and 10.4 (3,366 foods) are all sheets in the same workbook. 부록1 crosswalks food codes across them.
- Printed 『국가표준식품성분표』 books appear every 5 years (1970 first; 10th revision current). The integer part of the DB number is the revision; the decimal is the yearly update.

## Caveats
- The download needs the anonymous purpose survey, which curl can answer with a POST as described above.
- The `source` code 수('xx) is undocumented in the workbook.
- 1,276 foods lack a scientific name, mostly processed foods and dishes.
- Missing values are `-`.
- There are no cooked-dish recipes beyond ~54 prepared foods.
