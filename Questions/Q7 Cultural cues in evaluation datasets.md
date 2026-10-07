---
question: "Which evaluation-relevant medical datasets contain cultural cues: the patient's country or place, race or ethnicity, culture-specific foods, habits or religious practices, or traditional medicine?"
id: Q7
topics: [kg-medical-eval]
updated: 2026-10-07
tags:
  - type/question
  - q/7
---
# Q7: Which evaluation-relevant medical datasets contain cultural cues: the patient's country or place, race or ethnicity, culture-specific foods, habits or religious practices, or traditional medicine?

> [!summary] Short answer
> Few, and the ones that do are small, synthetic or not released.
> - **In our own 37,631 cases** ([[Q4 Patient case-conclusion datasets|Q4]]) a keyword count finds a cue in about 21% of
>   cases, but almost all of it is one of three things: a nationality or race word in [[MedCaseReasoning]] case
>   reports (10.3% place, 8.9% ethnicity), a cuisine name on the *dish* in [[NGQA]] and [[FAM-Bench]], or traditional
>   medicine by construction in [[MTCMB]] and [[TCM-BEST4SDT]]. [[RuMedBench]], [[MedArabiQ]] and [[MedicationQA]] are
>   regional only by language: under 3% of their cases state any cue.
> - **Datasets built around cultural cues** exist but are small: the counterfactual MedQA set of
>   [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA|Rezaei & Shakeri 2026]] (1,650 items, open),
>   [[Varadarajan2026 - CCBench|CCBench]] (3,120 dialogues, not released), [[RamadanSafeQA]] (68, not located),
>   [[Sayeed2025 - Tibbe-AG Islamic medicine validation|Tibbe-AG]] (30),
>   [[Nimo2025 - Africa Health Check|Africa Health Check]] (130+ herb pairs, not released) and
>   [[Hamna2025 - Samiksha community-centred health benchmark|Samiksha]] (1,590 Indian queries, no gold).
> - **No dataset found has both a culturally *decisive* cue and a clinician gold answer at scale.** The open set with a
>   gold answer (Rezaei) uses cues that are deliberately irrelevant to the answer.
> - **Most "regional" benchmarks carry the country as provenance, not as a patient attribute**
>   ([[PersianMedQA]], [[AfriMed-QA]], WorldMedQA-V). Race and ethnicity appear almost only as US-style tokens.
> - **By region:** Central Asia has nothing beyond the 50 [[ISSAI Dietary Recommendation profiles]]; the Gulf has only
>   tiny or synthetic sets; South Asia has the richest cue types but no gold answers; East Asia has traditional
>   medicine by construction.

## Detailed answer

### 1. What counts as a cultural cue
Four cue types (chosen by the user, 2026-10-07), each of which can sit in a structured field or in free text:
- **place:** the patient's country, city, nationality, migration or travel;
- **race / ethnicity:** a stated race or ethnic group;
- **food, habits, religion:** a named dish or cuisine-linked ingredient, a culture-linked habit (betel, khat,
  waterpipe), a religious practice (Ramadan fasting, halal);
- **traditional medicine:** TCM, Ayurveda, Unani, Kampo, Prophetic medicine, folk and herbal remedies.

Two distinctions matter for evaluation:
- **By construction vs in the item.** A Russian-language dataset is "from Russia", but a case that never mentions a
  place, food or habit gives a model nothing cultural to use. Language alone is not counted as a cue here.
- **Decisive vs incidental.** A cue is decisive when the gold answer depends on it (raw camel milk → brucellosis;
  Ramadan fasting → change the sulfonylurea dose). Most cues found are incidental ("a 71-year-old Japanese man").

### 2. Cues in the 37,631 cases we already have
The case table has since grown to 38,301 rows with the AI-flagged parts ([[Export tables]]); the counts below are
for the 8 gold datasets as first built and are unchanged for them.

Counted with `uv run db/cues.py` (keyword patterns in English, Russian, Chinese and Arabic over the `case` text; one
count per case; snippets checked by hand with `--examples`). The patterns are a **lower bound on recall** and are not
disambiguated.

