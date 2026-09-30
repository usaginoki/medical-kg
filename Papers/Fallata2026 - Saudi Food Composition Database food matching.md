---
title: "Saudi Food Composition Database: Food Identification and Food Matching"
citekey: "Fallata2026"
authors: ["Ghadir Fallata", "Deema Alsalman", "Omar A. Alhumaidan", "Mojca Korošec"]
year: 2026
published: 2026-04-17
venue: "Research Square preprint"
peer_reviewed: false
url: "https://doi.org/10.21203/rs.3.rs-9437605/v1"
arxiv: ""
doi: "10.21203/rs.3.rs-9437605/v1"
pdf: ""
pdf_url: "https://www.researchsquare.com/article/rs-9437605/v1.pdf"
datasets: ["[[Saudi Food Composition Tables]]"]
topics: [cultural-food-health]
questions: [Q2]
relevance: adjacent
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/2
  - kind/ingredient
  - region/middle-east
---
# Saudi Food Composition Database: Food Identification and Food Matching

> [!abstract] TL;DR
> This SFDA-led preprint describes the methodology behind the national **Saudi Food Composition Database (SFCD)**. SFCD takes McCance & Widdowson (UK) as its base and follows FAO/INFOODS and EuroFIR guidance. It adds Saudi-specific food groups and codes, an analytical tool for **matching the same food across literature sources**, and a quality-index score that assigns each value a confidence level. It is a methods paper with no composition values. It explains how the web database behind the [[Saudi Food Composition Tables]] (fd.sfda.gov.sa) is organised, but it does not describe the 130-dish analysis book.

## What was built
- **Dataset(s):** [[Saudi Food Composition Tables]] (the SFCD web database; the dish book is a separate SFDA output)
- **Sources & construction:**
  - Food groups are borrowed from McCance & Widdowson and FAO/WHO GIFT, then modified.
  - National foods get new codes prefixed with "S", e.g. the sub-group `SBB` Camel milk.
  - Values come from the literature, analysis, calculation, or borrowing (USDA, MWD). They are tagged with source and analytical-method assurance.
  - Supplementary material 1 gives the full group/sub-group tree with inclusion/exclusion rules.
- **Size & coverage:**
  - **17 food groups and ~90 sub-groups** (A cereals … T composite dishes, K savory snacks).
  - New groups for composite dishes, food supplements, and foods for particular nutritional uses.
  - Extra nutrients not in MWD: amino acids (for wheat-based diets) and heavy metals (for food-safety monitoring).
- **Evaluation / applications:** a worked example on camel-milk protein. A borrowed USDA value scores 20 (medium confidence); an analysed value by a recognised method scores 60 + 40 = 100 (high), so the analysed value is selected.

## Key findings
1. SFCD uses **17 food groups and ~90 sub-groups**, with Saudi-invented sub-groups such as camel milk (whole, semi-skimmed, skimmed, processed; defined by fat %).
2. The food-naming step uses **~16 descriptor categories**: Arabic and English name, scientific name, cooking method, maturity, wild vs domesticated, fortification, recipe info, and others. Spellings follow the Culinary Arts Commission.
3. The source quality index runs analysed 60 · calculated 50 · imputed 40 · recipe-calculated 30 · borrowed 20 · presumed 10 · undetermined 0. An analytical-assurance score (AQI) is added, giving a total of up to 100.
4. Confidence bands: high (60–100), then good / medium / low, then none (0).
5. Context: non-communicable diseases account for **78% of deaths** in Saudi Arabia, which motivates a national FCD for intake and exposure estimates.

## Relevance to research questions
### Q2: Cultural ingredient datasets
The paper explains how Saudi-specific ingredients (camel milk, local cereals, traditional composite dishes) are identified, coded and scored in the national database. This is useful if the fd.sfda.gov.sa data becomes accessible, because every value carries a source and confidence code.

See [[Q2 Cultural ingredient datasets]]

## Limitations / caveats
- This is a preprint (not peer reviewed). It is methodological only: no food counts, no released data, and figures and tables are only in the PDF.
- The confidence-band thresholds in the text are garbled by citation-manager errors (the band limits are replaced by references).
- The web database it describes was geo-blocked from our location.

## Related work to follow
![[Backlog.base#Cited by this paper]]
