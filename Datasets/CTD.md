---
title: "CTD"
slug: ctd
kind: [compound]
version: "Monthly release, files generated 2026-08-28 (described in the 'update 2025' NAR paper)"
previous_versions: "Update 2023 (NAR gkac833), update 2021 (gkaa891), update 2019 (gky868) and earlier yearly/biennial updates since 2004"
papers: ["[[Davis2025 - CTD 20th anniversary update 2025]]"]
url: "https://ctdbase.org/"
license: "Free for non-commercial use under CTD terms (cite CTD, link back to CTD pages, notify CTD of use); commercial use needs a licence"
availability: open-download
access_link: "https://ctdbase.org/downloads/"
accessed: partial
access_method: [website-download]
access_date: 2026-09-30
access_notes: "Direct TSV.gz downloads from https://ctdbase.org/reports/ work with curl (no login, no captcha). Fetched CTD_chemicals (10.6 MB gz), CTD_chemicals_diseases (162 MB gz, 9,876,631 rows) and CTD_chem_gene_ixns (43 MB gz, 3,158,204 rows, 633 MB unzipped). To stay under ~500 MB we kept: the full chemical vocabulary; only the 109,665 chemical–disease rows with DirectEvidence (curated), leaving out the ~9.77 M gene-inferred rows; and only the 1,329,897 Homo sapiens chemical–gene interactions. The '#' comment headers were stripped. Gene–disease, pathway, phenotype and exposure files were not downloaded."
countries: []
regions: ["[[Global]]"]
n_records: "179,669 chemicals · 109,665 curated chemical–disease associations (10,744 chemicals × 3,326 diseases) · 1,329,897 human chemical–gene interactions (11,103 chemicals × 28,629 genes)"
size: "312 MB (uncompressed TSV subset)"
formats: [tsv, csv, xml]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Curated chemical→disease associations with DirectEvidence 'therapeutic' (a known or possible therapeutic role) or 'marker/mechanism' (the chemical correlates with or may cause the disease) plus PubMed IDs; curated chemical→gene interactions (increases/decreases expression, activity, binding…) give mechanisms; gene-inferred chemical→disease links with an InferenceScore are in the full file."
join_keys: [MeSH chemical id, CAS RN, PubChem CID, InChIKey, DTXSID, MeSH/OMIM disease id, NCBI Gene id, PubMed id]
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
---
# CTD

> [!abstract] TL;DR
> The Comparative Toxicogenomics Database (NC State University) is curated by hand from more than 149,000 papers. It
> links chemicals to genes, phenotypes and diseases, and a further 48 M relationships are inferred from those links.
> It has no food or culture labels. For the agent it is the **chemical → disease evidence layer** that food
> composition resources lack: take a compound found in a food (via [[FoodAtlas]], [[HMDB]] or FooDB) and CTD gives
> curated "therapeutic" or "marker/mechanism" associations with PubMed IDs. [[FoodAtlas]] builds its chemical–disease
> edges from exactly this file, and our curated subset (109,665 rows) is what a FoodAtlas rebuild needs.

## Access
| | |
|---|---|
| Availability | open-download (TSV/CSV/XML gz, monthly; free for non-commercial use under CTD terms) |
| Link | https://ctdbase.org/downloads/ → `https://ctdbase.org/reports/<file>.tsv.gz` |
| Accessed? | partial (full chemical vocabulary; the curated part of chemical–disease; the human part of chemical–gene) |
| How | `curl -L https://ctdbase.org/reports/CTD_chemicals_diseases.tsv.gz` etc., then `awk` filters (DirectEvidence ≠ "" / Organism = Homo sapiens) |
| Downloaded | `Data/ctd/CTD_chemicals.tsv`, `CTD_chemicals_diseases_curated.tsv`, `CTD_chem_gene_ixns_human.tsv` (312 MB total) |

