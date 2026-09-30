---
title: "SymMap: an integrative database of traditional Chinese medicine enhanced by symptom mapping"
citekey: "Wu2019"
authors: ["Yang Wu", "Feilong Zhang", "Kuo Yang", "Shuangsang Fang", "Dechao Bu", "Hui Li", "Liang Sun", "Hairuo Hu", "Kuo Gao", "Wei Wang", "Xuezhong Zhou", "Yi Zhao", "Jianxin Chen"]
year: 2019
published: 2018-10-31
venue: "Nucleic Acids Research 47(D1):D1110–D1117"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gky1021"
arxiv: ""
doi: "10.1093/nar/gky1021"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC6323958?pdf=render"
datasets: ["[[SymMap]]"]
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
# SymMap: an integrative database of traditional Chinese medicine enhanced by symptom mapping

> [!abstract] TL;DR
> The paper presents SymMap v1. It is built from the Chinese Pharmacopoeia (2015): herbs are linked to
> expert-standardised TCM symptoms, which a 17-expert committee mapped to modern-medicine (UMLS) symptoms. These
> are joined to ingredients, targets and diseases integrated from TCMID/TCMSP/TCM-ID/HIT/HPO/OMIM/Orphanet.
> Fisher's-exact-test inference fills in all pairwise indirect relations (e.g. herb → disease). The aim is
> phenotypic drug discovery. For us it is the curated bridge from traditional indications to modern symptom
> vocabularies. The current site is v2.0 (see [[SymMap]]).

## What was built
- **Dataset(s):** [[SymMap]] (v1.0 in the paper; the vault note describes v2.0)
- **Sources & construction:** herbs and TCM symptom terms extracted from the Chinese Pharmacopoeia 2015 and
  standardised against national TCM terminology publications. Each TCM symptom was mapped to MM symptoms (from
  MeSH 2017, SIDER 2017, UMLS 2016) by 3 randomly chosen experts, with at least 2 agreeing. Ingredients come from
  TCMID 2015, TCMSP 2.3 and TCM-ID 1.0 (de-duplicated by CAS/CID/InChIKey); targets from HIT 2.0, TCMSP, HPO,
  DrugBank 5.0 and NCBI Gene; diseases from OMIM and Orphanet.
- **Size & coverage:** 499 herbs, 1,717 TCM symptoms, 961 MM symptoms, 19,595 ingredients, 4,302 targets, 5,235
  diseases; China only.
- **Evaluation / applications:** 6 direct and 9 indirect association types. The indirect ones are inferred by
  Fisher's exact test with Bonferroni and BH FDR. Web browse/search/visualise/download (Flask + MySQL), no
  registration.

## Key findings
1. Direct associations: 6,638 herb–TCM symptom, 2,978 TCM symptom–MM symptom, 48,372 herb–ingredient,
   12,107 MM symptom–disease, 29,370 ingredient–target and 7,256 gene–disease associations.
2. Each herb is linked to 13.30 TCM symptoms on average; each TCM symptom to 3.87 herbs.
3. Each TCM symptom maps to 1.74 MM symptoms and each MM symptom to 3.13 TCM symptoms, so the two vocabularies
   do not map one-to-one.
4. Herb–disease links are obtained three ways: manually from pharmacopoeia indications (few), two-step tests
   via ingredients, and two-step tests via MM symptoms. The smallest P/FDR is kept.
5. Herb → MM symptom and TCM symptom → disease pairs are kept without a statistical test, because the expert
   intermediate links were judged reliable.

## Relevance to research questions
### Q2: Cultural ingredient datasets
The herb list is the Chinese Pharmacopoeia, which includes many culinary items (ginger, jujube, goji, cassia,
hawthorn, yam). SymMap gives their TCM properties, meridians and traditional indications as structured,
English-mapped symptoms: the "cultural meaning" of an ingredient in Chinese food therapy.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
Herb → ingredient → target → disease, and herb → symptom → UMLS symptom. A route from a culturally used food
to both its compounds and its claimed effect, with P-values to rank inferred links.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- The inferred relations rest on co-membership statistics and include many implausible links.
- Only herbs registered in the pharmacopoeia (499 in v1). No food or everyday-use flag.
- Ingredient and target data are inherited from older TCM databases (TCMSP, TCMID) with known noise.
- Bulk downloads contain entity tables only. Relations are web-only (see [[SymMap]]).
- Paper licence CC BY-NC 4.0.

## Related work to follow
![[Backlog.base#Cited by this paper]]
