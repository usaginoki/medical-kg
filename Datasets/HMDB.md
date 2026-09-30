---
title: "HMDB"
slug: hmdb
kind: [compound]
version: "5.0 (metabolite XML dated 2021-10-23; <version>5.0</version> in every record)"
previous_versions: "1.0 (2007), 2.0 (2009), 3.0 (2013), 3.5, 4.0 (2018, NAR gkx1089; 114,100 compounds)"
papers: ["[[Wishart2022 - HMDB 5.0]]"]
url: "https://hmdb.ca/"
license: "Free for non-commercial use with citation (HMDB terms; data described as CC BY-NC 4.0 in redistributions); commercial use needs permission"
availability: open-download
access_link: "https://hmdb.ca/downloads"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "hmdb.ca/downloads and every /system/downloads file sit behind a Cloudflare managed challenge: curl and automated Chrome both got 403, and the challenge was not bypassed. The user downloaded the official All Metabolites XML (hmdb_metabolites.zip, 954 MB → hmdb_metabolites.xml, 6.5 GB, dated 2021-10-23) in a browser into Data/hmdb/raw/ (git-ignored). We streamed it with `unzip -p | iterparse` without extracting it and wrote 4 flat CSVs to Data/hmdb/ (261 MB): all 217,920 metabolites (ids, class, cross-refs, food/source ontology, food sentences from the description), their disease links, abnormal concentrations, and the ChemFOnt 'Source' and 'Physiological effect' subtrees. Not kept: spectra, pathways, protein associations, normal concentrations (count only), full descriptions (first 400 chars), synonyms, and the other ontology branches. Alternative source: Zenodo record 20747030 has a third-party frozen copy of the same 5.0 XML (CC BY-NC 4.0) that streams without a browser."
countries: []
regions: ["[[Global]]"]
n_records: "217,920 metabolites (3,385 quantified, 20,924 detected, 98,256 expected, 95,355 predicted) · 27,670 metabolite–disease links (657 diseases, 22,600 metabolites) · 40,635 abnormal-concentration records · 1,150,792 ontology rows"
size: "261 MB (derived CSV; source XML 6.5 GB)"
formats: [xml, csv, sdf]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Metabolite → disease links with OMIM ids and PubMed references (mostly 'altered levels observed in patients', i.e. biomarker associations, not food effects); abnormal concentrations in biofluids by patient condition; ChemFOnt 'Physiological effect > Health effect > Health condition' terms. Food origin comes from ChemFOnt 'Disposition > Source' (Food / Endogenous / Biological > Plant > …) and FooDB ids; the food → disease direction needs CTD or Exposome-Explorer."
join_keys: [HMDB id, FooDB id, PubChem CID, ChEBI id, KEGG id, DrugBank id, Phenol-Explorer id, InChIKey, CAS RN, OMIM id, PubMed id]
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
# HMDB

> [!abstract] TL;DR
> The Human Metabolome Database 5.0 (Wishart lab, University of Alberta) is the reference encyclopaedia of 217,920
> small molecules found in, or expected in, the human body. It includes food-derived compounds: 146,742 carry the
> ChemFOnt source tag "Food" and 74,427 link to FooDB. Each record has identifiers, chemical class, biofluid
> locations, normal and abnormal concentrations, and disease associations with PubMed references. For the agent it is
> the **identifier hub** connecting food composition (FooDB, [[FoodAtlas]]) to human biology ([[CTD]],
> [[Exposome-Explorer]]). Its disease links are **biomarker** associations (altered levels in patients), not "eating X
> helps Y". It has no culture labels. The food-origin annotations are coarse, and a food named in the text is rarely
> a regional one.

## Access
| | |
|---|---|
| Availability | open-download (XML/CSV/SDF, free for non-commercial use), but behind a Cloudflare browser challenge |
| Link | https://hmdb.ca/downloads → `hmdb_metabolites.zip` (All Metabolites, XML) |
| Accessed? | yes: the full metabolite XML, reduced to 4 CSVs |
| How | the user downloaded it in a browser (Cloudflare); then `unzip -p hmdb_metabolites.zip hmdb_metabolites.xml \| python3 hmdb_stream.py Data/hmdb` (ElementTree iterparse) |
| Downloaded | `Data/hmdb/hmdb_metabolites.csv`, `hmdb_metabolite_diseases.csv`, `hmdb_abnormal_concentrations.csv`, `hmdb_ontology_terms.csv` (261 MB); the source zip stays in `Data/hmdb/raw/` |

