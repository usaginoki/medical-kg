---
title: "Biomedical knowledge graph-optimized prompt generation for large language models"
citekey: Soman2024
authors: [Karthik Soman, Peter W Rose, John H Morris, Rabia E Akbas, Brett Smith, Braian Peetoom, Catalina Villouta-Reyes, Gabriel Cerono, Yongmei Shi, Angela Rizk-Jackson, Sharat Israni, Charlotte A Nelson, Sui Huang, Sergio E Baranzini]
year: 2024
published: 2023-11-29
venue: "Bioinformatics 2024"
peer_reviewed: true
url: "https://academic.oup.com/bioinformatics/article/40/9/btae560/7759620"
arxiv: "2311.17330"
doi: "10.1093/bioinformatics/btae560"
pdf: "[[Soman2024.pdf]]"
pdf_url: "https://arxiv.org/pdf/2311.17330"
datasets: []
topics: [kg-medical-eval]
questions: [Q5, Q6]
relevance: core
found_by: [search/evaluation, search/supply]
added: 2026-10-07
cites:
  - "[[Morris2023 - The scalable precision medicine open knowledge engine (SPOKE)]]"
  - "[[Singhal2022 - Large Language Models Encode Clinical Knowledge]]"
  - "[[Yasunaga2021 - QA-GNN]]"
  - "[[Yasunaga2022 - Deep Bidirectional Language-Knowledge Graph Pretraining]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/5
  - q/6
  - inject/graph-rag
  - inject/tool
  - eval/mcqa
  - eval/retrieval
---
# Biomedical knowledge graph-optimized prompt generation for large language models

> [!abstract] TL;DR
> **KG-RAG** links the disease named in a question to a node of the SPOKE biomedical KG (42 M nodes) and fetches that
> node's neighbours. It verbalises the edges with their provenance and keeps only the edges most similar to the question
> (embedding prune, at most 100–150 edges), then puts them in the prompt. On expert-reviewed biomedical true/false and 5-option
> MCQ sets it improves Llama-2-13b, GPT-3.5-Turbo and GPT-4 (Llama-2 MCQ 0.31 → 0.53, "~71%"). Against
> LLM-written Cypher queries (Cypher-RAG) it retrieves more reliably (97% vs 75%; 97% vs 0% when entity names are
> lower-cased) and uses 53.9% fewer tokens.

## What was built
- **Framework:** KG-RAG, seven steps: "i) entity recognition from user prompt; ii) extraction of biomedical concepts from
  SPOKE; iii) concept embedding; iv) prompt-aware context generation; v) conversion into natural language; vi) prompt
  assembly; and vii) answer retrieval". Code and benchmark sets: [GitHub BaranziniLab/KG_RAG](https://github.com/BaranziniLab/KG_RAG).
- **KG:** SPOKE, "42 million nodes of 28 different types and 160 million edges of 91 types", built from 41 biomedical
  databases, "the vast majority" from curated experimental data rather than literature text mining. It is accessed
  through a REST API.
- **LLMs:** Llama-2-13b (4,096-token window, self-hosted), GPT-3.5-Turbo and GPT-4 (OpenAI API), all at temperature 0.
- **Benchmarks they built:** 311 true/false questions (from DisGeNET, MONDO, SemMedDB), 306 five-option single-answer
  MCQs (from Monarch Initiative and ROBOKOP), "thoroughly reviewed by domain experts to remove any false positives"; 100
  disease–gene questions from SPOKE for the retrieval comparison; 165 validation prompts (75 one-disease, 90
  two-disease) for hyperparameter tuning.
- **Version note:** the docling text is arXiv v2 (2024-05-13). The *Bioinformatics* version (received 15 May 2024,
  published 17 Sep 2024) adds a third retrieval baseline, Neo4j's Lucene full-text index (numbers below, read from the
  journal page).

## How the KG is given to an LLM (→ Q6)
Graph retrieval with embedding-based linking and pruning. The result goes into the prompt as plain-English triples.
No fine-tuning, and no tool calls at answer time.
1. **Disease entity recognition.** GPT-3.5-Turbo, prompted zero-shot, extracts disease names as JSON. Each name is matched
   to SPOKE disease nodes by cosine similarity of `all-MiniLM-L6-v2` embeddings (384-d, stored in Chroma). The
   extraction plus matching step "retrieved the disease nodes from the graph with an accuracy of 99.7%". If no
   disease is extracted, the 5 disease nodes most similar to the whole prompt are used.
