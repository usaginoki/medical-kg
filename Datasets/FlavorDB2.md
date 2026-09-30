---
title: "FlavorDB2"
slug: "flavordb2"
kind: [ingredient, compound]
version: "FlavorDB2 (Goel et al. 2024, J Food Sci)"
previous_versions: "FlavorDB (Garg et al. 2018, Nucleic Acids Res 46:D1210, https://cosylab.iiitd.edu.in/flavordb/; the v1 JSON endpoint still answers)"
papers: ["[[Goel2024 - FlavorDB2 updated flavor molecules database]]"]
url: "https://cosylab.iiitd.edu.in/flavordb2/"
license: "CC BY-NC-SA 3.0 (site footer)"
availability: open-web
access_link: "https://cosylab.iiitd.edu.in/flavordb2/entities_json?id=<entity_id>"
accessed: partial
access_method: [api]
access_date: 2026-09-30
access_notes: "No bulk download. The site is browse/search only, with per-molecule downloads (Mol2/SDF/SMILES/JSON). The web UI uses undocumented JSON endpoints: /flavordb2/entities_json?id=<n> (an ingredient with all its molecules), /flavordb2/molecules_json?id=<pubchem_cid>, /flavordb2/entities?entity=<name>, /flavordb2/molecules_autocomplete?.... We fetched 49 entity ids at 1 req/s (48 ok; id 992 Cayenne returned an empty body): all 26 CulinaryDB 'Spice' entities plus 23 staples of priority cuisines. A full crawl (~1,000 entity ids) is technically easy but was not done (polite-scrape limit); the lead should decide."
countries: []
regions: ["[[Global]]"]
n_records: "25,595 flavor molecules; 2,254 linked to 936 natural ingredients in 34 categories (paper). Local: 48 entities, 959 molecules, 6,758 entity-molecule links"
size: "11 MB local subset"
formats: [json, csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: linkable
body_effect_how: "Molecules carry PubChem CID, InChI, CAS and FooDB id → join to CTD/FooDB/SpiceRx for disease or health effects. FlavorDB2 itself only has flavor/odor/taste, bitterness flags, FEMA and physicochemical/ADMET-type properties."
join_keys: [PubChem CID, CAS, FooDB id, InChI, SMILES, FlavorDB entity id, BitterDB id, SuperSweet id]
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
# FlavorDB2

> [!abstract] TL;DR
> FlavorDB2 (CoSyLab, IIIT-Delhi; Goel et al. 2024) is an updated database of **25,595 flavor molecules**. Of these, **2,254 are linked to 936 natural ingredients** (entities) in 34 categories, and each ingredient has a natural source (genus or species). For each molecule it records its flavor profile, FEMA number and profile, FooDB id, PubChem CID, CAS, SMILES and InChI, bitterness/sweetness flags, and about 20 physicochemical descriptors. It is the **ingredient → compound** layer under [[CulinaryDB]]: CulinaryDB's `Entity ID` equals FlavorDB's `entity_id`. There is no health data, but PubChem/FooDB ids make the molecules linkable to effect databases.

## Access
| | |
|---|---|
| Availability | open-web (search UI; per-molecule file downloads; no dump) |
| Link | https://cosylab.iiitd.edu.in/flavordb2/ · JSON: `/flavordb2/entities_json?id=<n>`, `/flavordb2/molecules_json?id=<cid>` |
| Accessed? | partial: 48 ingredients with all their molecules |
| How | Found the endpoints in the page JS (`search` page ajax URLs) and the FlavorDB v1 JSON convention, then made 49 GET requests at 1 req/s |
| Downloaded | `Data/flavordb2/`: `entities.csv` (48), `molecules.csv` (959 unique molecules), `entity_molecules.csv` (6,758 links), `raw/entities_full.jsonl.gz` (raw API responses) |

Entities fetched: Anise, Anise Hyssop, Star Anise, Caraway, Cardamom, Cassia, Celery, Cinnamon, Clove, Cumin, Ginger, Mace, Marjoram, Nutmeg, Oregano, Parsley, Pepper, Saffron, Turmeric, Allspice, Asafoetida, Carom Seed (ajwain), Jalapeno, Poppy Seed, White Pepper, Green Tea, Rice, Milk, Yogurt, Apricot, Coconut, Fig, Tamarind, Basil, Coriander, Garlic, Mint, Lamb, Soybean, Sesame, Olive, Tea, Okra, Eggplant, Pomegranate, Chickpea, Pistachio, Wheat.

## Tables & columns
### `entities.csv` (48 rows): one ingredient per row (`entities_json` minus molecules)
| column | type | meaning | example |
|---|---|---|---|
| `entity_id` | int | FlavorDB ingredient id (= CulinaryDB `Entity ID`) | 341 |
| `category` / `category_readable` | str | one of 34 categories | spice / Spice |
| `entity_alias` / `entity_alias_readable` | str | canonical name | turmeric / Turmeric |
| `entity_alias_basket` | str | aliases merged into this entity | anise, anise-oil, anise-seed |
| `entity_alias_synonyms` | str | synonyms, including Indian names | Aniseed, Saunf |
| `entity_alias_url` | str | Wikipedia page | https://en.wikipedia.org/wiki/Turmeric |
| `natural_source_name` / `natural_source_url` | str | natural source genus/species (Wikipedia) | Curcuma |
| `n_molecules` | int | number of linked flavor molecules (added by us) | 130 |

### `entity_molecules.csv` (6,758 rows)
`entity_id` → `pubchem_id`, the ingredient-contains-molecule links. Molecules per entity range from 1 (Jalapeno) to 391 (Tea).

### `molecules.csv` (959 rows × 43 columns)
| column | type | meaning | example |
|---|---|---|---|
| `pubchem_id` | int | PubChem CID (primary key) | 31266 |
| `common_name` / `iupac_name` | str | names | Allyl hexanoate / prop-2-enyl hexanoate |
| `smile`, `inchi` | str | structure | CCCCCC(=O)OCC=C |
| `cas_id` | str | CAS registry number (98% filled) | 123-68-2 |
| `fooddb_id` | str | FooDB compound id (93%) | FDB019922 |
| `flavor_profile` | str | `@`-separated flavor descriptors (union of sources) | pineapple@ethereal@fruity@… |
| `fooddb_flavor_profile` | str | descriptors from FooDB | same |
| `fema_number`, `fema_flavor_profile` | str | FEMA GRAS number and flavor (68% / 58%) | 2032 · Pineapple |
| `odor`, `taste` | str | odor/taste text (27% / 19%) | |
| `bitter`, `bitterdb_id` | int/str | bitter flag; BitterDB link (bitterdb_id 11%) | 0 |
| `super_sweet`, `supersweetdb_id` | str | SuperSweet link (1%) | |
| `natural`, `synthetic`, `unknown_natural`, `fenoroli_and_os`, `flavornet_id` | 0/1 | origin flags and source-listing flags (Fenaroli's handbook, Flavornet) (inferred) | 1,0,0,1,0 |
| `functional_groups` | str | `@`-separated functional groups | carboxylic acid ester@alkene |
| physicochemical (≈20 cols) | num | `molecular_weight`, `xlogp`, `hbd_count`, `hba_count`, `num_rotatablebonds`, `topological_polor_surfacearea`, `complexity`, `heavy_atom_count`, `volume3d`, stereo/isotope counts, masses, `charge` (PubChem-derived) | 156.225 |

Sample: `Data/flavordb2/sample.csv` · full profile: `Data/flavordb2/schema.md`

## Countries & cultures covered
None. FlavorDB2 is a global ingredient/compound resource with no country fields. Some synonyms carry South Asian names ("Saunf", "Ajwain"), and the entity list covers the spices of Middle Eastern, South Asian and East Asian cooking (saffron, cardamom, asafoetida, carom, star anise, tamarind). Sumac was not in the CulinaryDB spice list, so it is not in our subset.

## Inferring effects on the body
- **Linkable, not direct.** FlavorDB2 describes *sensory* chemistry: flavor, odor, taste, bitterness and FEMA status. It has no disease, target or health fields.
- **How to link:** `pubchem_id`, `fooddb_id`, `cas_id` or `inchi` → [[SpiceRx]] phytochemicals (PubChem id), CTD chemical-disease associations, FooDB health effects.
- **Evidence type:** compound presence is curated from FooDB, the literature and flavor handbooks. Any effect evidence comes from the linked database.
- **Example:** Turmeric (entity 341, natural source *Curcuma*) → 130 molecules, including coumarin (CID 323, FooDB FDB030742, flavor "sweet@new mown hay@…@bitter", bitter = 1), curcumenol (CID 387977) and curcumene (CID 92139). **Curcumin itself is not in the FlavorDB2 turmeric list.** SpiceRx links turmeric → curcumin (CID 969516) → Inflammation, Neoplasms, Breast Neoplasms, so the bioactive layer has to come from [[SpiceRx]], FooDB or CTD.

## Linking to other datasets
- **[[CulinaryDB]]:** `entity_id` = CulinaryDB `Entity ID` (verified for onion 348, turmeric 341, cumin 332, cardamom 327). This gives cuisine → recipe → ingredient → molecule.
- **[[SpiceRx]]:** PubChem CID overlap with SpiceRx phytochemicals, or spice name.
- **[[RecipeDB2]]:** v1 FAQ says ingredients were manually labelled with FlavorDB ids (not exposed).
- **[[FooDB]]**: `fooddb_id` (93% of molecules), which gives concentrations and health effects. **[[CTD]]**: PubChem CID or CAS → chemical-disease associations. PubChem, BitterDB and SuperSweet via their id columns.

## Versions
- **FlavorDB (2018, NAR):** 25,595 molecules, 2,254 linked to 936 ingredients, flavor profiles and physicochemical properties. The v1 endpoint `/flavordb/entities_json?id=` still answers, with one extra key `entity_flavor_profile_union`.
- **FlavorDB2 (2024, J Food Sci):** same molecule and ingredient counts. The abstract says it adds regulatory status, consumption statistics, taste/aroma threshold values, reported uses in food categories and synthesis information, plus a new interface and food-pairing app. Those extra fields are on the molecule detail pages (`/flavordb2/molecules_details?id=`), not in the JSON we pulled.

## Caveats
- The local copy is a 48-ingredient subset. Molecule lists are *flavor* compounds (mostly volatiles), not full composition, and there are no concentrations.
- Some natural-source labels are coarse (e.g. Mint → "Lamiaceae", Milk → "Cattle").
- The JSON API is undocumented and could change. Licence is CC BY-NC-SA 3.0.
