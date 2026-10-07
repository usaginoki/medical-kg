---
title: "DiversityMedQA: Assessing Demographic Biases in Medical Diagnosis using Large Language Models"
citekey: "Rawat2024"
authors: "Rawat et al."
year: 2024
published: 2024-09-02
venue: "NLP4PI workshop at EMNLP 2024"
url: "https://arxiv.org/abs/2409.01497"
arxiv: "2409.01497"
doi: ""
pdf_url: "https://arxiv.org/pdf/2409.01497"
topics: [kg-medical-eval]
status: candidate
priority: 2
relevance: core
kind: [case]
questions: [Q7, Q8]
manipulation: "gender and ethnicity sentence added to MedQA items (567 ethnicity, 540 gender); GPT-4 filters items where the change matters clinically"
outcome: "accuracy change"
why: "LLM-as-filter for whether a cue is clinically relevant; US-style ethnicity tokens"
found_by: [search/culture-cued-cases, search/cue-injection]
cited_by: []
added: 2026-10-07
cited_by_count: 0
tags:
  - type/candidate
  - kind/case
---
