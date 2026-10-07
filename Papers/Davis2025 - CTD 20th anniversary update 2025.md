---
title: "Comparative Toxicogenomics Database's 20th anniversary: update 2025"
citekey: "Davis2025"
authors: ["Allan Peter Davis", "Thomas C. Wiegers", "Daniela Sciaky", "Fern Barkalow", "Melissa Strong", "Brent Wyatt", "Jolene Wiegers", "Roy McMorran", "Sakib Abrar", "Carolyn J. Mattingly"]
year: 2025
published: 2024-10-10
venue: "Nucleic Acids Research 53(D1):D1328–D1334 (Database issue)"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkae883"
arxiv: ""
doi: "10.1093/nar/gkae883"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC11701581?pdf=render"
datasets: ["[[CTD]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
cites: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/3
  - kind/compound
  - region/global
---
# Comparative Toxicogenomics Database's 20th anniversary: update 2025

> [!abstract] TL;DR
> This is the 20th-anniversary update of CTD, the hand-curated knowledgebase of chemical–gene, chemical–phenotype,
> chemical–disease and gene–disease interactions taken from the literature. It reports the size of CTD (3.8 M curated
> interactions; 94 M relationships once inferred links and imported data are included) and describes new curation
> tools (PubTator NLP, Exposure Curation Tool), tool upgrades (Tetramers, Pathway View) and new infrastructure.

## What was built
- **Dataset(s):** [[CTD]]
- **Sources & construction:** biocurators read PubMed articles and code interactions with controlled vocabularies
  (MeSH chemicals and diseases (MEDIC), NCBI genes, GO phenotypes) as structured sentences. Articles are prioritised by
  a chemical-centric strategy, targeted journals and text-mining scores. PubTator NLP is now built into the curation
  interface. Inferences follow Swanson's ABC model: chemical–gene + gene–disease → inferred chemical–disease.
- **Size & coverage (Aug 2024):** 3.8 M direct interactions from >149,000 articles, covering >17,700 chemicals,
  55,400 genes, 6,700 phenotypes, 7,200 diseases, 214,000 exposure statements, 980 anatomy terms and >630 species;
  48 M inferred relationships; 94 M relationships in total.
- **Evaluation / applications:** web tools (Tetramers, Pathway View, Set Analyzer), an API, and monthly bulk
  downloads. 227 external databases link to or use CTD.

## Key findings
1. CTD grew from a 2004 prototype to 3.8 M curated direct interactions, and to 94 M relationships including
   inferences and imported GO/KEGG/Reactome/BioGRID data.
2. The Exposure module holds 214,000 statements on 1,500 stressors, 1,400 human genes and 1,000 outcomes (500
   phenotypes and 500 diseases) from >3,400 articles, now entered through a new Exposure Curation Tool with real-time
   QC.
3. CTD Tetramers (chemical–gene–phenotype–disease) can now be queried by chemical or gene, show an Evidence column
   with the five supporting statements, and export chord diagrams for AOP building.
4. >8,000 Google Scholar citations, at about 3 citations per day since 2023.

## Relevance to research questions
### Q3: Food compound & health-effect datasets
CTD is the curated **compound → disease** layer. Food-composition resources (FooDB, [[HMDB]], [[FoodAtlas]]) give a
food's compounds, and CTD's DirectEvidence ("therapeutic" / "marker/mechanism") plus PubMed ids gives what each
compound is associated with. FoodAtlas uses exactly this. It has no food or culture dimension of its own, and it
leans towards toxicology, so "therapeutic" often reflects animal or cell work, not dietary trials.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- The paper does not give per-type counts of chemical–disease curation or evidence strength. Study type (human or
  animal) is not a field in the downloads.
- Terms of use: cite and link CTD and notify it; commercial use needs a licence.

## Related work to follow
![[Backlog.base#Cited by this paper]]
