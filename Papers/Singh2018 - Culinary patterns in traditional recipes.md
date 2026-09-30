---
title: "Data-driven investigations of culinary patterns in traditional recipes across the world"
citekey: "singh2018culinary"
authors: ["Navjot Singh", "Ganesh Bagler"]
year: 2018
published: 2018-04-01
venue: "2018 IEEE 34th International Conference on Data Engineering Workshops (ICDEW)"
peer_reviewed: true
url: "https://arxiv.org/abs/1803.04343"
arxiv: "1803.04343"
doi: "10.1109/ICDEW.2018.00033"
pdf: ""
pdf_url: "https://arxiv.org/pdf/1803.04343"
datasets: ["[[CulinaryDB]]"]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
cites: []
cited_by: []
cited_by_count: 5
tags:
  - type/paper
  - relevance/core
  - q/1
  - q/2
---
# Data-driven investigations of culinary patterns in traditional recipes across the world

> [!abstract] TL;DR
> The paper introduces **CulinaryDB**: 45,772 recipes from AllRecipes, Food Network, Epicurious and TarlaDalal, grouped into 22 world regions. Ingredients are aliased to FlavorDB entities. The authors use the data with FlavorDB flavor molecules to test the food-pairing hypothesis, region by region, against randomised cuisines.

## What was built
- **Dataset(s):** [[CulinaryDB]]
- **Sources & construction:** recipes scraped from 4 sites (AllRecipes 16,177; Food Network 15,917; Epicurious 11,069; TarlaDalal 2,609). The ingredient list is based on FlavorDB (29 noisy entities removed, synonyms added, 13 + 4 + 7 ingredients added), giving 840 basic ingredients plus 103 compound ingredients.
- **Size & coverage:** 45,772 recipes and 22 regions (Korea 301 up to USA 16,118). 207 recipes from Portugal, Belgium, Central America and the Netherlands were used only in the aggregate. On average a region has 321 unique ingredients.
- **Evaluation / applications:** food-pairing Z-scores against random cuisines, and null models that preserve ingredient popularity and/or category composition.

## Key findings
1. The recipe size distribution is bounded, averaging about 9 ingredients per recipe. Ingredient popularity follows a consistent scaling across all cuisines.
2. 16 of 22 regions show *uniform* (positive) food pairing, including the Indian Subcontinent, Middle East, China, Thailand and South East Asia. 6 show *contrasting* pairing: Scandinavia, Japan, DACH, British Isles, Korea and Eastern Europe.
3. No cuisine was indistinguishable from random.
4. Ingredient popularity alone reproduces the observed pairing patterns. Category composition does not.
5. The Indian Subcontinent, Africa, the Middle East and the Caribbean use spices most prominently. France, the British Isles and Scandinavia use dairy more than vegetables.

## Relevance to research questions
### Q1: Cultural food datasets
CulinaryDB is an openly downloadable recipe × region × ingredient table, and Middle East (993) and Indian Subcontinent (4,058) are among its regions. It is useful as a baseline "what ingredients does cuisine X use" resource.

See [[Q1 Cultural food datasets]]

### Q2: Cultural ingredient datasets
Ingredients are normalised to FlavorDB entity ids with categories and synonyms (including Hindi names such as jeera or methi), which gives a region → ingredient-frequency profile that links to flavor chemistry.

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables
Table 1: recipes and unique ingredients per region (reproduced in [[CulinaryDB]]).

## Limitations / caveats
- The recipes come from Western recipe sites except TarlaDalal, and the regions are coarse.
- It is a short workshop paper with no nutrition and no quantities.

## Related work to follow
![[Backlog.base#Cited by this paper]]
