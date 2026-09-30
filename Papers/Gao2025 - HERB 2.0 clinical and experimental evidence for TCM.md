---
title: "HERB 2.0: an updated database integrating clinical and experimental evidence for traditional Chinese medicine"
citekey: "Gao2025"
authors: ["Kai Gao", "Liu Liu", "Shuangshuang Lei", "Zhinong Li", "Peipei Huo", "Zhihao Wang", "Lei Dong", "Wenxin Deng", "Dechao Bu", "Xiaoxi Zeng", "Chun Li", "Yi Zhao", "Wei Zhang", "Wei Wang", "Yang Wu"]
year: 2025
published: 2024-11-18
venue: "Nucleic Acids Research 53(D1) (Database issue)"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkae1037"
arxiv: ""
doi: "10.1093/nar/gkae1037"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC11701625?pdf=render"
datasets: ["[[HERB]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# HERB 2.0: an updated database integrating clinical and experimental evidence for traditional Chinese medicine

> [!abstract] TL;DR
> HERB 2.0 adds a **clinical-evidence layer** to the HERB TCM database: 8,558 ClinicalTrials.gov trials and
> 8,032 PROSPERO meta-analyses whose study subject is a herb, herbal ingredient or formula. They were found by
> keyword search, filtered by two LLMs plus manual curation, and 1,941 trials / 593 meta-analyses have curated
> conclusions. It also adds 6,743 formulae, more experiments (2,231) and references (6,644), connectivity mapping
> against CMap drugs and diseases, and a Neo4j knowledge graph.

## What was built
- **Dataset(s):** [[HERB]]
- **Sources & construction:** herbs and ingredients de-duplicated across multiple TCM databases; formulae from
  the Chinese Pharmacopoeia 2020, CFDA patent medicines and national classic prescriptions (2018, 2022),
  cross-referenced to ETCM/ITCM; targets from HIT 2.0 plus curation (GenBank, GeneCards, TTD); diseases from
  DisGeNET plus curation (OMIM, HPO, DO). Trials and meta-analyses were searched by herb/ingredient/formula
  names and aliases up to 2024-01-01 (102,151 trial and 54,855 meta-analysis hits), screened with ChatGPT 3.5
  and Gemini, then manually curated. Conclusions, source, origin and processing were extracted from companion
  PubMed papers.
- **Size & coverage:** 6,892 herbs, 44,595 ingredients, 6,743 formulae, 15,515 targets, 30,170 diseases, 8,558
  trials, 8,032 meta-analyses, 2,231 experiments, 6,644 references.
- **Evaluation / applications:** LLM screening evaluated on 2,438 trials and 7,884 meta-analyses labelled by
  hand. Pairwise connectivity mapping among herbs/ingredients/formulae, 2,837 CMap drugs and diseases. A
  gene-expression upload interface. A knowledge graph with 9 entity and 28 relation types.

## Key findings
1. Trials cover 249 herbs, 375 ingredients and 59 formulae, 556 diseases and 119 registration countries.
   Meta-analyses cover 267 herbs, 399 ingredients and 336 formulae, 485 diseases and 81 countries.
2. Phases: 12.5% Phase 1, 19.6% Phase 2, 12.6% Phase 3, 11.3% Phase 4. About 3,964 trials are randomised and
   double-blind or stricter.
3. Companion papers were found for 1,941 trials (22.7%) and 593 meta-analyses (7.4%). Trials with clear
   conclusions involve 96 herbs, 165 ingredients and 13 formulae.
4. The LLMs had 51.3% accuracy in judging records; 98.6% of errors were false positives, so every record
   either LLM kept was curated by hand.
5. Knowledge-graph relations: 99.9% of non-built-in relations are supported by one evidence type; 3,702 by at
   least two. Among reciprocal connectivity-mapping pairs (score ≥ 75), the KG validated 30.2% (e.g.
   tomato ↔ lycopene 77.0/79.8).

## Relevance to research questions
### Q2: Cultural ingredient datasets
The herb catalogue is TCM-centred but includes many foods. The trial table's most-studied "herbs" are green tea,
olive, peanut, pomegranate, cocoa, honey, garlic, tomato and cinnamon. Formulae add Chinese multi-herb
preparations (no dosages).

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
This is the strongest evidence tier in the TCM batch: trial and meta-analysis records per food/herb and per
compound (e.g. cinnamon → HbA1c in diabetes; curcumin, gingerol). The records have NCT/CRD ids, and the
ingredients have InChIKey/PubChem ids for joins to food-compound databases.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- False negatives from the LLM screen are acknowledged as missing entries.
- Curated conclusions exist for a minority of records and are not in the bulk TSV.
- The bulk download lacks association tables (see [[HERB]]).
- Herb and ingredient counts dropped from 1.0 because of de-duplication, so v1 ids may not all carry over.

## Related work to follow
![[Backlog.base#Cited by this paper]]
