---
title: "FlavorDB2: An updated database of flavor molecules"
citekey: "goel2024flavordb2"
authors: ["Mansi Goel", "Nishant Grover", "Devansh Batra", "Neelansh Garg", "Rudraksh Tuwani", "Apuroop Sethupathy", "Ganesh Bagler"]
year: 2024
published: 2024-09-24
venue: "Journal of Food Science 89(11):7076-7082"
peer_reviewed: true
url: "https://doi.org/10.1111/1750-3841.17298"
arxiv: ""
doi: "10.1111/1750-3841.17298"
pdf: ""
pdf_url: ""
datasets: ["[[FlavorDB2]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites:
  - "[[Phenol-Explorer (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# FlavorDB2: An updated database of flavor molecules

> [!abstract] TL;DR
> The paper is an update of FlavorDB (NAR 2018). FlavorDB2 holds 25,595 flavor molecules, of which 2,254 are associated with 936 natural ingredients from 34 categories. It records flavor profile, chemical properties, regulatory status, consumption statistics, taste/aroma thresholds, reported uses in food categories and synthesis, behind a new interface with food pairing. *The full text is paywalled (Wiley returned 403), so this note is based on the abstract, Crossref metadata and the live site.*

## What was built
- **Dataset(s):** [[FlavorDB2]]
- **Sources & construction:** (from the site FAQ) the ingredient list was built from FooDB and Ahn et al. (arXiv 1502.03815). 951 entities were manually classified into 34 categories and mapped to 532 natural sources using Wikipedia. Molecule properties come from PubChem, with flavor profiles from FooDB, FEMA and Fenaroli.
- **Size & coverage:** 25,595 molecules; 2,254 linked to 936 ingredients; 34 categories.
- **Evaluation / applications:** a database/webserver paper. Applications are food pairing, flavor search, and similarity search (Tanimoto ≥ 0.3 via OpenBabel).

## Key findings
1. 25,595 flavor molecules are catalogued, and 2,254 are associated with 936 natural ingredients.
2. Ingredients fall into 34 categories (e.g. Spice, Herb, Vegetable Root, Fruit Citrus).
3. New molecule attributes: regulatory status, consumption statistics, taste/aroma thresholds, uses in food categories, synthesis.

## Relevance to research questions
### Q2: Cultural ingredient datasets
FlavorDB2 is the ingredient vocabulary (entity ids, synonyms including Indian names, natural sources) that [[CulinaryDB]] uses, so it is the bridge from cuisine ingredients to chemistry.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
It supplies ingredient → compound links with PubChem, FooDB and CAS ids. It has no health effects itself, but those ids join to CTD, FooDB and [[SpiceRx]].

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables
Not read (paywalled).

## Limitations / caveats
- It covers flavor (mostly volatile) compounds, not complete composition, and has no concentrations.
- There is no bulk download. We could not read the full text.

## Related work to follow
![[Backlog.base#Cited by this paper]]
