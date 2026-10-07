---
title: "The World Wide recipe: A community-centred framework for fine-grained data collection and regional bias operationalisation"
citekey: Magomere2024
authors: [Jabez Magomere, Shu Ishida, Tejumade Afonja, Aya Salama, Daniel Kochin, Foutse Yuehgoh, Imane Hamzaoui, Raesetje Sefala, Aisha Alaagib, Samantha Dalal, Beatrice Marchegiani, Elizaveta Semenova, Lauren Crais, Siobhan Mackenzie Hall]
year: 2024
published: 2024-06-13
venue: "FAccT 2025 (ACM Conference on Fairness, Accountability, and Transparency)"
peer_reviewed: true
url: "https://arxiv.org/abs/2406.09496"
arxiv: "2406.09496"
doi: "10.1145/3715275.3732019"
pdf: ""
pdf_url: "https://arxiv.org/pdf/2406.09496"
datasets: ["[[World Wide Dishes]]"]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - q/2
---
# The World Wide recipe: A community-centred framework for fine-grained data collection and regional bias operationalisation

> [!abstract] TL;DR
> Builds **World Wide Dishes** (765 dishes, names in 131 languages, 201 contributors from 106 countries) through a
> community website instead of web scraping, then uses it to show that text-to-image models and LLMs know far less
> about (especially African) home dishes than about US ones.

## What was built
- **Dataset(s):** [[World Wide Dishes]]
- **Sources & construction:** a purpose-built website (worldwidedishes.com) where volunteers entered dishes from
  their own culture: local name, language, countries/regions/cultures, meal time, dish type, occasion, utensils,
  drink, ingredients, recipe link, optional CC image; recruited through grassroots AI communities; manual review
  and cleaning by the authors.
- **Size & coverage:** 765 dishes, 131 languages, 106 contributor countries; 62% of contributors used mobile phones.
  Two test suites: 30 dishes each for Algeria, Cameroon, Kenya, Nigeria, South Africa and the US.
- **Evaluation / applications:** community review of Stable Diffusion / DALL-E 2 / DALL-E 3 dish images; VQA and
  CLIP-based automated bias probes; LLM probing (GPT-3.5, Llama 3 8B/70B) of dish → country and ingredients.

## Key findings
1. More than 50% of WWD dishes are not found in common web-scraped sources, and WWD metadata is more detailed than
   Wikimedia-based sets; the web-scraped WorldCuisines tracks internet access by country.
2. T2I models generate recognisable US dishes far more often than dishes from the five African countries, and
   depict African dishes with stereotyped "African-style" crockery and settings.
3. Reviewers reported that DALL-E 2 in particular made African dishes look unappetising, rotten or inedible; automated CLIP descriptor scores tie negative descriptors to African dishes and positive ones to European dishes.
4. LLMs score lowest for African dishes on predicting country and ingredients from the dish name, and sometimes
   call real dishes "fictional".

## Relevance to research questions
### Q1: Cultural food datasets
A rare non-web-scraped dish list with local names, meal times and occasions (Ramadan, Eid) — but Africa-heavy and
with only 1–2 dishes for each GCC and Central Asian country.

See [[Q1 Cultural food datasets]]

### Q2: Cultural ingredient datasets
Every dish has a free-text ingredient list, giving dish → ingredient links (no amounts) that can be aggregated to
country-level ingredient profiles after normalisation.

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables
Not extracted (no local PDF).

## Limitations / caveats
- Small and unevenly distributed; systematic coverage of all regions was not achievable with volunteer collection.
- Results use one prompt template per experiment; generated images are not released.
- Terms of use restrict using the data to build training-data generators.

## Related work to follow
![[Backlog.base#Cited by this paper]]
