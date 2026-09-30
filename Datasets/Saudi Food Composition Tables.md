---
title: "Saudi Food Composition Tables"
slug: saudi-food-composition-tables
kind: [food, ingredient]
version: "1st edition, English PDF SFCT-E.pdf (PDF created 2026-02-17, posted 2026-04); SFDA National Nutrition Committee"
previous_versions: "None as an official national table. SFDA's 2023 Saudi Branded Food Database (beverages) is a separate product."
papers: ["[[Fallata2026 - Saudi Food Composition Database food matching]]"]
url: "https://www.sfda.gov.sa/en/news/5521984"
license: "Not stated in the PDF (government publication, free access per FAO/INFOODS listing)"
availability: open-download
access_link: "https://www.sfda.gov.sa/sites/default/files/2026-04/SFCT-E.pdf"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "The English PDF (311 pages, 44.9 MB) downloaded with a browser User-Agent. The first attempt was cut off at 13 MB; the retry was complete. We parsed all 130 dishes to CSV (recipe, ingredients with amounts, 49 analytes per 100 g and per full recipe). The searchable web tool https://fd.sfda.gov.sa/ is geo-restricted: the TCP connection is reset from our host (3 tries plus WebFetch). FAO's listing warns 'access may be restricted in certain countries'. We did not get the Arabic PDF."
countries: ["[[Saudi Arabia]]"]
regions: ["[[Middle East]]"]
n_records: "130 dishes × 49 analytes (6,370 values per 100 g + full-recipe values); 1,154 ingredient lines"
size: "44.9 MB PDF; 1.2 MB extracted CSV"
formats: [pdf, csv]
has_ingredients: true
has_amounts: "yes"
has_cooking_method: steps
has_nutrition: true
body_effect: linkable
body_effect_how: "Laboratory-analysed nutrients per dish (sodium, saturated/trans fat, cholesterol, fibre, sugars, iodine, vitamin D, folate…) link to nutrient→health guidance (WHO/SFDA reference intakes, Appendix 2 of the book). There are no compound or health fields."
join_keys: [dish name (English transliteration), region of KSA, ingredient name (free text), nutrient name]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/regions, search/ingredients]
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
# Saudi Food Composition Tables

> [!abstract] TL;DR
> This is the first official food composition book for **traditional Saudi dishes**, published by the Saudi Food and Drug Authority (SFDA) National Nutrition Committee under Vision 2030. It covers **130 dishes from all 13 regions of the Kingdom**. Each dish has a standardized recipe from the Culinary Arts Commission (ingredients with grams or ml, numbered preparation steps, servings of 4–6 adults), was cooked 3 times by Saudi chefs, and was **analysed in ISO 17025 labs for 49 components** (about 19,000 analyses). Values are given per 100 g and per full recipe. For the agent this is the best GCC resource: region-labelled home dishes (kabsa, jareesh, mathlouthah, marqouq, harees-type dishes, masabeeb, aseedah) with measured sodium, fat quality, fibre, iodine and vitamins. We parsed the whole book into CSV.

## Access
| | |
|---|---|
| Availability | open-download (PDF); searchable web tool at fd.sfda.gov.sa (geo-restricted) |
| Link | https://www.sfda.gov.sa/sites/default/files/2026-04/SFCT-E.pdf · web tool https://fd.sfda.gov.sa/ · FAO listing https://www.fao.org/food-composition/tables-and-databases/detail/saudi-arabia--2025)-saudi-food-composition-tables/en |
| Accessed? | true: full PDF. Web tool: false (connection reset, likely geo-block) |
| How | `curl -L -A "<browser UA>"` → PDF; `pdftotext -layout` + a Python parser (per page: "Recipe Name" page → dish, servings, ingredients, steps; next page → "The dish's nutritional content" table) |
| Downloaded | `Data/saudi-food-composition-tables/SFCT-E.pdf` (311 pp) + `extracted/` (4 CSVs, all 130 dishes) |

## Tables & columns
Region is assigned from the book's table of contents (page ranges per region).

