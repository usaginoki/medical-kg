---
title: "CulinaryDB"
slug: "culinarydb"
kind: [food, ingredient]
version: "2018 release (files dated 2018-03-15/16)"
previous_versions: ""
papers: ["[[Singh2018 - Culinary patterns in traditional recipes]]"]
url: "https://cosylab.iiitd.edu.in/culinarydb/"
license: "CC BY-NC-SA 3.0 (site footer)"
availability: open-download
access_link: "https://cosylab.iiitd.edu.in/culinarydb/static/data/CulinaryDB.zip"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "The full zip (5.3 MB, 4 CSVs) downloads directly from the site with no login. Nothing blocked access."
countries: ["[[United States]]", "[[Italy]]", "[[Mexico]]", "[[France]]", "[[Canada]]", "[[Greece]]", "[[Spain]]", "[[Thailand]]", "[[China]]", "[[Japan]]", "[[South Korea]]", "[[Portugal]]", "[[Netherlands]]", "[[Belgium]]", "[[Australia]]", "[[New Zealand]]", "[[United Kingdom]]", "[[Ireland]]", "[[Germany]]", "[[Austria]]", "[[Switzerland]]"]
regions: ["[[North America]]", "[[Europe]]", "[[South Asia]]", "[[Middle East]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Latin America]]", "[[Sub-Saharan Africa]]", "[[North Africa]]", "[[Oceania]]"]
n_records: "45,772 recipes; 456,279 recipe-ingredient rows; 930 basic + 103 compound ingredients"
size: "29 MB unzipped"
formats: [csv]
has_ingredients: true
has_amounts: partial
has_cooking_method: no
has_nutrition: false
body_effect: linkable
body_effect_how: "Entity ID = FlavorDB/FlavorDB2 entity_id → flavor molecules (PubChem CID) → CTD/FooDB for health effects"
join_keys: [FlavorDB entity id, ingredient name]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food, search/ingredients]
tags:
  - type/dataset
  - kind/food
  - kind/ingredient
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# CulinaryDB

> [!abstract] TL;DR
> CulinaryDB is a database of 45,772 traditional recipes from 22 world regions plus 4 small "Misc." groups, built by CoSyLab at IIIT-Delhi (Singh & Bagler 2018). The recipes come from AllRecipes, Food Network, Epicurious and TarlaDalal. Every ingredient line is mapped to one of 930 basic ingredients or 103 compound ingredients, and each ingredient carries a **FlavorDB entity id**. That makes CulinaryDB the easiest open path from a *cuisine* to *ingredients* to *flavor molecules* (via [[FlavorDB2]]). The download is small and open. Its limits: cuisine labels are mostly region-level (e.g. "Middle East", "Indian Subcontinent"), there is no nutrition, and there are no cooking steps.

## Access
| | |
|---|---|
| Availability | open-download (link on the home page, "Download CulinaryDB") |
| Link | https://cosylab.iiitd.edu.in/culinarydb/static/data/CulinaryDB.zip |
| Accessed? | yes, complete |
| How | `curl -L` of the zip, then unzip (the zip was deleted afterwards) |
| Downloaded | `Data/culinarydb/`: all 4 CSVs (29 MB) |

## Tables & columns
Column meanings come from the paper (Materials section) and the file headers.

### `01_Recipe_Details.csv` (45,772 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Recipe ID` | int | recipe key (1–45772) | 1 |
| `Title` | str | recipe title | 5 spice vegetable fried rice |
| `Source` | str | source website: ALLRECIPES 16,177 · FOOD_NETWORK 15,917 · EPICURIOUS 11,069 · TARLA_DALAL 2,609 | TARLA_DALAL |
| `Cuisine` | str | geo-cultural region, one of 26 labels (22 regions + 4 "Misc.") | Indian Subcontinent |

### `04_Recipe-Ingredients_Aliases.csv` (456,279 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Recipe ID` | int | FK → `01_Recipe_Details` | 3398 |
| `Original Ingredient Name` | str | raw ingredient line from the source, often with quantity, unit and preparation | 1 1/2 pounds chicken legs, cut up |
| `Aliased Ingredient Name` | str | normalised ingredient (741 unique) | chicken |
| `Entity ID` | int | ingredient id; equals the FlavorDB entity_id for basic ingredients (e.g. onion 348, turmeric 341, checked against FlavorDB2) and is 2000+ for compound ingredients | 272 |

45,749 recipes have ingredient rows. The mean is 9.97 ingredients per recipe (median 9, max 63).

### `02_Ingredients.csv` (930 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Aliased Ingredient Name` | str | canonical ingredient | Cumin |
| `Ingredient Synonyms` | str | `;`-separated synonyms, including Hindi names | cumin; jeera |
| `Entity ID` | int | FlavorDB entity id | 332 |
| `Category` | str | one of 21 categories (Fruit 136, Fish 119, Vegetable 73, Dish 68, Plant 64, Herb 51, Spice 26, …) | Spice |

