---
title: "LLMs as Cultural Archives: Cultural Commonsense Knowledge Graph Extraction"
citekey: Tonga2026
authors: [Junior Cedric Tonga, Chen Cecilia Liu, Iryna Gurevych, Fajri Koto]
year: 2026
published: 2026-03-24
venue: "EACL 2026"
peer_reviewed: true
url: "https://aclanthology.org/2026.eacl-long.295/"
arxiv: ""
doi: ""
pdf: "[[Tonga2026.pdf]]"
pdf_url: "https://aclanthology.org/2026.eacl-long.295.pdf"
datasets: []
topics: [kg-medical-eval]
questions: [Q5, Q6]
relevance: core
found_by: [user]
cites: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/5
  - q/6
  - inject/vector-rag
  - inject/context
  - eval/mcqa
  - eval/human
  - eval/llm-judge
---
# LLMs as Cultural Archives: Cultural Commonsense Knowledge Graph Extraction

> [!abstract] TL;DR
> The source paper of this project. GPT-4o is prompted to write ATOMIC-style if–then assertions (*action → relation
> → action*) about daily life in five countries, which are expanded iteratively into multi-step **paths**, giving a
> Cultural Commonsense Knowledge Graph (CCKG). Feeding retrieved assertions or paths **in context** to small LLMs
> gives small, mixed gains on cultural MCQA and clear gains in human-rated story generation.

## What was built
- **Resource:** CCKG for China, Indonesia, Japan, England and Egypt, in English and each native language; 11 daily-life
  topics, 65 subtopics (food, weddings, pregnancy, death, religious holidays…); 37,363 English and 16,709
  native-language assertions after de-duplication, composed into **27,649 English and 6,571 native-language paths**. Code at [GitHub](https://github.com/JuniorTonga/Cultural_Commonsense_Knowledge_Graph); the
  full generated graph is available on request (see `research/cultural_dataset_search_2026-09-22.md`).
- **Construction:** five relations (`xNext`, `xEffect`, `xNeed`, `oNext`, `oEffect`; the `x/oNext` ones are new).
  Step 1 generates initial assertions per subtopic; step 2 expands `xNext`/`oNext` assertions with intermediate and
  forward actions; post-processing composes simple paths per subtopic.
- **Quality (human, binary labels, 2 native annotators):** English versions score higher than native-language ones on
  most criteria, e.g. Egypt cultural relevance 56.9% (EN) vs 13.4% (MSA); China 80.8% vs 59.1%.

![[Tonga2026-fig-01-p1.png]]
*Figure 1: initial generation, iterative expansion and post-processing into a CCKG sub-graph (breakfast, Indonesia).*

## How the KG is given to an LLM (→ Q6)
- **In-context augmentation:** 5 retrieved assertions ("-Asrt") or 1 retrieved path ("-Path") are prepended to the
  benchmark prompt.
- **Retrieval:** semantic search with SBERT `stsb-xlm-r-multilingual` embeddings between the question and the
  verbalised assertions or paths.
- No fine-tuning, no tool use, no graph traversal at inference time.

## How the gain is measured (→ Q5)
- **Benchmarks:** [[ArabCulture]] (13 Arab countries, MSA) and IndoCulture (11 Indonesian provinces), as 3-option MCQA
  (accuracy, official scripts) and as open sentence completion (BERTScore-F1 and sentence similarity to the reference).
- **Models:** 13 small models (Qwen2.5 0.5–7B, Llama3.x 1–8B, Gemma2 2–9B; base and instruction-tuned).
- **Baselines:** zero-shot (Base), chain-of-thought (CoT), and in-context augmentation with another LLM-extracted
  knowledge base, Mango (5-shot assertions). Conditions vary the KG language (English vs native) and unit
  (assertion vs path).
- **Free-form generation:** short stories on 25 subtopics for China, Indonesia and Egypt, rated 1–10 by two
  annotators for cultural relevance, fluency and coherence; GPT-4o as LLM-judge, checked by correlation with humans.

## Key findings
1. **MCQA gains are small and dataset-dependent.** Average change over Base on IndoCulture: CoT −3.8, Mango +0.6,
   English assertions +0.8, English paths +0.7, native assertions +1.0, native paths +1.2. On ArabCulture: CoT −4.6,
   Mango −1.3, English assertions −0.7, English paths −1.5, native assertions **+0.4**, native paths −1.2.
2. **Small or base models benefit most;** strong instruction-tuned models can lose accuracy: Gemma2-9B-IT on
   ArabCulture drops from 57.3% (Base) to 42.9–49.3% with any augmentation. Qwen2.5-7B (base) gains the most on
   ArabCulture, 49.3% → 59.6% with Arabic assertions.
3. **Chain-of-thought hurts** cultural commonsense MCQA on almost every model.
4. **Sentence completion:** similarity rises (e.g. Llama3.1-8B-IT 32.6 → 36.0 on IndoCulture), BERTScore barely moves.
5. **Stories:** 1-shot CCKG paths raise human scores in all nine model–country pairs, most for cultural relevance
   (+1.4 on average for Llama). Inter-annotator correlation is 0.72 for cultural relevance but only 0.34 for
   coherence and 0.26 for fluency.
6. **LLM-as-judge:** correlation with humans on cultural relevance is ~0.4 for English stories and ~0.8 for
   native-language stories; for English fluency and coherence it is ≈0 or negative.

![[Tonga2026-fig-02-p9.png]]
*Figure 2: relative lift from +CCKG over the baseline in native vs English story generation (human scores).*

## Relevance to research questions
### Q5: Evaluating a KG-augmented LLM
This is the template our evaluation should improve on. It shows the minimum set of comparisons: no knowledge, a
reasoning-only baseline (CoT), and a **competing knowledge source** (Mango), each crossed with the KG's language and
unit. It also shows the risks: on a strong model the KG can **lower** accuracy, MCQA differences of ±1 point need
significance tests, and LLM-judges agree with humans only partly. For a medical KG the same design applies, with
case→conclusion benchmarks instead of cultural commonsense MCQA and a safety dimension that this paper does not have.

See [[Q5 Evaluating KG-augmented medical LLMs]]

### Q6: Supplying the KG to an LLM
The paper uses the simplest option: dense retrieval of verbalised assertions or paths, put in the prompt as
few-shot context. Paths help most for open generation, assertions for MCQA, and native-language knowledge for
native-language questions. It does not compare with graph traversal, tools, or fine-tuning, so those remain
open for our graph.

See [[Q6 Supplying the KG to an LLM]]

## Limitations / caveats
- The graph is LLM-generated, so it inherits GPT-4o's errors and stereotypes; the authors call it a research
  prototype, "not a formal dataset".
- Only five higher-resource countries; country-level culture only.
- Prompt-sensitive construction; MCQA has 3 options (33% chance), and several base models sit near chance on
  ArabCulture regardless of method, which makes their "gains" uninformative.
- No statistical tests are reported for the ±1-point MCQA differences.

## Related work to follow
![[Backlog.base#Cited by this paper]]
