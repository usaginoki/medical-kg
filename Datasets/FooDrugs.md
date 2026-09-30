---
title: "FooDrugs"
slug: foodrugs
kind: [compound]
version: "v4 (FinalFooDrugs_v4.sql, 28 July 2023; Zenodo record 8192515, 'version 4.0.0')"
previous_versions: "v2 (FinalFooDrugs_v2.sql, 2022-06); v3 (FinalFooDrugs_v3.sql, 2023-01-31); same Zenodo record, concept DOI 10.5281/zenodo.6638469"
papers: ["[[LacruzPleguezuelos2023 - FooDrugs food-drug interactions database]]"]
url: "https://doi.org/10.5281/zenodo.6638469"
license: "CC BY 4.0"
availability: open-download
access_link: "https://zenodo.org/records/8192515"
accessed: true
access_method: [zenodo]
access_date: 2026-09-30
access_notes: "Streamed the 1.56 GB MySQL dump FinalFooDrugs_v4.sql from Zenodo and parsed the INSERT statements into CSV without a MySQL server. All 10 tables were parsed. To stay under 500 MB, the following were cut down: `texts` is kept as metadata plus the first 300 characters (full text only for the 537 DrugBank/drugs.com documents); `cmap_foodrugs` is filtered to |tau| > 90 (the paper's threshold; 2.43 M of 26.4 M rows); `topTable` keeps its first 100,000 of 2.8 M rows. Full CSVs of all tables remain in the session scratchpad only."
countries: []
regions: ["[[Global]]"]
n_records: "1,108,429 text-mined food–drug mentions from 439,338 documents; 26.4 M food-condition × CMap tau scores (2,434,671 with |tau| > 90); 150 GEO studies / 4,559 samples"
size: "1.56 GB SQL (v4); 283 MB kept as CSV"
formats: [sql, csv]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: linkable
body_effect_how: "Text module: food string + drug string + character span in a PubMed/ClinicalTrials/DrugBank/drugs.com document (the span holds the effect sentence); transcriptomic module: food-condition signature vs CMap drug signature tau score. No effect grade or ontology ids; PMIDs/NCT ids link to evidence."
join_keys: [PMID, NCT id, DrugBank ID (in DrugBank-sourced links), GEO accession (GSE/GSM), Entrez gene id, CMap/LINCS perturbagen name, food/drug free-text name]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
found_by: [search/compounds]
tags:
  - type/dataset
  - kind/compound
  - q/3
  - access/accessed
  - access/open
  - region/global
---
# FooDrugs

> [!abstract] TL;DR
> FooDrugs is a very large, **automatically generated** catalogue of *potential* food–drug interactions, built by the IMDEA Food Institute (Madrid) for the EU FNS-Cloud project and released on Zenodo as a MySQL dump (CC BY 4.0). It has two modules:
> 1. **Text mining.** 1,108,429 food–drug mentions from 439,338 documents: PubMed 425,023, ClinicalTrials.gov 13,778, DrugBank 285 and drugs.com 252. The paper counts those 537 as the "DDI corpus" documents; 285 + 252 = 537 is our inference. Each mention stores the food string, the drug string and the character span of the evidence sentence.
> 2. **Transcriptomics.** 150 human GEO studies of foods or bioactives, compared with Connectivity Map (CMap) drug signatures, giving 2.43 M food-condition × drug links with |tau| > 90.
>
> There is no manual grading, no ontology IDs and no country dimension. For the agent it is a high-recall literature index ("has anyone written about fenugreek + metformin?") that points to PMIDs. Graded advice should come from [[DDID]] or [[DrugBank]].

## Access
| | |
|---|---|
| Availability | open-download (Zenodo, CC BY 4.0, no login) |
| Link | https://zenodo.org/records/8192515 (files `FinalFooDrugs_v2.sql` 1.36 GB, `_v3.sql` 0.94 GB, `_v4.sql` 1.56 GB) |
| Accessed? | yes. The full v4 dump was parsed; a reduced set is kept |
| How | `curl -L ".../FinalFooDrugs_v4.sql?download=1" \| python sqlparse.py` (streaming parser of the MySQL INSERTs into one CSV per table) |
| Downloaded | `Data/foodrugs/` (283 MB): `TM_interactions.csv` (full), `texts_meta.csv` (all 439,338 docs: id, source, link, citation, first 300 chars), `texts_drugbank_drugscom_full.csv` (537 full documents), `cmap_foodrugs_abs_tau_gt90.csv`, `cmap.csv`, `nodes.csv`, `geo_sample.csv` (the SQL table `sample`, renamed so the profiler does not overwrite it), `study.csv`, `misc_sample.csv`, `misc_study.csv`, `topTable_first100k.csv` |

