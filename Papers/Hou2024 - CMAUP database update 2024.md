---
title: "CMAUP database update 2024: extended functional and association information of useful plants for biomedical research"
citekey: "Hou2024"
authors: ["Dongyue Hou", "Hanbo Lin", "Yuhan Feng", "Kaicheng Zhou", "Xingxiu Li", "Yuan Yang", "Shuaiqi Wang", "Xue Yang", "Jiayu Wang", "Hui Zhao", "Xuyao Zhang", "Jiajun Fan", "SongLin Lu", "Dan Wang", "Lyuhan Zhu", "Dianwen Ju", "Yu Zong Chen", "Xian Zeng"]
year: 2024
published: 2023-10-28
venue: "Nucleic Acids Research 52(D1):D1508–D1518"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkad921"
arxiv: ""
doi: "10.1093/nar/gkad921"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC10767869?pdf=render"
datasets: ["[[CMAUP]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# CMAUP database update 2024: extended functional and association information of useful plants for biomedical research

> [!abstract] TL;DR
> This is the 2024 update of CMAUP, a database of "useful plants" (medicinal, food, edible, agricultural, garden,
> drug-producing) and their ingredients' collective molecular activities. It grows to 7,865 plants and 60,222
> ingredients. New layers: plant → human disease associations from four evidence types (targets,
> transcriptomic reversal, plant clinical trials, ingredient clinical trials), clinical-trial data, DNA
> barcodes, phylogeny and predicted oral bioavailability.

## What was built
- **Dataset(s):** [[CMAUP]]
- **Sources & construction:** ingredients and targets as in CMAUP-2019, updated. Transcriptomic changes for
  74 diseases from 20,027 patient samples (DESeq2 DEGs overlapping plant targets). Clinical trials from
  ClinicalTrials.gov (plant/extract level) and ChEMBL v32 (ingredient level). Therapeutic target → disease
  links from TTD. Oral bioavailability predicted with SwissADME rules and HobPre. ITS DNA barcodes and
  phylogenetic trees built with phyloT/iTOL.
- **Size & coverage:** 7,865 plants, 60,222 ingredients, 758 targets, 1,399 diseases, 238 KEGG pathways, 3,013
  GO terms, 1,203 Disease Ontology terms. Plants are mapped to countries on a world map and to traditional
  medicine systems on the web interface (not described quantitatively in the paper).
- **Evaluation / applications:** a case study (*Hypericum perforatum*: DEG reversal for dengue, DNA barcode,
  disease network, phylogeny, bioavailability, trials); comparison with HERB, TCMPG, SuperTCM and others.

## Key findings
1. Data grew **21–107%** over CMAUP-2019: plants 5,654 → **7,865** (+39.1%), ingredients 47,645 → **60,222**
   (+26.4%), targets 436 → **758** (+73.9%), diseases 656 → **1,399** (+113.3%).
2. Plant–disease associations: **428,737** by therapeutic target (up from 263,130), **220,935** by reversal of
   transcriptomic changes, **764** by clinical trials of the plant, **154,121** by clinical trials of plant
   ingredients.
3. **691** clinical trials cover 175 (abstract: 185) individual plants and 334 diseases. There are **14,516**
   ingredient-level trial records for 381 ingredients.
4. **4,649** plants (~60%; abstract says 4,694) are labelled "drug-producing" because they are linked to
   clinical-trial information.
5. DNA barcodes for **3,949** plants. Transcriptomic overlap covers 1,152 targets of 5,765 plants.

## Relevance to research questions
### Q2: Cultural ingredient datasets
CMAUP's plant list includes food and edible plants. Its web interface attaches **countries of occurrence**
(153 on the world map), **countries where the plant is used medicinally** and **traditional medicine systems**
(TCM 2,490 plants, Indian Folk 681, Ayurveda 397, Siddha 367, Unani 274, Sowa-Rigpa 153, Kampo 91). This is a
coarse but global culture → ingredient layer. The downloads do not include it.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
Plant → ingredient → target (with IC50/Ki) → ICD-11 disease, with evidence type per link. This makes CMAUP a
ready-made bridge from a culturally named plant to candidate health effects. Clinical-trial evidence at the
plant level is thin (764 associations). Ingredient-level trial links are broad and noisy.

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables
*Table 1: CMAUP-2019 vs CMAUP-2024. Transcriptomic profiles (new, 20,027 samples, 74 diseases); clinical
trials plant-level 691 and ingredient-level 14,516 (new); DNA barcodes 3,949 (new); diseases 656 → 1,399;
plants 5,654 → 7,865; functional classes 5 → 6 (drug-producing added); ingredients 47,645 → 60,222; targets
436 → 758; KEGG 234 → 238; GO 2,473 → 3,013; DO terms 1,203 (new); plant–disease by target 263,130 →
428,737.*

## Limitations / caveats
- Associations are mostly mechanistic inference (shared targets, DEG overlap), not evidence of efficacy.
- The ingredient-trial layer links a plant to any trial of any compound it contains, including common
  compounds and drugs.
- The paper gives no counts or sources for the geography and traditional-use layers shown on the website. They
  are not downloadable.
- There are inconsistencies between the abstract and the body (185 vs 175 plants in trials; 4,694 vs 4,649
  drug-producing plants).

## Related work to follow
![[Backlog.base#Cited by this paper]]
