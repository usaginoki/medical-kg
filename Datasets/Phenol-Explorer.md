---
title: "Phenol-Explorer"
slug: phenol-explorer
kind: [compound]
version: "3.6 (downloads dated 2016-12-10)"
previous_versions: "1.0 (2009, composition), 2.0 (2012, + metabolism/pharmacokinetics), 3.0 (2013, + food-processing retention factors)"
papers: ["[[Rothwell2013 - Phenol-Explorer 3.0]]"]
url: "http://phenol-explorer.eu/"
license: "Free for non-commercial use with citation; commercial use needs the authors' permission (downloads page). The 3.0 paper is CC BY."
availability: open-download
access_link: "http://phenol-explorer.eu/downloads"
accessed: true
access_method: [website-download, scrape]
access_date: 2026-09-30
access_notes: "All 'Latest (Version 3.6)' files downloaded with curl (composition-data.xlsx, foods, foods-classification, compounds, compounds-classification, compounds-structures, metabolites, metabolites-structures, publications; 1.3 MB). The metabolism/pharmacokinetic (intervention study) data and the retention factors are NOT in the bulk downloads; we fetched one metabolism page (metabolite 768) as an example (web_metabolism_origins_768.csv). The site's HTTPS certificate is misconfigured; HTTP works."
countries: []
regions: ["[[Global]]"]
n_records: "458 foods × 501 polyphenols; 7,486 aggregated composition rows (from 38,063 content values); 372 metabolites; 1,308 publications"
size: "1.3 MB"
formats: [xlsx, csv]
has_ingredients: false
has_amounts: no
has_cooking_method: no
has_nutrition: false
body_effect: linkable
body_effect_how: "Downloads give food→polyphenol contents with PubChem CID / ChEBI ids (link to CTD, ChEBI roles, FooDB health effects). The website adds human/animal intervention studies (metabolites detected in plasma/urine, Cmax, Tmax, urinary excretion) = bioavailability, not disease outcomes."
join_keys: [PubChem CID, ChEBI id, CAS number, SMILES, scientific name, Phenol-Explorer food/compound id]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
found_by: [search/compounds, search/ingredients]
tags:
  - type/dataset
  - kind/compound
  - q/3
  - access/accessed
  - access/open
  - region/global
---
# Phenol-Explorer

> [!abstract] TL;DR
> INRA/IARC + Wishart-lab database of **polyphenol contents in foods** (458 foods × 501 polyphenols, 38,063 literature
> values aggregated into 7,486 mean/min/max/SD rows, each traced to publications), plus **polyphenol metabolism** in humans
> and animals (424 intervention studies, web only) and **processing retention factors** (4,296, web only). It has no
> country labels, but it covers spices and staples of the priority regions (turmeric, cumin, cloves, saffron, dates,
> pomegranate, ginger, coriander, Chinese cinnamon, green tea, soy products incl. Korean *cheonggukjang*). It is the most
> reliable quantitative source for the chain "spice → polyphenol (mg/100 g) → what the body absorbs".

## Access
| | |
|---|---|
| Availability | open-download (CSV/XLS zips) + open-web for metabolism & retention data |
| Link | http://phenol-explorer.eu/downloads |
| Accessed? | yes (all bulk files); metabolism only as a 1-page sample |
| How | `curl -L -O http://phenol-explorer.eu/system/downloads/current/<file>.zip` × 9, unzip; 1 metabolism page fetched and transcribed |
| Downloaded | `Data/phenol-explorer/`: `composition-data.xlsx`, `foods.csv`, `foods-classification.csv`, `compounds.csv`, `compounds-classification.csv`, `compounds-structures.csv`, `metabolites.csv`, `metabolites-structures.csv`, `publications.csv`, `web_metabolism_origins_768.csv` |

## Tables & columns
### `composition-data.xlsx` (7,486 rows)
One row per food × polyphenol × analytical-method group, aggregated over publications.

| column | type | meaning | example |
|---|---|---|---|
| `food_group` / `food_sub_group` | str | 9 groups / 67 sub-groups (Fruits 2,489 rows, Vegetables 1,142, Seasonings 949, Seeds 914, Non-alcoholic beverages 762…) | `Seasonings` / `Spices` |
| `food` | str | food name (458) | `Turmeric, dried` |
| `experimental_method_group` | str | Chromatography (4,677), Chromatography after hydrolysis (2,285), Folin assay (302), Normal phase HPLC (185), pH differential (37) | `Chromatography` |
| `compound_group` / `compound_sub_group` | str | Flavonoids, Phenolic acids, Lignans, Stilbenes, Other polyphenols, "Polyphenols, total" / 30 sub-classes | `Other polyphenols` / `Curcuminoids` |
| `compound` | str | polyphenol (508 names) | `Curcumin` |
| `units` | str | `mg/100 g fresh weight` (6,185) or `mg/100 ml` (1,298) | `mg/100 g fresh weight` |
| `mean`, `min`, `max`, `sd` | float | content statistics across samples | `2213.57 / 580 / 5650 / 1526.47` |
| `n` / `N` | int | number of samples / of original values (inferred) | `14` |
| `nb_of_publications` | int | sources aggregated | `2` |
| `publication_ids` / `pubmed_ids` | str | `;`-separated → `publications.csv` / PubMed | `12059141; 25324941` |

