---
title: "World Wide Dishes"
slug: world-wide-dishes
kind: [food]
version: "v1 (WorldWideDishes_2024_June; HF repo updated 2025-02-13)"
previous_versions: ""
papers: ["[[Magomere2024 - World Wide Dishes]]"]
url: "https://github.com/oxai/world-wide-dishes"
license: "CC-BY-4.0 + terms of use (evaluation use; no use for prompt templates that generate training data; no image generation for training)"
availability: open-download
access_link: "https://huggingface.co/datasets/WorldWideDishes/worldwidedishes-v1"
accessed: true
access_method: [huggingface]
access_date: 2026-09-30
access_notes: "Whole HF repo downloaded with `hf download` (no login, not gated). The contributor photos are only in a Google Drive folder and were not downloaded; image URLs in the CSV point to Openverse/DuckDuckGo/Drive."
countries:
  - "[[Algeria]]"
  - "[[Angola]]"
  - "[[Argentina]]"
  - "[[Armenia]]"
  - "[[Australia]]"
  - "[[Austria]]"
  - "[[Bangladesh]]"
  - "[[Belgium]]"
  - "[[Benin]]"
  - "[[Bosnia and Herzegovina]]"
  - "[[Brazil]]"
  - "[[Brunei]]"
  - "[[Bulgaria]]"
  - "[[Burkina Faso]]"
  - "[[Burundi]]"
  - "[[Cameroon]]"
  - "[[Canada]]"
  - "[[Chile]]"
  - "[[China]]"
  - "[[Colombia]]"
  - "[[Croatia]]"
  - "[[Côte d'Ivoire]]"
  - "[[Democratic Republic of the Congo]]"
  - "[[Denmark]]"
  - "[[Egypt]]"
  - "[[Equatorial Guinea]]"
  - "[[France]]"
  - "[[Gabon]]"
  - "[[Gambia]]"
  - "[[Germany]]"
  - "[[Ghana]]"
  - "[[Hong Kong]]"
  - "[[India]]"
  - "[[Indonesia]]"
  - "[[Israel]]"
  - "[[Italy]]"
  - "[[Jamaica]]"
  - "[[Japan]]"
  - "[[Jordan]]"
  - "[[Kazakhstan]]"
  - "[[Kenya]]"
  - "[[Laos]]"
  - "[[Lebanon]]"
  - "[[Libya]]"
  - "[[Luxembourg]]"
  - "[[Malawi]]"
  - "[[Malaysia]]"
  - "[[Mali]]"
  - "[[Mexico]]"
  - "[[Mongolia]]"
  - "[[Morocco]]"
  - "[[Mozambique]]"
  - "[[Myanmar]]"
  - "[[Namibia]]"
  - "[[Nepal]]"
  - "[[Netherlands]]"
  - "[[Nicaragua]]"
  - "[[Niger]]"
  - "[[Nigeria]]"
  - "[[North Korea]]"
  - "[[Pakistan]]"
  - "[[Palestine]]"
  - "[[Papua New Guinea]]"
  - "[[Paraguay]]"
  - "[[Peru]]"
  - "[[Philippines]]"
  - "[[Poland]]"
  - "[[Republic of the Congo]]"
  - "[[Russia]]"
  - "[[Rwanda]]"
  - "[[Saudi Arabia]]"
  - "[[Senegal]]"
  - "[[Singapore]]"
  - "[[Sint Maarten]]"
  - "[[Slovakia]]"
  - "[[South Africa]]"
  - "[[Spain]]"
  - "[[Sri Lanka]]"
  - "[[Sudan]]"
  - "[[Switzerland]]"
  - "[[Syria]]"
  - "[[Taiwan]]"
  - "[[Tajikistan]]"
  - "[[Tanzania]]"
  - "[[Thailand]]"
  - "[[Togo]]"
  - "[[Tunisia]]"
  - "[[Turkey]]"
  - "[[Turkmenistan]]"
  - "[[Uganda]]"
  - "[[Ukraine]]"
  - "[[United Arab Emirates]]"
  - "[[United Kingdom]]"
  - "[[United States]]"
  - "[[Uruguay]]"
  - "[[Uzbekistan]]"
  - "[[Vietnam]]"
  - "[[Zambia]]"
  - "[[Zimbabwe]]"
