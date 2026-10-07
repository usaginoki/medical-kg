---
title: "Does Mapo Tofu Contain Coffee? Probing LLMs for Food-related Cultural Knowledge"
citekey: Zhou2024
authors: [Li Zhou, Taelin Karidi, Wanlong Liu, Nicolas Garneau, Yong Cao, Wenyu Chen, Haizhou Li, Daniel Hershcovich]
year: 2024
published: 2024-04-10
venue: "NAACL 2025"
peer_reviewed: true
url: "https://arxiv.org/abs/2404.06833"
arxiv: "2404.06833"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2404.06833"
datasets: ["[[FmLAMA]]"]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
cites: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - q/2
---
# Does Mapo Tofu Contain Coffee? Probing LLMs for Food-related Cultural Knowledge

> [!abstract] TL;DR
> Builds **FmLAMA** by querying Wikidata (SPARQL) for dishes with a country of origin and "has part(s)" ingredients
> (33,600 dish instances, 128 cultural groups, 250 languages) and uses it to probe LLMs for dish → ingredient
> knowledge across cultures and prompt languages.

## What was built
- **Dataset(s):** [[FmLAMA]]
- **Sources & construction:** SPARQL over Wikidata food items; properties "country of origin", "has part(s)"
  (ingredients), plus "made from material" and "image"; one instance per dish label language; filtered
  sub-datasets per probing language where dish and ingredient labels exist in all six languages.
- **Size & coverage:** 33,600 dish instances, 128 cultural (country) groups, 250 languages; mean 2.04
  ingredients per dish; English has the most dishes (2,804); Italy the most instances (2,975); only 8 countries
  have >200 instances.
- **Evaluation / applications:** LAMA-style masked ingredient prediction with 5 templates (± country context) in
  en, zh, ar, ko, ru, he and code-switched prompts; metrics mAP, mWS (FastText similarity) and a manual/GPT-4o
  evaluation score; models BERT/mBERT, T5/mT5, Qwen2, Llama2, Llama3.

## Key findings
1. Decoder-only LLMs recall food ingredients much better than encoder-only and encoder-decoder models.
2. With English prompts, US and Indian dishes score best — a bias towards US/English-speaking cultures that
   weakens with prompts in other languages.
3. Adding the dish's country to the prompt ("In [C], [X] is a dish made with [Y]") improves probing scores.
4. Probing performance barely correlates with the number of dishes per country in Wikidata.
5. Error types: coarse (foreign ingredient, e.g. coffee in a Chinese dish), fine-grained (wrong local ingredient,
   e.g. Chinese wine in mapo tofu), inconsistent; rice, wheat and flour dominate Llama3's wrong guesses.

## Relevance to research questions
### Q1: Cultural food datasets
Gives a multilingual dish → origin-country list keyed on Wikidata QIDs (2,818 unique dishes), strong for Turkey,
India, Japan, China, Indonesia; near-empty for the Gulf and Central Asia.

See [[Q1 Cultural food datasets]]

### Q2: Cultural ingredient datasets
Dish → ingredient triples (Wikidata "has part(s)") in up to 248 languages; aggregating by origin gives per-country
ingredient usage. Lists are short (main ingredients only).

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables
Not extracted (no local PDF).

## Limitations / caveats
- Wikidata coverage is incomplete (soy sauce chicken lists only chicken) and ingredient labels can be generic (oil).
- Non-standard recipes vary by cook; mWS relies on FastText, which lacks vectors for some Chinese/Korean terms.
- Cross-lingual aligned knowledge is scarce, limiting the multilingual analysis.

## Related work to follow
![[Backlog.base#Cited by this paper]]
