---
title: "Exposome-Explorer"
slug: exposome-explorer
kind: [compound]
version: "4.0 (October 2025; download files dated 2025-10-26)"
previous_versions: "1.0 (Feb 2017, NAR gkw980); 2.0 (Sep 2019, NAR gkz1009); 3.0 (Mar 2021, gut microbial metabolites, Sci Rep 2023)"
papers: ["[[Neveu2020 - Exposome-Explorer 2.0]]"]
url: "http://exposome-explorer.iarc.fr/"
license: "© IARC/WHO, all rights reserved (IARC copyright page); free to download, no explicit open licence; the 2.0 paper is CC BY 3.0 IGO"
availability: open-download
access_link: "http://exposome-explorer.iarc.fr/downloads"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "All 10 CSV zips on the Downloads page fetched with curl (no login). The downloads are the curated data tables; the web pages also show classification trees (foods, compounds, cancers, biospecimens) and per-food intake pages that have no bulk file. The cancer-association download lists which biomarker–cancer pairs each study tested but carries no effect sizes (RR/OR, direction). The paper says to follow the publication links for those."
countries: ["[[United States]]", "[[Japan]]", "[[China]]", "[[Germany]]", "[[France]]", "[[Sweden]]", "[[Norway]]", "[[Spain]]", "[[Netherlands]]", "[[Denmark]]", "[[United Kingdom]]", "[[Costa Rica]]", "[[South Korea]]", "[[Canada]]", "[[Finland]]", "[[Italy]]", "[[Australia]]", "[[Belgium]]", "[[Taiwan]]", "[[Mexico]]", "[[Czech Republic]]", "[[Slovakia]]", "[[Switzerland]]", "[[Iran]]", "[[Faroe Islands]]", "[[Poland]]", "[[Latvia]]", "[[Luxembourg]]", "[[Russia]]", "[[Peru]]", "[[New Zealand]]", "[[Puerto Rico]]", "[[Greece]]", "[[Israel]]", "[[Singapore]]", "[[Thailand]]", "[[Romania]]", "[[India]]", "[[Egypt]]", "[[Bolivia]]", "[[Vietnam]]", "[[Malaysia]]", "[[Kuwait]]", "[[Ireland]]", "[[Benin]]", "[[Tunisia]]", "[[Turkey]]", "[[Slovenia]]", "[[Brazil]]", "[[Ukraine]]", "[[Croatia]]", "[[Guernsey]]", "[[Argentina]]", "[[Gambia]]"]
regions: ["[[Europe]]", "[[North America]]", "[[East Asia]]", "[[Southeast Asia]]", "[[South Asia]]", "[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "1,841 biomarkers · 13,676 concentration values · 8,898 biomarker–intake correlations · 1,356 biomarker–cancer associations · 415 metabolomic food-intake associations · 3,060 reproducibility values · 1,848 microbiota evidence rows · 1,113 publications"
size: "9 MB (10 CSV)"
formats: [csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "cancer_associations: biomarker measured in blood/urine → cancer site tested in prospective cohort / nested case-control studies (no effect size in the download); correlations + metabolomic_associations: food or nutrient intake → biomarker level in human biospecimens (correlation r, p, AUC). This gives a human-evidence chain food → compound in the body → cancer."
join_keys: [PubChem CID, InChIKey, HMDB id, FooDB id, ChEBI id, CAS RN, PubMed id, cohort name]
topics: [cultural-food-health]
questions: [Q3]
relevance: core
found_by: [search/compounds]
tags:
  - type/dataset
  - kind/compound
  - q/3
  - access/accessed
  - access/open
---
# Exposome-Explorer

> [!abstract] TL;DR
> Exposome-Explorer (IARC/WHO, Lyon, built with the Wishart lab) is a manually curated database of **biomarkers of
> diet and pollution measured in human populations**, taken from 1,113 publications. For 1,841 biomarkers it gives
> concentrations in blood and urine per population and country, correlations with food intake (FFQ, recalls,
> records), candidate food biomarkers from metabolomics, reproducibility over time, and 1,356 biomarker–cancer
> associations from prospective cohorts. Release 4.0 (Oct 2025) added environmental pollutants. For the agent this is
> the **human-evidence** layer of a food → compound → disease chain, which lab-heavy [[CTD]] lacks. Asian cohorts
> (Shanghai, JPHC Japan, Korea, Taiwan) are well represented. The Middle East appears only through Iran (Golestan),
> Israel, Kuwait, Egypt, Tunisia and Turkey, with few rows, and Central Asia is absent.

## Access
| | |
|---|---|
| Availability | open-download (CSV zips; © IARC, no explicit licence) |
| Link | http://exposome-explorer.iarc.fr/downloads |
| Accessed? | yes: all 10 download files |
| How | `curl -L http://exposome-explorer.iarc.fr/system/downloads/current/<name>.csv.zip` + unzip |
| Downloaded | `Data/exposome-explorer/*.csv` (10 files, 9 MB) |

## Tables & columns
Meanings come from the web table headers and the 2.0 paper; items marked (inferred) are our reading of the data.

### `biomarkers.csv` (1,841 rows × 24) — compound dictionary
| column | type | meaning | example |
|---|---|---|---|
| `ID`, `Name` | int, str | biomarker id and name | `1792`, `Epigallocatechin 3-gallate` |
| `Classification` | str | IARC exposure-based class | `Isoflavones` |
| `Synonyms`, `Description` | str | synonyms; free text | `Metabolite of daidzein.` |
| `Level` | str | `Single` compound (1,500), `Combined` sum (324), `Ratio` (12)… | `Single` |
| `CAS Number`, `PubChem ID`, `ChEBI ID`, `FooDB ID`, `HMDB ID` | str/float | cross-references (PubChem 52%, HMDB 34%, FooDB 32% filled) | `65064`, `HMDB0003153`, `FDB017702` |
| `SMILES`, `Formula`, `InChI`, `InChIKey`, `Average mass`, `Mono. mass` | str/float | structure | `WMBWREPUVVBILR-WIYYLYMNSA-N` |
| `No. of Publications` … `No. of Cancer associations` | int | counts of linked records by type | `2` |

### `correlations.csv` (8,898 rows × 38) — biomarker level vs dietary intake
| column | type | meaning | example |
|---|---|---|---|
| `Intake ID`, `Excretion ID` | int | ids of the intake and biomarker measurements | `25` |
| `Subject group`, `Population`, `Country`, `Cohort` | str | who was studied, and where | `France`, `EPIC` |
| `Intake Assessment method` | str | FFQ (4,942 rows), 24-h recall, dietary record… | `Food Frequency Questionnaire (FFQ)` |
| `Intake`, `Intake detail` | str | food or nutrient (277 distinct: `Tea`, `Black tea`, `Fruits`, `Genistein`…) | `Tea` |
| `Intake Arithmetic mean` … `Intake Unit` | float/str | intake level | `mg/day` |
| `Biospecimen`, `Analytical method` | str | e.g. `Urine, 24-h`; `LC-MS` | `Urine, 24-h` |
| `Biomarker`, `Biomarker detail`, `Biomarker … mean/median/Unit` | str/float | biomarker and its level | `4-O-Methylgallic acid` |
| `Correlation size`, `Correlation type`, `Correlation value`, CI, `Correlation p-value`, `Significant?` | mixed | n, Pearson/Spearman r, p | `476`, `0.55`, `= 2.86e-2` |
| `Measurement adjustment`, `Deattenuated?`, `Covariates`, `Publication` | str | statistics details; short citation | `Edmands 2015` |

### `cancer_associations.csv` (1,356 rows × 16) — biomarker ↔ cancer risk studies
| column | type | meaning | example |
|---|---|---|---|
| `Excretion ID` | int | biomarker measurement id | `21004` |
| `Population`, `Country`, `Cohort` | str | 18 countries, 71 cohorts | `Japan`, `JPHC …` |
| `No. of subjects`, `No. of cases`, `No. of controls` | int | study size | `144` cases |
| `Biospecimen`, `Analytical method` | str | e.g. `Plasma, fasting…`, `HPLC` | |
| `Biomarker`, `Biomarker detail` | str | 132 distinct (carotenoids, tocopherols, folates, fatty acids, polyphenols) | `Epigallocatechin 3-gallate` |
| `Cancer` | str | ICD-10-grouped site (17): breast 452, prostate 255, colorectal 196, gastric/oesophageal 93… | `Breast cancer` |
| `Study design`, `Publication` | str | nested case-control / prospective cohort / case-cohort | `Iwasaki 2010` |

### `metabolomic_associations.csv` (415 × 24) — candidate food-intake biomarkers from metabolomics
`Intake` (56 foods, e.g. `Citrus fruits`, `Red meat`), `Intervention dose`, `Biomarker` (217), `Biospecimen`,
`Analytical method`, `Structural identification`, `Feature selection`, `Area under curve`, `Sensitivity`,
`Specificity`, `PLS-DA VIP`, `Beta coefficient`, p-values, `Country` (8), `Cohort`, `Publication`.
Example: citrus fruits → proline betaine (urine).

### `concentrations.csv` (13,676 × 45) — biomarker concentrations in human biospecimens
`Population`, `Country` (51), `Cohort`, `Biospecimen` (68), `Analytical method`, `Biomarker` (1,045), sample size and
detection rate, arithmetic/geometric mean, SD, percentiles, min/max, `Unit`, `Converted …` (harmonised units),
`Adjustment type`, `Adjusted on` (creatinine, lipids…), `Publication`. Hierarchical rows (`Parent ID`, `Depth`) split a
population into subgroups.

### Other tables
- `reproducibilities.csv` (3,060 × 25): within-person ICC and CV over time for a biomarker (how well one sample reflects habitual intake).
- `microbial_metabolites.csv` (457 × 22) + `microbial_metabolite_identifications.csv` (1,848 × 9): gut-microbial
  origin evidence (produced by faecal bacteria / reduced by antibiotics / reduced in germ-free animals, with substrate, e.g. daidzein → equol).
- `environmental_pollutants.csv` (313 × 19): pollutant dictionary (new in 4.0).
- `publications.csv` (1,113 × 20): `PubMed ID`, `DOI`, `Study design` (observation 550, nested case-control 264…), counts per data type.

Sample: `Data/exposome-explorer/sample.csv` (+ `sample_*_csv.csv`) · full profile: `Data/exposome-explorer/schema.md`

## Countries & cultures covered
Countries of the study populations, counted as data rows across concentrations / correlations / reproducibilities /
cancer_associations / metabolomic_associations (54 countries or territories). We normalised the names: Czechia →
Czech Republic, Türkiye → Turkey, Russian Federation → Russia. Faroe Islands, Puerto Rico and Guernsey are
territories.

| country | conc. | corr. | repro. | cancer | metabol. | total |
|---|---|---|---|---|---|---|
| United States | 3070 | 2932 | 920 | 471 | 160 | 7553 |
| Japan | 1571 | 611 | 82 | 87 | 0 | 2351 |
| China | 1308 | 154 | 438 | 100 | 0 | 2000 |
| Germany | 640 | 87 | 907 | 10 | 0 | 1644 |
| France | 261 | 817 | 0 | 126 | 69 | 1273 |
| Sweden | 407 | 732 | 28 | 61 | 6 | 1234 |
| Norway | 478 | 610 | 65 | 30 | 0 | 1183 |
| Spain | 688 | 231 | 63 | 0 | 39 | 1021 |
| Netherlands | 303 | 350 | 130 | 54 | 0 | 837 |
| Denmark | 311 | 384 | 53 | 28 | 26 | 802 |
| United Kingdom | 124 | 458 | 5 | 110 | 98 | 795 |
| Costa Rica | 212 | 577 | 0 | 0 | 0 | 789 |
| South Korea | 616 | 37 | 88 | 8 | 0 | 749 |
| Canada | 583 | 154 | 0 | 3 | 0 | 740 |
| Finland | 207 | 212 | 6 | 140 | 5 | 570 |
| Italy | 471 | 19 | 0 | 33 | 0 | 523 |
| Australia | 226 | 165 | 0 | 80 | 0 | 471 |
| Belgium | 248 | 0 | 187 | 0 | 0 | 435 |
| Taiwan | 378 | 2 | 0 | 1 | 0 | 381 |
| Mexico | 148 | 52 | 17 | 0 | 0 | 217 |
| Czech Republic | 202 | 0 | 0 | 0 | 0 | 202 |
| Slovakia | 166 | 0 | 0 | 0 | 0 | 166 |
| Switzerland | 146 | 12 | 0 | 0 | 0 | 158 |
| Iran | 14 | 124 | 0 | 0 | 0 | 138 |
| Faroe Islands | 122 | 0 | 0 | 0 | 0 | 122 |
| Poland | 104 | 0 | 13 | 0 | 0 | 117 |
| Latvia | 2 | 112 | 0 | 0 | 0 | 114 |
| Luxembourg | 68 | 0 | 28 | 0 | 0 | 96 |
| Russia | 87 | 0 | 0 | 0 | 0 | 87 |
| Peru | 77 | 0 | 0 | 0 | 0 | 77 |
| New Zealand | 62 | 9 | 0 | 0 | 0 | 71 |
| Puerto Rico | 29 | 0 | 30 | 0 | 0 | 59 |
| Greece | 36 | 11 | 0 | 0 | 0 | 47 |
| Israel | 14 | 28 | 0 | 0 | 0 | 42 |
| Singapore | 25 | 0 | 0 | 11 | 0 | 36 |
| Thailand | 33 | 0 | 0 | 0 | 0 | 33 |
| Romania | 30 | 0 | 0 | 0 | 0 | 30 |
| India | 26 | 0 | 0 | 0 | 0 | 26 |
| Egypt | 26 | 0 | 0 | 0 | 0 | 26 |
| Bolivia | 24 | 0 | 0 | 0 | 0 | 24 |
| Vietnam | 22 | 0 | 0 | 0 | 0 | 22 |
| Malaysia | 22 | 0 | 0 | 0 | 0 | 22 |
| Kuwait | 22 | 0 | 0 | 0 | 0 | 22 |
| Ireland | 8 | 0 | 0 | 0 | 12 | 20 |
| Benin | 18 | 0 | 0 | 0 | 0 | 18 |
| Tunisia | 15 | 0 | 0 | 0 | 0 | 15 |
| Turkey | 12 | 0 | 0 | 0 | 0 | 12 |
| Slovenia | 3 | 8 | 0 | 0 | 0 | 11 |
| Brazil | 0 | 8 | 0 | 0 | 0 | 8 |
| Ukraine | 6 | 0 | 0 | 0 | 0 | 6 |
| Croatia | 4 | 0 | 0 | 0 | 0 | 4 |
| Guernsey | 0 | 0 | 0 | 3 | 0 | 3 |
| Argentina | 1 | 1 | 0 | 0 | 0 | 2 |
| Gambia | 0 | 1 | 0 | 0 | 0 | 1 |

**Priority regions.**
- East Asia is strong: [[Japan]] (JPHC, 87 cancer rows), [[China]] (Shanghai Cohort Study, Shanghai Women's Health
  Study; 100 cancer rows), [[South Korea]], [[Taiwan]].
- Southeast Asia is thin: [[Singapore]] (11 colorectal-cancer rows, Singapore Chinese Health Study),
  [[Thailand]], [[Vietnam]], [[Malaysia]].
- South Asia: only [[India]], with 26 PAH/pollutant concentrations.
- Middle East: [[Iran]] (Golestan Province: fruit/vegetable/vitamin intake ↔ plasma vitamin C, β-carotene,
  retinol), [[Israel]], [[Kuwait]] (22 PAH urinary metabolites from a seven-Asian-country study), [[Turkey]];
  North Africa: [[Egypt]], [[Tunisia]].
- No GCC country except Kuwait, and no Central Asia.

## Inferring effects on the body
**Direct, human evidence.** Two relations can be chained:
1. **Food → biomarker** (`correlations.csv`, `metabolomic_associations.csv`): intake measured by FFQ/recall/record or
   a controlled intervention is correlated with a compound measured in urine or blood. This shows that the food
   delivers the compound into the body.
2. **Biomarker → cancer** (`cancer_associations.csv`): the compound was measured in pre-diagnostic blood/urine in
   prospective cohorts (nested case-control, case-cohort). The download gives the pair tested, the cohort and the
   number of cases, but **not the effect size or direction**. Those have to be read from the paper (`Publication` →
   `publications.csv` → PubMed id).

**Evidence type:** observational epidemiology (cohorts) and controlled feeding/metabolomics. There are no
traditional claims and nothing text-mined; all rows are hand-curated.

**Example chain: green tea (East Asia) → tea catechins → cancer**
| step | row(s) |
|---|---|
| tea → urinary biomarkers | `correlations.csv`: `Tea` ↔ 4-O-methylgallic acid, urine 24-h, France, r = 0.55 (n = 476, Edmands 2015); `Tea` ↔ 4-O-methylgallic acid, Australia, r = 0.57 (n = 344, Hodgson 2004); `Tea` ↔ methyl(epi)catechin sulfate r = 0.29 |
| compound id | `biomarkers.csv`: Epigallocatechin 3-gallate, PubChem 65064, HMDB0003153, FooDB FDB017702, InChIKey `WMBWREPUVVBILR-WIYYLYMNSA-N` |
| catechins → cancer | `cancer_associations.csv`: Epigallocatechin 3-gallate & epigallocatechin → **Breast cancer**, Japan, JPHC, nested case-control, 144 cases (Iwasaki 2010); → **Gastric and oesophageal cancer**, Japan, JPHC, 494 cases (Sasazuki 2008); epigallocatechin → **Liver cancer**, China, Shanghai Cohort Study, 211 cases (Butler 2015); → **Colon and rectal cancer**, China, SCS, 162 cases (Yuan 2007) |
| mechanism (other DB) | [[CTD]]: EGCG → Breast Neoplasms `therapeutic` (PMID 10518005) |

The same InChIKey links to [[HMDB]] (food-source ontology, disease links) and [[CTD]] (curated
therapeutic/marker evidence). Turmeric/curcumin and dates have **no** rows here: the database covers polyphenols,
carotenoids, vitamins, fatty acids and pollutants, and is mostly built from Western/East Asian cohorts.

## Linking to other datasets
- **PubChem CID / InChIKey / HMDB ID / FooDB ID** in `biomarkers.csv` → [[HMDB]] (`accession`, `inchikey`),
  [[CTD]] (`PubChemCID`, `InChIKey`), FooDB and [[FoodAtlas]] (PubChem-keyed chemicals). HMDB and FooDB ids come from
  the same Wishart-lab ecosystem, so they match directly.
- **Intake names** (e.g. `Tea`, `Citrus fruits`, `Red meat`) are free-text food terms that can be string-matched to
  food nodes in [[FoodAtlas]] or FoodOn. There are no food ids.
- **Cohort** names (EPIC, JPHC, SCS, SWHS…) connect rows to countries and populations.

## Versions
- **4.0 (Oct 2025, used here):** adds 313 environmental pollutants, 1,741 concentration values and 2,492
  reproducibility values.
- 3.0 (Mar 2021): 462 gut microbial metabolites with 3 types of microbial-origin evidence from 166 publications;
  ChemOnt-based chemical classification (Sci Rep 2023, doi:10.1038/s41598-022-26366-w).
- 2.0 (Sep 2019): 185 candidate dietary biomarkers from metabolomics (403 associations) and 1,356 biomarker–cancer
  associations from 313 publications; new classifications (paper: [[Neveu2020 - Exposome-Explorer 2.0]]).
- 1.0 (Feb 2017): 692 biomarkers from 480 publications.

## Caveats
- The cancer download has **no effect estimates**, so it tells you a pair was studied, not whether the risk was
  lower or higher. Effect sizes must come from the source paper.
- Few food-intake associations for Middle-East, South-Asian or Central-Asian foods. Priority-region coverage is
  mostly pollutant concentrations.
- No explicit open licence (© IARC); fine for research use, but redistribution terms are unclear.