## Tables & columns
Field meanings come from the HMDB XML element names and the HMDB 5.0 paper. The CSVs were derived by us.

### `hmdb_metabolites.csv` (217,920 rows × 26), one row per metabolite
| column | type | meaning | example |
|---|---|---|---|
| `accession` | str | HMDB id | `HMDB0002269` |
| `name` | str | common name | `Curcumin` |
| `status` | str | evidence of presence in humans: `quantified` (3,385), `detected` (20,924), `expected` (98,256, mostly lipids), `predicted` (95,355) | `quantified` |
| `chemical_formula`, `monisotopic_molecular_weight`, `cas_registry_number`, `inchikey`, `smiles` | str | structure | `VFLDPWHFBUODDF-FCXRPNKRSA-N` |
| `kingdom`, `super_class`, `class`, `sub_class`, `direct_parent` | str | ClassyFire chemical taxonomy | `Phenylpropanoids and polyketides` |
| `pubchem_compound_id`, `chebi_id`, `kegg_id`, `foodb_id`, `drugbank_id`, `phenol_explorer_compound_id` | str | cross-references (PubChem 104,230; FooDB 74,427; Phenol-Explorer 341 filled) | `969516`, `FDB012292` |
| `source_terms` | str | our flattening of ChemFOnt `Disposition > Source` leaves: `Food`, `Endogenous`, `Biological > Plant > <taxon>`, `Biological > Microbe > …`, `Environmental > Tobacco smoke`, `Synthetic > …` (`\|`-separated) | `Biological > Plant > Glycine max\|Food` |
| `food_sentences` | str | sentences from the full description that mention "food(s)". Usually FooDB-derived text such as "found in the highest concentration within … such as …" (6,680 metabolites) | `…detected, but not quantified in, several different foods, such as cassava, shiitakes…` |
| `biospecimens` | str | biofluids where found | `Blood\|Feces\|Urine` |
| `n_diseases`, `n_normal_concentrations`, `n_abnormal_concentrations` | int | counts of linked records | `1` |
| `description` | str | first 400 characters of the description | `Curcumin is a natural component of the rhizome of turmeric…` |

### `hmdb_metabolite_diseases.csv` (27,670 rows × 6)
| column | type | meaning | example |
|---|---|---|---|
| `accession`, `metabolite_name` | str | metabolite | `HMDB0002269`, `Curcumin` |
| `disease_name` | str | disease (657 distinct) | `Colorectal cancer` |
| `omim_id` | str | OMIM id if any | `114500` |
| `n_references`, `pubmed_ids` | int, str | supporting references | `15`, `7482520\|22148915\|…` |

Distribution: 20,020 rows are cardiolipins linked to "3-methylglutaconic aciduria type II, X-linked" (Barth
syndrome). Next come colorectal cancer (831), pregnancy (771), obesity (763), eosinophilic oesophagitis (334),
ulcerative colitis (304) and Crohn's disease (237). Many links come from a few metabolomics studies applied to
hundreds of metabolites.

### `hmdb_abnormal_concentrations.csv` (40,635 rows × 9)
`accession`, `metabolite_name`, `biospecimen`, `concentration_value`, `concentration_units`, `patient_age`,
`patient_sex`, `patient_information` (the condition, e.g. `Colorectal Cancer`, `Pregnancy with fetuses with trisomy
18`), `pubmed_ids`. Example: curcumin, Feces, Adult, Both, Colorectal Cancer, PMID 27275383.

### `hmdb_ontology_terms.csv` (1,150,792 rows × 6), ChemFOnt, 2 branches only
`accession`, `root` (`Disposition` 592,848 rows, restricted to the `Source` subtree; `Physiological effect` 557,944
rows), `path` (e.g. `Physiological effect > Health effect > Health condition > Psychiatric disorders > Agitation`),
`term`, `level`, `type` (parent/child). The most frequent Physiological-effect terms are Organoleptic effect /
Touch / Smooth (89k, a generic template), Health condition (42k), Metabolic syndrome, Cancer, Obesity and
Atherosclerosis (~39–41k each, mostly lipid templates).

Sample: `Data/hmdb/sample.csv` (+ `sample_*.csv`) · full profile: `Data/hmdb/schema.md`

