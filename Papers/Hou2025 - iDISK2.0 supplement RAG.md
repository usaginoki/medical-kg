---
title: "Improving Dietary Supplement Information Retrieval: Development of a Retrieval-Augmented Generation System With Large Language Models"
citekey: Hou2025
authors: [Yu Hou, Jeffrey R Bishop, Hongfang Liu, Rui Zhang]
year: 2025
published: 2025-03-19
venue: "Journal of Medical Internet Research 2025"
peer_reviewed: true
url: "https://www.jmir.org/2025/1/e67677"
arxiv: ""
doi: "10.2196/67677"
pdf: ""
pdf_url: "https://www.jmir.org/2025/1/e67677/PDF"
datasets: []
topics: [kg-medical-eval]
questions: [Q5, Q6]
relevance: core
found_by: [search/evaluation, search/supply, search/global-cases]
added: 2026-10-07
cites:
  - "[[Hou2023 - From Answers to Insights]]"
  - "[[Su2023 - Biomedical discovery through the integrative biomedical knowledge hub (iBKH)]]"
  - "[[Xu2024 - Retrieval-Augmented Generation with Knowledge Graphs for Customer Service Questi]]"
  - "[[Yan2024 - KNOWNET]]"
  - "[[Zakka2023 - Almanac]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/5
  - q/6
  - inject/graph-rag
  - eval/mcqa
  - eval/safety
---
# Improving Dietary Supplement Information Retrieval: Development of a Retrieval-Augmented Generation System With Large Language Models

> [!abstract] TL;DR
> The authors rebuild the integrated Dietary Supplement Knowledgebase as **iDISK2.0**: 174,317 UMLS-normalised entities
> and 334,265 relations from NMCD, MSKCC "About Herbs", NIH DSLD and Canada's LNHPD, stored in Neo4j. On top of it
> they build a RAG system: GPT-4 extracts entities, embeddings match them to KG nodes, a templated Cypher query fetches the
> triples, and an LLM answers. On true/false and MCQ items generated from MSKCC (with MSKCC withheld from retrieval)
> it scores 95–99%, vs 52–93% for stand-alone GPT-4. The largest gap is on **supplement–drug interactions**: MCQ
> 95% vs 52%, T/F 97% vs 62%.

