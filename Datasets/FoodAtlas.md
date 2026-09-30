---
title: "FoodAtlas"
slug: foodatlas
kind: [compound]
version: "KGv2 (npj Science of Food 2026) as served on foodatlas.ai; the live build now comes from AI-Institute-Food-Systems/foodatlas (versioned KGC bundles, e.g. 20260413T221503Z), which adds bioactivity, trust and efficacy layers"
previous_versions: "FoodAtlas v1 (Youn et al., Comput Biol Med 2024; repo IBPA/FoodAtlas): 285,077 triplets, 230,848 food–chemical 'contains' relations from 155,260 papers via an entailment model with active learning; no disease layer. KGv2 repo IBPA/FoodAtlas-KGv2 (code only, now archived/migrated)."
papers: ["[[Li2026 - FoodAtlas unified food-chemical-disease KG]]"]
url: "https://www.foodatlas.ai/"
license: "Apache-2.0 (code and FoodAtlas data); CTD-derived edges are not redistributed (CTD terms)"
availability: registration
access_link: "https://www.foodatlas.ai/food-composition-downloads"
accessed: partial
access_method: [github]
access_date: 2026-09-30
access_notes: "The KG itself was NOT obtained. (1) github.com/IBPA/FoodAtlas-KGv2 contains only pipeline code and seed lookup tables; built KG files (entities.tsv, triplets.tsv…) are gitignored, and the Box links in data/download.sh (Lit2KG.zip, CTD.zip…) return 404. (2) The repo moved to github.com/AI-Institute-Food-Systems/foodatlas; the KG is released as parquet bundles at foodatlas.ai/food-composition-downloads and api.foodatlas.ai/v1/bundles, both gated by a free API key requested via the contact form (api.foodatlas.ai returns 'Invalid API key'). (3) The website's internal proxy (/_proxy-api) sits behind a Vercel bot checkpoint (429 for curl and automated Chrome), so no scrape was possible. What we have: the 5 real example API responses shipped in the repo docs (bioactivity layer: first 25 of 11,109 antioxidant-tested chemicals, first 25 of 972 foods, quercetin's 17 bioactivities, onion's 2) and the synthetic test fixtures that show the bundle schema. Needs the user to request an API key."
countries: []
regions: ["[[Global]]"]
n_records: "Paper (KGv2): 1,430 foods · 3,610 chemicals in foods (10,266 chemical nodes in total) · 2,181 diseases · 958 flavour descriptors; 48,474 food–contains–chemical edges from 125,723 sentences; 23,211 chemical–disease assertions from CTD (13,417 treats / 9,794 worsens); 15,222 chemical–bioactivity records (ChEMBL); 3,645 chemical–flavour links. Downloaded: 70 real API records + 14 synthetic fixture rows."
size: "1.5 MB downloaded (API example JSON + fixture parquet)"
formats: [parquet, json, tsv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Chemical → disease edges POSITIVELY_CORRELATED ('worsens', from CTD marker/mechanism) / NEGATIVELY_CORRELATED ('improves', from CTD therapeutic) with PubMed ids; chemical → bioactivity (anticancer, antioxidant, anti-inflammatory, antidiabetic… from ChEMBL/PubChem assays, active/inactive counts); food → predicted antioxidant / antidiabetic bioactivity (FoodAtlas random-forest model). Food → chemical 'contains' edges with concentration and PMC/FDC provenance give the first hop."
join_keys: [FoodAtlas id, FoodOn id, NCBI taxon, FDC id, ChEBI id, PubChem CID, MeSH chemical id, InChIKey, MeSH disease id, PubMed id]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/compounds, search/ingredients]
tags:
  - type/dataset
  - kind/compound
  - q/2
  - q/3
  - access/blocked
  - access/registration
---
# FoodAtlas

> [!abstract] TL;DR
> FoodAtlas (UC Davis, Tagkopoulos lab / USDA-NSF AIFS) is a knowledge graph of **food → contains → chemical (with
> concentration) → disease / bioactivity / flavour**. LLMs (fine-tuned GPT-3.5) extract the food–chemical edges from
> PubMed Central sentences, and these are merged with FoodOn, ChEBI, FDC, CTD, ChEMBL, FlavorDB and PubChem. In KGv2
> 1,430 foods link to 3,610 chemicals through 48,474 provenance-tracked edges, and those chemicals link to 2,181
> diseases through 23,211 CTD assertions. It is the most direct ready-made **food → compound → disease** chain for
> Q3. It has no culture or country labels. Foods are FoodOn/FDC entities. **We could not get the graph:** bulk bundles need a free API key (contact form), and
> the CTD edges must be rebuilt locally from [[CTD]] (the rebuild recipe is below).

