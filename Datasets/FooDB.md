---
title: "FooDB"
slug: foodb
kind: [compound]
version: "Pre-release 1.0 (bulk CSV dump dated 2020-04-07; website records keep being updated)"
previous_versions: ""
papers: []
url: "https://foodb.ca/"
license: "CC BY-NC 4.0"
availability: open-download
access_link: "https://foodb.ca/downloads"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "foodb.ca sits behind a Cloudflare bot check: curl/scripts get HTTP 403 even with a browser User-Agent. The user downloaded the bulk files manually in a browser into Access-help/FooDB/ (CSV, JSON, MySQL and XML dumps). We extracted all 31 CSV tables of foodb_2020_4_7_csv.tar.gz (in fact an uncompressed tar) into Data/foodb/ (953 MB). The 2020 dump may lag the live website."
countries: []
regions: ["[[Global]]"]
n_records: "992 foods, 70,477 compounds (Compound.csv), 39 nutrients, 5,145,532 content rows, 1,435 health effects, 11,062 compound–health-effect links, 883 flavours, 1,744 enzymes/targets, 31,778 references"
size: "CSV tar 952 MB; extracted 953 MB (Content.csv 780 MB)"
formats: [csv, json, xml, sql]
has_ingredients: false
has_amounts: no
has_cooking_method: no
has_nutrition: true
body_effect: direct
body_effect_how: "CompoundsHealthEffect links compounds to HealthEffect terms (1,430 effects used, 1,374 compounds; mostly from Duke's phytochemical database, some ChEBI roles); CompoundsEnzyme links 5,997 compounds to 1,744 human enzymes/targets (UniProt ids, from HMDB); CompoundOntologyTerm adds ChemFOnt-style 'Health effect' / 'Disposition' terms. Food → compound via Content (food_id, source_id/source_type)."
join_keys: [FooDB food id (FOOD#####), FooDB compound id (FDB######), FooDB nutrient id (FDBN#####), NCBI taxon, ITIS id, scientific name, InChIKey, CAS number, ChEBI id, UniProt id, SMPDB/KEGG pathway id]
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
# FooDB

> [!abstract] TL;DR
> FooDB is the Wishart lab's food-chemistry database (University of Alberta, TMIC). It links **992 foods** (with
> taxonomy and food groups) through **5.1 M content rows** to compounds and nutrients, with amounts where measured.
> About 64% of the content rows are *predicted* (PathBank/HMDB). Compounds then link to **1,435 health-effect
> terms** (1,374 compounds carry at least one), to 1,744 human enzymes/targets and to 883 flavours. There are no country
> or cuisine labels; the only geographic hints are free-text descriptions and 8 "… cuisine" food subgroups. It is the
> backbone for Q3 (**food → compound → effect**), e.g. turmeric → curcumin 2,507 mg/100 g → 115 effect terms
> (anti-inflammatory, COX-2 inhibitor, …). Nigella/black cumin, sumac and camel milk are **not** in FooDB.

## Access
| | |
|---|---|
| Availability | open-download (CSV / JSON / XML / MySQL, plus spectra files), CC BY-NC 4.0 |
| Link | https://foodb.ca/downloads → `foodb_2020_4_7_csv.tar.gz` |
| Accessed? | **yes**: the full CSV dump |
| How | Scripts (curl) get a Cloudflare 403. **The user downloaded the files by hand in a browser** into `Access-help/FooDB/` (git-ignored): the CSV tar, JSON zip, MySQL and XML dumps. `foodb_2020_4_7_csv.tar.gz` is really an *uncompressed* POSIX tar (`tar -xf`). |
| Downloaded | `Data/foodb/*.csv`: all 31 tables (953 MB, including the 780 MB `Content.csv`). The earlier web transcriptions (turmeric and curcumin pages) are kept in `Data/foodb/web/`. |

## Tables & columns
Row counts come from `Data/foodb/schema.md` (profiled with `--max-read 300000`, so its per-column stats for
`Content.csv` and `CompoundOntologyTerm.csv` cover only the first 300k rows). The full-table numbers below were
computed with DuckDB over the complete files. Almost every table also has Rails bookkeeping columns
(`created_at`, `updated_at`, `creator_id`, `updater_id`), which are not repeated below.

| table | rows | role |
|---|---|---|
| `Content.csv` | 5,145,532 | **core fact table**: food × (compound or nutrient) × amount |
| `CompoundOntologyTerm.csv` | 1,587,712 | compound ↔ ontology term |
| `CompoundSynonym.csv` | 171,240 | compound synonyms |
| `CompoundsEnzyme.csv` | 105,089 | compound ↔ enzyme/target |
| `CompoundSubstituent.csv` | 95,299 | ClassyFire substituents per compound |
| `Compound.csv` | 70,477 | compounds |
| `CompoundAlternateParent.csv` | 50,691 | ClassyFire alternative parents |
| `Reference.csv` | 31,778 | literature references per compound |
| `CompoundsFlavor.csv` | 11,775 | compound ↔ flavour |
| `CompoundsHealthEffect.csv` | 11,062 | compound ↔ health effect |
| `OntologyTerm.csv` | 4,370 | ChemFOnt-style ontology terms |
| `CompoundExternalDescriptor.csv` | 4,009 | ChEBI role annotations |
| `Enzyme.csv` | 1,744 | enzymes / protein targets |
| `OntologySynonym.csv` | 1,669 | ontology-term synonyms |
| `CompoundsPathway.csv` | 1,604 | compound ↔ pathway |
| `HealthEffect.csv` | 1,435 | health-effect vocabulary |
| `AccessionNumber.csv` | 1,424 | secondary FDB accession numbers |
| `Food.csv` | 992 | foods |
| `FoodTaxonomy.csv` | 889 | lineage rows per food |
| `Flavor.csv` | 883 | flavour/odour descriptors |
| `NcbiTaxonomyMap.csv` | 242 | NCBI taxonomy names and ranks |
| `Pathway.csv` | 97 | SMPDB/KEGG pathways |
| `Nutrient.csv` | 39 | macronutrients and fatty-acid classes |
| `EnzymeSynonym`, `MapItemsPathway`, `PdbIdentifier`, `Pfam`, `PfamMembership`, `Sequence` | 0 | empty in this dump (headers only) |

### How the tables join
```
Food.id ──< Content.food_id
Content.source_type = 'Compound' → Content.source_id = Compound.id
Content.source_type = 'Nutrient' → Content.source_id = Nutrient.id
Compound.id ──< CompoundsHealthEffect.compound_id >── HealthEffect.id (health_effect_id)
Compound.id ──< CompoundsFlavor.compound_id       >── Flavor.id (flavor_id)
Compound.id ──< CompoundsEnzyme.compound_id       >── Enzyme.id (enzyme_id)
Compound.id ──< CompoundsPathway.compound_id      >── Pathway.id (pathway_id)
Compound.id ──< CompoundOntologyTerm.compound_id  >── OntologyTerm.id (ontology_term_id) ─ parent_id → OntologyTerm
Compound.id ──< Reference.source_id (source_type='Compound'), CompoundSynonym.source_id, CompoundSubstituent,
                CompoundAlternateParent, CompoundExternalDescriptor, AccessionNumber
Food.id ──< FoodTaxonomy.food_id  (lineage names; TaxonomyName ↔ NcbiTaxonomyMap)
```
> [!warning] Dangling ids
> `Compound.csv` holds only the 70,477 exported compounds. **343,098 compound content rows** point to
> `source_id`s that are not in it, and so do 154 of the 1,374 compounds in `CompoundsHealthEffect` and part of
> `CompoundOntologyTerm` (78,133 distinct compound ids). In `Content.food_id`, 987 food ids are used but only 982
> exist in `Food.csv`. Use inner joins and count what drops out.

### `Food.csv` (992 rows)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | internal food id (joins `Content.food_id`) | `68` |
| `public_id` | str | stable FooDB accession | `FOOD00068` |
| `name` | str | common English name | `Turmeric` |
| `name_scientific` | str | Latin binomial (675/992 filled; empty for composite foods) | `Curcuma longa` |
| `description` | str | Wikipedia-style text; the only place with geography (422/992 mention "native to", India, China, Asia, Africa, Mediterranean, …) | `Turmeric is a rhizomatous herbaceous perennial plant…` |
| `itis_id` | str | ITIS taxonomic serial number (610 filled) | `42394` |
| `wikipedia_id` | str | Wikipedia page title (853 filled) | `Turmeric` |
| `picture_file_name`, `picture_content_type`, `picture_file_size`, `picture_updated_at` | | image metadata (images not in the dump) | |
| `legacy_id` | int | id in older FooDB versions | |
| `food_group` | str | 24 groups: Aquatic foods 169, Fruits 157, Vegetables 147, Herbs and Spices 126, Dishes 51, Cereals 50, Beverages 38, Milk products 36, … | `Herbs and Spices` |
| `food_subgroup` | str | about 100 subgroups (Fishes, Berries, Herbs, Spices, … and 8 "… cuisine" subgroups, see below) | `Spices` |
| `food_type` | str | `Type 1` (706; single-species foods) / `Type 2` (264; composite or processed foods) / `Unknown` (22) (inferred) | `Type 1` |
| `category` | str | `specific` (876) / `generic` (25) / empty | `specific` |
| `ncbi_taxonomy_id` | int | NCBI Taxonomy id (619 filled) | `136217` |
| `export_to_foodb` | bool | shown on the website (797 true) | `true` |
| `export_to_afcdb` | bool | exported to a sister food-composition DB (inferred) | |

### `Content.csv` (5,145,532 rows): the core food → compound/nutrient table
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | row id | `1` |
| `source_id` | int | id of the chemical: `Compound.id` or `Nutrient.id` depending on `source_type` | `12295` |
| `source_type` | str | `Compound` (5,007,500 rows) or `Nutrient` (138,032) | `Compound` |
| `food_id` | int | → `Food.id` | `68` |
| `orig_food_id` | str | food id in the source database | `29` |
| `orig_food_common_name` | str | food name as written in the source (e.g. "Goat milk", "Milk, indian buffalo, fluid") | `Kiwi` |
| `orig_food_scientific_name` | str | source's Latin name, with author and family | `Actinidia chinensis PLANCHON [Actinidiaceae]` |
| `orig_food_part` | str | plant part measured | `Rhizome`, `Seed`, `Leaf` |
| `orig_source_id`, `orig_source_name` | str | chemical id and name in the source DB | `FAT`, `Protein, total` |
| `orig_content` | float | **amount** (mean/typical). Only 855,958 rows (16.6%) have it; the rest mean "expected/detected, not quantified" | `2800.45` |
| `orig_min`, `orig_max` | float | range reported by the source | `0.9`, `5600` |
| `orig_unit` | str | unit, mostly `mg/100g` (638,566) or `mg/100 g` (165,273). Also `uM`, `kcal/100g`, `IU`, `RE`, `α-TE`, `NE`, `mg/kg`, … Not normalised | `mg/100g` |
| `orig_citation` | str | citation text from the source | |
| `citation` | str | where the row came from: `PATHBANK` 2.06 M, `HMDB` 1.21 M, `MANUAL` 0.96 M, `USDA` 591k, `DTU` (Danish food DB) 222k, `DUKE` 40k, `DFC CODES` 25k, `PHENOL EXPLORER` 7.3k, `KNAPSACK` 5.8k, `PHYTOHUB` 4k, PubMed ids and article texts | `DUKE` |
| `citation_type` | str | evidence class: `PREDICTED` 3,273,562 · `UNKNOWN` 943,349 · `DATABASE` 895,467 · `ARTICLE` 25,077 · `EXPERIMENTAL` 6,785 · `TEXTBOOK` 1,292 | `DATABASE` |
| `orig_method` | str | analytical method (rare: `Chromatography`, `Chromatography after hydrolysis`) | |
| `orig_unit_expression` | str | basis, e.g. `fresh weight` (5,592 rows) | |
| `standard_content` | float | content in standard units (filled where `orig_content` is; mostly the same value) | `1955.0` |
| `preparation_type` | str | `raw`, `cooked`, `dried or powder`, `tea or coffee`, `other`, `beverage (juice)`, … | `dried or powder` |
| `export` | 0/1 | shown on the website (4,605,654 rows = 1) | `1` |

### `Compound.csv` (70,477 rows)
> [!warning] Shifted header
> The header row in this dump does **not** match the data columns. From the actual values (e.g. the curcumin row
> `12295,FDB012292,Curcumin,Solid,low,"Isolated from Curcuma zedoaria…"`), the true order is
> `id, public_id, name, state, annotation_quality, description, cas_number, moldb_smiles, moldb_inchi,
> moldb_mono_mass, moldb_inchikey, moldb_iupac, kingdom, superklass, klass, subklass`. Read the file by position, not by header.

| true column (header label) | type | meaning | example |
|---|---|---|---|
| `id` (`id`) | int | internal id (joins `Content.source_id`, link tables) | `12295` |
| `public_id` (`public_id`) | str | FooDB accession | `FDB012292` |
| `name` (`name`) | str | compound name | `Curcumin` |
| `state` (`moldb_iupac`) | str | physical state | `Solid` |
| `annotation_quality` (`state`) | str | curation level (`low` for 22,589, else empty) | `low` |
| `description` (`annotation_quality`) | str | free-text summary, often with food occurrence and use | `Natural colouring matter used extensively in Indian curries…` |
| `cas_number` (`description`) | str | CAS RN | `458-37-7` |
| `moldb_smiles` (`cas_number`) | str | SMILES | |
| `moldb_inchi` (`moldb_inchikey`) | str | InChI | `InChI=1S/C21H20O6/…` |
| `moldb_mono_mass` (`moldb_inchi`) | float | monoisotopic mass | `368.126` |
| `moldb_inchikey` (`moldb_smiles`) | str | InChIKey (70,415 filled): the main cross-DB join key | `VFLDPWHFBUODDF-FCXRPNKRSA-N` |
| `moldb_iupac` (`moldb_mono_mass`) | str | IUPAC name | |
| `kingdom`, `superklass`, `klass`, `subklass` | str | ClassyFire taxonomy (mostly filled only for kingdom/superclass) | `Organic compounds` / `Phenylpropanoids and polyketides` / `Flavonoids` |

### `Nutrient.csv` (39 rows)
Macronutrients and fatty-acid classes that are not modelled as compounds: Fat, Proteins, Carbohydrate, Fatty acids,
Fiber (dietary), Energy, Ash, and fatty-acid classes (`13:0`, `16:1 c`, `18:2 CLAs`, `22:5 n-3`, …).
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | joins `Content.source_id` when `source_type='Nutrient'` | `1` |
| `legacy_id` | int | old id | `10930` |
| `public_id` | str | accession | `FDBN00001` |
| `name` | str | nutrient | `Fat` |
| `description`, `wikipedia_id` | str | text and Wikipedia title | `Carbohydrate` |
| `duke_id`, `dfc_id`, `eafus_id`, `dfc_name` | str | ids in Duke / Dictionary of Food Compounds / EAFUS | `PROTEIN\|PROTEINS` |
| `compound_source` | str | where the nutrient came from | `DUKE` |
| `annotation_quality`, `export`, `state`, `type`, `comments`, `metabolism`, `synthesis_citations`, `general_citations` | | mostly empty metadata | `low` |

### `HealthEffect.csv` (1,435 rows)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | joins `CompoundsHealthEffect.health_effect_id` | `1` |
| `name` | str | effect label, mostly Duke's "activity" vocabulary (lower case) | `anti inflammatory`, `hypoglycemic`, `pesticide` |
| `description` | str | FooDB definition (619 filled) | `An agent that alters the force … of muscular contractions.` |
| `chebi_name` | str | mapped ChEBI role | `anti-inflammatory drug` |
| `chebi_id` | str | ChEBI id (710/1,435 filled) | `35472` |
| `chebi_definition` | str | ChEBI definition (698 filled) | `A substance that reduces or suppresses inflammation.` |

### `CompoundsHealthEffect.csv` (11,062 rows)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | row id | `1` |
| `compound_id` | int | → `Compound.id` | `453` |
| `health_effect_id` | int | → `HealthEffect.id` | `1` |
| `orig_health_effect_name` | str | effect name in the source | `(+)-Inotropic` |
| `orig_compound_name` | str | compound name in the source | `THEOPHYLLINE` |
| `orig_citation` | str | source citation (empty) | |
| `citation` | str | source DB: `DUKE` 10,930 rows, `CHEBI` 132 | `DUKE` |
| `citation_type` | str | always `DATABASE` | `DATABASE` |
| `source_id`, `source_type` | | polymorphic copy of the compound (`Compound`) | `453`, `Compound` |

### `Flavor.csv` (883 rows) and `CompoundsFlavor.csv` (11,775 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Flavor.id` / `name` | int / str | flavour descriptor | `celery`, `cumin`, `spicy` |
| `Flavor.flavor_group` | str | coarse group (113 filled: fruity, floral, balsamic, …) | `vegetable` |
| `Flavor.category` | str | always `odor` | `odor` |
| `CompoundsFlavor.compound_id`, `flavor_id` | int | the link (2,871 compounds) | `11947`, `159` |
| `CompoundsFlavor.citations` | str | source, e.g. Flavornet (Arn & Acree 1998) | `# Arn, H, Acree TE. "Flavornet…"` |
| `CompoundsFlavor.source_id`, `source_type` | | polymorphic copy of the compound | `Compound` |

### `Enzyme.csv` (1,744 rows) and `CompoundsEnzyme.csv` (105,089 rows)
| column | type | meaning | example |
|---|---|---|---|
| `Enzyme.id` | int | joins `CompoundsEnzyme.enzyme_id` | `2` |
| `Enzyme.name` | str | protein name | `Estrogen receptor beta` |
| `Enzyme.gene_name` | str | HGNC gene symbol | `ESR2` |
| `Enzyme.uniprot_id` | str | UniProt accession: the join key to target/drug DBs | `Q92731` |
| `Enzyme.description`, `go_classification`, `general_function`, `specific_function`, `pathway`, `reaction`, `cellular_location`, `signals`, `transmembrane_regions`, `molecular_weight`, `theoretical_pi`, `locus`, `chromosome`, `uniprot_name`, `pdb_id`, `genbank_protein_id`, `genbank_gene_id`, `genecard_id`, `genatlas_id`, `hgnc_id`, `hprd_id`, `organism`, `general_citations`, `comments` | | protein annotation fields; **empty in this dump** (only name, gene_name, uniprot_id filled) | |
| `CompoundsEnzyme.compound_id`, `enzyme_id` | int | link (5,997 compounds × 1,744 enzymes) | `362`, `2` |
| `CompoundsEnzyme.citations` | str | always `HMDB` | `HMDB` |

### `OntologyTerm.csv` (4,370 rows) and `CompoundOntologyTerm.csv` (1,587,712 rows)
A ChemFOnt-style ontology (hierarchy by `parent_id`, `level` 1–7). The 6 roots are **Process**, **Role**,
**Physiological effect** (children: *Health effect*, *Organoleptic effect*), **Disposition** (*Biological location*,
*Source*, *Route of exposure*), **Biomarkers** and **Foods** (Dairy products, Beverages, Herbs and spices, Grains, …).
| column | type | meaning | example |
|---|---|---|---|
| `OntologyTerm.id` | int | joins `CompoundOntologyTerm.ontology_term_id` | `7694` |
| `term` | str | term | `Health effect`, `Hypercholesterolemia`, `Plant`, `Ingestion` |
| `definition` | str | definition | `Biological or chemical events … leading to a known function or end-product.` |
| `external_id`, `external_source` | str | mapped id and source (SMPDB 799, HMDB 763, FBOnto 358, EPA 319, Disease Ontology 182, HPO 161, NCI CTCAE 133) | |
| `parent_id`, `level` | int | tree structure | `7693`, `2` |
| `comment`, `curator`, `legacy_id` | | curation metadata | |
| `CompoundOntologyTerm.compound_id`, `ontology_term_id` | int | link (78,133 distinct compound ids) | `23204`, `8494` |
| `CompoundOntologyTerm.export` | bool | shown on the website (`true` for 1,547,397 rows) | `true` |

Curcumin's terms, for example, include *Plant*, *Animal*, *Ingestion*, *Pharmaceutical*, *Food* and plant families.

### `Reference.csv` (31,778 rows)
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | row id | `2` |
| `ref_type` | str | always `general` | `general` |
| `text` | str | full citation text | `Neveu V, … Phenol-Explorer … Database (Oxford). 2010` |
| `pubmed_id`, `link`, `title` | str | almost always empty (2 PubMed ids) | |
| `source_id`, `source_type` | | the compound the reference supports (`Compound`) | `1`, `Compound` |

### Other tables (summary)
- **`CompoundSynonym`** (171,240): `synonym`, `synonym_source` (biospider, hmdb, db_source, ChEBI, Generator…), `source_id`/`source_type` → compound. Useful for name matching.
- **`CompoundSubstituent`** (95,299) and **`CompoundAlternateParent`** (50,691): `name`, `compound_id`. ClassyFire chemical substructure and alternative class labels (e.g. `Hydroxyflavonoid`, `7-hydroxyflavonoids`).
- **`CompoundExternalDescriptor`** (4,009): `external_id` (e.g. `CHEBI:6584`), `annotations` (ChEBI role text such as `anthocyanidin cation`), `compound_id`.
- **`AccessionNumber`** (1,424): secondary/merged FDB numbers (`number`) → `compound_id`.
- **`Pathway`** (97): `smpdb_id`, `kegg_map_id`, `name` (e.g. `SMP00006`, `map00350`, Tyrosine Metabolism). **`CompoundsPathway`** (1,604): `compound_id`, `pathway_id`.
- **`FoodTaxonomy`** (889): `food_id`, `ncbi_taxonomy_id`, `classification_name`, `classification_order`. One row per lineage level; covers only 62 foods.
- **`NcbiTaxonomyMap`** (242): `TaxonomyName`, `Rank` (genus 48, family 41, order 32, …).
- **`OntologySynonym`** (1,669): `ontology_term_id`, `synonym` (e.g. "High cholesterol" for Hypercholesterolaemia), `external_id`, `external_srouce` [sic], `parent_id`, `parent_source`.
- Empty: `EnzymeSynonym`, `MapItemsPathway`, `PdbIdentifier`, `Pfam`, `PfamMembership`, `Sequence`.

Sample: `Data/foodb/sample.csv` (Content) and `Data/foodb/sample_<Table>_csv.csv` · full profile: `Data/foodb/schema.md`

## Key numbers (computed over the full dump)
- **Foods**: 992 in `Food.csv` (797 shown on the website). **982 have ≥1 content row** (10 have none, e.g. Veggie burger, Monterey Jack cheese). **898 have ≥1 quantified row** (`orig_content` not null). A food typically has about 6,000 compound rows (turmeric: 6,088 distinct compounds), mostly from PathBank/HMDB predictions.
- **Content**: 5,007,500 compound rows (65,134 distinct compound ids) plus 138,032 nutrient rows. Only 3,709 compounds have a quantified amount somewhere.
- **Health effects**: 1,435 terms, 1,430 used. **1,374 compound ids have ≥1 health effect** (1,220 of them resolve to `Compound.csv`); 1,373 of them occur in `Content`, across 948 foods. Mean about 8 effects per compound; curcumin has 115.
- **Top health effects** (by number of compounds): pesticide 503 · antioxidant 277 · anti bacterial 214 · anti inflammatory 212 · flavor 198 · fungicide 196 · cancer preventive 193 · antitumor 182 · perfumery 141 · anti septic 136 · anti viral 122 · anti spasmodic 114 · anti mutagenic 107 · aldose reductase inhibitor 95 · irritant 90 · allergenic 90 · hepatoprotective 80 · cytotoxic 80 · anti cancer 78 · analgesic 78 · anti aggregant 75 · sedative 73 · hypocholesterolemic 67. Many "effects" are uses or roles (pesticide, flavor, perfumery), not effects on the human body.
- **Other links**: 5,997 compounds → 1,744 enzymes/targets; 2,871 compounds → 883 odour descriptors; 1,604 compound–pathway links.

## Countries & cultures covered
None as structured labels (`countries: []`, `regions: [[Global]]`). The Food table's geography-related fields:
- **No country or region column.** `food_group` / `food_subgroup` are commodity classes (Herbs and Spices → Spices, Herbs; Pulses → Peas, Beans, Lentils; Teas; Milk products → Fermented milks …).
- **8 cuisine-named subgroups** (all under `food_group = Dishes`, 20 foods): Tex-Mex cuisine 4 (Taco, Chili, Burrito, Nachos), Mexican cuisine 4, Latin American cuisine 4 (Empanada, Pupusa, Tamale, Arepa), American cuisine 3, Asian cuisine 2 (Egg roll, Rice cake), **Levantine cuisine 1 (Hummus)**, **Berber cuisine 1 (Couscous)**, Jewish cuisine 1 (Gefilte fish). Other regional dishes sit in "Other dishes" (Falafel) or "Flat breads" (Pita bread).
- **Free-text `description`**: 422/992 foods mention places (e.g. "native to", India, China, Asia, Africa, Mediterranean). This is extractable with NLP but not a label.
- `Content.orig_food_common_name` keeps the source's food name and sometimes carries origin ("Milk, indian buffalo, fluid").

### Priority-region foods: present vs missing
| food | FooDB | content rows (quantified) |
|---|---|---|
| Turmeric | FOOD00068 *Curcuma longa* | 6,374 (302) |
| Date | FOOD00135 *Phoenix dactylifera* | 6,559 (601) |
| Fenugreek | FOOD00186 *Trigonella foenum-graecum* | 6,337 (195) |
| Cumin | FOOD00067 *Cuminum cyminum* | 6,247 (244) |
| Saffron | FOOD00063 *Crocus sativus* | 6,176 (137) |
| Green tea / Black tea / Tea | FOOD00908 / FOOD00907 / FOOD00038 | 11,866 (2,707) / 11,876 (2,707) / 5,795 (2,241) |
| Cardamom, Ginger, Cloves, Coriander, Pepper, Cinnamon (3 kinds) | FOOD00074, 00206, 00179, 00061, 00139, 00050/51/572 | ~6–7k each |
| Pomegranate, Fig, Apricot, Jujube, Tamarind, Mango, Pistachio | FOOD00151, 00081, 00144, 00388, 00180, 00106, 00140 | ~6–8k each |
| Chickpea, Lentils, Mung bean, Sesame, Okra, Bitter gourd, Rice, Millet, Barley | … | ~6–11k each |
| Hummus (Levantine), Couscous (Berber), Falafel, Pita bread | FOOD00845, FOOD00740, FOOD00727, FOOD00802 | 75 for hummus (USDA-derived only) |
| Soy products (Tofu, Miso, Soy sauce, Natto), Kombu, Purple laver, Lotus, Ginseng | … | present |
| Yogurt, Kefir, Buffalo, Domestic goat, "Milk (Other mammals)" (goat, sheep, Indian buffalo milk) | … | present |
| **Nigella / black cumin / black seed** (*Nigella sativa*) | **missing** (no food; its marker compound thymoquinone FDB013274 exists but is linked only to winter savory) | – |
| **Sumac** (*Rhus coriaria*) | **missing** | – |
| **Camel milk / camel meat** | **missing** ("Ostrich" is *Struthio camelus*; no camel in Content source names either) | – |
| Za'atar blend, ghee, labneh/laban | missing (thyme and butter are present) | – |

## Inferring effects on the body
- **Relations**: `Food —Content→ Compound —CompoundsHealthEffect→ HealthEffect` (qualitative bioactivity labels,
  half mapped to ChEBI roles); `Compound —CompoundsEnzyme→ Enzyme` (human proteins with UniProt ids, from HMDB);
  `Compound —CompoundOntologyTerm→ OntologyTerm` under *Physiological effect → Health effect* (disease/phenotype
  terms mapped to Disease Ontology / HPO); `CompoundsPathway` → SMPDB/KEGG.
- **Evidence type**: health effects are **database-curated** (98.8% from Duke's Phytochemical and Ethnobotanical
  Databases, the rest from ChEBI), with no dose, study type or organism; many come from in-vitro or ethnobotanical
  claims. Content rows: 64% `PREDICTED`, 18% `UNKNOWN` (manual, unquantified), 17% `DATABASE` (USDA, DTU, Duke,
  Phenol-Explorer), under 1% article/experimental.
- **Amount matters**: only 16.6% of content rows have a number. Ranking by amount needs a unit filter (`mg/100g` and
  `mg/100 g` are both used) and should skip obvious mis-mappings (see caveats).

### Concrete chains (full dump, averages of `orig_content` over sources, unit mg/100 g)
The top compounds by amount are often generic (starch, sugars, potassium), so the lists below give the most abundant
compounds **that have health effects**, plus the food's characteristic bioactive compound.

- **Turmeric** (FOOD00068) → starch 42,500 · β-D-glucopyranose 28,000 · **alpha-curcumene** (FDB005326) 12,170 *(anti inflammatory, antitumor, anti ulcer, anti viral, hypotriglyceridemic)* · D-fructose 6,225 · **curcumin** (FDB012292) **2,507** (Duke 2,800.45 [0.9–5,600], rhizome; Phenol-Explorer 2,213.57, dried powder) → **115 effects**, incl. anti inflammatory, antioxidant, cyclooxygenase-2 inhibitor, NF-kappa-B inhibitor, TNF inhibitor, anti Alzheimeran, anti amyloid-beta, hepatoprotective, hypocholesterolemic, hypotensive, neuroprotective, cancer preventive, anti arthritic.
- **Date** (FOOD00135) → sugars 63,805 · D-glucose 21,938 *(sweetener)* · D-fructose 19,707 *(anti diabetic, laxative, sweetener, …)* · sucrose 19,054 *(atherogenic, triglycerigenic, hypercholesterolemic, …)* · starch 10,300 · **pectic acid** 2,310 *(hypocholesterolemic, hypoglycemic, anti atheromic, peristaltic, cancer preventive, …)* · quercetin 0.93 (USDA).
- **Fenugreek** (FOOD00186) → **lignin** 28,000 *(hypocholesterolemic, laxative, antioxidant, anti diarrheic, …)* · L-glutamic acid 4,088 · arginine 2,466 *(vasodilator, anti hypertensive, anti diabetic, …)* · choline 1,350 *(hepatoprotective, lipotropic, cholinergic, …)* · **diosgenin** (FDB012734) 1,115 [330–1,900], seed *(anti inflammatory, hypocholesterolemic, hepatoprotective, estrogenic, anti neoplastic, …)* · **trigonelline** (FDB002237) 130, seed *(hypoglycemic, anti hyperglycemic, hypocholesterolemic, anti migraine, …)*.
- **Cumin** (FOOD00067) → potassium 1,864 *(hypotensive, anti hypertensive, diuretic, …)* · cuminyl alcohol 1,098 *(flavor)* · calcium 1,086 *(anti osteoporotic, …)* · **cuminaldehyde** (FDB008724) 1,000 [400–1,600], seed *(anti bacterial, sedative, tyrosinase inhibitor, fungicide, irritant; odour: cumin, spicy, green)* · p-cymene 672 *(anti viral, analgesic, anti bacterial, …)* · γ-terpinene 599 *(antioxidant, ACE inhibitor, aldose reductase inhibitor)*.
- **Saffron** (FOOD00063) → starch 12,510 · **alpha-crocin** (FDB014549) 2,000, stigma *(neuroprotective, choleretic, colorant)* · potassium 1,724 · phosphorus 252 · **kaempferol** 205 *(68 effects: antioxidant, anti cancer, anti ulcer, …)* · kaempferol 3-sophoroside 151 *(analgesic)*. Safranal (FDB014884) exists but has no quantified saffron row.
- **Green tea** (FOOD00908) → Chinese tannin 15,190 *(67 effects: antioxidant, anti hypertensive, anti obesity, xanthine-oxidase inhibitor, …)* · pectic acid 6,500 · potassium 1,122 · hexanal 790 · **caffeine** 423 *(57 effects: energizer, anti obesity, phosphodiesterase inhibitor, hypertensive, …)* · **L-theanine** 394 *(hypocholesterolemic, anti thromboxane)* · epigallocatechin 1,593 (Duke, leaf) vs 0.1–20 (USDA/Phenol-Explorer, brewed): leaf and infusion values are mixed in the same food.
- **Pomegranate** (FOOD00151) → Chinese tannin 12,112 *(67 effects)* · β-D-glucopyranose 8,000 · calcium oxalate 4,000 *(lithogenic, laxative)* · pectic acid 1,635.
- **Hummus** (FOOD00845, Levantine cuisine) → only 75 compounds (USDA amino acids and minerals): L-glutamic acid 882, arginine 501, sodium 310.5 *(hypertensive)*.
- **Nigella / black cumin**: not a food in FooDB. Its key compound **thymoquinone** (FDB013274) has 16 effects (anti asthmatic, anti arthritic, cyclooxygenase and lipoxygenase inhibitor, antioxidant, anti histaminic, …) but links only to *Winter savory* (3.8 mg/100 g).

## Linking to other datasets
- **InChIKey / CAS / ChEBI** → [[Phenol-Explorer]] (FooDB imports it: `citation = PHENOL EXPLORER`), [[CTD]] (chemical–disease), [[DrugBank]], [[Exposome-Explorer]]; HMDB is a sister Wishart DB (PathBank/HMDB predictions fill most of `Content`).
- **UniProt id** (`Enzyme.uniprot_id`) → protein targets in [[DrugBank]] / [[CTD]].
- **NCBI taxon / scientific name / ITIS** → [[USDA FoodData Central]] (FooDB also imports USDA rows: `citation = USDA`), [[IMPPAT]] (Indian medicinal plants), [[FlavorDB2]].
- **Food names** ↔ recipe ingredients in [[Food.com Recipes and Interactions]], [[CulinaryDB]], [[RecipeDB2]]; the regional composition tables ([[Saudi Food Composition Tables]], [[Indian Nutrient Databank (INDB)]], [[Korean Food Composition Table]]) cover foods FooDB lacks, such as camel milk.
- **Flavours** ↔ [[FlavorDB2]] (compound → odour descriptors).

## Versions
Still "Pre-release 1.0". The only bulk dump is 2020-04-07 (CSV, JSON, XML, MySQL); spectra files were added in 2022.
The website keeps changing: the curcumin I record was updated 2026-09-29, and the turmeric page lists 4,309 content rows
against 6,374 in the 2020 dump. The dump and the website may therefore differ; `Data/foodb/web/` keeps the two web pages
transcribed earlier.

## Caveats
- **Cloudflare**: the files can only be fetched in a browser, not from scripts, so the download is not reproducible from code.
- **`Compound.csv` header is shifted** (see above); dangling compound and food ids (343k content rows).
- **Mostly predicted content**: 64% of rows are PathBank predictions with no amount, so "food contains compound" is
  often inferred from metabolic pathways (e.g. curcumin appears in cumin as an unquantified `MANUAL` row).
- **Mis-mapped amounts** in Duke/DTU rows: e.g. *17alpha-ethynylestradiol* (a synthetic drug) at 3,500 mg/100 g in cumin,
  6,250 in cardamom, 4,270 in ginger, and *(E)-2-phenyl-2-butenal* 3,200 in chickpea. These look like mappings of generic
  "estrogens"/other source names. Filter by `citation` and sanity-check.
- Units are not normalised (`mg/100g` vs `mg/100 g`, IU, RE, uM); raw leaf, dried spice and brewed tea values are mixed.
- Health effects are qualitative Duke "activities" (incl. pesticide, perfumery, flavor) without dose, evidence grade or
  species; they can conflict (kaempferol: anti cancer *and* carcinogenic).
- No culture labels; regional staples such as nigella, sumac and camel milk are absent. CC BY-NC (non-commercial).
