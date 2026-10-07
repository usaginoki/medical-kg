---
title: "MedCaseReasoning"
slug: medcasereasoning
kind: [case]
version: "HF zou-lab/MedCaseReasoning @ 469a536 (last modified 2025-06-02)"
previous_versions: ""
papers: ["[[Wu2025 - MedCaseReasoning diagnostic reasoning from case reports]]"]
url: "https://huggingface.co/datasets/zou-lab/MedCaseReasoning"
license: "HF dataset card: `license: mit`. GitHub README (kevinwu23/Stanford-MedCaseReasoning, no LICENSE file): 'Code — MIT · Dataset — CC-BY 4.0 (derived from the PMC Open Access Subset)'. Source articles keep their own PMC OA licences, not recorded per row."
availability: open-download
access_link: "https://huggingface.co/datasets/zou-lab/MedCaseReasoning"
accessed: true
access_method: [huggingface]
access_date: 2026-10-07
access_notes: "`uv run hf download zou-lab/MedCaseReasoning --repo-type dataset --local-dir Data/medcasereasoning` worked without login (not gated; revision 469a536, 406 MB). The repo also has medcasereasoning_core.csv (205 MB) and medcasereasoning_core.pqt (110 MB). We checked that they are the union of the three split parquets plus a `split` column (all 14,489 pmcids and every field identical), so we deleted them and the .cache/ folder and kept data/{train,val,test} parquet (110 MB). The GitHub repo is marked 'under construction': prompts.py, evaluate.py and the fine-tuning code listed in its README are missing, so the official LLM-judge scoring cannot be rerun from the repo."
countries: []
regions: ["[[Global]]"]
n_records: "14,489 cases: train 13,092 · val 500 · test 897"
size: "110 MB (3 parquet files)"
formats: [parquet]
join_keys: [PMCID, final diagnosis name (free text; ~52% match a MeSH/UMLS condition name or alias)]
case_type: [real]
conclusion_type: [diagnosis, differential]
languages: [en]
n_cases: "14,489 real published case reports → 1 final diagnosis + 1–21 clinician reasoning statements (test 897)"
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
  - region/global
  - access/accessed
  - access/open
---
# MedCaseReasoning

> [!abstract] TL;DR
> MedCaseReasoning (Wu, Wu, … Zou; Stanford / UCSF / USC; arXiv May 2025) turns **14,489 open-access PubMed Central
> case reports** (813 journals, 2005–2025) into diagnostic question–answer pairs:
> - a case presentation cut off before the diagnosis is revealed (median 179 words);
> - a **gold final diagnosis**;
> - the authors' **differential-diagnosis reasoning** as numbered statements with quotes (median 5).
>
> An LLM pipeline built the cases: o4-mini converted and scored them, gemini-2.5-pro filtered for faithfulness. Physicians checked 100 of them.
> The test set has 897 cases; the paper scores diagnostic accuracy (LLM judge, 1/5/10 attempts) and "reasoning recall".
>
> It is global English with no country field, but 11% of prompts name a country or nationality.
>
> Diet is a subset theme:
> - 1,334 cases (9.2%; test 105) mention diet, food, meals, nutrition, supplements, vitamins or herbal products;
> - ~343 gold diagnoses (test 20) are food-related: scurvy, brucellosis, anisakiasis, star fruit intoxication,
>   liquorice-induced pseudo-hyperaldosteronism, kratom liver injury, alpha-gal syndrome…
>
> This makes it a good source of **real cases for a food/herb–drug test set**.

## Access
| | |
|---|---|
| Availability | open-download (Hugging Face, not gated) |
| Link | https://huggingface.co/datasets/zou-lab/MedCaseReasoning · code: https://github.com/kevinwu23/Stanford-MedCaseReasoning |
| Accessed? | true (complete) |
| How | `uv run hf download zou-lab/MedCaseReasoning --repo-type dataset --local-dir Data/medcasereasoning` |
| Downloaded | `Data/medcasereasoning/data/{train,val,test}-00000-of-00001.parquet` (110 MB), `README.md` (dataset card). Duplicate `medcasereasoning_core.{csv,pqt}` deleted after checking. |