| Dataset | Cases | Place | Ethnicity | Religion | Habit | Food | Trad. medicine | Any cue |
|---|---|---|---|---|---|---|---|---|
| [[MedCaseReasoning]] | 14,489 | 1,486 (10.3%) | 1,291 (8.9%) | 12 (0.1%) | 18 (0.1%) | 37 (0.3%) | 60 (0.4%) | 2,761 (19.1%) |
| [[NGQA]] | 13,802 | 0 | 0 | 0 | 0 | 3,814 (27.6%) | 0 | 3,814 (27.6%) |
| [[RuMedBench]] | 6,360 | 0 | 2 | 0 | 0 | 1 | 4 (0.1%) | 7 (0.1%) |
| [[FAM-Bench]] | 1,500 | 0 | 0 | 0 | 1 | 576 (38.4%) | 0 | 576 (38.4%) |
| [[MedicationQA]] | 680 | 0 | 0 | 0 | 0 | 0 | 1 | 1 (0.1%) |
| [[MTCMB]] | 400 | 2 (0.5%) | 0 | 0 | 203 (50.7%) | 8 (2.0%) | 396 (99.0%) | 396 (99.0%) |
| [[TCM-BEST4SDT]] | 300 | 32 (10.7%) | 0 | 0 | 53 (17.7%) | 2 (0.7%) | 210 (70.0%) | 230 (76.7%) |
| [[MedArabiQ]] | 100 | 2 (2.0%) | 0 | 0 | 0 | 0 | 1 (1.0%) | 3 (3.0%) |
| All | 37,631 | 1,522 (4.0%) | 1,293 (3.4%) | 12 | 275 (0.7%) | 4,438 (11.8%) | 672 (1.8%) | 7,788 (20.7%) |

What the matches are:
- **[[MedCaseReasoning]]** is the only set where the patient's nationality or ethnicity is stated in free text at
  scale: "A 71-year-old Japanese man", "A 22-year-old man from Kabul, Afghanistan", "A 68-year-old African-American
  man". There is no country field.
  - It also has a thin tail of **decisive** cues: unpasteurised camel milk → brucellosis, khat and betel chewing,
    "his diet consisted mainly of injera", the Kampo medicine Sai-rei-to before drug-induced illness, "presented during
    a month of religious fasting". These are tens of cases, not hundreds.
