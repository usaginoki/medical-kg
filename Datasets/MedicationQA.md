---
title: "MedicationQA"
slug: medicationqa
kind: [case]
version: "MedInfo2019-QA-Medications.xlsx in abachaa/Medication_QA_MedInfo2019, clone of commit 20363d1 (2025-12-05, README edit); the xlsx itself was uploaded on 2019-05-07 (0ef9dec) and has not changed since"
previous_versions: ""
papers: ["[[BenAbacha2019 - MedicationQA consumer medication QA]]"]
url: "https://github.com/abachaa/Medication_QA_MedInfo2019"
license: "CC BY 4.0. The README says: 'The medicationQA dataset is published under a Creative Commons Attribution 4.0 International License (CC BY).' There is no LICENSE file, and the GitHub API reports no licence. The MEDINFO paper itself is CC BY-NC 4.0. The answers are excerpts copied from third-party pages (DailyMed, MedlinePlus, Mayo Clinic, Healthline, Livestrong, Medical News Today…)."
availability: open-download
access_link: "https://github.com/abachaa/Medication_QA_MedInfo2019"
accessed: true
access_method: [github]
access_date: 2026-10-07
access_notes: "git clone --depth 1 worked: one 163 KB Excel file (sheet `DrugQA`, 690 rows) plus the README. Nothing was gated. The .git folder was dropped. The Hugging Face mirror truehealth/medicationqa exists but was not used."
countries: ["[[United States]]"]
regions: ["[[North America]]"]
n_records: "690 rows: 651 distinct questions, 680 rows with an answer (the paper reports 674 QA pairs)"
size: "0.2 MB"
formats: [xlsx]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: ""
body_effect_how: ""
join_keys: [drug name (Focus column; generic or US brand), answer URL (DailyMed setid, MedlinePlus drug page)]
case_type: [real]
conclusion_type: [advice, safety-warning, drug-information]
languages: [en]
n_cases: "690 real consumer medication questions with a reference answer (680 answered). 33 rows pair a food, drink, alcohol, supplement or meal with a drug; 38 more ask about a vitamin, mineral, supplement or herb itself"
diet_relevance: subset
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases]
tags:
  - type/dataset
  - kind/case
  - case/real
  - q/4
  - access/accessed
  - access/open
  - region/americas
---
# MedicationQA

> [!abstract] TL;DR
> MedicationQA is the US National Library of Medicine's gold standard of **real consumer questions about medicines** ([[BenAbacha2019 - MedicationQA consumer medication QA|Ben Abacha et al., MEDINFO 2019]]).
> - **What a row is:** an anonymised question that a consumer sent to MedlinePlus, plus a reference answer passage that annotators found by hand. Sources were DailyMed, MedlinePlus, other NIH/CDC pages, then Mayo Clinic and others. Each row is also annotated with its focus drug and question type.
> - **Size:** the file has 690 rows (the paper reports 674 QA pairs). Everything is in English and from the US.
> - **Case and conclusion:** the "case" is a short patient-side question, not a clinical vignette. The conclusion is advice or a safety warning.
> - **The food subset is the point:**
>   - 20 rows (19 distinct questions) pair a food, drink, alcohol, supplement, herb or vitamin with a drug: grapefruit + statins, warfarin + cabbage/spices, levothyroxine + walnut/calcium, and others.
>   - 7 more rows ask when to take a drug relative to meals.
>   - In 6 more, only the gold answer brings in a food, alcohol or supplement fact.
>   - Total: **33 rows (4.8%)**.
> - **KG coverage:** our KG's [[DDID]] edges cover **7 of the 26 distinct pair or timing questions**.
> - **Use for us:** a small but real test of whether food–drug knowledge improves answers to consumer questions.

## Access
| | |
|---|---|
| Availability | open-download (GitHub; README states CC BY 4.0) |
| Link | https://github.com/abachaa/Medication_QA_MedInfo2019 |
| Accessed? | true |
| How | `git clone --depth 1` (commit `20363d1`); the data file is unchanged since 2019-05-07 |
| Downloaded | `Data/medicationqa/MedInfo2019-QA-Medications.xlsx` (163 KB) + `README.md` |

