---
title: "Our Regional Cuisines (Japan MAFF)"
slug: our-regional-cuisines-japan-maff
kind: [food]
version: "HF snapshot 2024-12-14 of MAFF うちの郷土料理 database (launched 2019)"
previous_versions: ""
papers: []
url: "https://www.maff.go.jp/j/keikaku/syokubunka/k_ryouri/index.html"
license: "Apache-2.0 on the HF mirror (third-party scrape); MAFF site content under the government website terms"
availability: open-download
access_link: "https://huggingface.co/datasets/JunichiroMorita/Our-Regional-Cuisines"
accessed: true
access_method: [huggingface]
access_date: 2026-09-30
access_notes: "MAFF itself has web pages only (JP + EN), no bulk file. A third party (Junichiro Morita) scraped them to Markdown and posted them on Hugging Face in Dec 2024. We downloaded both CSVs (7.7 MB) with curl and parsed the Markdown into columns. The English file lacks the prefecture field. MAFF may have added dishes after the snapshot (the Hokkaido page lists ~30 dish links vs 27 in the snapshot)."
countries: ["[[Japan]]"]
regions: ["[[East Asia]]"]
n_records: "1,355 dishes (Japanese); 885 dishes (English)"
size: "7.7 MB (2 CSV)"
formats: [csv, markdown-in-csv]
has_ingredients: true
has_amounts: yes
has_cooking_method: steps
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [dish name (JP/EN), prefecture]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
---
# Our Regional Cuisines (Japan MAFF)

> [!abstract] TL;DR
> The Japanese Ministry of Agriculture's **"うちの郷土料理" (Our Regional Cuisines)** database has **1,355 traditional regional dishes (~30 per prefecture, all 47 prefectures)**. Each dish comes with:
> - the local area where it is handed down,
> - main ingredients,
> - history and origin,
> - **when and on what occasions it is eaten** (seasons, festivals),
> - how it is eaten,
> - a recipe with amounts and steps.
>
> It is an authoritative, curated source of **cultural context** (occasions, seasonality, lore) for Japanese food, which the crowd recipe corpora lack. 885 dishes have official English translations.

## Access
| | |
|---|---|
| Availability | open-download (HF mirror of a MAFF website that is browse-only) |
| Link | HF: <https://huggingface.co/datasets/JunichiroMorita/Our-Regional-Cuisines> · source JP: <https://www.maff.go.jp/j/keikaku/syokubunka/k_ryouri/index.html> · EN: <https://www.maff.go.jp/e/policies/market/k_ryouri/index.html> |
| Accessed? | true (whole HF snapshot) |
| How | `curl -L …/resolve/main/our_regional_cuisines_{jpn,eng}.csv`, then parsed the Markdown into fields with a script |
| Downloaded | `Data/our-regional-cuisines-japan-maff/`: the 2 raw CSVs plus `parsed_jpn.csv` (1,355) and `parsed_eng.csv` (885) |

## Tables & columns
### `our_regional_cuisines_jpn.csv` / `our_regional_cuisines_eng.csv` (1,355 / 885 rows)
A single column, `text`: one Markdown page per dish, with a `# title`, `**field**: value` lines and `## section` blocks. The profiler's delimiter sniffing mis-reads these files (it shows `Unnamed: 0`); use the parsed files instead.

### `parsed_jpn.csv` (1,355 rows) and `parsed_eng.csv` (885 rows)
We parsed the Markdown into columns. The Japanese source headers are given in parentheses.

