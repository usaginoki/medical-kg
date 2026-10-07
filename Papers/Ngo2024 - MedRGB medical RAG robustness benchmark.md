---
title: "Comprehensive and Practical Evaluation of Retrieval-Augmented Generation Systems for Medical Question Answering"
citekey: Ngo2024
authors: [Nghia Trung Ngo, Chien Van Nguyen, Franck Dernoncourt, Thien Huu Nguyen]
year: 2024
published: 2024-11-14
venue: "AAAI 2026 Workshop AI4Research"
peer_reviewed: workshop
url: "https://arxiv.org/abs/2411.09213"
arxiv: "2411.09213"
doi: ""
pdf: "[[Ngo2024.pdf]]"
pdf_url: "https://arxiv.org/pdf/2411.09213"
datasets: []
topics: [kg-medical-eval]
questions: [Q5, Q6]
relevance: core
found_by: [search/evaluation]
added: 2026-10-07
cites:
  - "[[Es2023 - Ragas]]"
  - "[[He2023 - MedEval]]"
  - "[[JAMA Clinical Challenge + Medbullets]]"
  - "[[Jin2023a - MedCPT]]"
  - "[[MedQA]]"
  - "[[Wang2024 - JMLR]]"
  - "[[Xiong2024 - MIRAGE MedRAG benchmark]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/5
  - q/6
  - inject/vector-rag
  - inject/context
  - eval/mcqa
  - eval/safety
  - eval/llm-judge
---
# Comprehensive and Practical Evaluation of Retrieval-Augmented Generation Systems for Medical Question Answering

> [!abstract] TL;DR
> **MedRGB** adds retrieval topics, signal documents, sub-question/answer pairs and counterfactual documents to 3,480
> questions from four MIRAGE datasets. It then tests LLMs in four scenarios: standard RAG, **sufficiency** (relevant
> documents mixed with irrelevant ones, plus an "Insufficient Information" option), **integration** (sub-questions per
> document) and **robustness** (some documents minimally edited to support a wrong answer). Retrieval barely helps
> strong models on exam questions. Irrelevant context makes models abstain even when they know the answer, and models
> detect only a small share of planted factual errors.