## Tables & columns
Column meanings come from the README and the paper. The file has no id column. **In this note, `#n` is the row's 1-based position in the sheet** (Excel row = n + 1).

### `MedInfo2019-QA-Medications.xlsx:DrugQA` (690 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Question` | str | the consumer question as submitted to MedlinePlus: lower case, typos kept (median 38 characters). Questions were picked by MetaMapLite drug entities (UMLS types antibiotic, clinical drug, pharmacologic substance, steroid, **vitamin**…) and then filtered by hand (paper). 651 distinct; 29 questions occur on more than one row (different types or answers) | `what if i eat grapefruit on simvastatin` |
| `Focus (Drug)` | str | the annotated question focus, "always a Drug name". It is written as in the question, so it can be a brand, a class, or `n/a (Exploration)`. 515 distinct (471 after lower-casing); missing on 1 row (#213) | `Simvastatin` |
| `Question Type` | str | annotated question type: 37 labels in the file, including compound ones such as `Usage/time`, `Action/time`, `Dose/time`. The paper groups them into 25 types and uses 14 for classification. Most frequent: Information 112, Dose 66, Usage 61, Side effects 57, Indication 55, **Interaction 51**, Appearance 38, Action 36, Usage/time 36 | `Interaction` |
| `Answer` | str | **gold answer**: the passage copied from the source (median 256 characters). 10 rows say `No answers` (#32, 122, 145, 148, 151, 158, 159, 169, 213, 449) | `Certain classes of drugs — most notably statins — are metabolized … by an enzyme called CYP3A … Grapefruit juice contains compounds called furanocoumarins that stop CYP3A…` |
| `Section Title` | str | the section of the source page the answer comes from (89% filled) | `What special dietary instructions should I follow?`, `DRUG INTERACTIONS` |
| `URL` | str | the source page (98% filled). By domain: dailymed.nlm.nih.gov 290, medlineplus.gov 134, ncbi.nlm.nih.gov 33, cdc.gov 28, mayoclinic.org 14, wikipedia 9, healthline 9, drugabuse.gov 8, fda.gov 7 | `https://www.health.harvard.edu/heart-health/grapefruit-juice-and-statins` |

Sample: `Data/medicationqa/sample.csv` (first 50 rows) · full profile: `Data/medicationqa/schema.md`

## Countries & cultures covered
- **[[United States]] only.** The questions were submitted to MedlinePlus (NLM). The answer guideline followed FDA advice: MedlinePlus, then DailyMed, then other US government sites, then trusted sites, then Google.
- Drug names are mostly US brands (Synthroid, Coumadin, Fosamax, Rapaflo). A handful of answers come from UK sources (NHS, medicines.org.uk).
- **Not culture-specific.** The foods in the subset are generic Western items: grapefruit, walnut, cabbage, tea, coconut oil, spices, alcohol, calcium/magnesium supplements. No cuisine or dish is named, and no traditional-medicine herbs appear except the [[DDID]]-style ones that the answers list (garlic, ginger, ginkgo, ginseng, St John's wort, yohimbe).

## Cases & conclusions
**One real case** (#132, type Interaction, focus Simvastatin):
- *Question:* "what if i eat grapefruit on simvastatin"
- *Gold answer* (Harvard Health, "Grapefruit juice and statins"): "Certain classes of drugs — most notably statins — are metabolized (broken down) in your intestines by an enzyme called CYP3A, which normally reduces the amount of drug that enters your bloodstream. Grapefruit juice contains compounds called furanocoumarins that stop CYP3A from doing its job. As a result, more of the drug is absorbed, making it more powerful than it's meant to be — even toxic in some cases."

**What the gold is.** One reference passage per row. Four annotators searched the sources in a fixed order. A medical doctor and a QA expert then reconciled the question types and validated the answers (paper). Answers are often **conditional** (on manufacturer, dose or patient) or **distributed** across several snippets.
- Some gold answers miss the food. #15 (Metamucil + ciprofloxacin) answers with a generic antibiotic-diarrhoea warning. #50 (tea + azithromycin) answers with a list of interacting drugs that does not mention tea.

**How it is scored.** The release defines no answer-scoring protocol.
- The paper evaluates only question understanding:
  - focus recognition with a Bi-LSTM-CRF: F1 74.07 exact / 90.37 partial;
  - question type with a CNN over 14 merged types: 75.7% accuracy.
- Answer retrieval was judged by hand on 20 questions. CHiQA found a correct answer in the top 4 for 35%, only related answers for 35%, and irrelevant answers for 30%.
- Later work uses the questions as long-form items judged by human raters: MultiMedQA in [[Singhal2022 - Large Language Models Encode Clinical Knowledge]].
- For us this means rubric or LLM-judge scoring against the reference passage. Check the safety-critical point, e.g. "avoid grapefruit", "take 4 h apart from calcium", "limit alcohol".

### Food, drink and supplement × drug subset
Found by reading all 690 questions, plus a regex over the answers. Rows are numbered as above.

**A. The question pairs a food, drink, alcohol, supplement, herb or vitamin with a drug: 20 rows (19 distinct questions)**

| # | food / drink / supplement | drug | gold answer (gist) | KG edge? |
|---|---|---|---|---|
| 7 | alcohol ("a cocktail") | acetaminophen (Tylenol) | small amounts usually safe; with alcohol, risk of severe or fatal liver damage; >3 drinks/day ask a doctor | no |
| 12 | walnut (dietary fibre) | levothyroxine (Synthroid) | dietary fibre in walnuts, soy, iron supplements and multivitamins impedes absorption | **yes** (DDID, Negative) |
| 15 | Metamucil (psyllium fibre supplement) | ciprofloxacin | off-target: antibiotic-associated diarrhoea warning | no (no psyllium ingredient) |
| 50 | tea | azithromycin | off-target: generic interacting-drug list | no (azithromycin has 0 food edges) |
| 122 | salt | hydromorphone | `No answers` | no |
| 132 | grapefruit | simvastatin | furanocoumarins block CYP3A → more drug absorbed | **yes** (DDID, CYP3A4, Positive/Harmful) |
| 144 | probiotic | antibiotics (class) | can reduce diarrhoea; take a few hours apart | no |
| 147 | vitamin K foods (leafy greens, some oils), grapefruit | warfarin | keep vitamin K intake consistent; ask about grapefruit | **yes** (spinach, broccoli, cabbage, grapefruit) |
| 169 | coconut oil | ursodiol | `No answers` | no (UDCA has 0 food edges) |
| 304 | OTC calcium | alendronate | calcium, antacids and multivalent cations block absorption; wait ≥ 30 min | partial (alendronate–coffee/orange juice only) |
| 376 | foods in general, alcohol | metformin | no foods to avoid; limit alcohol | partial (metformin–ginseng, licorice… but no alcohol) |
| 399 | magnesium | phenytoin (Dilantin) | rat study: high-dose MgO enhances phenytoin's effect | no (minerals are compounds; no compound–drug edges) |
| 417 | herbal supplements (yohimbe) | brimonidine | yohimbine can block brimonidine; avoid | no |
| 418 | OTC calcium | alendronate | duplicate of #304 | partial |
| 490 | grapefruit | statins (simvastatin, atorvastatin), nifedipine, cyclosporine, buspirone, budesonide, amiodarone, fexofenadine | FDA list of drug classes that grapefruit juice interacts with | **yes**, all 8 drugs |
| 572 | calcium (carbonate) | levothyroxine (Synthroid) | insoluble chelate; take 4 h apart | partial (levothyroxine has food edges, but not to calcium) |
| 575 | vitamins (gold: tyramine-rich foods) | rasagiline | MAO-B selective, no tyramine restriction needed, but very high-tyramine foods (≥ 150 mg) may raise blood pressure | no |
| 607 | spices and herbs: garlic, ginger, ginkgo, St John's wort, ginseng | warfarin | review: 58 plants alter haemostasis; coumarins, quinones, vitamin K… | **yes** for garlic, ginger, ginkgo, ginseng (St John's wort not in the KG) |
| 635 | alcohol | levodopa/carbidopa | alcohol can worsen side effects | no |
| 649 | cabbage (vitamin K foods, cranberry juice, green tea, fish oil, herbal teas) | warfarin | keep intake consistent; eat only small amounts | **yes** (cabbage, cranberry, green tea, fish oil) |

**B. The question asks about meal timing for a drug: 7 rows (6 distinct)**

| # | food | drug | gold answer (gist) | KG edge? |
|---|---|---|---|---|
| 16 | meal | lansoprazole | before eating, in the morning | no (food-effect timing is not in the KG) |
| 48 | meal | silodosin (Rapaflo) | once daily with a meal | no |
| 134 / 191 | food | statins (class) | some brands with food, others with or without | n/a |
| 464 | evening meal | metformin ER | once daily with the evening meal | no |
| 552 | food (general) | any drug | NHS: 6 reasons to take medicines with or after food | n/a |
| 595 | breakfast, coffee, orange juice | alendronate (Fosamax) | bioavailability falls ~40% with a meal; take after an overnight fast | **yes** (alendronate–coffee and –orange: Negative) |

**C. Only the gold answer brings in a food, alcohol or supplement fact: 6 rows**
- #36 denosumab: take calcium + vitamin D supplements.
- #56 medicines that raise blood sugar: includes the B vitamin niacin.
- #85 valsartan: hypotension more likely on a low-salt diet.
- #141 pain medicines: acetaminophen + ≥ 3 alcoholic drinks/day → liver damage.
- #197 lansoprazole long term: vitamin B12 and magnesium deficiency.
- #358 gabapentin: avoid with antacids and ginkgo.

**D. The focus is a vitamin, mineral, supplement, herb or food, with no second drug: 38 rows**
- **Vitamins (19 rows):**
  - vitamin C: #22
  - vitamin D: #43, 46, 168, 463, 570
  - vitamin A: #155, 390
  - vitamin B compound: #127
  - B12 / cobalamin / cyanocobalamin: #128, 130, 260, 484, 494, 563, 580, 626
  - fat-soluble vitamins: #624
  - multivitamin (Thera-Tabs): #605
- **Minerals and supplements (10 rows):**
  - magnesium: #108, 242, 587
  - iron: #592, 665, 666
  - fish oil: #568
  - bioflavonoid: #218
  - biotin interfering with blood tests: #298
  - glucosamine and glaucoma: #365
- **Herbs and foods (9 rows):**
  - peppermint oil in mouthwash: #99, 340, 397, 458
  - palmarosa: #203
  - senna: #389
  - beetroot (*Beta vulgaris*): #486
  - Epsom salt in diabetes: #466
  - salt-water mouthwash: #492
- **Not counted:** marijuana/CBD (17 rows), nicotine, fluoride, Tums, pepsin, thymol, nanosilver.

**Totals (diet_relevance: subset):** A + B + C = **33 rows (4.8%) with a food/drink/supplement × drug question or answer**. Adding D gives 71 rows (10.3%) that touch food, drink, supplements, herbs or vitamins at all. All A–C items are Western foods. This is a seed set for a food–drug test, not a full benchmark.

## Linking to the vault's KG
Here "KG" is the [[Unified database]] (export: [[Export tables]]).
- **Drugs → `drug` table.**
  - Exact, case-insensitive name match: **149 of 471 distinct focus strings match a `drug.name` (263 / 690 rows)**. 82 of those drugs have at least one food or herb edge (155 rows).
  - Brand names need a brand → generic map first (Synthroid → levothyroxine, Dilantin → phenytoin, Fosamax → alendronic acid, Rapaflo → silodosin, Tylenol → acetaminophen). [[DrugBank]] synonyms or RxNorm would provide it.
  - Every generic drug in the A–C rows is in the table (ursodiol as "Ursodeoxycholic Acid", alendronate as "Alendronic Acid").
- **Foods → `ingredient`.**
  - These resolve through `ingredient_alias`: grapefruit, walnut, tea / green tea, coconut oil, cabbage, garlic, ginger, ginkgo (as `ginkgo nuts`), ginseng, salt, spinach, broccoli, cranberry, coffee, orange.
  - These do not: psyllium/Metamucil, probiotics, yohimbe, St John's wort, and "alcohol" (only generic `alcoholic beverages`).
- **Edges → `ingredient_drug` ([[DDID]], plus [[DrugBank]] via DDID).**
  - The KG answers 6 of the 19 distinct A questions (#12, 132, 147, 490, 607, 649) and 1 of the 6 distinct B questions (#595). That is 7 of 26.
  - Grapefruit alone has edges to 233 drugs.
- **Gaps the subset exposes:**
  1. **Minerals and vitamins as interactants.** Calcium, magnesium, iron, vitamin K and tyramine are `compound` rows, but the KG has no compound → drug edges. So levothyroxine–calcium, alendronate–calcium, phenytoin–magnesium and warfarin–vitamin K are only reachable indirectly (food → vitamin K content).
  2. **Alcohol.** Only 2 alcohol–drug edges exist (beer–phenelzine, beer–tranylcypromine). Acetaminophen, levodopa and metformin + alcohol are missing.
  3. **Meal-timing / food-effect rules** (take with or without food, before breakfast) are not modelled.
  4. **Supplements without a plant source** (probiotics, psyllium) are missing.
  - [[FooDrugs]] is the other food–drug source to check for items 2–4.
- **Test design.** Give the LLM the question with and without the KG's food–drug paths for the drug and food, then score against the gold passage with a rubric. The 6 + 1 covered items test whether retrieval helps. The others test whether the model says "not known" rather than inventing an interaction.
- Related case sets: [[FAM-Bench]] (Coumadin-safe recipe tags, no food–drug gold) and [[NGQA]] (diet suitability, no drugs).

## Versions
- One release: the xlsx uploaded on 2019-05-07. Later commits change only the README (2019–2025).
- Paper: MEDINFO 2019 (Lyon), *Stud Health Technol Inform* 264:25–29, online 2019-08-22.
- Copies: Hugging Face `truehealth/medicationqa` (2023) and others. MedicationQA is one of the MultiMedQA sets used by Med-PaLM ([[Singhal2022 - Large Language Models Encode Clinical Knowledge]]).

## Caveats
- **Small and dated.** Only 20 rows pair a named food, drink or supplement with a drug, and 4 of these have no usable gold: #122 and #169 are unanswered, #15 and #50 are off-target. Answers reflect 2018–2019 web pages; DailyMed labels have changed since.
- **Not a patient case.** There is no age, sex, comorbidity or other drugs, so the answers are generic. The paper notes that many questions are "too underspecified" and that answers are often conditional.
- **Gold is extractive.** It is one copied passage per row, sometimes incomplete or only partly on topic, and sometimes from non-authoritative sites (Livestrong, tadalafildosage.info). The duplicate rows (#304 = #418, #134 = #191) inflate counts.
- **Licence.** CC BY 4.0 per the README, but the answer passages are third-party text (many US-government public domain, others copyrighted: Mayo Clinic, Healthline, Livestrong, Medical News Today, Harvard Health). CC BY cannot override that. Our committed `sample.csv` holds 50 rows of these answers, the same situation as [[FAM-Bench]].
- **Possible contamination:** public since 2019 and part of MultiMedQA, so LLMs have likely seen it.
- The food subset was coded by one reader (us) from the question text; regex over the answers may miss paraphrases.
