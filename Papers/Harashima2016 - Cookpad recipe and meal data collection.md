---
title: "A Large-scale Recipe and Meal Data Collection as Infrastructure for Food Research"
citekey: "Harashima2016"
authors: ["Jun Harashima", "Michiaki Ariga", "Kenta Murata", "Masayuki Ioki"]
year: 2016
published: 2016-05-23
venue: "LREC 2016, pp. 2455–2459"
peer_reviewed: true
url: "https://aclanthology.org/L16-1389/"
arxiv: ""
doi: ""
pdf: ""
pdf_url: "https://aclanthology.org/L16-1389.pdf"
datasets: ["[[NII Cookpad Dataset]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
---
# A Large-scale Recipe and Meal Data Collection as Infrastructure for Food Research

> [!abstract] TL;DR
> Cookpad Inc. describes the corpus it released through NII's IDR:
> - ~1.72M Japanese recipes and ~36k meals (combinations of recipes) uploaded to cookpad.com up to Sept 2014,
> - ~1,100 user categories,
> - ~10M "tsukurepo" cook-reports.
>
> It is distributed as a 12-table MySQL dump to researchers at public institutions.

## What was built
- **Dataset(s):** [[NII Cookpad Dataset]]
- **Sources & construction:**
  - **Recipes** were entered on Cookpad's upload template: title (≤ 20 characters), description, ingredients with quantities and servings, steps, advice, history, plus recipe id, author id and upload date.
  - **Meals** use a template with title, noteworthy points, cooking time, advice, main dishes and side dishes, plus ids and date.
  - Related data: categories and user votes.
  - Images are not included.
- **Size & coverage:** ~1,715,000 recipes; ~36,000 meals; ~146,000 recipes classified into ~1,100 categories; ~10M reviews. All Japanese.
- **Evaluation / applications:** a resource paper, with no experiments. It compares scale with the Rakuten (~440k), Yummly/NTCIR (~100k) and flow-graph (266) corpora, and reports uptake.

## Key findings
1. It was the largest recipe corpus of its time: ~1.715M recipes, against ~440k in Rakuten data and ~100k in the NTCIR Yummly data.
2. It is the first public corpus with **meal data** (~36k meals linking main and side dishes).
3. Uptake: between release in Feb 2015 and Feb 2016, 82 research groups at 56 universities obtained it.
4. It is distributed as a MySQL dump of 12 tables (6 recipe, 6 meal), only to researchers at public institutions, for research purposes.

## Relevance to research questions
### Q1: Cultural food datasets
- Everyday **Japanese home cooking** at population scale, with structured quantities and servings.
- Meal composition (which dishes are eaten together) fits the agent's need to reason about whole meals, not single dishes, e.g. the sodium load of a typical 一汁三菜 ("one soup, three dishes") meal.
- Access needs an institutional contract, and the NII terms restrict feeding the data to external LLM services.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- The data stops in Sept 2014 and comes from Cookpad's user base only.
- No images, no nutrition, no regional labels.
- Access requires an application and contract. The paper gives no column-level schema.

## Related work to follow
![[Backlog.base#Cited by this paper]]
