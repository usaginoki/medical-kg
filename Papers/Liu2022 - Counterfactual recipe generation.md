---
title: "Counterfactual Recipe Generation: Exploring Compositional Generalization in a Realistic Scenario"
citekey: "Liu2022"
authors: ["Xiao Liu", "Yansong Feng", "Jizhi Tang", "Chengang Hu", "Dongyan Zhao"]
year: 2022
published: 2022-10-20
venue: "EMNLP 2022 (main), pp. 7354–7370"
peer_reviewed: true
url: "https://aclanthology.org/2022.emnlp-main.497/"
arxiv: "2210.11431"
doi: "10.18653/v1/2022.emnlp-main.497"
pdf: ""
pdf_url: "https://arxiv.org/pdf/2210.11431"
datasets: ["[[XiaChuFang Recipe Corpus]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites:
  - "[[Majumder2019 - Personalized recipe generation]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
---
# Counterfactual Recipe Generation: Exploring Compositional Generalization in a Realistic Scenario

> [!abstract] TL;DR
> Liu et al. (Peking University / Baidu) scraped **~1.5M Chinese recipes from xiachufang.com** into the XiaChuFang corpus. They use it to test whether pretrained LMs can rewrite a recipe when one main ingredient changes, e.g. red-braised pork → red-braised crucian carp. Models fine-tuned on the corpus write fluent recipes but rarely make the ingredient-specific action changes, which shows they do not really compose culinary knowledge.

## What was built
- **Dataset(s):** [[XiaChuFang Recipe Corpus]]
- **Sources & construction:** recipes published on 下厨房 (XiaChuFang) before Dec 2020, collected "with permission of licence" under the site's principles. Recipe titles were mapped to the site's list of canonical dishes.
- **Size & coverage:**
  - 1,550,151 recipes collected. The released full corpus has 1,520,327.
  - 1,242,206 recipes map to 30,060 dishes, 41.3 recipes per dish on average.
  - Mean recipe length is 224 characters.
  - All Chinese.
- **Evaluation / applications:**
  - 50 base→target dish pairs × 50 base recipes = 2,500 test instances.
  - Pivot actions (actions to remove or insert) were mined from action frequencies across each dish's recipes and verified by annotators with culinary experience.
  - A 1,479,764-recipe fine-tuning corpus excludes the test dishes.
  - Baselines: GPT-2 fine-tuned on the corpus, and the unsupervised counterfactual generators DeLorean and EDUCAT.

## Key findings
1. With 1.5M recipes, XiaChuFang is 1.5× the size of the English Recipe1M+.
2. A dish pair has 22.4 pivot actions on average: 13.6 to remove and 8.8 to insert.
3. All models reach ≤ 20% hard F1 and ≤ 30% soft F1 on action-level changes. Inserting needed actions is harder than removing inappropriate ones.
4. Models fail to keep the base recipe's style: BLEU to the base recipe is < 5% for GPT-2 and DeLorean, against 65.2% for human expert rewrites. In best–worst scaling, experts score 75.6 / 82.5 / 77.8 for grammar / correctness / preservation, far above every model.
5. In GPT-2 (D), 99% of inserted pivot actions are in a valid position. The figure drops to 80–87% for rewrite-based methods.

## Relevance to research questions
### Q1: Cultural food datasets
- This is the main open large-scale source of **everyday Chinese home cooking**: dish names, ingredient lists with amounts, and steps.
- The dish↔recipe grouping (41 recipes per dish) lets the agent learn what is "typical" in a Chinese dish and what varies, e.g. which ingredients can be swapped.
- Useful when adapting advice to Chinese users, e.g. suggesting a lower-sodium variant of a dish.
- Has no nutrition and no province labels.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- Only common Chinese dishes are covered; the authors note the task may not generalise to other languages.
- The data is user-generated and noisy (amounts, style).
- Action parsing is coarse (dependency-based, verb-centred).
- No regional or nutritional metadata.
- Non-commercial use only.

## Related work to follow
![[Backlog.base#Cited by this paper]]
