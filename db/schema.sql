-- Unified dish ↔ ingredient ↔ compound ↔ condition database (DuckDB).
-- Built by db/build.py; every row carries source_id, every link carries evidence_type + direction.
-- ID conventions (deterministic, so modules can be built independently):
--   dish_id        '<source_id>:<source record id>'           e.g. 'sfct:12'
--   ingredient_id  'ING:<slug of canonical name>'              e.g. 'ING:turmeric'
--   compound_id    'IK:<InChIKey>' | 'CID:<pubchem>' | 'MESH:<id>' | 'CAS:<cas>' | 'NAME:<slug>'  (first available, in that order)
--   condition_id   'MESH:<D…|C…>' | 'UMLS:<CUI>' | 'TCM:<SymMap SMTS id>' | 'TCMSY:<SMSY id>' | 'ICD11:<code>' | 'ACT:<slug>' | 'X:<slug>'
--   drug_id        'DB:<DrugBank id>' | 'DRUGNAME:<slug>'

-- reference ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS source (
  source_id     VARCHAR PRIMARY KEY,   -- short code, e.g. 'ctd', 'foodb', 'sfct'
  dataset_note  VARCHAR,               -- vault note name in Datasets/, e.g. 'CTD'
  name          VARCHAR,
  version       VARCHAR,
  license       VARCHAR,
  access_date   DATE
);

CREATE TABLE IF NOT EXISTS evidence_type (
  code  VARCHAR PRIMARY KEY,   -- clinical | curated_literature | epidemiological | traditional | text_mined | predicted
  rank  INTEGER,               -- 1 = strongest
  label VARCHAR
);

-- dishes ------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS dish (
  dish_id          VARCHAR PRIMARY KEY,
  name             VARCHAR,     -- English (or romanised) name
  name_local       VARCHAR,     -- name in the local language/script if given
  lang             VARCHAR,     -- language of the recipe text (en, zh, ja, ar…)
  country_iso2     VARCHAR,     -- ISO 3166-1 alpha-2; NULL if only a region label
  subregion        VARCHAR,     -- sub-national label (Saudi region, Indian state, Japanese prefecture…)
  cuisine_label    VARCHAR,     -- cuisine label as given by the source
  source_id        VARCHAR,
  source_record_id VARCHAR,
  servings         VARCHAR,
  steps_text       VARCHAR,     -- cooking steps if available
  has_amounts      BOOLEAN
);

CREATE TABLE IF NOT EXISTS dish_ingredient (
  dish_id       VARCHAR,
  ingredient_id VARCHAR,        -- NULL if unmatched
  raw_text      VARCHAR,        -- ingredient line as in the source
  quantity      DOUBLE,
  unit          VARCHAR,
  grams         DOUBLE,         -- NULL if unknown
  match_method  VARCHAR,        -- xref | exact | normalised | fuzzy | manual | unmatched
  match_score   DOUBLE,
  source_id     VARCHAR
);

CREATE TABLE IF NOT EXISTS dish_nutrient (
  dish_id              VARCHAR,
  nutrient_compound_id VARCHAR, -- compound with is_nutrient = true
  amount_per_100g      DOUBLE,
  unit                 VARCHAR,
  source_id            VARCHAR
);

-- ingredients -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS ingredient (
  ingredient_id   VARCHAR PRIMARY KEY,
  canonical_name  VARCHAR,
  category        VARCHAR,      -- spice, herb, vegetable, meat, dairy, grain, … (best effort)
  scientific_name VARCHAR,
  ncbi_taxon_id   BIGINT,
  foodon_id       VARCHAR,
  is_herb         BOOLEAN       -- used in a traditional-medicine materia medica
);

CREATE TABLE IF NOT EXISTS ingredient_alias (
  ingredient_id VARCHAR,
  alias         VARCHAR,        -- stored as given; matching uses norm_text(alias)
  lang          VARCHAR,
  alias_type    VARCHAR,        -- common | scientific | pharmacopoeia | pinyin | zh | ja | ar | fa | hi | ko
  source_id     VARCHAR
);

CREATE TABLE IF NOT EXISTS ingredient_xref (
  ingredient_id VARCHAR,
  db            VARCHAR,        -- foodb_food | flavordb | usda_fdc | usda_ndb | culinarydb | indicrecipenutri | symmap | herb | tmmc | imppat | cmaup | npass | ddid_herb | ddid_food | spicerx | unaprod | duke | wikidata
  xref_id       VARCHAR
);

