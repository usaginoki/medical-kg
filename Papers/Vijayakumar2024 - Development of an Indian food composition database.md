---
title: "Development of an Indian Food Composition Database"
citekey: "Vijayakumar2024"
authors: ["Aswathy Vijayakumar", "Hima Bindu Dubasi", "Ananya Awasthi", "Lindsay M Jaacks"]
year: 2024
published: 2024-06-13
venue: "Current Developments in Nutrition 8(7):103790"
peer_reviewed: true
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795/"
arxiv: ""
doi: "10.1016/j.cdnut.2024.103790"
pdf: ""
pdf_url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC11277795/pdf/"
datasets: ["[[Indian Nutrient Databank (INDB)]]"]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - q/2
---
# Development of an Indian Food Composition Database

> [!abstract] TL;DR
> The paper builds the open **Indian Nutrient Databank (INDB)**, giving nutrient values for 1,014 commonly
> consumed Indian recipes. Recipes come from two Indian home-science cookbooks and food blogs. Ingredients were
> matched to the ICMR-NIN Indian Food Composition Tables (IFCT 2017, then 2004), with UK CoFID and USDA as
> fallbacks. USDA nutrient retention factors were applied for cooking losses.

## What was built
- **Dataset(s):** [[Indian Nutrient Databank (INDB)]]
- **Sources & construction:** 1,124 recipes (611 from *Basic Food Preparation* 4th ed., 513 from *The Art &
  Science of Cooking* 5th ed.) plus 148 blog recipes, deduplicated to 1,014. 1,095 raw foods were compiled:
  528 from IFCT 2017, 369 more from IFCT 2004, then 144 UK and 54 USDA ingredients. Household measures were
  converted to grams, and USDA Nutrient Retention Factors (Release 6) were applied for 17 nutrients.
- **Size & coverage:** 1,014 recipes, about 40 nutrients per 100 g and per serving. India only, with no
  regional labels.
- **Evaluation / applications:** compares nutrient content across dishes and with vs. without retention
  factors. Released as open Stata code plus Excel files on GitHub.

## Key findings
1. 1,014 unique recipes were kept from 1,124 collected.
2. Only 42.62% of recipe ingredients could be given a retention factor.
3. Energy density varies widely, e.g. vegetable samosa 443 kcal/100 g vs. khichdi 57 kcal/100 g.
4. Retention was highest for calcium and zinc (75–100%) and most variable for vitamin C (20–100%).
5. Applying retention factors changed nutrients significantly (P < 0.01) but by small amounts (median loss e.g.
   copper 0.001 mg, potassium 5.15 mg).

## Relevance to research questions
### Q1: Cultural food datasets
An open, citable table of standard Indian dishes with nutrients. It is the nutrient backbone for South Asian
dietary advice, used by [[IndicRecipeNutri]] (only its UK/US rows) and by nutrition-recommendation work.

See [[Q1 Cultural food datasets]]

### Q2: Cultural ingredient datasets
Recipe → ingredient tables with gram amounts linked to IFCT codes show which ingredients Indian dishes use
and in what proportions.

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables

## Limitations / caveats
- Recipes come from Delhi-based home-science manuals and blogs, so regional diversity is limited and there are
  no state labels.
- No packaged foods. Cooking yield factors are incomplete, and serving sizes are missing for pickles and
  weaning foods.
- Nutrient losses may be underestimated for foods absent from the USDA retention tables.
- The IFCT source data is not openly redistributable.

## Related work to follow
![[Backlog.base#Cited by this paper]]
