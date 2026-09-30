---
title: "IMPPAT"
slug: imppat
kind: [ingredient, compound]
version: "3.0 (released September 2026)"
previous_versions: "1.0 (2018-01-25, Mohanraj et al. Sci Rep 2018); 2.0 (2022-06-17, Vivek-Ananth et al. ACS Omega 2023)"
papers: ["[[Vivek-Ananth2023 - IMPPAT 2.0 phytochemical atlas]]"]
url: "https://cb.imsc.res.in/imppat/"
license: "CC BY-NC-ND 4.0"
availability: open-download
access_link: "https://cb.imsc.res.in/imppat/download"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "All 8 TSV batch files of v3.0 downloaded. The links on the download page point to /imppat/images/Batch_Download1/…, which returned 404 on release day; the same file names under /imppat/images/Batch_Download/ (no '1') work and hold v3.0 data (IMPPAT3_ ids, counts match the statistics page). Not downloaded: the 2D/3D SDF structure files (87 + 85 MB). The IMPPAT-KG page (/imppat/kgraph) returned 404. MeSH/ICD-11/UMLS/DOID mappings of therapeutic uses are shown on the web pages but are not in the batch TSVs."
countries: ["[[India]]"]
regions: ["[[South Asia]]"]
n_records: "4,154 plants · 18,314 phytochemicals · 196,220 plant–part–phytochemical links · 94,261 plant–part–therapeutic-use links · 1,576 formulations · 38,842 phytochemical–human-target links"
size: "41 MB (TSV, without SDF)"
formats: [tsv, sdf]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Plant → therapeutic use (traditional-medicine texts, standardised to MeSH/ICD-11/UMLS/DO terms); phytochemical → human gene targets (ChEMBL, NPASS, BindingDB, experimentally supported) and bioactivity values (IC50/EC50/Ki/Kd); formulation → therapeutic use (Ayurvedic Pharmacopoeia and Formulary of India)."
join_keys: [PubChem CID, InChIKey, ChEBI, ChEMBL id, scientific name, HGNC symbol, Ensembl gene id, Entrez gene id, UniProt]
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
# IMPPAT

> [!abstract] TL;DR
> IMPPAT (Indian Medicinal Plants, Phytochemistry And Therapeutics) is a manually curated database from the
> Samal lab at IMSc Chennai. It was built from 100+ books on traditional Indian medicine and 7,000+ research
> articles. **Version 3.0** (September 2026) links **4,154 Indian medicinal plants** by plant part to
> **18,314 phytochemicals** and **1,544 therapeutic uses**. It adds **1,576 Ayurvedic formulations** (from the
> Ayurvedic Pharmacopoeia and Formulary of India) and **38,842 experimentally supported phytochemical–human
> target links**. Many plants are also foods and spices (turmeric, okra, amla, ginger, fenugreek). That makes
> IMPPAT the main South Asian bridge from ingredient to compound to traditional claim to human target (Q2, Q3).

## Access
| | |
|---|---|
| Availability | open download (10 batch files on the download page), plus per-plant, per-phytochemical and per-therapeutic-use web pages |
| Link | https://cb.imsc.res.in/imppat/download |
| Accessed? | yes: all 8 TSV tables of v3.0 |
| How | `curl` with a browser User-Agent. The links on the page (`images/Batch_Download1/…`) returned 404 on release day, so the files were fetched from `images/Batch_Download/<same name>` |
| Downloaded | `Data/imppat/`: 8 TSVs, 41 MB. The 2D/3D SDF structure files were skipped; the InChI and SMILES in `Chemical_Information` are enough for joins |

Other access routes: the website has Browse (by plant, phytochemical, chemical superclass, therapeutic use or
formulation), a Basic search and an Advanced search (physicochemical or drug-likeness filters). There is no
documented REST API. The IMPPAT-KG page advertised on the home page returned 404 on 2026-09-30.

## Tables & columns
Identifiers use the prefixes `IMPPAT3_PLTID`, `IMPPAT3_PHYID` and `IMPPAT3_TPUID`, plus `API…` and `AFI…` for formulations.

### `Plant_Information_IMPPAT.tsv` (4,154 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_identifier` | str | IMPPAT plant id | IMPPAT3_PLTID000001 |
| `Indian_Medicinal_plant` | str | accepted scientific name | Abelmoschus esculentus |
| `Synonymous names` | str | pipe-separated botanical synonyms | Hibiscus esculentus\|Abelmoschus esculentus |
| `Kingdom`, `Family`, `Group` | str | taxonomy; Group = Angiosperms (3,973) / Pteridophytes (91) / Gymnosperms (89) | Plantae, Malvaceae, Angiosperms |
| `Common_name` | str | English common name | Ladies Finger |
| `IUCN_Red_List_Category` | str | conservation status (sparse) | Least Concern |
| `System_of_Medicine` | str | comma-separated traditional systems using the plant | Ayurveda,Siddha,Unani |