- **[[NGQA]]** and **[[FAM-Bench]]**: the case is a dish plus a condition, so the cue is on the dish ("Puerto Rican
  style", "Simple Persian Salad", curry, soy sauce). The person has no culture. NGQA's NHANES users could be joined
  back to a US race/ethnicity field, but that is not in the released items.
- **[[MTCMB]]** and **[[TCM-BEST4SDT]]** are traditional medicine by construction. Their "habit" matches are the
  solar term of onset (节气, a field in MTCMB's 200 real records) and taste preferences such as 喜食辛辣. TCM-BEST4SDT
  gives the patient's home province in 32 cases (籍贯：浙江杭州).
- **[[RuMedBench]]**: almost nothing. Two records state a nationality; one mentions raw elk liver (строганина); four
  mention herbal self-treatment. The "travel abroad: denied" template line was excluded.
- **[[MedArabiQ]]** patient questions: one asks whether cinnamon raises or lowers blood pressure, one names Saudi
  Arabia. Separately, its bias-injected MCQ file has 13 of 100 items with an injected "cultural" biasing sentence (see
  [[Q8 Injecting cultural cues into datasets|Q8]]).
- **[[ISSAI Dietary Recommendation profiles]]** (not in the case table, no gold): all 50 profiles are Kazakh by
  construction, with Kazakh diet histories.

### 3. Datasets designed around cultural cues
- **[[Rezaei2026 - Counterfactual Cultural Cues in Medical QA|Rezaei & Shakeri 2026]]:** 150 MedQA items × (3 groups
  × 3 cue types) + original + neutral control = 1,650 MCQs. Groups: Indigenous Canadian, Middle-Eastern Muslim,
  Southeast Asian. Cue types: identifier ("a Muslim man"), context ("symptoms began during evening prayer at a
  mosque"), or both. The repository is public but has no licence, and it stores the 1,350 cultural variants without
  the neutral control. The cues are non-decisive by design.
  - The cues are mostly place and occasion: "prayer" is in 73 of the 150 Middle-Eastern context variants and "mosque"
    in 57, but Ramadan in only 7, and herbal remedies in 3 of the 150 Southeast Asian ones. Food, fasting and
    traditional medicine are nearly absent.
- **[[Varadarajan2026 - CCBench|CCBench]]:** 60 personas, 10 for each of 6 cultures (Afghan, Burmese, Chinese, Māori,
  Nepali, Vietnamese), each asking 52 real forum health questions: 3,120 interactions. Norms such as halal diet,
  Ramadan fasting and dietary therapy are signalled implicitly in the dialogue history.
  - The gold is an LLM-written checklist of cultural accommodations per persona, not a clinical answer; no clinician
    or member of the cultures rated it.
  - The data is not released, but all 95 norms (diet, religion, traditional medicine per culture) are printed in the
    paper's appendix and tabulated in our note, so the norm inventory is usable now.
- **[[RamadanSafeQA]]:** 68 synthetic Ramadan × diabetes vignettes with a 4-item safety rubric (workshop poster; data
  not located). [[Alomair2026 - Ramadan medication advice by chatbots|Alomair et al. 2026]] adds 23 templated Ramadan
  medication scenarios in English and Arabic, with prompts in the supplement.
- **[[Sayeed2025 - Tibbe-AG Islamic medicine validation|Tibbe-AG]]:** 30 Prophetic-medicine questions with
  human-verified remedies (honey, black seed, vinegar, olive oil).
- **[[Nimo2025 - Africa Health Check|Africa Health Check]]:** MCQs built from 130+ country–herbal remedy pairs in 10
  African countries; the correct answer is the traditional remedy only in the country context. The GitHub repository
  held only a README on 2026-10-07.
- **[[Hamna2025 - Samiksha community-centred health benchmark|Samiksha]]:** 1,590 community-written queries in Hindi,
  Kannada and Malayalam ("I have low BP. Can I fast for Shivratri?", "Why shouldn't I eat mango or jackfruit when
  pregnant?"). No gold answers by design; data link not found.
- **[[Asiedu2024 - TRINDs tropical and infectious diseases|TRINDs]]:** 52 seed personas with a location slot, expanded
  to 11,719 queries. Swapping the endemic location for San Francisco lowers accuracy; adding a race token does not.

### 4. Datasets with structured demographic or country fields
- **[[NutriBench]]:** a `country` field on 15,617 meals from 24 countries (USA 11,071; about 200 each for India,
  Pakistan, Sri Lanka, Malaysia, Laos, Philippines, Tunisia…). No Gulf, Central Asian or East Asian country, and no
  medical conclusion.
- **[[PerMedCQA]]** (67,791 real Iranian patient questions with physician answers): fields are only Age, Sex and
  Weight, each empty in about half of rows. In free text, a rough Persian keyword count (ours, 2026-10-07) finds a
  city or province in 1,279 questions (1.9%), Ramadan fasting or prayer in 288 (0.4%), Iranian foods or waterpipe in
  205 (0.3%) and herbal or Persian traditional medicine in up to 1,071 (1.6%; overcounted). It is the largest open
  source of real Middle Eastern cases with naturally occurring cues.
- **[[DDXPlus]]:** a geographical region per synthetic patient; the default is North America and other regions enter
  only as recent travel.
- **[[HealthBench]]:** no per-item country field, but 1,097 of 5,000 conversations (21.9%) carry the "global health"
  theme, where practice norms, resources or local epidemiology matter.
  [[Hisada2025 - HealthBench for the Japanese medical system|Hisada et al. 2025]] re-annotated it for Japan: 82.1% of
  conversations are directly applicable, but only 39.1% of rubric criteria.
- **No dataset found has a religion field or a diet-pattern field.** The MENST dataset
  ([[MenstLLaMA2025 - MENST menstrual health dataset (India)|MenstLLaMA]]) may have a sociocultural-context field;
  this comes from a search snippet and is unverified.

### 5. Race and ethnicity as US-style tokens
[[Rawat2024 - DiversityMedQA|DiversityMedQA]] (567 items with "The patient is of African descent" etc.),
[[Xiao2025 - FairMedQA|FairMedQA]] (4,806 variants of 801 vignettes), [[Pfohl2024 - EquityMedQA health equity toolbox|EquityMedQA]] (4,619 questions in seven sets, no gold answers) and
[[Omar2025 - Sociodemographic biases in LLM medical decisions|Omar et al. 2025]] (1,000 cases × 32 variants) all use
Black / White / Asian / Hispanic labels. They are bias audits ([[Q8 Injecting cultural cues into datasets|Q8]]), not
sources of cultural content.

### 6. Regional by construction only
[[PersianMedQA]], [[AfriMed-QA]], [[Matos2024 - WorldMedQA-V|WorldMedQA-V]], [[KorMedMCQA]], [[IgakuQA]],
[[Gabriel2026 - IyawoBench|IyàwóBench]] and [[BhashaBench-Ayur]] carry the country as the source of the exam or
question. PersianMedQA's "3–10% of questions can only be answered correctly in Persian" is attributed by its authors
to Iranian clinical protocols, regional disease prevalence and translation drift, not to food or religion.
[[Jang2023 - GPT-4 on the Korean Medicine licensing exam|Jang et al. 2023]] is the one quantified split: 204 of 340
Korean-medicine exam questions need traditional-medicine knowledge.

## Comparison table
Ranked by how useful the cultural content is for our evaluation.

| Dataset | Region / language | Cue types | Cue form | Decisive for the answer? | Size | Gold | Access |
|---|---|---|---|---|---|---|---|
| [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA\|Rezaei & Shakeri 2026]] | Middle-Eastern Muslim, SE Asian, Indigenous Canadian; EN | ethnicity, religion, place and occasion | injected free text | no, by design (a few items leak or lose a decisive cue) | 1,650 (1,350 released) | MCQ, one clinician | public GitHub, no licence |
| [[Varadarajan2026 - CCBench\|CCBench]] | Afghan, Burmese, Chinese, Māori, Nepali, Vietnamese; EN | food, religion, tradmed | implicit in dialogue | yes | 3,120 | LLM-written persona checklist | not released; 95 norms printed in the paper |
| [[MedCaseReasoning]] | global; EN | place, ethnicity; rare food, habit, tradmed | free text | mostly no; tens of decisive cases | 14,489 (2,761 with a cue) | diagnosis | open ✅ |
| [[PerMedCQA]] | Iran; FA | place, religion, tradmed, food | free text | sometimes | 67,791 (~4% with a cue) | physician answer | open (HF, CC BY-NC-SA) |
| [[TCM-BEST4SDT]] | China; ZH | tradmed, province, solar term, taste habits | fields in text | yes (diet precautions in gold) | 300 | syndrome → prescription | open ✅ |
| [[MTCMB]] | China; ZH | tradmed, solar term | fields in text | partly | 400 in the case table | syndrome, herbs | open ✅ |
| [[ISSAI Dietary Recommendation profiles]] | Kazakhstan; EN/RU/KK | food, habits | profile text | yes | 50 × 3 | none (GPT-4 answers) | open ✅ |
| [[Hamna2025 - Samiksha community-centred health benchmark\|Samiksha]] | India; HI/KN/ML | food, religion | free text | yes | 1,590 | none | not found |
| [[RamadanSafeQA]] | Muslim patients | religion | by construction | yes | 68 | safety rubric | not located |
| [[Asiedu2024 - TRINDs tropical and infectious diseases\|TRINDs]] | tropical regions; EN | place, race | template slot | place yes, race no | 11,719 | disease label | seed open, rest on request |
| [[Nimo2025 - Africa Health Check\|Africa Health Check]] | 10 African countries; EN | tradmed, country | structured pairs | yes | 130+ pairs | herbal remedy | not released |
| [[NutriBench]] | 24 countries; EN | country, food | `country` field | n/a | 15,617 | macros | open (HF) |
| [[FAM-Bench]], [[NGQA]] | US; EN | cuisine name on the dish | dish text | no | 1,500; 13,802 | suitability | open ✅ |
| [[HealthBench]] | global; multilingual | resource setting | theme tag | sometimes | 1,097 of 5,000 | rubric (US-normed) | open |
| [[RuMedBench]], [[MedArabiQ]], [[MedicationQA]] | Russia; Arab region; US | language only | — | — | 6,360; 100; 680 | ✓ | open ✅ |

## Gaps & open questions
1. **No culturally decisive cases with a clinician gold at scale.** The decisive ones in hand are the tail of
   [[MedCaseReasoning]] (camel milk, khat, injera, Kampo), TCM-BEST4SDT's diet precautions and a few hundred
   PerMedCQA questions. Mining them (the `cue_*` and `relevance` columns of `db/export/cases.parquet` mark the rows) gives a small real
   seed set.
2. **Central Asia has no cue-bearing medical items at all**, and the Gulf has only synthetic or tiny sets. Any
   evaluation for these regions has to be built, by injection ([[Q8 Injecting cultural cues into datasets|Q8]]) or by
   collection.
3. **Cues sit on the dish or on the patient, never on both.** Diet benchmarks have culturally named dishes and a
   condition but no person; clinical cases have a person but no diet. Joining them is exactly what our graph allows.
4. **The keyword count is a lower bound.** A model-based tagger (as in Global MMLU's sensitive / agnostic labels)
   over the 37,631 cases would give recall and separate decisive from incidental cues.
5. **To verify or obtain:** the PerMedCQA count needs a native reader; MENST's sociocultural field; CCBench,
   Samiksha, RamadanSafeQA and Africa Health Check data need the authors ([[Access requests]]).
6. **Corrections made to earlier notes:** RamadanSafeQA is a MusIML workshop poster at ICML 2026, not a main-track
   paper; PersianMedQA's "Persian-specific" share is about protocols and epidemiology, not cultural lifestyle cues.

## Papers
![[Papers.base#This question]]