2. **Context retrieval.** The neighbours of each matched disease node, i.e. one hop (the journal version names SPOKE's
   `/api/v1/neighborhood/` endpoint). Only disease-centred questions are supported.
3. **Graph → text.** SPOKE predicate names encode the subject and object types (e.g. `ASSOCIATES_DaG`), so a rule
   turns a triple into a sentence: `(Disease hypertension, ASSOCIATES_DaG, Gene VHL)` → "Disease hypertension
   associates Gene VHL". **Provenance** (the edge's source attribute) is always appended. Statistical evidence
   (p-value, z-score, enrichment score) is appended when the `-e` flag is set (off by default).
4. **Context pruning.** The prompt and every verbalised association are embedded (PubMedBERT after tuning). An
   association is kept if its similarity is "(i) greater than 75th percentile of the similarity distribution
   encompassing all the context related to the chosen disease node and (ii) having a minimum similarity value of 0.5".
   **Context volume** "defines the upper limit on the number of graph connections permitted to flow from the KG to the
   LLM": 150 by default, 100 for true/false.
5. **Prompt assembly.** The question plus this "prompt-aware context" go to the LLM.

The paper defines **prompt-aware context** as "only the essential biomedical context from SPOKE … which is adequate
enough to address the user prompt with accurate provenance and statistical evidence".

**Comparison arm (text-to-query): Cypher-RAG.** LangChain's `GraphCypherQAChain`. The method "involves explicitly
embedding the schema of the graph into the input prompt, directing the LLM to generate a structured Cypher query based
on this schema". It was compared on retrieval and token use only, not on final answer accuracy.

## How the gain is measured (→ Q5)
- **Arms:** "prompt-based" (the question alone) vs KG-RAG, for each of the 3 LLMs. There is no chain-of-thought, text-RAG
  or fine-tuning baseline.
- **Answer accuracy:** true/false and MCQ. 150 questions are sampled with replacement 1,000 times, and accuracy is
  reported as the mean ± std of the bootstrap distribution.
- **Retrieval:** on 100 SPOKE disease–gene questions, whether the gold association reaches the context (KG-RAG vs
  Cypher-RAG, plus full-text index in the journal version). The same is repeated after a **perturbation**: entity names
  lower-cased.
- **Cost:** average total tokens per answer.
- **Hyperparameters:** GPT-4 with KG-RAG returns JSON lists, which are scored by Jaccard similarity to the ground truth
  across context volumes and two embedding models.
- **Qualitative:** GPT-4 with and without KG-RAG on example prompts (Fig 1), checking whether the answer gives a
  correct, sourced statement.

## Key findings
1. **KG-RAG improved every model on both sets** (Table 1). The largest gain is on MCQ for the smallest model: Llama-2-13b
   0.31 → 0.53, "approximately 71%" relative. GPT-3.5-Turbo MCQ 0.63 → 0.79, GPT-4 MCQ 0.68 → 0.74. True/false rises
   from 0.87–0.90 to 0.94–0.95 for all three.