## Tables & columns
### `TM_interactions.csv` (1,108,429 rows)
One text-mined potential interaction per row.

| column | type | meaning | example |
|---|---|---|---|
| `TM_interactions_ID` | int | interaction id | 1217 |
| `texts_ID` | int | document → `texts` | 530 |
| `start_index` / `end_index` | int | character span of the sentence expressing the interaction in `texts.document` | 0 / 116 |
| `food` | str | food/food-compound entity as written (50,951 distinct) | grapefruit |
| `drug` | str | drug entity as written (161,792 distinct) | felodipine |

The top "foods" are generic nutrients and noise: protein 41,591, calcium 26,457, insulin 16,870, d-glucose 16,568, oxygen, water, and "same" (9,170).

### `texts_meta.csv` (439,338 rows) · `texts_drugbank_drugscom_full.csv` (537 rows)
The SQL table `texts` has the columns `texts_ID`, `document` (title + abstract, or label text; median 1,622 chars), `link` and `citation` (17% filled, PubMed only). The meta file adds `source` (inferred from the link domain: pubmed.ncbi.nlm.nih.gov 425,023 · clinicaltrials.gov 13,778 · go.drugbank.com 285 · drugs.com 252) and keeps `document_head` (first 300 chars). The full-text file keeps the complete `document` for the DrugBank and drugs.com records. drugs.com documents begin with the severity, e.g. "Moderate Food Interaction||GENERALLY AVOID: …".

### Transcriptomic module
| table (rows) | columns | meaning |
|---|---|---|
| `study.csv` (150) | `study_id`, `contributor`, `entrez_id`, `accession` (GSE), `gpl`, `title`, `abstract`, `study_type` (One color array 110 · HTS 29 · Two channel array 11), `publication_date`, `pubmed_id` | GEO series of food/bioactive exposures in humans or human cells |
| `geo_sample.csv` (4,559) | `sample_id`, `study_id`, `treatment` (298 values, e.g. grapefruit juice, glycyrrhizic acid, epigallocatechin gallate, Mediterranean diet, heavy drinking), `origin_type` (tissue 1,856 · cell line 1,593 · cell type 912…), `origin_name`, `GSM`, `time_point`, `concentration` | GEO samples (SQL table `sample`) |
| `misc_study.csv` (192) / `misc_sample.csv` (6,846) | `*_id`, `attribute_name`, `attribute_value` | extra GEO attributes |
| `nodes.csv` (2,617) | `node_id`, `sample_id` | groups samples into conditions (food × time × concentration × origin); 418 nodes |
| `topTable_first100k.csv` (100,000 of 2,799,422) | `entrez_Id`, `logFC`, `AveExpr`, `moderated_t`, `P_value`, `adjusted_P_value`, `B`, `node_id`, `geneSet` (up/down), `top150` | limma differential expression per condition |
| `cmap.csv` (70,895) | `cmap_node_id`, `cell_line` (9), `compound` (6,395 perturbagens), `pert_type` (trt_cp = compound 21,869; trt_sh.cgs = knock-down 30,292; trt_oe = over-expression 18,716) | CMap/LINCS signatures |
| `cmap_foodrugs_abs_tau_gt90.csv` (2,434,671 of 26,365,254) | `node_id`, `cmap_node_id`, `tau` (−100…100) | connectivity of a food condition with a CMap signature: positive tau = similar transcriptional effect, negative = opposite (per CMap docs) |

Sample: `Data/foodrugs/sample.csv` · full profile: `Data/foodrugs/schema.md`

