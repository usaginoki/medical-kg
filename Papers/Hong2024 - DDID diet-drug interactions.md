---
title: "DDID: a comprehensive resource for visualization and analysis of diet–drug interactions"
citekey: "Hong2024"
authors: ["Yanfeng Hong", "Hongquan Xu", "Yuhong Liu", "Sisi Zhu", "Chao Tian", "Gongxing Chen", "Feng Zhu", "Lin Tao"]
year: 2024
published: 2024-05-06
venue: "Briefings in Bioinformatics"
peer_reviewed: true
url: "https://doi.org/10.1093/bib/bbae212"
arxiv: ""
doi: "10.1093/bib/bbae212"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC11074590?pdf=render"
datasets: ["[[DDID]]"]
topics: [cultural-food-health]
questions: [Q3]
relevance: core
cites:
  - "[[FooDB (candidate)]]"
  - "[[FooDrugs (candidate)]]"
  - "[[SymMap (candidate)]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/3
  - kind/compound
  - tradmed/tcm
  - region/east-asia
  - region/global
---
# DDID: a comprehensive resource for visualization and analysis of diet–drug interactions

> [!abstract] TL;DR
> The Diet-Drug Interactions Database (DDID) is a manually curated, openly downloadable knowledge base with 23,950 food/herb–drug interaction records. It covers 1,338 foods and herbs (most of them Chinese herbs) and 1,516 drugs. The records come from 1,485 PubMed articles, FDA package inserts and DrugBank. The authors rated each interaction as positive, negative, no effect, harmful or possible, using FDA bioequivalence criteria, and linked the entities to DrugBank, FooDB, PubChem, NPASS, HERB, SymMap and NCBI Taxonomy.

## What was built
- **Dataset(s):** [[DDID]]
- **Sources & construction:** PubMed keyword searches ("drug + food + interactions", "drug + herb + interactions", "drug + herbal ingredient + interactions"). From these, 1,485 articles were reviewed and extracted by hand. FDA labels of oral drugs approved over the past 20 years were reviewed. The DrugBank SQL dump was parsed for its drug–food interaction statements. Entities were then mapped to external databases.
- **Size & coverage:** 23,950 interactions (the text also says 23,915) from 3,013 literature reports. It covers 212 unique foods, 14 common food ingredients (e.g. alcohol), 44 meal types ("food combinations") and 1,068 herbs from 155 plant families. There are 171 food/herb ingredients and 112 targets.
- **Evaluation / applications:** a web interface for search and browse by food, herb or drug, plus bulk CSV download. The paper includes case studies on grapefruit (228 drugs) and ginseng. It proposes DDID as training data for AI models that predict diet–drug interactions.

## Key findings
1. There are 23,950 interactions: 1,338 foods/herbs × 1,516 drugs. This is roughly 20× the 1,195 drug–food interactions in DrugBank 5.0.
2. Five effect classes are defined. Human bioequivalence studies are classed positive or negative using the FDA 80–125% AUC/Cmax window. Because animal results translate poorly (about 8%), animal studies are mostly classed "no effect" or "possible". "Harmful" marks serious side effects, for example celery extract raising venlafaxine levels and triggering mania.
3. Fabaceae is the top herb family. Phenylpropanoids and polyketides account for 47.5% (11,207) of the interactions.
4. The main mechanisms are CYP450 (54.7%, 10,947 interactions), P-gp (20.4%, 4,087) and OATP (9.3%, 1,869).
5. The authors position DDID as fully hand-curated, in contrast with FooDrugs (about 1.1M text-mined entries, little manual review).

## Relevance to research questions
### Q3: Food compound & health-effect datasets
DDID links culturally important foods and TCM herbs to drugs, with a graded effect, a mechanism (target) and a PubMed/FDA citation. Examples: grapefruit, liquorice, green tea, turmeric, fenugreek, dates, pomegranate, black seed, jujube and ginseng. For each food or herb it tells the agent which medicines to warn about. Its herb table carries Chinese/Pinyin names, TCM properties, meridians and indications, and flags herbs on China's food–medicine homology list, so it also acts as a small TCM ingredient resource.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- Most records are herb–drug interactions (19,085 herb vs 4,865 food rows). Most experiments are in rats (12,335 rows), not humans (3,647).
- "Possible" is by far the largest class (17,827), so most records give no firm clinical verdict.
- Foods have no country or cuisine labels. The Chinese focus comes from the herb list.
- DrugBank-derived rows map generic statements to single foods. For example, "limit caffeine intake" is attached to *Fructus Evodiae* and to tea.

## Related work to follow
![[Backlog.base#Cited by this paper]]
