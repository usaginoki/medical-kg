---
title: "BLEnD: A Benchmark for LLMs on Everyday Knowledge in Diverse Cultures and Languages"
citekey: Myung2024
authors: [Junho Myung, Nayeon Lee, Yi Zhou, Jiho Jin, Rifki Afina Putri, Dimosthenis Antypas, Hsuvas Borkakoty, Eunsu Kim, Carla Perez-Almendros, Abinew Ali Ayele, Víctor Gutiérrez-Basulto, Yazmín Ibáñez-García, Hwaran Lee, Shamsuddeen Hassan Muhammad, Kiwoong Park, Anar Sabuhi Rzayev, Nina White, Seid Muhie Yimam, Mohammad Taher Pilehvar, Nedjma Ousidhoum, Jose Camacho-Collados, Alice Oh]
year: 2024
published: 2024-06-14
venue: "NeurIPS 2024 Datasets and Benchmarks Track"
peer_reviewed: true
url: "https://arxiv.org/abs/2406.09948"
arxiv: "2406.09948"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2406.09948"
datasets: ["[[BLEnD]]"]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
cites:
  - "[[Hershcovich2022 - Challenges in cross-cultural NLP]]"
  - "[[Naous2023 - CAMeL cultural bias in LLMs]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - q/2
---
# BLEnD: A Benchmark for LLMs on Everyday Knowledge in Diverse Cultures and Languages

> [!abstract] TL;DR
> Hand-crafted benchmark of 52.6k question-answer pairs about everyday life (food, sports, family, education,
> holidays, work) in 16 countries/regions and 13 languages; the same 500 question templates are answered by ~5 native
> annotators per culture, and LLMs are scored on short-answer and multiple-choice formats.

## What was built
- **Dataset(s):** [[BLEnD]]
- **Sources & construction:** native annotators from each culture proposed 10–15 questions per category; templates
  deduplicated and generalised ("…in your country?"), localised and translated (except US/GB); answers collected
  from native speakers who lived there > half their life (crowdsourcing or direct recruitment of 5 annotators),
  variants grouped with vote counts and translated to English; English MCQs built with other cultures' answers as
  distractors.
- **Size & coverage:** 500 templates × 16 cultures = 15,000 short-answer questions; 52.6k QA pairs; cultures
  include Iran, Azerbaijan, China, South and North Korea, Indonesia, West Java, Assam, Algeria, Ethiopia, Northern
  Nigeria, Greece, Spain, Mexico, UK, US. (A 2026 SemEval extension adds 17 language-culture pairs; see dataset note.)
- **Evaluation / applications:** 16 LLMs in local languages and English.

## Key findings
1. Average LLM accuracy on short answers: US 79.22% vs Spain 69.08%, Iran 50.78%, North Korea 41.92%, Northern
   Nigeria 21.18%, Ethiopia 12.18% — much worse for cultures under-represented online.
2. Up to 57.34% gap between cultures for GPT-4 (the best model); 31.63% between South and North Korea.
3. Food and holiday/leisure questions are significantly harder for LLMs than work-life or education (ANOVA p<0.05).
4. Mean annotator agreement 3.16/5 (63.2%); answer overlap is highest between culturally close pairs (Indonesia &
   West Java, US & UK, Spain & Mexico).
5. The most stereotypical LLM answers concern food and festivals (48.33% of Ethiopia answers stereotypical; West Java
   food questions answered "Seblak").

## Relevance to research questions
### Q1: Cultural food datasets
Food is 105 of the 500 templates: typical breakfasts, snacks, festival foods, fruits, drinks, meal times — a
human-voted everyday-eating profile per culture (incl. Iran, Azerbaijan, Assam, China, Koreas, Indonesia, and via
the 2026 extension Saudi Arabia, Egypt, Sri Lanka).

See [[Q1 Cultural food datasets]]

### Q2: Cultural ingredient datasets
Templates on the most common spice/herb, cooking oil and indispensable seasoning give direct culture → ingredient
answers with vote counts (e.g. Iran: turmeric, saffron).

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables
Not extracted (no local PDF).

## Limitations / caveats
- About five annotators per question, sometimes from one locality; language experts were mostly English-proficient
  academics.
- MCQ only in English at release.

## Related work to follow
![[Backlog.base#Cited by this paper]]
