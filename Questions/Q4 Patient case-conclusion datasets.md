---
question: "Which datasets pair a patient case (real case, exam vignette, synthetic patient or diet scenario) with a reference medical conclusion, and which are culture- or region-specific?"
id: Q4
topics: [kg-medical-eval]
updated: 2026-10-07
tags:
  - type/question
  - q/4
---
# Q4: Which datasets pair a patient case (real case, exam vignette, synthetic patient or diet scenario) with a reference medical conclusion, and which are culture- or region-specific?

> [!summary] Short answer
> There are many case → conclusion datasets, but almost none of them test **food, diet or food–drug knowledge in a
> cultural setting**, which is what our graph adds. So a test suite has to combine:
> - **Diet / food-as-medicine benchmarks** (mostly US): [[FAM-Bench]] (2,500 dish × condition items), [[NGQA]].
> - **Regional real-case sets**: [[RuMedBench]] (6,360 Russian outpatient visits → ICD-10; the closest real-case set
>   for Central Asia), [[MedArabiQ]] (100 real Arabic patient questions → doctor advice), [[CMB (CMB-Clin)]] and
>   ClinicalBench (Chinese), [[PersianMedQA]] (20,785 Iranian vignettes; gated).
> - **Traditional-medicine case sets**: [[MTCMB]] (800 TCM case → syndrome/formula items), TCM-BEST4SDT.
> - **A Central Asian diet case set**: [[ISSAI Dietary Recommendation profiles]] (50 Kazakh profiles in EN/RU/KK). Its
>   answers are GPT-4 outputs, not gold, and they miss most food–drug warnings.
> - **General vignettes** as a regression check: [[MedQA]], [[MedCaseReasoning]], [[HealthBench]].
>
> **Missing everywhere:** a gold food–drug interaction *case* set; Kazakh, Kyrgyz and Uzbek clinical cases; Gulf EHR
> cases; and expert-written diet advice for our priority cuisines.
>
> **Combined table (2026-10-07):** the 8 downloaded sets with a gold conclusion (all above except ISSAI, plus
> [[TCM-BEST4SDT]] and [[MedicationQA]]) are merged into one table `case_id, source, case, conclusion` of 37,631 cases:
> `uv run db/cases.py` → `db/export/cases.parquet`. Counts and rules: [[Export tables]].
>
> **Extended (2026-10-07, later):** the table now has 38,301 rows. It adds the AI-flagged parts (ISSAI, MTCMB
> dialogues, MedArabiQ rewrites) and small PerMedCQA and Rezaei samples, and every case has origin, AI and
> relevance columns.

## Detailed answer

### 1. What counts as "case ↔ conclusion"
Four kinds were searched, all treated as core:
- **real cases:** case reports, EHR notes, consultations;
- **exam vignettes:** licensing-exam questions that start with a patient;
- **synthetic patients:** generated profiles with a ground truth;
- **diet scenarios:** a person or condition plus a food → advice.

The conclusion can be a diagnosis, syndrome, treatment or prescription, a piece of advice or triage, or an MCQ answer.
For our graph only the subset whose conclusion depends on **food, ingredients, herbs or food–drug interactions** measures
the graph's contribution ([[Q5 Evaluating KG-augmented medical LLMs|Q5]]). Each dataset note therefore reports a
`diet_relevance` with keyword counts.

### 2. Processed this session (downloaded and profiled)
- **[[MTCMB]]** (China, TCM; [[Kong2025 - MTCMB multi-task TCM benchmark|Kong et al. 2025]]):
  - 800 case → conclusion items: 200 real EMRs → syndrome + disease or herb set; 100 published case records; 400
    textbook vignettes → syndrome / treatment principle / formula + herbs. Plus 554 vignette MCQs; 7,100 items in all.
  - Diet: 254 items (3.6%) contain a food or diet keyword and 60 contain diet advice, but 47 of those 60 sit in
    LLM-written dialogue input, not in gold answers.
  - Gold herbs match SymMap and HERB for 84–93% of mentions, but our unified DB for only ~20%, because it has few
    Chinese aliases. A fix for the DB, and a cheap way to test the TCM layer.
  - Licence: Apache-2.0 / CC BY 4.0. Caveats: some items come from a commercial question bank, and 297 exam items are
    duplicated.