## Countries & cultures covered
None (`countries: []`, `[[Global]]`). There are no country, cuisine or population fields. Biofluid concentrations
come from studies worldwide, but the study country is not recorded.

## Inferring effects on the body
**Direct but weak for diet.** What HMDB offers:
- **Disease links** (`hmdb_metabolite_diseases`): "metabolite X is altered in disease Y" with PubMed ids. The evidence
  is mostly clinical metabolomics (case vs control). This is a *biomarker* signal, not an effect of eating the
  compound. For example, curcumin, caffeine and others all link to colorectal cancer through the same 14 PubMed ids
  (a faecal-metabolome study).
- **Abnormal concentrations**: patient condition, biofluid and value.
- **ChemFOnt health-condition terms**: curated or templated. Caffeine → headache, agitation, confusion, psychosis
  (adverse effects).
- **Food origin**: `source_terms` (Food / Plant taxon) plus `food_sentences` and `foodb_id`. The plant taxa are
  coarse and look templated: the same five (Coffea, Cucurbitaceae, Fabaceae, Poaceae, Theobroma cacao) recur across
  thousands of compounds. EGCG, for instance, is not tagged *Camellia sinensis*, although its description says
  "the principal catechin in tea".

**Example chain (turmeric, used across South Asia and the Gulf, and green tea, East Asia):**
| hop | source | row |
|---|---|---|
| turmeric → curcumin | HMDB `description` | HMDB0002269 "Curcumin is a natural component of the rhizome of turmeric (*Curcuma longa*)…", `source_terms` includes `Food`, FooDB FDB012292, PubChem 969516 |
| curcumin → disease (biomarker) | `hmdb_metabolite_diseases` | Colorectal cancer, OMIM 114500, 15 refs (altered faecal level) |
| curcumin → disease (therapeutic claim) | [[CTD]] via PubChem 969516 / MeSH D003474 | Diabetes Mellitus, Type 2 `therapeutic` (PMID 18403477), 156 other therapeutic links |
| green tea → EGCG | HMDB `description` | HMDB0003153 "EGCG is the principal catechin in tea from Camellia sinensis… a single cup of green tea may contain 100–200 mg EGCG" |
| EGCG → cancer (human cohorts) | [[Exposome-Explorer]] via `HMDB0003153` | breast cancer (JPHC, Japan), gastric cancer (JPHC), liver cancer (Shanghai) |

HMDB lists turmeric compounds (`food_sentences` mentions turmeric for 19 metabolites, e.g. camphene, curzerenone C,
bisabolane sesquiterpenes, mostly `expected`), saffron (12) and cumin (11). "Dates" in the Phoenix-dactylifera sense
appears in only 1 food sentence (myristoleic acid). For dates, FooDB or [[FoodAtlas]] are better.

## Linking to other datasets
- **HMDB id**: [[Exposome-Explorer]] (`HMDB ID`), FooDB, MiMeDB, MarkerDB.
- **FooDB id**: FooDB's food → compound content tables (the missing food hop with concentrations).
- **PubChem CID / InChIKey / CAS**: [[CTD]] (`PubChemCID`, `InChIKey`, `CasRN`), [[FoodAtlas]], [[IMPPAT]].
- **DrugBank id**: [[DrugBank]] (drug–nutrient overlap, e.g. caffeine DB00201).
- **Phenol-Explorer id**: Phenol-Explorer polyphenol content in foods.

## Versions
- **5.0 (NAR 2022, online 2021-11-19; XML dated 2021-10-23), used here and still the current release on
  hmdb.ca.** It grew from 114,100 to 217,920 compounds (oxidised lipids, cardiolipins, blood-exposome compounds,
  3,168 food-derived compounds), rewrote descriptions, and expanded ChemFOnt to 247 subcategories and 221,454
  definitions. It added predicted NMR/MS/RI/CCS spectra and >19,715 new or corrected concentrations. The disease,
  gene and SNP layers were *not* updated.
- 4.0 (2018): 114,100 compounds; introduced ChemFOnt.

## Caveats
- Disease links are biomarker associations dominated by a few large studies and by templated lipid entries
  (Barth-syndrome cardiolipins). Filter `status in (quantified, detected)` and look at `n_references` before using
  them.
- About 88% of entries are `expected` or `predicted`, with no human measurement.
- Plant-source ontology tags are coarse and templated. Use FooDB or FoodAtlas for real food → compound content.
- Licence: non-commercial. The downloads need a browser because of Cloudflare.
