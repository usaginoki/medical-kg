---
title: "FAM-Bench: A Multimodal Benchmark for Condition-Aware Food-as-Medicine Reasoning"
citekey: Mao2026
authors: [Mingyang Mao, Bhargav Rishi Medisetti, Utkarsh Grover, Tanvir Ibrahim, Wenyan Li, Tingting Zhang, Xiaomin Lin]
year: 2026
published: 2026-05-29
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2605.31410"
arxiv: "2605.31410"
doi: ""
pdf: ""
pdf_url: "https://arxiv.org/pdf/2605.31410"
datasets: ["[[FAM-Bench]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases, search/evaluation]
cites:
  - "[[NutriBench]]"
  - "[[Recipe1M+]]"
  - "[[RecipeNLG]]"
  - "[[Singhal2022 - Large Language Models Encode Clinical Knowledge]]"
  - "[[Xiong2024 - MIRAGE MedRAG benchmark]]"
  - "[[Yang2024a - ChatDiet]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
---
# FAM-Bench: A Multimodal Benchmark for Condition-Aware Food-as-Medicine Reasoning

> [!abstract] TL;DR
> Builds **FAM-Bench**, 2,500 nutrition-expert-verified items asking whether a concrete dish (image + ingredients) is
> suitable for one of 13 diet-related conditions (1,500 binary items with ingredient rationales) and how four dishes
> rank for 1–3 conditions (1,000 items). Five VLMs are tested with baseline, CoT, knowledge injection (KI) from a
> curated condition → food knowledge base, and CoT+KI.

## What was built
- **Dataset(s):** [[FAM-Bench]]
- **Sources & construction:** 3,859 recipes from 54 web domains (74.6% health-information portals of medical
  societies, clinical-nutrition programmes and public-health agencies; 26.3% food publications); normalised dish
  records; a knowledge base of beneficial / limit / avoid foods per condition from AHA, NIH, Harvard Nutrition Source,
  American Liver Foundation; a canonical ingredient vocabulary; LLM-proposed annotations (GPT-5.5 per the release)
  checked by rules and confirmed or corrected by nutrition experts.
- **Size & coverage:** 2,500 items, 13 conditions (CVD, heart failure, hyperlipidemia, hypertension, stroke, T2D,
  metabolic syndrome, obesity, NAFLD, CKD, GERD, IBS, osteoporosis); US-heavy recipes.
- **Evaluation / applications:** GPT-5.4, Claude Sonnet 4.6, Gemini 2.5 Pro, Qwen3-VL-8B, Gemma-3-12B × four prompt
  modes; metrics: accuracy and rationale F1 (Task 1), top-1/MRR (Task 2), cross-task consistency; 100-item non-expert
  human baseline; text/image ablation.

## Key findings
1. Verdicts are easier than rationales: best Task 1 accuracy 82.80% (Gemini 2.5 Pro, KI) vs best rationale macro-F1
   0.2614 (GPT-5.4, CoT+KI).
2. Knowledge injection mostly improves the verdict (+2.0 to +3.3 points over baseline for every model; e.g. GPT-5.4
   77.67 → 80.47), CoT mostly improves rationale F1; CoT+KI is best overall.
3. Ranking is hard: Task 2 top-1 29.3–41.5% (chance 25%), MRR 0.53–0.63; non-expert humans 63.0% (Task 1) and 37.0%
   (Task 2).
4. Recipe text carries most of the evidence; dropping the image barely changes accuracy, dropping the text costs up
   to ~9 points (Qwen3-VL-8B).
5. Claude Sonnet 4.6 baseline is internally inconsistent across tasks (CTC 0.63), fixed by CoT (0.93).

## Relevance to research questions
### Q4: Patient case-conclusion datasets
A diet-scenario case set (dish × condition → recommend / not recommend + justifying ingredients; and condition →
ranked dishes), the most direct published test of food-as-medicine reasoning and close to our dish → ingredient →
condition KG. It is global/US rather than culture-specific (no cuisine labels), has no herbs and no gold food–drug
items. It is also relevant to Q5 (not tagged here): KI from a condition → food knowledge base vs baseline gives a
measured +2–3 points, and about a third of Task 1 items get no injected knowledge in the released code.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted (no local PDF). Main results: Table 1 (5 models × 4 modes, both tasks); Table 2 (modality ablation);
Figure 3 (recipe counts by country); Figure 5 (per-condition accuracy).

## Limitations / caveats
- U.S.-heavy recipes, terminology and guidelines (stated by the authors).
- Hidden ingredients, portion size and dose are not modelled; binary labels per condition.
- Under double-blind review at the time of access; repo is anonymous and will move.

## Related work to follow
![[Backlog.base#Cited by this paper]]
