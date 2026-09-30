---
title: "Digital Mapping of Central Asian Foods: Towards a Standardized Visual Atlas for Nutritional Research"
citekey: "Omarova2025"
authors: ["Zhuldyz Omarova", "Bibinur Nurmanova", "Aibota Sanatbyek", "Huseyin Atakan Varol", "Mei-Yen Chan"]
year: 2025
published: 2025-10-22
venue: "Nutrients"
peer_reviewed: true
url: "https://doi.org/10.3390/nu17213315"
arxiv: ""
doi: "10.3390/nu17213315"
pdf: ""
pdf_url: "https://www.mdpi.com/2072-6643/17/21/3315/pdf?version=1761142579"
datasets: ["[[Central Asian Digital Visual Food Atlas]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - kind/food
  - region/central-asia
---
# Digital Mapping of Central Asian Foods: Towards a Standardized Visual Atlas for Nutritional Research

> [!abstract] TL;DR
> This is the first digital visual food atlas for Central Asia. It has 115 items: 95 foods photographed at small, average and large portions with measured weights, and 20 beverage guide photos. The items were chosen from the CAFD/CAFSD class lists and cover Kazakhstan, Uzbekistan, Kyrgyzstan, Tajikistan and Turkmenistan. Local names are given in Kazakh, Uzbek, Kyrgyz, Tajik and Turkmen. It gives portion weights but no nutrient values yet.

## What was built
- **Dataset(s):** [[Central Asian Digital Visual Food Atlas]]
- **Sources & construction:** Foods were selected from [[Central Asian Food Dataset]] (CAFD, 42 classes) and CAFSD (239 classes). Ready-to-eat items were excluded. All photos are new: an iPhone 13 at a 60° angle with two softboxes, on a standard tray with plate, cutlery, ruler and napkin, and 8 types of household tableware. Portions were pre-weighed to ±0.1 g. The average portion is the baseline (1.0), with small = 0.5× and large = 1.5×, based on commonly sold and food-service portions. The layout was made in Canva.
- **Size & coverage:** 115 items in 9 sections: main dishes (about 20), soups (about 12), meat dishes, salads, snacks, bakery & bread, side dishes, beverages and desserts. About 30 items contain meat, and 12 are meat-based dishes. Table 2 gives each item's name in English plus Kaz/Uzb/Kir/Tgk/Tuk names and a short description (for example pilaf = Palau/Osh/Paloo/Oshi palav/Palaw). Traditional dishes (plov, beshbarmak, lagman, naryn, kuyrdak, orama, kazan kebab, shorpa, kespe, manpar) sit alongside international ones (pizza, burger, udon, ramen, Caesar salad).
- **Evaluation / applications:** The atlas is descriptive and was not validated with users. The intended uses are 24-hour recalls and FFQs, portion guides in apps, training data for AI portion estimation, and nutrition education.

## Key findings
1. The atlas has 115 items: 95 photo series with three portions each and 20 beverage guides.
2. Each portion carries its exact weight. For example, pilaf is shown at 192 g, 385 g and 580 g (small/average/large).
3. Multilingual naming (5 local languages plus English) is a design goal, to cover the region's linguistic diversity.
4. The atlas has no nutrient composition yet ("research work is in progress"), so it cannot be used directly to estimate intake.

## Relevance to research questions
### Q1: Cultural food datasets
This is the only source in the vault with portion sizes (grams per typical serving) for Central Asian dishes. It also gives cross-language dish-name synonyms for five Central Asian countries. Combined with per-100 g composition from [[Kyrgyzstan Food Composition Table]], it would let the agent turn "a plate of plov" into grams and then nutrients. Coverage is modest (115 items). The weights appear only in the atlas PDF; we extracted them to a CSV table.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- The paper does not validate the atlas against weighed intake. The large portion is a fixed 1.5× coefficient rather than survey-derived.
- Recipes vary between households and countries. Bones and fat in meat dishes are not separated from edible weight, and raw vs cooked weights are not given.
- There are no nutrient values. The atlas is English-only in the interface, although local names are listed.
- The GitHub repo cited as the distribution point (Central-Asian-Food-Innovation-Lab/Central-Asian-Digital-Visual-Food-Atlas) holds only a README at its head. The atlas PDF (122 pp) is still retrievable from git history via Git LFS (commit 0ab8965); we parsed it (see [[Central Asian Digital Visual Food Atlas]]). The repo has no licence file; the article is CC BY 4.0.

## Related work to follow
![[Backlog.base#Cited by this paper]]
