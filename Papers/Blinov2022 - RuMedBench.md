---
title: "RuMedBench: A Russian Medical Language Understanding Benchmark"
citekey: "Blinov2022"
authors: ["Pavel Blinov", "Arina Reshetnikova", "Aleksandr Nesterov", "Galina Zubkova", "Vladimir Kokh"]
year: 2022
published: 2022-01-17
venue: "AIME 2022 (Artificial Intelligence in Medicine, Halifax), LNCS pp. 383–392"
peer_reviewed: true
url: "https://arxiv.org/abs/2201.06499"
arxiv: "2201.06499"
doi: "10.1007/978-3-031-09342-5_38"
pdf: ""
pdf_url: "https://arxiv.org/pdf/2201.06499"
datasets: ["[[RuMedBench]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - kind/case
  - case/real
---
# RuMedBench: A Russian Medical Language Understanding Benchmark

> [!abstract] TL;DR
> Sber AI Lab (Moscow) built the first open Russian medical NLP benchmark, with five text tasks over four text types. Two tasks are built on **real outpatient notes** from the Siberian State Medical University hospital:
> - **RuMedTop3:** complaints → ICD-10 code.
> - **RuMedSymptomRec:** incomplete complaints → the missing symptom.
>
> The other three are yes/no medical QA (RuMedDaNet), a translated MedNLI (RuMedNLI) and drug-review NER (RuMedNER). The paper gives baselines from a naive model to BERT plus a human baseline: models beat clinicians on the case → diagnosis tasks, but humans keep a large lead on knowledge QA and NLI. Read from the arXiv v2 PDF text (not extracted with docling; no local PDF).

## What was built
- **Dataset(s):** [[RuMedBench]]
- **Sources & construction:**
  - **RuMedTop3 / RuMedSymptomRec** come from RuMedPrime: 7,625 anonymised visit records (Zenodo 10.5281/zenodo.5765873).
    - Only the `symptoms` field and the ICD-10 code are used.
    - Codes are cut to the "second level of the ICD-10 classification code hierarchy", and codes with fewer than 10 records are dropped. That leaves "6,360 visits … with 105 target codes".
    - For SymptomRec, an internal tool extracts UMLS symptom concepts. One random symptom is removed from the text and becomes the label (141 symptom codes).
  - **RuMedDaNet:** assessors wrote yes/no questions for medical text excerpts of up to 300 words, balanced positive/negative.
  - **RuMedNLI:** MedNLI was translated by two MT services, then corrected by a human (units, drug names, cultural phenomena). It is released through PhysioNet (MIMIC-III derived).
  - **RuMedNER:** RuDReC drug reviews, 6 entity types.
- **Size & coverage:** Top3 4,690 / 848 / 822 · SymptomRec 2,470 / 415 / 415 · DaNet 1,052 / 256 / 256 · NLI 11,232 / 1,395 / 1,422 · NER 3,440 / 676 / 693 (train/dev/test). Russian only.
- **Evaluation / applications:**
  - Metrics: accuracy for every task; Hit@3 for Top3 and SymptomRec; F1 for NER. The overall score is the mean over tasks.
  - Baselines: naive, tf-idf + logistic regression (CRF for NER), BiLSTM, RuBERT, RuPoolBERT, human.
  - Clinicians solved Top3, SymptomRec and NLI; a non-medical assessor solved DaNet and NER.

## Key findings
1. On RuMedTop3 the **linear tf-idf model is best (Hit@1 49.76 / Hit@3 72.75)**, ahead of RuPoolBERT (47.45 / 70.44). The authors attribute this to the "mapping between char N-grams and a set of target codes" being "quite trivial" statistically.
2. **Clinicians score only 25.06 / 48.54 on RuMedTop3** and 7.23 / 12.53 on SymptomRec. The assessors blamed "insufficient and noisy information provided in the Symptom field": sex, age, examination and anamnesis are missing. The authors conclude that future reformulations "should encompass more patient-related information, not only symptoms".
3. Humans lead by large margins on knowledge and reasoning tasks: RuMedDaNet 93.36 vs best model 71.48; RuMedNLI 83.26 vs 77.64.
4. Overall scores: RuPoolBERT 67.20, human 61.89 (paper Table 3). The later GitHub README adds RuBioRoBERTa 71.54.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
RuMedTop3 is a **real, region-specific** case → diagnosis set: Russian outpatient notes from Tomsk, with ICD-10 gold codes and a clear Hit@1/Hit@3 metric.
- **Why it suits us:** Russian is the clinical language of much of Central Asia, so it is the most realistic open test of whether a food/compound KG helps diagnosis in that setting.
- **Diet content:** about 18% of visits have a diet-modifiable gold code (gastritis, obesity, T2DM, GERD, cholecystitis, goitre), but only 3.7% of inputs mention food.
- **Build richer cases:** the paper's own finding that the symptoms field is too thin argues for joining the source corpus's **anamnesis**. It carries diet exposures such as raw river fish and opisthorchiasis, and current drugs.
- **Other tasks:** RuMedTest (MCQ, closed answers) and RuMedNLI are less useful here.

See [[Q4 Patient case-conclusion datasets]]

## Limitations / caveats
- Single-site data (one Tomsk outpatient unit). One gold code per visit, with no adjudication. The test labels are public, so there is a contamination risk.
- The paper evaluates encoder models only. LLM results exist only on the later leaderboard (medbench.ru), and RuMedTop3 is not on it.
- RuMedNLI derives from MIMIC-III and is under PhysioNet credentialed access.

## Related work to follow
![[Backlog.base#Cited by this paper]]
