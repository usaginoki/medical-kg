---
title: "Commonsense Reasoning in Arab Culture"
citekey: Sadallah2025
authors: [Abdelrahman Sadallah, Junior Cedric Tonga, Khalid Almubarak, Saeed Almheiri, Farah Atif, Chatrine Qwaider, Karima Kadaoui, Sara Shatnawi, Yaser Alesh, Fajri Koto]
year: 2025
published: 2025-02-18
venue: "ACL 2025"
peer_reviewed: true
url: "https://arxiv.org/abs/2502.12788"
arxiv: "2502.12788"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2502.12788"
datasets: ["[[ArabCulture]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites: []
cited_by: []
cited_by_count: 22
tags:
  - type/paper
  - relevance/core
  - q/1
---
# Commonsense Reasoning in Arab Culture

> [!abstract] TL;DR
> Introduces **ArabCulture**, 3,482 native-written MSA commonsense items (premise + 3 completions) from 13 Arab
> countries across 12 daily-life topics, and shows that Arabic and multilingual LLMs struggle with culture-specific
> reasoning, especially for Levantine and country-specific items.

## What was built
- **Dataset(s):** [[ArabCulture]]
- **Sources & construction:** 26 hired native workers (2 per country; ≥10 years residence, parents from the
  country) wrote 150 two-sentence stories each on pre-defined topics; country representatives reviewed; peer
  validation by MCQ (disagreements discarded); country-specific vs shared annotation. 3,900 planned → 3,606 after
  QC round 1 → 3,482 final.
- **Size & coverage:** 3,482 items; 13 countries in 4 regions (Gulf: Saudi Arabia, Yemen, UAE; Levant: Syria,
  Jordan, Palestine, Lebanon; North Africa: Morocco, Algeria, Tunisia, Libya; Nile Valley: Egypt, Sudan), ~82% of the
  Arab population; 12 topics / 54 sub-topics, Food being the largest (breakfast, lunch, dinner, sahoor, iftar,
  dessert, fruits, snacks).
- **Evaluation / applications:** zero-shot MCQ and sentence completion with none / region / region+country location
  context; Arabic-centric and multilingual LLMs.

## Key findings
1. Best open models reach ~80% MCQ accuracy (Qwen-2.5-72B-Instruct 80%, AceGPT-v2-32B 79.7%, Llama-3.3-70B 75.4%);
   GPT-4o is higher; Arabic-centric models (e.g. Jais) do not consistently beat multilingual ones.
2. Sentence completion is much less reliable than MCQ (Qwen-2.5-32B: 75.2% MCQ vs 37.6% completion).
3. Adding region/country context has mixed effects (Jais-30B −6 points; Qwen-2.5-14B 55.2% → 61.6%).
4. Jordan items exceed 90% for all models; Lebanon and Tunisia are hardest (AceGPT-v2 63.6% / 62.7%); the Levant is
   the hardest region; country-specific items are harder (−10 points for GPT-4o in the Nile Valley).

## Relevance to research questions
### Q1: Cultural food datasets
The Food topic (724 items) records typical meals, Ramadan iftar/sahoor foods and desserts per country, including
Saudi Arabia and the UAE — rare native-written GCC meal-pattern data, but as short Arabic MCQ sentences rather than
dish/ingredient records.

See [[Q1 Cultural food datasets]]

## Key figures & tables
Not extracted (no local PDF).

## Limitations / caveats
- Two annotators per country; MSA only (no dialects); no Qatar, Kuwait, Bahrain, Oman, Iraq.
- Reasoning-oriented MCQ; wrong options are synthetic.

## Related work to follow
![[Backlog.base#Cited by this paper]]
