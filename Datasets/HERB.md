---
title: "HERB"
slug: herb
kind: [ingredient, compound]
version: "2.0 (NAR 2025 database issue)"
previous_versions: "1.0 (Fang et al., NAR 2021; 7,263 herbs, 49,258 ingredients, 12,933 targets, 28,212 diseases, 1,037 experiments, 1,966 references)"
papers: ["[[Gao2025 - HERB 2.0 clinical and experimental evidence for TCM]]"]
url: "http://herb.ac.cn/v2"
license: "not stated on the site"
availability: open-download
access_link: "http://47.92.70.12/download/file/?file_path=/www/wwwroot/47.92.70.12/HERB_web/static/download_data/V2/HERB_herb_info_v2.txt"
accessed: true
access_method: [website-download, api]
access_date: 2026-09-30
access_notes: "herb.ac.cn/v2 redirects to http://47.92.70.12 (React app). The Download page's files come from GET /download/file/?file_path=<server path>. All 9 v2 files downloaded (herb, ingredient, formula, target, disease, meta-analysis, clinical trial, reference, experiment; 92 MB). The download has NO association tables (herb–ingredient, ingredient–target, herb–disease). We pulled those for 6 medicine-food herbs from the JSON API (POST /chedi/api/ with func_name=detail_api, key_id=<HERB id>, label=Herb; 6 requests). Server is slow (a 40 MB JS bundle) but no registration."
countries: ["[[China]]"]
regions: ["[[East Asia]]"]
n_records: "6,892 herbs · 44,595 ingredients · 6,743 formulae · 15,515 targets · 30,170 diseases · 8,558 clinical trials · 8,032 meta-analyses · 6,705 references · 2,231 high-throughput experiments"
size: "92 MB (9 TSV) + 0.9 MB scraped JSON"
formats: [tsv, json, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Clinical-trial (ClinicalTrials.gov) and meta-analysis (PROSPERO) records per herb/ingredient/formula with conditions and, for 1,941 trials, curated conclusions; herb Function/Indication text (TCM claims); literature-curated targets/diseases; transcriptomic experiments; inferred herb–target/disease (P, FDR) on the web."
join_keys: [PubChem CID, InChIKey, CAS, SymMap id, TCMSP id, TCMID id, TCM-ID id, DrugBank id, NPASS id, HIT id, NCT id, PROSPERO CRD id, PubMed id, UMLS CUI, MeSH id, ICD-10, OMIM, DO id, HPO id, Entrez gene id, Ensembl gene id, HGNC id, TTD id]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients, search/compounds]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
---
# HERB

> [!abstract] TL;DR
> HERB 2.0 (Beijing University of Chinese Medicine and ICT-CAS, the same group as [[SymMap]]; Gao et al., NAR 2025) is a TCM database built around
> **evidence**. It covers **6,892 herbs, 44,595 ingredients and 6,743 formulae**, plus **8,558 clinical trials**
> (ClinicalTrials.gov) and **8,032 meta-analyses** (PROSPERO), filtered with LLMs and manual curation. It also
> has 6,705 curated references and 2,231 re-analysed transcriptomic experiments. The "herbs" include many
> **everyday foods** (green tea, olive, peanut, pomegranate, cocoa, garlic, tomato, cinnamon, pistachio), so it
> directly answers "is there trial evidence that food X / compound Y affects condition Z" (Q3).

## Access
| | |
|---|---|
| Availability | open download (entity + evidence tables); relations via web/JSON API |
| Link | http://herb.ac.cn/v2 → http://47.92.70.12 (Download page) |
| Accessed? | yes: all 9 v2 tables; herb detail JSON for 6 herbs |
| How | `curl "http://47.92.70.12/download/file/?file_path=/www/wwwroot/47.92.70.12/HERB_web/static/download_data/V2/<file>"`; `POST /chedi/api/` JSON `{"func_name":"detail_api","key_id":"HERB005017","label":"Herb"}` |
| Downloaded | `Data/herb/HERB_*_v2.txt` (TSV, 92 MB); `Data/herb/scrape/herb_detail_<id>.json` + flattened CSVs |

Scraped herbs: 生姜 Sheng Jiang fresh ginger (HERB005017), 干姜 Gan Jiang dried ginger (HERB001787), 大枣 Da Zao
jujube (HERB001164), 枸杞子 Gou Qi Zi goji (HERB001915), 肉桂 Rou Gui cassia bark (HERB004694), 姜黄 Jiang Huang
turmeric (HERB002840). The v1 files are also on the server (`…/download_data/V1/…_v1.txt`) but were not downloaded.

