---
title: "Session 2026-10-07: kg-medical-eval - literature and dataset survey"
date: 2026-10-07
session: literature-review
topics: [kg-medical-eval]
questions: [Q4, Q5, Q6]
tags:
  - type/session
  - q/4
  - q/5
  - q/6
---
# Session 2026-10-07: kg-medical-eval (literature and dataset survey)

> [!question] Questions addressed in this session
> - [[Q4 Patient case-conclusion datasets|Q4]]: Which datasets pair a patient case with a reference medical conclusion,
>   and which are culture- or region-specific?
> - [[Q5 Evaluating KG-augmented medical LLMs|Q5]]: How can we measure whether giving an LLM our cultural food–health
>   knowledge graph makes it better at medicine?
> - [[Q6 Supplying the KG to an LLM|Q6]]: How should the knowledge graph be supplied to an LLM: in context, vector
>   retrieval, graph retrieval, tools/MCP, or fine-tuning?

**Research question:** we now have a cultural food–health knowledge graph ([[Unified database]], [[Export tables]]).
How do we give it to an LLM, and how do we show the LLM got better at medicine? The idea comes from
[[Tonga2026 - LLMs as Cultural Archives|Tonga et al. 2026]] (EACL 2026), which feeds an LLM-extracted cultural
commonsense KG to small LLMs.

**Corpus / scope:**
- **Search:** 4 parallel strands, run on 2026-10-07:
  - regional case datasets;
  - global and diet case datasets;
  - evaluation of knowledge-augmented LLMs;
  - ways to supply a KG.
- **Candidates:** the strands produced **94 candidates**, and 19 more came from the processed papers' reference lists,
  all in [[Backlog]]. All 81 arXiv ids and every DOI and ACL id were checked against arXiv, Crossref, DataCite or the
  ACL Anthology. The one exception is RamadanSafeQA: its title is confirmed, its authors and data are not.
- **Processed:** depth was light (agreed with the user).
  - **5 datasets** downloaded and profiled, each with a light paper note: [[MTCMB]], [[FAM-Bench]], [[RuMedBench]],
    [[MedArabiQ]], [[ISSAI Dietary Recommendation profiles]]. Four more were added later the same day at the
    user's request: [[TCM-BEST4SDT]], [[MedicationQA]], [[NGQA]], [[MedCaseReasoning]].
  - **Cases table:** the 8 downloaded sets with a gold conclusion (all except ISSAI) were merged into one table
    `case_id, source, case, conclusion` of 37,631 cases (`uv run db/cases.py` → `db/export/cases.parquet`; counts in
    [[Export tables]]). `db/fetch.py` now downloads all 9 case datasets.
  - **5 full paper notes:** [[Tonga2026 - LLMs as Cultural Archives|Tonga 2026]],
    [[Xiong2024 - MIRAGE MedRAG benchmark|Xiong 2024]], [[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo 2024]],
    [[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman 2024]], [[Hou2025 - iDISK2.0 supplement RAG|Hou 2025]].
- **Vault changes:**
  - new topic `kg-medical-eval` with facet tags `case/`, `inject/`, `eval/` (`_tools/README.md`);
  - case datasets as `kind: [case]` with `case_type`, `conclusion_type`, `languages`, `n_cases`, `diet_relevance`
    (template, `check_vault.py`);
  - a "Patient case datasets" section in the country and region notes (`_tools/build_geo.py`);
  - access needs added to [[Access requests]].

> [!important] Main takeaways
> 1. **A case ↔ conclusion dataset is the right test, but only its food-dependent part measures our graph.** Diet-answer
>    items are ~1–1.5% of MedQA and MedXpertQA. FAM-Bench, NGQA, MTCMB, the ISSAI profiles and food–drug cases carry
>    the signal; general benchmarks only check for regressions.
> 2. **Knowledge augmentation helps weak models and can hurt strong ones.**
>    - Gemma2-9B-IT drops on ArabCulture from 57.3% to 42.9–49.3% (Tonga 2026).
>    - GPT-4 loses 1.2–3.2 points on exam sets with a medical library (Xiong 2024).
>    - GPT-4o falls on MedQA from 89.5 to 83.7 with 5 retrieved documents (Ngo 2024).
>
>    The evaluation must include strong models and controls (irrelevant and counterfactual KG), and report harm.
> 3. **For a structured KG, retrieval of the right rows beats dumping or fine-tuning.** KG-RAG retrieves correctly in
>    97% of cases vs 75% for LLM-written Cypher, using 53.9% fewer tokens (Soman 2024). iDISK2.0's KG lifted
>    supplement–drug interaction MCQ from 52% to 95% (Hou 2025). Typed tools, e.g. an MCP server over DuckDB, are the
>    natural route for lookups.
> 4. **The clearest open gap is food–drug safety in culturally specific advice.** In the ISSAI Kazakh profiles, 29 of
>    50 patients take drugs, but GPT-4's diet advice states a food–drug interaction in only 4. No gold food–drug *case*
>    dataset exists, and building one from DDID and case reports is a natural first contribution.
> 5. **No clinical case data exists in Kazakh, Kyrgyz or Uzbek, and none from Gulf EHRs.** The proxies are Russian
>    (RuMedBench, real Tomsk outpatients → ICD-10) and the ISSAI profiles (EN/RU/KK), and diet benchmarks are US-centric.

