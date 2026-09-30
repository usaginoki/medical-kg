---
title: "FmLAMA"
slug: fmlama
kind: [food]
version: "GitHub main (last push 2025-02-12; NAACL 2025 camera-ready)"
previous_versions: ""
papers: ["[[Zhou2024 - Does Mapo Tofu Contain Coffee]]"]
url: "https://github.com/lizhou21/FmLAMA-master"
license: "none stated in the repo (data derived from Wikidata, CC0)"
availability: open-download
access_link: "https://github.com/lizhou21/FmLAMA-master/tree/main/data"
accessed: true
access_method: [github]
access_date: 2026-09-30
access_notes: "The repo is ~500 MB because of probing outputs; only the data files were fetched with curl from raw.githubusercontent.com (Dishes.csv = the full FmLAMA, Dish_Count.json, country_info.json, ingredient_info_English.json, the English filtered sub-dataset and English templates). Other-language filtered sub-datasets (ar, he, ko, ru, zh) and results/ were not downloaded. No licence file in the repo."
countries:
  - "[[Afghanistan]]"
  - "[[Albania]]"
  - "[[Algeria]]"
  - "[[Argentina]]"
  - "[[Armenia]]"
  - "[[Australia]]"
  - "[[Austria]]"
  - "[[Azerbaijan]]"
  - "[[Bahrain]]"
  - "[[Bangladesh]]"
  - "[[Belarus]]"
  - "[[Belgium]]"
  - "[[Bhutan]]"
  - "[[Bolivia]]"
  - "[[Botswana]]"
  - "[[Brazil]]"
  - "[[Brunei]]"
  - "[[Bulgaria]]"
  - "[[Cambodia]]"
  - "[[Cameroon]]"
  - "[[Canada]]"
  - "[[Cape Verde]]"
  - "[[Chile]]"
  - "[[China]]"
  - "[[Colombia]]"
  - "[[Costa Rica]]"
  - "[[Croatia]]"
  - "[[Cuba]]"
  - "[[Cyprus]]"
  - "[[Czech Republic]]"
  - "[[Côte d'Ivoire]]"
  - "[[Denmark]]"
  - "[[Dominican Republic]]"
  - "[[Ecuador]]"
  - "[[Egypt]]"
  - "[[El Salvador]]"
  - "[[Eritrea]]"
  - "[[Estonia]]"
  - "[[Ethiopia]]"
  - "[[Fiji]]"
  - "[[Finland]]"
  - "[[France]]"
  - "[[Germany]]"
  - "[[Ghana]]"
  - "[[Greece]]"
  - "[[Guatemala]]"
  - "[[Guinea]]"
  - "[[Haiti]]"
  - "[[Honduras]]"
  - "[[Hungary]]"
  - "[[India]]"
  - "[[Indonesia]]"
  - "[[Iran]]"
  - "[[Iraq]]"
  - "[[Ireland]]"
  - "[[Israel]]"
  - "[[Italy]]"
  - "[[Jamaica]]"
  - "[[Japan]]"
  - "[[Jordan]]"
  - "[[Kazakhstan]]"
  - "[[Kyrgyzstan]]"
  - "[[Laos]]"
  - "[[Latvia]]"
  - "[[Lebanon]]"
  - "[[Libya]]"
  - "[[Lithuania]]"
  - "[[Malaysia]]"
  - "[[Maldives]]"
  - "[[Mali]]"
  - "[[Malta]]"
  - "[[Mexico]]"
  - "[[Mongolia]]"
  - "[[Morocco]]"
  - "[[Mozambique]]"
  - "[[Myanmar]]"
  - "[[Nepal]]"
  - "[[Netherlands]]"
  - "[[New Zealand]]"
  - "[[Nicaragua]]"
  - "[[Nigeria]]"
  - "[[North Korea]]"
  - "[[Norway]]"
  - "[[Pakistan]]"
  - "[[Palau]]"
  - "[[Paraguay]]"
  - "[[Peru]]"
  - "[[Philippines]]"
  - "[[Poland]]"
  - "[[Portugal]]"
  - "[[Romania]]"
  - "[[Russia]]"
  - "[[Saudi Arabia]]"
  - "[[Senegal]]"
  - "[[Singapore]]"
  - "[[Slovakia]]"
  - "[[Slovenia]]"
  - "[[Somalia]]"
  - "[[South Africa]]"
  - "[[South Korea]]"
  - "[[Spain]]"
  - "[[Sri Lanka]]"
  - "[[Sweden]]"
  - "[[Switzerland]]"
  - "[[Syria]]"
  - "[[São Tomé and Príncipe]]"
  - "[[Tajikistan]]"
  - "[[Tanzania]]"
  - "[[Thailand]]"
  - "[[Togo]]"
  - "[[Trinidad and Tobago]]"
  - "[[Tunisia]]"
  - "[[Turkey]]"
  - "[[Turkmenistan]]"
  - "[[Uganda]]"
  - "[[United Kingdom]]"
  - "[[United States]]"
  - "[[Uruguay]]"
  - "[[Uzbekistan]]"
  - "[[Venezuela]]"
  - "[[Vietnam]]"
  - "[[Yemen]]"
