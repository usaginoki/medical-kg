---
title: "IMPPAT 2.0: An Enhanced and Expanded Phytochemical Atlas of Indian Medicinal Plants"
citekey: "Vivek-Ananth2023"
authors: ["R. P. Vivek-Ananth", "Karthikeyan Mohanraj", "Ajaya Kumar Sahoo", "Areejit Samal"]
year: 2023
published: 2023-02-23
venue: "ACS Omega 8(9):8827–8845"
peer_reviewed: true
url: "https://pubs.acs.org/doi/10.1021/acsomega.3c00156"
arxiv: ""
doi: "10.1021/acsomega.3c00156"
pdf: ""
pdf_url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC9996785/pdf/ao3c00156.pdf"
datasets: ["[[IMPPAT]]"]
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
# IMPPAT 2.0: An Enhanced and Expanded Phytochemical Atlas of Indian Medicinal Plants

> [!abstract] TL;DR
> The paper describes version 2.0 of IMPPAT, a manually curated database of Indian medicinal plants. It
> links 4,010 plants by plant part to 17,967 phytochemicals and 1,095 standardised therapeutic uses, built from
> 100+ traditional-medicine books and 7,000+ articles. It adds cheminformatic annotation (drug-likeness, ADMET,
> scaffolds) and predicted human targets. Version 3.0 (September 2026, no paper yet) extends it further; see
> [[IMPPAT]].

## What was built
- **Dataset(s):** [[IMPPAT]] (v2.0; the vault note describes v3.0)
- **Sources & construction:** phytochemicals from 70 specialised books (61 not used in v1.0, e.g. *The Wealth
  of India*, Indian pharmacopoeias, *Reviews on Indian Medicinal Plants*), 7,000+ research articles and one
  phytochemical database. Therapeutic uses come from 146 books and were manually standardised against MeSH,
  ICD-11, UMLS and Disease Ontology. Human targets come from STITCH (score ≥ 700).
- **Size & coverage:** 4,010 plants, 17,967 phytochemicals, 189,386 plant–part–phytochemical and 89,733
  plant–part–therapeutic-use associations, and 27,365 predicted phytochemical–target links (1,294 compounds,
  5,042 proteins).
- **Evaluation / applications:** drug-likeness filtering, scaffold diversity compared with other
  natural-product libraries, similarity to approved drugs, overlap with TCM resources.

## Key findings
1. More than doubles v1.0: 1,742 → 4,010 plants and 9,596 → 17,967 phytochemicals. Plant–phytochemical links
   rose 5-fold (27,074 → 124,995).
2. 1,335 phytochemicals pass all six drug-likeness rules; only 11 of them are already approved drugs.
3. 5,179 scaffolds at the graph/node/bond level. IMPPAT ranks third of seven natural-product libraries for
   scaffold diversity.
4. Only 130 drug-like phytochemicals have Tanimoto ≥ 0.5 similarity to an approved drug, so most of the space
   is novel.
5. Only 18.6% (3,342) of phytochemicals overlap with TCM-Mesh, which suggests Indian and Chinese
   pharmacopoeias are complementary.

## Relevance to research questions
### Q2: Cultural ingredient datasets
Culinary plants (turmeric, okra, amla, fenugreek, ginger) are in IMPPAT with part-level phytochemistry and
traditional-system labels (Ayurveda, Siddha, Unani, Sowa Rigpa, Homeopathy). This gives a culturally grounded
South Asian ingredient vocabulary.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
It provides plant → compound → target, and plant → traditional therapeutic use mapped to MeSH/ICD-11/DO
vocabularies. Version 3.0 replaces the predicted targets with experimentally supported ones.

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables

## Limitations / caveats
- Therapeutic uses are traditional claims, not clinical evidence. The 2.0 targets are predicted (STITCH).
- 3D structures could not be generated for 57 phytochemicals, and ADMET predictions are missing for 493
  compounds because of SMILES length limits.
- Vernacular-language formulation sources were hard to collect, and database licensing limited integration of
  other resources.
- CC BY-NC-ND licence.

## Related work to follow
![[Backlog.base#Cited by this paper]]