## Tables & columns
Three splits with the same 10 columns. Meanings come from the paper (Fig. 1C, §2.1) and the GitHub README.

### `data/train` (13,092 rows) · `data/val` (500) · `data/test` (897)
| column | type | meaning | example (test, PMC11126872) |
|---|---|---|---|
| `Unnamed: 0` | int | row number in the combined core file (0–14,488, unique); a leftover pandas index (inferred) | `5145` |
| `pmcid` | str | PubMed Central id of the source case report; unique | `PMC11126872` |
| `title` | str | article title | `A case report of a childhood scurvy musculoskeletal manifestation…` |
| `journal` | str | journal; 813 distinct | `Radiology Case Reports` |
| `article_link` | str | PMC URL | `https://www.ncbi.nlm.nih.gov/pmc/articles/PMC…` |
| `publication_date` | str | `YYYY-MM-DD`, `YYYY-MM` or `YYYY` | `2024-05-17` |
| `text` | str | full article body extracted from the PMC XML (median 1,606 words); **contains the answer** | |
| `case_prompt` | str | **model input**: "the case presentation that contains the relevant and sufficient patient information for making a diagnosis", written by o4-mini with an "information cutoff". Median 179 words (p10 117, max 479). | `A 6-year-old boy was brought for evaluation…` |
| `diagnostic_reasoning` | str | "the diagnostic decision-making by the case author (in enumerated statements)", each with a quote. 1–21 items, median 5. | `1. Primary bone neoplasm was considered…` |
| `final_diagnosis` | str | **gold label**, short free text. 8,861 distinct strings (7,383 after normalising case/underscores); median 22 characters. | `scurvy` |

- **Splits:** 897 test cases were picked where the transparency and integrative-reasoning scores were ≥ 4 (of 5). The val split (500) is not described in the paper.
- **Publication years:** 59.6% from 2020 or later, 16.5% from 2024 or later; one row has the date `201`.
- **Top journals:** J Med Case Reports 1,183 · Clinical Case Reports 1,098 · Int J Surg Case Rep 991 · Radiology Case Reports 925 · J Surg Case Rep 419 · JAAD Case Reports 359.

Sample: `Data/medcasereasoning/sample.csv` (train) + `sample_data_test_…csv`, `sample_data_val_…csv` · full profile: `Data/medcasereasoning/schema.md`

## Countries & cultures covered
**[[Global]]**: there is no country, site or ethnicity field. PMC case reports come from authors worldwide.
- 1,594 case prompts (11.0%) name a country or nationality (our regex over country names and demonyms). Most frequent: Japan/Japanese ~284, India ~136, China ~131, Iran 45, Nepal 40, Thailand 36, Sri Lanka 32, Ethiopia 31, Mexico 29, Philippines 29, Saudi Arabia 28, Morocco 26, Brazil 26. The US count is inflated by "African American".
- 1,253 prompts give a race or ethnicity descriptor (Caucasian, Asian, Hispanic…).
- Culture-specific exposures appear in the case text:
  - grilled freshwater crab and shrimp → paragonimiasis (e.g. a man from Kathmandu, Nepal);
  - anchovies → anisakiasis;
  - a Hmong man's herbal remedy → aconitine poisoning;
  - the Japanese Kampo formula Sai-rei-to → lung injury;
  - "chow" pickled fruit and grapefruit biting → erosive tooth wear (Trinidad).
  
  These are not labelled. Country facets would need NER over `case_prompt`/`text`, so `countries` is left empty.