### `extracted/sfct_dishes.csv` (130 rows)
| column | type | meaning | example |
|---|---|---|---|
| `dish_id` | int | our running id (book order) | `1` |
| `dish_name` | str | English dish name as printed | `Qursan` |
| `region` | str | administrative region chapter of the book | `Riyadh` |
| `serves_adults` | int | "Approximately N adults": the full recipe serves 4 or 6 | `4` |
| `recipe_page` | int | PDF page of the recipe | `14` |
| `preparation_steps` | str | numbered steps joined with ` \| ` | `1. Heat oil in a deep pot and sauté the onions…` |

### `extracted/sfct_ingredients.csv` (1,154 rows; median 7 per dish)
| column | type | meaning | example |
|---|---|---|---|
| `dish_id`, `dish_name` | | dish | `94`, `Lamb Kabsa` |
| `component` | str | ingredient block heading (dishes can have e.g. broth, dough, garnish blocks) | `Kishnah (Sautéed Onion Mixture) Ingredients` |
| `ingredient` | str | ingredient with preparation note | `Lamb fat (tail fat), chopped` |
| `quantity` | str | amount + unit as printed (g, ml, L, pieces, "(optional)") | `80 g` |

### `extracted/sfct_nutrients_long.csv` (6,370 rows = 130 × 49)
| column | type | meaning | example |
|---|---|---|---|
| `analyte` | str | one of 49 components (below) | `Sodium` |
| `per_100g` | str | value per 100 g edible portion; `-` = below detection limit | `422` |
| `full_recipe` | str | value for the whole recipe (4–6 adults) | `10500` |
| `unit` | str | unit as printed | `mg` |

### `extracted/sfct_per100g_wide.csv` (130 rows × 53)
One row per dish with `region`, `serves_adults` and 49 columns `"<analyte> [<unit>]"` (per 100 g). Analytes:
- **Energy & proximates:** energy kJ/kcal, moisture, total protein, total nitrogen, total fat, available and total carbohydrates, total and added sugars, total/soluble/insoluble dietary fibre, ash, cholesterol.
- **Fatty acids:** SFA, MUFA, PUFA, total unsaturated, trans fat, sums of n-3, n-6 and n-9.
- **Minerals:** Ca, Fe, Mg, P, K, Na, Cl, Zn, Cu, Mn, Se, I.
- **Vitamins:** A (retinol), β-carotene, D, E, K, C, B1, B2, B3, B5, B6, B7 (biotin), B9 (folic acid), B12.

The most sparse (`-`, below detection) are vitamin C (129/130), β-carotene (126), B6 (104), vitamin A (102) and B2 (100).

Sample: `Data/saudi-food-composition-tables/sample.csv` · full profile: `Data/saudi-food-composition-tables/schema.md`

## Countries & cultures covered
- **[[Saudi Arabia]]**: 130 dishes, all Saudi. By region chapter:
  - Makkah 22 · Al-Madinah 13 · Al-Baha 13 · Al-Jawf 12 · Tabuk 11 · Riyadh 10 · Najran 9
  - Eastern 8 · Jazan 8 · Al-Qassim 7 · Aseer 7 · Hail 5 · Northern Borders 5
- Dishes include:
  - **Najd/Riyadh:** Qursan, Al-Jareesh, Margaouq, Qishd, Hamees, Henaini
  - **Hijaz/Makkah:** Bukhari rice, Saleeg, Mutabbaq, Ma'soub, Mantu (Yemeni yaghmish), Miro camel kabab
  - **Madinah:** Madini rice, Mathlouthah, Kunafah
  - **Eastern:** Hassawi rice, Balaleet, Muhammar fish
  - **Qassim:** Kleja, Matazeez
  - **Aseer:** Haneeth, Areekah
  - **Tabuk:** Mansaf, Sayadiah
  - **Baha:** Lamb, camel and chicken Kabsa
  - **Jawf:** desert-truffle dishes, Samh bread
  - **Jazan:** Marsah, Lahouh, Mkashan fish
  - **Najran:** Bormah, corn Ma'asoubah
