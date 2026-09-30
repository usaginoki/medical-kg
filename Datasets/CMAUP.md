---
title: "CMAUP"
slug: cmaup
kind: [ingredient, compound]
version: "2.0 (CMAUP database update 2024; NAR 2024, online 2023-10-28)"
previous_versions: "1.0 (CMAUP-2019, Zeng et al. NAR 2019, doi:10.1093/nar/gky965; 5,645 plants; still online at bidd.group/CMAUP-2019 and its files at CMAUP/downloadFiles_2018/)"
papers: ["[[Hou2024 - CMAUP database update 2024]]"]
url: "https://bidd.group/CMAUP/"
license: "not stated on the download page (the 2024 paper is CC BY 4.0)"
availability: open-download
access_link: "https://bidd.group/CMAUP/download.html"
accessed: true
access_method: [website-download, scrape]
access_date: 2026-09-30
access_notes: "Downloaded 10 of the 13 v2.0 files (197 MB) with curl. Skipped: Plant_molecular_targets_overlapping_with_DEGs.txt (99 MB) and Transcriptomic_profiling_of_74_diseases.rar (159 MB), both transcriptomics layers. Added header lines to the two headerless Plant_Ingredient_Associations files. Plant geography and 'used in medicines by country' are NOT in any download file; they exist only on the web. We therefore scraped (1 req/s) the world-map values embedded in index.html (plants per country, 153 countries), the plant lists behind the world map for 43 priority countries (searchresults.php?location=xx; 9,111 plant–country rows, 2,471 plants), and 11 plant pages (Used in Medicines Country/Region, Traditional Medicine System, Medicinal Functions, Geographical Distribution)."
countries: ["[[Afghanistan]]", "[[Albania]]", "[[Algeria]]", "[[Angola]]", "[[Argentina]]", "[[Australia]]", "[[Austria]]", "[[Bahamas]]", "[[Bangladesh]]", "[[Belarus]]", "[[Belgium]]", "[[Belize]]", "[[Benin]]", "[[Bhutan]]", "[[Bolivia]]", "[[Botswana]]", "[[Brazil]]", "[[Bulgaria]]", "[[Burkina Faso]]", "[[Burundi]]", "[[Cape Verde]]", "[[Cambodia]]", "[[Cameroon]]", "[[Canada]]", "[[Chad]]", "[[Chile]]", "[[China]]", "[[Colombia]]", "[[Comoros]]", "[[Costa Rica]]", "[[Croatia]]", "[[Cuba]]", "[[Cyprus]]", "[[Czech Republic]]", "[[Côte d'Ivoire]]", "[[Democratic Republic of the Congo]]", "[[Denmark]]", "[[Djibouti]]", "[[Dominican Republic]]", "[[Ecuador]]", "[[Egypt]]", "[[El Salvador]]", "[[Equatorial Guinea]]", "[[Eritrea]]", "[[Estonia]]", "[[Eswatini]]", "[[Ethiopia]]", "[[Fiji]]", "[[Finland]]", "[[France]]", "[[Gabon]]", "[[Gambia]]", "[[Georgia]]", "[[Germany]]", "[[Ghana]]", "[[Greece]]", "[[Guatemala]]", "[[Guinea]]", "[[Guinea-Bissau]]", "[[Guyana]]", "[[Haiti]]", "[[Honduras]]", "[[Hungary]]", "[[Iceland]]", "[[India]]", "[[Indonesia]]", "[[Iran]]", "[[Iraq]]", "[[Ireland]]", "[[Israel]]", "[[Italy]]", "[[Jamaica]]", "[[Japan]]", "[[Jordan]]", "[[Kazakhstan]]", "[[Kenya]]", "[[Kuwait]]", "[[Laos]]", "[[Lebanon]]", "[[Lesotho]]", "[[Liberia]]", "[[Libya]]", "[[Lithuania]]", "[[Madagascar]]", "[[Malawi]]", "[[Malaysia]]", "[[Maldives]]", "[[Mali]]", "[[Mauritania]]", "[[Mauritius]]", "[[Mexico]]", "[[Mongolia]]", "[[Morocco]]", "[[Mozambique]]", "[[Myanmar]]", "[[Namibia]]", "[[Nepal]]", "[[Netherlands]]", "[[New Zealand]]", "[[Nicaragua]]", "[[Niger]]", "[[Nigeria]]", "[[Norway]]", "[[Oman]]", "[[Pakistan]]", "[[Papua New Guinea]]", "[[Paraguay]]", "[[Peru]]", "[[Philippines]]", "[[Poland]]", "[[Portugal]]", "[[Qatar]]", "[[Romania]]", "[[Russia]]", "[[Rwanda]]", "[[Saudi Arabia]]", "[[Senegal]]", "[[Seychelles]]", "[[Sierra Leone]]", "[[Somalia]]", "[[South Africa]]", "[[South Korea]]", "[[Spain]]", "[[Sri Lanka]]", "[[Sudan]]", "[[Suriname]]", "[[Sweden]]", "[[Switzerland]]", "[[Syria]]", "[[Taiwan]]", "[[Tajikistan]]", "[[Tanzania]]", "[[Thailand]]", "[[Togo]]", "[[Trinidad and Tobago]]", "[[Tunisia]]", "[[Turkey]]", "[[Turkmenistan]]", "[[Uganda]]", "[[Ukraine]]", "[[United Kingdom]]", "[[United States]]", "[[Uruguay]]", "[[Uzbekistan]]", "[[Vanuatu]]", "[[Venezuela]]", "[[Vietnam]]", "[[Yemen]]", "[[Zambia]]", "[[Zimbabwe]]"]
regions: ["[[Global]]", "[[Middle East]]", "[[North Africa]]", "[[Central Asia]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]"]
n_records: "7,865 plants · 60,222 ingredients · 412,761 plant–ingredient links · 758 targets · 28,871 ingredient–target activity records · 765,266 plant–disease associations (1,404 ICD-11 diseases) · 429,050 plant–clinical-trial rows · plant geography for 153 countries (web only)"
size: "197 MB downloaded (TSV) + 0.3 MB scraped CSV"
formats: [tsv, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Plant → ICD-11 disease associations with four evidence types (shared therapeutic targets, reversal of disease transcriptomic changes, clinical trials of the plant, clinical trials of its ingredients); ingredient → human target with IC50/Ki/EC50 values and PMIDs; predicted human oral bioavailability per ingredient. On the web only: plant → 'Medicinal Functions' (e.g. Carminative, Hypoglycaemic) and traditional medicine system (TCM, Ayurveda, Unani, Siddha, Sowa-Rigpa, Kampo…)."
join_keys: [PubChem CID, InChIKey, ChEMBL id, NCBI taxon, scientific name, UniProt, gene symbol, TTD id, ICD-11 code, NCT id, CMAUP/NPASS NPO and NPC ids]
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
  - region/global
  - tradmed/tcm
  - tradmed/ayurveda
  - tradmed/unani
---
# CMAUP

> [!abstract] TL;DR
> CMAUP (Collective Molecular Activities of Useful Plants) comes from Chen Yu Zong's and Zeng Xian's BIDD group
> (Tsinghua / Fudan), the same team as [[NPASS]]. The **2024 update (v2.0)** covers **7,865 plants**
> (medicinal, food, human-edible, agricultural, garden and drug-producing). They are linked to **60,222
> ingredients**, 758 human targets with measured activities, and **765,266 plant → ICD-11 disease
> associations** backed by targets, transcriptomics or clinical trials. The geography layer is on the web only:
> a world map gives **plants per country for 153 countries**, and each plant page lists the **countries and
> traditional medicine systems where it is used medicinally**. That layer is what makes CMAUP useful for
> culture-aware advice (Q2), and the disease/target layer covers Q3.

## Access
| | |
|---|---|
| Availability | open download of the tables (no registration); geography and traditional-use fields on web pages only |
| Link | https://bidd.group/CMAUP/download.html |
| Accessed? | yes for the tables (10 of 13 files); partial for geography (scraped) |
| How | `curl` with a browser User-Agent for `downloadFiles/CMAUPv2.0_download_*.txt`. Scraped at 1 req/s: `index.html` (world-map JSON values), `searchresults.php?location=<iso2>` for 43 priority countries, `plant.php?plant=<NPO id>` for 11 plants |
| Downloaded | `Data/cmaup/`: 10 TSVs (197 MB) + `Download_Readme.txt` + `worldmap_plants_per_country.csv` + `scraped_plant_location_priority.csv` + `scraped_plant_pages_sample.csv` |

Skipped: `Plant_molecular_targets_overlapping_with_DEGs.txt` (99 MB) and
`Transcriptomic_profiling_of_74_diseases.rar` (159 MB). The disease-association table already summarises the
transcriptomic evidence (column `Association_by_Disease_Transcriptiome_Reversion`).

## Tables & columns
Meanings come from `Download_Readme.txt`. Ids: `NPO…` = plant (organism), `NPC…` = ingredient, `NPT…` = target.
These are the **same id spaces as [[NPASS]]** (NPO24124 = *Curcuma longa* and NPC109083 = curcumin in both).

### `CMAUPv2.0_download_Plants.txt` (7,865 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_ID` | str | CMAUP plant id | NPO24124 |
| `Plant_Name` | str | Latin name as displayed | Curcuma Longa |
| `Species_Tax_ID`, `Species_Name` | str | NCBI Taxonomy id and name at species level (NA when unresolved) | 136217, Curcuma longa |
| `Genus_Tax_ID`, `Genus_Name`, `Family_Tax_ID`, `Family_Name` | str | genus and family with NCBI ids | 99568 Curcuma; 4642 Zingiberaceae |

### `CMAUPv2.0_download_Ingredients_All.txt` (60,222 rows) and `…_onlyActive.txt` (2,979 rows)
| column | type | meaning | example |
|---|---|---|---|
| `np_id` | str | ingredient id | NPC109083 |
| `pref_name`, `iupac_name` | str | common and IUPAC name | Curcumin |
| `chembl_id`, `pubchem_cid` | str | ChEMBL id, PubChem CID | CHEMBL116438, 5281767 |
| `MW`, `LogS`, `LogD`, `LogP`, `nHA`, `nHD`, `TPSA`, `nRot`, `nRing` | float | physicochemical properties (ADMETlab 2.0) | – |
| `InChI`, `InChIKey`, `SMILES` | str | structure | ZIUSSTSXXLLKKK-KOBPDPAPSA-N |

"onlyActive" = ingredients with measured activity against a target.

### `CMAUPv2.0_download_Plant_Ingredient_Associations_allIngredients.txt` (412,761 rows) and `…_onlyActiveIngredients.txt` (56,948 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_ID` | str | plant (7,760 plants have ingredients) | NPO27288 |
| `Ingredient_ID` | str | ingredient (59,620 distinct) | NPC139546 |

The files have no header; we added `Plant_ID\tIngredient_ID`. No amounts or plant parts.

### `CMAUPv2.0_download_Targets.txt` (758 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Target_ID`, `Gene_Symbol`, `Protein_Name` | str | target | NPT31, PTGS2, Cyclooxygenase-2 |
| `Uniprot_ID`, `ChEMBL_ID`, `TTD_ID` | str | cross-references | Q92753 |
| `if_DTP`, `if_CYP`, `if_therapeutic_target` | int | drug transporter / cytochrome P450 / other therapeutic target (per DrugMAP) | 0, 0, 1 |
| `Target_Class_Level1..3`, `Target_Class_level_displayed`, `Target_type` | str | protein class hierarchy and DrugMAP type | Transcription factor › Nuclear receptor |

### `CMAUPv2.0_download_Ingredient_Target_Associations_ActivityValues_References.txt` (28,871 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Ingredient_ID`, `Target_ID` | str | 3,496 ingredients × 1,143 target ids | NPC109083, NPT31 |
| `Activity_Type`, `Activity_Relationship`, `Activity_Value`, `Activity_Unit` | str | measured activity (IC50 12,874; Potency 8,387; Ki 4,812; EC50 2,182) | IC50 = 11060 nM |
| `Reference_ID`, `Reference_ID_Type` | str | source (PMID…) | 465319, PMID |

### `CMAUPv2.0_download_Plant_Human_Disease_Associations.txt` (765,266 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_ID` | str | plant (6,556 plants) | NPO24124 |
| `ICD-11 Code`, `Disease_Category`, `Disease` | str | disease in ICD-11 (1,404 diseases, 28 chapters) | 6A20, 06.Mental…, Schizophrenia |
| `Association_by_Therapeutic_Target` | str | plant targets that are therapeutic targets of the disease (428,736 rows filled) | SLC6A4,AKR1B1 |
| `Association_by_Disease_Transcriptiome_Reversion` | str | disease DEGs overlapping the plant's targets (220,936 filled) | – |
| `Association_by_Clinical_Trials_of_Plant` | str | NCT ids of trials of the plant/extract (764 filled) | NCT02104752 |
| `Association_by_Clinical_Trials_of_Plant_Ingredients` | str | NCT ids of trials of its ingredients (154,121 filled) | NCT00211562 |

### `CMAUPv2.0_download_Plant_Clinical_Trials_Associations.txt` (429,050 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_ID`, `NCT_ID`, `Title` | str | plant (4,797) and ClinicalTrials.gov trial (15,155) | NCT04535427 |
| `Disease/Condition` | str | indication | rheumatoid arthritis |
| `Form_in_Clinical_Use` | str | what was tested: an ingredient with its NPC id, or the plant | Arginine (NPC226453) |
| `Phase` | str | trial phase | Phase 2 |
| `Associated_by plant_or_compound` | str | plant (747 rows) or compound (428,303 rows) | compound |

### `CMAUPv2.0_download_Human_Oral_Bioavailability_information_of_Ingredients_All.txt` (60,222 rows)
`Ingredient_ID`, `SMILES`, `XLOGP3`, `RTB`, `TPSA`, `Fcsp3`, `MW`, `ESOL`, and three predicted 0/1 labels:
`Prediction_Hob` (HobPre, 32,459 high), `Prediction_Swissadme` (all six SwissADME rules, 15,122 high),
`Prediction_Hob&Swissadme` (both, 13,084 high).

### Scraped: `worldmap_plants_per_country.csv` (153 rows)
| column | type | meaning | example |
|---|---|---|---|
| `location_code` | str | ISO-3166 alpha-2 code used by the site's world map | ir |
| `country` | str | our canonical name | Iran |
| `n_plants` | int | number of CMAUP plants whose *geographical distribution* includes the country (the map's colour scale) | 140 |

### Scraped: `scraped_plant_location_priority.csv` (9,111 rows)
`location_code`, `country`, `Plant_ID`: the plant list returned by clicking a country on the map, for 43
priority countries (Middle East, North Africa, Central/South/East/Southeast Asia). It covers 2,471 distinct
plants. The site renders a few duplicate rows, so counts are 1–4% below the map values.

### Scraped: `scraped_plant_pages_sample.csv` (11 rows)
`Plant_ID`, `Plant_Name`, `used_in_medicines_country_region`, `traditional_medicine_system`,
`medicinal_functions`, `geographical_distribution`, parsed from the "Plant General Information" section of
`plant.php`. Example: *Trigonella foenum-graecum*: used in medicines in Canada; Israel; Turkmenistan; Algeria;
India; Indonesia; Lebanon; Jordan; Chile; Argentina; Iraq; Spain · TM systems Indian Folk; Unani; Ayurveda;
Siddha · functions Anticholesterolemic; …; Hypoglycaemic; Hypotensive; …. The *Nigella sativa* and
*Cuminum cyminum* pages have no such section.

Sample: `Data/cmaup/sample.csv` · full profile: `Data/cmaup/schema.md`

## Countries & cultures covered
CMAUP has two geographic signals, both on the web only.
1. **Geographical distribution**: where the plant occurs. It is the basis of the world map and the per-country
   plant counts below, and it is closer to "what grows locally" than to "what is used".
2. **Used in Medicines Country/Region** and **Traditional Medicine System** per plant, closer to a cultural
   use label. The Browse page gives medicinal plants per system: **TCM 2,490, Indian Folk 681, Ayurveda 397,
   Siddha 367, Unani 274, Sowa-Rigpa 153, Homeopathy 148, Kampo 91**.

**Priority countries: plants per country (world map) / plants we scraped:**
China 1,726/1,683 · India 1,096/1,074 · Thailand 529/521 · Vietnam 397/391 · Indonesia 379/372 ·
Bangladesh 313/305 · Myanmar 291/287 · Turkey 288/283 · Japan 271/264 · Philippines 269/262 · Taiwan 234/228 ·
Laos 228/226 · Cambodia 210/206 · Nepal 208/202 · South Korea 192/187 · Algeria 192/185 · Sri Lanka 191/188 ·
Morocco 184/178 · Pakistan 183/181 · **Iran 140/137** · Tunisia 136/130 · **Kazakhstan 127/126** · **Iraq 126/124** ·
Sudan 128/122 · **Jordan 118/113** · Libya 116/111 · **Turkmenistan 105/103** · Afghanistan 96/94 · Mongolia 95/93 ·
Malaysia 94/92 · **Uzbekistan 90/89** · **Tajikistan 90/88** · **Lebanon 87/84** · Egypt 88/83 · Georgia 75/74 ·
**Saudi Arabia 62/59** · **Yemen 56/55** · **Oman 48/47** · Israel 45/41 · **Kuwait 15/15** · Syria 6/5 · **Qatar 3/2** ·
Bhutan 2/1. There is no entry for the UAE, Bahrain, Kyrgyzstan, Azerbaijan, Armenia or North Korea.

**All 153 map entries (plants):** China 1726; India 1096; Thailand 529; South Africa 519; United States 445;
Vietnam 397; Indonesia 379; Italy 378; Russia 360; Bangladesh 313; Myanmar 291; Turkey 288; Australia 283;
Spain 281; Mexico 276; Japan 271; Philippines 269; Tanzania 268; Brazil 267; Kenya 264; France 258;
Taiwan 234; Laos 228; Greece 224; Bulgaria 224; Albania 222; Germany 217; Romania 210; Cambodia 210;
Austria 210; Ukraine 209; Nepal 208; Rwanda 196; Switzerland 195; Bolivia 193; Algeria 192; South Korea 192;
Sri Lanka 191; Morocco 184; Portugal 183; Pakistan 183; Trinidad and Tobago 182; Argentina 180; Hungary 180;
Nigeria 177; Angola 171; Peru 170; Netherlands 170; Zimbabwe 168; Colombia 168; Cuba 168; Venezuela 163;
Poland 162; Belgium 160; United Kingdom 159; Dominican Republic 156; Cameroon 149; Ecuador 142; Belarus 142;
Sweden 142; Ethiopia 141; Iran 140; Guinea 138; Haiti 138; Madagascar 138; Honduras 137; Tunisia 136;
Ghana 134; Denmark 131; Finland 131; Mozambique 129; Canada 128; Sudan 128; Kazakhstan 127; Iraq 126;
Jamaica 120; Norway 119; Jordan 118; Mauritius 118; Uganda 118; Libya 116; New Zealand 112;
Côte d'Ivoire 109; Costa Rica 109; Turkmenistan 105; Togo 104; Eswatini 102; Benin 101; Ireland 101;
Zambia 96; Afghanistan 96; Mongolia 95; Guatemala 94; Burkina Faso 94; Malaysia 94; New Caledonia (France) 94;
Gabon 92; DR Congo 92; Sierra Leone 92; Fiji 91; Senegal 91; Tajikistan 90; Uzbekistan 90; Chad 88;
Egypt 88; Malawi 88; Lebanon 87; Belize 87; Chile 85; Liberia 84; Nicaragua 84; Somalia 81; Eritrea 76;
Guinea-Bissau 75; Georgia 75; Cyprus 74; Burundi 72; El Salvador 72; Gambia 68; Paraguay 68; Bahamas 66;
Mali 66; Seychelles 66; French Guiana (France) 62; Saudi Arabia 62; Namibia 57; Guyana 56; Yemen 56;
Botswana 55; Papua New Guinea 54; Suriname 52; Mauritania 50; Oman 48; Cape Verde 48; Uruguay 48; Niger 47;
Israel 45; Vanuatu 42; Djibouti 40; Lesotho 37; Equatorial Guinea 32; Maldives 32; Iceland 29;
Lithuania 26; Comoros 24; Kuwait 15; Greenland (Denmark) 13; Syria 6; Qatar 3; Croatia 3; Estonia 2;
Bhutan 2; Czech Republic 2.

## Inferring effects on the body
`body_effect: direct`. Evidence types:
- **Plant → disease (ICD-11)**: four evidence columns. Two are mechanistic/predicted: the plant's ingredient
  targets are therapeutic targets of the disease (from TTD), or those targets overlap the disease's DEGs from
  20,027 patient samples. Two come from clinical-trial registries: the plant itself (764 rows) or one of its
  ingredients (154,121 rows). None of them is a traditional claim.
- **Ingredient → human target**: measured IC50/Ki/EC50 values with PMIDs (in vitro).
- **Oral bioavailability**: predicted (HobPre, SwissADME rules).
- **Traditional use** (web only): plant → "Medicinal Functions" (e.g. *Crocus sativus*: Antispasmodic;
  Aphrodisiac; Carminative; Emmenagogue; Sedative…) and the medicine systems using it.

Chain example, turmeric (`NPO24124`, *Curcuma longa*):
- It is associated with 517 ICD-11 diseases. For example, Schizophrenia (6A20) via targets SLC6A4 and AKR1B1,
  a plant trial (NCT02104752) and an ingredient trial (NCT00211562). Chronic kidney disease stage 5 via plant
  trials NCT01906840 and NCT01037595.
- Curcumin (`NPC109083`, CID 5281767) has 89 target-activity rows, e.g. PTGS2 (COX-2) IC50 11,060 nM,
  amyloid-beta precursor protein Ki 0.208 nM, ALOX5 IC50 8,000 nM.
- Web: used in medicines in Thailand, Indonesia, India and China; systems Sowa-Rigpa, Indian Folk, Unani,
  Siddha, Ayurveda, TCM, Homeopathy.

## Linking to other datasets
- **NPO/NPC/NPT ids are shared with [[NPASS]]**, so no mapping is needed: the NPASS tables add quantitative
  composition (web), toxicity and more activity records for the same plants and compounds.
- **PubChem CID / InChIKey / ChEMBL** → [[FooDB]], [[IMPPAT]], [[Phenol-Explorer]], [[DrugBank]].
- **NCBI taxon / scientific name** → [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] (folk use by
  country), [[IMPPAT]], [[SymMap]]. [[UNaProd]] already hyperlinks its Persian materia-medica monographs to
  CMAUP plant pages (`SciName1`/`SciName2` links such as `plant.php?plant=NPO21495`).
- **Gene symbol / UniProt / TTD** → [[CTD]], [[DrugBank]]. **ICD-11** and **NCT ids** → disease and trial
  registries.

## Versions
| | CMAUP-2019 (v1.0) | CMAUP-2024 (v2.0) |
|---|---|---|
| plants | 5,645 (paper) / 5,654 (2024 paper's table) | **7,865** |
| ingredients | 47,645 | **60,222** |
| targets (activity < 1 µM) | 436 | **758** |
| diseases | 656 | **1,399** |
| plant–disease associations by target | 263,130 | **428,737** |
| new layers | – | transcriptomic reversion (74 diseases, 20,027 samples); clinical trials (691 plant-level; 14,516 ingredient-level); drug-producing plant class; DNA barcodes (3,949 plants); phylogenetic tree; oral bioavailability predictions; Disease Ontology (1,203 terms) |

v1.0 files remain at `downloadFiles_2018/`. We downloaded v2.0 only.

## Caveats
- **Geography is not downloadable**, and the map counts reflect **where a plant grows**, not where it is eaten
  or used. For a use-by-culture signal you need the per-plant "Used in Medicines Country/Region" field, which
  would need a crawl of ~7,865 plant pages (we took 11).
- **Ingredient-trial associations are very permissive**: any trial of any compound found in the plant counts.
  Turmeric picks up paclitaxel, etoposide and ascorbate oncology trials because those compounds are listed as
  its ingredients. Use `Association_by_Clinical_Trials_of_Plant` or target evidence for anything plant-specific.
- Plant–ingredient links have **no amounts and no plant part**. Get composition from [[NPASS]] (web) or
  [[Dr. Duke's Phytochemical and Ethnobotanical Databases]].
- The activity table uses 1,143 target ids, but the Targets file lists only 758 (the < 1 µM targets).
  385 target ids (6.7% of activity rows) do not resolve in the download.
- Licence not stated on the site.