## Tables & columns
Missing values are the string `NA`. Multi-valued fields use `; ` or `|`.

### `HERB_herb_info_v2.txt` (6,892 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Herb_id` | str | HERB herb id | HERB005017 |
| `Herb_pinyin_name`, `Herb_cn_name`, `Herb_alias_name` | str | names | Sheng Jiang, 生姜, 姜根; 鲜生姜… |
| `Herb_en_name`, `Herb_latin_name` | str | English and Latin names | Fresh Ginger; Zingiberis Rhizoma Recens |
| `Properties`, `Meridians` | str | TCM nature/flavour, meridians (35% / 26%) | Pungent; Slightly Warm |
| `UsePart` | str | part used (48%) | Fresh rhizome |
| `Function` | str | TCM function (52%) | To induce perspiration and dispel cold, to warm the stomach and arrest vomiting… |
| `Indication` | str | indications (51%) | Wind-cold common cold…, vomiting, phlegm-rheum cough asthma… |
| `Toxicity`, `Clinical_manifestations` | str | toxicity; modern pharmacology notes (5%) | 1. oral administration can stimulate the … gastric mucosa… |
| `Therapeutic_en_class`, `Therapeutic_cn_class` | str | TCM therapeutic class (13%) | Pungent-Warm Exterior-Releasing Medicinal |
| `SymMap_id`, `TCMID_id`, `TCMSP_id`, `TCM_ID_id` | id | cross-references | SMHB00367 |

### `HERB_ingredient_info_v2.txt` (44,595 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Ingredient_id` | str | HERB ingredient id | HBIN012366 |
| `Ingredient_name`, `Ingredient_alias_name` | str | name and synonyms | 6-gingerol; gingerol; 23513-14-6… |
| `Molecular_formula`, `Canonical_smiles`, `Isomeric_smiles`, `InChI`, `InChIKey` | str | structure (SMILES 69%) | NLDDIKRKFXEWBK-AWEZNQCLSA-N |
| `MolWt`, `NumHAcceptors`, `NumHDonors`, `MolLogP`, `NumRotatableBonds` | num | RDKit descriptors (inferred) | 294.391 |
| `Drug_likeness`, `OB_score` | num | drug-likeness; oral bioavailability (%) | 0.65; 35.6 |
| `CAS_id`, `SymMap_id`, `TCMID_id`, `TCMSP_id`, `TCM_ID_id`, `PubChem_id`, `DrugBank_id`, `NPASS_id`, `HIT_id` | id | cross-references | PubChem 442793; NPASS NPC20287 |

### `HERB_formula_info_v2.txt` (6,743 rows, new in 2.0)
`Formula_id` (HBFO…), `Formula_pinyin_name`, `Formula_cn_name`, `Formula_en_name`, `Dosage_form`,
`Administration`, `Type`/`Category` (TCM class, e.g. 补益药 tonics 749), `Herbs_in_Chinese`/`Herbs_in_pinyin`
(composition, **no amounts**), `Syndromes_in_Chinese/English`, `Indications_in_Chinese/English` (e.g.
"Dysmenorrhea, Menstrual irregularities"), `Source` (ETCM 3,297; Chinese Pharmacopoeia 2020 1,595; ITCM 1,255;
CPMCP 428; ancient classic prescriptions 168), `CPMCP_*_id`, `ITCM_id`, `ETCM_id`.

### `HERB_clinical_trials_v2.txt` (8,558 rows, new in 2.0)
| column | type | meaning | example |
|---|---|---|---|
| `Clinical_trial_id` | str | HERB trial id | HBCT000001 |
| `Subject_id`, `Subject_name`, `Subject_type` | str | the herb/ingredient/formula studied (Ingredient 6,938 · Herb 1,536 · Formula 84) | HERB004694 · Rou Gui; 肉桂; Cassia Bark… · Herb |
| `NCT_id`, `NCT_title`, `URL` | str | ClinicalTrials.gov record | NCT00445354 · Randomized Controlled Clinical Trial of Cinnamon to Lower Hemoglobin A1c |
| `Study_condition` | str | condition(s), `\|`-separated | Diabetes |
| `Status`, `Phase `, `Study_result` | str | status; phase (note the trailing space in the column name); whether results were posted (Yes 1,707) | Completed · Phase 3 |
| `Study_type`, `Study_design`, `Intervention*`, `Gender`, `Age`, `Enrollment`, `Outcome_measure` | | design fields | Interventional · Randomized · Double |
| `Sponsor_collaborator`, `Funded_by`, `Location`, dates, `Study_document` | | administrative | |