- **[[FAM-Bench]]** (US recipes, 13 diet-related conditions; [[Mao2026 - FAM-Bench food-as-medicine benchmark|Mao et al. 2026]]):
  - 1,500 dish × condition → recommend / not recommend + justifying ingredients, and 1,000 four-dish rankings.
  - It is the closest task to our dish → ingredient → condition path, and it has its own knowledge-injection baseline
    (+2.0–3.3 points).
  - Its own knowledge base gives no knowledge for 514 of the 1,500 suitability items (IBS, GERD, CKD, heart failure,
    NAFLD), a gap our graph could fill.
  - Labels were proposed by GPT-5.5 and then expert-checked. The anonymous review repo is snapshotted in
    `Data/fam-bench/`.
- **[[RuMedBench]]** (Russia, Tomsk; [[Blinov2022 - RuMedBench|Blinov et al. 2022]]):
  - RuMedTop3: 6,360 real outpatient complaint records → one ICD-10 code (Hit@1 / Hit@3).
  - 3.7% mention food or diet, and 18% have a diet-modifiable gold code. 159 visits mention opisthorchiasis (from river
    fish), a regional food → disease signal.
  - 90 of 105 codes map to our condition table.
  - Russian is the clinical lingua franca of Kazakhstan and Kyrgyzstan.
- **[[MedArabiQ]]** (Arab region; [[AbuDaoud2025 - MedArabiQ Arabic medical benchmark|Abu Daoud et al. 2025]]):
  - 100 real Altibbi patient questions → doctor's answer, in three variants, plus 400 exam and fill-in knowledge items.
  - 18 of the 100 cases involve food or diet, and 3 involve food–drug questions (metformin with meals, cinnamon with
    antihypertensives).
  - **Licence: internal research only, no redistribution**, so no samples are committed.
- **[[ISSAI Dietary Recommendation profiles]]** (Kazakhstan; [[Adilmetova2024 - ChatGPT multilingual clinical nutrition advice|Adilmetova et al. 2024]]):
  - 50 mock clinical and lifestyle profiles in English, Russian and Kazakh, with Kazakh diet histories (beshbarmak,
    kumys, baursak…).
  - The reference answers are GPT-4's 2023 advice. 29 profiles list drugs (warfarin, statins, isoniazid…), but only 4
    of those answers state a food–drug interaction.
  - It is the most direct test of whether our DDID layer changes advice.

**Added later the same day (four more, all downloaded and profiled):**
- **[[TCM-BEST4SDT]]** (China; [[Li2025 - TCM-BEST4SDT syndrome differentiation benchmark|Li et al. 2025]]):
  - 300 expert-annotated TCM cases (150 classical, 50 modern records, 100 vignettes), each with a 19-field gold chain:
    syndrome → cause → pathogenesis → treatment principle → prescription → precautions.
  - **Diet is part of the gold:** 262 of 300 gold "precautions" contain diet advice, and 81 contain food taboos while
    taking the medicine.
  - Herbs match SymMap and HERB at 83–91% but our DB at only 22%, the same alias gap as MTCMB. CC BY 4.0.
- **[[MedicationQA]]** (US; [[BenAbacha2019 - MedicationQA consumer medication QA|Ben Abacha et al. 2019]]):
  - 690 real consumer medication questions → trusted answers. 33 pair a food, drink, alcohol or supplement with a drug,
    e.g. "what if I eat grapefruit on simvastatin".
  - Our DDID edges answer 7 of the 26 distinct food–drug and with-meals questions. There is no official answer scoring.
- **[[NGQA]]** (US, NHANES; [[Zhang2024 - NGQA nutritional graph QA benchmark|Zhang et al. 2024]]):
  - 13,802 user × food items → healthy or not + the deciding nutrient tags + a one-sentence reason.
  - **Caveat:** each item already contains the links that decide the answer, so they must be stripped to test our KG,
    and 136 gold labels contradict the item's own links.
  - Some Puerto Rican, Mexican and Asian dishes by name, but no culture labels.
