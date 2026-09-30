---
title: "FooDrugs: a comprehensive food–drug interactions database with text documents and transcriptional data"
citekey: "LacruzPleguezuelos2023"
authors: ["Blanca Lacruz-Pleguezuelos", "Oscar Piette", "Marco Garranzo", "David Pérez-Serrano", "Jelena Milešević", "Isabel Espinosa-Salinas", "Ana Ramírez de Molina", "Teresa Laguna", "Enrique Carrillo de Santa Pau"]
year: 2023
published: 2023-11-11
venue: "Database (Oxford)"
peer_reviewed: true
url: "https://doi.org/10.1093/database/baad075"
arxiv: ""
doi: "10.1093/database/baad075"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC10640380?pdf=render"
datasets: ["[[FooDrugs]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/3
  - kind/compound
  - region/global
---
# FooDrugs: a comprehensive food–drug interactions database with text documents and transcriptional data

> [!abstract] TL;DR
> FooDrugs is a MySQL database of *potential* food–drug interactions (FDIs), released on Zenodo under CC BY 4.0. It combines two sources. The first is an NLP pipeline (DistilBERT NER plus a relation classifier trained on the DDI corpus) that pulled 1,108,429 potential FDIs from 439,338 PubMed abstracts, ClinicalTrials.gov records and DDI-corpus documents. The second is a transcriptomic "connectivity" approach: GEO food-compound signatures are compared with Connectivity Map drug signatures, giving 2,321,633 inferred FDIs.

## What was built
- **Dataset(s):** [[FooDrugs]]
- **Sources & construction:**
  - Text module: documents with both a food term and a drug term in the title or abstract. Food terms come from FooDB, KEGG BRITE phytochemicals, PhytoHub and the DFI corpus; drug terms from ATC and the DFI corpus. Food NER used a dictionary plus DistilBERT (F1 0.88). The relation model was trained on the DDI corpus (F1 0.77).
  - Molecular module: 150 human GEO series (121 microarray, 29 RNA-seq) giving 462 conditions (food compound × time × concentration × sample origin). The differentially expressed genes (DEGs) of each condition were queried against CMap. An interaction is kept when |tau| > 90.
- **Size & coverage:** 3,430,062 potential FDIs in total. The text module holds 632,358 unique pairs between 50,960 food compounds/bioactives and 161,809 drug terms. The molecular module links 293 foods × 6,395 CMap perturbagens (2,545 of them drugs).
- **Evaluation / applications:** the NLP pipeline was tested on the DFI corpus. Case studies cover resveratrol (220 citations, 154 unique potential FDIs) and a drug-centred query.

## Key findings
1. There are 1,108,429 text-mined potential FDIs from 439,338 texts: 425,023 PubMed, 13,778 ClinicalTrials.gov and 537 DDI corpus.
2. There are 2,321,633 transcriptomics-inferred FDIs (|tau| > 90) against 70,895 CMap profiles.
3. The relation extractor is entity-agnostic and reaches F1 0.77, so many "interactions" are co-mentions in an interaction-like sentence rather than validated effects.
4. Each molecular condition has on average 2,451 DEGs (median 730).

## Relevance to research questions
### Q3: Food compound & health-effect datasets
FooDrugs gives very wide, low-precision recall of which foods or food compounds have been discussed alongside which drugs. That makes it useful as a candidate generator, for example to check that a regional food such as fenugreek, black seed or dates has any literature on drug interactions. It is not a source of graded clinical advice. Its mentions point back to PMIDs, so an agent can fetch the evidence.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- There is no manual curation. The DDID authors point this out as its main weakness.
- Food and drug entities are free-text strings with no ontology IDs in the interaction table.
- The transcriptomic links are hypotheses based on signature similarity in cell lines.
- There is no country or culture dimension.

## Related work to follow
![[Backlog.base#Cited by this paper]]
