---
title: "MedCaseReasoning: Evaluating and learning diagnostic reasoning from clinical case reports"
citekey: Wu2025
authors: [Kevin Wu, Eric Wu, Rahul Thapa, Kevin Wei, Angela Zhang, Arvind Suresh, Jacqueline J. Tao, Min Woo Sun, Alejandro Lozano, James Zou]
year: 2025
published: 2025-05-16
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2505.11733"
arxiv: "2505.11733"
doi: "10.48550/arXiv.2505.11733"
pdf: ""
pdf_url: "https://arxiv.org/pdf/2505.11733"
datasets: ["[[MedCaseReasoning]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases]
tags:
  - type/paper
  - relevance/core
  - q/4
  - kind/case
  - case/real
---
# MedCaseReasoning: Evaluating and learning diagnostic reasoning from clinical case reports

> [!abstract] TL;DR
> Stanford, UCSF and USC built **MedCaseReasoning**, "the first open-access dataset for evaluating LLMs on their
> ability to align with clinician-authored diagnostic reasoning": 14,489 diagnostic cases from PubMed Central case
> reports. Each case has a case prompt, a gold final diagnosis and the authors' differential reasoning as numbered
> statements.
> - Reasoning models fall short: o3 reaches 64.5% 10-shot accuracy, and DeepSeek-R1 48.0% with 64% reasoning recall.
> - Fine-tuning on the reasoning traces improves both, and the gains carry over to NEJM CPC.
>
> Read from the arXiv v2 PDF text (no docling extraction). The GitHub README cites the paper as "NeurIPS 2025", but
> OpenReview lists it as a *withdrawn ICLR 2026 submission*, so it is treated as a preprint.

## What was built
- **Dataset(s):** [[MedCaseReasoning]]
- **Sources & construction:**
  - Start: 98,994 free-access "case report" articles from the PMC Open Access subset (Jan 2005 – Apr 2025).
  - Keep the 28,313 that contain "differential". o4-mini converts each into a QA (case prompt with an information cutoff, enumerated reasoning, final diagnosis) and scores it on 5 clinician-designed criteria.
  - Drop cases with thin presentations, without 2+ alternatives or without a stated diagnosis: 19,428 remain.
  - gemini-2.5-pro flags unfaithful or implausible cases: 14,489 remain.
  - Test set: 897 cases with transparency and integrative-reasoning scores ≥ 4.
- **Size & coverage:** 13,092 train / 897 test (+ 500 val on Hugging Face); 813 journals, "30+ specialties", English. 16% of reports date from 2024 or later.
- **Evaluation:**
  - diagnostic accuracy with a gpt-4o-mini judge (McDuff et al. 2025 prompt), 1/5/10-shot over 10 samples;
  - **reasoning recall** = share of gold reasoning statements found in the model's trace (o4-mini judge);
  - external check on 302 NEJM CPC cases (licensed, not released).

## Key findings
1. 10-shot accuracy on the test set: o3 0.645, DeepSeek-R1 0.480, QwQ-32B 0.398, MedReason-8B 0.382, LLaMA-3.1-8B 0.332, Qwen-2.5-7B 0.287. Reasoning recall: R1 0.642, QwQ 0.590, LLaMA 0.451.
2. SFT on stitched reasoning traces lifts MedReason-8B to 0.501 10-shot accuracy (above R1) and 0.522 recall. The abstract reports average relative gains of 29% (accuracy) and 41% (recall).
3. Gains transfer to NEJM CPC: MedReason-8B +18%. o3 and R1 score similarly on both benchmarks (62.3% and 43.7% on NEJM CPC).
4. **Physician validation:** 100 cases, 4 physicians. 98% had no hallucination; 92% of final diagnoses were faithful and inferable; 93% of reasoning steps were faithful. The recall judge agreed with a physician on 84 of 89 pairs.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
The largest open set of **real** case → diagnosis pairs with clinician reasoning. It is global English, with no country labels.
- **Diet content:** a subset theme. About 9% of cases mention diet, food, nutrition, supplements, vitamins or herbal products, and ~343 gold diagnoses are food-related (scurvy, brucellosis, anisakiasis, liquorice pseudo-hyperaldosteronism, star fruit intoxication, kratom liver injury, alpha-gal syndrome).
- **Food–drug test set:** these cases are a ready source of real cases for one (10 shortlisted in the dataset note).
- **Hidden exposures:** some food-caused cases hide the dietary exposure behind the information cutoff.
- **KG links:** about half of the diagnoses match a MeSH/UMLS condition name in our database.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted. Table 3 (test results with 95% CIs), Fig. 2 (accuracy vs recall, and the correlation with NEJM CPC), Table 4 (physician validation), Table 5 (top journals).

## Limitations / caveats
- Inputs, reasoning lists and labels are LLM-generated from the articles. Only 100 cases were checked by humans.
- Case reports over-represent rare diseases and give a single time-point. The authors note that some cases are intractable and others trivial.
- Recall measures only reasons that the authors wrote down. Precision and wrong reasoning are not penalised.
- Licence statements conflict: MIT on Hugging Face, CC BY 4.0 in the GitHub README.

## Related work to follow
![[Backlog.base#Cited by this paper]]
