---
title: "A unified knowledge graph linking foodomics to chemical-disease networks and flavor profiles"
citekey: "Li2026"
authors: ["Fangzhou Li", "Jason Youn", "Kaichi Xie", "Trevor Chan", "Pranav Gupta", "Arielle Yoo", "Michael Gunning", "Keer Ni", "Ilias Tagkopoulos"]
year: 2026
published: 2026-01-20
venue: "npj Science of Food 10:33"
peer_reviewed: true
url: "https://doi.org/10.1038/s41538-025-00680-9"
arxiv: ""
doi: "10.1038/s41538-025-00680-9"
pdf: ""
pdf_url: "https://www.nature.com/articles/s41538-025-00680-9.pdf"
datasets: ["[[FoodAtlas]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites:
  - "[[CTD (candidate)]]"
  - "[[FlavorGraph]]"
  - "[[NutriChem]]"
  - "[[USDA FoodData Central (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
  - kind/compound
  - region/global
---
# A unified knowledge graph linking foodomics to chemical-disease networks and flavor profiles

> [!abstract] TL;DR
> The paper presents FoodAtlas KGv2. LLMs extract food–chemical–concentration facts from PubMed Central, and these
> are fused with FoodOn, ChEBI, FDC, CTD, ChEMBL, FlavorDB and PubChem into one provenance-tracked graph of foods,
> chemicals, diseases, bioactivities and flavours. The authors use it to cluster foods by disease-relevant chemistry,
> to predict antioxidant capacity, and to propose healthier one-ingredient substitutions in real US meals.

## What was built
- **Dataset(s):** [[FoodAtlas]]
- **Sources & construction:** 1,300 food names (FooDB, FDC) were searched in PubMed/PMC with "{food} AND ((compound)
  OR (nutrient))". Sentences were fuzzy-filtered (~10 M) and then classified by a fine-tuned BioBERT, giving 773,366
  sentences with p > 0.9. A fine-tuned GPT-3.5 extracted (food, part, chemical, concentration) tuples. Units were
  normalised, and entities were linked to FoodOn/ChEBI. Diseases come from CTD DirectEvidence (therapeutic → treats,
  marker/mechanism → worsens), flavours from FlavorDB and PubChem HSDB, and bioactivity from ChEMBL (via InChIKey).
- **Size & coverage:** 1,430 foods, 3,610 chemicals, 2,181 diseases and 958 flavour descriptors, linked by 96,981
  provenance-tracked edges. These include 48,474 food–chemical edges from 125,723 sentences and 23,211 CTD
  chemical–disease assertions. The Fig. 2 schema counts all nodes: 10,266 chemicals, 263,021 chemical is-a edges and
  138,792 chemical–disease edges over 3,177 diseases. No culture or country labels.
- **Evaluation / applications:** IE evaluation on 356 test sentences; food clustering (Node2Vec + t-SNE + hurdle
  tests); a Bioactivity Prediction Model (random forest) for FRAP antioxidant capacity; a one-hop substitution engine
  on USDA WWEIA meals.

## Key findings
1. The fine-tuned GPT-3.5 reached F1 = 0.67 for food–chemical–concentration extraction, against 0.42 for one-shot
   GPT-4.
2. Six disease-relevant food clusters were found, e.g. omega-3 marine oils (EPA enrichment q = 1.3 × 10⁻²⁰;
   protective for cardiovascular disease), citrus-terpene modulators (limonene), and fat-dense animal proteins
   (palmitic acid, trans fats).
3. The antioxidant model explained R² = 0.52 of FRAP variance (PCC = 0.72) using concentrations, Morgan fingerprints
   and pChEMBL potency.
4. 14,580 disease-focused one-hop swaps raised the mean disease-prevention score by 11.9% (e.g. hummus → olive in a
   pita-and-chickpea lunch, +18% aggregate). 7,798 antioxidant swaps raised predicted antioxidant activity by 210.6%
   on average.

## Relevance to research questions
### Q2: Cultural ingredient datasets
Food–chemical edges carry food part, processing state and concentration from the source sentence. This is useful
ingredient-level composition for foods that FooDB/FDC lack. The foods are ontology entities (FoodOn) with no cultural
labels, so cultural relevance comes from joining to Q1/Q2 datasets.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
This is the most complete ready-made food → compound → disease chain, with PubMed provenance on every hop. But the
disease hop is CTD's binary "treats/worsens" (see [[CTD]]), which the authors themselves say lacks dose–response and
clinical outcomes. CTD tables are not redistributed; users must rebuild them locally.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- Extraction errors (F1 0.67), especially from tables and complex sentences.
- CTD-derived disease links are binary, with no dose or clinical endpoint.
- The substitution model ignores synergy, bioavailability, palatability and "cultural dietary patterns" (stated in
  the Discussion).
- The data availability statement points to GitHub and foodatlas.ai, but the built KG is not in the repo, and
  bundles need an API key (as of 2026-09-30).

## Related work to follow
![[Backlog.base#Cited by this paper]]