### `Chemical_Information_IMPPAT_Phytochemicals.tsv` (18,314 rows)
| column | type | meaning | example |
|---|---|---|---|
| `IMPPAT_Phytochemical_identifier` | str | IMPPAT compound id | IMPPAT3_PHYID000002 |
| `Reference_identifier` | str | source id used for the structure (mostly `CID_…`) | CID_5793 |
| `Phytochemical name_standardised` | str | preferred name | D-Glucose |
| `Synonymous chemical names` | str | names found in the curated sources | d-glucose\|glucose |
| `Pubchem_CID` | str | PubChem CID (17,738 non-null) | CID_5793 |
| `ChEMBL`, `ChEBI`, `ZINC`, `FDASRS`, `SureChEMBL`, `MolPort` | str | cross-references (ChEBI: 5,738) | CHEBI:4167 |
| `Canonical_SMILES`, `DeepSMILES`, `InChI`, `InChIKey` | str | structure (InChIKey 100%) | WQZGKKKJIJFFOK-GASJEMHNSA-N |
| `Scaffold Graph`, `Scaffold Graph/Node`, `Scaffold Graph/Node/Bond` | str | molecular scaffolds at 3 levels of abstraction | C1CCOCC1 |
| `Functional_Groups` | str | `;`-separated functional groups | CO;COC(O)C |

### `IMPPAT_Phytochemical_Plant_Association.tsv` (196,220 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Plant_identifier`, `Indian_Medicinal_plant` | str | plant | IMPPAT3_PLTID000001, Abelmoschus esculentus |
| `Plant_part` | str | part in which the compound was reported (leaf 43,587; aerial part 21,193; flower 17,694; fruit 15,398; seed 11,457; root 11,274…) | seed |
| `IMPPAT_Phytochemical_identifier`, `Reference_identifier` | str | compound | IMPPAT3_PHYID000061, CID_7655 |

### `IMPPAT_TherapeuticUse_Plant_Association.tsv` (94,261 rows)
| column | type | meaning | example |
|---|---|---|---|
| `IMPPAT_Plant_identifier`, `Indian_Medicinal_plant` | str | plant (4,109 plants have at least one use) | Curcuma longa |
| `Plant_part` | str | part used (often empty) | rhizome |
| `IMPPAT_Therapeutic_use_identifier` | str | standardised use id (1,298 distinct in this file) | IMPPAT3_TPUID001453 |
| `Therapeutic_use` | str | standardised term; the web pages map these to MeSH/ICD-11/UMLS/DO | urination disorders, dyspepsia, antirheumatic agents |

### `Target_IMPPAT_Phytochemicals.tsv` (38,842 rows)
| column | type | meaning | example |
|---|---|---|---|
| `IMPPAT_Phytochemical_identifier` | str | compound (2,944 distinct) | IMPPAT3_PHYID000002 |
| `Gene_identifier` | str | Ensembl gene id of the human target | ENSG00000085662 |
| `HGNC_Symbol` | str | gene symbol (1,943 distinct) | AKR1B1 |
| `Entrez gene identifier` | int | NCBI gene id | 231 |
| `Source` | str | evidence source: ChEMBL, NPASS, BindingDB, or combinations | ChEMBL \| NPASS |

### `Bioactivity_IMPPAT_Phytochemicals.tsv` (31,812 rows)
| column | type | meaning | example |
|---|---|---|---|
| `IMPPAT_Phytochemical_identifier` | str | compound | IMPPAT3_PHYID005594 (curcumin) |
| `Target_name`, `Target_organism`, `UniProt_identifier` | str | assayed protein (Homo sapiens 20,461 rows; rat, mouse…) | Monoamine oxidase A, Homo sapiens, P21397 |
| `EC50`, `IC50`, `Kd`, `Ki` | str | `\|`-separated measured values with relation and unit | = 5020.0 nM\|= 2740.0 nM |
| `Source` | str | NPASS / BindingDB | NPASS |

### `IMPPAT_SingleHerbalFormulations.tsv` (541 rows, 541 formulations) and `IMPPAT_PolyHerbalFormulations.tsv` (13,860 rows, 1,035 formulations)
One row per formulation × ingredient.
| column | type | meaning | example |
|---|---|---|---|
| `Formulation_identifier` | str | `API…` = Ayurvedic Pharmacopoeia of India single-herb drug; `AFI…` = Ayurvedic Formulary of India polyherbal | AFI000054 |
| `Formulation_name_in_API_original` / `Formulation name_in_AFI_original` | str | Sanskrit name (IAST) | Triphalā cūrṇa |
| `Ingredient name in …_original`, `Plant part in …_original` | str | ingredient as written in the pharmacopoeia | Pathyā (Harītakī), (P.) |
| `Therapeutic uses (according to …)` | str | Ayurvedic indications as written | gulma\| aṣhṭīlā\| kṛmiroga |
| `Ingredient_name_standardised`, `Plant_name_standardised`, `Plant_part_standardised` | str | curated botanical name and part (non-plant ingredients such as "Alkaline water" too) | Terminalia chebula, fruit |
| `Therapeutic_uses_standardised` | str | English/biomedical terms | abdominal pain\|prostatic hyperplasia\|helminthiasis |
| `IMPPAT_identifiers` | str | matching `IMPPAT3_TPUID` ids | IMPPAT3_TPUID000017\|… |
| `References` | str | ISBN of the source book | ISBN:8190115146 |