| column | type | meaning | example (JP / EN) |
|---|---|---|---|
| `row_id` | int | row index in the raw CSV | 0 |
| `dish_name` | str | dish name (郷土料理名 / Cuisine Name) | 豚丼 / Kasube no Nitsuke (Simmered Kasube) |
| `prefecture` (JP) / `region_field` (EN) | str | prefecture (都道府県). The EN file's field is always the constant "Our Regional Cuisines", so it has **no prefecture** | 北海道 |
| `lore_area` | str | main area where the dish is handed down (主な伝承地域 / Main Lore Areas) | 十勝地方 · Iburi, Hidaka, Kushiro, Tokachi |
| `main_ingredients` | str | main ingredients, comma-separated text (主な使用食材) | 豚肉、米、ねぎ |
| `history_origin` | str | history, origin, related events (歴史・由来・関連行事) | 明治時代末ごろから十勝地方では養豚業が… |
| `occasion_season` | str | occasions and seasons when eaten (食習の機会や時季 / Opportunities and Times of Eating Habits) | 1年を通して幅広い世代に食べられている |
| `how_eaten` | str | how it is prepared and eaten (飲食方法 / How to Eat) | 主に豚肉はロースやバラ肉を使う… |
| `preservation_efforts` | str | preservation and succession efforts (保存・継承の取組). Always "Not found" in the JP scrape; filled in EN | Not found |
| `recipe_provider` | str | recipe provider plus a dish image URL (レシピ提供元) | レシピ提供元名 : 北海道文教大学 山際睦子氏 ![料理画像](https://…) |
| `ingredients_with_amounts` | str | `- ingredient: amount` lines (材料). 1,340 / 1,355 JP dishes have a recipe | - 豚肉（ロース）: 150g - 長ねぎ: 1／4本 … |
| `servings` | str | yield from the 材料 header (JP only): 4人分 (4 servings) ×662, 2人分 ×71, 5人分 ×65 … | 4人分 |
| `steps` | str | numbered steps (作り方 / Recipe) | 1. 長ねぎを適当な長さに切り… |

Sample: `Data/our-regional-cuisines-japan-maff/sample.csv` · full profile: `Data/our-regional-cuisines-japan-maff/schema.md`

## Countries & cultures covered
**[[Japan]]**: 1,355 dishes across all 47 prefectures. Two records are malformed: one has prefecture "Not found" and one has "/ べろべろ 石川県".

Per prefecture (JP file):
- **Hokkaido/Tohoku:** Hokkaido 27 · Aomori 29 · Iwate 30 · Miyagi 29 · Akita 28 · Yamagata 29 · Fukushima 30
- **Kanto:** Ibaraki 30 · Tochigi 28 · Gunma 27 · Saitama 29 · Chiba 28 · Tokyo 30 · Kanagawa 19
- **Chubu:** Niigata 30 · Toyama 30 · Ishikawa 29 · Fukui 29 · Yamanashi 30 · Nagano 29 · Gifu 30 · Shizuoka 28 · Aichi 30
- **Kinki:** Mie 30 · Shiga 30 · Kyoto 30 · Osaka 29 · Hyogo 28 · Nara 30 · Wakayama 27
- **Chugoku/Shikoku:** Tottori 27 · Shimane 28 · Okayama 28 · Hiroshima 30 · Yamaguchi 30 · Tokushima 30 · Kagawa 30 · Ehime 25 · Kochi 29
- **Kyushu/Okinawa:** Fukuoka 30 · Saga 25 · Nagasaki 30 · Kumamoto 29 · Oita 30 · Miyazaki 30 · Kagoshima 30 · Okinawa 30

The Okinawan (Ryukyu) dishes are notable for health advice because they are distinct from mainland cuisine: 中身汁 (pork-offal soup), クーブイリチー (stir-fried kelp with pork belly), イナムドゥチ (pork miso soup). Ainu influence is mentioned in Hokkaido entries.

## Ingredients, amounts, cooking method
- **Ingredients and amounts:** yes. Each line is `ingredient: amount` with Japanese units (g, カップ, 大さじ/小さじ, 本, 枚) and servings. For example, クーブイリチー (4人分) uses 昆布 40g, 豚三枚肉 60g, こんにゃく 40g, かまぼこ 30g, 揚げ豆腐 30g, 豚だし 2カップ, sugar, mirin, sake, soy sauce.
- **Cooking method:** numbered steps. In the EN steps the numbers are duplicated ("1. 1. …").
- **Nutrition:** none. It can be computed via [[Standard Tables of Food Composition in Japan]], since ingredient names are standard Japanese.
- **Cultural context** is the unique value here. `occasion_season` states festival, seasonal and ceremonial use (e.g. winter dish, New Year, snack with sake), and `history_origin` gives lore.

## Linking to other datasets
- Ingredient names → [[Standard Tables of Food Composition in Japan]] (`food_name_ja`) for per-recipe nutrient estimates.
- Dish names → [[NII Cookpad Dataset]] titles, to find home variants and how popular each dish is.
- JP↔EN: no shared id. Match by order within a prefecture or by the romanised dish name in the EN title.

## Versions
MAFF launched the site in 2019 and keeps adding dishes. The HF snapshot is from 2024-12-14. No versioned releases exist, so re-scraping MAFF would give the latest set.

## Caveats
- This is a third-party scrape. The Apache-2.0 licence on HF is the uploader's claim; MAFF's own terms apply to the content.
- The EN file has 885 of 1,355 dishes and no prefecture.
- The `preservation_efforts` section is missing in the JP scrape.
- Curated "traditional" dishes are not what people eat daily; pair it with Cookpad for everyday food.
