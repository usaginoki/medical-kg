---
title: "A benchmark dataset for evaluating Syndrome Differentiation and Treatment in large language models"
citekey: Li2025
authors: [Kunning Li, Jianbin Guo, Zhaoyang Shang, Yiqing Liu, Hongmin Du, Lingling Liu, Yuping Zhao, Lifeng Dong]
year: 2025
published: 2025-12-02
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2512.02816"
arxiv: "2512.02816"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2512.02816"
datasets: ["[[TCM-BEST4SDT]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
tags:
  - type/paper
  - relevance/core
  - q/4
  - tradmed/tcm
  - region/east-asia
---
# A benchmark dataset for evaluating Syndrome Differentiation and Treatment in large language models

> [!abstract] TL;DR
> Introduces **TCM-BEST4SDT**, a Chinese TCM benchmark of 600 items led by experts from the China Academy of Chinese
> Medical Sciences, with a Beijing AI company (Wenge). Its centre is 300 clinical and classical cases scored on the
> *whole* "syndrome differentiation and treatment" chain, from syndrome to prescription and precautions, rather than
> on syndrome accuracy alone. A trained reward model (FangZheng-RM) scores how well a prescription fits a syndrome.
> 15 general and TCM-specific LLMs are evaluated. Read from the arXiv v1 PDF text and the figshare v8 README (no docling
> extraction).

## What was built
- **Dataset(s):** [[TCM-BEST4SDT]]
- **Sources & construction:**
  - SDT cases come from "clinical cases and classical case records". The clinical cases were approved by the Ethics Committee of Xiyuan Hospital of CACMS (2025XLA135-2).
  - Basic-knowledge items come from licensing, postgraduate (TCM integrated) and herbal-medicine title exams. Ethics items come from exam banks plus expert-written scenarios. Content-safety items were written by experts.
  - All items were deduplicated, cleaned and anonymised.
  - Three-stage annotation: TCM experts, then cross-validation, then independent third-party review. Choice questions have "sophisticated distractors".
- **Size & coverage:** 600 items = SDT 300 + basic knowledge 100 + ethics 100 + content safety 100.
  - SDT covers 257 syndromes and 20 ICD-11 disease chapters.
  - 14 outcome dimensions (syndrome, nature, location, principles, herbal composition and dosage, cause, pathogenesis, combination principles, incompatibility, pregnancy contraindications, herb safety, preparation, modification, precautions) plus 2 process dimensions (CoT completeness and CoT accuracy).
- **Evaluation:**
  - choice questions: 3 rounds with shuffled options; single choice counts only if all 3 are correct; multi-select uses a partial-credit formula;
  - a Qwen3-32B judge with expert prompts;
  - FangZheng-RM: Qwen3-14B fine-tuned on 10k expert-rated samples of one syndrome × 6 candidate prescriptions.

## Key findings
1. In paper v1, frontier general models led (Gemini 2.5 Pro well above GPT-5). Some TCM models (ShizhenGPT-32B) were competitive, but most small TCM models (Sunsimiao, Zhongjing, Taiyi 2) lagged. The text gives no numbers; they are in Fig. 4.
2. The Qwen3 series improves steadily from 4B to 235B, which the authors read as evidence that the benchmark discriminates between models.
3. The figshare v8 README re-runs with newer models:
   - Gemini 3 Pro total 0.871 (SDT 0.834) and GPT-5.2 0.787 (SDT **0.842**, the best). The gap comes from basic knowledge (0.957 vs 0.657).
   - Base Qwen2.5 models beat their TCM fine-tunes: 32B 0.808 vs ShizhenGPT 0.783; 7B 0.670 vs HuatuoGPT-o1 0.663.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
A culture-specific (Chinese TCM) set of 300 real or vignette cases. Each has a complete gold treatment plan: syndrome, principles, a dosed herbal prescription, decoction method and precautions.
- **Diet content:** unusually high. The scored Precautions field gives diet advice in 262 / 300 cases, mostly TCM food taboos while taking the medicine, and 279 prescriptions contain medicine–food-homology items.
- **KG links:** gold herbs link to SymMap/HERB (83–91% of mentions).
- **Scoring:** choice dimensions are deterministic, but the official prescription score needs the authors' reward model and judge.
- **Licence:** open, CC BY 4.0.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted. Main results: Fig. 4 (15 LLMs) and Fig. 5 (Qwen3 scaling) in v1; the README's Table 1 gives per-task scores for the v8 model set (see [[TCM-BEST4SDT]]).

## Limitations / caveats
- The paper does not give the split between hospital cases and classical records, nor inter-annotator agreement.
- Prescriptions are not compared with the gold herbs. The reward model and judge (both Qwen3-based) define the score, so results depend on those models.
- Small case set (300); classical cases and exam items are likely in pre-training data.

## Related work to follow
![[Backlog.base#Cited by this paper]]