## What was built
- **Resource: iDISK2.0**, an update of iDISK (2020). 7 entity types: 8,091 dietary-supplement ingredients (DSI), 163,806
  products (DSP), 786 diseases, 625 drugs, 425 symptoms, 567 therapeutic classes, 17 system organ classes. 6 relation
  types (334,265 relations) and 471,063 attributes, including **3,086 DSI–drug interaction ratings** and **4,623
  DSI–disease effectiveness ratings**. Released as CSVs (`dsi`, `dsp`, `disease`, `drug`, `symptom`, `relationships`) on
  [GitHub houyurain/iDISK2.0](https://github.com/houyurain/iDISK2.0) (Apache-2.0, per the repo page).
- **Sources & construction:**
  - MSKCC: crawled after approval. 279 DSI, 270 drugs, 231 diseases, 425 symptoms. GPT-4 extracted disease and drug
    entities from MSKCC's free-text relations.
  - DSLD: release download + API. 4,318 DSI and 92,651 DSP; ingredient synonyms were merged with DSLD's "Ingredient
    Group".
  - LNHPD: 4,690 DSI and 71,364 DSP.
  - NMCD: content carried over from iDISK 1.
  - GPT-4 also unified noisy strings (e.g. company addresses), and filters removed nonsense ingredient names ("8", "%").
  - Entities were mapped to UMLS CUIs with QuickUMLS, restricted by semantic type. A CUI is assigned only if the
    similarity is 1 or the term is preferred, else left blank. Entities were then merged greedily by CUI or identical
    name, triples de-duplicated, and "multiple rounds of manual quality checks" applied.
- **Application:** a Django web portal (iDISK2.0-RAG) for free-text questions (Fig 4 in the paper, not extracted).

## How the KG is given to an LLM (→ Q6)
Graph retrieval with embedding-based entity linking and a **fixed relation per entity-type pair**. The retrieved
triples go into the prompt; there is no fine-tuning.
1. All iDISK2.0 entity names are embedded with OpenAI `text-embedding-3-small`.
2. GPT-4.0 extracts entities from the question with a tailored prompt, and these are embedded with the same model.
3. The best-matching KG entity is taken "provided that the score is 0.75 or higher".
4. The relation is not inferred: "we leverage the fixed and well-defined set of 6 relationship types … to assign
   relationships based on the queried entity pairs. For instance, DSI-disease pairs are always associated with the
   is_effective_for relationship."
5. Matched nodes are turned into Cypher queries on Neo4j. The returned triples, together with the question, go to the LLM.
6. **Fallback:** if no entity matches, "the LLM (GPT-4.0) relies on its internal knowledge base", and the interface tells
   the user that iDISK2.0 has no such knowledge.

The answer-generating LLM is not named separately in Methods. GPT-4.0 is the model named for extraction and fallback.

## How the gain is measured (→ Q5)
- **Items, generated from MSKCC records.** For example, "Vitamin C is used to prevent and treat the common cold" becomes:
  - T/F: "Is it true that Vitamin C is effective for the common cold?" (True);
  - MCQ: "Out of the given list, which disease is Vitamin C effective for?", options "Bladder stones, Common cold,
    Stroke, Bleeding hemorrhoids, and None of the above".
- **Two relation families:** DS–disease effectiveness (164 T/F, 123 MCQ) and **DS–drug interaction** (309 T/F, 206 MCQ).
  In total 473 T/F and 329 MCQ. The paper does not describe how false T/F statements or distractors were generated.
- **Leakage control:** "all knowledge from MSKCC was excluded from the retrieval stage in the RAG framework".
- **Arms:** stand-alone GPT-3.5 and GPT-4.0 vs iDISK2.0-RAG. There is no GPT-3.5 + RAG arm and no text-RAG baseline.
- **Sampling:** 100 random questions per type, repeated 10 times ("bootstrapping"), so each system answers 1,000
  T/F and 1,000 MCQ per relation family. Accuracy is reported per iteration and as a rose plot (Fig 3, not extracted).

## Key findings
1. **RAG ≥ 95% on every item type, stand-alone GPT far lower on interactions** (all numbers from the text):

| Task | iDISK2.0-RAG | GPT-4.0 | GPT-3.5 |
|---|---|---|---|
| T/F, DS–disease effectiveness | 99% (990/1000) | 93% (929/1000) | 85% (854/1000) |
| MCQ, DS–disease effectiveness | 99% (993/1000)¹ | 73% (727/1000) | 43% (426/1000) |
| T/F, **DS–drug interaction** | 97% (974/1000) | 62% (618/1000) | **40%** (400/1000) |
| MCQ, **DS–drug interaction** | 95% (948/1000) | **52%** (517/1000) | 46% (457/1000) |

   ¹ printed as "993/100" in the paper. The abstract also prints "948/100".
2. **Interaction knowledge is the weak spot of stand-alone LLMs.** GPT-4.0 drops from 93% on effectiveness T/F to 62% on
   interaction T/F. GPT-3.5's 40% on interaction T/F is below the 50% of a coin flip.
3. **Example error:** asked which disease ubiquinone (CoQ10) is effective for, GPT-4.0 chose "Cholestasis" (supported by
   only a few studies) over "Migraines" (supported by RCTs). The RAG system answered correctly.
4. **Integration reduces noise.** iDISK2.0 has more entities than iDISK (174,317 vs 144,654) but fewer relations
   (334,265 vs 709,675), mostly from de-duplicated `has_ingredient` links (317,062 vs 689,826). Symptoms shrink from 985
   to 425.

## Relevance to research questions
### Q5: Evaluating a KG-augmented LLM
This is the closest **template for testing our [[DDID]] food–drug layer**. Copy its item format, but fix three
weaknesses.
- **Copy:** one curated record becomes one T/F item plus one 5-option MCQ with "None of the above". Report effectiveness
  and interaction families separately, because the stand-alone gap is largest on interactions. For us, DDID rows in
  `ingredient_drug` would give items such as "Is it true that grapefruit interacts with simvastatin?" and "Which of these
  drugs interacts with liquorice?". The `ingredient_condition` / `compound_condition` claims would give the
  effectiveness family.
- **Copy the leakage control:** withhold the question source from retrieval, as Hou et al. withhold MSKCC. DDID labels
  each row's source (`Relationship_classification`: 17,670 literature, 2,784 DrugBank, 1,666 + 1,009 package-insert,
  821 dietary-effect). We can build items from the package-insert or DrugBank rows and retrieve only from the
  literature rows, or use an independent set such as [[FooDrugs]] or [[DrugBank]] as the question source.
- **Fix 1, true negatives.** The paper does not say how false items were made. DDID's 2,374 "No Effect" rows are real
  tested negatives. Rows graded "Possible" without a PMID (our evidence grade *predicted*) should not be gold.
- **Fix 2, honest counting.** 10 resamples of 100 items give "1000" answers from at most 164–309 distinct questions. We
  should report per-unique-item accuracy with confidence intervals and a paired test.
- **Fix 3, cultural multi-hop.** All of Hou's items are single entity pairs. Our real question is two hops, "I eat
  dish X (country Y) and take drug Z": dish → ingredient → drug through `dish_ingredient` + `ingredient_drug`. We should
  also add open-ended, case-style versions (Q4) graded for whether the warning is given (an `eval/safety` item, not only
  MCQ accuracy).
- **Caution on the headline:** the abstract compares RAG's 99% on effectiveness T/F with GPT's 62%, which is the
  *interaction* T/F score. On the same task GPT-4.0 scored 93%. The abstract also calls the model "GPT-4o" while the body
  says GPT-4.0. Our write-up should compare like with like.

See [[Q5 Evaluating KG-augmented medical LLMs]]