## Access
| | |
|---|---|
| Availability | registration: free API key via https://www.foodatlas.ai/contact?api-access, then bundles from `/food-composition-downloads` or `GET https://api.foodatlas.ai/v1/bundles` (Bearer key) |
| Link | https://www.foodatlas.ai/ · code: https://github.com/AI-Institute-Food-Systems/foodatlas (was IBPA/FoodAtlas-KGv2) |
| Accessed? | partial, and only samples: the KG was **not** obtained |
| How | `git clone --depth 1` of both repos; copied `docs/bioactivity-api-examples/*.json` and `backend/db/tests/fixtures/*.parquet` |
| Downloaded | `Data/foodatlas/api-examples/` (5 real API responses), `Data/foodatlas/schema-fixtures-synthetic/` (5 synthetic parquet files, 2–4 rows each, schema only) |

> [!warning] Needs user action
> Request a free API key at https://www.foodatlas.ai/contact?api-access. Then download the newest bundle zip from
> https://www.foodatlas.ai/food-composition-downloads (it unzips to `foodatlas-<version>/` with `entities`,
> `relationships`, `triplets`, `evidence`, `attestations` parquet) into `Data/foodatlas/`.

## Tables & columns
### Bundle schema (from `backend/db/src/models/*.py` + synthetic fixtures; no real rows)
**`entities`**: `foodatlas_id` (e.g. `e10005`), `entity_type` (food / chemical / disease / bioactivity / flavor),
`common_name`, `scientific_name`, `synonyms` (list), `external_ids` (JSON; keys seen in the KGC registry code: food `foodon`, `fdc`;
chemical `chebi`, `pubchem_compound`/`pubchem_cid`, `mesh`, `kegg`, `cdno`, `fdc_nutrient`, `dmd`; disease `ctd`/`mesh`), `attributes` (JSON).

**`relationships`**: `foodatlas_id` → `name`. Fixture values are `CONTAINS`, `IS_A`, `POSITIVELY_CORRELATED`,
`NEGATIVELY_CORRELATED`. The KGC code maps CTD `marker/mechanism` → positively correlated and `therapeutic` →
negatively correlated.

**`triplets`**: `head_id`, `relationship_id`, `tail_id`, `source` (e.g. `fdc`, `lit2kg`, `ctd`), `attestation_ids` (list).

**`attestations`** (one per supporting claim): `attestation_id`, `evidence_id`, `source`, `head_name_raw`,
`tail_name_raw`, `conc_value`, `conc_unit` (standardised, e.g. `mg/100g`), `conc_value_raw`, `conc_unit_raw`,
`food_part`, `food_processing`, `filter_score`/`quality_score`, `validated`, `validated_correct`,
`head_candidates`, `tail_candidates` (ambiguous entity resolutions).

**`evidence`**: `evidence_id`, `source_type` (`pubmed`, `fdc`…), `reference` (JSON: `pmid`, `pmcid`, sentence
`text`, or `fdc_id` + url).

### `api-examples/*.json` (real API responses, bioactivity layer)
| file | rows | content |
|---|---|---|
| `bioactivity-metadata.json` | 1 | concept `antioxidant` (`e227382`): `synonyms`, `description`, `n_foods` = 972, `n_chemicals` = 11,109 |
| `bioactivity-chemicals.json` | 25 (of 11,109) | chemicals tested for antioxidant activity: `name` (quercetin, l-ascorbic acid, trolox…), `id`, `measurement_count`, `active_count`, `inactive_count`, `unspecified_count`, `inconclusive_count`, `measurements` |
| `bioactivity-foods.json` | 25 (of 972) | foods with a (predicted) antioxidant value, e.g. snail, enoki mushroom, gum arabic |
| `chemical-bioactivities.json` | 17 | quercetin's bioactivities: anticancer (755 measurements, 83 active), antioxidant (232, 67 active), anti-inflammatory, antibacterial, antiviral… |
| `food-bioactivities.json` | 2 | onion: antioxidant, antidiabetic (model predictions) |

Each `measurements` item: `assay` (e.g. `AID: 1508616` or `FoodAtlasModel: RF_antioxidant_v1`), `endpoint`
(Potency, GI50, Activity…), `value`, `unit`, `outcome` (Active / Inactive / Unspecified / Inconclusive),
`evidence_type` (`in vitro`, `in silico`), `evidence_source` (Experimental / Predicted), `assay_meta` (source
PubChem/ChEMBL/FoodAtlasModel, description, target UniProt/gene), dose–response fit fields (`efficacy_logac50_value`,
`efficacy_hillslope`, `evidence_fit_r2`).

