---
title: "GRAYU"
slug: grayu
kind: [ingredient, compound]
version: "web portal as of 2026-09-30 (ToS effective 2025-10-16; paper published 2026-01-22)"
previous_versions: ""
papers: ["[[Joshi2026 - GRAYU Ayurveda graph database]]"]
url: "https://caps.ncbs.res.in/GRAYU/"
license: "GRAYU Terms of Use: non-commercial research and education only; no bulk copying or large-scale scraping; bulk/API access by separate agreement (mini@ncbs.res.in)"
availability: open-web
access_link: "https://caps.ncbs.res.in/GRAYU/"
accessed: partial
access_method: [scrape]
access_date: 2026-09-30
access_notes: "There is no download page or public API. The Terms of Use (static/tos.txt §3B) forbid copying substantial portions or large-scale scraping, and ask users to email mini@ncbs.res.in for bulk or API access. We took a small excerpt: 5 POST calls (10 s apart, following robots.txt Crawl-delay 10) to the site's own internal JSON endpoint /GRAYU/api/graph-search, for 'Curcuma longa' (plants), 'Curcumin' (phytochemicals), 'Diabetes' (diseases) and 'Abhayarishta'/'Abhaya' (formulations). The returned subgraphs were flattened into node and edge CSVs. Bulk access needs the user to email the authors (reported to the lead as NEEDS USER)."
countries: ["[[India]]"]
regions: ["[[South Asia]]"]
n_records: "full DB (paper/portal): 1,039 formulations · 12,743 plants · 129,542 phytochemicals · 13,480 diseases; 157,010 nodes / 1,520,687 edges. Our excerpt: 4,639 nodes, 5,664 edges"
size: "30 MB excerpt (raw JSON gz + CSV)"
formats: [json, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Plant –ASSOCIATED_WITH_DISEASE→ Disease (MeSH/DOID/ICD-11 ids) with an evidence type per edge (clinical trials of the plant or its ingredients, therapeutic-target overlap, disease-transcriptome reversal, literature/book reference); Formulation –TREATS→ Disease with the Ayurvedic term; Phytochemical –FOUND_IN→ Plant."
join_keys: [PubChem CID, InChIKey, scientific name, NCBI taxon, MeSH id, DOID, ICD-11, UniProt]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients, search/regions]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
---
# GRAYU

> [!abstract] TL;DR
> GRAYU is a Neo4j knowledge graph from R. Sowdhamini's lab (NCBS Bengaluru, *Front. Pharmacol.* 2026). It
> links **1,039 Ayurvedic formulations → 12,743 plants → 129,542 phytochemicals**, and plants and
> formulations to **13,480 diseases** mapped to MeSH, Disease Ontology and ICD-11. It merges IMPPAT 2.0, CMAUP,
> NPASS, OSADHI, FooDB and HMDB with the Ayurvedic Pharmacopoeia, the Ayurvedic Formulary and the Standard
> Treatment Guidelines. Each plant–disease edge records **why** it exists (clinical trial, target overlap,
> transcriptome reversal, traditional text). Plants also carry the **Indian states where they are found**.
> It is very relevant for Q3, but only browse-only access is open. Bulk data needs a request to the authors.

## Access
| | |
|---|---|
| Availability | open-web (browse, search, interactive graph with per-view CSV/JSON export). Bulk or API access only by agreement with the authors |
| Link | https://caps.ncbs.res.in/GRAYU/ |
| Accessed? | partial: a small excerpt |
| How | Five POST requests to the portal's internal endpoint `/GRAYU/api/graph-search` (`{"query", "limit", "category"}`), the same call the "Interactive Knowledge Graph" page makes, spaced 10 s apart |
| Downloaded | `Data/grayu/`: `raw_api/search_*.json.gz` (raw responses) and the flattened `nodes_plant.csv`, `nodes_phytochemical.csv`, `nodes_disease.csv`, `nodes_formulation.csv`, `edges.csv` |