## Cases & conclusions
**One real case** (test, PMC11126872, Radiology Case Reports 2024):
> *Input (`case_prompt`, shortened):* "A 6-year-old boy was brought for evaluation of 2 months of persistent, throbbing right
> thigh pain and progressive swelling… generalized lethargy and low-grade fever… **Dietary history revealed minimal
> fruit and vegetable intake.** On examination, he appeared irritable and malnourished (weight <1st percentile). There
> were hemorrhagic findings on the gingiva and labia… a firm, tender mass extended across the mid-thigh… hemoglobin
> 4.8 g/dL… platelets 751,000/µL. Coagulation studies… normal… the orthopedic team considered a primary bone neoplasm."
> *Gold reasoning:* "1. Primary bone neoplasm was considered because of persistent thigh pain, swelling, and a palpable
> mass… 2. Nutritional deficiency–related bone disorder was suggested by the patient's diet — 'the child's dietary
> recall highlighted a significant deficit in the consumption of fruits and vegetables.'"
> *Gold `final_diagnosis`:* **scurvy**.

**Scoring** (paper §2.2–2.3):
- **Diagnostic accuracy:** a gpt-4o-mini judge with the McDuff et al. (2025) prompt decides whether the predicted diagnosis matches the gold one. Each model answers 10 times (temperature 0.8, top-p 0.95); 1-, 5- and 10-shot accuracy are reported.
- **Reasoning recall:** the share of gold reasoning statements found in the model's trace (o4-mini judge). A physician agreed with 84 of 89 judged statement–trace pairs.
- **Results** (test, 10-shot accuracy / recall):
  - OpenAI o3 0.645 / n.a. · DeepSeek-R1 0.480 / 0.642 · QwQ-32B 0.398 / 0.590 · LLaMA-3.1-8B 0.332 / 0.451
  - after SFT on the train split: MedReason-8B 0.501 / 0.522
- **Validity:** physicians reviewed 100 cases. 98% were free of hallucinations; 92% of final diagnoses were faithful and inferable; 93% of reasoning steps were faithful.

**Food, diet, supplements, food–drug** (case-insensitive word regex over the three answer-relevant fields, n = 14,489; test n = 897):
| keyword (pattern) | `case_prompt` | `diagnostic_reasoning` | `final_diagnosis` | any field | any field, test |
|---|---|---|---|---|---|
| diet\* | 199 | 70 | 4 | 242 | 24 |
| food(s) / food-borne | 211 | 55 | 5 | 238 | 18 |
| meal(s) | 109 | 16 | 0 | 117 | 10 |
| nutrition\* / nutrient\* | 74 | 54 | 1 | 117 | 12 |
| supplement\* | 301 | 63 | 0 | 338 | 27 |
| vitamin(s) | 367 | 177 | 15 | 450 | 32 |
| herbal / herb(s) | 55 | 16 | 0 | 64 | 6 |
| grapefruit | 2 | 0 | 0 | 2 | 0 |
| alcohol\* | 943 | 159 | 3 | 1,002 | 68 |
| malnutrition / malnourish\* | 66 | 23 | 1 | 84 | 5 |
| deficien\* | 224 | 395 | 79 | 566 | 31 |
| **any of the above** | 2,080 | 776 | 95 | **2,436 (16.8%)** | **174 (19.4%)** |
| **any excl. alcohol and deficien\*** | 1,153 | 403 | 26 | **1,334 (9.2%)** | **105 (11.7%)** |

Most alcohol hits are social history ("denied alcohol use"). Most "deficiency" hits are non-nutritional (G6PD, factor, immunodeficiency).

