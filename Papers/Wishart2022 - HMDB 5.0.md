---
title: "HMDB 5.0: the Human Metabolome Database for 2022"
citekey: "Wishart2022"
authors: ["David S. Wishart", "AnChi Guo", "Eponine Oler", "Fei Wang", "Afia Anjum", "Harrison Peters", "Raynard Dizon", "Zinat Sayeeda", "Siyang Tian", "Brian L. Lee", "et al."]
year: 2022
published: 2021-11-19
venue: "Nucleic Acids Research 50(D1):D622–D631 (Database issue)"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkab1062"
arxiv: ""
doi: "10.1093/nar/gkab1062"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC8728138?pdf=render"
datasets: ["[[HMDB]]"]
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
# HMDB 5.0: the Human Metabolome Database for 2022

> [!abstract] TL;DR
> HMDB 5.0 roughly doubles the Human Metabolome Database, from 114,100 to 217,920 compounds (mostly oxidised lipids,
> cardiolipins and blood-exposome compounds, plus 3,168 food-derived compounds). It rewrites descriptions, expands the
> ChemFOnt functional ontology (which records origin: food / microbial / endogenous, and source organism), and adds
> large predicted spectral libraries and new search and visualisation tools.

## What was built
- **Dataset(s):** [[HMDB]]
- **Sources & construction:** literature scans (2018–2020) plus a targeted 2021 expansion (oxidised lipids,
  cardiolipins, blood-exposome compounds, acylcarnitines, acylamides, bile-acid conjugates, food-derived compounds
  from FooDB, sulfated metabolites, new drugs, microbial metabolites). Up to 130 data fields per MetaboCard are
  generated or collected and partly checked by hand. Descriptions come from hand-written templates and the
  ChemoSummarizer program. The ChemFOnt ontology covers process, role, physiological effect and disposition.
- **Size & coverage:** 217,920 compounds (113,568 added; 9,548 BioTransformer-predicted and 323 erroneous compounds
  removed). ChemFOnt grew to 247 subcategories and 221,454 definitions. More than 19,715 concentrations were added or
  corrected, along with 37,589 experimental MS spectra.
- **Evaluation / applications:** website search (text, structure, mass, spectra); downloads in XML/CSV/SDF/TXT/JSON.

## Key findings
1. Compounds grew from 114,100 to 217,920. The additions include 40,142 oxidised lipids, 52,783 cardiolipins, 14,929
   blood-exposome compounds and 3,168 food-derived compounds.
2. Descriptions were manually rewritten for >800 well-known or disease-associated metabolites, and >200,000 were
   generated from templates.
3. ChemFOnt now gives provenance-backed disposition data, meaning origin (food, microbial, endogenous), source
   species and body location, for every entry.
4. The authors state that this update "precluded further expansion" of the metabolite–disease, metabolite–gene and
   metabolite–SNP collections, so disease links are essentially carried over from HMDB 4.0.

## Relevance to research questions
### Q3: Food compound & health-effect datasets
HMDB links a compound to (a) food/plant origin (ChemFOnt "Disposition > Source > Food / Biological > Plant > …"),
(b) disease associations with PubMed references, and (c) normal/abnormal concentrations in human biofluids. Its ids
(HMDB, FooDB, PubChem, ChEBI, KEGG) connect FooDB-style food composition to [[CTD]] and [[Exposome-Explorer]]. The
disease links are metabolite-as-biomarker associations (altered levels in a disease), not dietary health effects.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- The disease, gene and SNP layers were not updated in 5.0.
- Most new entries are "expected but not quantified" lipids with no human measurement.
- The official downloads now sit behind a Cloudflare challenge (see [[HMDB]]). The licence is non-commercial.

## Related work to follow
![[Backlog.base#Cited by this paper]]
