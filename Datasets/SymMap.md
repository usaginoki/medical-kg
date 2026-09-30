---
title: "SymMap"
slug: symmap
kind: [ingredient, compound]
version: "2.0 (web copyright 2022; no v2 paper found)"
previous_versions: "1.0 (Wu et al., NAR 2019; 499 herbs, 1,717 TCM symptoms, 961 MM symptoms, 19,595 ingredients, 4,302 targets, 5,235 diseases)"
papers: ["[[Wu2019 - SymMap TCM database with symptom mapping]]"]
url: "http://www.symmap.org/"
license: "not stated on the site; the v1 paper is CC BY-NC 4.0"
availability: open-download
access_link: "http://www.symmap.org/download/"
accessed: true
access_method: [website-download, scrape]
access_date: 2026-09-30
access_notes: "All 14 v2.0 entity files (7 description files + 7 search-key files, xlsx) downloaded. The download page has NO association files: herb–symptom, herb–ingredient, ingredient–target and all inferred relations are only reachable through the web detail pages. We fetched those for 8 medicine-food herbs (48 POST requests to the undocumented /related_components/ JSON endpoint, 1 req/s). Full relation tables would need a larger crawl (698 herbs × 6 relation types) or a request to the authors."
countries: ["[[China]]"]
regions: ["[[East Asia]]"]
n_records: "698 herbs · 2,285 TCM symptoms · 1,148 MM symptoms · 233 syndromes · 26,035 ingredients · 20,965 targets · 14,086 diseases (active, non-suppressed rows)"
size: "12 MB (14 xlsx) + 2.5 MB scraped relations"
formats: [xlsx, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Herb → TCM symptom (Chinese Pharmacopoeia indications, expert-curated) → modern-medicine (MM) symptom (UMLS, expert mapping) → disease (HPO/OMIM); herb → ingredient → target → disease (database integration + Fisher's-exact-test inference with P/FDR). Relations are on the web only."
join_keys: [PubChem CID, CAS, TCMSP id, TCMID id, TCM-ID id, HERB id, UMLS CUI, MeSH id, OMIM id, ICD-10-CM, HPO id, Ensembl gene id, HGNC id, UniProt, Latin herb name]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
---
# SymMap

> [!abstract] TL;DR
> SymMap (Beijing University of Chinese Medicine, ICT-CAS, Beijing Jiaotong University) links the **698 herbs
> of the Chinese Pharmacopoeia** to **2,285 TCM symptoms**, which a 17-expert committee mapped to **1,148
> modern-medicine symptoms** (UMLS). It then connects herbs to **26,035 ingredients**, **20,965 targets** and
> **14,086 diseases**. v2.0 adds TCM **syndromes** (233). It is the cleanest resource for the
> *traditional claim → modern symptom* step, e.g. fresh ginger (生姜) → vomiting (呕吐) → *Emesis* (UMLS).
> The bulk files are entity lists only; the relations have to be pulled from the web pages.

## Access
| | |
|---|---|
| Availability | open download (entity tables); relations browse-only |
| Link | http://www.symmap.org/download/ |
| Accessed? | yes: all v2.0 entity tables; relations partial (8 herbs scraped) |
| How | `curl` of `/static/download/V2.0/SymMap v2.0, <TABLE> file.xlsx`; POST `rrid=<SMHB id>&table_name=<Syndrome\|TCM_symptom\|MM_symptom\|Mol\|Gene\|Disease>&filter=0` to `/related_components/` |
| Downloaded | `Data/symmap/`: 14 xlsx (renamed `symmap_v2_<TABLE>[_key].xlsx`), 12 MB; `Data/symmap/scrape/`: 6 relation CSVs for 8 herbs |

The scraped herbs (all "medicine-food" herbs): 生姜 fresh ginger (SMHB00367), 干姜 dried ginger (SMHB00136),
大枣 jujube (SMHB00090), 枸杞子 goji (SMHB00143), 肉桂 cassia bark (SMHB00340), 姜黄 turmeric (SMHB00198),
山楂 hawthorn (SMHB00515), 山药 Chinese yam (SMHB00359).

## Tables & columns
Every component has a *description file* and a *key file* (`<id>, Field_name, Field_context`: search aliases,
e.g. Chinese/Pinyin/Latin/English names for herbs, CAS and aliases for ingredients). `Suppress = 1` marks
terms discarded in v2 (with `Link_*_id` pointing to the replacement). `Version` = `v1`, `v2` or `v1,v2`.
Column meanings follow the download page's "File formats" section.

### `symmap_v2_SMHB.xlsx`: herbs (703 rows, 698 active)
| column | type | meaning | example |
|---|---|---|---|
| `Herb_id` | int | SymMap herb id (web id `SMHB00367`) | 367 |
| `Chinese_name`, `Pinyin_name` | str | herb name | 生姜, Shengjiang |
| `Latin_name`, `English_name` | str | pharmacopoeial Latin name(s); English name | Zingiberis Rhizoma Recens; Fresh Ginger |
| `Properties_Chinese/_English` | str | TCM nature and flavour | Pungent, Slightly Warm |
| `Meridians_Chinese/_English` | str | TCM meridians entered | Lung, Spleen, Stomach |
| `Class_Chinese/_English` | str | TCM therapeutic class (47 classes) | Pungent-Warm Exterior-Releasing Medicinal |
| `UsePart` | str | part used (40% filled) | fresh rhizome |
| `TCMID_id`, `TCM-ID_id`, `TCMSP_id`, `HERBDB_ID` | id | cross-references to other TCM databases | HERB005017 |
| `Alias`, `Link_herb_id`, `Suppress` | | aliases; replacement id; discarded flag | |

The download page also documents a `Function` column (TCM function text); it is not in the v2 file.

### `symmap_v2_SMTS.xlsx`: TCM symptoms (2,364 rows, 2,285 active)
| column | type | meaning | example |
|---|---|---|---|
| `TCM_symptom_id` | int | id (`SMTS…`) | 755 |
| `TCM_symptom_name`, `Symptom_pinYin` | str | symptom term | 呕吐, Ou Tu |
| `Symptom_definition` | str | Chinese definition (31%) | 是以胃失和降，气逆于上所致… |
| `Symptom_locus` | str | body location | 胃 (stomach) |
| `Symptom_property` | str | TCM pathomechanism | 胃气上逆 |
| `Type` | str | Ontological terms / Synonymous terms | Ontological terms |

### `symmap_v2_SMMS.xlsx`: modern-medicine symptoms (1,148 rows)
| column | type | meaning | example |
|---|---|---|---|
| `MM_symptom_id`, `MM_symptom_name` | | UMLS-based symptom | Postoperative Pain |
| `MM_symptom_definition` | str | definition with source (MeSH/HPO) | MSH2017_…:Pain during the peri… |
| `UMLS_id`, `MeSH_id`, `MeSH_tree_numbers`, `ICD10CM_id`, `HPO_id`, `OMIM_id` | id | cross-references | C0030201, G89.18, HP:0000988 |

### `symmap_v2_SMSY.xlsx`: syndromes, new in v2 (233 rows)
`Syndrome_id`, `Syndrome_name` (下元虚冷), `Syndrome_English` (deficiency-cold of kidney), `Syndrome_PinYin`,
`Syndrome_definition` (Chinese), `Type` = Summarized terms (a syndrome is a group of co-occurring symptoms).

### `symmap_v2_SMIT.xlsx`: ingredients (27,690 rows, 26,035 active)
| column | type | meaning | example |
|---|---|---|---|
| `Mol_id` | int | ingredient id (`SMIT…`) | 159 |
| `Molecule_name` | str | first PubChem name | 6-Gingerol |
| `PubChem_CID` | str | PubChem CID(s), `\|`-separated (42%) | 442793 |
| `Molecule_formula`, `Molecule_weight` | | formula, MW | C17H26O4 |
| `OB_score` | float | predicted oral bioavailability (%) (51%) | 35.6 |
| `CAS_id`, `TCMID_id`, `TCM-ID_id`, `TCMSP_id` | id | cross-refs | MOL…  |
| `Type` | str | herb–ingredient evidence type: Other (23,607) / Blood (2,226, detected in blood) / Metabolic (1,263, metabolites) / QC (407, pharmacopoeia quality-control markers) | Other ingredients |

### `symmap_v2_SMTT.xlsx`: targets (20,965 rows)
`Gene_id`, `Gene_symbol` (A2M), `Gene_name`, `Protein_name`, `Chromosome`, plus ids `HIT_id`, `TCMSP_id`,
`Ensembl_id` (82%), `NCBI_id`, `HGNC_id` (89%), `UniProt_id`, `PDB_id`, `MIM_id`, `Vega_id`, `GenBank_*`,
`miRBase_id`, `IMGT/GENE-DB_id`.

### `symmap_v2_SMDE.xlsx`: diseases (14,434 rows, 14,086 active)
`Disease_id`, `Disease_Name`, `Disease_definition` (53%), `UMLS_id` (98%), `MeSH_id`, `OMIM_id`, `Orphanet_id`,
`ICD10CM_id` (26%), `MedDRA_id`.

### Scraped relations: `scrape/herb_<type>_relations.csv` (8 herbs)
| file | rows | key columns |
|---|---|---|
| `herb_syndrome_relations.csv` | 45 | `Syndrome_id`, `Syndrome_name`, `Syndrome_English` |
| `herb_tcm_symptom_relations.csv` | 364 | `TCM_symptom_id`, `TCM_symptom_name`, `Symptom_pinyin`, `Symptom_locus`, `Symptom_property`, `Type` |
| `herb_mm_symptom_relations.csv` | 358 | `MM_symptom_name`, `UMLS_id`, `Relationship` (all `By_TCM_symptom`), `Value`, `P_value`, `FDR(BH)`, `FDR(Bonferroni)` |
| `herb_ingredient_relations.csv` | 2,373 | `MOL_id`, `Molecule_name`, `PubChem_CID`, `OB_score`, `score` (inferred), `type`/`evidence` (raw HTML: blood/metabolic tags and literature snippets) |
| `herb_target_relations.csv` | 6,113 | `Gene_symbol`, `UniProt_id`, `Relationship` (`By_ingredient`), `P_value`, FDRs |
| `herb_disease_relations.csv` | 5,798 | `Disease_name`, `OMIM_id`, `Relationship` (`By_MM_symptom` / `By_ingredient` / both), `P_value`, FDRs |

`source_herb_id`/`source_herb` were added by us. Sample: `Data/symmap/sample.csv` · full profile: `Data/symmap/schema.md`

## Countries & cultures covered
- **[[China]]**: 698 herbs, all from the Chinese Pharmacopoeia (2015 and 2020 editions) plus standard Chinese
  materia medica references. Symptom and syndrome terms are TCM (Chinese) concepts with Chinese definitions.
- No other country labels. Many herbs are shared with Korean and Japanese medicine (see [[TM-MC]]) and many are
  foods across Asia (ginger, jujube, goji, cinnamon, hawthorn, yam, turmeric).
- **Medicine-food homology is not flagged.** There is no "food" or 药食同源 field; `Class_English` is a TCM
  therapeutic class (e.g. "Digestants"), and `UsePart` does not distinguish culinary use. A food flag would have
  to come from the Chinese NHC medicine-food homology list or from [[KNApSAcK Family]] (edible vs medicinal).

## Inferring effects on the body
`body_effect: direct`. There are three kinds of evidence, which should be kept apart:
1. **Traditional claim, expert-curated**: herb → TCM symptom (from Chinese Pharmacopoeia indications), and
   TCM symptom → MM symptom (UMLS). The mapping was done by a 17-expert committee, with at least 2 of 3
   experts agreeing.
2. **Database integration**: herb → ingredient (TCMSP/TCMID/TCM-ID/HIT/HERB/DCABM-TCM), ingredient → target
   (HIT, TCMSP), target → disease (HPO, OMIM).
3. **Statistical inference**: herb → MM symptom, herb → target and herb → disease, via Fisher's exact test over
   an intermediate component, reported with `P_value`, `FDR(BH)` and `FDR(Bonferroni)`. Herb → MM symptom
   pairs are kept without a test. These are hypotheses, not evidence of effect.

Example chain (scraped data):
**Fresh ginger 生姜 (SMHB00367)**, Pungent/Slightly Warm, meridians Lung/Spleen/Stomach →
- ingredient **6-Gingerol** (SMIT00159, PubChem 442793, OB 35.6), plus 6-shogaol, zingiberene and 553 other
  ingredients;
- TCM symptoms 呕吐 *Ou Tu* (vomiting), 胃寒呕吐 (vomiting from stomach cold), 咳嗽 (cough), 感冒 (common
  cold), 鱼蟹中毒 (fish/crab poisoning);
- → MM symptoms *Emesis*, *Cough*, *Common Cold*, *Gastric Disorder* (P = 0.023), *Food Poisoning*;
- → diseases (872 inferred, e.g. *Bipolar Disorder*, P = 2.2e-24, via MM symptom + ingredient): statistically
  significant but clinically implausible, which shows why the inferred layer needs filtering.

## Linking to other datasets
- `HERBDB_ID` (646 herbs) → [[HERB]] herb ids (e.g. HERB005017 = fresh ginger); HERB also stores `SymMap_id`.
- `PubChem_CID`/`CAS_id` → [[FooDB]], [[TM-MC]] (CID/InChIKey), [[IMPPAT]], [[CTD]], [[DrugBank]].
- Latin pharmacopoeial name (`Zingiberis Rhizoma Recens`) → [[TM-MC]] `LATIN`, which is the same naming scheme.
  To join to food datasets you have to map to the binomial (*Zingiber officinale*).
- `UMLS_id`/`MeSH_id`/`ICD10CM_id`/`HPO_id` → disease vocabularies in [[CTD]] and [[HERB]] (DisGeNET CUIs).
- Gene `Ensembl_id`/`HGNC_id`/`UniProt_id` → [[CTD]], [[DrugBank]], [[TM-MC]] (STITCH ENSP via Ensembl).

## Versions
| version | herbs | TCM symptoms | MM symptoms | syndromes | ingredients | targets | diseases |
|---|---|---|---|---|---|---|---|
| 1.0 (NAR 2019) | 499 | 1,717 | 961 | – | 19,595 | 4,302 | 5,235 |
| **2.0** (site © 2022) | **698** | **2,285** | **1,148** | **233** | **26,035** | **20,965** | **14,086** |

What v2.0 adds (download page and `Version` column): herbs from the 2020 Chinese Pharmacopoeia and other
materia medica; the new syndrome component; ingredients also from HERB and DCABM-TCM; targets also from HERB;
diseases also from MalaCards and UMLS; the herb–ingredient evidence `Type` (QC/blood/metabolic). No v2 paper
was found (Europe PMC search, 2026-09-30).

## Caveats
- **No bulk relations**: the download is entity tables only. Any KG use needs a crawl of
  `/related_components/` (about 4,200 requests for all herbs) or a data request to the authors.
- Inferred herb–disease and herb–target links are ranked by P-value and include many implausible hits.
- TCM symptom definitions are in Chinese only; MM symptom names are UMLS strings (some are odd, e.g.
  "Poisoning By").
- Scraped `type`/`evidence` columns contain raw HTML.
- No licence is stated for the data; the paper is CC BY-NC.
