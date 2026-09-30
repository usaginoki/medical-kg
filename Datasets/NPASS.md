---
title: "NPASS"
slug: npass
kind: [compound]
version: "3.0 (\"NPASS-2026\"; data released 2025-06-15; paper NAR 2026, online 2025-11-17)"
previous_versions: "1.0 (Zeng et al. NAR 2018, released Aug 2017); 2.0 (NPASS-2023, Zhao et al. NAR 2023; still online at bidd.group/NPASS-2023)"
papers: ["[[Lin2026 - NPASS database update 2026]]"]
url: "https://bidd.group/NPASS/"
license: "not stated on the download page (the 2026 paper is open access)"
availability: open-download
access_link: "https://bidd.group/NPASS/downloadnpass.html"
accessed: true
access_method: [website-download, scrape]
access_date: 2026-09-30
access_notes: "All 11 NPASS 3.0 download files fetched with curl (332 MB, under the 500 MB limit, so no subsetting). The headline new layer of the 2026 update, the 208,415 quantitative composition records (NP amount in a species/part), is NOT in any download file; it is shown only in the 'NP Quantity Composition' table of each compound page. We scraped that table for 17 compounds relevant to Middle-Eastern/Asian spices (1 req/s; 2,551 rows) into scraped_np_quantity_sample.csv. The 'Experimental ADME' records (9,713) are also web-only. NPASS3.0_naturalproducts_generalinfo.txt could not be profiled by profile_dataset.py (stray quote characters); it reads fine with quoting disabled. Added collect_location_country_counts.csv (our country extraction from org_collect_location)."
countries: ["[[Algeria]]", "[[Argentina]]", "[[Australia]]", "[[Austria]]", "[[Bahamas]]", "[[Brazil]]", "[[Bulgaria]]", "[[Burkina Faso]]", "[[Cambodia]]", "[[Cameroon]]", "[[Canada]]", "[[Chile]]", "[[China]]", "[[Colombia]]", "[[Costa Rica]]", "[[Croatia]]", "[[Cuba]]", "[[Czech Republic]]", "[[Dominican Republic]]", "[[Ecuador]]", "[[Egypt]]", "[[El Salvador]]", "[[Ethiopia]]", "[[Fiji]]", "[[France]]", "[[Gabon]]", "[[Georgia]]", "[[Germany]]", "[[Ghana]]", "[[Greece]]", "[[Guinea]]", "[[Guyana]]", "[[Hungary]]", "[[India]]", "[[Indonesia]]", "[[Iran]]", "[[Ireland]]", "[[Israel]]", "[[Italy]]", "[[Jamaica]]", "[[Japan]]", "[[Jordan]]", "[[Kenya]]", "[[Madagascar]]", "[[Malaysia]]", "[[Maldives]]", "[[Mali]]", "[[Mexico]]", "[[Micronesia]]", "[[Mongolia]]", "[[Morocco]]", "[[Myanmar]]", "[[Nepal]]", "[[Netherlands]]", "[[New Zealand]]", "[[Nigeria]]", "[[Pakistan]]", "[[Palau]]", "[[Panama]]", "[[Papua New Guinea]]", "[[Peru]]", "[[Philippines]]", "[[Poland]]", "[[Portugal]]", "[[Samoa]]", "[[Saudi Arabia]]", "[[Singapore]]", "[[Solomon Islands]]", "[[South Africa]]", "[[South Korea]]", "[[Spain]]", "[[Sri Lanka]]", "[[Suriname]]", "[[Sweden]]", "[[Switzerland]]", "[[Taiwan]]", "[[Tanzania]]", "[[Thailand]]", "[[Tunisia]]", "[[Turkey]]", "[[Uganda]]", "[[United States]]", "[[Uzbekistan]]", "[[Vanuatu]]", "[[Vietnam]]"]
regions: ["[[Global]]"]
n_records: "204,023 natural products · 48,940 organisms · 1,117,269 organism–NP pairs · 1,048,756 activity records · 8,764 targets · 34,975 toxicity records · 208,415 composition records (web only; 2,551 scraped)"
size: "332 MB (TSV) + 0.3 MB scraped/derived CSV"
formats: [tsv, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Compound → target activity records (IC50, Ki, EC50, MIC, GI50…; molecular, in vitro and in vivo) against human proteins, cell lines and organisms, with PMIDs; compound → quantitative toxicity (LD50 etc.). Species → compound pairs (and web-only amounts per species/part) connect a food or medicinal plant to those effects."
join_keys: [InChIKey, PubChem CID, ChEMBL id, NCBI taxon, scientific name, UniProt, CMAUP/NPASS NPO and NPC ids, PMID]
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
# NPASS

> [!abstract] TL;DR
> NPASS (Natural Product Activity and Species Source) comes from the same BIDD group as [[CMAUP]] and uses the
> same NPO/NPC ids. **Version 3.0** (data June 2025, paper NAR 2026) covers **204,023 natural products** from
> **48,940 organisms** (plants, fungi, bacteria, marine animals). It links them through **1.12 M organism–NP
> pairs** to **1.05 M quantitative activity records** against 8,764 targets, plus **34,975 toxicity records**.
> The 2026 update's headline is **208,415 quantitative composition records** (how much of a compound is in a
> species or part, e.g. thymoquinone 22–42% of *Nigella sativa* oil). Those are **only on the web**, not in the
> downloads. It has no cultural labels, so it is `adjacent`. It is the quantitative compound → body-effect layer
> behind culturally specific plants that other datasets name (Q3).