regions: ["[[North Africa]]", "[[Sub-Saharan Africa]]", "[[Middle East]]", "[[Central Asia]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "765 dishes; 5,982 community image-review rows"
size: "3.5 MB"
formats: [csv, xlsx, json]
has_ingredients: true
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [dish name (local + English), country name, ISO 639-3 language_code, ingredient name (free text)]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# World Wide Dishes

> [!abstract] TL;DR
> 765 home-cuisine dishes written by 201 community contributors (Oxford AI Society et al., FAccT 2025), each with the local
> dish name in one of 131 languages, the countries and sub-national regions/cultures that eat it, meal time, dish type,
> occasion (e.g. Ramadan, Eid), utensils, accompanying drink and a free-text **ingredient list**. It is Africa-heavy
> (501/765 dishes are tagged Africa) and thin on the Gulf and Central Asia (Saudi Arabia 2, UAE 1, Uzbekistan 2,
> Kazakhstan 2). Its value for the agent is authentic, non-web-scraped "what people actually cook at home" with
> ingredient lists and eating context; there are no amounts, recipes steps or nutrition.

## Access
| | |
|---|---|
| Availability | open-download (HF dataset, CC-BY-4.0, not gated) + GitHub code |
| Link | https://huggingface.co/datasets/WorldWideDishes/worldwidedishes-v1 |
| Accessed? | yes |
| How | `hf download WorldWideDishes/worldwidedishes-v1 --repo-type dataset` |
| Downloaded | `Data/world-wide-dishes/` — full repo: `data/*.csv`, `data/WorldWideDishes_2024_June.xlsx`, Croissant JSON, README, LICENCE (3.5 MB) |

## Tables & columns
### `data/WorldWideDishes_2024_June_World_Wide_Dishes.csv` (765 rows) — the dataset
Same content as the `World Wide Dishes` sheet of the xlsx. Meanings from the README/paper (App. B.2 metadata).

| column | type | meaning | example |
|---|---|---|---|
| `id` | int | dish id | 748 |
| `local_name` | str | dish name in the contributor's language/script | `Tli Tli B'djedj - تليتلي بالجاج` |
| `english_name` | str (73% filled) | English name or transliteration | `khdawej ala derbuz` |
| `language` / `language_code` | str | language(s) of the local name; ISO 639-3 codes | `Daridja arabic` / `ary` |
| `countries` | str, comma-separated | countries where the dish is eaten | `Algeria, Egypt, Lebanon, Palestine, Saudi Arabia, …` |
| `continent` | str | continent(s) | `Africa` |
| `regions` | str (65%) | sub-national regions | `East, Center` |
| `cultures` | str (38%) | ethnic/cultural group | `Touareg/ Ouargla` |
| `time_of_day` (+`_more`) | list-str | meal slot(s) | `['lunch', 'dinner']` |
| `type_of_dish` (+`_more`) | list-str | course / role | `['Main dish - eaten with sides', …]` |
| `utensils` | str (80%) | utensils used | `spoon, fork` |
| `drink` | str (34%) | drink served with it | `fermented milk` |
| `occasions` (+`_more`) | str | regular / special / both; festival names | `both` / `Yennayer, Ramadhan, Mouloud, Achoura` |
| `ingredients` | str, comma-separated | main ingredients, no quantities | `ghee, butter, chickpea, chicken, cinnamon, onions` |
| `recipe` | str (61%) | URL to a recipe (YouTube/blog) | `https://www.youtube.com/watch?v=…` |
| `more_details` | str (31%) | free-text cultural context | "This dish is eaten in Algeria during …" |
| `public_cc_image_url` / `_caption` | str | CC image link + caption | Openverse URL |
| `uploaded_image_name` / `_url` / `_caption` | str (9%) | contributor photo on Google Drive | `717.jpg` |

### `data/Community_Review_Generated_Dish_Images.csv` (5,982 rows × 38)
Community reviewers' ratings of text-to-image outputs (Stable Diffusion, DALL-E 2/3) for 181 dishes from 6 countries
(Nigeria, Cameroon, Algeria, South Africa, Kenya, United States): `Country`, `Rater_id`, `Dish name`, `Model`,
familiarity, "is this food / this dish", image quality 1–5, free-text explanation, and binary descriptor flags
(`Gross`, `Rotten`, `Unappetising`, `Disturbing`, …). Not useful for the agent except as evidence of model bias.

### `data/WorldWideDishes_2024_June_Selected_Countries.csv` (30 rows × 6) and `…_US_Test_Set.csv` (30 × 2)
30 dish names per country for the image-generation test suites (columns `Nigeria`, `Cameroon`, `Algeria`,
`South Africa`, `Kenya`, `the United States of America`); the US set adds a `Region` (e.g. `New England`).

### `data/countries_with_continent.csv` (331 rows × 6)
Lookup: `Name`, `Official Name`, `Association`, `Country Code` (ISO-2), `Continent Code`, `Continent Name`.

Sample: `Data/world-wide-dishes/sample.csv` · full profile: `Data/world-wide-dishes/schema.md`

## Countries & cultures covered
99 countries after normalising names (`countries` column split on commas; "United States of America (USA)" →
United States; England/Wales/"United Kingdom (UK)" → United Kingdom; Burma+Myanmar → Myanmar; Catalonia → Spain;
Zanzibar → Tanzania; West Papua → Indonesia; Sint Maarten and Hong Kong kept as their own entries). The paper counts
106 contributor countries and 131 languages. A dish can list several countries, so counts overlap (924 dish–country
pairs); *single-country dishes* are dishes tagged with only that country. By continent tag: Africa 501, Asia 152,
Europe 39, North America 32, South America 10, rest mixed.

**Top countries**

| rank | country | dishes | single-country dishes | priority region |
|---|---|---|---|---|
| 1 | [[Nigeria]] | 88 | 72 |  |
| 2 | [[Kenya]] | 85 | 71 |  |
| 3 | [[Algeria]] | 84 | 75 |  |
| 4 | [[South Africa]] | 81 | 78 |  |
| 5 | [[India]] | 62 | 55 | South Asia |
| 6 | [[Cameroon]] | 47 | 39 |  |
| 7 | [[Uganda]] | 40 | 36 |  |
| 8 | [[Philippines]] | 33 | 32 | Southeast Asia |
| 9 | [[United States]] | 30 | 24 |  |
| 10 | [[Sudan]] | 28 | 18 |  |
| 11 | [[Egypt]] | 24 | 13 | Middle East |
| 12 | [[Ghana]] | 23 | 19 |  |
| 13 | [[Japan]] | 23 | 23 | East Asia |
| 14 | [[Democratic Republic of the Congo]] | 21 | 15 |  |
| 15 | [[Indonesia]] | 19 | 12 | Southeast Asia |
| 16 | [[Tanzania]] | 11 | 0 |  |
| 17 | [[Brazil]] | 10 | 8 |  |
| 18 | [[Russia]] | 9 | 4 |  |
| 19 | [[Mexico]] | 8 | 7 |  |
| 20 | [[China]] | 8 | 6 | East Asia |
| 21 | [[United Kingdom]] | 8 | 7 |  |
| 22 | [[Lebanon]] | 7 | 0 | Middle East |
| 23 | [[Republic of the Congo]] | 7 | 0 |  |
| 24 | [[Morocco]] | 6 | 0 |  |
| 25 | [[Italy]] | 6 | 3 |  |

**Priority regions** (unlinked name = 0 dishes)

| region | country | dishes | single-country dishes | rank |
|---|---|---|---|---|
| Middle East | [[Saudi Arabia]] | 2 | 0 | 47 |
| Middle East | [[United Arab Emirates]] | 1 | 0 | 61 |
| Middle East | Qatar | 0 | 0 | – |
| Middle East | Kuwait | 0 | 0 | – |
| Middle East | Bahrain | 0 | 0 | – |
| Middle East | Oman | 0 | 0 | – |
| Middle East | [[Jordan]] | 3 | 0 | 42 |
| Middle East | [[Lebanon]] | 7 | 0 | 22 |
| Middle East | [[Syria]] | 5 | 0 | 28 |
| Middle East | [[Palestine]] | 4 | 0 | 35 |
| Middle East | [[Israel]] | 1 | 0 | 96 |
| Middle East | [[Turkey]] | 1 | 0 | 70 |
| Middle East | [[Egypt]] | 24 | 13 | 11 |
| Caucasus | [[Armenia]] | 1 | 1 | 62 |
| Central Asia | [[Kazakhstan]] | 2 | 0 | 58 |
| Central Asia | [[Uzbekistan]] | 2 | 0 | 56 |
| Central Asia | [[Tajikistan]] | 1 | 0 | 82 |
| Central Asia | Kyrgyzstan | 0 | 0 | – |
| Central Asia | [[Turkmenistan]] | 1 | 1 | 95 |
| South Asia | [[India]] | 62 | 55 | 5 |
| South Asia | [[Pakistan]] | 3 | 1 | 45 |
| South Asia | [[Bangladesh]] | 1 | 0 | 75 |
| South Asia | [[Sri Lanka]] | 2 | 0 | 60 |
| South Asia | [[Nepal]] | 1 | 1 | 73 |
| East Asia | [[China]] | 8 | 6 | 20 |
| East Asia | [[Japan]] | 23 | 23 | 13 |
| East Asia | [[North Korea]] | 2 | 0 | 55 |
| East Asia | [[Taiwan]] | 1 | 0 | 66 |
| East Asia | [[Mongolia]] | 1 | 0 | 83 |
| East Asia | [[Hong Kong]] | 1 | 1 | 71 |
| Southeast Asia | [[Indonesia]] | 19 | 12 | 15 |
| Southeast Asia | [[Malaysia]] | 5 | 0 | 31 |
| Southeast Asia | [[Singapore]] | 4 | 0 | 40 |
| Southeast Asia | [[Thailand]] | 1 | 0 | 93 |
| Southeast Asia | [[Vietnam]] | 1 | 1 | 97 |
| Southeast Asia | [[Philippines]] | 33 | 32 | 8 |
| Southeast Asia | [[Myanmar]] | 5 | 4 | 29 |
| Southeast Asia | [[Laos]] | 1 | 0 | 92 |
| Southeast Asia | [[Brunei]] | 1 | 0 | 86 |

Middle East coverage is mostly pan-Arab dishes (e.g. shawarma tagged Algeria, Egypt, Lebanon, Palestine, Saudi Arabia,
Sudan, Syria, UAE; `roz belkhalta` Saudi Arabia + Egypt). Sub-national `regions`/`cultures` fields add e.g. Algerian
regions (Miliana, Algiers), Touareg/Ouargla, Kabyle.

## Ingredients, amounts, cooking method
- **Ingredients:** every dish has an `ingredients` list (free text, comma-separated, mixed case, no normalisation):
  shawarma → `black pepper, onion, cayenne pepper, olive oil, lemon, cardamom, salt, paprika, beef, cumin, garlic,
  coriander, chicken`; Algerian dish → `chicken, tlitli, Chickpeas, cinamon` (spelling errors kept).
- **Amounts:** none.
- **Cooking method:** no steps; 61% of dishes link to an external `recipe` URL (not downloaded). `utensils` and
  `type_of_dish` give light preparation/serving context.
- **Nutrition:** none.
- **Eating context (useful for advice):** `time_of_day`, `occasions`/`occasions_more` (Ramadan, Eid, weddings,
  Yennayer…), `drink`.

## Linking to other datasets
- Dish names (local + English) can be fuzzy-matched to [[WorldCuisines]] (Wikipedia dish names, the paper's App. D.2
  compares the two) and [[FmLAMA]] (Wikidata dishes); >50% of WWD dishes are *not* in web-scraped sources, so
  expect low overlap.
- Free-text `ingredients` need normalising (lower-case, spelling) before joining to ingredient/compound resources
  (FooDB, USDA FDC) by name.
- `language_code` (ISO 639-3) and country names give country-level joins to the Countries notes.

## Versions
Only one release (`WorldWideDishes_2024_June`, HF repo created 2025-02-12). The GitHub repo
`oxai/world-wide-dishes` holds the same CSVs plus experiment code and the data-collection web app.

## Caveats
- Terms of use: meant for evaluating models; the authors prohibit using it to build prompt templates for
  generating training data.
- Small (765 dishes) and skewed to Africa and to the countries of the core team; Gulf and Central Asia have only
  1–2 dishes each, always multi-country.
- Community-written, uncurated text: spelling variants, mixed languages, ingredient names not standardised.