## Countries & cultures covered
None. The data has no country or cuisine labels (`countries: []`, `[[Global]]`). Foods are free-text entities from the literature. Region-relevant foods do occur, though noisily (text-module rows / distinct documents): grapefruit 891 / 438, green tea 741 / 467, liquorice 175 / 124, turmeric or curcumin 2,900 / 1,536, fenugreek 88 / 61, "date palm/dates" 110 / 81 (mostly agronomy noise), pomegranate 175 / 118, Nigella / black seed 96 / 68, saffron 21 / 15, cinnamon 143 / 99. The GEO module includes a Mediterranean-diet study, and the treatments include grapefruit juice, glycyrrhizic acid, curcuminoid and green-tea extracts, and EGCG.

## Inferring effects on the body
**Linkable, low precision.** No field states an effect or its direction. The effect sits in the evidence sentence (`texts.document[start_index:end_index]`) and in the cited PMID. The relation model had F1 0.77 on its test corpus. Evidence types: literature text-mining, drug labels (DrugBank, drugs.com), and transcriptomic similarity (hypothesis only).

Examples found in the data (TM row → evidence span):

| food | drug | source | evidence sentence (span) |
|---|---|---|---|
| grapefruit | felodipine | DrugBank DB01023 | "Co-administration of CYP3A4 inhibitors (eg, … grapefruit juice …) with felodipine may lead to several-fold increases in the plasma levels of felodipine" |
| green tea | nadolol | drugs.com | "Moderate Food Interaction\|\|GENERALLY AVOID: Coadministration with green tea may significantly decrease the plasma concentrations of nadolol." |
| licorice | spironolactone | PMID 17113210 | "the activation of the renin-aldosterone system was significantly lower during spironolactone plus licorice than with spironolactone alone" |
| turmeric | tacrolimus | PMID 28104136 | "a probable food-drug interaction between the herb turmeric and tacrolimus leading to acute calcineurin inhibitor nephrotoxicity" (the same case is graded *Harmful* in [[DDID]]) |
| fenugreek | metformin | PMID 35424379 | "concomitant administration of fenugreek extract with metformin maintains lower blood glucose levels than metformin alone" |
| Nigella sativa oil | gliclazide | PMID 34327715 | "higher systemic exposures of gliclazide by modulating bioavailability (29% increase) and clearance (20% decrease)" |
| pomegranate | warfarin | PMID 20029019 | "We report a potential interaction between pomegranate juice and warfarin." |
| date palm | ozone | PMID 34601178 | "Chronic ozone exposure preferentially modifies root … metabolism of date palm" (false positive: "drug" = ozone) |

Transcriptomic example: glycyrrhizic acid (MCF7 cells, node 201) vs warfarin (HEPG2) gives tau −93.5. EGCG (MCF7) vs cyclosporin-A gives tau −97.2. Grapefruit juice (PBMC, node 667) has 889 links with |tau| > 90 but none to the classic CYP3A4 substrates, which shows that transcriptional similarity does not capture pharmacokinetic interactions.

## Linking to other datasets
- `texts.link` → PMID / NCT id / DrugBank ID. The PMIDs join to `PMID` in [[DDID]], so a text-mined mention can be upgraded to a curated, graded DDID record. The 285 DrugBank documents are keyed by DrugBank ID ([[DrugBank]]).
- Food and drug strings need normalisation before joining, e.g. to FooDB or PubChem names, DrugBank vocabulary or ATC.
- GEO accessions and Entrez genes link to expression resources. CMap compound names link to LINCS or PubChem.

## Versions
- **v2** (2022-06): 6,422 text interactions from 2,849 documents (2,312 PubMed, 285 DrugBank, 252 drugs.com); 161 GEO series.
- **v3** (2023-01-31): +85,675 documents (PubMed, ClinicalTrials.gov), +168,826 interactions; +32 GEO series, 43 non-food series removed; tau = 0 rows dropped; new columns `texts.citation`, `study.contributor/publication_date/pubmed_id`, `topTable.top150`.
- **v4** (2023-07-28, latest, the one used here): +439,338 documents (PubMed, ClinicalTrials.gov, DDI corpus), +1,108,429 text-mined interactions (the counts in the paper).

## Caveats
- NER noise: "foods" include protein, insulin, oxygen, water and "same"; "drugs" include ozone, "arabic" and "covid-19". Filter against a food vocabulary before use.
- The count of |tau| > 90 links in v4 (2,434,671) differs slightly from the paper's 2,321,633.
- The transcriptomic links compare cell-line signatures, so they are not clinical interactions.
- The DrugBank and drugs.com documents are copies of proprietary label text; check the terms before redistributing.