## Access
| | |
|---|---|
| Availability | open download (11 TSV files, no registration); composition and ADME tables on compound web pages only |
| Link | https://bidd.group/NPASS/downloadnpass.html |
| Accessed? | yes: all download files; composition layer only as a scraped sample |
| How | `curl` with a browser User-Agent for `downloadFiles/NPASS3.0_*`. Scraped the `#NPQuantity` table of `compound.php?compoundID=<NPC id>` for 17 compounds at 1 req/s |
| Downloaded | `Data/npass/`: 11 files (332 MB) + `scraped_np_quantity_sample.csv` (2,551 rows) + `collect_location_country_counts.csv` (derived) |

## Tables & columns
No README ships with the files. Meanings are inferred from column names, the paper and the web pages, and are
marked (inferred) where not documented.

### `NPASS3.0_naturalproducts_generalinfo.txt` (204,023 rows)
| column | type | meaning | example |
|---|---|---|---|
| `np_id` | str | NPASS/CMAUP compound id | NPC109083 |
| `inchikey`, `pref_name`, `iupac_name` | str | identity | ZIUSSTSXXLLKKK-KOBPDPAPSA-N, Curcumin |
| `chembl_id`, `pubchem_id` | str | cross-refs (33,579 and 74,224 filled; "n.a." otherwise) | CHEMBL116438, 5281767 |
| `num_of_organism`, `num_of_target`, `num_of_activity` | int | counts of source organisms, targets and activity records (47,561 NPs have ≥ 1 activity) | 30, 347, 1302 |
| `gene_cluster` | str | biosynthetic gene cluster link (inferred) | n.a. |
| `ifQuantity` | str | whether composition (amount) data exist on the web page (Yes for 6,085 NPs) | Yes |

This file is not in `schema.md`: the profiler failed on stray quotes. Read it with `quoting=3` (QUOTE_NONE).

### `NPASS3.0_naturalproducts_structure.txt` (203,390 rows)
`np_id`, `InChI`, `InChIKey`, `SMILES`.

### `NPASS3.0_naturalproducts_species_pair.txt` (1,117,269 rows)
| column | type | meaning | example |
|---|---|---|---|
| `src_org_record_id`, `src_org_pair_id`, `src_org_pair` | str | record / pair ids; pair = `org_id-np_id` | NPO27288-NPC251357 |
| `org_id`, `np_id` | str | organism and compound | NPO24124, NPC109083 |
| `new_cp_found` | str | whether the paper reported a new compound (Y/N/n.a.) (inferred) | N |
| `org_isolation_part` | str | part the compound was isolated from (mostly n.a.; Fruits 5,562, Seeds 3,309…) | Roots |
| `org_collect_location` | str | free-text collection place of the specimen (23,722 rows filled) | Tsukuba, Japan |
| `org_collect_time` | str | collection date | 1998-JUN |
| `ref_type`, `ref_id`, `ref_id_type`, `ref_url` | str | source: Database (996,216 rows: UNPD 558,412; COCONUT 173,739; **FooDB 112,252**; TM-MC 59,549; TCMID 48,666; TCM_Taiwan 19,694; HerDing 19,019; Phenol-Explorer 2,159…) or Publication (121,053, PMID/DOI) | Database, TM-MC |

### `NPASS3.0_species_info.txt` (48,940 rows)
`org_id`, `org_name`, `org_tax_level`, `org_tax_id`, subspecies/species/genus/family/kingdom/superkingdom
tax ids and names (NCBI), `num_of_np_act`, `num_of_np_no_act`, `num_of_np_quantity`, and flags
`if_org_coculture`, `if_org_engineered`, `if_org_symbiont`. Kingdoms: Viridiplantae 26,339; Fungi 6,701;
Bacillati 5,313; Metazoa 3,947…

