---
title: "XiaChuFang Recipe Corpus"
slug: xiachufang-recipe-corpus
kind: [food]
version: "Full Recipe Corpus (recipes published before Dec 2020; released 2022)"
previous_versions: ""
papers: ["[[Liu2022 - Counterfactual recipe generation]]"]
url: "https://counterfactual-recipe-generation.github.io/dataset_en.html"
license: "MIT (HF mirror card); recipes © XiaChuFang users, collected under xiachufang.com/principle, non-commercial research use per paper"
availability: open-download
access_link: "https://huggingface.co/datasets/xzm1999/XiaChuFang_Recipe_Corpus"
accessed: partial
access_method: [huggingface]
access_date: 2026-09-30
access_notes: "Full corpus is a single 2.0 GB JSON-lines file (recipe_corpus_full.json). Official links are Google Drive; we used the Hugging Face mirror (xzm1999/XiaChuFang_Recipe_Corpus) and an HTTP range request for the first 80 MB, i.e. the first 64,742 of 1,520,327 recipes (4.3%). The file order is not documented, so the subset may not be a random sample."
countries: ["[[China]]"]
regions: ["[[East Asia]]"]
n_records: "1,520,327 recipes (full corpus); 1,479,764 in the finetuning corpus; 64,742 downloaded"
size: "2.0 GB JSONL (full); 84 MB downloaded"
formats: [jsonl]
has_ingredients: true
has_amounts: partial
has_cooking_method: steps
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [dish name (Chinese), ingredient strings (Chinese)]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
---
# XiaChuFang Recipe Corpus

> [!abstract] TL;DR
> 1.52M user-written **Chinese home-cooking recipes** from 下厨房 (xiachufang.com), published before Dec 2020. Each record has a title, a dish label (1.24M recipes mapped to 30,060 canonical dishes), a free-text ingredient list with amounts, ordered steps and site keywords. Liu et al. (EMNLP 2022, Peking University) collected it for counterfactual recipe generation. It is the largest open corpus of everyday Chinese cooking, so it is the main Q1 source for what people in China cook and how. It has no nutrition data and no province labels.

## Access
| | |
|---|---|
| Availability | open-download (Google Drive links on the project page; HF mirror) |
| Link | <https://counterfactual-recipe-generation.github.io/dataset_en.html> · HF: <https://huggingface.co/datasets/xzm1999/XiaChuFang_Recipe_Corpus> · code: <https://github.com/xxxiaol/counterfactual-recipe-generation> |
| Accessed? | partial |
| How | `curl -r 0-83886079` on `…/resolve/main/recipe_corpus_full.json` (HF mirror), then dropped the last partial line |
| Downloaded | `Data/xiachufang-recipe-corpus/recipe_corpus_full_first80MB.jsonl`: first 64,742 recipes, 84 MB |

There are two official downloads, both 1.9–2.0 GB Google Drive files: the **Full Recipe Corpus** (1,520,327 recipes) and the **Finetuning Recipe Corpus** (1,479,764 recipes, which leaves out the 50 evaluation dish pairs). To get the rest, run `curl -L` on the HF URL without `-r`.

## Tables & columns
### `recipe_corpus_full_first80MB.jsonl` (64,742 rows downloaded; 1,520,327 in full)
One JSON object per line. Column meanings come from the project page.

| column | type | meaning | example |
|---|---|---|---|
| `name` | str | recipe title as written by the author | 西班牙金枪鱼沙拉 |
| `dish` | str | canonical dish from XiaChuFang's dish list; `Unknown` if the title didn't map (12,686 / 64,742 = 20% in our subset) | 金枪鱼沙拉 |
| `description` | str | author's free-text intro (often empty) | 每到桂花香满城后，就可以吃羊肉温补身体了 |
| `recipeIngredient` | list[str] | ingredient lines; amount and ingredient are fused in one string | `['1kg羊肉', '5片姜', '3瓣蒜', '适量花椒', …]` |
| `recipeInstructions` | list[str] | ordered cooking steps (mean 6.7 steps per recipe in the subset) | `['滩羊肉在姜水里焯3分钟…', …]` |
| `author` | str | anonymised author id | author_67696 |
| `keywords` | list[str] | XiaChuFang search keywords: templated "X的做法" strings plus site tags (家常菜, 早餐, 减肥, 汤羹…) | `['…的做法', '沙拉']` |

