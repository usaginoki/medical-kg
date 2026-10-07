---
title: "A framework for recipe data structure with applications for culinary and nutritional insights"
citekey: "goel2026recipedb2"
authors: ["Mansi Goel", "Sumit Bhagat", "Saloni Srivastava", "Malav Patel", "Hardi Parikh", "Shlok Vinodkumar Mehroliya", "Ganesh Bagler"]
year: 2026
published: 2026-08-12
venue: "arXiv (cs.CL)"
peer_reviewed: false
url: "https://arxiv.org/abs/2609.22099"
arxiv: "2609.22099"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2609.22099"
datasets: ["[[RecipeDB2]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites:
  - "[[FlavorDB2 (candidate)]]"
  - "[[FooDis]]"
  - "[[FoodKG]]"
  - "[[Recipe1M+]]"
  - "[[RecipeNLG]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
---
# A framework for recipe data structure with applications for culinary and nutritional insights

> [!abstract] TL;DR
> The paper presents **RecipeDB2**: 128,942 recipes (RecipeDB v1 + Archana's Kitchen + Awesome Cuisine) with 35,474 ingredients from 32 regions and 99 countries. Ingredient phrases are parsed by a spaCy-transformer NER into 7 attributes and mapped to USDA SR Legacy with BERT embeddings, which gives 148 nutrients. Ingredient categories are predicted with a Random Forest and dietary styles are assigned by rules. The data is served through a MongoDB/Express/React web server but is **not publicly released**.

## What was built
- **Dataset(s):** [[RecipeDB2]]
- **Sources & construction:** RecipeDB v1 (118,171 recipes) + Archana's Kitchen (9,730) + Awesome Cuisine (1,132). Geo-cultural hierarchy: continent → region → country → state → city. NER extracts name, unit, quantity, state, size, temperature and dry/fresh. The top ingredient-unit pairs were converted to grams/ml by hand. BERT/RoBERTa/Jaccard were compared for mapping to USDA. TF-IDF + 7 classifiers were compared for the 34 ingredient categories.
- **Size & coverage:** 128,942 recipes; 35,474 ingredients; 1,163 units; 81,240 ingredient-unit pairs; 7 continents, 32 regions, 99 sub-regions (countries), 34 sub-sub-regions, 12 sub-sub-sub-regions.
- **Evaluation / applications:** mapping evaluated on the 200 most frequent ingredients; category prediction on 10,659 hand-labelled ingredients. Use cases: search by cuisine, by macronutrients, and by ingredients or categories used/not used.

## Key findings
1. BERT mapping to USDA achieves F1 = 87.90 (accuracy 79.50%) on the 200 most frequent ingredients, against RoBERTa 71.09 and Jaccard 37.38. 25,903 of 35,474 ingredients (73.01%) were mapped with similarity ≥ 70%.
2. 128,899 recipes were fully or partially mapped to nutrition. Only 43 remained unmapped.
3. Random Forest predicts ingredient category with accuracy 89.12% / weighted F1 89.16%. The largest categories are Dish (3,723), Spice (3,314), Vegetable (3,303) and Meat (3,261).
4. Only 6.1% of the 81,240 ingredient-unit pairs were already in standard units. 43.90% of the frequent pairs were converted manually.
5. The most common ingredients are salt (41.28% of recipes), garlic (33.18%), onion (28.84%), water (21.55%) and butter (20.64%). The mean recipe has 245.2 g carbohydrate, 49.48 g protein and 1,989 kcal (whole recipe).

## Relevance to research questions
### Q1: Cultural food datasets
This is the largest recipe resource labelled with cuisine and country that also has amounts, steps and USDA-based nutrition. It covers Middle Eastern, Indian-subcontinent and East/Southeast Asian sub-regions, which is exactly what a culturally tuned diet agent needs. But the Data Availability statement says the data is not publicly available due to institutional copyright, so using it needs author contact.

See [[Q1 Cultural food datasets]]

## Key figures & tables
Table 1 (top-20 ingredients with units) · Table 2 (mapping model comparison) · Table 3 (category classifiers). Supplementary Table S1 has the region schema (not seen).

## Limitations / caveats
- The recipes mostly come from English-language Western sites plus Indian sites. There is little GCC or Central Asian content.
- Nutrition estimates depend on the NER and mapping pipeline: ~27% of ingredients are unmapped and only 43.9% of frequent units were converted.
- The data is not released. The web API search endpoints were broken when we tried them (2026-09-30).
- This is a preprint (not peer-reviewed).

## Related work to follow
![[Backlog.base#Cited by this paper]]