### `foods.csv` (459) · `foods-classification.csv` (543)
`id`, `food_group`, `food_subgroup`, `name`, `food_source_french`, `food_source_scientific_name` (91 % filled, e.g.
`Juglans regia L.`), `food_source_botanical_family`, `created_at`, `updated_at`. The classification file maps
`food_id` → `class` / `subclass` (includes non-composition foods).

### `compounds.csv` (501) · `compounds-classification.csv` (751) · `compounds-structures.csv` (492)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | Phenol-Explorer compound id | `713` |
| `compound_class` / `compound_subclass` | str | 5 classes / 29 sub-classes | `Other polyphenols` / `Curcuminoids` |
| `name`, `synonyms` | str | name | `Curcumin` |
| `molecular_weight`, `formula` | | | `368.38`, `C21H20O6` |
| `cas_number` | str | CAS (39 %) | `458-37-7` |
| `chebi_id` | float | ChEBI (22 %) | `3962` |
| `pubchem_compound_id` | float | PubChem CID (56 %) | `969516` |
| `aglycones` | str | aglycone(s) of glycosides | `Curcumin` |
Structures file adds `smiles`.

### `metabolites.csv` (372) · `metabolites-structures.csv` (371)
Polyphenol metabolites detected in biofluids (e.g. `Epicatechin 3'-O-glucuronide`, `4'-O-Methylepicatechin`):
`id`, `name`, `molecular_weight`, `synonyms`, `formula`, `cas_number`, `chebi_id` (15 %), `pubchem_compound_id` (47 %); structures add `smiles`.

### `publications.csv` (1,308)
`id`, `authors`, `year_of_publication`, `title`, `abbreviation` (e.g. `AABY 2007`), `journal_name`, `journal_volume`, `journal_issue`, `pages`.

### `web_metabolism_origins_768.csv` (4 rows, transcribed from http://phenol-explorer.eu/metabolism/origins/768)
`metabolite_id, metabolite, source_administered, source_type, dose, dose_duration, n_subjects, biofluid, kinetic_summary, reference`:
where Epicatechin 3'-O-glucuronide was detected after giving (−)-epicatechin (1 g, 4 subjects), Choladi green tea (500 mL, 10 subjects), a polyphenol-rich beverage and reconstituted green tea.

Sample: `Data/phenol-explorer/sample.csv` · full profile: `Data/phenol-explorer/schema.md`

## Countries & cultures covered
No country or cuisine labels (`countries: []`); the foods are generic commodities compiled from literature worldwide.
Foods relevant to priority regions: Turmeric, dried; Curry, powder; Cumin; Cloves; Saffron; Date, dried/fresh (56 rows);
Pomegranate (3 foods, 52 rows); Ginger; Coriander (4 foods); Ceylan & Chinese cinnamon; herbal teas; 24 soy foods (379 rows,
incl. `Soy paste, cheonggukang`).

## Inferring effects on the body
- **What the data gives**: food → polyphenol amount (mg/100 g, with SD and PubMed ids) and, on the web, polyphenol →
  circulating/excreted metabolites with pharmacokinetics from human intervention studies (**clinical/feeding studies**,
  bioavailability evidence). It does *not* list diseases or bioactivities, so `body_effect: linkable`: PubChem CID/ChEBI
  join to [[FooDB]] health effects, ChEBI roles, CTD chemical–disease links.
- **Concrete chain from the data** (turmeric):
  `Turmeric, dried` → `Curcumin` (Chromatography; mean **2,213.57** mg/100 g FW, range 580–5,650, n = 14, PubMed 12059141; 25324941)
  + `Demethoxycurcumin` 1,982.5 and `Bisdemethoxycurcumin` 1,237.5 mg/100 g; `Curry, powder` → curcumin 285.26 mg/100 g (n = 19).
  Curcumin → PubChem CID 969516 / ChEBI 3962 → [[FooDB]] "Curcumin I" (FDB019238) health effects: anti-inflammatory,
  anti-oxidant, anti-bacterial.
- **Metabolism example** (web): green tea → (−)-epicatechin → Epicatechin 3'-O-glucuronide found in human urine/plasma
  (STALMACH 2009: 500 mL, 10 subjects). Curcumin has no metabolite entries in this release.

## Linking to other datasets
- PubChem CID, ChEBI, CAS, SMILES → [[FooDB]] compounds, CTD, ChEBI.
- `food_source_scientific_name` → FooDB `name_scientific`, NCBI taxon, USDA FoodOn ids ([[USDA FoodData Central]]).
- Food names ↔ recipe ingredients (e.g. [[Food.com Recipes and Interactions]] "turmeric", "ground cumin") by string match.

## Versions
- **3.6** (current site; download files dated 2016-12-10; statistics page: 38,063 content values, 458 foods, 501
  polyphenols, 637 composition publications; 4,296 retention factors / 155 foods / 35 processes; 424 intervention studies from 221 publications).
- 3.0 (2013): added food-processing retention factors (1,253 aggregated from 4,626 published values, 129 papers).
- 2.0 (2012): added metabolism & pharmacokinetics from >200 intervention studies. 1.0 (2009): composition (502 polyphenols, 452 foods).

## Caveats
- Last data update ~2015–2016; no newer release. Content values are literature means, not nationally representative.
- Metabolism and retention data are browse-only (no bulk file); scraping them would need many page requests.
- Non-commercial reuse only without permission.