### `NPASS3.0_activities.txt` (1,048,756 rows)
| column | type | meaning | example |
|---|---|---|---|
| `np_id`, `target_id` | str | compound (46,062 distinct) × target | NPC109083, NPT31 |
| `activity_type_grouped`, `activity_type` | str | grouped type (Others 547,786; IC50 181,506; MIC 123,914; GI50 68,120; Potency; EC50; ED50; Ki…) and the original one (604 kinds) | IC50 |
| `activity_relation`, `activity_value`, `activity_units` | str | measured value | = 11060 nM |
| `assay_organism`, `assay_tax_id`, `assay_strain`, `assay_tissue`, `assay_cell_type` | str | assay system (Homo sapiens in 330,439 rows) | Homo sapiens, 9606 |
| `ref_id`, `ref_id_type` | str | PMID / DOI / Dataset | 15780608, PMID |

### `NPASS3.0_target.txt` (8,764 rows)
`target_id`, `target_type` (Individual protein 2,927; Organism 1,879; Cell line 1,639; Single protein 1,377;
Protein complex 343…), `target_name`, `target_organism_tax_id`, `target_organism`, `uniprot_id`.

### `NPASS3.0_toxicity.txt` (34,975 rows)
Same 14 columns as `activities` (np_id × target/organism, `activity_type` LD50/LD90/LC50…, value, units,
assay organism, reference). It covers 3,662 NPs, mostly insecticidal and antimicrobial lethality plus
rodent LD50.

### `NPASS3.0_Symbiont.tsv` (491), `…_Elicitation.tsv` (382), `…_Coculture.tsv` (869), `…_Engineer.tsv` (811)
Compounds produced by symbionts, elicitor-treated organisms, co-cultures and engineered microbes, with the
organism, effect or pharmacological action, and the reference. Mostly microbial and not relevant to food.

### Scraped: `scraped_np_quantity_sample.csv` (2,551 rows)
| column | type | meaning | example |
|---|---|---|---|
| `np_id`, `pref_name` | str | compound (17 scraped: crocin, piperine, thymoquinone, glycyrrhizin, quercetin, allicin, cinnamaldehyde, cuminaldehyde, capsaicin, eugenol, thymol, carvacrol, apigenin, rosmarinic acid, bisdemethoxycurcumin, limonene, anethole) | NPC166788, Thymoquinone |
| `org_id`, `org_name` | str | source species (600 distinct) | NPO12297, Nigella sativa |
| `material_preparation`, `org_part` | str | e.g. Oil, Dried, Fresh; part | Oil |
| `quantity_standard`, `quantity_min`, `quantity_max`, `quantity_unit` | str | amount, sometimes "mean ± sd" | 34.8 ± 2.9, % |
| `reference` | str | PMID or source database (USDA 225, Phenol-Explorer 289, **DUKE 97**, FooDB 41) | PMID[39519627] |

### Derived: `collect_location_country_counts.csv` (92 rows)
`country`, `pairs`, `species`, `compounds`: our regex extraction of country names and demonyms from
`org_collect_location`.

Sample: `Data/npass/sample.csv` · full profile: `Data/npass/schema.md`

## Countries & cultures covered
There are no cultural labels. The only geography is the **specimen collection site** (`org_collect_location`),
filled for 23,722 of 1.12 M pairs. Of those, 11,723 mention a recognisable country: 92 names, 85 after folding
territories into their sovereign state and dropping Antarctica. The rest are body fluids (blood, urine: human
metabolite records) or plant parts typed into the wrong field. Pairs per country: China 4,118; Poland 587;
Taiwan 516; South Korea 500; Indonesia 389; Japan 376; Thailand 348; Brazil 334; Turkey 315; Vietnam 288;
Morocco 248; Australia 216; Italy 205; Malaysia 193; India 189; Bulgaria 189; Madagascar 188; Ethiopia 174;
New Zealand 160; Algeria 135; Hungary 130; Mexico 126; South Africa 121; Myanmar 105; United States 94 (+ Guam
25, Puerto Rico 11, American Samoa 9, N. Mariana Is. 2); Philippines 79; Mongolia 66; Burkina Faso 65;
Spain 63; Papua New Guinea 61; Argentina 51; El Salvador 51; Suriname 51; **Iran 50**; Germany 49; Greece 48;
Micronesia 48; **Egypt 44**; France 41 (+ New Caledonia 21, French Guiana 8); Cameroon 41; Palau 41;
**Jordan 36**; Peru 35; Colombia 28; **Uzbekistan 28**; Israel 25; Sweden 24; Fiji 24; Nigeria 24; Panama 23;
Canada 23; Vanuatu 21; **Pakistan 21**; Mali 19; Uganda 18; Sri Lanka 17; Costa Rica 14; Austria 12;
Tunisia 12; Nepal 12; Kenya 11; Ecuador 10; Ireland 9; Georgia 9 (may include the US state); Bahamas 9;
Maldives 8; Croatia 8; Cuba 6; Chile 6; Singapore 6; Guinea 6; Guyana 6; Switzerland 5; Dominican Republic 5;
Cambodia 4; Portugal 4; Czech Republic 4; **Saudi Arabia 4**; Netherlands 4; Solomon Islands 3; Gabon 3;
Jamaica 2; Ghana 1; Samoa 1; Tanzania 1.

