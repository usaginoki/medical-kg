---
title: "MedArabiQ: Benchmarking Large Language Models on Arabic Medical Tasks"
citekey: AbuDaoud2025
authors: [Mouath Abu Daoud, Chaimae Abouzahir, Leen Kharouf, Walid Al-Eisawi, Nizar Habash, Farah E. Shamout]
year: 2025
published: 2025-05-06
venue: "MLHC 2025 (PMLR 298)"
peer_reviewed: true
url: "https://arxiv.org/abs/2505.03427"
arxiv: "2505.03427"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2505.03427"
datasets: ["[[MedArabiQ]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases, search/global-cases]
cites:
  - "[[JAMA Clinical Challenge + Medbullets]]"
  - "[[MMedBench]]"
  - "[[MedMCQA]]"
  - "[[MedQA]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - region/middle-east
---
# MedArabiQ: Benchmarking Large Language Models on Arabic Medical Tasks

> [!abstract] TL;DR
> Introduces **MedArabiQ**, seven 100-item Arabic medical datasets (exam MCQs, bias-injected MCQs, fill-in-the-blank
> with/without choices, and real patient–doctor Q&A from AraMed/Altibbi in original, grammar-corrected and
> GPT-4o-paraphrased form), and evaluates eight LLMs zero-shot plus three bias-mitigation prompts.

## What was built
- **Dataset(s):** [[MedArabiQ]]
- **Sources & construction:** paper exams and lecture notes from student platforms of regional medical schools,
  digitised and checked by hand (chosen because they are unlikely to be in training data); 100 Q&A pairs selected from
  the 400 public [[AraMed]] samples (of 270,000), patient age/sex prepended; GEC with CAMeL Tools + BERT GED + mBART
  GEC; GPT-4o paraphrases; seven bias types injected by hand (following AgentClinic-style bias prompts).
- **Size & coverage:** 700 items; Arabic (MSA exams, dialectal questions), English parallel text for fill-in items; no
  country labels.
- **Evaluation / applications:** accuracy (MCQ, fill-in with choices), BERTScore with XLM-RoBERTa-large (open
  answers), GPT-4 judge on Q&A (1–5 on similarity, relevance, factuality, safety); models: Falcon3-10B, Jais-13B,
  LLaMA-3.1-8B, Qwen2.5-7B, Claude 3.5 Sonnet, GPT-4, Gemini 1.5 Pro, DeepSeek-V3.

## Key findings
1. Closed models lead on structured tasks: MCQ 57.5 (Gemini 1.5 Pro), 53.5 (GPT-4, Claude); fill-in with choices 79.7
   (DeepSeek-V3); open models 16–38 on MCQ.
2. On patient Q&A, BERTScores are flat (81.1–85.7) and Arabic-centric Jais scores highest (85.7) but gets a GPT-4 judge
   score of 3.2 vs 4.2 (DeepSeek), 4.1 (Gemini), 3.9 (GPT-4); Falcon 1.1 — BERTScore misses hallucination.
3. Injected cognitive biases lower accuracy, most for GPT-4 (66.3 → 35.7); few-shot mitigation helps partly (46.9);
   Gemini is most robust (55.1 → 55.1; 59.2 with few-shot).
4. Language-specific pretraining (Jais) matters less than task competence on structured items.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
A culture/region-specific (Arabic) set whose only true case → conclusion part is 100 real Altibbi patient questions
with a physician's reply (advice/triage), scored by BERTScore. 18 of the 100 cases involve food or diet (dialysis
diet, cinnamon and blood pressure, metformin and meals, folk "strengthening" foods), so it can probe Arabic diet
advice on a small scale. Its custom NYU licence forbids redistribution, which limits it to internal evaluation.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted (no local PDF). Main results: Table 1 (8 models × 6 tasks), Table 2 (bias and mitigation for Claude,
GPT-4, Gemini), Figure 4 (per-bias-type accuracy), Appendix J (GPT-4 judge).

## Limitations / caveats
- 100 items per task; the three Q&A files are variants of the same 100 cases.
- Possible contamination (authors acknowledge it); reference answers are unvetted forum replies.
- Zero-shot only; English prompts for exam tasks, Arabic prompts for Q&A.

## Related work to follow
![[Backlog.base#Cited by this paper]]