- **[[MedCaseReasoning]]** (global PMC case reports; [[Wu2025 - MedCaseReasoning diagnostic reasoning from case reports|Wu et al. 2025]]):
  - 14,489 real cases → final diagnosis + clinician reasoning.
  - 1,334 (9.2%) mention diet, food or supplements, and ~343 gold diagnoses are food-related: scurvy, pellagra,
    liquorice intoxication, star fruit intoxication, aconite poisoning, kratom liver injury, milk–alkali syndrome,
    alpha-gal syndrome…
  - **These are the best seed for a real food–drug and herb case set.** In some, the food exposure is cut from the case
    text, so they test whether the model *asks* for a diet history.

### 3. Other datasets by region (candidates in [[Backlog]], verified 2026-10-07)
- **Middle East / Gulf:**
  - [[PersianMedQA]]: 20,785 Iranian board vignettes; 3–10% are answered correctly only in Persian, which the
    authors attribute to Iranian protocols, disease prevalence and translation drift, not to food or religion
    ([[Q7 Cultural cues in evaluation datasets|Q7]]); gated on HF.
  - [[PerMedCQA]]: 68k real Iranian questions with demographics → physician answers.
  - [[MedAraBench]]: 24,883 Arabic MCQs, knowledge items rather than vignettes.
  - [[Arabic Healthcare Dataset (AHD)]]: ~808k Altibbi Q&A, uncleaned.
  - [[AraMed]]: Saudi authors; on request.
  - [[RamadanSafeQA]]: 68 Ramadan-fasting × diabetes safety vignettes (workshop poster); data not located.
- **Central Asia:** no Kazakh, Kyrgyz or Uzbek clinical case set exists. [[KazMMLU]] has only ~300 Russian medicine
  MCQs. Use RuMedBench and the ISSAI profiles.
- **South Asia:**
  - [[BhashaBench-Ayur]]: 14,963 Ayurveda exam items; gated.
  - [[HiMed]]: Hindi Western and traditional medicine.
  - [[MedMCQA]]: Indian exams; 1.4% diet.
- **East Asia:**
  - [[CMB (CMB-Clin)]]: 74 complex real cases + 11,200 exam items.
  - [[ClinicalBench (ClinicalLab)]]: 1,500 real EHRs → full work-up; evaluation-only licence.
  - [[TCM-SD]]: 54,152 real TCM records → syndrome; Tianchi login.
  - [[TCM-BEST4SDT]]: 300 expert cases → syndrome → prescription; CC BY.
  - [[TCM-TBOSD]] (signed pledge) and [[LingLanMiDian]] (labels withheld).
  - [[IgakuQA]] and [[J-ClinicalBench]] (Japan); [[KorMedMCQA]] (Korea).
- **Southeast Asia:** [[VM14K]] (Vietnamese).
- **Multilingual / global:**
  - [[MMedBench]]: 6 languages incl. Russian and Japanese.
  - [[HealthBench]]: 5,000 rubric-graded conversations; ~8% touch diet or herbs.
  - [[Varadarajan2026 - CCBench|CCBench]]: cultural norms in health advice; not released.
  - [[AfriMed-QA]]: a template for a regional benchmark.
  - [[TreeProbe]]: Tibetan medicine with drift-typed distractors.
- **Food–drug and real global cases:**
  - [[MedicationQA]]: ~30 of 690 items involve food, drinks or supplements.
  - [[PMC-Patients]]: 250k case reports, to mine for food–drug cases.
  - [[MedCaseReasoning]]: 14,489 real cases with gold reasoning; 13% mention diet.
  - [[MIMIC-IV-Note]]: discharge diet advice; PhysioNet credentialing.
- **Diet benchmarks:** [[NGQA]] (NHANES users → is this food healthy), [[NutriBench]] (24 countries; meals → macros),
  [[OmniFood-Bench]] (food image + disease → advice).
- **Synthetic or exam regression sets:** [[MedQA]] (11% mention diet, ~1.6% have a diet answer), [[MedXpertQA]],
  [[DDXPlus]], [[AgentClinic]].

