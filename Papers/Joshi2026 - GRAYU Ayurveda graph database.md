---
title: "GRAYU: graph-based database integrating Ayurvedic formulations, medicinal plants, phytochemicals and diseases"
citekey: "Joshi2026"
authors: ["Sarthak Joshi", "Aditi Pathak", "Dheemanth Reddy Regati", "Revathy Menon", "Deepthi S. Ajith", "Aditya Sheshadri", "Neerja Viswanathan", "Poulomi Ray", "Vimarishi Koul", "Pratishruti Panda", "Shriya Anand Bhambore", "Shailya Verma", "Ananya Sinha", "K. Mohamed Shafi", "Murugavel Pavalam", "Ramanathan Sowdhamini"]
year: 2026
published: 2026-01-22
venue: "Frontiers in Pharmacology 16:1727224"
peer_reviewed: true
url: "https://www.frontiersin.org/articles/10.3389/fphar.2025.1727224/full"
arxiv: ""
doi: "10.3389/fphar.2025.1727224"
pdf: ""
pdf_url: "https://www.frontiersin.org/articles/10.3389/fphar.2025.1727224/pdf"
datasets: ["[[GRAYU]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites:
  - "[[BATMAN-TCM]]"
  - "[[CMAUP (candidate)]]"
  - "[[ETCM]]"
  - "[[HERB (candidate)]]"
  - "[[HMDB (candidate)]]"
  - "[[IMPPAT (candidate)]]"
  - "[[OSADHI]]"
  - "[[PubChem]]"
  - "[[SymMap (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# GRAYU: graph-based database integrating Ayurvedic formulations, medicinal plants, phytochemicals and diseases

> [!abstract] TL;DR
> The paper builds GRAYU, a Neo4j knowledge graph with a Flask and Cytoscape.js web portal. It connects 1,039
> Ayurvedic formulations to 12,743 plants, 129,542 phytochemicals and 13,480 diseases mapped to MeSH and the
> Disease Ontology. It integrates IMPPAT 2.0, CMAUP, NPASS, OSADHI, FooDB, HMDB and PubChem with three official
> Ayurvedic texts. The portal supports multi-step graph queries.

## What was built
- **Dataset(s):** [[GRAYU]]
- **Sources & construction:** formulations from the Ayurvedic Standard Treatment Guidelines, the Ayurvedic
  Pharmacopoeia of India and the Ayurvedic Formulary of India. Plants and phytochemicals from CMAUP, FooDB,
  HMDB, IMPPAT 2.0, NPASS and OSADHI, consolidated on PubChem. Diseases from the MeSH Diseases branch and DOID.
- **Size & coverage:** 157,010 nodes and 1,520,687 edges. FOUND_IN about 1,370,257 · ASSOCIATED_WITH_DISEASE
  116,531 · IS_INGREDIENT_IN 2,389 · formulation–disease 4,087 · plus SUBCLASS_OF and HAS_SYMPTOM.
- **Evaluation / applications:** a web portal (search, browse, interactive graph, advanced multi-step search)
  with example queries such as finding the plants and compounds shared between formulations for one disease.

## Key findings
1. 1,039 formulations, 12,743 plants, 129,542 phytochemicals, 13,480 diseases.
2. About 1.37 M phytochemical–plant edges dominate the 1.52 M-edge graph.
3. 116,531 plant–disease associations versus only 4,087 formulation–disease links: the traditional formulation
   layer is thin compared with the database-derived plant layer.
4. Only 2,389 plant–formulation ingredient links for 1,039 formulations, reflecting incomplete digitisation of
   the pharmacopoeia volumes.

## Relevance to research questions
### Q2: Cultural ingredient datasets
Links Ayurvedic formulations and their plant ingredients (with quantities) to vernacular plant names and to the
Indian states where each plant occurs. This is a culturally specific ingredient layer for India.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
Plant → disease edges carry typed evidence (clinical trials, target overlap, transcriptome reversal,
literature) and standard disease ids (MeSH, DOID, ICD-11). This is one of the most directly usable
compound-to-health bridges for South Asian ingredients.

See [[Q3 Food compound & health-effect datasets]]

## Key figures & tables

## Limitations / caveats
- Evidence quality is heterogeneous across the source databases, and polyphenols (PAINS) are prone to false
  positive associations.
- Some Ayurvedic Pharmacopoeia volumes are incompletely digitised, and there are no standardised
  ethnopharmacological activity labels.
- Health effects come only through paths via plants (no direct phytochemical → disease edge).
- Mapping Ayurvedic disease concepts to modern ontologies is approximate.
- Preparation methods and formulation proportions are not modelled systematically.
- Data are available through the web portal only. The ToS ask for bulk access to be arranged by email.

## Related work to follow
![[Backlog.base#Cited by this paper]]
