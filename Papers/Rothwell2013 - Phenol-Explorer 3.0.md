---
title: "Phenol-Explorer 3.0: a major update of the Phenol-Explorer database to incorporate data on the effects of food processing on polyphenol content"
citekey: Rothwell2013
authors: [Joseph A. Rothwell, Jara Perez-Jimenez, Vanessa Neveu, Alexander Medina-Remón, Nouha M'hiri, Paula García-Lobato, Claudine Manach, Craig Knox, Roman Eisner, David S. Wishart, Augustin Scalbert]
year: 2013
published: 2013-10-07
venue: "Database (Oxford)"
peer_reviewed: true
url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3792339/"
arxiv: ""
doi: "10.1093/database/bat070"
pdf: ""
pdf_url: "https://pmc.ncbi.nlm.nih.gov/articles/PMC3792339/pdf/bat070.pdf"
datasets: ["[[Phenol-Explorer]]"]
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
---
# Phenol-Explorer 3.0: a major update of the Phenol-Explorer database to incorporate data on the effects of food processing on polyphenol content

> [!abstract] TL;DR
> Third release of Phenol-Explorer (IARC/INRA + Wishart lab), the only free web database of polyphenol contents in foods
> and their in-vivo metabolism/pharmacokinetics. Version 3.0 adds retention factors describing how cooking and processing
> change polyphenol contents, compiled by systematic literature review.

## What was built
- **Dataset(s):** [[Phenol-Explorer]]
- **Sources & construction:** systematic search of Web of Knowledge (to April 2012); values extracted from peer-reviewed
  papers, evaluated, and entered into new tables linked to the existing relational design. The effect of processing is
  expressed as retention factors (proportion of a polyphenol retained after processing, adjusted for water change). All data are traceable to the source publications.
- **Size & coverage:** >100 foods, 161 polyphenols or groups before/after processing, 129 publications; 1,253 final
  retention factors aggregated from 4,626 published values. The composition module (v1.0) had 502 polyphenols in 452
  foods; v2.0 added metabolism/pharmacokinetics from >200 intervention studies (humans and animals). No country labels.
- **Evaluation / applications:** estimating polyphenol exposure from dietary surveys more accurately (e.g. cooked vs raw foods).

## Key findings
1. 1,253 retention factors from 4,626 published values; boiling, steaming, refrigeration and room-temperature storage are the most studied domestic processes.
2. Fruit and vegetable groups and their main polyphenols dominate; flavonols and hydroxycinnamic acids are the most studied sub-classes.
3. Retention can exceed 1, e.g. 2.39 for quercetin aglycone in cauliflower after blanching (better extractability).
4. The current site (v3.6) reports 38,063 content values, 458 foods, 501 polyphenols; 4,296 retention factors; 424 intervention studies (statistics page, 2026-09-30).

## Relevance to research questions
### Q3: Food compound & health-effect datasets
Gives reliable, referenced amounts for polyphenols in spices and staples of the priority regions (e.g. curcumin 2,213.57
mg/100 g in dried turmeric) and, through the metabolism module, which metabolites reach human plasma/urine. Health outcomes
are not included, so it must be joined (PubChem/ChEBI) to FooDB/CTD for effects. The retention factors let the agent
adjust for cooking method.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- Retention factors from different methods may not be comparable; aggregated values should be assessed per use (authors).
- Literature-based means, not nationally representative; the database has not been updated since ~2015–2016 (v3.6).
- Metabolism and retention data are web-only (not in the bulk downloads).

## Related work to follow
![[Backlog.base#Cited by this paper]]
