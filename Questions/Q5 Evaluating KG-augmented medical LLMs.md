---
question: "How can we measure whether giving an LLM our cultural food–health knowledge graph makes it better at medicine?"
id: Q5
topics: [kg-medical-eval]
updated: 2026-10-07
tags:
  - type/question
  - q/5
---
# Q5: How can we measure whether giving an LLM our cultural food–health knowledge graph makes it better at medicine?

> [!summary] Short answer
> Use a **paired, controlled experiment**: the same models answer the same cases with and without the graph, and a few
> control conditions show that any gain comes from *our* knowledge.
>
> **Case → conclusion datasets ([[Q4 Patient case-conclusion datasets|Q4]]) are the right test material, but only their
> knowledge-dependent part measures the graph.**
> - In general medical benchmarks only ~1–1.5% of items have a diet or nutrient answer (MedQA, MedXpertQA).
> - A whole medical library gives strong models ≤ +3 points, or a loss, on exam questions
>   ([[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]).
>
> **So the evaluation should:**
> 1. Use **food-, diet-, herb- and food–drug-dependent cases**: subsets of regional case sets plus food-as-medicine
>    benchmarks. The full benchmarks serve only as a check that general accuracy does not drop.
> 2. Run **control conditions**: CoT; a generic medical corpus; irrelevant knowledge; deliberately wrong (counterfactual)
>    knowledge; and the gold facts as an upper bound.
> 3. Score **open-ended advice and safety** as well as accuracy: rubric grading, attribution to claims, and missed
>    interaction warnings. LLM judges must be validated against clinicians.
> 4. Use **paired statistics**, reported per country and language.
>
> Expect the largest gains for small models and on items the graph actually covers. Strong models can lose accuracy
> ([[Tonga2026 - LLMs as Cultural Archives|Tonga et al. 2026]], [[Ngo2024 - MedRGB medical RAG robustness benchmark|Ngo et al. 2024]]).

## Detailed answer

### 1. Is a case ↔ conclusion dataset the right idea? Yes, with three conditions
**The idea.** Give the LLM a patient case, compare its conclusion with the reference, with and without the KG. This is
exactly how the source paper and the medical RAG papers measure gains. Tonga et al. used ArabCulture/IndoCulture MCQA;
MIRAGE and MedRGB use MedQA/MedMCQA/PubMedQA. Three conditions make it measure *our graph*:

1. **The items must depend on our knowledge.**
   - In MedQA-US, 11% of test items mention diet or supplements, but only ~1.6% have a diet or nutrient answer
     (keyword counts from the global-cases search; see the [[MedQA]] candidate note).
   - On full exam sets the expected KG effect is therefore ≈ 0. Tag each item as knowledge-heavy vs reasoning-heavy
     ([[Thapa2025 - Disentangling Reasoning and Knowledge in Medical LLMs|Thapa et al. 2025]]), and as covered vs not
     covered by the graph. Report gains on the covered, knowledge-heavy slice.
2. **The items must not come from the graph itself.**
   - MIRAGE's big gains come from PubMedQA*/BioASQ, whose questions were written from abstracts that are in the
     retrieval corpus ([[Xiong2024 - MIRAGE MedRAG benchmark|Xiong et al. 2024]]).
   - KG-RAG's true/false and MCQ items come from knowledge bases like the one retrieved from
     ([[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman et al. 2024]]).
   - Questions generated from our own tables would measure lookup, not medicine. Use independent case sets
     ([[Q4 Patient case-conclusion datasets|Q4]]), or withhold the question source from retrieval, as
     [[Hou2025 - iDISK2.0 supplement RAG|Hou et al. 2025]] withhold MSKCC.
3. **The items must include cultural and safety cases**, not only exam MCQs. Cultural ones: the Kazakh diet profiles in
   [[ISSAI Dietary Recommendation profiles]], Ramadan-fasting diabetes cases (RamadanSafeQA), and TCM syndrome →
   formula cases in [[MTCMB]]. Safety ones: food–drug interaction cases (MedicationQA's food subset, and cases still to
   be built from DDID or PMC-Patients).

### 2. Conditions to compare (same items, same models)
| Condition | What it isolates | Source of the idea |
|---|---|---|
| Base (no KG) | the model's own knowledge | all papers |
| CoT | reasoning without knowledge (it *hurt* cultural MCQA: −3.8 / −4.6 points) | [[Tonga2026 - LLMs as Cultural Archives\|Tonga 2026]] |
| Generic medical RAG (e.g. MedRAG corpora) at a matched token budget | "any medical text" vs "our graph" | [[Xiong2024 - MIRAGE MedRAG benchmark\|Xiong 2024]] |
| Another knowledge base (Mango-style) | our graph vs a competing knowledge source | [[Tonga2026 - LLMs as Cultural Archives\|Tonga 2026]] |
| **Our KG**, in variants: assertions vs paths, English vs native language, with vs without grade tiers, k sweep | which form of the graph works | Tonga 2026; [[Q6 Supplying the KG to an LLM\|Q6]] |
| Irrelevant KG (paths for other dishes, conditions or drugs), with an "insufficient information" option | "the KG helped" vs "any context changed the answer" | [[Ngo2024 - MedRGB medical RAG robustness benchmark\|Ngo 2024]]; [[Sui2024 - Can Knowledge Graphs Make Large Language Models More Trustworthy (OKGQA)\|Sui 2024]] |
| Counterfactual KG (flip one food–drug interaction or effect direction; downgrade a grade) at 10–50% corruption | harm: does wrong KG content override correct knowledge? | Ngo 2024; [[Wu2024b - ClashEval\|Wu 2024b]]; Sui 2024 |
| Oracle (the gold facts given directly) | upper bound; share of the gap the retriever closes | [[CCBench]]-style explicit-norm condition |

**Models and languages.**
- Run several sizes. Gains are largest for small models: Llama-2-13b 0.31 → 0.53 with KG-RAG vs GPT-4 0.68 → 0.74
  ([[Soman2024 - KG-RAG on the SPOKE biomedical KG|Soman 2024]]). Strong models can lose: Gemma2-9B-IT fell from 57.3%
  to 42.9–49.3% on ArabCulture; GPT-4o fell from 89.5 to 83.7 on MedQA.
- Run English and native-language prompts and knowledge. Native-language assertions helped native-language questions
  most (Tonga 2026).

### 3. Test sets, in tiers
See [[Q4 Patient case-conclusion datasets|Q4]] for details and availability.

| Tier | Purpose | Sets |
|---|---|---|
| A. Graph-dependent, independent of the graph | main effect | food-as-medicine and diet cases ([[FAM-Bench]], [[NGQA]], NutriBench); food–drug interaction QA (MedicationQA food subset; a DDID-held-out set built like Hou 2025's); TCM case → syndrome/formula ([[MTCMB]], TCM-BEST4SDT) |
| B. Cultural / regional medicine | does it help across cultures | [[MedArabiQ]], PersianMedQA, [[RuMedBench]], CMB-Clin, IgakuQA, [[ISSAI Dietary Recommendation profiles]] (needs expert gold), RamadanSafeQA |
| C. General medicine | regression check | MedQA, MedXpertQA, MedCaseReasoning (13% of test cases mention diet) |
| D. Open-ended advice | quality and safety of free-text advice | HealthBench diet/herb subset (~8% of conversations), case prompts from tiers A–B |

### 4. Metrics
- **Accuracy.** MCQ accuracy, or exact match against KG ids for structured answers.
- **Retrieval.** Recall@k of the gold KG facts, with answers split by retrieval hit vs miss. Only ~25% of medical RAG
  studies evaluate retrieval separately
  ([[Liu2025 - Improving LLM applications in biomedicine with RAG|Liu et al. 2025]]; Soman 2024 does).
- **Attribution and faithfulness.** Answers cite claim ids, and each statement is checked for support
  ([[Wu2024c - An automated framework for assessing how well LLMs cite relevant medical references (SourceCheckup)|SourceCheckup]]);
  hallucination is scored at the level of individual facts (FActScore, as in Sui 2024).
- **Open-ended quality.** Per-item physician rubrics in the HealthBench style, rewritten for local context:
  off-the-shelf rubrics penalised culturally appropriate Indian advice, including diet advice
  ([[Dey2025 - Beyond the Rubric|Dey et al. 2025]]). Cultural fit is scored with a CCBench-style checklist.
- **Safety.**
  - Missed food–drug or herb–drug warnings, weighted by harm.
  - **Context bias:** how often wrong KG content overrides an answer the model had right (ClashEval).
  - **Detection of planted errors:** only ~7–29% in MedRGB, which makes the robustness test a safety metric, not an extra.
- **Cost.** Tokens per answer: KG-RAG used 3,693 vs 8,006 for Cypher-RAG.

### 5. Who judges
- **LLM judges need validation.**
  - In Tonga 2026, GPT-4o agreed with humans on cultural relevance at r ≈ 0.4 for English stories and ≈ 0.8 for
    native-language ones; on English fluency and coherence agreement was ≈ 0.
  - An LLM-judge panel reached ICC 0.47 with clinicians
    ([[Bedi2025 - Holistic evaluation of LLMs for medical tasks with MedHELM|Bedi et al. 2025]]).
  - Judges detect missing content near chance, AUC 0.49–0.66
    ([[DeLucia2026 - Same Verdict, Different Reasons|DeLucia et al. 2026]]), so a missing interaction warning must be
    checked by a human.
- **Plan:** clinicians or dietitians rate 50–100 items per culture, and agreement with the judge is reported.

### 6. Statistics
- Paired per-item tests between conditions (McNemar or paired bootstrap), with standard errors clustered by country,
  dish or template ([[Miller2024 - Adding Error Bars to Evals|Miller et al. 2024]]).
- Expected precision: the SE is about ±1.3 points at n = 1,273 and about ±4 points for a ~140-item diet subset
  (Xiong 2024 note). ±1-point differences like those in Tonga 2026 need paired tests and enough items.
- Errors we found in the literature:
  - Soman 2024 ran a t-test over bootstrap resamples, which is not valid inference.
  - Hou 2025's abstract compares numbers from different tasks (99% effectiveness vs 62% interaction).

## Comparison table
| What is measured | How | Datasets | Key papers |
|---|---|---|---|
| Does the KG raise accuracy on KG-dependent cases? | paired with/without KG, oracle as upper bound | FAM-Bench, NGQA, MTCMB, DDID-held-out set | Tonga 2026; Soman 2024; Hou 2025 |
| Is it our knowledge, or any context? | irrelevant KG, generic medical RAG at matched tokens | same + MedQA | Ngo 2024; Xiong 2024 |
| Does wrong KG content cause harm? | counterfactual edges; context-bias rate | food–drug and condition items | Ngo 2024; ClashEval; OKGQA |
| Is open-ended advice better and safe? | localised physician rubrics; validated judge | HealthBench subset; case prompts | HealthBench; Dey 2025; MedHELM; DeLucia 2026 |
| Does it work across cultures and languages? | per-country / per-language breakdown; native vs English KG | MedArabiQ, PersianMedQA, RuMedBench, CMB-Clin, ISSAI | Tonga 2026; CCBench; Lertvittayakumjorn 2025 |
| Is the answer grounded in the KG? | citation of claim ids; statement-level support | all open-ended items | SourceCheckup; MedGraphRAG |
| Did general medicine get worse? | full-benchmark regression | MedQA, MedXpertQA | Xiong 2024 |

## Gaps & open questions
1. **No gold food–drug *case* dataset exists.** MedicationQA has ~30 food, drink or supplement items; the iDISK2.0
   questions were not released. Building one from DDID (holding out its source classes) and from PMC-Patients or
   MedCaseReasoning case reports is the obvious first contribution.
2. **No gold diet-advice cases for Central Asia or the Gulf.** The ISSAI profiles have GPT-4 answers, not expert ones;
   CCBench and RamadanSafeQA data are not public. Expert annotation of ~100 cases per region is needed.
3. **Judges for non-English, culture-specific advice** are barely validated. Tonga's native-language r ≈ 0.8 is the only
   positive signal, and it comes from stories, not medicine.
4. **Do evidence grades in the prompt reduce harm?** Untested; see [[Q6 Supplying the KG to an LLM|Q6]].
5. **Contamination.** Public exam sets may be in the training data, so post-cutoff or newly written items help (as
   KGARevion's MedDDx did).

## Papers
![[Papers.base#This question]]
