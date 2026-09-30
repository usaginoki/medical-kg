---
title: "SpiceRx"
slug: "spicerx"
kind: [ingredient, compound]
version: "SpiceRx web resource (bioRxiv 2018 preprint; site data mostly 2010s literature)"
previous_versions: ""
papers: ["[[Rakhi2018 - SpiceRx health impacts of culinary spices and herbs]]"]
url: "https://cosylab.iiitd.edu.in/spicerx/"
license: "CC BY-NC-SA 3.0 (site footer)"
availability: open-web
access_link: "https://cosylab.iiitd.edu.in/spicerx/search_plants?page=1&id=<NCBI tax id>"
accessed: partial
access_method: [scrape, api]
access_date: 2026-09-30
access_notes: "No bulk download or documented API. We made a small polite scrape (≈50 requests, 1 req/s): the JSON autocomplete endpoint (/spicerx/autocomplete?table_name=plants&common_name=…) to get NCBI tax ids, then page 1 of /spicerx/search_plants for 29 priority spices. Page 1 holds the top-10 diseases by number of publications, with all PMIDs, linked phytochemicals and the full spice-phytochemical list. We also downloaded the 6 public Google Sheets behind the statistics charts (CSV export). The remaining disease pages (up to 28 per spice) and the disease and chemical detail pages were not crawled. Four name queries resolved to near matches (mint→catnip, chili→Capsicum annuum 'Bell Pepper', onion→Welsh onion, mustard→brown mustard), and nigella/black cumin was not found by that name."
countries: []
regions: ["[[Global]]"]
n_records: "188 spices/herbs, 11,750 MEDLINE abstracts, 8,957 spice-disease associations (8,172 positive / 783 negative) for 152 spices × 848 MeSH diseases; 866 phytochemicals, 2,042 spice-phytochemical links (paper). Local: 29 spices, 267 spice-disease rows, 2,280 PMID rows, 616 spice-phytochemical rows"
size: "3.4 MB local subset"
formats: [csv, html]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Spice→disease (MeSH) associations text-mined from MEDLINE with positive/negative polarity and PMIDs; spice→phytochemical (KNApSAcK, Phenol-Explorer); phytochemical→disease via CTD"
join_keys: [NCBI taxon, scientific name, PubChem CID, MeSH disease id, MeSH/CTD chemical id, PMID]
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
# SpiceRx

> [!abstract] TL;DR
> SpiceRx (CoSyLab, IIIT-Delhi; Rakhi et al. 2018) links **culinary spices and herbs → diseases → phytochemicals**. It starts from a dictionary of 188 spices and herbs. Spice-disease associations were text-mined from 28 M MEDLINE abstracts (TaggerOne disease NER plus a CNN relation classifier trained on 6,712 hand-labelled sentences). The result is 8,957 associations (8,172 positive, 783 negative) for 152 spices and 848 MeSH diseases, each backed by PMIDs. The spices were also linked to 866 phytochemicals (KNApSAcK, Phenol-Explorer), and those to diseases through CTD. For the agent this is a **direct health-effect layer for the spices that define Middle Eastern and South Asian cooking** (turmeric, fenugreek, saffron, cumin, cardamom, sumac, asafoetida, ajwain). The limits: it is web-only and the evidence is text-mined.

## Access
| | |
|---|---|
| Availability | open-web (search pages only; statistics charts read from public Google Sheets) |
| Link | https://cosylab.iiitd.edu.in/spicerx/ |
| Accessed? | partial: 29 spices (page 1 each) + global statistics tables |
| How | autocomplete JSON → tax id; GET `search_plants?page=1&id=<taxid>`; parsed HTML tables; Google-Sheets CSV export for stats |
| Downloaded | `Data/spicerx/`: `spices.csv`, `spice_disease_associations.csv`, `spice_disease_references.csv`, `disease_linked_phytochemicals.csv`, `spice_phytochemicals.csv`, `stats/*.csv`, `raw/plant_<taxid>.html` |

## Tables & columns
Meanings come from the preprint and the page labels.

### `spices.csv` (29 rows)
| column | type | meaning | example |
|---|---|---|---|
| `tax_id` | str | NCBI Taxonomy id (SpiceRx plant key) | 136217 |
| `common_name` | str | SpiceRx display name | Turmeric |
| `scientific_name` | str | species | Curcuma Longa |
| `disease_pages` | int | number of 10-row disease pages for this spice (≈ distinct diseases/10) | 22 |
| `query` | str | our search term | turmeric |

### `spice_disease_associations.csv` (267 rows): top-10 diseases per spice
| column | type | meaning | example |
|---|---|---|---|
| `tax_id`, `spice` | | spice | 136217, Turmeric |
| `mesh_id` | str | MeSH disease id (MeSH or supplementary concept) | MESH:D007249 |
| `disease` | str | MeSH disease name | Inflammation |
| `n_positive` | int | abstracts with a *positive* (beneficial) association (green count) | 60 |
| `n_negative` | int | abstracts with a *negative* (adverse) association (red count) | 1 |