2. **With KG-RAG, GPT-4 was worse than GPT-3.5-Turbo on MCQ** (0.74 vs 0.79; "T-test, p-value < 0.0001, t-statistic =
   -47.7, N = 1000"). Without RAG GPT-4 was the better of the two. The authors suggest "GPT-3.5 may be a better context
   listener than GPT-4".
3. **Retrieval: KG-RAG 97%, Cypher-RAG 75%.** After lower-casing entity names, Cypher-RAG fell to **0%** because it
   needs exact keyword matches, while KG-RAG stayed at 97%. The journal version adds the full-text index: 61%
   unperturbed, 58% perturbed.
4. **Tokens: 3,693 for KG-RAG vs 8,006 for Cypher-RAG** (−53.9%), because Cypher-RAG puts the whole schema into the
   prompt. The journal version adds 10,590 for the full-text index (−65.1% for KG-RAG).
5. **Pruning hyperparameters.** PubMedBERT beat MiniLM as the pruning embedder: mean Jaccard 0.67 vs 0.61 on
   one-disease prompts, 0.40 vs 0.37 on two-disease prompts. Performance plateaus with context volume. From Fig 2A,
   one-disease PubMedBERT rises from ~0.51 at the smallest volume to ~0.72 at 100–150 and stays there at 200;
   two-disease prompts are still rising at 200 (~0.51).
6. **Provenance shows up in answers.** In Fig 1, KG-RAG GPT-4 names setmelanotide for Bardet–Biedl syndrome with "phase 3"
   and "[Provenance: ChEMBL, DrugCentral]". It also compares the GWAS p-values (4e-14 vs 2e-08) for PNPLA3 vs HLA-B.
   Without KG-RAG, GPT-4 says no specific drug exists.

## Relevance to research questions
### Q5: Evaluating a KG-augmented LLM
Soman et al. give us a minimal **three-level evaluation** to copy, and the main traps to avoid.
- **Copy the three levels.** Measure them separately:
  - *Retrieval:* did the right rows reach the prompt? Use gold associations, e.g. 100 dish→condition or food→drug pairs
    sampled from our tables.
  - *Answers:* KG vs no-KG accuracy per model, over a range of model sizes. Their small open model gained the most,
    as in [[Tonga2026 - LLMs as Cultural Archives|Tonga et al. 2026]].
  - *Cost:* tokens per answer.
- **Copy the perturbation test, adapted to our inputs.** Lower-casing broke exact-match retrieval completely. Our
  equivalents are dish names in local script or transliteration ("plov"/"palov"/"osh"), misspelt ingredients, lay symptom
  words instead of MeSH terms, and TCM terms. Each should be a perturbed copy of the retrieval set.
- **Measure context adherence on its own.** GPT-4 used the KG context worse than GPT-3.5. For each answer we should log
  whether it agrees with the retrieved rows, and whether it overrides them correctly (e.g. a "traditional" claim) or
  wrongly.
- **Avoid their lookup bias.** Their T/F and MCQ items come from curated KBs of the same kind as SPOKE's sources, and the
  overlap is not reported. The gain may therefore be partly KB lookup. For our graph, items generated from our own
  tables would measure lookup only. Questions should come from a held-out source (see
  [[Hou2025 - iDISK2.0 supplement RAG|Hou et al. 2025]], who exclude the question source from retrieval) or from
  case→conclusion benchmarks (Q4).
- **Avoid their statistics.** A t-test over 1,000 bootstrap replicates (t = −47.7) is not a valid significance test,
  because the replicates are resamples of the same ~300 items. We should use paired per-item tests (e.g. McNemar)
  between arms. They also report no open-ended or safety evaluation, both of which we need.

See [[Q5 Evaluating KG-augmented medical LLMs]]

### Q6: Supplying the KG to an LLM
KG-RAG is the closest published architecture to what our DuckDB needs. Each stage maps onto our tables as follows.

| KG-RAG stage | SPOKE implementation | Our DuckDB equivalent / what changes |
|---|---|---|
| Entity linking | LLM extracts diseases → MiniLM vector match over SPOKE disease names (99.7%); fallback top-5 by whole prompt | Link **several entity types**: `dish` (46k, local-script `name_local`), `ingredient_alias` (11,005 aliases in 9 languages), `condition_alias` (233k, incl. TCM), `drug`, plus country. English MiniLM/PubMedBERT will not cover zh/ja/ar/fa aliases, so a multilingual embedder is needed (our inference). Keep the top-k fallback for vague symptom descriptions. |
| Hops | 1 hop around one disease node | Our questions need 2–3 hops (dish → ingredient → compound → condition; dish → ingredient → drug). These are precomputed in `v_ingredient_condition_all`, `ingredient_condition_rollup` and `v_dish_condition`, so "fetch neighbourhood" = filter those views by the linked ids. `v_dish_condition` is ~10⁸ rows unfiltered, so our **salience rules** (characteristic paths) act as a structural pre-filter before the semantic prune. |
| Graph → text | predicate-name rule + provenance (+ p-values with `-e`) | One sentence per path row with `direction`, `evidence_type` (clinical … predicted), `source`, `tradition`, `pmids`, e.g. "licorice — harmful for — hypertension (SpiceRx, text-mined, 12 positive / 57 negative papers)". Keep conflicting rows side by side, as the DB does. |
| Prune | cosine > 75th percentile and ≥ 0.5; cap 100–150 associations | Reusable as is. Re-tune the cap on our tasks, since their plateau was measured on disease→gene list questions. Consider ranking by evidence grade before similarity, so that a clinical row is not dropped in favour of a similar traditional one. |
| Provenance | SPOKE edge source, shown by the model in answers (Fig 1) | Our 5.2M claims all carry source + grade. Test whether the model repeats the grade ("traditional Persian claim, not validated") instead of upgrading it. |

**Tools/MCP vs fixed retrieval.** The Cypher-RAG result is the strongest evidence here against giving the LLM raw
query access as the only route. Text-to-query needed the schema in every prompt (2.2× tokens) and failed on trivial
surface variation. For our DuckDB this favours **typed tools** that do embedding-based linking internally, such as the
existing `db/trace.py dish|condition` with `--country`/`--drug`, over free text-to-SQL. Two limits on this evidence: the
baseline is a 2023 LangChain chain with exact-match Cypher, and only retrieval was compared, not answer quality. A
modern tool-calling model with fuzzy-match helpers remains untested.

See [[Q6 Supplying the KG to an LLM]]

## Key figures & tables
![[Soman2024-fig-05-p18.png]]
*Figure 5: KG-RAG pipeline. LLM disease extraction → match in a disease embedding space → SPOKE neighbourhood →
verbalised edges → prompt–context matching (pruning) → LLM.*

![[Soman2024-fig-02-p8.png]]
*Figure 2: (A) mean Jaccard vs context volume for MiniLM (blue) and PubMedBERT (red) pruning, one- and two-disease
prompts. (B) retrieval accuracy of Cypher-RAG vs KG-RAG, unperturbed and lower-cased, and average token usage
(8,006 vs 3,693).*

![[Soman2024-fig-01-p6.png]]
*Figure 1: GPT-4 with and without KG-RAG. The retrieved edge (with source and p-value) is shown, and the KG-RAG answer
cites ChEMBL/DrugCentral and GWAS p-values.*

*Table 1: accuracy (mean ± std over 1,000 bootstrap samples of 150 questions).*

| Model | True/False, prompt-based | True/False, KG-RAG | MCQ, prompt-based | MCQ, KG-RAG |
|---|---|---|---|---|
| Llama-2-13b | 0.89 ± 0.02 | 0.94 ± 0.01 | 0.31 ± 0.03 | **0.53 ± 0.03** |
| GPT-3.5-Turbo | 0.87 ± 0.02 | 0.95 ± 0.01 | 0.63 ± 0.03 | **0.79 ± 0.02** |
| GPT-4 | 0.90 ± 0.02 | 0.95 ± 0.01 | 0.68 ± 0.03 | 0.74 ± 0.03 |

*Retrieval comparison (100 disease–gene questions; full-text index from the journal version).*

| Method | Retrieval acc. | Retrieval acc., lower-cased | Avg. tokens |
|---|---|---|---|
| Full-text index (Lucene) | 61% | 58% | 10,590 |
| Cypher-RAG | 75% | 0% | 8,006 |
| KG-RAG | 97% | 97% | 3,693 |

## Limitations / caveats
- **Disease-centred only.** Entity recognition embeds only disease nodes, so questions starting from a drug, gene or food
  are out of scope (the authors note this).
- **One-hop context.** Multi-hop reasoning chains are not retrieved. The two-disease prompts score much lower (mean
  Jaccard 0.40 vs 0.67).
- **Small benchmarks.** 311 T/F and 306 MCQ items, with bootstrap std. The T/F baselines are already 0.87–0.90, which
  leaves little headroom. Overlap between the benchmark sources and SPOKE's sources is not analysed.
- **Invalid significance test.** The GPT-4 vs GPT-3.5 test uses N = 1000 bootstrap replicates as if they were independent
  samples.
- **No answer-level comparison with Cypher-RAG.** There are also no human or open-ended ratings beyond the qualitative
  examples, and no harm/safety analysis. The authors say SPOKE is not asserted to be "entirely error-free or ready for
  clinical use".
- **Dated models and versions.** The models are 2023 GPT-3.5/GPT-4/Llama-2. The authors link the GPT-4 result to drift in
  GPT-4's instruction following, so it may not hold for current models.

## Related work to follow
![[Backlog.base#Cited by this paper]]
