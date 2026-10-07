---
title: "NPASS database update 2026: comprehensive quantitative composition, bioactivity, and ADME-Tox data of natural products for biomedical research"
citekey: "Lin2026"
authors: ["Hanbo Lin", "Dongyue Hou", "Xianhan Jiang", "Ruining Yin", "Shuntao Yu", "Songlin Lu", "Shanshan Wang", "Dianwen Ju", "Hui Zhao", "Yuzong Chen", "Xian Zeng"]
year: 2026
published: 2025-11-17
venue: "Nucleic Acids Research 54(D1):D1519–"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkaf1196"
arxiv: ""
doi: "10.1093/nar/gkaf1196"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC12807772?pdf=render"
datasets: ["[[NPASS]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
cites:
  - "[[BATMAN-TCM]]"
  - "[[COCONUT]]"
  - "[[PubChem]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/3
---
# NPASS database update 2026: comprehensive quantitative composition, bioactivity, and ADME-Tox data of natural products for biomedical research

> [!abstract] TL;DR
> NPASS 3.0 is the third release of the Natural Product Activity and Species Source database. It covers 204,023
> natural products from 48,940 organisms, with 1.05 M quantitative activity records, 208,415 composition
> (concentration-in-species) records, and new experimental ADME (9,713) and toxicity (34,975) data. Records
> were curated from 1,822 new publications (Sept 2022 onward) and from other databases.

## What was built
- **Dataset(s):** [[NPASS]]
- **Sources & construction:** a systematic PubMed search (natural product, herb, marine, microbe, IC50, MIC,
  LD50…) followed by manual curation. A publication had to give the producing organism, a structure-inferable
  NP, the target, and a quantitative value with units. ADME/Tox records come from ChEMBL ADME/Toxicity assays
  (ADMET target category), ToxVal, TOXRIC and the literature. Seven categorical toxicity labels come from
  TOXRIC. Species–compound pairs are also imported from UNPD, COCONUT, FooDB, TM-MC, TCMID and others (seen in
  the download).
- **Size & coverage:** 204,023 NPs; 48,940 organisms (including 341 symbiont, 164 elicitation, 462
  engineered and 289 co-culture organisms); 1,117,269 organism–NP pairs; 8,764 targets; 1,048,756 activity
  records; 208,415 composition records; 88 properties per NP. No cultural or country dimension.
- **Evaluation / applications:** statistics and comparison with COCONUT, NPAtlas and SuperNatural (Table 2);
  AI-assisted search and community submission are new features.

## Key findings
1. **+87,507 quantitative composition records** for 4,873 NPs in 1,030 species were added. Total composition
   records went from 95,004 to **208,415** (+119%).
2. NPs more than doubled (**94,413 → 204,023**, +116%). NPs with activity values rose only 9.6% (43,285 →
   47,418), so about 77% of NPs have no activity annotation.
3. Activity records rose 958,866 → **1,048,756**, now split into molecular level 221,541, in vitro 681,970
   and in vivo 145,245.
4. New safety layers: **34,975 toxicity records** for 3,662 NPs and **9,713 ADME records** for 744 NPs.
5. Compared with COCONUT (695,119 NPs), NPASS has fewer NPs but is the only one of the four with
   composition, activity, ADME and toxicity counts. All 204,023 NPs have species-source annotation (COCONUT:
   26.24%).

## Relevance to research questions
### Q3: Food compound & health-effect datasets
NPASS is the quantitative layer linking a plant or food species to its compounds (and, on the web, how much of
each) and to measured effects: human-protein activity, cell-based and in vivo activity, toxicity and ADME. It
is `adjacent` because it has no culture labels. It becomes useful when a culturally specific ingredient
(e.g. black seed, saffron) is named elsewhere ([[UNaProd]],
[[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[CMAUP]]). The composition layer that would matter
most for dietary exposure is web-only.

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables
*Table 1: NPASS-2023 vs NPASS-2026. Total NPs 94,413 → 204,023; organisms 32,561 → 48,940; organism–NP pairs
872,723 → 1,117,269; activity records 958,866 → 1,048,756; targets 7,753 → 8,764; composition records 95,004
→ 208,415; properties 54 → 88; ADME 9,713 (new); symbiont and elicitation organisms (new).*

## Limitations / caveats
- The composition and ADME layers are not in the bulk download files (checked 2026-09-30). Only activities,
  toxicity, species pairs and metadata are.
- Coverage is skewed to microbial and marine NPs and to cancer-cell or antimicrobial assays. The food-plant
  relevance has to be filtered for.
- Many species–compound pairs are imported from other databases without re-curation.
- No cultural, dietary or geographic-use information.

## Related work to follow
![[Backlog.base#Cited by this paper]]
