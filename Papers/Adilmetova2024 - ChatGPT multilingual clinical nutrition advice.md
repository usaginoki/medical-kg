---
title: "Evaluating ChatGPT's Multilingual Performance in Clinical Nutrition Advice Using Synthetic Medical Text: Insights from Central Asia"
citekey: "Adilmetova2024"
authors: ["Gulnoza Adilmetova", "Ruslan Nassyrov", "Aizhan Meyerbekova", "Aknur Karabay", "Huseyin Atakan Varol", "Mei-Yen Chan"]
year: 2024
published: 2024-12-26
venue: "The Journal of Nutrition 155(3):729–735 (March 2025; online Dec 2024)"
peer_reviewed: true
url: "https://doi.org/10.1016/j.tjnut.2024.12.018"
arxiv: ""
doi: "10.1016/j.tjnut.2024.12.018"
pdf: ""
pdf_url: ""
datasets: ["[[ISSAI Dietary Recommendation profiles]]"]
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
cites:
  - "[[Yang2024a - ChatDiet]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - kind/case
  - case/synthetic
  - case/diet
  - region/central-asia
---
# Evaluating ChatGPT's Multilingual Performance in Clinical Nutrition Advice Using Synthetic Medical Text: Insights from Central Asia

> [!abstract] TL;DR
> - **Who:** Nazarbayev University (School of Medicine + ISSAI, Astana); PubMed 39732434.
> - **What:** the team wrote **50 mock patient profiles** for Kazakhstan in English, Russian and Kazakh and asked **ChatGPT-4** (May–August 2023) for dietary recommendations and a one-day Central Asian meal plan.
> - **Scoring:** answers were rated for personalisation, consistency with guidelines and practicality on a 5-point Likert scale.
> - **Result:** English and Russian were moderate (≈3.2–3.5); Kazakh outputs were "unsuitable for evaluation" (≈1.0–1.1).
>
> The full text was not available (ScienceDirect returned 403; the article is CC BY 4.0 but not in PMC). This note uses the abstract, the dataset README, `gpt_response_extraction.py` and the data itself.

## What was built
- **Dataset(s):** [[ISSAI Dietary Recommendation profiles]]
- **Sources & construction:**
  - The profiles were written by the team ("synthetic medical text"; README: "easy, medium, and complex cases and various diseases").
  - **Pipelines:** the Russian and Kazakh profiles were sent both directly and after Google machine translation to English, with the answer back-translated. These are the `_tr` files.
  - **Prompts:** "Provide dietary recommendations for this patient profile" and the follow-up "Give a specific diet plan for the day based on the patient profile using Central Asian food" (`gpt-4`, 800 max tokens).
- **Size & coverage:** 50 profiles × 3 languages. All patients live in Kazakhstan; ethnicities are mixed (Kazakh, Russian, Uzbek, Korean-, Chinese-, German-Kazakh…). 10 profiles are lifestyle/sport cases and 40 clinical, from anaemia and TB to IBD and AKI.
- **Evaluation / applications:** Likert ratings (1–5) on 3 criteria; Kruskal–Wallis test across languages with post hoc Dunn's test.

## Key findings
1. Scores (mean ± SD):

   | language | personalisation | consistency | practicality |
   |---|---|---|---|
   | English | 3.32 ± 0.46 | 3.48 ± 0.43 | 3.25 ± 0.41 |
   | Russian | 3.18 ± 0.38 | 3.38 ± 0.39 | 3.37 ± 0.38 |
   | Kazakh | 1.01 ± 0.06 | 1.09 ± 0.18 | 1.07 ± 0.15 |

2. Performance differed significantly across languages (Kruskal–Wallis P < 0.001). English and Russian each differed significantly from Kazakh (Dunn's test).
3. The authors conclude that GPT-4's ability "to produce sensible outputs is limited by the lack of training data in non-English languages". They call for "a customized large language model … to take into account specific local diets and practices".
4. **Our own check of the released answers:** only 4 of the 29 EN answers for profiles with current medications state a food/alcohol–drug interaction (warfarin–vitamin K, alcohol–TB drugs, alcohol–antivirals, potassium–losartan). Statins get no grapefruit warning, and kumys is recommended to a patient on isoniazid.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
This is the **only diet-scenario case set built on Central Asian patients and cuisine**, in all three local languages.
- **What it offers:** profile → diet advice + meal plan. Diet histories name Kazakh dishes (baursak, beshbarmak, plov, kazy, kumys), and 29/50 profiles carry drug lists.
- **That makes it a natural test of:**
  - whether a KG of Central Asian dishes → nutrients → conditions, plus food–drug interactions, improves advice;
  - whether the model can handle Kazakh.
- **Limits:**
  - The stored "conclusions" are GPT-4 answers rated only moderate, not expert gold, and the ratings were not released.
  - Use the profiles as inputs with a rubric (the paper's three criteria + food–drug safety) instead of answer matching.
  - 50 cases is small.

See [[Q4 Patient case-conclusion datasets]]

## Limitations / caveats
- Full text not read (paywall bot block). Who rated the answers, and how many raters, is not in the abstract.
- Mock profiles; one model (GPT-4, 2023); answers from 2023 only.
- The back-translation pipeline adds machine-translation noise.

## Related work to follow
![[Backlog.base#Cited by this paper]]
