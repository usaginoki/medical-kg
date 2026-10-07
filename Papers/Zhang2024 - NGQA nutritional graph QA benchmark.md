---
title: "NGQA: A Nutritional Graph Question Answering Benchmark for Personalized Health-aware Nutritional Reasoning"
citekey: "Zhang2024"
authors: ["Zheyuan Zhang", "Yiyang Li", "Nhi Ha Lan Le", "Zehong Wang", "Tianyi Ma", "Vincent Galassi", "Keerthiram Murugesan", "Nuno Moniz", "Werner Geyer", "Nitesh V. Chawla", "Chuxu Zhang", "Yanfang Ye"]
year: 2024
published: 2024-12-20
venue: "ACL 2025 (Long Papers), pp. 5934–5966"
peer_reviewed: true
url: "https://arxiv.org/abs/2412.15547"
arxiv: "2412.15547"
doi: "10.18653/v1/2025.acl-long.296"
pdf: ""
pdf_url: "https://aclanthology.org/2025.acl-long.296.pdf"
datasets: ["[[NGQA]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases, search/evaluation]
cites:
  - "[[FoodKG]]"
  - "[[Sun2023 - Think-on-Graph]]"
  - "[[Yasunaga2021 - QA-GNN]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - kind/case
  - case/diet
---
# NGQA: A Nutritional Graph Question Answering Benchmark for Personalized Health-aware Nutritional Reasoning

> [!abstract] TL;DR
> Notre Dame, IBM Research, UConn and Brandeis built **NGQA**, which they call "the first graph question answering dataset designed for personalized nutritional health reasoning".
> - **Data:** NHANES 2003–2020 respondents (health statuses, special diets, dietary habits) are paired with FNDDS foods (ingredients, nutrient tags).
> - **Tasks:** is this food healthy for this user, which nutrient tags decide it, and a short explanation. Each is asked at three question levels.
> - **Baselines:** five graph-RAG baselines (Plain, KAPING, CoT-Zero, CoT-BAG, ToG) on GPT-4o-mini and Llama-3.1-70B (GPT-3.5 in the appendix).
> - Read from the ACL Anthology PDF text (`pdftotext`); there is no local PDF and no docling extraction.

## What was built
- **Dataset(s):** [[NGQA]]
- **Sources & construction:**
  - **Users:** NHANES (CDC) laboratory, examination and questionnaire data. Four health statuses are defined by thresholds: obesity, hypertension (mean SBP ≥ 140 or DBP ≥ 90), diabetes (glucose ≥ 7.0 mmol/L and HbA1c ≥ 6.5%), and opioid misuse (illicit use within a year, or > 90 days of prescription opioids). Nine self-reported special diets and "54 distinct dietary habits" are added; the habits are the top or bottom 10% on diet-behaviour items.
  - **Foods:** FNDDS / WWEIA foods, restricted to "mixed dishes" plus bakery and dessert categories and deduplicated by keyword, giving 849 foods.
  - **Nutrient tags:** thresholds per 100 g from the EU Nutrition & Health Claims Regulation and the Codex Alimentarius (e.g. "low sodium" ≤ 0.12 g / 100 g).
  - **Links:** a status → needed-nutrient map (Table 11) creates `match` / `contradict` edges between user statuses and food tags.
  - **Checks:** "LLMs perform an initial sanity check", then three annotators with domain expertise cross-validate.
- **Size & coverage:** 13,802 records: Sparse 8,490 (avg 25.8 nodes), Standard 3,622 (28.2), Complex 1,690 (30.9). There are 5,644 users and 849 foods; the population is US only.
- **Evaluation / applications:**
  - Three task forms: binary (-B, accuracy/P/R/F1), multi-label tags (-ML, weighted metrics) and text generation (-TG, ROUGE/BLEU/BERTScore).
  - Gold: Yes iff #match > #contradict.
  - Also reported: efficiency, ToG retrieval quality, and the ratio of factual to contextual hallucinations.

## Key findings
1. **Binary task:** models are conservative, with low recall. GPT-4o-mini, sparse / standard / complex accuracy:
   - Plain 0.597 / 0.576 / 0.660
   - CoT-Zero 0.660 / 0.657 / 0.663
   - ToG best at 0.773 / 0.863 / 0.747
   - Llama-3.1-70B with ToG: 0.848 / 0.865 / 0.722.
2. **More links help.** Recall rises from Sparse to Standard for every baseline ("richer external knowledge provides LLMs with greater context"). ToG's pruning raises the signal-to-noise ratio (SNR) and gives the largest gains.
3. **ML and TG are hardest on Sparse and easiest on Complex.** The authors explain this by SNR: complex items have the most relevant tags (tag SNR 76.3 vs 19.3).
4. **Errors are mostly contextual.** Contextual hallucinations (being misled by irrelevant retrieved nodes) dominate factual ones: 0.960 vs 0.040 for Llama-3.1-70B, 0.845 vs 0.155 for GPT-4o-mini.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
A large **diet-scenario** case set: a real NHANES profile × food → healthy yes/no + the deciding nutrients. Its structure (food → ingredients → nutrients ↔ user conditions) maps directly onto our dish → ingredient → compound → condition KG.
- **Coverage:** we resolve 857 of its 954 ingredient names to KG ingredients. Its nutrient tags and its 4 conditions map to KG compounds and MeSH conditions.
- **Not culture-specific:** US-only, though ~170 foods are Puerto Rican, Mexican / Central American or Asian dishes.
- **Two cautions** (from our check of the release):
  1. Each item's graph already contains the `match` / `contradict` edges that decide the answer, so it must be stripped to test knowledge.
  2. Some special-diet habit labels look misassigned.
- **Also relevant to Q5 (not tagged here):** the paper benchmarks graph-RAG baselines against a plain pipeline.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted (no local PDF):
- Table 1: statistics by question level.
- Table 2: SNR.
- Tables 3–4: results for the five baselines × three tasks.
- Tables 8–11: nutrient thresholds, health-indicator thresholds, and the tag ↔ indicator maps.
- Tables 13–14: user statuses and diets.

## Limitations / caveats
- **Authors' own list:** few conditions; no food insecurity or socioeconomic factors; complex items are reduced to counting match vs contradict edges; and a single task family.
- **Rule-derived gold** rather than clinical judgement. Habits never affect the label.
- **Licence:** no data licence is stated (data on Google Drive, code on GitHub).

## Related work to follow
![[Backlog.base#Cited by this paper]]