### `spice_disease_references.csv` (2,280 rows): the evidence
| column | type | meaning | example |
|---|---|---|---|
| `tax_id`, `spice`, `mesh_id`, `disease` | | association | Turmeric · Inflammation |
| `pmid` | int | PubMed id of the supporting abstract | 22554269 |
| `polarity` | str | positive / negative (row colour on the site); 2,090 positive, 190 negative | positive |
| `title`, `journal`, `year` | str | article metadata | "Curcumin inhibits inflammatory response and bone loss during experimental periodontitis in rats." · Acta odontologica Scandinavica · 2013 |

### `disease_linked_phytochemicals.csv` (187 rows)
These are phytochemicals of the spice that CTD independently associates with the same disease (the paper's "triangular" evidence). The paper says about 20% of associations have one.
| column | type | meaning | example |
|---|---|---|---|
| `tax_id`, `spice`, `mesh_id`, `disease` | | association | Turmeric · Inflammation |
| `pubchem_id`, `chemical` | | phytochemical | 969516 · Curcumin |

### `spice_phytochemicals.csv` (616 rows; 350 unique compounds)
| column | type | meaning | example |
|---|---|---|---|
| `tax_id`, `spice` | | spice | Turmeric |
| `pubchem_id` | int | PubChem CID | 5469424 |
| `chemical` | str | common name | Demethoxycurcumin |
| `ctd_chemical_id` | str | MeSH/CTD chemical id (the button id on the page) (inferred) | MESH:C050229 |

### `stats/` (global, from the site's Google Sheets)
- `stats_spice_top_associations.csv` (48): positive/negative counts for the top spices, e.g. Garlic 782/40, Ginkgo 554/25, Turmeric 515/6, Ginger 505/3, Liquorice 271/123, Black cumin 179/7.
- `stats_disease_category_pos_neg.csv` (25): per MeSH category, e.g. Neoplasms 1,033/9, Cardiovascular 765/95, Nutritional and Metabolic 857/74.
- `stats_disease_category_references.csv` (24), `stats_chemical_top_references.csv` (62: morphine 394, quercetin 210, curcumin 151, …), `stats_chemicals_alogp_mw.csv` (866 phytochemicals with ALogP and molecular weight).

Sample: `Data/spicerx/sample.csv` · full profile: `Data/spicerx/schema.md`

## Countries & cultures covered
None: SpiceRx is a global resource keyed by plant species with no country fields. Its spice dictionary leans toward South Asian and Middle Eastern cooking (ajwain, asafoetida, fenugreek, curry leaf, sumac, golpar/Persian cow parsley, mastic, saffron, black cumin), which makes it well aligned with the priority regions.

## Inferring effects on the body
- **Direct.** Each spice-disease pair has a direction (positive = therapeutic, negative = adverse) and PMIDs.
- **Evidence type:** text-mined from MEDLINE abstracts, manually assisted. It mixes in-vitro, animal and human studies without distinguishing them. Phytochemical-disease links come from CTD (curated + inferred).
- **Mechanism:** spice → phytochemical (PubChem CID) → CTD disease gives a candidate explanation.
- **Example rows:**
  - Turmeric (*Curcuma longa*, tax 136217) → Inflammation (MESH:D007249): 60 positive / 1 negative. PMID 22554269 is positive (curcumin, periodontitis in rats). PMID 12616304, the NTP turmeric oleoresin toxicology study, is negative. The linked phytochemical is Curcumin (CID 969516), which is also linked to Breast Neoplasms and Drug-Induced Liver Injury.
  - Fenugreek → Diabetes Mellitus: 75 positive / 0 negative.
  - Saffron → Depressive Disorder: 22 / 0.
  - Garlic → Carcinogenesis, with linked diallyl trisulfide (CID 16315).
- **Noise:** text-mining produces some odd pairs, e.g. Cumin → "Keratosis Linearis with Ichthyosis Congenita…" (1 abstract). Filter by `n_positive` and read the evidence before use.

## Linking to other datasets
- **[[FlavorDB2]]:** `pubchem_id` overlaps with FlavorDB2 molecules, and spice names/genus match FlavorDB2 entities.
- **[[CulinaryDB]] / [[RecipeDB2]]:** by spice name (e.g. CulinaryDB Turmeric 341). This lets recipe spice usage per region be scored for disease associations.
- **[[CTD]]:** `ctd_chemical_id` (MeSH chemical id) and `mesh_id` (disease) are CTD's own keys, so the full phytochemical-disease evidence can be pulled there. **[[Phenol-Explorer]]:** one of SpiceRx's phytochemical sources (PubChem CID). **[[IMPPAT]]:** by plant scientific name, for Indian medicinal-plant phytochemicals.
- MeSH, PubMed, NCBI Taxonomy: via `mesh_id`, `pmid`, `tax_id`.

## Versions
There is only one version. The bioRxiv preprint (2018) says "Supplementary data are available at Bioinformatics online", but no journal version was found on Crossref. The site has been restyled since (a Bootstrap 4 UI with a "Linked Phytochemicals" block). Its statistics sheets roughly match the preprint (866 phytochemicals).

## Caveats
- The local copy covers page 1 (top-10 diseases) for 29 spices, not the full 8,957 associations. A full crawl would need about 1,500 page requests.
- The evidence is abstract-level and text-mined, with no dose or study-type information. Literature mostly ends in 2018.
- There is no spice-quantity dimension. The paper itself notes that effects depend on dose, which is not captured.