### `03_Compound_Ingredients.csv` (103 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Compound Ingredient Name` | str | ready-made mixes, sauces and dishes used as ingredients | Garam Masala |
| `Compound Ingredient Synonyms` | str | synonyms | garam masala |
| `entity_id` | int | id (2000–2102) | 2000 |
| `Contituent Ingredients` | str | basic ingredients the compound is made of (sic, header typo) | black pepper, mace, cinnamon, clove, cardamom, nutmeg |
| `Category` | str | 12 categories | Spice |

Sample: `Data/culinarydb/sample.csv` · full profile: `Data/culinarydb/schema.md`

## Countries & cultures covered
Counts of recipes per `Cuisine` label (value_counts over `01_Recipe_Details.csv`):

| Cuisine label | recipes | countries / vault region |
|---|---|---|
| USA | 16,118 | [[United States]] |
| Italy | 7,504 | [[Italy]] |
| Indian Subcontinent | 4,058 | [[South Asia]] (no country split; mostly TarlaDalal, so largely Indian) |
| Mexico | 3,138 | [[Mexico]] |
| France | 2,703 | [[France]] |
| Canada | 1,112 | [[Canada]] |
| Caribbean | 1,103 | [[Latin America]] |
| British Isles | 1,075 | [[United Kingdom]], [[Ireland]] |
| Middle East | 993 | [[Middle East]] (no country split) |
| China | 941 | [[China]] |
| Greece | 934 | [[Greece]] |
| Spain | 816 | [[Spain]] |
| Thailand | 667 | [[Thailand]] |
| Africa | 651 | [[Sub-Saharan Africa]] / [[North Africa]] (not split) |
| South East Asia | 611 | [[Southeast Asia]] (no country split) |
| Japan | 580 | [[Japan]] |
| Eastern Europe | 565 | [[Europe]] |
| Australia & NZ | 494 | [[Australia]], [[New Zealand]] |
| DACH Countries | 487 | [[Germany]], [[Austria]], [[Switzerland]] |
| Scandinavia | 404 | [[Europe]] |
| South America | 310 | [[Latin America]] |
| Korea | 301 | [[South Korea]] |
| Misc.: Portugal | 138 | [[Portugal]] |
| Misc.: Dutch | 40 | [[Netherlands]] |
| Misc.: Belgian | 15 | [[Belgium]] |
| Misc.: Central America | 14 | [[Latin America]] |

For the priority regions, the Middle East (993), the Indian Subcontinent (4,058), China, Japan and Korea, Thailand and South East Asia are each represented by a few hundred to a few thousand recipes. There is **no Central Asia label and no GCC country label**.

## Ingredients, amounts, cooking method
- **Ingredients:** yes. Each recipe is a list of ingredients normalised to 930 basic and 103 compound entities. For example, Middle East recipe 3398 contains cardamom, chicken, olive, onion, pomegranate, salt, sugar and walnut.
- **Amounts:** partial. There are no quantity or unit columns, but the raw line in `Original Ingredient Name` usually carries the amount ("4 cups pomegranate juice", "1/2 pound walnuts, toasted…") and would need parsing.
- **Cooking method:** no. The paper says procedures were extracted, but they are not in the released files.
- **Nutrition:** no.

## Inferring effects on the body
CulinaryDB has no health fields, so this is *linkable* only. `Entity ID` joins to [[FlavorDB2]] entities → molecules (PubChem CID, FooDB id). Those molecules can then be looked up in [[CTD]], [[FooDB]] or [[SpiceRx]] (e.g. Turmeric 341 → FlavorDB2 molecules → PubChem CID → SpiceRx/CTD disease links). The chain is ingredient-level flavor chemistry, not quantities.

## Linking to other datasets
- **[[FlavorDB2]]**: `Entity ID` = FlavorDB `entity_id` (checked: onion 348, turmeric 341, cumin 332, cardamom 327).
- **[[RecipeDB2]]**: same lab and a related ingredient vocabulary, but no shared recipe ids. RecipeDB2 links ingredients to the USDA `ndb_id` instead.
- **[[SpiceRx]]**: by spice name or scientific name. There is no shared id.

## Versions
One public release (2018). The larger, nutrition-annotated successor from the same lab is [[RecipeDB2]] (RecipeDB v1 had 118k recipes, v2 has 128,942). CulinaryDB remains the only one with a bulk download.

## Caveats
- Region labels are coarse and uneven: 35% of recipes are from the USA. "Africa", "Middle East" and "South East Asia" are not split by country.
- The recipes come from English-language Western recipe sites (plus TarlaDalal for India), so they reflect how these cuisines are presented to a Western audience rather than home cooking in those countries.
- Licence is CC BY-NC-SA 3.0 (non-commercial).