### Q6: Supplying the KG to an LLM
iDISK2.0-RAG shows that for a KG with a **small fixed schema**, the LLM does not have to write queries or choose
relations. It extracts and links entities, and code picks the relation from the entity-type pair. Our DuckDB has the
same property:
- (ingredient, drug) → `ingredient_drug`;
- (ingredient, condition) → `ingredient_condition_rollup`;
- (dish, condition) → `v_dish_condition`;
- (dish, drug) → `dish_ingredient` ⋈ `ingredient_drug`.

So a small set of typed tools or templated SQL calls, one per pair, covers the main question types. This matches
[[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman et al. 2024]]'s finding that LLM-written queries are brittle.

Differences to plan for:
- **No pruning is needed for single pairs.** Our dish–condition paths fan out, though, so we still need salience rules
  and a semantic prune, as in Soman.
- **Linking threshold and fallback.** Hou et al. link with a 0.75 cosine threshold and fall back to the LLM's own
  knowledge. We should log whether each answer came from the KG or from fallback, and score the two separately.
- **Evidence grades.** Hou's triples carry an effectiveness or interaction rating as an attribute. Our rows carry an
  evidence grade, a direction and a tradition, which should be verbalised in the same way.

**Overlap with vault datasets.**
- *Content.* iDISK2.0's interaction layer (3,583 `interacts_with` edges, 3,086 ratings) covers **supplements and
  herbs**. [[DDID]] covers **foods and (mostly TCM) herbs** (23,950 records). [[Dr. Duke's Phytochemical and Ethnobotanical Databases]]
  gives traditional uses of the same kind of botanicals that iDISK2.0 grades for effectiveness.
- *Sources.* None of iDISK2.0's four sources is in `Datasets/`. The Backlog has dataset candidates [[iDISK]] (it points
  to this paper's DOI) and [[NIH DSLD]].
- *Join.* iDISK2.0's diseases carry UMLS CUIs, which can join to `condition.umls_cui` in our DB. Drugs would need a
  UMLS → DrugBank mapping.
- *Use.* The CSVs are on GitHub and could add a supplement–drug layer next to DDID.

See [[Q6 Supplying the KG to an LLM]]

## Key figures & tables
Figures were not extracted: the JMIR PDF is behind bot checks. The text here comes from the Europe PMC full-text XML
(PMC11966073). The four figures are the study pipeline (Fig 1), RAG design (Fig 2), the accuracy rose plot (Fig 3,
numbers in the table under *Key findings*) and portal screenshots (Fig 4).

*Table 1: concepts, relationships and attributes in iDISK (old) vs iDISK2.0 (new).*

| Data element | iDISK (old), n | iDISK2.0 (new), n |
|---|---|---|
| **Concepts** | | |
| Dietary supplement ingredient | 4,208 | 8,091 |
| Dietary supplement product | 137,568 | 163,806 |
| Drug | 495 | 625 |
| Disease | 776 | 786 |
| Therapeutic class | 605 | 567 |
| System organ class | 17 | 17 |
| Sign/symptoms | 985 | 425 |
| Total | 144,654 | 174,317 |
| **Relationships** | | |
| is_effective_for | 5,363 | 5,245 |
| has_therapeutic_class | 5,454 | 4,435 |
| has_adverse_effect_on | 3,168 | 2,598 |
| has_adverse_reaction | 2,233 | 1,342 |
| has_ingredient | 689,826 | 317,062 |
| interacts_with | 3,631 | 3,583 |
| Total | 709,675 | 334,265 |
| **Attributes** | | |
| Company name | — | 163,806 |
| Company address | — | 163,806 |
| Product purpose | — | 65,097 |
| Product risk | — | 63,623 |
| Background | 1,399 | 1,289 |
| Safety | 1,219 | 1,179 |
| Mechanism of action | 258 | 277 |
| Source material | 5,532 | 4,277 |
| Interaction rating | 3,076 | 3,086 |
| Effectiveness rating | 4,307 | 4,623 |
| Total | 15,791 | 471,063 |

## Limitations / caveats
- **Close to a lookup test.** MSKCC is withheld, but NMCD (via iDISK 1) is a parallel professional monograph source
  covering the same well-known supplement facts. Items are single-pair templates matching the KG's relation types, so
  ~95–99% mostly shows that the KG holds the fact and retrieval finds it. This is our inference; the paper reports no
  overlap analysis.
- **Small, resampled test.** "1000" answers per cell are 10 × 100 resamples of 123–309 unique items. There are no
  confidence intervals or significance tests, and the per-type sampling is ambiguous (100 per format vs per format ×
  relation).
- **Unfair comparison arms.** RAG is compared with stand-alone GPT-3.5/GPT-4.0. There is no RAG arm for GPT-3.5 and no
  text-RAG baseline. The abstract compares mismatched tasks and names "GPT-4o".
- **Narrow format, no safety review.** T/F and MCQ only, with no open-ended or user-study evaluation; the authors list
  "real-world, open-ended queries" as future work. No clinician review of harmful answers.
- **Mapping errors remain.** For example, QuickUMLS mapped "Blood pressure-lowering drugs" to the generic UMLS concept
  "Drug" (C0013227).
- **US/Canada products only.** No cultural or traditional-medicine framing.

## Related work to follow
![[Backlog.base#Cited by this paper]]