regions: ["[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[Central Asia]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "33,600 dish×language rows = 2,818 unique Wikidata dishes; 873 English ingredients"
size: "7.2 MB downloaded"
formats: [csv, json, jsonl]
has_ingredients: true
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [Wikidata QID (dish), dish name (248 languages), ingredient label (Wikidata has-part), country of origin]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# FmLAMA

> [!abstract] TL;DR
> FmLAMA (Zhou et al., NAACL 2025) is a SPARQL dump of Wikidata food items that have a **country of origin** and a
> **has part(s)** (ingredient) statement: 2,818 dishes (Wikidata QIDs) from 122 countries, each repeated for every
> language that has a label (33,600 rows, 248 languages), with ingredient labels in that language, optional "made
> from material" and Commons images. It was built to probe LLMs for dish→ingredient knowledge. For the agent it is a
> multilingual **dish → origin country → ingredients** graph keyed on Wikidata, strong for Turkey (105 dishes),
> India, Japan, China, Indonesia, but with only 1–7 dishes per Gulf and Central Asian country and a mean of ~2
> ingredients per dish (main ingredients only).

## Access
| | |
|---|---|
| Availability | open-download (public GitHub repo, no licence file) |
| Link | https://github.com/lizhou21/FmLAMA-master |
| Accessed? | yes (all dataset files; experiment outputs skipped) |
| How | `curl -L https://raw.githubusercontent.com/lizhou21/FmLAMA-master/main/<file>` |
| Downloaded | `Data/fmlama/data/`: `Dishes.csv` (33,600 rows, 7.4 MB), `Dish_Count.json`, `country_info.json`, `ingredient_info_English.json`, `data_filter/en/*`, `templates/en_templates.jsonl`; `README.md` |

## Tables & columns
### `data/Dishes.csv` (33,600 rows × 8) — FmLAMA
One row per (dish, language). Meanings from the paper §3 (Wikidata properties) and inspection.

| column | type | meaning | example |
|---|---|---|---|
| `url` | str | Wikidata entity URI of the dish (QID) | `http://www.wikidata.org/entity/Q396184` |
| `origin` | str | country of origin (Wikidata P495), English label | `Canada` |
| `origin_name` | str | country label in the row's language | `캐나다` |
| `name` | str | dish label in `lang` | `Poutine` / `푸틴` |
| `lang` | str | Wikidata label language code (248 values; en 2,804 rows, es 1,599, fr 1,582, ja 1,580) | `ko` |
| `hasParts` | str (Python set literal) | ingredients from "has part(s)" (P527), labels in `lang`, comma-joined; never empty | `{'cheese curds, gravy, french fries'}` |
| `materia` | str (set literal) | "made from material" (P186); `{''}` when absent (79% of rows) | `{'chicken meat'}` |
| `image` | str (list literal) | Wikimedia Commons image URLs (96% of rows non-empty) | `['http://commons.wikimedia.org/wiki/Special:FilePath/Poutine.JPG']` |

### `data/ingredient_info_English.json` (873 rows)
Per English ingredient label (`_key`): `count` (dishes in the English sub-dataset using it), `origin` (list of origin
countries of those dishes), `continent`. E.g. `rice` 71 dishes; `pomegranate` → Iran.

### `data/Dish_Count.json` (211 rows) and `data/country_info.json` (202 rows)
`Dish_Count`: rows per origin (incl. historical states with 0, e.g. `Principality of Chernigov`); matches the
dish×language row counts in the table below. `country_info`: origin → continent (8 values).

### `data/data_filter/en/en_dishes.jsonl` (175 rows) + `en_count.jsonl` (41 rows)
The paper's filtered English probing subset: dishes whose subject and ingredient labels exist in all six probing
languages (en, zh, ar, ko, ru, he). Columns `url`, `origin`, `origin_name`, `lang`, `sub_label` (dish),
`obj_label` (list of ingredients).

### `data/templates/en_templates.jsonl` (10 rows)
Probing templates, e.g. `[X] is a dish made with [Y].` and the country-context variant `In [C], [X] is a dish made
with [Y].` (`relation`, `template`, `avg`).

Sample: `Data/fmlama/sample.csv` · full profile: `Data/fmlama/schema.md`

## Countries & cultures covered
122 countries after normalising `origin` (England/Scotland/Wales/Northern Ireland → United Kingdom;
People's Republic of China → China; United States of America → United States; Republic of Ireland → Ireland;
Catalonia → Spain; Ivory Coast → Côte d'Ivoire; Cape Verde and Palau kept). The raw `origin` column has 127 values
(the paper says 128 cultural groups). 72 dishes have more than one origin. Counts are unique dish QIDs per country;
the second column is rows (dish × language), which is what `Dish_Count.json` and the paper's Fig. 7 count
(e.g. Italy 2,975 rows).

**Top countries**

| rank | country | unique dishes (QIDs) | rows (dish × language) | priority region |
|---|---|---|---|---|
| 1 | [[United States]] | 285 | 2674 |  |
| 2 | [[Italy]] | 258 | 2975 |  |
| 3 | [[France]] | 199 | 2857 |  |
| 4 | [[Japan]] | 189 | 2335 | East Asia |
| 5 | [[India]] | 149 | 1486 | South Asia |
| 6 | [[United Kingdom]] | 133 | 1759 |  |
| 7 | [[Spain]] | 124 | 1159 |  |
| 8 | [[Indonesia]] | 113 | 981 | Southeast Asia |
| 9 | [[Turkey]] | 105 | 1203 | Middle East |
| 10 | [[China]] | 103 | 1271 | East Asia |
| 11 | [[Germany]] | 70 | 909 |  |
| 12 | [[Mexico]] | 61 | 752 |  |
| 13 | [[Russia]] | 57 | 872 |  |
| 14 | [[Philippines]] | 55 | 416 | Southeast Asia |
| 15 | [[Portugal]] | 54 | 552 |  |
| 16 | [[Vietnam]] | 44 | 394 | Southeast Asia |
| 17 | [[Peru]] | 44 | 421 |  |
| 18 | [[Nigeria]] | 43 | 186 |  |
| 19 | [[Poland]] | 38 | 588 |  |
| 20 | [[Thailand]] | 32 | 352 | Southeast Asia |
| 21 | [[Sweden]] | 30 | 301 |  |
| 22 | [[Netherlands]] | 28 | 370 |  |
| 23 | [[Austria]] | 27 | 459 |  |
| 24 | [[Hungary]] | 24 | 343 |  |
| 25 | [[Iran]] | 22 | 322 | Middle East |
| 26 | [[Belgium]] | 22 | 328 |  |
| 27 | [[Greece]] | 22 | 381 |  |
| 28 | [[Switzerland]] | 21 | 322 |  |
| 29 | [[Brazil]] | 21 | 249 |  |
| 30 | [[Bangladesh]] | 20 | 142 | South Asia |

**Priority regions** (unlinked name = 0 dishes)

| region | country | unique dishes (QIDs) | rows (dish × language) | rank |
|---|---|---|---|---|
| Middle East | [[Saudi Arabia]] | 4 | 12 | 81 |
| Middle East | United Arab Emirates | 0 | 0 | – |
| Middle East | Qatar | 0 | 0 | – |
| Middle East | Kuwait | 0 | 0 | – |
| Middle East | [[Bahrain]] | 1 | 34 | 117 |
| Middle East | Oman | 0 | 0 | – |
| Middle East | [[Yemen]] | 2 | 11 | 101 |
| Middle East | [[Iraq]] | 2 | 7 | 100 |
| Middle East | [[Iran]] | 22 | 322 | 25 |
| Middle East | [[Jordan]] | 4 | 43 | 80 |
| Middle East | [[Lebanon]] | 7 | 116 | 63 |
| Middle East | [[Syria]] | 5 | 106 | 74 |
| Middle East | [[Israel]] | 10 | 63 | 47 |
| Middle East | [[Turkey]] | 105 | 1203 | 9 |
| Middle East | [[Cyprus]] | 6 | 20 | 72 |
| Middle East | [[Egypt]] | 4 | 66 | 85 |
| Caucasus | [[Azerbaijan]] | 9 | 79 | 52 |
| Caucasus | [[Armenia]] | 9 | 178 | 54 |
| Central Asia | [[Kazakhstan]] | 5 | 94 | 77 |
| Central Asia | [[Uzbekistan]] | 5 | 96 | 79 |
| Central Asia | [[Tajikistan]] | 5 | 46 | 75 |
| Central Asia | [[Kyrgyzstan]] | 7 | 125 | 62 |
| Central Asia | [[Turkmenistan]] | 3 | 57 | 95 |
| South Asia | [[India]] | 149 | 1486 | 5 |
| South Asia | [[Pakistan]] | 4 | 61 | 83 |
| South Asia | [[Bangladesh]] | 20 | 142 | 30 |
| South Asia | [[Sri Lanka]] | 8 | 52 | 58 |
| South Asia | [[Nepal]] | 4 | 49 | 82 |
| South Asia | [[Bhutan]] | 4 | 26 | 87 |
| South Asia | [[Maldives]] | 6 | 45 | 69 |
| South Asia | [[Afghanistan]] | 4 | 62 | 86 |
| East Asia | [[China]] | 103 | 1271 | 10 |
| East Asia | [[Japan]] | 189 | 2335 | 4 |
| East Asia | [[South Korea]] | 12 | 86 | 42 |
| East Asia | [[North Korea]] | 3 | 46 | 97 |
| East Asia | [[Mongolia]] | 3 | 44 | 98 |
| Southeast Asia | [[Indonesia]] | 113 | 981 | 8 |
| Southeast Asia | [[Malaysia]] | 17 | 131 | 35 |
| Southeast Asia | [[Singapore]] | 9 | 64 | 53 |
| Southeast Asia | [[Thailand]] | 32 | 352 | 20 |
| Southeast Asia | [[Vietnam]] | 44 | 394 | 16 |
| Southeast Asia | [[Philippines]] | 55 | 416 | 14 |
| Southeast Asia | [[Myanmar]] | 3 | 37 | 94 |
| Southeast Asia | [[Laos]] | 6 | 102 | 68 |
| Southeast Asia | [[Cambodia]] | 12 | 93 | 45 |
| Southeast Asia | [[Brunei]] | 1 | 25 | 110 |

No dish in FmLAMA has UAE, Qatar, Kuwait or Oman as origin; Saudi Arabia has 4 (e.g. `kleicha` → cardamom,
`Qassami Tawa` → water, sugar, table salt, flour, whole-wheat flour).

## Ingredients, amounts, cooking method
- **Ingredients:** yes, from Wikidata "has part(s)", in every row's language. English rows have 1–22 ingredients,
  mean 2.1, median 1 (the paper: 18,546 of the 33,600 dish instances have a single ingredient). Examples (English):
  `hasip` (Uzbekistan) → rice, Piper nigrum, tail fat, cumin seed, mutton, onion, liver; `baba ghanoush` (Lebanon) →
  tahini, eggplant; `Fesenjān` (Iran) → pomegranate juice; `sorshe ilish` (India) → mustard, table salt, mustard oil,
  Tenualosa ilisha. Wikidata labels sometimes use scientific names (`Piper nigrum`, `Tenualosa ilisha`).
- **Amounts, cooking method, nutrition:** none.

## Linking to other datasets
- **Wikidata QID** (`url`) is the key: Wikidata ingredient items carry links to FooDB/USDA/ChEBI/PubChem-type ids for
  many foods, so FmLAMA ingredients can be resolved to compound resources via Wikidata (not done here).
- Dish QIDs ↔ English Wikipedia titles ↔ [[WorldCuisines]] `Name` (join via the Wikipedia/Wikidata API).
- Dish names can be fuzzy-matched to [[World Wide Dishes]].

## Versions
Single release in the GitHub repo (arXiv v1 April 2024 → NAACL 2025 version Feb 2025). No HF mirror found.

## Caveats
- Wikidata-derived: incomplete ingredient lists (paper: "soy sauce chicken" lists only chicken meat), generic labels
  (`oil`, `meat`, `fish as food`), and origin = where Wikidata says it comes from, not where it is eaten.
- Heavily Western/East-Asian skewed; Gulf and Central Asia nearly absent.
- No licence file; Wikidata content itself is CC0.
