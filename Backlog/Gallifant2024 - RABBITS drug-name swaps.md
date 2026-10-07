---
title: "Language Models are Surprisingly Fragile to Drug Names in Biomedical Benchmarks"
citekey: "Gallifant2024"
authors: "Gallifant et al."
year: 2024
published: 2024-06-17
venue: "Findings of EMNLP 2024"
url: "https://arxiv.org/abs/2406.12066"
arxiv: "2406.12066"
doi: ""
pdf_url: "https://arxiv.org/pdf/2406.12066"
topics: [kg-medical-eval]
status: candidate
priority: 2
relevance: adjacent
kind: []
questions: [Q8]
manipulation: "brand ↔ generic drug names swapped in MedQA and MedMCQA via RxNorm"
outcome: "accuracy drop 1–10%"
why: "Model for a faithful, ontology-driven surface swap with expert review; same recipe fits local drug or food names"
found_by: [search/cue-injection]
cited_by: []
added: 2026-10-07
cited_by_count: 0
tags:
  - type/candidate
---
