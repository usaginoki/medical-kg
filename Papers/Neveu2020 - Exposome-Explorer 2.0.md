---
title: "Exposome-Explorer 2.0: an update incorporating candidate dietary biomarkers and dietary associations with cancer risk"
citekey: "Neveu2020"
authors: ["Vanessa Neveu", "Geneviève Nicolas", "Reza M. Salek", "David S. Wishart", "Augustin Scalbert"]
year: 2020
published: 2019-11-14
venue: "Nucleic Acids Research 48(D1):D908–D912 (Database issue)"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkz1009"
arxiv: ""
doi: "10.1093/nar/gkz1009"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC7145555?pdf=render"
datasets: ["[[Exposome-Explorer]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/3
  - kind/compound
  - region/global
---
# Exposome-Explorer 2.0: an update incorporating candidate dietary biomarkers and dietary associations with cancer risk

> [!abstract] TL;DR
> This is the second release of IARC's manually curated database of dietary and pollutant biomarkers measured in
> human populations. It adds candidate food-intake biomarkers from metabolomics studies and 1,356 associations between
> dietary biomarkers and cancer risk from prospective epidemiological studies. It also reorganises the compound, food,
> biospecimen, analytical-method and cancer (ICD-10) classifications.

## What was built
- **Dataset(s):** [[Exposome-Explorer]]
- **Sources & construction:** two literature searches. (1) Metabolomics studies of dietary biomarkers (20
  publications, 2010–2016). (2) Prospective epidemiological studies of biomarker–cancer associations, focused on
  vitamins, polyphenols and fatty acids (313 publications, 1984–2018). Data were entered through a password-protected
  annotation interface. Only peer-reviewed human studies were included. Compounds are classified by exposure type
  (Diet / Pollution) and also get ChemOnt classes via ClassyFire.
- **Size & coverage:** 908 biomarkers (from 692 in release 1.0, which drew on 480 publications); 185 candidate
  dietary biomarkers with 403 food-intake associations; 1,356 biomarker–cancer associations. Country is recorded per
  population.
- **Evaluation / applications:** a web interface with classification trees, typeahead search, structure search and
  CSV downloads.

## Key findings
1. Biomarker count rose from 692 (v1.0) to 908, with 185 metabolomics-derived candidate dietary biomarkers linked to
   foods through 403 associations.
2. 1,356 biomarker–cancer associations were collated from 313 prospective studies (1984–2018).
3. New data came from 332 publications. 32 new epidemiological dietary biomarkers were added.
4. Some metabolomic biomarkers have undetermined structures (e.g. urolithin A 3- or 8-glucuronide) and are stored
   without a structure.

## Relevance to research questions
### Q3: Food compound & health-effect datasets
This is the only resource in the set with **human population evidence on both hops**: food intake ↔ biomarker in
blood/urine (correlations, metabolomic associations), and biomarker ↔ cancer risk in cohorts (e.g. tea catechins and
breast/gastric cancer in the JPHC and Shanghai cohorts). It complements [[CTD]]'s mechanistic links and [[HMDB]]'s
food-origin annotations, with which it shares HMDB/FooDB/PubChem ids.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- For cancer associations the database lists the studies and pairs tested. "For more details on the statistical
  significance, association trends, or confounding adjustments, hyperlinks to the original publications are
  provided", so effect sizes are not in the downloadable table.
- Candidate biomarkers from only 20 metabolomics papers. The cancer studies focus on vitamins, polyphenols and fatty
  acids.
- Mostly European, US and East Asian cohorts.

## Related work to follow
![[Backlog.base#Cited by this paper]]