These counts say where samples were collected, not which cultures use a food, so `regions` is `[[Global]]` only.

## Inferring effects on the body
`body_effect: direct` (at compound level). Evidence is experimental and quantitative: molecular-level
(221,541), in vitro (681,970) and in vivo (145,245) activity records per the paper, plus toxicity. There are
no traditional claims. Route: food/medicinal plant (scientific name → `org_id`) → `species_pair` → `np_id` →
`activities` / `toxicity` → target (UniProt) → disease resources.

Example, turmeric → curcumin:
- `NPO24124` *Curcuma longa* → `NPC109083` curcumin (also listed in 29 other organisms, e.g. *Curcuma zedoaria*,
  *C. wenyujin*, *Daucus carota*).
- Curcumin has 1,264 activity rows. Targets include individual proteins (317 rows), cell lines (420) and
  organisms (202). Examples: COX-2 IC50 11,060 nM (PMID 15780608); amyloid-beta A4 protein Ki 0.208 nM
  (PMID 17004725); histone acetyltransferase p300 IC50 400,000 nM.

Example with an amount (scraped), black seed: thymoquinone (`NPC166788`) in *Nigella sativa* oil 22.6–42.4%
(PMIDs 39519627, 36128855); crocin in *Crocus sativus* stigma 2,000 mg/100 g (source: Duke).

## Linking to other datasets
- **Same ids as [[CMAUP]]** (NPO plants, NPC compounds, NPT targets): CMAUP adds plant → disease and
  traditional-medicine-system labels. NPASS adds quantity, toxicity and far more activity records.
- **InChIKey / PubChem CID / ChEMBL** → [[FooDB]], [[Phenol-Explorer]], [[IMPPAT]], [[DrugBank]]. NPASS
  itself imports [[FooDB]] (112,252 pairs) and [[Phenol-Explorer]] (2,159 pairs) species–compound links, and
  USDA and Duke composition values
  ([[USDA FoodData Central]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]]).
- **UniProt** → [[CTD]], [[DrugBank]] for target → disease/drug.
- **NCBI taxon / scientific name** → [[UNaProd]], [[IMPPAT]], [[SymMap]] (via plant binomials).

## Versions
| | NPASS 1.0 (2018) | NPASS 2.0 (2023) | **NPASS 3.0 (2026)** |
|---|---|---|---|
| NPs | – | 94,413 | **204,023** |
| organisms | – | 32,561 | **48,940** |
| organism–NP pairs | – | 872,723 | **1,117,269** |
| activity records | – | 958,866 | **1,048,756** (split into molecular / in vitro / in vivo) |
| targets | – | 7,753 | **8,764** |
| composition records | – | 95,004 | **208,415** (+87,507 new from 1,822 papers, 4,873 NPs, 1,030 species) |
| toxicity / ADME | – | – | **34,975 toxicity, 9,713 ADME** (new) |
| other new | – | co-culture, engineered | symbiont (341 org) and elicitation (164 org) sources, 88 properties per NP, AI search, community submission |

2.0 numbers are from Table 1 of the 2026 paper. The v1.0 files (`NPASSv1.0_download_*`) are still on the
download page. The v2.0 site is at bidd.group/NPASS-2023.

## Caveats
- **The composition (quantity) layer, the most food-relevant part, is not downloadable.** Getting it means
  crawling ~6,085 compound pages (`ifQuantity = Yes`) or asking the authors. We took 17 compounds.
- The data are dominated by microbial and marine NPs and by database imports (UNPD, COCONUT). Filter by
  `kingdom_name = Viridiplantae` and by food species for this project.
- Activity targets are often organisms (MIC against bacteria) or cancer cell lines, not human proteins. Filter
  `target_type` and `target_organism`.
- Units and value formats in the scraped composition table are heterogeneous (%, mg/g, mg/100g, "mean ± sd").
- No cultural or country-of-use labels. Collection locations are sparse free text; our extraction is heuristic.