## Comparison table
Ranked for our purpose: culture- or region-specific, diet-relevant, open.

| Dataset | Region / language | Case type | Conclusion | Size (cases) | Diet relevance | Access | Use for |
|---|---|---|---|---|---|---|---|
| [[ISSAI Dietary Recommendation profiles]] | Kazakhstan; EN/RU/KK | synthetic, diet | advice (GPT-4, not gold) | 50 × 3 languages | central; 29 on drugs | open (MIT) ✅ | food–drug + Central Asian diet advice (needs expert gold) |
| [[FAM-Bench]] | US recipes; EN | diet | suitability, ranking | 2,500 | central | open (CC BY per README) ✅ | dish × condition, ingredient rationales |
| [[MTCMB]] | China; ZH | real, vignette, synthetic | syndrome, formula, herbs | 800 (+554 MCQ) | subset (3.6%) | open ✅ | TCM layer |
| [[RuMedBench]] | Russia; RU | real | ICD-10 diagnosis | 6,360 | subset (3.7%; 18% diet-modifiable codes) | open ✅ | Central Asian proxy, real cases |
| [[MedArabiQ]] | Arab region; AR | real | doctor advice | 100 | subset (18%) | open, no redistribution ✅ | Arabic advice |
| [[PersianMedQA]] | Iran; FA/EN | vignette | MCQ | 20,785 | not counted | HF-gated | Middle East vignettes |
| [[CMB (CMB-Clin)]] | China; ZH | real, vignette | diagnosis, treatment | 74 + 11,200 | not counted | open | Chinese clinical |
| [[TCM-BEST4SDT]] | China; ZH | real, vignette | syndrome → prescription → precautions | 300 | central (262 diet precautions) | open (CC BY) ✅ | TCM chain incl. diet advice |
| [[NGQA]] | US; EN | diet | food healthy? + nutrients | 13,802 | central | open, no licence stated ✅ | profile × food (strip answer links) |
| [[MedicationQA]] | US; EN | real | trusted answer | 690 rows | 33 food/drink/supplement–drug | open (CC BY) ✅ | food–drug seed |
| [[MedCaseReasoning]] | global; EN | real | diagnosis + reasoning | 14,489 | 9.2% mention; ~343 food-related diagnoses | open (MIT / CC BY) ✅ | real food–drug and herb cases |
| [[HealthBench]] | global; multilingual | synthetic | rubric | 5,000 | ~8% | open (MIT) | open-ended grading |
| [[MedQA]] | US/CN/TW | vignette | MCQ | 12,723 US | ~1.6% diet answers | open | regression check |

## Gaps & open questions
1. **No gold food–drug interaction case set.** Build one by:
   - writing cases from DDID rows, holding out their source class from retrieval (as in
     [[Hou2025 - iDISK2.0 supplement RAG|Hou et al. 2025]]);
   - mining [[PMC-Patients]] and [[MedCaseReasoning]] for grapefruit, St John's wort, tyramine, warfarin–vitamin K and
     herb-induced liver injury cases;
   - adding expert gold to the 29 drug-taking ISSAI profiles.
2. **No clinical cases in Kazakh, Kyrgyz or Uzbek**, and no open Gulf (Saudi or Emirati) EHR or SMLE vignette set.
   Russian (RuMedBench) and the ISSAI profiles are the only proxies; a small expert-written set of ~100 cases per
   region would fill this.
3. **Diet benchmarks are US-centric** (NHANES, US recipe sites). None uses dishes from our priority cuisines, although
   our dish table could supply them: FAM-Bench's format applied to Saudi, Kyrgyz or Indian dishes.
4. **Gated and on-request data:** PersianMedQA, BhashaBench-Ayur and AfriMed-QA need an HF login and accepted terms;
   MIMIC-IV-Note needs PhysioNet credentialing; TCM-SD needs Tianchi; TCM-TBOSD needs a signed pledge; AraMed,
   CCBench and RamadanSafeQA need the authors. See [[Access requests]].
5. **Licences:** MedArabiQ (no redistribution) and ClinicalBench (evaluation only) can be used locally only; never
   commit their samples.

## Papers
![[Papers.base#This question]]