## Q4: Patient case ↔ conclusion datasets → [[Q4 Patient case-conclusion datasets]]
- **Processed:**
  - MTCMB: 800 TCM case → syndrome/formula items. Its gold herbs match SymMap/HERB at 84–93% but our DB at only ~20%,
    so Chinese aliases are missing.
  - FAM-Bench: 2,500 dish × condition items; its own knowledge base covers none of 514 items, a gap our graph could fill.
  - RuMedBench: 6,360 real Russian outpatient visits; 90 of 105 ICD codes map to our conditions.
  - MedArabiQ: 100 real Arabic patient questions → doctor advice; no-redistribution licence, samples kept out of git.
  - ISSAI: 50 Kazakh profiles in 3 languages; GPT-4 answers, not gold.
- Strongest unprocessed candidates: PersianMedQA (gated), CMB-Clin, TCM-BEST4SDT, NGQA, MedicationQA, MedCaseReasoning,
  HealthBench.

## Q5: Evaluating a KG-augmented LLM → [[Q5 Evaluating KG-augmented medical LLMs]]
- **Design:** paired with/without-KG on the same items; controls are CoT, generic medical RAG at matched tokens,
  another KB, irrelevant KG, counterfactual KG, and an oracle; several model sizes; English vs native language.
- **Metrics:** accuracy on KG-covered, knowledge-heavy slices; retrieval recall; attribution; localised rubric grading;
  safety (missed interaction warnings, context bias); tokens.
- **Judges:** LLM judges validated against clinicians, with expected agreement ICC ≈ 0.47 and omission detection near
  chance. Statistics are paired per item, clustered by country.

## Q6: Supplying the KG → [[Q6 Supplying the KG to an LLM]]
- **Route by question type:** typed tools/MCP for lookups; entity-linked path retrieval with evidence-grade tiers for
  multi-hop; hybrid vector RAG for fuzzy cultural questions; no KG for general medicine.
- **Later:** Microsoft GraphRAG and fine-tuning as later arms only.

## Most important papers to read first
| Why | Paper |
|---|---|
| The project's own baseline and its limits (small, mixed MCQA gains; CoT hurts) | [[Tonga2026 - LLMs as Cultural Archives]] |
| Closest architecture to our DuckDB graph; text-to-query brittleness | [[Soman2024 - KG-RAG on the SPOKE biomedical KG]] |
| Template for food–drug interaction tests (52% → 95%) | [[Hou2025 - iDISK2.0 supplement RAG]] |
| Controls: irrelevant and counterfactual knowledge, abstention | [[Ngo2024 - MedRGB medical RAG robustness benchmark]] |
| Baseline harness and expected effect sizes for medical RAG | [[Xiong2024 - MIRAGE MedRAG benchmark]] |

## Open gaps / next steps
1. **Build a food–drug case set:** DDID rows with their source class held out of retrieval, PMC-Patients and
   MedCaseReasoning case reports, and expert gold for the 29 drug-taking ISSAI profiles.
2. **Link the cases table to the graph:** ICD-10 codes → conditions, dish and ingredient names → `ingredient_id`, so
   graph-covered cases can be scored separately.
3. **First experiment:** replicate Tonga-style SBERT top-k vs entity-linked path retrieval vs typed tools on FAM-Bench +
   MTCMB + the ISSAI profiles + a MedQA regression set, with small and strong models, in English and native languages.
4. **Fix the KG's Chinese alias coverage:** MTCMB herbs match only ~20% of our ingredients. HMDB can be filled from the
   Zenodo copy listed in [[Access requests]].
5. **Expert annotation:** ~100 diet-advice cases per priority region (Central Asia, Gulf), since none exist.
6. **Access:** HF login for PersianMedQA, BhashaBench-Ayur and AfriMed-QA; authors for CCBench, RamadanSafeQA and AraMed
   (see [[Access requests]]).

## Papers in this topic
![[Papers.base#This topic]]

## Backlog for this topic
![[Backlog.base#This topic]]
