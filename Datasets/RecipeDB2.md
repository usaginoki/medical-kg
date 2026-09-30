---
title: "RecipeDB2"
slug: "recipedb2"
kind: [food]
version: "RecipeDB2 (arXiv 2609.22099, Aug 2026)"
previous_versions: "RecipeDB v1 (Batra et al. 2020, Database baaa077; 118,171 recipes, 74 countries; https://cosylab.iiitd.edu.in/recipedb/)"
papers: ["[[Goel2026 - RecipeDB2 recipe data structure framework]]"]
url: "https://cosylab.iiitd.edu.in/recipedb2/"
license: "Data not released (paper: 'not publicly available due to institutional copyright restrictions'); v1 site CC BY-NC-SA 3.0; paper CC BY-NC-ND 4.0"
availability: contact-authors
access_link: "https://cosylab.iiitd.edu.in/recipedb2-api/recipe/<Recipe_id>"
accessed: partial
access_method: [api, scrape]
access_date: 2026-09-30
access_notes: "No bulk download for v2 or v1. The paper says the data is not public (institutional copyright). The RecipeDB2 React front end calls a JSON API (https://cosylab.iiitd.edu.in/recipedb2-api). GET /recipe/<id> works and returns a full recipe (ingredients with quantity/unit/state/USDA ndb_id, instructions, ~150 nutrients). All /recipe-search/* endpoints return an Express error or an empty payload, so v2 cannot be enumerated or counted. v1 search (POST /recipedb/search_recipe) works: 150 polite requests (1 req/s) gave per-country hit counts and 375 embedded sample records. The v1 statistics page's Plotly geoplot gave per-region counts. Full data needs the authors to be contacted (flagged to lead as NEEDS USER)."
countries: ["[[Italy]]", "[[Mexico]]", "[[United States]]", "[[Canada]]", "[[France]]", "[[Argentina]]", "[[India]]", "[[China]]", "[[Australia]]", "[[Greece]]", "[[United Kingdom]]", "[[Thailand]]", "[[Germany]]", "[[Ireland]]", "[[Nigeria]]", "[[Spain]]", "[[Japan]]", "[[Sweden]]", "[[Morocco]]", "[[Switzerland]]", "[[New Zealand]]", "[[Russia]]", "[[Netherlands]]", "[[Vietnam]]", "[[Poland]]", "[[Portugal]]", "[[South Korea]]", "[[Hungary]]", "[[Cuba]]", "[[Philippines]]", "[[Lebanon]]", "[[Brazil]]", "[[Turkey]]", "[[Denmark]]", "[[Norway]]", "[[Pakistan]]", "[[Indonesia]]", "[[Belgium]]", "[[Honduras]]", "[[Austria]]", "[[Egypt]]", "[[Czech Republic]]", "[[Peru]]", "[[Malaysia]]", "[[Puerto Rico]]", "[[Chile]]", "[[Finland]]", "[[Colombia]]", "[[Ethiopia]]", "[[Iraq]]", "[[Saudi Arabia]]", "[[Venezuela]]", "[[Nepal]]", "[[Cambodia]]", "[[Palestine]]", "[[Mongolia]]", "[[Costa Rica]]", "[[Jamaica]]", "[[Laos]]", "[[Guatemala]]", "[[Israel]]", "[[Ecuador]]", "[[Libya]]", "[[Somalia]]", "[[Sudan]]", "[[Bangladesh]]", "[[Namibia]]", "[[Angola]]", "[[Iceland]]"]
regions: ["[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "128,942 recipes, 35,474 ingredients (paper); we hold 43 v2 API recipes + 375 v1 web records + per-country/region counts"
size: "23 MB local sample (full DB not available)"
formats: [json, csv]
has_ingredients: true
has_amounts: yes
has_cooking_method: steps
has_nutrition: true
body_effect: linkable
body_effect_how: "ingredients carry USDA SR Legacy ndb_id (nutrients); v1 FAQ says generic ingredients were manually linked to FlavorDB and DietRx ids (health associations), not exposed in API output"
join_keys: [USDA NDB id, Recipe_id, ingredient name]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/contact
---
# RecipeDB2

> [!abstract] TL;DR
> RecipeDB2 (CoSyLab, IIIT-Delhi; Goel et al. 2026) is a structured database of **128,942 recipes** with 35,474 ingredients from **7 continents, 32 regions and 99 countries**. It combines RecipeDB v1 (118,171 recipes) with Archana's Kitchen (9,730) and Awesome Cuisine (1,132). Each ingredient is parsed into name, quantity, unit, state, size, temperature and dry/fresh, and linked to a USDA SR Legacy `ndb_id`. That link gives about 148 nutrients per recipe, plus dietary-style flags, cooking processes, utensils and ordered instructions. It is the richest cuisine-labelled recipe resource for the agent: amounts, steps and nutrition all in one place, with Middle Eastern, Indian-subcontinent and East/Southeast-Asian sub-regions. **But the data is not released.** We have only an API sample and web-derived counts.

## Access
| | |
|---|---|
| Availability | contact-authors. The paper's Data Availability statement says the data is "not publicly available due to institutional copyright restrictions". The web UI is browse-only. |
| Link | UI https://cosylab.iiitd.edu.in/recipedb2/ · API `https://cosylab.iiitd.edu.in/recipedb2-api/recipe/<id>` · v1 https://cosylab.iiitd.edu.in/recipedb/ |
| Accessed? | partial (sample + counts) |
| How | (1) Read the endpoints out of the React `bundle.js`. `GET /recipe/<id>` works, `GET /recipe/recipeOftheDay` works, and every `/recipe-search/*` call (continents, regions, sub-regions, recipe, recipesAdvanced, recipesByCategory) fails or returns no payload. We fetched 43 recipes by id. (2) v1 site: `POST /recipedb/search_recipe` with `autocomplete_cuisine=<country>` for all 75 country labels from `/recipedb/autocomplete_cuisine?q=`, first + last results page (1 req/s). Each results page embeds full recipe JSON for 20 rows, and we kept 5 per country. (3) v1 statistics geoplot (`/recipedb/static/geoplots/recipe_geoplot.html`) → per-region counts. |
| Downloaded | `Data/recipedb2/`: `v2_recipes.csv` (43), `v2_recipe_ingredients.csv` (484), `v2_recipe_instructions.csv` (462), `v2_recipe_nutrition_long.csv` (6,450 = 43 × 150 nutrients), `v1_web_sample_recipes.csv` (375), `v1_web_sample_ingredients.csv` (3,866), `raw/v1_country_counts.csv` (75), `raw/v1_geoplot_country_region_counts.csv` (149 map rows), raw JSON |

> [!warning] NEEDS USER
> The full RecipeDB2 dump needs someone to email the corresponding author, Ganesh Bagler (bagler@iiitd.ac.in; contact page https://cosylab.iiitd.edu.in/recipedb/contactUs). Files would go in `Data/recipedb2/`. As an alternative, enumerating `/recipe/<id>` over ids ≈ 2,610–140,000 would technically work but means ~130k requests. The lead should decide; it was not done.

## Tables & columns
Meanings come from the paper (NER attributes, dietary rules) and the v1 FAQ. API field names are quoted as served.

### `v2_recipes.csv` (43 rows): recipe header from `GET /recipe/<id>`
| column | type | meaning | example |
|---|---|---|---|
| `Recipe_id` | int | recipe key; same ids as v1 (observed range ≈ 2,610–130,000) | 72416 |
| `Recipe_title` | str | title | Iraqi Shish Kebab |
| `Continent` / `Region` / `Sub_region` | str | geo-cultural hierarchy (continent → region → country) | Asian / Middle Eastern / Iraqi |
| `Source` | str | origin site (AllRecipes, Geniuskitchen/Food.com, …) | Geniuskitchen |
| `url`, `img_url` | str | source recipe URL, image | http://www.geniuskitchen.com/recipe/iraqi-shish-kebab-234055 |
| `servings`, `prep_time`, `cook_time`, `total_time` | str/int | servings; minutes | 4 · 0 · 0 · 130 |
| `Calories` | float | calories per serving as given by source (inferred) | 226.5 |
| `Energy (kcal)`, `Protein (g)`, `Carbohydrate, by difference (g)`, `Total lipid (fat) (g)` | float | estimated whole-recipe macros from USDA mapping | 1460.26 · 78.39 · 15.52 · 118.36 |
| `Processes` | str | `||`-separated cooking verbs extracted from instructions | marinate\|\|put\|\|thread |
| `Utensils` | str | `||`-separated utensils | pan\|\|saucepan |
| `vegan`, `pescetarian`, `ovo_vegetarian`, `lacto_vegetarian`, `ovo_lacto_vegetarian` | 0/1 | rule-based dietary style (paper: exclusion-based on ingredient categories) | 0.0 |

### `v2_recipe_ingredients.csv` (484 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Recipe_id` | int | FK | 72416 |
| `position` | int | order in the recipe | 0 |
| `ingredient` | str | NER-extracted ingredient name | lamb |
| `quantity` | str | NER quantity | 1 1/2 |
| `unit` | str | NER unit (noisy, e.g. "1/2") | teaspoon |
| `state` | str | processing state | cubed |
| `ndb_id` | int | USDA SR Legacy NDB number used for nutrition | 17001 |

### `v2_recipe_instructions.csv` (462 rows)
`Recipe_id`, `step` (1…n), `instruction`, e.g. 72416 step 2 "Marinate the cubed meat in the marinade for at least 2 hours."

### `v2_recipe_nutrition_long.csv` (6,450 rows)
`Recipe_id`, `nutrient`, `value`. There are 150 USDA nutrient keys per recipe (e.g. `Calcium, Ca (mg)`, `Fatty acids, total polyunsaturated (g)`, `Caffeine (mg)`). The paper reports 148 nutritional parameters.

### `v1_web_sample_recipes.csv` (375) / `v1_web_sample_ingredients.csv` (3,866)
These are the v1 records embedded in search pages (5 per country label). Recipe fields are the same as v2. The ingredients add `ingredient_Phrase` (raw line), `size`, `temperature`, `D_F` (dry/fresh) and `M_or_C`/`Ing_id` (v1 internal ids; meaning not documented). The raw JSON (`raw/v1_sample_records.json`) also holds per-ingredient `nutrient_info`.

### `raw/v1_country_counts.csv` (75) · `raw/v1_geoplot_country_region_counts.csv` (149)
These hold the counts used below.

Sample: `Data/recipedb2/sample.csv` · full profile: `Data/recipedb2/schema.md`

## Countries & cultures covered
The paper gives 7 continents, 32 regions, 99 sub-regions (countries), 34 sub-sub-regions (states) and 12 sub-sub-sub-regions (cities), in Supplementary Table S1, which we did not see. **v2 counts could not be pulled**: the search API is broken. The counts below are from **RecipeDB v1 (118,171 recipes)**, which makes up 92% of v2. The ~10.9k recipes new in v2 come from Indian sites (Archana's Kitchen, Awesome Cuisine), so v2 Indian counts are higher.

**Region level (v1 statistics geoplot, exact):** Italian 16,582 · Mexican 14,463 · South American 7,176 · Canadian 6,700 · Indian Subcontinent 6,464 · French 6,381 · Chinese and Mongolian 5,896 · Australian 5,823 · US 5,031 · UK 4,401 · Deutschland 4,323 · Greek 4,185 · **Middle Eastern 3,905** · Caribbean 3,026 · Spanish and Portuguese 2,844 · Scandinavian 2,811 · Rest Africa 2,740 · Thai 2,605 · Irish 2,532 · Eastern European 2,503 · Japanese 2,041 · Southeast Asian 1,940 · Northern Africa 1,611 · Belgian 1,060 · Korean 668 · Central American 460. That makes 26 regions. The geoplot maps the Middle Eastern region onto Bahrain, Egypt, Iraq, Israel, Jordan, Kuwait, Lebanon, Oman, Palestine, Qatar, Saudi Arabia, Syria, Turkey, UAE and Yemen, but that is a map shading, not recipe labels.

**Country level (v1 search hits; approximate):** pages hold 20 rows and the last-page request appears to ignore `page`, so counts are rounded **up** to a multiple of 20.

| country (v1 label) | v1 region | recipes (≈) |
|---|---|---|
| [[Italy]] (Italian) | Italian | 16,580 |
| [[Mexico]] (Mexican) | Mexican | 14,460 |
| [[United States]] (US) | US | 10,900 ⚠ substring search also matches e.g. "Russian", "Australian" |
| [[Canada]] | Canadian | 6,700 |
| [[France]] | French | 6,380 |
| [[Argentina]] (Argentine) | South American | 6,040 ⚠ looks like a default label for most South American recipes |
| [[India]] | Indian Subcontinent | 5,980 |
| [[China]] | Chinese and Mongolian | 5,820 |
| [[Australia]] | Australian | 4,680 |
| [[Greece]] | Greek | 4,180 |
| [[United Kingdom]] (English 2,840 · Scottish 1,120 · Welsh 200 · UK 180) | UK | 4,340 |
| [[Thailand]] | Thai | 2,600 |
| [[Germany]] | Deutschland | 2,580 |
| [[Ireland]] | Irish | 2,520 |
| [[Nigeria]] (Nigerian) | Rest Africa | 2,520 ⚠ probably a default label for most of "Rest Africa" |
| — Rest Middle Eastern | Middle Eastern | 2,300 (includes e.g. Iranian/Persian recipes; no country label) |
| — Rest Caribbean | Caribbean | 2,200 |
| [[Spain]] | Spanish and Portuguese | 2,140 |
| [[Japan]] | Japanese | 2,040 |
| [[Sweden]] | Scandinavian | 1,820 |
| [[Morocco]] | Northern Africa | 1,560 |
| [[Switzerland]] | Deutschland | 1,380 |
| [[New Zealand]] | Australian | 1,120 |
| [[Russia]] | Eastern European | 840 |
| [[Vietnam]] | Southeast Asian | 700 |
| [[Poland]] | Eastern European | 700 |
| [[Netherlands]] (Dutch) | Belgian | 700 |
| [[Portugal]] | Spanish and Portuguese | 680 |
| [[South Korea]] (Korean) | Korean | 660 |
| [[Hungary]] | Eastern European | 560 |
| [[Philippines]] (Filipino) | Southeast Asian | 540 |
| [[Cuba]] | Caribbean | 540 |
| [[Lebanon]] | Middle Eastern | 460 |
| [[Brazil]] | South American | 440 |
| [[Turkey]] | Middle Eastern | 420 |
| [[Norway]] · [[Denmark]] | Scandinavian | 400 · 400 |
| [[Pakistan]] | Indian Subcontinent | 360 |
| [[Indonesia]] | Southeast Asian | 360 |
| [[Belgium]] · [[Austria]] · [[Honduras]] | Belgian · Deutschland · Central American | 340 each |
| [[Egypt]] | Middle Eastern | 320 |
| [[Czech Republic]] · [[Peru]] | Eastern European · South American | 240 each |
| [[Malaysia]] · [[Puerto Rico]] | Southeast Asian · Caribbean | 220 each |
| [[Chile]] | South American | 160 |
| [[Finland]] · [[Colombia]] · [[Ethiopia]] | … | 140 each |
| [[Iraq]] · [[Saudi Arabia]] | Middle Eastern | 100 each |
| — Rest Eastern European | Eastern European | 100 |
| [[Venezuela]] · [[Nepal]] · [[Cambodia]] | … | 80 each |
| [[Palestine]] · [[Mongolia]] | Middle Eastern · Chinese and Mongolian | 60 each |
| [[Laos]] (labelled Middle Eastern in v1!) · [[Jamaica]] · [[Costa Rica]] · [[Guatemala]] | … | 40 each |
| [[Israel]] · [[Ecuador]] · [[Libya]] | … | 20 each |
| [[Somalia]] 19 · [[Sudan]] 19 · [[Bangladesh]] 16 · [[Namibia]] 14 · [[Angola]] 12 · [[Iceland]] 9 | | exact (single page) |

Priority regions:
- **Middle East:** Lebanon, Turkey, Egypt, Iraq, Saudi Arabia, Palestine, Israel, plus "Rest Middle Eastern". No UAE, Kuwait, Qatar or Oman labels. One v2 sample recipe, "Al Harees … Traditional Qatari, Iraqi", is labelled Iraqi.
- **South Asia:** India, Pakistan, Nepal, Bangladesh.
- **East Asia:** China, Japan, South Korea, Mongolia.
- **Southeast Asia:** Thailand, Vietnam, Philippines, Indonesia, Malaysia, Cambodia, Laos.
- **Central Asia:** nothing.

## Ingredients, amounts, cooking method
- **Ingredients + amounts:** yes. Each ingredient has `quantity`, `unit` and `state`, and v1 adds `size`, `temperature` and dry/fresh. Example: Iraqi Shish Kebab (72416) = lamb 1 cubed · vinegar 1 1/2 · olive oil 1 1/2 · onion 1 chopped · salt 1/2 teaspoon · pepper 1/4 teaspoon. The paper converted 43.9% of the frequent ingredient-unit pairs to grams/ml.
- **Cooking method:** yes. There are ordered `instructions` (steps) plus the extracted `Processes` and `Utensils`.
- **Nutrition:** yes. Every mapped ingredient links to USDA via `ndb_id`, and recipes carry 150 nutrient keys. 73% of ingredients (25,903/35,474) were mapped with BERT similarity ≥ 70%.

## Linking to other datasets
- **[[USDA FoodData Central]] (SR Legacy):** `ndb_id` → full nutrient profile.
- **[[FlavorDB2]] / DietRx:** the v1 FAQ says generic ingredients were hand-linked to FlavorDB ids and DietRx ids, but those ids are not in the API output we saw.
- **[[CulinaryDB]]:** same lab and similar sources (AllRecipes, Epicurious, Food Network), but no shared keys.

## Versions
- **RecipeDB v1** (2020, Database baaa077): 118,171 recipes, 6 continents, 26 regions, 74 countries, 268 processes, >8,700 ingredients (v1 how-to page). Flask/SQLite web UI with working search; **no bulk download either**.
- **RecipeDB2** (2026): adds 10,862 recipes (Archana's Kitchen, Awesome Cuisine). It also brings a transformer NER, BERT-based USDA mapping (F1 87.9; the paper says v1 had low NER performance and mapping efficiency), 34 ingredient categories predicted with Random Forest (accuracy 89.1%), a conservative dietary-style rule set, and 32 regions / 99 countries.

## Caveats
- Neither version is openly downloadable. Everything held locally is a sample, and the counts come from v1.
- v1 country labels are unreliable in places: Laos is placed under "Middle Eastern", and "Argentine" and "Nigerian" look like default labels. The US count is inflated by substring search.
- The recipes come from English-language Western sites (AllRecipes, Food.com) plus Indian sites. There is almost no GCC or Central Asian content.
- API macros are sometimes 0.0 (e.g. recipe 3064), so nutrition estimates can be incomplete.
