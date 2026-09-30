---
title: "Bahrain Food Composition Tables"
slug: bahrain-food-composition-tables
kind: [food, ingredient]
version: "BFCT First Edition 2025 (Ministry of Health, Kingdom of Bahrain; PDF modified 2025-08-24)"
previous_versions: "Musaiger 1985 Bahrain FCT; Musaiger 2011 Gulf FCT (150 raw foods, ready meals and composite dishes of Arabian Gulf countries)"
papers: []
url: "https://www.moh.gov.bh/Content/Upload/File/638916394661198002-FCT-book-final-2025_ar.pdf"
license: "Not stated (government publication, free download)"
availability: open-download
access_link: "https://www.moh.gov.bh/Content/Upload/File/638916394661198002-FCT-book-final-2025_ar.pdf"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "The PDF (73 pages, 1.1 MB) downloaded directly with a browser UA. Despite the '_ar' file name, the book is in English with an Arabic-name column. We extracted all dish tables to CSV: 83 dish rows each for macronutrients, minerals and vitamins, plus macronutrients of 113 market products. Not extracted: the second half of the market-product table (SFA…sodium) and the annex 'Ingredients of the Dishes' (pp. 66–71), whose text layer is garbled (overlapping duplicate text)."
countries: ["[[Bahrain]]"]
regions: ["[[Middle East]]"]
n_records: "83 composite/traditional dish rows (82 dishes per the book) × 12 macro + 15 mineral + 10 vitamin columns; 113 market products × 7 (+8 not extracted) columns"
size: "1.1 MB PDF; ~60 KB CSV"
formats: [pdf, csv]
has_ingredients: true
has_amounts: partial
has_cooking_method: "no"
has_nutrition: true
body_effect: linkable
body_effect_how: "Per-100 g nutrients chosen for Bahrain's public-health problems (iron, iodine, vitamin D deficiency; energy, fat, SFA/TFA, cholesterol, sodium for NCDs) → link to nutrient-health guidance. No compound or health fields."
join_keys: [BFCT item code (e.g. 3.1), dish name (English transliteration + Arabic), source FCT (Kuwait/Lebanon/Oman/Jordan/Pakistan/UAE)]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/ingredients, search/regions]
tags:
  - type/dataset
  - kind/food
  - kind/ingredient
  - q/1
  - q/2
  - access/accessed
  - access/open
  - region/middle-east
---
# Bahrain Food Composition Tables

> [!abstract] TL;DR
> This is Bahrain's national food composition table (BFCT, 1st edition 2025), produced by the Ministry of Health Nutrition Section with WHO-EMRO technical support. It gives per-100 g composition of **82 commonly consumed traditional and composite dishes** and **113 market products**.
> - **27 dish rows are MOH-funded lab analyses.** The dishes were chosen by 24-h recall of 470 Bahraini adults, and recipes were standardised from 20 households.
> - **The rest are borrowed from other Gulf/Arab tables:** Kuwait (24), Oman (12), Lebanon (12), Jordan (7), UAE (1). The book cites Pakistan for chapati, but its row carries Jordan's 5-star marker; see Caveats.
> - **Dishes covered:** machboos (chicken, meat, hamour), saloona, harees, qouzi, marag, balaleet, halwa Bahraini, rahash, khubz tanoor/regag/mahyawa, karak tea.
> - **Values:** macronutrients (incl. SFA/TFA/MUFA, cholesterol), 15 minerals (incl. iodine, selenium) and 10 vitamins (incl. D, B12, folate).
>
> The whole dish section is extracted to CSV.

## Access
| | |
|---|---|
| Availability | open-download (PDF on moh.gov.bh) |
| Link | https://www.moh.gov.bh/Content/Upload/File/638916394661198002-FCT-book-final-2025_ar.pdf |
| Accessed? | true |
| How | `curl -L -A "<browser UA>"`. The dish tables were parsed from `pdftotext -layout` with a custom parser: row code + trailing value tokens, names completed up to the source-marker asterisks, Arabic names kept. Market macronutrients were parsed the same way. |
| Downloaded | `Data/bahrain-food-composition-tables/FCT-book-final-2025_ar.pdf` + `extracted/` (4 CSVs) |

## Tables & columns
Value tokens are kept as printed: `ND` = "not defined" (not analysed), `T` = traces, `<x` = below limit.

### `extracted/bfct_dishes_macronutrients.csv` (83 rows × 19)
| column | type | meaning | example |
|---|---|---|---|
| `code` | str | BFCT item code `<group>.<n>` | `3.1` |
| `category` | str | dish group (8): cereal, milk, chicken, meat, seafood, vegetables & legumes, sandwiches, traditional sweets | `Chicken-based dishes` |
| `english_name` | str | transliterated dish name | `MACHBOOS DAJAJ` |
| `arabic_name` | str | Arabic name from the table | `مجبوس دجاج` |
| `source_stars` / `source` | int / str | the footnote asterisks → data source: `*` direct analysis (MOH Bahrain), `**` FCT Kuwait, `***` Lebanon, `****` Oman, `*****` Jordan, `******` Pakistan, `*******` UAE | `1` / `Direct chemical analysis (MOH Bahrain)` |
| `H2O (ml/100g)` | str | water | `64.10` |
| `Energy (kcal/100g)` | float | energy (available, incl. fibre factor) | `168.00` |
| `CHO`, `Fiber`, `Sugar`, `Protein`, `Fat`, `SFA`, `TFA`, `MUFA`, `Ash` (g/100g) | str | total carbohydrate, total dietary fibre, sugars, protein, fat, saturated, trans and monounsaturated fatty acids, ash | `15.00`, `2.94`, `1.00`, `12.40`, `7.33`, `2.31`, `0.20`, `3.47`, `1.30` |
| `Cholesterol (mg/100g)` | str | cholesterol | `46.00` |