Sample: `Data/imppat/sample.csv` · full profile: `Data/imppat/schema.md`

## Countries & cultures covered
- **[[India]]**: every plant is an "Indian medicinal plant". There are **no state or sub-national labels** in the
  batch files. The cultural axis is the **system of medicine**: Ayurveda 1,328 plants, Siddha 1,151, Unani 813,
  Sowa Rigpa 325, Homeopathy 289 (a plant can have several).
- Formulations are Ayurvedic only (Ayurvedic Pharmacopoeia and Formulary of India).
- Many species are shared with other Asian pharmacopoeias. The 2.0 paper found that 18.6% of phytochemicals
  overlap with TCM-Mesh.

## Inferring effects on the body
`body_effect: direct`. There are three routes, each with a different kind of evidence:
1. **Traditional claim**: plant (and part) → `Therapeutic_use`, from 100+ traditional-medicine books,
   standardised to biomedical vocabularies. Formulation → `Therapeutic_uses_standardised` from the
   pharmacopoeias.
2. **Experimental (in vitro) target evidence**: phytochemical → human gene (`Target_…`, from ChEMBL, NPASS,
   BindingDB). In v2.0 these were STITCH-predicted links; in 3.0 they are experimentally supported.
3. **Bioactivity**: IC50/EC50/Ki/Kd values per compound–protein pair.

Example: turmeric (*Curcuma longa*) has 263 therapeutic-use rows, 128 of them for the rhizome, including
common cold, fever, diarrhoea, dyspepsia, bronchitis and "antirheumatic agents". Curcumin
(`IMPPAT3_PHYID005594`, CID 969516) is listed in 10 plants (including *Curcuma longa*, *C. aromatica*,
*C. amada*, *C. zedoaria*). It has 194 human-target rows (MAPK1, MAPK8, HDAC4/7/9, PPARD, TLR9…) and measured
activity such as MAO-A IC50 2.74–5.02 µM (NPASS). Targets can then be joined to [[CTD]] or disease resources
through HGNC or Entrez ids.

## Linking to other datasets
- **PubChem CID / InChIKey** → [[PubChem]], [[FooDB]], [[NPASS]], [[CMAUP]], [[COCONUT]], [[HMDB]]: compound-level
  joins to food-compound and bioactivity resources.
- **Scientific plant name** → [[GRAYU]] (which imports IMPPAT 2.0), [[OSADHI]], [[CMAUP]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]],
  and to ingredient names in food datasets such as [[IndicRecipeNutri]] or [[Indian Nutrient Databank (INDB)]].
  The join is manual: common name ↔ binomial (turmeric ↔ *Curcuma longa*).
- **HGNC / Entrez / UniProt** → [[CTD]], [[DrugBank]], and disease–gene resources.

## Versions
| version | released | plants | phytochemicals | therapeutic uses | formulations | targets |
|---|---|---|---|---|---|---|
| 1.0 | 2018-01-25 | 1,742 | 9,596 | 1,124 | – | predicted |
| 2.0 | 2022-06-17 (paper 2023) | 4,010 | 17,967 | 1,095 | 974 (plant links only) | 27,365 predicted (STITCH ≥ 700) |
| **3.0** | **Sept 2026** | **4,154** | **18,314** | **1,544** | **1,576** | **38,842 experimentally supported** |

What **3.0** adds over 2.0, per the website:
- **Formulation data**: 541 single-herb (API) and 1,035 polyherbal (AFI) formulations, each with ingredients and
  therapeutic uses. In 2.0 there were only plant–formulation links.
- More therapeutic uses (1,095 → 1,544) and more plant–therapeutic-use links (89,733 → 94,261).
- More plant–part–phytochemical links (189,386 → 196,220).
- Targets are now **experimentally supported** (ChEMBL, NPASS, BindingDB), where 2.0 had STITCH predictions.
- New annotations: bioactivity values, clinical trials, patents, spectral data, plant images, links to AyuCaRe
  reports.
- The whole dataset is transformed into a knowledge graph, **IMPPAT-KG**.

Release date: the home page says "released on September 30, 2026" and the statistics page says "September 5,
2026". No 3.0 paper was found as of 2026-09-30; the latest paper is the 2.0 one.

## Caveats
- **Licence CC BY-NC-ND 4.0**: no derivatives, so redistributing a modified or merged IMPPAT is restricted.
  Internal research use is fine; check before publishing a merged KG.
- Therapeutic uses are **traditional claims** digitised from books, not clinical evidence. Targets are in vitro.
- Target coverage is sparse: 2,944 of 18,314 compounds have any target.
- Plant–compound links carry no concentrations.
- There are no food or culinary labels. To tell culinary plants from purely medicinal ones you need common
  names or a join to a food dataset.
- Release-day download links pointed to a non-existent folder. Re-check later: the file contents may change
  if the site is updated.
