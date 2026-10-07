---
title: "Contextual Evaluation of Large Language Models for Classifying Tropical and Infectious Diseases"
citekey: "Asiedu2024"
authors: "Asiedu et al."
year: 2024
published: 2024-09-13
venue: "NeurIPS 2024 workshops"
url: "https://arxiv.org/abs/2409.09201"
arxiv: "2409.09201"
doi: ""
pdf_url: "https://arxiv.org/pdf/2409.09201"
topics: [kg-medical-eval]
status: candidate
priority: 1
relevance: core
kind: [case]
questions: [Q7, Q8]
manipulation: "52 seed personas with a location slot; counterfactual location (→ San Francisco), race and gender insertions; 11,719 queries"
outcome: "diagnosis accuracy vs expert baseline"
why: "Place is a decisive cue (accuracy drops when the endemic location is swapped) while US race tokens are not; seed set inside EquityMedQA, expanded set on request"
found_by: [search/culture-cued-cases, search/cue-injection]
cited_by: []
added: 2026-10-07
cited_by_count: 0
tags:
  - type/candidate
  - kind/case
---