Sample: `Data/foodatlas/sample.csv` (+ `sample_*.csv`) · full profile: `Data/foodatlas/schema.md`

## Countries & cultures covered
No country or cuisine fields (`countries: []`, `[[Global]]`). Foods are FoodOn/FDC/FooDB entities (1,300 seed food
names from FooDB and FDC), so coverage follows the English-language literature. Regional foods (dates, turmeric, green tea…) are expected
as FoodOn/FDC entities, but we could not check this because the site blocked us, and there is no way to filter by
culture.
Cultural grounding has to come from Q1/Q2 datasets that name the foods.

## Ingredients, amounts, cooking method
Not a recipe dataset. For Q2 the "contains" edges carry **concentration** (`conc_value`/`conc_unit`), **food part**
(leaf, seed…) and **processing** (dried, cooked…) from the source sentence, e.g. "Chinese cabbage leaves contain Ca
(1020 g kg-1 FW)" → (Chinese cabbage, leaves, Ca, 1020 g kg-1 FW).

## Inferring effects on the body
**Direct** (in the KG), but in our copy only in principle, since we hold no KG rows.
- Chemical → disease: `POSITIVELY_CORRELATED` / `NEGATIVELY_CORRELATED`, copied from [[CTD]] DirectEvidence with
  PubMed ids. The evidence is curated literature, mostly mechanistic/animal studies. The paper notes these links are
  "binary and do not capture dose-response dynamics or clinical outcomes".
- Chemical → bioactivity: ChEMBL/PubChem assay results (in vitro).
- Food → bioactivity: model predictions (in silico), e.g. onion antioxidant 0.52 mmol/100 g from `RF_antioxidant_v1`.

**Rebuilding the CTD edges** (FoodAtlas does not redistribute them): take the chemical entities' MeSH ids
(`external_ids.mesh`), join to `Data/ctd/CTD_chemicals_diseases_curated.tsv` on `ChemicalID` (MeSH, no prefix), join diseases on `external_ids.ctd`, and
map `therapeutic` → NEGATIVELY_CORRELATED and `marker/mechanism` → POSITIVELY_CORRELATED. This is what
`backend/kgc/src/pipeline/triplets/chemical_disease/ctd.py` does. Our curated file has 109,665 rows; the KGC README
reports "~107K" DirectEvidence rows in the CTD release it used.

**Example chain (to be checked against the bundle once we have a key):**
green tea (FoodOn) —CONTAINS→ epigallocatechin gallate (MeSH C045651, CID 65064) —NEGATIVELY_CORRELATED→ Breast
Neoplasms / Diabetes Mellitus, Type 2 / Colorectal Neoplasms (CTD `therapeutic`, PMIDs 10518005, 16988119, 20346928).
The disease hop was verified in [[CTD]], and human cohort evidence for tea catechins is in [[Exposome-Explorer]]. The
food hop (tea contains EGCG, with concentration) needs the bundle.

## Linking to other datasets
- **MeSH chemical id** → [[CTD]] (how FoodAtlas itself builds disease edges).
- **PubChem CID / ChEBI / InChIKey** → [[HMDB]], [[Exposome-Explorer]], [[IMPPAT]], FooDB.
- **FDC id** → [[USDA FoodData Central]] (FoodAtlas ingests FDC nutrient values as "contains" edges).
- **FoodOn id / NCBI taxon / scientific name** → any food or recipe dataset whose ingredients are mapped to FoodOn
  or taxonomy.

## Versions
- **v1 (2024, Comput Biol Med 181:109072):** entailment-model extraction with active learning. 230,848 food–chemical
  relations from 155,260 papers (46% not in any database), KG of 285,077 triplets. Food–chemical only.
- **KGv2 (npj Sci Food 10:33, online 2026-01-20):** GPT-based extraction with concentrations, plus CTD disease,
  ChEMBL bioactivity, FlavorDB/PubChem flavour and FoodOn/ChEBI/MeSH ontologies. This is the version described above.
- **Live platform (2026):** the repo moved to AI-Institute-Food-Systems/foodatlas. It adds a bioactivity layer
  (11,109 chemicals and 972 foods for antioxidant), LLM "trust" signals per attestation (Gemini judge), PTFI reference-food
  efficacy, and versioned downloadable bundles (key-gated; page shows "Bulk downloads are being rebuilt").

## Caveats
- The graph is not publicly downloadable without a key, and the CTD layer must be rebuilt (licence).
- The extraction F1 of 0.67 means many "contains" edges are wrong or ambiguous. Use `validated`/trust signals once
  available.
- Disease edges inherit CTD's bias towards lab and toxicology studies. "Improves" does not mean clinically
  demonstrated.
