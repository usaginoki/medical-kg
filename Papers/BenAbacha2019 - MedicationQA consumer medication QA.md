---
title: "Bridging the Gap Between Consumers' Medication Questions and Trusted Answers"
citekey: "BenAbacha2019"
authors: ["Asma Ben Abacha", "Yassine Mrabet", "Mark Sharp", "Travis R. Goodwin", "Sonya E. Shooshan", "Dina Demner-Fushman"]
year: 2019
published: 2019-08-22
venue: "MEDINFO 2019 (Lyon), Stud Health Technol Inform 264, pp. 25–29"
peer_reviewed: true
url: "https://ebooks.iospress.nl/doi/10.3233/SHTI190176"
arxiv: ""
doi: "10.3233/SHTI190176"
pdf: ""
pdf_url: ""
datasets: ["[[MedicationQA]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases]
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - kind/case
  - case/real
---
# Bridging the Gap Between Consumers' Medication Questions and Trusted Answers

> [!abstract] TL;DR
> The US National Library of Medicine (Lister Hill Center) built **MedicationQA**: 674 real consumer questions about medicines, taken from MedlinePlus. Each question is annotated with its focus drug and question type, and paired with a manually retrieved, trusted reference answer. The paper reports the annotation process, baselines for focus recognition and question-type classification, and a small qualitative answer-retrieval test. It was read from the IOS Press open-access PDF (CC BY-NC 4.0); there is no local PDF and no docling extraction.

## What was built
- **Dataset(s):** [[MedicationQA]]
- **Sources & construction:**
  - **Question selection:** anonymised consumer questions sent to MedlinePlus were run through MetaMapLite. Questions were kept if they contained UMLS medication types: antibiotic, clinical drug, neuroreactive substance, pharmacologic substance, steroid or vitamin. They were then hand-filtered to those that were "understandable and potentially answerable" and had a drug name as focus.
  - **Annotation:** each question got a focus (drug name) and a question type.
  - **Answer search:** annotators searched for a reference answer in a fixed order: (1) MedlinePlus and DailyMed, (2) other NIH or US government sites, (3) other trustworthy sites such as Mayo Clinic, (4) Google. They recorded the answer passage, URL and section title. Answers had to be "correct" and "complete".
  - **Validation:** four annotators did the work. A medical doctor and a QA expert reconciled the question types and validated the answers.
- **Size & coverage:** 674 QA pairs (the released file has 690 rows) and 25 question types.
  - Answer sources: DailyMed 290, MedlinePlus 128, other sites 256.
  - Questions average 7.16 tokens; answers average 69.06 tokens and 3.23 sentences.
  - English, United States.
- **Evaluation / applications:**
  - Focus recognition: Bi-LSTM-CRF with UMLS BIOES and GloVe embeddings, 80/10/10 split.
  - Question type: CNN over 14 merged types.
  - Answer retrieval: CHiQA on 20 random questions, judged by hand.

## Key findings
1. **Focus recognition** F1: 74.07 (±2.1) for an exact span and 90.37 (±3.4) for a partial span. **Question type** accuracy: 75.7% over 5 runs.
2. **Answer retrieval is hard.** CHiQA put a correct answer in its top 4 for 35% of the questions, only related answers for 35%, and irrelevant answers for 30%. The authors conclude that "classical QA systems may not be the best fit for medication questions".
3. **Questions are often underspecified or conditional.** Many lack patient context ("what would a normal dose be for valacyclovir?"). Many answers depend on the manufacturer (phenytoin has four possible colours) or must be assembled from several sources. Interaction questions needed external resources (eHealthMe), and one oxygen + fluticasone question took an expert an hour on PubMed.
4. The authors call for more data on "drug interactions and usage guidelines" and for dialogue-based answers to conditional questions.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
MedicationQA is a **real**, US, English set of consumer question → trusted answer pairs, where the answer is advice or a safety warning. It is not a clinical vignette, but it is the only open QA set with consumer-written questions about **food, drinks and supplements with drugs**.
- **The subset (our count):** 20 rows name a food, drink or supplement together with a drug, e.g. grapefruit + simvastatin, warfarin + cabbage/spices, levothyroxine + walnut/calcium, levodopa + alcohol. Another 13 rows deal with meal timing or carry a food fact only in the gold answer.
- **KG coverage:** our KG ([[DDID]] edges) covers 7 of the 26 distinct pair or timing questions.
- **Use for us:** a small, real test of whether injecting food–drug knowledge improves safety-relevant answers. It also exposes KG gaps: minerals and vitamins as interactants, alcohol, and meal-timing rules.
- **Limits:** there is no scoring protocol for answers, and the population is US-only.

See [[Q4 Patient case-conclusion datasets]]

## Key figures & tables
Not extracted (no local PDF). Table 1 lists the question types with counts and examples. Table 3 gives the focus-recognition results. Table 4 shows example questions and answers. Figure 4 shows the answer sources.

## Limitations / caveats
- There is no patient context, and the gold is one extractive passage per question, sometimes from non-authoritative sites.
- The answer evaluation is qualitative and covers only 20 questions.
- The data have been public since 2019 and are part of MultiMedQA ([[Singhal2022 - Large Language Models Encode Clinical Knowledge]]), so contamination is likely.

## Related work to follow
![[Backlog.base#Cited by this paper]]