The web version adds curated `Result`/`Conclusion`, `Side effect`, `Place of Origin`, `Processing method`
and `PubMed id` for 1,941 trials (see `scrape/clinical_herb.csv`). These fields are **not** in the download file.

### `HERB_meta_info_v2.txt` (8,032 rows, new in 2.0)
`Meta-analysis_id` (HBMA…), `Subject_id/name/type` (Ingredient 5,850 · Formula 1,240 · Herb 942), `CRD_id`
(PROSPERO), `CRD_title`, `Review_question`, `Condition_being_studied`, `Participant`, `Intervention`,
`Comparator_control`, `Main_outcome`, `Outcome_measure`, `Country` (registrant country), `Review_stage`, dates,
and 15 more PROSPERO fields.

### `HERB_target_info_v2.txt` (15,515) · `HERB_disease_info_v2.txt` (30,170)
Targets: `Target_id` (HBTAR…), `Gene_symbol`, `Protein_name`, `Type_of_gene`, `TTD_target_type`, `Organism`,
`Entrez_id`, `OMIM_id`, `HGNC_id`, `Ensembl_id`, `MGI_id`, `TTD_id`. Diseases: `Disease_id` (HBDIS…),
`Disease_name`, `Disease_alias_name`, `DisGeNET_disease_type`, `UMLS_disease_type`, `MeSH_disease_class`,
`HPO_disease_class`, `DO_disease_class`, `DisGeNET_id` (UMLS CUI), `MeSH_id`, `HPO_id`, `DO_id`, `ICD10_id`,
`OMIM_id`.

### `HERB_reference_info_v2.txt` (6,705) · `HERB_experiment_info_v2.txt` (2,231)
References: `Reference_id`, `PubMed_id`, `Subject_id/name/type`, `Paper_title`, `Paper_abstract`, `Journal`,
`DOI`, `Experiment_subject`, `Experiment_type`, `Phenotype_related`. Experiments: GEO-derived (`GSE_id`,
`Organism`, `Experiment_type`, `Control_*`, `Treatment_samples`, `Platform`, `Tissue`, `Cell_line`…) for
herbs/ingredients/formulae/diseases.

### Scraped: `scrape/*.csv` (6 herbs)
| file | rows | content |
|---|---|---|
| `herb_ingredient.csv` | 1,597 | herb → `Ingredient id`, `Ingredient name`, formula, SMILES (ginger 466, goji 296, dried ginger 251, jujube 229, cinnamon 209, turmeric 146) |
| `formula_herb.csv` | 1,552 | formulae containing the herb |
| `herb_target.csv` | 143 | herb → target with `P value`, `FDR BH` |
| `clinical_herb.csv` | 46 | trials with curated `Result`, `Conclusion`, `Side effect`, `Place of Origin` (turmeric 32, cinnamon 14) |
| `drug_paper_target.csv`, `meta_herb.csv`, `herb_disease.csv` | 13 / 8 / 8 | literature-curated targets, meta-analyses, diseases |

Sample: `Data/herb/sample.csv` · full profile: `Data/herb/schema.md`

## Countries & cultures covered
- **[[China]]**: the herb, formula and TCM-property layers are Chinese (Chinese Pharmacopoeia 2020, CFDA patent
  medicines, national classic prescriptions, TCMID/TCMSP/SymMap).
- The **evidence layer is global**. The paper reports trials registered from 119 countries and meta-analyses from
  81 countries. Meta-analysis `Country` counts (single-country values): China 2,981 · Brazil 625 · **Iran 577** ·
  United States 371 · **India 321** · England 316 · Australia 256 · Canada 164 · Italy 119 · **Indonesia 95** ·
  **Taiwan 90** · **South Korea 90** (+3 "Korea, South") · **Thailand 73** · **Malaysia 65** · **Saudi Arabia 49** ·
  **Japan 47** · **Egypt 38** · **Pakistan 36** · Turkey 16 · Qatar 14 · Jordan 8 · Lebanon 7 · United Arab
  Emirates 6 · Vietnam 5 · Kuwait 2 · Bahrain 2 · Iraq 2 · Oman 1 · Bangladesh 1. Trial `Location` is free
  text (top: United States, China, Canada, United Kingdom, Egypt, Germany, Turkey…).
  These are *where the evidence was produced*, not cultural usage, so only China is in `countries`.
- **Medicine-food homology is not flagged** (no food field). In practice the herb list mixes TCM materia medica
  with foods, and the trial table shows it. The most-trialled herb subjects are Cannabis Sativa 117, Green Tea 67,
  Common Olive 64, Peanut 51, Ginkgo Leaf 45, Pomegranate 42, Sucrose 39, Honey 38, Cocoa 38, Linseed 38,
  Turmeric 32, Garlic 26, Cow Milk 25, Tomato 18, Cassia Bark (cinnamon) 14, Pistachio 11, Oat 10, Saffron 10.