**Food-related gold diagnoses** (tightened regex over `final_diagnosis` after splitting CamelCase and underscores; hand-checked lists, approximate):
| group | cases (test) | examples |
|---|---|---|
| nutritional deficiency / excess | 58 (6) | scurvy (9, test 2), thiamine deficiency / Wernicke / beriberi, pellagra, B12 and vitamin D deficiency, kwashiorkor, copper deficiency, hypervitaminosis D, milk–alkali syndrome, refeeding syndrome. A few are genetic (cobalamin C defect, hypophosphatemic rickets). |
| food-, water- or faecal–oral-borne infections and parasites | 230 (11) | brucellosis (unpasteurised dairy), echinococcosis, cysticercosis, toxoplasmosis, typhoid, listeriosis, botulism (incl. a stale fried gram-flour snack), fascioliasis, paragonimiasis, anisakiasis, hepatitis E. Not all are strictly food-borne. |
| toxic ingestion of a food, plant, herb or supplement | 18 (0) | liquorice intoxication / pseudoaldosteronism, star fruit intoxication, aconite/aconitine poisoning, kratom liver injury / toxicity / hyperpigmentation, scombrotoxinism, ricin, shiitake dermatitis, ergotism, homeopathy- and Xenadrine-induced injury, oxalate nephropathy |
| food allergy / intolerance | 29 (3) | coeliac disease, alpha-gal syndrome, food-dependent exercise-induced anaphylaxis, FPIES, cow's milk protein allergy, eosinophilic oesophagitis |
| ingested food body | 8 (0) | fish-bone perforation, phytobezoar, lactobezoar |
| **any** | **~343 (20)** | |

- **Food–drug / herb–drug.** No gold label names an interaction. But 14 cases mention liquorice, tyramine, grapefruit or St John's wort in the prompt or reasoning (test 2).
- **Herb or supplement plus injury.** 81 prompts mention a herbal product or supplement and have an injury- or syndrome-type diagnosis (noisy regex). Clear cases include Sai-rei-to lung injury (test), kratom DILI, and insulin autoimmune syndrome after "fat-burner" supplements (test).
- **Hidden exposures.** In several food-caused cases the o4-mini information cutoff **removes the dietary exposure from `case_prompt`**; it appears only in `text` and often in the reasoning. Examples:
  - star fruit, PMC6977387;
  - licorice root, PMC4624913;
  - aconite remedy, PMC5419964;
  - liquorice sweets, PMC8349066.

  These are hard "think of the diet" cases, and the model must say that it would take a diet history.
- **diet_relevance: subset.** About 2.4% of cases have a food-related gold diagnosis and ~9% mention diet or supplements.

**Ten most relevant cases for a food/herb/supplement–drug test set** (our selection):
| pmcid (split) | case in one line | gold `final_diagnosis` |
|---|---|---|
| PMC7527885 (train) | 45 M on amlodipine + perindopril, drinks alcohol-free "pastis" daily; K⁺ 1.65, BP 240/120, torsades | Liquorice intoxication |
| PMC8349066 (train) | 79 F on lercanidipine and escalating antihypertensives + K⁺ supplements; K⁺ 2.2, alkalosis, low renin. Liquorice sweets appear only in the reasoning. | Apparent mineralocorticoid excess |
| PMC4624913 (train) | 15 F, K⁺ 1.8, pH 7.6, QT 600 ms, low renin and aldosterone; licorice root not in prompt | Pseudoaldosteronism |
| PMC5419964 (train) | 62 M Hmong, shock, bidirectional VT, hypokalaemia; herbal remedy not in prompt | Aconitine poisoning |
| PMC6831833 (test) | 88 M, CKD; fever, hypoxaemia and ground-glass opacities 2 weeks after starting Kampo Sai-rei-to | Drug-induced lung injury (Sai-rei-to) |
| PMC7643221 (train) | 37 F with depression and obesity; jaundice, ALP 672, ALT 578 after a kratom-containing herbal supplement | Kratom-induced liver injury |
| PMC6977387 (train) | 51 M, acute neuro deficit + AKI → anuria, normal imaging and CSF; star fruit not in prompt | Star fruit intoxication |
| PMC7238301 (train) | 61 M, Ca 11.1 mg/dL after six calcium-carbonate (Tums) tablets the evening before | Milk–alkali syndrome |
| PMC10448237 (train) | 70 M, hunter with tick bites; urticaria after repaglinide, simethicone and sausages, assumed to be drug allergy | Alpha-gal syndrome |
| PMC6930746 (test) | 25 M bodybuilder (anabolic steroids, oral amino acids, "fat-burner" supplements); hypoglycaemia, insulin > 301, anti-insulin antibodies | Insulin autoimmune syndrome |

