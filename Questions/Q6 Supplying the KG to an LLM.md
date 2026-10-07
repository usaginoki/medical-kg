---
question: "How should the knowledge graph be supplied to an LLM: in context, vector retrieval, graph retrieval, tools/MCP, or fine-tuning?"
id: Q6
topics: [kg-medical-eval]
updated: 2026-10-07
tags:
  - type/question
  - q/6
---
# Q6: How should the knowledge graph be supplied to an LLM: in context, vector retrieval, graph retrieval, tools/MCP, or fine-tuning?

> [!summary] Short answer
> **Retrieve, then put a small amount in context.** Do not dump the graph and do not fine-tune first. Three routes fit
> our DuckDB graph, one per kind of question:
> 1. **Exact lookups** ("I take warfarin, can I eat X?"): **typed tools**, e.g. an MCP server with a few functions
>    (`interactions(drug, food)`, `dish_ingredients(dish)`, `evidence(claim_id)`). Do not use free text-to-SQL.
> 2. **Multi-hop questions** (dish → ingredient → compound → condition): **entity-linked path retrieval**. Rank the paths
>    by evidence grade and relevance, and verbalise them with source and grade.
> 3. **Fuzzy, culture-level questions** ("Uzbek dishes that may help anaemia"): **vector retrieval** over verbalised
>    claims (BM25 + dense).
>
> Show evidence grades to the model as tiers. Retrieve only when the question mentions foods, herbs, diets or drugs.
> Expect gains mainly for **small models**. Strong models can get *worse* with extra context
> ([[Tonga2026 - LLMs as Cultural Archives|Tonga et al. 2026]],
> [[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]], [[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo et al. 2024]]).
> Fine-tuning and Microsoft-style GraphRAG are later, optional arms.

## Detailed answer

### 1. What the source paper did, and what it leaves open
[[Tonga2026 - LLMs as Cultural Archives|Tonga et al. 2026]] used the simplest route:
- **Retrieval:** SBERT (`stsb-xlm-r-multilingual`) semantic search between the question and the verbalised assertions or paths.
- **Prompt:** 5 assertions or 1 path prepended as few-shot context.
- **Results:** gains on IndoCulture MCQA were ≤ 1.2 points on average. On ArabCulture most variants *lowered* accuracy,
  and Gemma2-9B-IT fell from 57.3% to 42.9–49.3%. Story generation improved in all nine model–country pairs.

The paper does not compare this with graph traversal, tools or fine-tuning; those are the open options below.

### 2. The options and the evidence for each
**In context / long context (dump the neighbourhood).**
- Long EHR contexts were matched or beaten by targeted retrieval of fewer than 8K tokens
  ([[Myers2025 - Evaluating RAG vs Long-Context Input for Clinical Reasoning over EHRs|Myers et al. 2025]]).