CREATE TABLE IF NOT EXISTS ingredient_property (
  ingredient_id VARCHAR,
  system        VARCHAR,        -- persian_mizaj | tcm | knapsack_use | ayurveda
  property      VARCHAR,        -- e.g. 'mizaj', 'nature', 'flavour', 'use_in_<ISO2>'
  value         VARCHAR,        -- e.g. 'hot 2 dry 2', 'warm', 'pungent', 'edible'
  source_id     VARCHAR
);

-- compounds ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS compound (
  compound_id VARCHAR PRIMARY KEY,
  name        VARCHAR,
  inchikey    VARCHAR,
  pubchem_cid BIGINT,
  cas         VARCHAR,
  chebi_id    VARCHAR,
  mesh_id     VARCHAR,          -- 'MESH:D…' as used by CTD
  is_nutrient BOOLEAN
);

CREATE TABLE IF NOT EXISTS compound_xref (
  compound_id VARCHAR,
  db          VARCHAR,          -- foodb | hmdb | npass | cmaup | imppat | phenol_explorer | ctd | flavordb | tmmc | herb | symmap
  xref_id     VARCHAR
);

CREATE TABLE IF NOT EXISTS ingredient_compound (
  ingredient_id VARCHAR,
  compound_id   VARCHAR,
  amount        DOUBLE,
  unit          VARCHAR,
  mg_per_100g   DOUBLE,         -- normalised where the unit allows
  plant_part    VARCHAR,
  evidence_type VARCHAR,        -- curated_literature (measured) | predicted
  source_id     VARCHAR,
  citation      VARCHAR
);

-- conditions --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS condition (
  condition_id VARCHAR PRIMARY KEY,
  name         VARCHAR,
  type         VARCHAR,         -- symptom | disease | finding | tcm_symptom | tcm_syndrome | action | unmapped
  mesh_id      VARCHAR,
  umls_cui     VARCHAR,
  icd11        VARCHAR,
  icd10cm      VARCHAR,
  doid         VARCHAR,
  hpo          VARCHAR,
  mesh_tree    VARCHAR,         -- '|'-joined tree numbers
  source_vocab VARCHAR          -- medic | symmap | herb | icd11 | action_map | free_text
);

CREATE TABLE IF NOT EXISTS condition_alias (
  condition_id VARCHAR,
  alias        VARCHAR,
  lang         VARCHAR,
  source_id    VARCHAR
);

CREATE TABLE IF NOT EXISTS condition_relation (
  from_id VARCHAR,
  to_id   VARCHAR,
  rel     VARCHAR               -- is_a (child → parent) | tcm_maps_to | action_targets | same_as
);

-- links -------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS compound_condition (
  compound_id   VARCHAR,
  condition_id  VARCHAR,
  direction     VARCHAR,        -- beneficial | harmful | association | marker
  evidence_type VARCHAR,
  source_id     VARCHAR,
  pmids         VARCHAR,        -- '|'-joined
  score         DOUBLE
);

CREATE TABLE IF NOT EXISTS ingredient_condition (
  ingredient_id VARCHAR,
  condition_id  VARCHAR,
  direction     VARCHAR,
  evidence_type VARCHAR,
  tradition     VARCHAR,        -- tcm | ayurveda | siddha | unani | persian | jamu | folk | NULL
  plant_part    VARCHAR,
  n_pos         INTEGER,
  n_neg         INTEGER,
  pmids         VARCHAR,
  source_id     VARCHAR,
  note          VARCHAR         -- original term / trial id / free text
);

CREATE TABLE IF NOT EXISTS drug (
  drug_id     VARCHAR PRIMARY KEY,
  name        VARCHAR,
  drugbank_id VARCHAR,
  inchikey    VARCHAR
);

CREATE TABLE IF NOT EXISTS drug_condition (
  drug_id      VARCHAR,
  condition_id VARCHAR,
  source_id    VARCHAR
);

CREATE TABLE IF NOT EXISTS ingredient_drug (
  ingredient_id VARCHAR,
  drug_id       VARCHAR,
  effect        VARCHAR,        -- DDID Effect: Harmful | Negative | Positive | No Effect | Possible
  mechanism     VARCHAR,        -- e.g. CYP3A4 inhibition
  evidence_type VARCHAR,
  pmid          VARCHAR,
  source_id     VARCHAR,
  note          VARCHAR
);