- Ingredients typical of the region are frequent in the ingredient lines: ghee (70 lines), whole wheat and cracked wheat (56), lamb (37), cardamom (25), dates (16), laban (10), dried black lime (12), saffron (6), camel meat (4), samh seeds (4), desert truffle (2).

## Ingredients, amounts, cooking method
- **Ingredients + amounts:** yes, in grams/ml per full recipe, grouped by sub-recipe. Example, *Lamb Kabsa* (Al-Baha, 4 adults): lamb 667 g, lamb tail fat 80 g, tomato 213 g, onion 93 g, black pepper 5 g, short-grain rice 600 g, salt 36 g, water 2.8 L. Kabsa spice lines (e.g. cardamom, dried lime) wrap onto 2 lines in the PDF, and our parser may drop them (see Caveats).
- **Cooking method:** numbered steps with times and heat (e.g. Al-Jareesh: pressure-cook cracked wheat with laban 1 h, add ghee + cumin, 30 min more).
- **Nutrition:** measured, not calculated.
  - Per 100 g: median energy 179.5 kcal, median sodium 215.5 mg (max 730 mg, Matboukhah), median fat 5.6 g (max 69.5 g, Hamashah, the most energy-dense at 666 kcal).
  - Examples: Qursan 132 kcal · 7.5 g fat · 422 mg Na · 4.1 g fibre. Lamb Kabsa 158 kcal · 6.1 g fat · 497 mg Na.

## Inferring effects on the body
- **Direct:** none. The book is compositional only; Appendix 2 lists reference dietary recommendations.
- **Linkable:**
  - The nutrient values support standard nutrient→health reasoning, e.g. sodium per serving for hypertension, SFA/cholesterol for CVD, available carbohydrate and sugars for diabetes, iodine and vitamin D (key GCC deficiencies).
  - Ingredient names (ghee, dates, black lime, cardamom, saffron) can be matched by hand to FooDB / USDA entries to reach compounds.
- **Evidence type:** laboratory analysis (accredited labs), 3 preparations per dish, at least 3 samples analysed.

## Linking to other datasets
- There are no standard IDs (no INFOODS codes or food codes in the PDF). Joins are by dish name and ingredient name.
- [[ArabCulture]] (Saudi meal-slot sentences) and [[BLEnD]] / [[WorldCuisines]] Saudi dish mentions can be matched by name (kabsa, jareesh, mutabbaq).
- Ingredient names → [[USDA FoodData Central]] / [[FooDB]] for single-ingredient composition and compounds.
- Compare with [[Bahrain Food Composition Tables]] for shared Gulf dishes (machboos/kabsa, harees, balaleet, qurs 'aqeeli).

## Versions
- This is the first edition (English PDF 2026; SFDA announced the book in 2026 and the FAO listing dates it 2025). An Arabic edition exists (per the book) but we did not download it.
- The web tool fd.sfda.gov.sa is the "Saudi Food Composition Database". Per the [[Fallata2026 - Saudi Food Composition Database food matching|Fallata et al. 2026]] preprint, it is a broader SFCD compiled from literature, analysis and borrowed McCance & Widdowson values, with 17 food groups and ~90 sub-groups. We could not reach it.

## Caveats
- The data is extracted from a PDF.
  - The nutrient tables parsed cleanly: every dish has all 49 analytes.
  - Ingredient lines whose name and quantity wrap across 2 lines may be merged or dropped: 24 dishes have fewer than 5 parsed ingredients. Verify against the PDF page given in `recipe_page`.
- There are source typos. On the *Mardhoufah* nutrient page the units are shifted by one row (energy kJ printed with unit "kcal", etc.). Our wide table keeps the values under the modal unit, and the long table keeps the printed unit.
- Energy is kept as printed (kJ/kcal). Full-recipe values are rounded to 3 significant figures.
- The web database may contain more foods than the book. It is inaccessible from our location (see NEEDS USER in the session report).