## Inferring effects on the body
`body_effect: direct`. Evidence types, from strongest to weakest:
1. **Clinical trial / meta-analysis**: subject (herb/ingredient/formula) → `Study_condition`/`Condition_being_studied`,
   with design and phase. Curated conclusions exist for 1,941 trials and 593 meta-analyses (web/JSON only).
2. **Literature-curated** targets and diseases (`drug_paper_target`, `drug_paper_disease`, `HERB_reference_info`).
3. **Traditional claim**: `Function` / `Indication` text for about half of the herbs.
4. **Transcriptomic / inferred**: GEO experiments, CMap-style connectivity scores, and herb–target/disease
   P-values inferred through ingredients.

Example chains:
- **Cinnamon, Rou Gui 肉桂 (HERB004694)** → ingredient **cinnamaldehyde** (HBIN020653, one of 209) → trial
  NCT00445354 (Phase 3, *Diabetes*). Curated result: "Cinnamon lowered HbA1C 0.83% (95% CI, 0.46–1.20)
  compared with usual care alone lowering HbA1C 0.37%". Other cinnamon trials are for obesity, prediabetes,
  metabolic syndrome ("3 g cinnamon for 16 weeks… significant improvements in all components of metabolic
  syndrome in… Asian Indians") and gastric emptying (no effect).
- **Fresh ginger, Sheng Jiang 生姜 (HERB005017)**: Function "warm the stomach and arrest vomiting" → ingredient
  **6-gingerol** (HBIN012366, PubChem 442793, InChIKey NLDDIKRKFXEWBK-AWEZNQCLSA-N) → meta-analysis
  CRD42022334940 "Anticancer effects of gingerol, shogaol and curcumin in cervical cancer" (Malaysia) → target
  TNF (herb-level P = 8.1e-10).

## Linking to other datasets
- `SymMap_id` ↔ [[SymMap]] (`HERBDB_ID`); `TCMSP_id`/`TCMID_id` ↔ other TCM databases.
- `PubChem_id`, `InChIKey`, `CAS_id` → [[TM-MC]], [[FooDB]], [[IMPPAT]], [[CTD]]; `DrugBank_id` → [[DrugBank]];
  `NPASS_id` → NPASS bioactivities.
- `NCT_id` → ClinicalTrials.gov; `CRD_id` → PROSPERO; `PubMed_id` → literature.
- Disease `DisGeNET_id` (UMLS CUI), `MeSH_id`, `ICD10_id`, `DO_id` → [[CTD]], [[TM-MC]] `DISEASEID` (DisGeNET
  CUIs), [[SymMap]] `UMLS_id`.
- Herb English names ("Green Tea", "Common Olive", "Pomegranate Fruit") → food-dataset ingredient names
  ([[FooDB]], [[USDA FoodData Central]]). Needs fuzzy matching.

## Versions
| | herbs | ingredients | formulae | targets | diseases | trials | meta-analyses | experiments | references |
|---|---|---|---|---|---|---|---|---|---|
| 1.0 (NAR 2021) | 7,263 | 49,258 | – | 12,933 | 28,212 | – | – | 1,037 | 1,966 |
| **2.0** (NAR 2025) | **6,892** | **44,595** | **6,743** | **15,515** | **30,170** | **8,558** | **8,032** | **2,231** | **6,705** (paper: 6,644) |

2.0 removed redundant herbs and ingredients (counts went down). It added formulae, clinical trials, meta-analyses,
disease transcriptomes (CREEDS/GEO, 376 diseases), a gene-expression upload/mapping tool and a Neo4j knowledge graph
(9 entity types, 28 relation types).

## Caveats
- The downloads contain no herb–ingredient, ingredient–target or subject–disease association tables. Building a
  KG needs the JSON API (`detail_api` per entity; ~6,900 herbs) or the knowledge-graph page.
- Trial/meta-analysis matching started from keyword search. The LLM filter had 51.3% accuracy on a manually
  labelled set (98.6% of errors were false positives), so everything the LLMs flagged was manually checked, but
  false negatives (missed trials) remain.
- Curated conclusions exist for only 22.7% of trials and 7.4% of meta-analyses, and are not in the TSV.
- `Subject_name` in trial/meta tables is a long `;`-joined alias string (the first element is the name).
- The server is a bare IP (47.92.70.12) with no HTTPS; the download path may change.
- No licence statement was found on the site.
