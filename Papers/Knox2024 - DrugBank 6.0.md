---
title: "DrugBank 6.0: the DrugBank Knowledgebase for 2024"
citekey: "Knox2024"
authors: ["Craig Knox", "Mike Wilson", "Christen M. Klinger", "Mark Franklin", "Eponine Oler", "Alex Wilson", "Allison Pon", "Jordan Cox", "Na Eun Chin", "David S. Wishart"]
year: 2024
published: 2023-11-11
venue: "Nucleic Acids Research (Database issue)"
peer_reviewed: true
url: "https://doi.org/10.1093/nar/gkad976"
arxiv: ""
doi: "10.1093/nar/gkad976"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC10767804?pdf=render"
datasets: ["[[DrugBank]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
cites:
  - "[[HMDB (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/3
  - kind/compound
  - region/global
---
# DrugBank 6.0: the DrugBank Knowledgebase for 2024

> [!abstract] TL;DR
> This is the 2024 update of DrugBank, the reference drug knowledgebase (drugs, targets, pathways, drug–drug and drug–food interactions, spectra). It covers 11,891 drugs. The number of curated drug–food interactions grew from 1,195 to 2,475. The update also adds drug–drug and drug–food interaction checkers. The full data is under CC BY-NC 4.0 and needs a (free academic) account; only the vocabulary and structures are CC0.

## What was built
- **Dataset(s):** [[DrugBank]]
- **Sources & construction:** expert curation from labels, literature and regulatory sources, maintained by the University of Alberta together with OMx Personal Health Analytics.
- **Size & coverage:** 4,563 FDA-approved drugs, 6,231 investigational drugs, 1,413,413 drug–drug interactions and 2,475 drug–food interactions. There are product data from regulators in 13 regions, including Turkey, Indonesia, Malaysia, Thailand and Singapore.
- **Evaluation / applications:** web search including a Drug/Food Interaction search, interaction checkers (up to five drugs; food interactions shown as one sentence per row), an API, and XML/CSV downloads.

## Key findings
1. The number of approved drugs rose from 2,646 to 4,563 (+72%) and investigational drugs from 3,394 to 6,231.
2. Drug–drug interactions rose from 365,984 to 1,413,413.
3. Drug–food interactions rose from 1,195 to 2,475 (reported as a 200% increase). These are short advice sentences such as "Avoid grapefruit products" or "Take with food".
4. Experimental or predicted MS/MS, NMR, CCS, RT and RI data were added for 9,464 of 11,710 small-molecule drugs.

## Relevance to research questions
### Q3: Food compound & health-effect datasets
DrugBank's `food-interactions` field is the standard short clinical guidance per drug. DDID ingested it, and FooDrugs v2 contains 285 DrugBank documents. For the agent, it is the reference to cite when a regional food (grapefruit, liquorice, green tea) meets a drug. It is also the ID hub (DrugBank ID → PubChem/ChEBI/UNII/ATC/RxNorm) that connects the food–drug sets to each other.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- The food interactions are brief advisory sentences keyed to a drug. There are no food IDs, no evidence grading and no citation per statement.
- The full data is non-commercial and account-gated. As of 2026-09-30 academic downloads were disabled (see [[DrugBank]]).

## Related work to follow
![[Backlog.base#Cited by this paper]]
