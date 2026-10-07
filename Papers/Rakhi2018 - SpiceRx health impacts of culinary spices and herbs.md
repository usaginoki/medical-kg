---
title: "SpiceRx: an integrated resource for the health impacts of culinary spices and herbs"
citekey: "rakhi2018spicerx"
authors: ["Rakhi N.K.", "Rudraksh Tuwani", "Neelansh Garg", "Jagriti Mukherjee", "Ganesh Bagler"]
year: 2018
published: 2018-02-28
venue: "bioRxiv"
peer_reviewed: false
url: "https://doi.org/10.1101/273599"
arxiv: ""
doi: "10.1101/273599"
pdf: ""
pdf_url: "https://www.biorxiv.org/content/10.1101/273599v1.full.pdf"
datasets: ["[[SpiceRx]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites:
  - "[[KNApSAcK Family (candidate)]]"
  - "[[Phenol-Explorer (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# SpiceRx: an integrated resource for the health impacts of culinary spices and herbs

> [!abstract] TL;DR
> SpiceRx combines three kinds of link for culinary spices and herbs:
> - spice → disease associations text-mined from 28 M MEDLINE abstracts (dictionary spice tagging, TaggerOne disease NER, CNN relation extraction with positive/negative/neutral classes)
> - spice → phytochemical data from KNApSAcK and Phenol-Explorer
> - phytochemical → disease links from CTD
>
> It is served as a Django/PostgreSQL web resource.

## What was built
- **Dataset(s):** [[SpiceRx]]
- **Sources & construction:** a dictionary of 188 spices and herbs; 28 M MEDLINE abstracts; TaggerOne for diseases; a CNN relation classifier trained on 6,712 manually annotated sentences (2,669 positive, 301 negative, the rest neutral); KNApSAcK and Phenol-Explorer for phytochemicals; CTD for chemical-disease links; MeSH hierarchy for disease classes.
- **Size & coverage:** 11,750 abstracts; 8,957 disease associations (8,172 positive, 783 negative) for 152 spices × 848 MeSH diseases; 866 phytochemicals (570 bioactive) for 142 spices; 2,042 spice-phytochemical links.
- **Evaluation / applications:** search by spice, disease (MeSH name/category/sub-category/id) or phytochemical (name, structure, ALogP). Disease-specific culinary recommendations and mechanism exploration.

## Key findings
1. It has 8,957 literature-supported spice-disease associations, 91% of them positive (8,172) and 783 negative.
2. About 20% of spice-disease associations are "triangular": a phytochemical of the spice is independently linked to the same disease in CTD.
3. 866 phytochemicals are linked to 142 spices through 2,042 associations.
4. From the live-site statistics: Garlic (782 positive / 40 negative abstracts), Ginkgo (554/25), Turmeric (515/6) and Ginger (505/3) have the most evidence, and Liquorice has the most negative evidence (123).

## Relevance to research questions
### Q2: Cultural ingredient datasets
It gives a spice/herb vocabulary keyed by NCBI taxon, with strong South Asian and Middle Eastern coverage (ajwain, asafoetida, fenugreek, sumac, golpar, mastic, saffron).

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
It offers direct, PMID-backed spice → disease effects with direction, plus phytochemical-level mechanisms via CTD. This is the most directly usable effect layer among the CoSyLab resources.

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables
Figure 1: tripartite spice-phytochemical-disease schema.

## Limitations / caveats
- The associations are text-mined at abstract level, with no dose information and no distinction between in-vitro, animal and human studies. The authors note that effects depend on quantity, which is not captured.
- This is a preprint. The Bioinformatics publication mentioned in the text was not found on Crossref.

## Related work to follow
![[Backlog.base#Cited by this paper]]
