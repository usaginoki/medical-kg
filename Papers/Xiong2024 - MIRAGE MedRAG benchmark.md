---
title: "Benchmarking Retrieval-Augmented Generation for Medicine"
citekey: Xiong2024
authors: [Guangzhi Xiong, Qiao Jin, Zhiyong Lu, Aidong Zhang]
year: 2024
published: 2024-02-20
venue: "Findings of ACL 2024"
peer_reviewed: true
url: "https://aclanthology.org/2024.findings-acl.372/"
arxiv: "2402.13178"
doi: "10.18653/v1/2024.findings-acl.372"
pdf: "[[Xiong2024.pdf]]"
pdf_url: "https://arxiv.org/pdf/2402.13178"
datasets: []
topics: [kg-medical-eval]
questions: [Q5, Q6]
relevance: core
found_by: [search/evaluation, search/supply]
added: 2026-10-07
cites:
  - "[[Jin2023a - MedCPT]]"
  - "[[Lievin2022 - Can large language models reason about medical questions]]"
  - "[[Liu2023a - Lost in the Middle]]"
  - "[[MedQA]]"
  - "[[Singhal2022 - Large Language Models Encode Clinical Knowledge]]"
  - "[[Wang2023a - Augmenting Black-box LLMs with Medical Textbooks for Biomedical Question Answeri]]"
  - "[[Yasunaga2022 - Deep Bidirectional Language-Knowledge Graph Pretraining]]"
  - "[[Zakka2023 - Almanac]]"
cited_by:
  - "[[Mao2026 - FAM-Bench food-as-medicine benchmark]]"
cited_by_count: 1
tags:
  - type/paper
  - relevance/core
  - q/5
  - q/6
  - inject/vector-rag
  - inject/finetune
  - eval/mcqa
  - eval/retrieval
---
# Benchmarking Retrieval-Augmented Generation for Medicine

> [!abstract] TL;DR
> Introduces **MIRAGE**, a 7,663-question benchmark built from five medical QA sets, and **MedRAG**, an open toolkit
> that crosses 5 corpora × 4 retrievers (+2 fusions) × 6 LLMs (41 combinations, >1.8 trillion prompt tokens). Plain
> "retrieve 32 snippets and prepend them" RAG beats chain-of-thought by 1–18% (relative) on average, but almost all of
> the gain comes from the two literature-derived datasets; on exam questions the gain is ≤ 3 points and GPT-4 loses
> accuracy. The corpus choice matters more than the retriever, accuracy scales log-linearly with the number of
> snippets, and accuracy depends on where the useful snippet sits in the context.