Sample: `Data/xiachufang-recipe-corpus/sample.csv` · full profile: `Data/xiachufang-recipe-corpus/schema.md`

## Countries & cultures covered
- **[[China]]**: all 1,520,327 recipes (64,742 in our subset). These are Chinese-language recipes from a mainland Chinese platform. There is no province or user-location field.
- Regional-cuisine tags in the subset's `keywords` are rare: 粤菜 (Cantonese) 88, 川菜 (Sichuan) 75, 湘菜 (Hunan) 9, 东北菜 (Northeastern) 9, 新疆菜 (Xinjiang) 5, 云南菜 (Yunnan) 3. Sub-national cuisine therefore has to be inferred from dish names such as 担担面 or 手抓饭.
- Foreign-style tags appear too, but they describe Chinese home adaptations, not data from those countries: 日式 (Japanese style) 440, 西式 (Western style) 379, 韩式 (Korean style) 319, 西餐 99, 泰国菜 9.
- Health-flavoured tags matter for the agent: 减肥 (weight loss) 1,121, 婴幼儿 (infants) 511, 宝宝辅食 (baby food) 108, 健康 68, 养生 (TCM-style nourishing) 38, 孕妇 (pregnancy) 9, 糖尿病 (diabetes) 2.

## Ingredients, amounts, cooking method
- **Ingredients:** yes. The subset has 466,082 ingredient lines, 7.2 per recipe.
- **Amounts:** partial. 81% of lines contain a number or a vague quantity word such as 适量 ("to taste") or 少许 ("a little"). Amounts are unstructured and fused with the ingredient ("1kg羊肉", "3勺老抽", "1000ml（消耗量25ml）色拉油"), so the agent needs a Chinese quantity/unit parser (克, 勺, 片, 个, 适量).
- **Cooking method:** full ordered steps. Method words (蒸 steam, 红烧 red-braise, 煎 pan-fry, 炖 stew) also appear as keyword tags.
- **Nutrition:** none. It could be estimated by mapping ingredients to the China Food Composition Tables (if added to the vault) or to USDA via translation.
- Example: 红烧滩羊肉 (red-braised Tan lamb) has ingredients 1kg羊肉, 5片姜, 3瓣蒜, 适量花椒, 3勺老抽, 3片香叶, 2个八角, 1块桂皮…, 8 steps, and a description noting lamb is eaten in autumn "to warm and tonify the body" (温补身体). That is a traditional-medicine food belief, and exactly the cultural signal the agent needs.

## Linking to other datasets
- No ids. Joins are text-based, on Chinese dish names and ingredient strings after stripping amounts.
- Ingredient strings → a Chinese/English food composition table or [[FooDB]], after translation. Dish names → Chinese dish lists in other food datasets.
- The paper's evaluation set (50 dish pairs with pivot-action annotations) is in the GitHub repo.

## Versions
Only one release (2022). The Finetuning corpus is the Full corpus minus the recipes of the 50 evaluation dish pairs, so it is a subset, not a new version. The paper reports 1,550,151 collected recipes; the released full corpus has 1,520,327.

## Caveats
- User-generated content: amounts are inconsistent and some recipes are very long (up to 62,722 characters).
- 20% of recipes have `dish = Unknown`.
- Heavy skew toward baking and desserts (蛋糕, 面包, 烘焙 are among the top tags), which over-represents urban, young, female users of the platform.
- Our 64,742-recipe subset is the file head, not a random sample.
- Recipes were collected with permission under the site principle; the paper states no commercial use.
