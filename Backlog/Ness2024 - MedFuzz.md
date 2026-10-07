---
title: "MedFuzz: Exploring the Robustness of Large Language Models in Medical Question Answering"
citekey: "Ness2024"
authors: "Ness et al."
year: 2024
published: 2024-06-03
venue: "arXiv preprint"
url: "https://arxiv.org/abs/2406.06573"
arxiv: "2406.06573"
doi: ""
pdf_url: "https://arxiv.org/pdf/2406.06573"
topics: [kg-medical-eval]
status: candidate
priority: 2
relevance: core
kind: []
questions: [Q8]
manipulation: "attacker LLM adds patient characteristics (age, sex, race, SES) to MedQA items to push the target to a distractor"
outcome: "accuracy drop; explanation faithfulness"
why: "Adversarial rather than random cue injection, constrained so a clinician would keep the answer"
found_by: [search/cue-injection]
added: 2026-10-07
cited_by:
  - "[[Xiao2025 - FairMedQA]]"
cited_by_count: 1
tags:
  - type/candidate
---