## What was built
- **Benchmark (MIRAGE):** five multiple-choice sets with their supporting contexts removed: MMLU-Med (1,089; six
  biomedical MMLU tasks), [[MedQA]]-US (1,273 USMLE test questions), [[MedMCQA]] (4,183 dev questions, Indian entrance
  exams), PubMedQA* (500 expert-annotated questions, abstract removed) and BioASQ-Y/N (618 yes/no questions,
  2019–2023). Code and data: [MIRAGE](https://github.com/Teddy-XiongGZ/MIRAGE).
- **Four evaluation settings** (the paper's definitions):
  - *Zero-shot learning*: "in-context few-shot learning is not permitted".
  - *Multi-choice evaluation*: accuracy on answer options, reported with "the standard deviation for the proportion
    of correctly answered questions, reflecting the error bound of the results", plus the mean over the five tasks.
  - *RAG*: external documents must be retrieved.
  - *Question-only retrieval (QOR)*: "answer options should not be provided as input during retrieval". The authors
    note that earlier medical RAG studies retrieved with the options, which is not realistic.
- **Toolkit (MedRAG):** [MedRAG](https://github.com/Teddy-XiongGZ/MedRAG). Corpora: PubMed (23.9M abstracts),
  StatPearls (9.3k point-of-care articles → 301.2k paragraph snippets), Textbooks (18 USMLE textbooks → 125.8k chunks
  ≤ 1,000 characters), Wikipedia (29.9M snippets) and MedCorp (all four). Retrievers: BM25 (lexical), Contriever
  (general dense), SPECTER (scientific dense), MedCPT (biomedical dense, trained on 255M PubMed search-log clicks), and
  Reciprocal Rank Fusion of BM25+MedCPT (RRF-2) or all four (RRF-4). LLMs: GPT-4, GPT-3.5, Mixtral 8×7B, Llama2-70B,
  MEDITRON-70B, PMC-LLaMA-13B.

![[Xiong2024-fig-02-p4.png]]
*Figure 2: MedRAG components: a question is sent to one of four retrievers over one of five corpora, and the retrieved
snippets plus the question go to one of six LLMs.*

## How the knowledge is given to an LLM (→ Q6)
- **Vanilla RAG:** "we concatenate and prepend retrieved snippets to the question input", then CoT prompting; 32
  snippets by default, temperature 0. The RAG prompt differs from the CoT prompt only by the line "Here are the
  relevant documents: {{context}}" and the instruction to use them (Figs. 6–7), so the comparison isolates the
  knowledge.
- **Knowledge unit:** short text snippets (average 119–296 tokens per corpus). There is no graph, no tool use, and no
  iterative retrieval; the authors list active RAG and re-rankers as future work.
- **Implicit comparison with fine-tuning:** domain-pretrained models (MEDITRON = Llama2 further trained on biomedical
  text; PMC-LLaMA) are run with and without RAG, which allows a RAG-vs-SFT comparison on the same base model.

## How the gain is measured (→ Q5)
- **Baseline:** the same LLM with the CoT prompt and no retrieval.
- **Metric:** accuracy per dataset ± the standard deviation of the proportion, plus the unweighted mean over the five
  datasets.
- **Grid:** Table 6 compares LLMs at fixed corpus/retriever (MedCorp, RRF-4, k = 32). Table 7 crosses all corpora and
  retrievers with GPT-3.5. Then three analyses with GPT-3.5 + RRF-4: number of snippets k ∈ {1, 2, 4, …, 64}, position
  of the ground-truth snippet (only possible for PubMedQA* and BioASQ, which have gold supporting snippets), and which
  sources the retriever picks from MedCorp.
- **Retrieval quality** is measured only indirectly: 79.6% of PubMedQA* ground-truth snippets are ranked top-1.

## Key findings
1. **Average gains are real but concentrated on literature questions.** CoT → MedRAG mean accuracy: GPT-4 73.44 →
   79.97, GPT-3.5 60.69 → 71.57, Mixtral 61.42 → 69.48, Llama2-70B 50.24 → 53.38, MEDITRON 57.04 → 60.18,
   PMC-LLaMA 52.40 → 52.92. GPT-3.5 and Mixtral with RAG reach GPT-4 (CoT) level. However, PubMedQA* (+31 points
   for GPT-3.5 and GPT-4) and BioASQ (+16 / +8) carry most of the gain. On the three exam sets GPT-3.5 gains only
   +1.6 to +2.8 points and **GPT-4 loses 1.2–3.2 points** (e.g. MedMCQA 69.88 → 66.65).
2. **Corpus first.** With GPT-3.5, single narrow corpora (StatPearls, Textbooks, Wikipedia) give a *lower* average than
   CoT (54.45–60.14 vs 60.69), because PubMedQA* falls to 22–31% (CoT 36%). Textbooks give the best MMLU-Med score
   (76.68) and StatPearls the best MedQA-US score (67.48). Only PubMed and MedCorp help on every task; MedCorp + RRF-4
   is best overall (71.57).
3. **Retrievers:** MedCPT and BM25 are the strongest single retrievers. SPECTER, trained for document–document
   similarity, is 6.8–7.8% worse than the others on MedCorp. RRF-4 on MedCorp beats single retrievers by 1.4–10.7%,
   but fusing a weak retriever can hurt (on Wikipedia, RRF-2 beats RRF-4 by 1.7%).
4. **Number of snippets (Fig. 3):** on the exam sets accuracy rises roughly log-linearly up to k = 32; with k ≤ 8 RAG
   is *below* CoT (MMLU-Med ~68–71 vs 72.9), i.e. a few weak snippets "even [hinder] the LLM from using its inherent
   knowledge". MedQA-US drops again at k = 64 (~63.6 vs 66.6 at k = 32). PubMedQA* is best at k = 1 (~72) and declines
   as k grows.
5. **Position (Fig. 4):** accuracy follows a U-shape over the position of the gold snippet: PubMedQA* ~67% (positions
   1–6), ~65% (7–12), ~80% (13–18); BioASQ ~90.7, ~89.6, ~91.9, ~93.1 over four bins of 8.
6. **RAG vs fine-tuning:** relative to Llama2 (CoT), RAG gives +6.3% and domain pretraining (MEDITRON, CoT) +13.5%;
   "While SFT is better at fusing medical knowledge into LLMs, RAG remains a more flexible and cost-efficient way".
   RAG on top of MEDITRON adds another +5.5% relative (57.04 → 60.18).
7. **Retrieved sources follow the task:** exam questions retrieve more Textbooks/StatPearls, literature questions
   retrieve more PubMed, and Wikipedia's share drops well below its share of MedCorp (Fig. 5).

![[Xiong2024-fig-03-p7.png]]
*Figure 3: MedRAG accuracy (GPT-3.5, MedCorp, RRF-4) vs number of retrieved snippets k = 1…64 (x-axis 2e1 = 2¹…);
red line = CoT without retrieval. Small k hurts on exam sets; PubMedQA* peaks at k = 1.*

![[Xiong2024-fig-04-p8.png]]
*Figure 4: accuracy by position of the ground-truth snippet in the context (GPT-3.5, PubMed, RRF-4); U-shaped
"lost-in-the-middle" pattern.*

**Table 6: CoT vs MedRAG (MedCorp, RRF-4, 32 snippets), accuracy %**

| LLM | Method | MMLU-Med | MedQA-US | MedMCQA | PubMedQA* | BioASQ-Y/N | Avg |
|---|---|---|---|---|---|---|---|
| GPT-4 | CoT | 89.44±0.93 | 83.97±1.03 | 69.88±0.71 | 39.60±2.19 | 84.30±1.46 | 73.44 |
| | MedRAG | 87.24±1.01 | 82.80±1.06 | 66.65±0.73 | 70.60±2.04 | 92.56±1.06 | 79.97 |
| GPT-3.5 | CoT | 72.91±1.35 | 65.04±1.34 | 55.25±0.77 | 36.00±2.15 | 74.27±1.76 | 60.69 |
| | MedRAG | 75.48±1.30 | 66.61±1.32 | 58.04±0.76 | 67.40±2.10 | 90.29±1.19 | 71.57 |
| Mixtral 8×7B | CoT | 74.01±1.33 | 64.10±1.34 | 56.28±0.77 | 35.20±2.14 | 77.51±1.68 | 61.42 |
| | MedRAG | 75.85±1.30 | 60.02±1.37 | 56.42±0.77 | 67.60±2.09 | 87.54±1.33 | 69.48 |
| Llama2-70B | CoT | 57.39±1.50 | 47.84±1.40 | 42.60±0.76 | 42.20±2.21 | 61.17±1.96 | 50.24 |
| | MedRAG | 54.55±1.51 | 44.93±1.39 | 43.08±0.77 | 50.40±2.24 | 73.95±1.77 | 53.38 |
| MEDITRON-70B | CoT | 64.92±1.45 | 51.69±1.40 | 46.74±0.77 | 53.40±2.23 | 68.45±1.87 | 57.04 |
| | MedRAG | 65.38±1.44 | 49.57±1.40 | 52.67±0.77 | 56.40±2.22 | 76.86±1.70 | 60.18 |
| PMC-LLaMA-13B | CoT | 52.16±1.51 | 44.38±1.39 | 46.55±0.77 | 55.80±2.22 | 63.11±1.94 | 52.40 |
| | MedRAG | 52.53±1.51 | 42.58±1.39 | 48.29±0.77 | 56.00±2.22 | 65.21±1.92 | 52.92 |

**Table 7 (condensed): GPT-3.5 + MedRAG, mean accuracy over the five MIRAGE tasks by corpus × retriever (CoT = 60.69)**

| Corpus | BM25 | Contriever | SPECTER | MedCPT | RRF-2 | RRF-4 |
|---|---|---|---|---|---|---|
| PubMed | 69.23 | 68.20 | 64.41 | 69.38 | 70.26 | 69.71 |
| StatPearls | 56.03 | 56.44 | 54.45 | 56.03 | 56.82 | 56.61 |
| Textbooks | 57.10 | 56.52 | 54.92 | 57.22 | 57.55 | 57.69 |
| Wikipedia | 57.74 | 58.08 | 55.51 | 58.95 | 60.14 | 59.14 |
| MedCorp | 70.05 | 68.61 | 64.63 | 70.06 | 70.61 | **71.57** |

## Relevance to research questions
### Q5: Evaluating KG-augmented medical LLMs
MIRAGE gives us the **baseline protocol**: the same model and prompt with and without the knowledge block, zero-shot,
temperature 0, accuracy ± SE per dataset, several LLMs. Three points to copy for our graph:
- **Question-only retrieval.** Our entity linking (dish, ingredient, drug, symptom) and graph lookup must use the
  question/case text only, never the answer options, or the KG "retrieves the answer".
- **Construct validity.** The large gains come from PubMedQA*/BioASQ, whose questions were written from PubMed
  abstracts that are themselves in the corpus. A benchmark generated from our own graph would inflate gains in the same
  way. We need independent case→conclusion sets (Q4) and should report the KG-answerable subset separately.
- **Expected effect size and power.** On exam sets a whole medical library gave GPT-3.5 only +1.6 to +2.8 points and
  GPT-4 −1.2 to −3.2. Our food–health graph covers a much smaller part of MedQA/MedMCQA, so on the full sets the
  expected gain is ≈ 0 and a strong model may lose a little. Report the full sets only as a regression check. The
  signal must come from a diet / food–drug / traditional-medicine subset. The SE is about ±1.3 points at n = 1,273 and
  ±2.2 at n = 500. A subset of ~140 MedQA-US questions (if the 11% diet-mention rate in our [[MedQA]] note holds for
  the test split) has an SE of ~±4 points, so we need paired tests on the same items, not two independent accuracies.

Further controls suggested by the paper: a **corpus ablation** in the style of Table 7 (KG alone vs KG + a general
medical corpus vs general corpus alone, so we can tell "more text" apart from "our graph"), a **k sweep**, and a
**fine-tuned/domain model** row. It does not cover open-ended answers, rationale quality or safety, so Q5 needs other
papers (e.g. [[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo et al. 2024]]) for those.

See [[Q5 Evaluating KG-augmented medical LLMs]]

### Q6: Supplying the KG to an LLM
This is the "vector RAG over text" baseline that any graph method should beat. Lessons for our graph:
- **Verbalise and retrieve, as a first baseline.** Turn each dish→ingredient→compound→condition path or claim into a
  short snippet that carries its source and evidence grade. Index the snippets with BM25 *and* a dense retriever and
  fuse them with RRF (the authors recommend RRF-2 = BM25 + MedCPT for PubMed and RRF-2 or RRF-4 for MedCorp). BM25 is competitive here, and exact
  matching on our alias table (zh/ja/ar/fa/hi dish and herb names) is something the English-trained MedCPT was never
  tested on.
- **How many snippets.** Too few snippets do harm (k ≤ 8 is below CoT on exam questions), and accuracy falls again at
  k = 64. Sweep k ∈ {4, …, 64}, and expect the best k to be larger for multi-hop diet questions than for single-fact
  lookups (PubMedQA* peaks at k = 1).
- **Ordering.** Accuracy is U-shaped over position, so the strongest (highest-evidence) paths should go first or last,
  not in the middle.
- **One source among several.** Narrow corpora hurt off-topic questions, and the mixed MedCorp corpus was the most
  robust. This argues for giving the KG *alongside* a general medical corpus, or routing to it only when the question
  mentions foods, herbs or drugs, rather than forcing KG context on every question.
- **Fine-tuning comparison.** SFT beat RAG on the same base (+13.5% vs +6.3%), and RAG still added on top of SFT. A
  fine-tuned arm (e.g. on verbalised KG paths) is worth one row in our comparison, but RAG remains the cheaper default,
  and it is the only option that keeps provenance.
- The **MedRAG toolkit** is open, so our verbalised graph could be added as a sixth corpus and the whole grid reused.

See [[Q6 Supplying the KG to an LLM]]

## Limitations / caveats
- Multiple choice only; the LLM still sees the options when answering, and rationales are not evaluated (authors'
  limitation).
- Only vanilla RAG; no re-ranking, iterative retrieval, graph retrieval or tools. The follow-up i-MedRAG (Xiong2024a,
  in Backlog) adds iterative follow-up queries.
- Retrieval quality can only be checked on the two literature datasets; for the exam sets it is unknown whether the
  retrieved snippets were actually helpful.
- One run per configuration, temperature 0. Error bars come from the binomial proportion; there are no significance
  tests or variance across prompts.
- Most component analyses (Table 7, Figs. 3–5) use GPT-3.5 only, the model that "benefits the most" (+17.9%), so the
  conclusions about corpus and k may overstate effects for stronger models.
- Minor inconsistency: MedCorp has 54.2M snippets in Table 3 but is labelled "65.3M" in Table 7.
- Possible test contamination of MMLU/MedQA in GPT-4 is not discussed (a later paper, MedRGB, suggests it).

## Related work to follow
![[Backlog.base#Cited by this paper]]