## What was built
- **Base questions:** 4 of the 5 MIRAGE sets from [[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]:
  MMLU-Med (1,089), [[MedQA]]-US (1,273), PubMedQA* (500), BioASQ-Y/N (618), giving 3,480 instances ("over 5 times
  that of RGB", the general-domain benchmark whose four abilities it adapts). MedMCQA is not used.
- **Retrieval topics:** GPT-4o writes ranked, diverse sub-topics per question, so that the retrieved set is less
  redundant than plain top-k similarity.
- **Signal documents** from two sources, meant to mimic an expert and a lay user:
  - *Offline:* MedCPT over MedCorp (PubMed, StatPearls, Textbooks, Wikipedia), top-3 per topic.
  - *Online:* Google Custom Search per topic; GPT-4o ranks the links, then scrapes and summarises each page into one
    signal document.
- **Noise documents:** "randomly sampled from set of all signal documents from other questions" (on-topic medical
  text that is irrelevant to this question).
- **Sub-QA pairs:** GPT-4o writes one sub-question per signal document, with a short answer extracted from it.
- **Adversarial documents:** GPT-4o produces "a deliberately incorrect new answer" and edits the signal document
  minimally into "a persuasive but factually incorrect new document supporting the incorrect answer".
- **Availability:** "Our data and source code will be released upon acceptance". No public release was found
  (2026-10-07).

![[Ngo2024-fig-02-p3.png]]
*Figure 2: MedRGB construction: GPT-4o generates retrieval topics, documents come from MedCorp (MedCPT) or Google
search, and each signal document gets a sub-QA pair and a counterfactual twin (red).*

## How the knowledge is given to an LLM (→ Q6)
- **In context:** a fixed number of documents (5 or 20 in standard RAG and sufficiency, 5 or 10 in integration) is
  placed in the prompt in random order, with document ids. The LLM reasons step by step and then picks an option.
- **Controlled composition:** apart from standard RAG, the context is assembled by hand, not by a retriever. *p* is
  "the percentage of signal documents in the retrieved context" (sufficiency, integration), or "the percentage of
  factually correct documents" (robustness, where all documents are relevant), with p ∈ {0, 20, 40, 60, 80, 100}.
- **Prompt-level defences only:** the model is told that "Some documents may be irrelevant" or "may contain factual
  errors", and must first flag noise or erroneous documents and correct them. There is no fine-tuning, re-ranking,
  verification module or tool.

## How the gain is measured (→ Q5)
The four scenarios, as the paper defines them:
- **Standard-RAG**: "evaluates LLMs performance when presented with multiple retrieved signal documents". Compared
  with a "No Retrieval" baseline on all 7 LLMs (GPT-3.5, GPT-4o-mini, GPT-4o, PMC-LLaMA-13B, MEDITRON-70B,
  Gemma-2-27B, Llama-3-70B).
- **Sufficiency**: "By adding 'Insufficient Information' as an additional response option, LLMs should only answer
  when they are confident to have enough information". Metrics: main accuracy, share of "insufficient" answers, and
  noise-detection accuracy.
- **Integration**: "ability to answer multiple supporting questions and integrate the extracted information to help
  address the main question". Metrics: main accuracy, plus sub-answer exact match and a lenient GPT-based score (1 /
  0.5 / 0 for full / partial / no semantic match).
- **Robustness**: "resiliency to factual errors in the retrieved context. A trustworthy AI medical system should be
  able detect factually incorrect documents and provide the corrected information". Metrics: main accuracy, sub-answer
  scores, and factual-error detection rate.
- The last three tests use only GPT-3.5, GPT-4o-mini and Llama-3-70B, because of cost. Temperature 0, one run, no
  significance tests.

## Key findings
1. **Standard RAG helps weak models and literature questions, not strong models on exams.** PubMedQA gains are large
   (GPT-3.5 49.8 → 71.0 with 20 offline documents), but on MedQA and MMLU almost every general model scores *below*
   no-retrieval with 5 offline documents (GPT-4o MedQA 89.5 → 83.7, Llama-3-70B 82.9 → 73.6, GPT-4o MMLU 93.4 → 88.3).
   The authors attribute this to "strong internal knowledge and potential data leakage". MEDITRON-70B is the clear
   exception (MedQA 51.7 → 62.9 online, 20 documents). PMC-LLaMA-13B (2k context) does not benefit.
2. **Offline vs online retrieval:** the curated corpus (MedCorp + MedCPT) improves with more documents, while web search
   "tends to provide high-quality top results but introduces more noise as the number of results increases".
3. **Irrelevant context plus an abstain option removes much of the model's own knowledge.** With 5 documents that are
   all noise (p = 0), models mostly answer "insufficient information" (BioASQ 82–93% of answers, MMLU 40–53%,
   MedQA 24–32%), and MMLU accuracy falls to 40.5–43.5% vs 76.3–88.3% without retrieval. A single signal document
   (p = 20) restores much of it. Even at p = 100 accuracy stays below standard RAG on the exam sets (MedQA GPT-3.5 55.3
   vs 63.0); the authors read this as models in standard RAG answering "even when they are not fully confident".
4. **Noise detection gets worse as the context becomes cleaner:** BioASQ noise-detection accuracy at p = 20 vs p = 100
   is 99.2 → 58.3 (GPT-3.5), 99.0 → 61.7 (GPT-4o-mini) and 99.0 → 67.9 (Llama-3-70B). When all documents are relevant,
   models fail to recognise them as relevant. A little noise (p = 60–80) sometimes beats p = 100.
5. **Sub-questions help when signal is scarce:** at p = 20 the integration test gives higher main accuracy than the
   sufficiency test (e.g. MMLU 66.0 / 80.5 / 71.9 vs 57.5 / 66.5 / 65.5). At p = 100 it is below standard RAG on MedQA
   (56.4 / 72.6 / 70.1 vs 63.0 / 77.1 / 73.6) and MMLU, which the authors read as an "inability to integrate
   information from sub-task effectively". Sub-answer exact match is only ~20–35%, while the GPT-based score stays
   at ~79–84%.
6. **Planted misinformation is mostly accepted.** When all 5 documents are counterfactual (p = 0), sub-answer exact
   match is ≤ ~1% (models repeat the planted answer), and the factual-error detection rate is only ~7–29% (read off
   Fig. 16). Main accuracy drops less than with irrelevant noise (MedQA 50.4 / 71.4 / 67.3), which the authors find
   "problematic": "models are able to leverage information from the adversarial documents". GPT-3.5 detects the most
   errors yet is the weakest model.

![[Ngo2024-fig-03-p4.png]]
*Figure 11: sufficiency test, main-question accuracy vs signal percentage p (5 documents; blue GPT-3.5, orange
GPT-4o-mini, green Llama-3-70B). At p = 0 models mostly abstain.*

![[Ngo2024-fig-07-p7.png]]
*Figure 15: robustness test, main-question accuracy vs percentage of factually correct documents (5 documents;
p = 0 means every document was counterfactually edited).*

**Table 1 (condensed): standard-RAG accuracy %, as No retrieval / Offline 5 / Offline 20 / Online 5 / Online 20 docs**

| LLM | BioASQ | PubMedQA | MedQA | MMLU |
|---|---|---|---|---|
| GPT-3.5 | 77.7 / 81.2 / 87.2 / 87.2 / 87.9 | 49.8 / 59.6 / 71.0 / 58.4 / 60.6 | 68.3 / 63.0 / 67.3 / 68.0 / 68.4 | 76.3 / 70.3 / 73.0 / 75.7 / 74.8 |
| GPT-4o-mini | 82.9 / 85.3 / 90.5 / 89.0 / 90.0 | 47.0 / 60.8 / 71.8 / 60.6 / 61.2 | 79.2 / 77.1 / 79.5 / 79.0 / 80.6 | 88.3 / 84.6 / 87.3 / 86.0 / 87.1 |
| GPT-4o | 87.9 / 86.1 / 90.8 / 87.4 / 87.4 | 52.6 / 59.2 / 71.2 / 53.2 / 54.4 | 89.5 / 83.7 / 86.9 / 84.6 / 86.9 | 93.4 / 88.3 / 90.1 / 89.5 / 89.1 |
| PMC-LLaMA-13B | 64.2 / 64.6 / 64.6 / 63.9 / 64.1 | 55.4 / 54.0 / 54.0 / 54.8 / 54.6 | 44.5 / 38.9 / 38.8 / 43.4 / 43.7 | 49.7 / 43.7 / 44.0 / 48.4 / 48.2 |
| MEDITRON-70B | 68.8 / 74.0 / 74.8 / 79.8 / 79.2 | 53.0 / 53.4 / 47.8 / 58.8 / 46.8 | 51.7 / 56.0 / 57.4 / 61.8 / 62.9 | 65.3 / 65.1 / 66.3 / 67.6 / 69.3 |
| Gemma-2-27B | 80.3 / 83.3 / 88.7 / 88.7 / 89.2 | 41.0 / 52.0 / 59.0 / 52.6 / 49.4 | 71.2 / 69.8 / 71.7 / 75.9 / 76.9 | 83.5 / 77.9 / 82.5 / 82.2 / 83.6 |
| Llama-3-70B | 82.9 / 84.6 / 89.3 / 89.3 / 89.3 | 59.2 / 77.6 / 70.8 / 59.4 / 59.2 | 82.9 / 73.6 / 79.4 / 76.1 / 78.3 | 85.2 / 77.6 / 83.4 / 81.8 / 83.8 |

**Across scenarios (5 documents), main accuracy %, as GPT-3.5 / GPT-4o-mini / Llama-3-70B** (from Table 1 and the
bar labels of Figs. 11–15)

| Condition | BioASQ | MedQA | MMLU |
|---|---|---|---|
| No retrieval | 77.7 / 82.9 / 82.9 | 68.3 / 79.2 / 82.9 | 76.3 / 88.3 / 85.2 |
| Standard RAG (offline) | 81.2 / 85.3 / 84.6 | 63.0 / 77.1 / 73.6 | 70.3 / 84.6 / 77.6 |
| Sufficiency, p = 0 (all irrelevant) | 10.2 / 9.4 / 6.0 | 43.8 / 54.6 / 56.0 | 40.9 / 43.5 / 40.5 |
| … share answering "insufficient" | 82.2 / 90.0 / 93.2 | 24.4 / 31.7 / 26.6 | 40.2 / 52.4 / 52.7 |
| Sufficiency, p = 20 | 61.5 / 60.8 / 54.1 | 48.6 / 68.1 / 63.2 | 57.5 / 66.5 / 65.5 |
| Sufficiency, p = 100 | 76.9 / 81.6 / 80.1 | 55.3 / 73.3 / 70.8 | 64.1 / 80.0 / 75.6 |
| Integration, p = 20 | 66.3 / 73.0 / 59.4 | 57.3 / 72.2 / 66.5 | 66.0 / 80.5 / 71.9 |
| Integration, p = 100 | 82.9 / 85.6 / 84.8 | 56.4 / 72.6 / 70.1 | 66.9 / 82.5 / 75.7 |
| Robustness, p = 0 (all counterfactual) | 63.3 / 70.6 / 68.3 | 50.4 / 71.4 / 67.3 | 60.1 / 80.4 / 69.9 |
| Robustness, p = 80 | 77.0 / 84.3 / 81.4 | 55.2 / 72.6 / 70.2 | 65.8 / 80.9 / 73.9 |

## Relevance to research questions
### Q5: Evaluating KG-augmented medical LLMs
This paper supplies the **controls** that MIRAGE-style accuracy lacks. All four can be rebuilt more cleanly from our
graph, because we know exactly which facts are relevant and which are true:
- **Standard:** gold KG paths for the question, e.g. the ingredients of the patient's dish, their compounds, and the
  linked conditions or drug interactions.
- **Sufficiency (irrelevant knowledge):** mix gold paths with paths for *other* dishes, conditions or drugs at
  p ∈ {0, 20, …, 100}, and add an "insufficient information" option. This separates "the KG helped" from "any
  medical-looking context changed the answer".
- **Integration (multi-hop):** one sub-question per hop (does dish X contain ingredient Y? which compound? which
  condition or drug?). Score the hops separately from the final answer, which shows *where* a KG-grounded chain breaks.
- **Robustness (counterfactual knowledge):** flip single edges (effect direction, evidence grade, a food–drug
  interaction from "avoid" to "safe"). With a KG this is exact and auditable. MedRGB needed GPT-4o rewrites, which may
  not always contradict the original.

Numbers to expect and pitfalls:
1. Without an abstain option, RAG can cost a strong model 5–9 points on exam questions (5 offline documents: GPT-4o
   MedQA −5.8, Llama-3-70B −9.3; with 20 documents −2.6 and −3.5).
2. All-irrelevant context with an abstain option costs 25–45 points on MedQA/MMLU. Report the abstention rate and
   score abstentions separately rather than as plain errors, or the noise condition dominates the result.
3. Misinformation detection of ~7–29% means a single wrong food–drug edge in our graph is likely to pass into the
   answer. The robustness test is therefore our **safety** metric, not an optional extra.
4. The GPT-judged sub-answer score (~79–84%) is far more lenient than exact match (~20–35%); use exact or structured
   matching against KG ids for hop-level scoring.
5. No significance tests, one run, and GPT-4o both generated the data and was evaluated. We should use paired tests and
   a non-GPT generator or judge.

See [[Q5 Evaluating KG-augmented medical LLMs]]

### Q6: Supplying the KG to an LLM
- **Curated source, more documents.** The offline curated corpus kept improving from 5 to 20 documents, web search did
  not. Our graph is a curated source, so passing more paths is likely safe *if* they are relevant. Integration-style
  prompting (one sub-question per path) helped most when relevant paths were a minority (p = 20–40).
- **Give the model a trust signal.** Models accepted planted errors and could not tell relevant from irrelevant when
  everything was relevant. Each verbalised claim should therefore carry its **source and evidence grade** (which our
  graph has), and the prompt should ask the model to weigh conflicts by grade. MedRGB documents carry no such signal.
  Whether grades actually raise error detection is untested, so it would be a contribution of ours.
- **Do not force KG context on every question.** Irrelevant context made models abstain on questions they could answer
  closed-book. Route to the KG (or retrieve with a relevance threshold) only when the case mentions foods, herbs,
  diets or drugs.
- **Structure helps only partly.** Sub-questions guide extraction but "may also restrict models' reasoning to only the
  given questions". For multi-hop dish→condition chains, a structured path (graph-RAG style) is worth testing against
  per-hop sub-questions.

See [[Q6 Supplying the KG to an LLM]]

## Limitations / caveats
- We processed arXiv v1 (Nov 2024). The workshop version (AAAI 2026 AI4Research) is titled "MedRGB: Practical
  Framework for Benchmarking Medical Retrieval-Augmented Generation System" and may differ.
- Data and code were promised "upon acceptance"; no public release was found, so the benchmark cannot yet be reused
  directly.
- The full results tables (Tables 4–6) are dense. The values in this note come from Table 1 and the bar labels of
  Figs. 11–15, which match the 5-document rows. The integration text says 10 documents, but Fig. 13 shows the
  5-document numbers.
- Standard-RAG vs scenario comparisons mix conditions: only the sufficiency prompt offers the abstain option, and it is
  not stated whether scenario contexts use offline, online or both signal sets.
- "Signal" documents are retrieved, not verified to contain the answer, and "noise" documents are other questions'
  signal documents, so both are approximate.
- Only 3 models in the three advanced tests; single-turn MCQA only (authors' limitation); no human evaluation.

## Related work to follow
![[Backlog.base#Cited by this paper]]