- Accuracy is U-shaped over where the useful snippet sits ([[Liu2023a - Lost in the Middle|Liu et al. 2023]];
  [[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]).
- Raw triple dumps can hurt small models ([[Tian2023 - Graph Neural Prompting with Large Language Models|Tian et al. 2023]]).
- Our 5.2M claims fan out (one dish reaches thousands of conditions), so dumping is not viable.

**Vector RAG over text or verbalised claims.**
- MIRAGE/MedRAG ([[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]):
  - 32 snippets raised GPT-3.5 from 60.7 to 71.6 and GPT-4 from 73.4 to 80.0 on average, but almost all of the gain is
    on literature-derived sets. On exam questions GPT-3.5 gained +1.6 to +2.8 and GPT-4 *lost* 1.2–3.2.
  - Fusing BM25 with a dense retriever (RRF) was most robust, and k ≤ 8 snippets was worse than CoT.
- Naive top-k retrieval returned only 22% relevant passages and lowered factuality by up to 6% in an expert
  evaluation; filtering and query reformulation recovered it
  ([[Kim2025 - Rethinking Retrieval-Augmented Generation for Medicine|Kim et al. 2025]], preprint).
- With 5 documents, retrieval *lowered* GPT-4o on MedQA from 89.5 to 83.7
  ([[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo et al. 2024]]).
- Culturally, knowledge-base grounding was limited by coverage and retriever quality, and neither grounding method
  improved human-judged cultural fluency
  ([[Lertvittayakumjorn2025 - Towards Geo-Culturally Grounded LLM Generations|Lertvittayakumjorn et al. 2025]]).

**Entity-linked subgraph or path retrieval (KG-RAG).**
- KG-RAG on SPOKE ([[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman et al. 2024]]):
  - The pipeline links the disease, fetches its neighbours, prunes edges by embedding similarity and keeps provenance.
  - It raised Llama-2-13b MCQ accuracy from 0.31 to 0.53, GPT-3.5 from 0.63 to 0.79 and GPT-4 from 0.68 to 0.74.
  - It retrieved correctly in 97% of cases vs 75% for LLM-written Cypher, and still 97% vs 0% when names were
    lower-cased, with 53.9% fewer tokens.
- iDISK2.0 ([[Hou2025 - iDISK2.0 supplement RAG|Hou et al. 2025]]):
  - The relation is chosen from the entity-type pair, so the LLM never writes queries.
  - Supplement–drug interaction MCQ accuracy rose from 52% (GPT-4 alone) to 95%.
- Diverse K-shortest paths gave +19.8 F1 on interaction severity
  ([[Abdullahi2025 - K-Paths|Abdullahi et al. 2025]]).
- Confidence-ranked paths from a TCM medicine–food-homology KG gave +14.5% Hits@1 for diet recommendations
  ([[Sha2025 - Leveraging Retrieval-Augmented LLMs for Dietary Recommendations With TCM Medicine Food Homology (Yaoshi-RAG)|Sha et al. 2025]]).
  This is the closest published analogue to our traditional-medicine layer.
- KG paths plus neighbours (MindMap) stayed robust when the KG was mismatched
  ([[Wen2023 - MindMap Knowledge Graph Prompting Sparks Graph of Thoughts in LLMs|Wen et al. 2023]]).
- Showing evidence-quality tiers in the prompt cut omissions from 16.3% to 5.3%
  ([[Hu2026 - Propagating construction-time knowledge quality into medical QA (clinical guidelines)|Hu et al. 2026]], preprint).

**Microsoft-style GraphRAG (community summaries).**
- It pays off only for multi-hop and summarisation questions, at roughly 40× the tokens of plain RAG; plain RAG is as
  good on fact lookup ([[Xiang2025 - When to use Graphs in RAG|Xiang et al. 2025]], preprint).
- In medicine its gain over plain RAG was small: GPT-4 MedQA 88.1 → 88.9
  ([[Wu2024a - Medical Graph RAG|Wu et al. 2024]]).
- Our graph is already structured, so building community summaries adds little.

**Tools, text-to-query and MCP.**
- Typed MCP tools scored 98% vs 85% for text-to-Cypher and 75% with no KG, though on only 40 questions
  ([[Mandarapu2026 - Open Biomedical Knowledge Graphs at Scale|Mandarapu et al. 2026]], preprint).
- API tools beat text retrieval for exact database facts, 0.83 vs 0.44 ([[Jin2023 - GeneGPT|Jin et al. 2023]]).
- Free text-to-SQL reached only ~60% execution accuracy on biomedical knowledge bases
  ([[Koretsky2025 - BiomedSQL|Koretsky et al. 2025]]).
- LLM-written Cypher broke on lower-cased names ([[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman et al. 2024]]).
- Agents over typed drug tools reached 92.1% on open-ended drug reasoning ([[Gao2025a - TxAgent|Gao et al. 2025]]).
- Biomedical MCP servers are now common enough for a registry
  ([[Kuehl2025 - BioContextAI is a community hub for agentic biomedical systems|Kuehl et al. 2025]]).
- Our `db/trace.py dish|condition --country --drug` is already the core of such tools.

**Fine-tuning, continued pretraining, graph tokens.**
- On facts new to the model, RAG scored 0.875 vs 0.504 for unsupervised fine-tuning
  ([[Ovadia2023 - Fine-Tuning or Retrieval Comparing Knowledge Injection in LLMs|Ovadia et al. 2023]]).
- Continued pretraining on a verbalised UMLS graph helped BERT but not BioBERT, while GraphRAG added +3/+5 points with
  no retraining ([[Klila2026 - Injecting Structured Biomedical Knowledge into Language Models|Klila et al. 2026]]).
- Domain fine-tuning beat RAG on the same base in MIRAGE (+13.5% vs +6.3% relative), and RAG still added on top
  ([[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]).
- Graph neural soft prompts can be strong (+13.5% on frozen LLMs) but need open weights and training, and give up
  readable citations ([[Tian2023 - Graph Neural Prompting with Large Language Models|Tian et al. 2023]]).
- Fine-tuning also freezes a graph that keeps changing (HMDB is still missing from the current build).

### 3. What fits our graph
Our DuckDB has a fixed schema (dish → ingredient → compound → condition, ingredient × drug), precomputed path views
and an evidence grade on every row ([[Unified database]], [[Export tables]]). That makes a routed design natural:

| Question type | Example | Route | Why |
|---|---|---|---|
| Point lookup | "warfarin + turmeric?" | typed tool over `ingredient_drug` (MCP or function calling) | exact, cheap, auditable; text-to-SQL is brittle |
| Multi-hop | "what can Timman rice do for an anaemic patient?" | entity link → filter `v_dish_condition` / rollups → rank by grade × relevance → verbalise ≤ k paths | KG-RAG/K-Paths style; salience rules pre-filter the fan-out |
| Explanation | "why is this dish risky for hypertension?" | path retrieval + require citations to claim ids | provenance is our advantage over text RAG |
| Fuzzy / cultural | "Kyrgyz dishes that may help a cough" | hybrid vector retrieval over verbalised claims | open-ended phrasing, multilingual aliases |
| General medicine | MedQA item with no food or drug content | no KG (router says no) | irrelevant context makes models abstain or err |

Implementation notes for our data:
- **Multilingual entity linking.** We have 11,005 ingredient aliases in 9 languages and 233k condition aliases, so the
  linker needs a multilingual embedder plus exact alias matching. The English-only retrievers in these papers were never
  tested on zh/ja/ar/fa names.
- **Verbalisation.** One sentence per claim with direction, evidence type, source, tradition and PMIDs, e.g. "licorice —
  harmful for — hypertension (SpiceRx, text-mined, 12 positive / 57 negative papers)". Keep conflicting claims side by
  side.
- **Routing and logging.** Log whether each answer used the KG or fell back to the model's own knowledge, and score the
  two separately ([[Hou2025 - iDISK2.0 supplement RAG|Hou et al. 2025]]).

## Comparison table
| Supply method | Best evidence | Typical effect | Token cost | Keeps provenance | Our priority |
|---|---|---|---|---|---|
| Dump neighbourhood in context | Myers 2025; Liu 2023 | ≈ or below targeted retrieval; lost in the middle | high | yes | no |
| SBERT top-k over claims (Tonga-style) | [[Tonga2026 - LLMs as Cultural Archives\|Tonga 2026]] | ±1 point MCQA; helps small models, can hurt strong ones | low | yes | **baseline (replication)** |
| Hybrid vector RAG (BM25 + dense, RRF) | [[Xiong2024 - MIRAGE MedRAG benchmark\|Xiong 2024]] | up to +11 points (GPT-3.5); ≤ +3 or negative on exams | low–moderate | yes | baseline |
| Entity-linked subgraph / path RAG with grade tiers | [[Soman2024 - KG-RAG on the SPOKE biomedical KG\|Soman 2024]]; [[Hou2025 - iDISK2.0 supplement RAG\|Hou 2025]]; K-Paths; Yaoshi-RAG; Hu 2026 | +6 to +43 points on KG-answerable items | moderate | yes | **main method** |
| Typed tools / MCP over DuckDB | Mandarapu 2026; GeneGPT; TxAgent | 75% → 98% on 40 KG questions | low tokens, more turns | yes | **main method for lookups** |
| Free text-to-SQL / Cypher | BiomedSQL; Soman 2024 | ~60% execution accuracy; brittle | moderate | yes | no (only behind tools) |
| Microsoft GraphRAG | Xiang 2025; Wu 2024a | +0.8 over RAG on MedQA (GPT-4) | very high | partly | no |
| Fine-tuning / continued pretraining | Ovadia 2023; Klila 2026 | weaker than RAG on new facts | high upfront | no | later arm |
| GNN soft prompts | Tian 2023; He 2024 | strong on frozen LLMs | training | no | methods paper only |

## Gaps & open questions
1. **No head-to-head on the same medical benchmark.** No study compares typed tools vs path retrieval vs vector RAG on
   the same set at scale; the MCP evidence is 40 questions in a preprint. Running that comparison on our graph would be
   a contribution.
2. **Do evidence grades work as a trust signal?** Models detect only ~7–29% of planted errors when documents carry no
   trust signal ([[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo et al. 2024]]). Whether showing our grades
   raises error detection is untested.
3. **Multilingual retrieval.** Linking in Arabic, Persian, Chinese, Japanese, Kazakh and Russian is untested in the
   medical KG-RAG papers. Tonga et al. found native-language assertions help native-language questions.
4. **When should the KG be skipped?** Retrieving only when needed (e.g. Self-BioRAG,
   [[Jeong2024 - Improving Medical Reasoning through Retrieval and Self-Reflection with Retrieval|Jeong et al. 2024]])
   is a candidate design that our router should be tested against.
5. **Fine-tuning arm.** Synthetic QA generated from KG subgraphs
   ([[Jonker2026 - BioGraphletQA Knowledge-Anchored Generation of Complex QA Datasets|Jonker et al. 2026]]) could train a
   small model to call our tools or answer with paths. It is untested in the food-health domain.

## Papers
![[Papers.base#This question]]