Other test-set food cases: PMC3355033 anisakiasis (anchovies 48 h earlier), PMC11126872 and PMC6180829 scurvy, PMC4808700 shiitake dermatitis, PMC2740089 cow's-milk protein allergy, PMC6307248 *Listeria* rhombencephalitis. PMC10445075 is a negative control: hepatitis after a watercress–garlic–ginger "green juice", with the gold "acute hepatitis of unknown origin".

## Linking to the vault's KG
- **Diagnoses → `condition`.**
  - After lower-casing, splitting CamelCase and replacing `_`, **7,582 / 14,489 cases (52.3%; test 438 / 897) match a `condition.name` or English `condition_alias` exactly**. That is 2,267 of 7,383 distinct labels.
  - Examples: scurvy → `MESH:D012614`, pellagra → `MESH:D010383`, brucellosis → `MESH:D002006`, anisakiasis → `MESH:D017129`, alpha-gal syndrome → `MESH:C000655084`, milk-alkali syndrome → `MESH:D006934`, pseudoaldosteronism → `MESH:D056929`, drug-induced liver injury → `MESH:D056486`.
  - Unmatched are long compound labels ("Kratom-induced liver injury", "Star fruit intoxication"). They need a UMLS / MeSH entry-term lookup, or an LLM normaliser to MeSH.
- **Exposures → `ingredient` / `drug`.**
  - Licorice, star fruit, grapefruit, shiitake and anchovy exist as ingredients.
  - `ING:licorice` has a direct `harmful` link to hypertension (SpiceRx) and [[DDID]] `Possible` interactions with amlodipine, felodipine, furosemide and hydrochlorothiazide. That is exactly the PMC7527885 setting.
  - But there is no direct licorice → pseudo-hyperaldosteronism / hypokalaemia edge: hypokalaemia appears only as a CTD `marker` via compounds. This is a gap a case-based test would expose.
  - Star fruit reaches acute kidney injury only through CTD compound paths.
- **Evaluation design.** For the food subset, compare the model with and without our KG context on:
  - diagnostic accuracy (LLM judge, as in the paper);
  - whether the reasoning raises the dietary or herbal exposure.

  Cases with a hidden exposure test whether KG hints such as "glycyrrhizin → mineralocorticoid excess" lead the model to the right question.

## Versions
- **Hugging Face** `zou-lab/MedCaseReasoning`: created 2025-05-16, last modified 2025-06-02 (revision 469a536), the only release. It has three splits plus the duplicate core CSV/PQT.
- **Paper:** arXiv v1 2025-05-16, v2 2025-05-20. The GitHub README cites it as "NeurIPS 2025", but OpenReview lists it as a *withdrawn ICLR 2026 submission*, and no proceedings version was found. Treat it as a preprint.
- The pipeline (PMC OA, Jan 2005 – Apr 2025) is designed to be re-run for newer case reports; no newer release exists.

## Caveats
- **Licence ambiguity:** MIT (HF card) vs CC BY 4.0 (GitHub README). Both allow redistribution, so the samples are committed. The `text` column holds full PMC OA articles, some of which are CC BY-NC(-ND); keep commercial use in mind.
- **LLM-made inputs and labels:** prompts, reasoning lists and diagnoses were written by o4-mini and filtered by gemini-2.5-pro. Only 100 cases were physician-checked (92% of diagnoses faithful and inferable).
- **Leakage and contamination:** `text` contains the answer, so never feed it to the model. Case reports are public and many predate model cutoffs.
- **Label format noise:** 19 labels use underscores (`Scleroderma_renal_crisis`, 3 in test). Several have spaces removed (`AmeloblasticFibroma`, `InsulinAutoimmuneSyndrome`). Synonyms are not unified (Celiac / Coeliac / CeliacDisease). An LLM judge or normaliser is needed.
- **Rare-disease bias:** case reports favour unusual presentations, so prevalence is far from clinical reality.
- **Hidden exposures** (see above) make some food cases unanswerable without asking for a diet history.
- **No geography field:** country counts are regex estimates.
