---
title: "MTCMB: A Multi-Task Benchmark Framework for Evaluating LLMs on Knowledge, Reasoning, and Safety in Traditional Chinese Medicine"
citekey: Kong2025
authors: [Shufeng Kong, Xingru Yang, Yuanyuan Wei, Zijie Wang, Hao Tang, Jiuqi Qin, Shuting Lan, Yingheng Wang, Junwen Bai, Zhuangbin Chen, Zibin Zheng, Caihua Liu, Hao Liang]
year: 2025
published: 2025-06-02
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2506.01252"
arxiv: "2506.01252"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2506.01252"
datasets: ["[[MTCMB]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
cites:
  - "[[CMB (CMB-Clin)]]"
  - "[[CMExam]]"
  - "[[MedMCQA]]"
  - "[[MedQA]]"
  - "[[Singhal2022 - Large Language Models Encode Clinical Knowledge]]"
  - "[[TCMBench]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - tradmed/tcm
  - region/east-asia
---
# MTCMB: A Multi-Task Benchmark Framework for Evaluating LLMs on Knowledge, Reasoning, and Safety in Traditional Chinese Medicine

> [!abstract] TL;DR
> Introduces **MTCMB**, a Chinese TCM benchmark of 12 sub-datasets (7,100 items) built with certified TCM
> practitioners from licensing exams, textbooks, real hospital EMRs (CCL25-Eval), published case records and the 2020
> Chinese Pharmacopoeia, and evaluates 15 LLMs (general, medical, reasoning) zero-shot, few-shot and with chain-of-thought. Models do well on exam
> knowledge but poorly on syndrome differentiation and prescription.

## What was built
- **Dataset(s):** [[MTCMB]]
- **Sources & construction:** national attending-physician (1,200) and practitioner (8 × 600) exam banks; a 1988 TCM
  Q&A bank; zhongyigen.com case records; licensing practical-skills case summaries turned into doctor–patient
  dialogues by DeepSeek-R1; Tianchi literature QA; CCL25-Eval Task 9 EMRs (syndrome/disease labels, herb sets);
  "13th Five-Year Plan" textbooks (200 cases → diagnosis, and → treatment principle/formula/herbs); pharmacopoeia
  safety records turned into cloze and MCQ items by DeepSeek-R1. All reviewed by licensed TCM physicians.
- **Size & coverage:** 7,100 items in five dimensions: knowledge QA 6,100, language understanding 300, diagnosis 300,
  prescription 300, safety 100. China only, Simplified Chinese.
- **Evaluation / applications:** accuracy (MCQ, multi-label), BLEU/ROUGE/BERTScore (generation), set-overlap score
  (prescription), GLM-4-Air judge (safety cloze); expert 1–10 ratings on 20 items per generative set to validate the
  metrics.

## Key findings
1. Knowledge QA is largely solved by Chinese frontier models (Doubao 92.1 ED-A / 94.2 ED-B; dimension top 91.8), but
   diagnosis tops out at 50.0 (Qwen3-235B few-shot) and prescription at 48.5 (Doubao/DeepSeek-V3 few-shot).
2. Multi-label syndrome/disease classification (MSDD) stays at or below 50 for all models; medical LLMs (HuatuoGPT-o1,
   Baichuan-M1, Taiyi, DISC-MedLLM, WiNGPT2) do not beat general models.
3. Few-shot and CoT give small, inconsistent gains (CoT sometimes hurts, e.g. Doubao LitData 67 → 34).
4. Safety: high headline scores (DeepSeek-R1 few-shot 87.9) but qualitative misses of rare contraindications.
5. Automatic metrics correlate with expert ratings: Pearson r 0.59 (CHGD), 0.68 (Diagnosis), 0.87 (FRD).

## Relevance to research questions
### Q4: Patient case-conclusion datasets
A culture-specific (Chinese TCM) set with 800 case → conclusion items: 200 real EMRs → syndrome + disease or → herb
set, 100 published case records, 100 dialogue vignettes and 400 textbook vignettes → syndrome, treatment principle,
formula and herbs; plus 554 vignette MCQs. Conclusions are herbs and formulas that join to SymMap/HERB, which makes
it a natural test of whether TCM herb/syndrome knowledge from our KG helps; explicit diet content is small (254
items with food/diet keywords, 60 with diet advice). Open (Apache-2.0 / CC-BY-4.0).

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted (no local PDF). Main results: Tables 2–4 of the paper (general, reasoning and medical LLMs × 12
sub-datasets × zero/few-shot/CoT), Table 5 (top-3 per dimension), Figure 4 (metric vs expert correlation).

## Limitations / caveats
- Clinical subsets are small (100–200 items); several subsets were generated or rewritten by DeepSeek-R1.
- Exam banks and Tianchi data are public, so contamination is likely for Chinese models.
- Generative tasks are scored with n-gram/BERTScore overlap, which rewards wording close to the reference.

## Related work to follow
![[Backlog.base#Cited by this paper]]