### `extracted/bfct_dishes_minerals.csv` (83 rows × 21)
Same id columns + `Na`, `K`, `Ca`, `P`, `Mg`, `Fe`, `Cu`, `Zn`, `Mn`, `B` (boron), `Cr`, `Al`, `I`, `Mo` (mg/100 g) and `Se` (mcg/100 g).
Example: Machboos dajaj Na 254 mg. Achar Bahraini (mixed pickles) Na 10,500 mg.

### `extracted/bfct_dishes_vitamins.csv` (83 rows × 16)
Same id columns + vitamin C, thiamin, riboflavin, niacin, B6 (mg/100 g), folate, B12 (mcg/100 g), vitamin A retinol (unit printed as "mg/100", probably µg), vitamin E (mg/100 g), vitamin D (IU).
Example: Karak tea C <2.00 · B1 0.50 · B2 0.55 · niacin 2.00 · B12 0.80 · D 12.50 IU.

### `extracted/bfct_market_products.csv` (113 rows × 10)
| column | type | meaning | example |
|---|---|---|---|
| `section` | str | 7 groups: Snacks 25, Dairy 19, beverages 17, Frozen 14, Baby food 14, Herbal water 13, Bakery 11 | `Snacks` |
| `product` | str | brand + product | `AL Kaleej Cheese and onion puff` |
| `H2O`, `Energy (kcal)`, `CHO`, `Fiber`, `Sugar`, `Protein`, `Total fat` (per 100 g) | str | macronutrients | `1.09`, `514.00`, `52.00`, `4.48`, `2.50`, `8.40`, `29.30` |

The book's second market table (SFA, TFA, MUFA, PUFA, cholesterol, calcium, iron, sodium) was **not** extracted because of misaligned rows.

Sample: `Data/bahrain-food-composition-tables/sample.csv` · full profile: `Data/bahrain-food-composition-tables/schema.md`

## Countries & cultures covered
- **[[Bahrain]]**: all 83 dish rows are foods consumed in Bahrain, and the 113 market products are sold there.
- By category: traditional sweets 20 · vegetables & legumes 13 · sandwiches 13 · meat 12 · seafood 10 · chicken 8 · cereal (breads) 4 · milk 3.
- About 56 of the 83 dish values are **borrowed** from other countries' tables (Kuwait 24, Oman 12, Lebanon 12, Jordan 7, UAE 1). Their compositions reflect those countries' recipes, not Bahraini ones. The data carries Bahraini labels only; we do not list the source countries as covered.
- The dishes are Gulf-typical (machboos, harees, qouzi, balaleet, gemat, rangina, tamrea, halwa Bahraini, shaar banaat) plus Levantine and South Asian foods common in Bahrain (hommos, falafel, shawarma, tabbouleh, biryani, chapati, mathai).

## Ingredients, amounts, cooking method
- **Ingredients:** the Annex (pp. 66–71) lists ingredients for each dish, many with grams. For example, Machboos dajaj: 100 g chicken, 500 g rice, 150 g onion, 20 g garlic, 10 g ginger, 60 g tomatoes, 15 g spices, 60 g coriander, 5 g turmeric, 60 g oil, 15 g salt, 5 g paprika, 10 g dry lemon, 5 g black pepper, 15 g mixed cumin and coriander seed, 100 g water. The annex text layer is garbled, so it was not converted to CSV (`has_amounts: partial`).
- **Cooking method:** not given per dish. The methods chapter describes standardised preparation by professional chefs.
- **Nutrition:** yes, per 100 g edible portion.

## Inferring effects on the body
- **Direct:** none.
- **Linkable:**
  - The nutrients were selected explicitly for Bahrain's deficiency diseases (iron, iodine, vitamin D) and NCD risks (energy, fat, SFA, TFA, cholesterol, sodium). They support advice such as sodium in pickles and machboos for hypertension, or sugar and fat in halwa and rahash for diabetes and obesity.
  - Mapping ingredients (turmeric, dry lime, cardamom, dates) to [[FooDB]] would add compounds.
- **Evidence type:** lab analysis (27 rows) or borrowed published data.

## Linking to other datasets
- There are no international food codes. Join by dish name.
- Shared Gulf dishes can be compared with [[Saudi Food Composition Tables]]: machboos ↔ kabsa, harees, balaleet, qurs 'aqeeli, halwa.
- Dish names can be matched in [[ArabCulture]] (no Bahrain split, but Gulf meal sentences) and [[WorldCuisines]].

## Versions
- 1st edition of BFCT, 2025. It supersedes Musaiger's 1985 Bahrain table and the 2011 Gulf FCT (150 foods), which are not in the vault.
- The MOH page file name ends in `_ar`, but the PDF is in English with Arabic names. We found no separate Arabic-only edition.

## Caveats
- The data is extracted from a PDF, and the source has typos:
  - item codes: `4.1` printed for `4.12`, `6.143` for `6.13`, and duplicated codes `7.1` and `8.19`
  - category headings: "SEAFOO-BASED DISHED", "TRADITIONAL SWEATS"
  - implausible values: Sweet corn H2O 123.5 ml/100 g, Machboos hamour CHO 114 g/100 g, Kounafa bil jeben protein 61 g/100 g
- Codes were repaired where unambiguous. Values are kept as printed.
- Source-marker asterisks are inconsistent between tables (Chapati has 5 stars in macros, 8 in vitamins). `source` is taken from the macronutrient table.
- `ND` means "not defined" and must not be read as zero.
- The market-product second table and the ingredient annex are not in CSV (see Access).