> [!warning] Terms of Use
> The ToS (https://caps.ncbs.res.in/GRAYU/static/tos.txt) allow viewing, querying and "export small excerpts for
> analysis". They forbid substantial downloads, large-scale scraping, mirroring, and "use the Service to provide
> medical advice". The last point matters for a medical-advice agent, so GRAYU content should be used for
> research on the agent, not served to users. Full data: email Prof. R. Sowdhamini, mini@ncbs.res.in.
> The paper's data-availability statement only points to the website.

The portal also has `/GRAYU/api/graph/expand-node` and `/GRAYU/api/graph/expansion-options` (POST, used by the
graph viewer). We did not call them.

## Tables & columns
The excerpt holds all subgraphs returned for the 5 queries: 3,712 plant, 709 phytochemical, 186 disease and 32
formulation nodes, and 5,664 edges. Most plant nodes come from the "Diabetes" disease query. Node ids are
Neo4j element ids (`4:<db-uuid>:<n>`). List-valued properties are `|`-joined.

### `nodes_plant.csv` (3,712 rows × 29 columns)
| column | type | meaning | example |
|---|---|---|---|
| `id`, `name_display`, `plant_name`, `clean_plant_name` | str | node id and scientific name | Curcuma longa |
| `synonyms` | str | botanical synonyms **and vernacular names** in Indian languages | Pasupu\|Haldi\|Arisina\|Halad\|Halud\|Turmeric |
| `family_name`, `genus_name`, `species_name`, `*_tax_id` | str | taxonomy with NCBI taxon ids | Zingiberaceae, 136217 |
| `group` | str | plant group | Angiosperms |
| `system_of_medicine` | str | traditional systems | Ayurveda\|Homeopathy\|Siddha\|Sowa Rigpa\|Unani |
| `available_in_states` | str | Indian states/UTs where the plant occurs, from FRLHT ENVIS (inferred) | Andhra Pradesh\|Assam\|…\|West Bengal |
| `iucn_redlist_category` | str | IUCN status | Data Deficient |
| `database_name` | str | source DBs that contributed the plant | cmaup_plants;imppat_herbs;osadhi_herbs |
| `disease_id`, `disease_name` | str | CMAUP-style plant indications (ICD-11 codes) | 6A20, Schizophrenia |
| `frlht_herbarium`, `frlht_plant_info`, `ipni_id`, `pow`, `wfo`, `tropicos`, `mpns_kew`, `plant_list_id`, `gardners_world` | str | external links | http://envis.frlht.org/… |

### `nodes_phytochemical.csv` (709 rows × 76 columns)
Important columns: `cid` (PubChem CID), `compound_name`, `compound_synonyms` (truncated at 100k characters),
`iupac_name`, `smiles`, `inchi`, `inchi_key`, `molecular_formula`, `molecular_weight`, `xlogp`,
`topological_polar_surface_area`, `hydrogen_bond_donor_count`/`acceptor_count`, ClassyFire and NP-Classifier
classes (`classyfire_superclass`, `np_classifier_pathway`…), drug-likeness and ADME flags (`is_pains`,
`brenk_violation`, `Prediction_Hob`, `ESOL`, `logS`, `logD`), `target_id`, `uniprot_id`, `enzyme_uniprot_id`,
`pathway_kegg_map_id` and `database_name` (e.g. `cmaup_ingredients;npass_chem_all;pubchem`). The other
columns are further computed descriptors.
Example: 3''-demethylhexahydrocurcumin, CID 56675574, InChIKey MSLIBNPPWWCGPY-HNNXBMFYSA-N.

### `nodes_disease.csv` (186 rows × 32 columns)
| column | type | meaning | example |
|---|---|---|---|
| `Label`, `name_display` | str | disease name (MeSH heading) | Uterine Cervical Neoplasms |
| `MESH_ID`, `MESH_label`, `MESH_subClassOf` | str | MeSH descriptor and parents | D002583 |
| `DOID_ID`, `DOID_label`, `DOID_description`, `subClassOf` | str | Disease Ontology | DOID_4362, cervical cancer |
| `dbxref` | str | ICD10CM, ICD9CM, MIM, NCI, SNOMED CT, UMLS CUI | ICD10CM:C53\|UMLS_CUI:C0007847 |
| `synonyms`, `has_symptom`, `disease_has_location`, … | str | DOID relations (mostly empty) | cervix cancer |
| `data_source`, `disease_node_id` | str | DOID and/or MESH; internal id | DOID\|MESH |

### `nodes_formulation.csv` (32 rows × 20 columns)
| column | type | meaning | example |
|---|---|---|---|
| `formulation_name` | str | Ayurvedic formulation | Abhaya lavana |
| `dosage_form`, `dosage`, `anupana`, `time_of_administration`, `duration` | str | form, dose, vehicle (anupāna), timing | Lavana; 1 to 2 g; Warm water |
| `combined_diseases` | str | indications: Ayurvedic term + English gloss | Gulma (Abdominal lump), Hrdroga (Heart disease)… |
| `METHOD`, `DEFINITION`, `DESCRIPTION`, `PHYSICO_CHEMICAL`, `STORAGE`, `REMARKS`, `OTHER_REQUIREMENTS` | str | preparation method and monograph text | "Ingredients 19 (Lavana) and 20 … are added to the reduced decoction…" |
| `Source` | str | source book | Ayurvedic Standard Treatment Guidelines; Ayurvedic Formulary of India |

### `edges.csv` (5,664 rows × 19 columns)
| column | type | meaning | example |
|---|---|---|---|
| `label` | str | relation: ASSOCIATED_WITH_DISEASE 4,617 · FOUND_IN 902 · SUBCLASS_OF 65 · TREATS 39 · IS_INGREDIENT_IN 37 · HAS_SYMPTOM 4 | ASSOCIATED_WITH_DISEASE |
| `source`, `target` | str | node ids | |
| `DOID`, `MESH`, `ICD11` | str | disease ids on plant–disease edges | DOID_4362, D002583, 2E66 |
| `association_by_clinical_trials_of_plant_ingredients` | str | NCT ids of trials on the plant's compounds (1,088 edges) | NCT01715597\|NCT02554344 |
| `association_by_clinical_trials_of_plant` | str | NCT ids of trials on the plant (14) | |
| `association_by_therapeutic_target` | str | shared gene targets supporting the link (3,544) | RELA;INSR;ESR1;PPARA;NFKB1 |
| `association_by_disease_transcriptome_reversion` | str | genes whose disease expression the compounds reverse (8) | HCAR2;SLCO1B3;MMP9 |
| `reference`, `part` | str | book ISBN or DOI; plant part (497 with reference) | ISBN:9788190648943, rhizome |
| `ayurvedic_term` | str | on TREATS edges: Ayurvedic disease name | Madhumeha |
| `quantity`, `pharmacopoeia_ref`, `matched_synonym`, `match_type` | str | on IS_INGREDIENT_IN: amount in the formulation, pharmacopoeia name, how the plant was matched | 480 g, Madhuka(Flower), synonym_exact |
| `source_db` | str | provenance | cmaup_ingredients;npass_chem_all |

Sample: `Data/grayu/sample.csv` · full profile: `Data/grayu/schema.md`

## Countries & cultures covered
- **[[India]]**, with Ayurveda as the core system. Plants also carry Siddha, Unani, Sowa Rigpa and Homeopathy
  labels.
- **Per-state counts (excerpt only):** 823 of the 3,712 plant nodes in our excerpt have `available_in_states`.
  Plants per state or UT: West Bengal 536 · Maharashtra ("Maharastra") 468 · Tamil Nadu 432 · Kerala 422 ·
  Chhattisgarh ("Chattisgarh") 378 · Andhra Pradesh 362 · Karnataka 355 · Odisha 347 · Madhya Pradesh 227 ·
  Jammu and Kashmir 205 · Uttarakhand 190 · Punjab 135 · Rajasthan 131 · Uttar Pradesh 127 · Telangana 109 ·
  Jharkhand 105 · Puducherry 99 · Delhi 85 · Ladakh ("Ladhak") 81 · Bihar 76 · Goa 75 · Andaman & Nicobar 62 ·
  Chandigarh 62 · Haryana 56 · Arunachal Pradesh 56 · Assam 47 · Himachal Pradesh 45 · Tripura 43 · Gujarat 42 ·
  Sikkim 41 · Manipur 40 · Nagaland 38 · Dadra and Nagar Haveli 27 · Meghalaya 23 · Mizoram 19 ·
  Lakshadweep ("Lakshawadeep") 10.
  These are counts **for a query-biased sample**, not the full database. They describe where plants grow, not
  where they are eaten.
- Vernacular synonyms (Telugu *Pasupu*, Hindi *Haldi*, Kannada *Arisina*, Bengali *Halud*) help map regional
  ingredient names.

## Inferring effects on the body
`body_effect: direct`. The chain is Phytochemical –FOUND_IN→ Plant –ASSOCIATED_WITH_DISEASE→ Disease and
Plant –IS_INGREDIENT_IN→ Formulation –TREATS→ Disease. Plant–disease edges state their evidence:
- **clinical trials** of the plant or its compounds (NCT ids): 1,088 edges via compound trials and 14 via plant trials, out of 4,617 excerpt edges;
- **therapeutic-target overlap** (computational): 3,544;
- **disease-transcriptome reversal** (computational): 8;
- **traditional text / literature** (`reference`, ISBN or DOI): 497.

Formulation → disease edges are **traditional claims** from the Ayurvedic Pharmacopoeia and Standard Treatment
Guidelines (e.g. `TREATS` with `ayurvedic_term = Madhumeha`, diabetes).
Example: turmeric (*Curcuma longa*) → 700 phytochemicals (FOUND_IN) → 104 diseases. Cervical cancer
(MeSH D002583, DOID_4362) is supported by trials NCT01715597, NCT02554344 and NCT03143491 on turmeric
compounds. Testicular diseases (D013733) are supported by the rhizome and Ayurvedic book references.
Turmeric is also an ingredient in 19 formulations.

## Linking to other datasets
- PubChem CID / InChIKey → [[IMPPAT]], [[FooDB]], [[HMDB]], [[NPASS]], [[CMAUP]], [[PubChem]].
- Scientific plant name and NCBI taxon → [[IMPPAT]], [[OSADHI]], [[CMAUP]]. GRAYU *imports* these, so it is
  largely a superset for plants and compounds, plus the Ayurvedic formulations.
- MeSH / DOID / ICD-11 / UMLS disease ids → [[CTD]] and clinical vocabularies. This makes GRAYU the easiest
  resource here for mapping traditional claims to modern disease codes.

## Versions
Only one version is public. The paper (published online 2026-01-22) and the portal both give 1,039 / 12,743 /
129,542 / 13,480 entities. The portal does not show a version number, although the ToS asks citations to
state one ("version [vX.Y]").

## Caveats
- **No bulk access** without the authors' permission. Our excerpt is query-biased and must not be treated as
  representative.
- The **ToS forbid using GRAYU to provide medical advice**, which is directly relevant to our agent.
- Evidence quality is mixed. Most plant–disease edges in the excerpt come from computational target overlap,
  not clinical data. The paper warns about PAINS-type polyphenol false positives.
- Plant `disease_id` codes contain spreadsheet-corrupted values (e.g. `2.00E+66`, `8.00E+47`).
- State names are misspelled ("Maharastra", "Chattisgarh", "Ladhak", "Lakshawadeep"), so normalise them before
  joining.