## Tables & columns
Column meanings come from the CTD download page (https://ctdbase.org/downloads/) and the file headers.

### `CTD_chemicals.tsv` (179,669 rows) — chemical vocabulary (MeSH-based)
| column | type | meaning | example |
|---|---|---|---|
| `ChemicalName` | str | preferred name | `Curcumin` |
| `ChemicalID` | str | MeSH identifier, with `MESH:` prefix | `MESH:D003474` |
| `CasRN` | str | CAS registry number | `458-37-7` |
| `PubChemCID` | str | PubChem compound id (`CID:` prefix; 11,684 filled) | `CID:969516` |
| `PubChemSID` | str | PubChem substance id | `SID:53788771` |
| `DTXSID` | str | EPA CompTox id | `DTXSID8031077` |
| `InChIKey` | str | structure key (9,134 filled) | `VFLDPWHFBUODDF-FCXRPNKRSA-N` |
| `Definition` | str | MeSH scope note | — |
| `ParentIDs`, `TreeNumbers`, `ParentTreeNumbers` | str | MeSH hierarchy (`\|`-separated) | — |
| `MESHSynonyms`, `CTDCuratedSynonyms` | str | synonyms (`\|`-separated) | `diferuloylmethane\|turmeric yellow…` |

### `CTD_chemicals_diseases_curated.tsv` (109,665 rows) — curated chemical–disease associations
| column | type | meaning | example |
|---|---|---|---|
| `ChemicalName` | str | chemical | `Curcumin` |
| `ChemicalID` | str | MeSH id **without** prefix (unlike `CTD_chemicals.tsv`) | `D003474` |
| `CasRN` | str | CAS number | `458-37-7` |
| `DiseaseName` | str | MEDIC disease term (MeSH + OMIM) | `Diabetes Mellitus, Type 2` |
| `DiseaseID` | str | `MESH:` (109,634) or `OMIM:` (31) id | `MESH:D003924` |
| `DirectEvidence` | str | `therapeutic` (39,800) = known or possible therapeutic role; `marker/mechanism` (69,865) = the chemical correlates with the disease or may be part of its cause | `therapeutic` |
| `InferenceGeneSymbol`, `InferenceScore` | str/float | empty in curated rows (filled only in the gene-inferred rows we dropped) | — |
| `OmimIDs` | str | OMIM ids for the disease | — |
| `PubMedIDs` | str | supporting papers (`\|`-separated) | `18403477` |

### `CTD_chem_gene_ixns_human.tsv` (1,329,897 rows) — curated chemical–gene interactions, Homo sapiens only
| column | type | meaning | example |
|---|---|---|---|
| `ChemicalName`, `ChemicalID`, `CasRN` | str | chemical (MeSH id without prefix) | `Curcumin`, `D003474` |
| `GeneSymbol`, `GeneID` | str/int | NCBI gene | `AARS1` |
| `GeneForms` | str | gene product involved (mRNA, protein…) | `mRNA` |
| `Organism`, `OrganismID` | str/int | species of the experiment (all `Homo sapiens`, 9606 here) | `Homo sapiens` |
| `Interaction` | str | curated sentence | `Curcumin results in decreased expression of AARS1 mRNA` |
| `InteractionActions` | str | `action^type` codes; the most common are `increases^expression` (523k), `decreases^expression` (434k), `affects^cotreatment` (308k), `decreases^reaction` (152k) | `decreases^expression` |
| `PubMedIDs` | str | supporting papers | `17198877` |

Sample: `Data/ctd/sample.csv` (+ `sample_CTD_*.csv`) · full profile: `Data/ctd/schema.md`

## Countries & cultures covered
None: this is a global chemical–gene–disease resource with no food, cuisine or country labels (`countries: []`,
`[[Global]]`). Country data exists only in CTD's *Exposure* module (exposure studies with the study country), which
we did not download.

## Inferring effects on the body
**Direct.** `DirectEvidence` on the curated chemical–disease rows is the effect statement, with PubMed provenance:
- `therapeutic` → "may help / treats". [[FoodAtlas]] maps it to `NEGATIVELY_CORRELATED` ("improves").
- `marker/mechanism` → "associated with / may worsen". FoodAtlas maps it to `POSITIVELY_CORRELATED`.
- Mechanism: human chemical–gene interactions (`InteractionActions`).

Evidence type: manual curation of the literature. Most of the literature is laboratory work (cell lines, rodents);
some is clinical. CTD does not record study type per association, so "therapeutic" is **not** proof of clinical
benefit.

**Example chain (green tea / turmeric, both everyday in South & East Asia and the Gulf):**
| food (from a food–compound DB) | compound | CTD row | evidence |
|---|---|---|---|
| green tea | epigallocatechin gallate (`MESH:C045651`, CID 65064, InChIKey `WMBWREPUVVBILR-WIYYLYMNSA-N`) | → Breast Neoplasms `MESH:D001943`: `therapeutic` (PMID 10518005) **and** `marker/mechanism` (PMID 22307971); → Diabetes Mellitus, Type 2 `therapeutic` (PMID 16988119); → Colorectal Neoplasms `therapeutic` (PMID 20346928) | 77 curated EGCG–disease rows (67 therapeutic, 10 marker/mechanism) |
| turmeric | curcumin (`D003474`) | → Diabetes Mellitus, Type 2 `therapeutic` (PMID 18403477); → Breast Neoplasms `therapeutic` (5 PMIDs); → Alzheimer Disease `therapeutic` (PMID 15590663) | 160 curated curcumin–disease rows (156 therapeutic, 4 marker/mechanism); 2,077 human curcumin–gene interactions |

The food → compound step is *not* in CTD: it comes from [[FoodAtlas]] (literature-extracted "contains" edges),
[[HMDB]] (ChemFOnt "Source > Biological > Plant > …") or FooDB. Population-level evidence for the same compounds
(tea catechins in Shanghai/JPHC cohorts) is in [[Exposome-Explorer]].

## Linking to other datasets
- **MeSH chemical id**: the key [[FoodAtlas]] uses to attach CTD disease edges (`ChemicalID`). To join the
  disease/gene files to `CTD_chemicals.tsv`, add the `MESH:` prefix to their `ChemicalID`.
- **PubChem CID / InChIKey** (from `CTD_chemicals.tsv`): join to [[HMDB]] (`pubchem_compound_id`, `inchikey`),
  [[Exposome-Explorer]] (`PubChem ID`, `InChIKey`), [[IMPPAT]] and FooDB. Only 11,684 of 179,669 CTD chemicals have a
  CID and 9,134 an InChIKey, so name/CAS matching is often needed.
- **CAS RN**: also in HMDB and Exposome-Explorer.
- **MeSH/OMIM disease ids**: can be mapped to ICD/UMLS for clinical wording.

## Versions
- Monthly data releases; the files used here were generated on 2026-08-28 (header "Report created").
- The latest paper is the 20th-anniversary "update 2025" (NAR 2025, online 2024-10-10). As of August 2024 it reported
  3.8 M curated interactions from >149,000 articles, 48 M inferred relationships and 94 M relationships in total;
  it added PubTator NLP in curation, a new Exposure Curation Tool, and better Tetramers and Pathway View tools.
  The previous paper was "update 2023" (gkac833).

## Caveats
- Curation mostly covers toxicology and pharmacology. Dietary doses, bioavailability and direction of effect in
  humans are not recorded, and the same pair can carry both evidence types (EGCG–breast cancer).
- The dropped gene-inferred rows (~9.77 M) are hypotheses (chemical–gene + gene–disease), not direct evidence.
- Licence: non-commercial use is free, but publications and apps must cite and link CTD and notify CTD. FoodAtlas
  does not redistribute CTD tables for this reason ("CTD edges must be rebuilt" locally).
