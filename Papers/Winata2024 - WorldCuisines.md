---
title: "WorldCuisines: A Massive-Scale Benchmark for Multilingual and Multicultural Visual Question Answering on Global Cuisines"
citekey: Winata2024
authors: [Genta Indra Winata, Frederikus Hudi, Patrick Amadeus Irawan, David Anugraha, Rifki Afina Putri, Yutong Wang, Adam Nohejl, Ubaidillah Ariq Prathama, Nedjma Ousidhoum, Afifa Amriani, Anar Rzayev, Anirban Das, "et al."]
year: 2024
published: 2024-10-16
venue: "NAACL 2025 (Best Theme Paper)"
peer_reviewed: true
url: "https://arxiv.org/abs/2410.12705"
arxiv: "2410.12705"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2410.12705"
datasets: ["[[WorldCuisines]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites:
  - "[[Adilazuarda2024 - Survey on measuring culture in LLMs]]"
  - "[[FoodieQA]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
---
# WorldCuisines: A Massive-Scale Benchmark for Multilingual and Multicultural Visual Question Answering on Global Cuisines

> [!abstract] TL;DR
> Builds WC-KB, a curated knowledge base of 2,414 culturally specific dishes (from Wikipedia, with categories,
> countries, areas, descriptions and 6,045 CC images), and from it WC-VQA, a 1M-item VQA benchmark in 30 languages
> and dialects asking VLMs to name a dish and its origin.

## What was built
- **Dataset(s):** [[WorldCuisines]]
- **Sources & construction:** dishes chosen from Wikipedia dish lists (must have their own page and a distinct
  cultural association; generic foods like ice cream excluded); annotators filled metadata (coarse/fine category,
  cuisines, countries, area, region, description) and picked up to 8 licensed Wikimedia images; quality checks on
  country/area; 401 locations and cuisine names translated (GPT-4o + native proofreading); 90 crowd-sourced prompt
  templates in 30 languages.
- **Size & coverage:** 2,414 dishes, 6,045 images, 189 countries; VQA: ~1M training items + 60k and 12k test sets.
- **Evaluation / applications:** Task 1 dish-name prediction (no context / correct context / adversarial context),
  Task 2 location prediction; MCQ and open-ended; many open and proprietary VLMs.

## Key findings
1. Dish entries concentrate in Asia, Europe and North America; Africa, Oceania and Latin America are thinner
   (paper Fig. 3–4).
2. No-context MCQ accuracy varies from about 30% to 80% across VLMs; GPT-4o models are best.
3. Open-ended dish-name prediction is hard: best accuracy under 20% without context.
4. Correct location context helps, adversarial (misleading) context sharply reduces accuracy.
5. Performance drops for lower-resource languages and for predicting specific regional cuisines.

## Relevance to research questions
### Q1: Cultural food datasets
The KB is the broadest open dish → country/region map found so far (all six GCC states, Iran, Turkey, South/East/
Southeast Asia; weaker Central Asia), with descriptions that name main ingredients. It has no structured ingredients
or recipes, so it needs linking (e.g. via Wikidata to [[FmLAMA]]).

See [[Q1 Cultural food datasets]]

## Key figures & tables
Not extracted (no local PDF).

## Limitations / caveats
- Wikipedia-based dish selection favours well-documented cuisines.
- VQA is generated from the KB with templates, so it adds evaluation scale, not new food knowledge.
- Author list abbreviated here (large open-source collaboration).

## Related work to follow
![[Backlog.base#Cited by this paper]]
