# Unified dish ↔ condition database

A DuckDB database that links **dishes → ingredients → compounds → conditions** (symptoms and diseases) and back,
built from the datasets documented in `Datasets/`. Human-facing documentation is in `Database/Unified database.md`,
and example traces are in `Database/Traces - *.md`.

```
uv run db/build.py --fresh          # full build → db/unified.duckdb (git-ignored)
uv run db/trace.py dish "Kabsa" --country SA
uv run db/trace.py condition "nausea" --country IN --drug warfarin
uv run db/export.py                 # → db/export/{dishes,ingredients,effects}.parquet + .csv
uv run db/cases.py                  # → db/export/cases.parquet + .csv (patient cases, separate from the graph)
uv run db/cues.py [--examples N]    # count cultural cues per case dataset (Q7); the flags are columns of cases.parquet
```

## Getting the data
`Data/` is git-ignored except each dataset's `schema.md` and `sample*.csv`. To rebuild from scratch:
```
uv run db/fetch.py      # downloads 33 sources into Data/<slug>/ (skips files already there; resumes partial ones)
uv run db/prep.py       # PDF tables, MAFF Markdown, polite scrapes (1 req/s, cached in Data/<slug>/raw/) → derived CSVs
uv run db/build/links_symmap_scrape.py   # appends 6 more herbs to the SymMap scrape
```
- **By hand (Cloudflare blocks scripts):** FooDB `foodb_2020_4_7_csv.tar.gz` → `Data/foodb/raw/`; HMDB
  `hmdb_metabolites.zip` → `Data/hmdb/raw/`. Then `uv run db/fetch.py foodb hmdb` unpacks and converts them.
- **Reference for checking:** each prep step's output can be compared with the committed `sample_*.csv`; `db/prep.py
  samples` restores the scraped files whose sample is the complete file.
- **Case datasets** (for `cases.py`, not for the graph): `uv run db/fetch.py medicationqa ngqa tcm_best4sdt mtcmb
  medcasereasoning rumedbench medarabiq fam_bench issai_diet`. None needs a login. `fetch.py` drops each clone's
  `.git` (a nested repository inside `Data/` would escape the vault's `.gitignore`) and zips the RuMedNLI and
  RuMedNER files, which must not be published (PhysioNet licence / no licence). `uv run db/prep.py issai` parses
  the ISSAI text files into `Data/issai-dietary-recommendation/derived/*.csv`.
- **Known gap:** the original Jamu scrape made 8 formula searches, but only "Jamu Batuk" is recorded, so
  `jamu_formula_herbs.csv` has 53 of the original 126 rows.

## Layout
| Path | Contents |
|---|---|
| `schema.sql` | all tables; the header comment defines the **id conventions** |
| `common.py` | `connect()`, `init_schema()`, `add_source()`, `data()`, `slug()`, `norm_text()` |
| `fetch.py` | downloads the raw datasets into `Data/<slug>/` |
| `prep.py` | turns raw files into the derived CSVs the build reads (PDF tables, Markdown, scrapes) |
| `build.py` | orchestrator; runs the stages in `STAGES` order |
| `build/<stage>.py` | one module per stage, each exposing `build(con)` |
| `build/resolve_*.py` | shared resolvers, one file per entity stage, re-exported by `build/resolve.py` |
| `maps/*.csv` | small curated maps: nutrients, actions, manual ingredient matches |
| `views.sql` | analysis views (`v_ingredient_condition_all`, `v_dish_condition`, `v_condition_dish`) |
| `export.py` | writes the 3 flat tables `dishes`, `ingredients`, `effects` to `export/` (Parquet + CSV) |
| `cases.py` | writes the patient-case table `cases` to `export/` (Parquet + CSV), see *Patient cases* below |
| `cues.py` | keyword patterns (EN / RU / KK / ZH / AR / FA) for cultural cues (place, ethnicity, religion, habit, food, traditional medicine) and diet content; `cases.py` calls `cues.tag`; run alone it counts them per dataset; a lower bound, check with `--examples` |
| `prep_issai.py` | ISSAI dietary-profile parser, run by `prep.py issai` |
| `viewer/index.html` | browser viewer for the exported tables (the Cases tab appears when `cases.parquet` exists): `uv run python -m http.server 8765 -d db` → http://localhost:8765/viewer/ |
| `trace.py` | CLI that prints dish → condition and condition → dish traces |
| `build_report.md` | generated: row counts, match rates, orphan checks |
| `presentation/` | interactive presentation: `uv run db/presentation/export.py` (after a build) writes `Database/presentation/index.html` from the DB, `content.py` (curated dataset text) and `template.html` |

## Patient cases (`cases.py`)
One flat table for testing whether an LLM gets better at medicine with the graph (topic `kg-medical-eval`,
`Questions/Q4 Patient case-conclusion datasets.md`, `Questions/Q5 Evaluating KG-augmented medical LLMs.md`). It is
not linked to the graph tables yet; matching cases to graph ids is the next step.

| Column | Meaning |
|---|---|
| `case_id` | `<dataset>:[<part>:]<id in the source file>`, unique, e.g. `rumedbench:top3-dev:q43dfecc`, `mtcmb:msdd:12`, `ngqa:4151` |
| `source` | dataset note name, `Datasets/<source>.md` |
| `case` | what is put to the model (patient text, case record, profile or dish + question), in the dataset's own language |
| `conclusion` | the dataset's answer (diagnosis, ICD-10 code, TCM syndrome and formula, doctor's answer, yes/no + reason); not always gold, see `gold` |
| `part`, `lang`, `origin` | dataset part (key of `PARTS` in `cases.py`), language, and where the case comes from |
| `case_ai`, `conclusion_ai`, `gold` | whether a model wrote the case text or the conclusion, and the summary `gold` / `weak gold` / `ai-generated` |
| `cue_*`, `culture_by_construction`, `diet` | flags from `cues.py` and from the part |
| `relevance`, `relevance_why` | high / medium / low for a culturally aware evaluation, and the reason (`relevance()` in `cases.py`) |

38,301 rows from 11 datasets; per-source rules are in the docstring of each reader in `cases.py`, counts and examples in
`Database/Export tables.md`.
- **Texts are copied as they are.** When a source stores the case or the answer as fields, `cases.py` writes them one
  per line as `field: value`, with the source's own field names.
- **Left out:** the ISSAI profiles (answers are GPT-4 outputs, not gold); multiple-choice exam items (MTCMB exam sets,
  TCM-BEST4SDT knowledge questions, the other MedArabiQ files); FAM-Bench Task 2; NGQA's nutrition tags and edges
  (they are what the answer is checked against); MedCaseReasoning's `diagnostic_reasoning`.
- **Licences:** MedArabiQ (100 rows) allows internal research only, so `export/` must never be committed or shared;
  MedicationQA and FAM-Bench answers quote third-party websites.

## Contract between stages
- **Ownership.** Each stage owns the tables it fills. It first deletes its own rows (`DELETE FROM t WHERE source_id IN (...)`,
  or the whole table if it owns all of it), so re-running a stage is safe.
- **Ids.** Ids are deterministic, following the conventions in `schema.sql`. That lets a later stage build an id
  without querying, e.g. `'ING:' + slug(name)` or `'MESH:D003474'`.
- **Resolvers.** Each entity stage writes its resolver class in its own `build/resolve_<entity>.py` (re-exported by `build/resolve.py`). A resolver loads its lookup tables from
  the DB once and returns ids or `None`:
  - `ConditionResolver(con).by_mesh(id)`, `.by_umls(cui)`, `.by_icd11(code)`, `.by_text(text, lang='en')` →
    `condition_id | None`. Free text is matched against aliases (normalised with `norm_text`), then against the
    action map.
  - `CompoundResolver(con).by_inchikey()`, `.by_cid()`, `.by_cas()`, `.by_mesh()`, `.by_name()`,
    `.by_xref(db, id)` → `compound_id | None`.
  - `IngredientResolver(con).by_xref(db, id)`, `.by_taxon(taxid)`, `.by_scientific(name)`,
    `.by_text(text, lang)` → `(ingredient_id, match_method, score) | None`.
- **Provenance.** Every row carries `source_id`, a code registered in `build/sources.py`. Every link row carries an
  `evidence_type` from `evidence_type`.
- **Working copies.** During development each stage can be run against its own file with
  `UNIFIED_DB=<path> uv run db/build.py --only …`, which avoids DuckDB's single-writer lock.

## Data quirks handled in loaders
- **FooDB `Compound.csv`: the header is shifted.** Read it by position. The true order is `id, public_id, name,
  state, annotation_quality, description, cas_number, moldb_smiles, moldb_inchi, moldb_mono_mass, moldb_inchikey,
  moldb_iupac, kingdom, superklass, klass, subklass`.
- **FooDB `Content`:**
  - keep `source_type='Compound'`;
  - rows with `citation_type='PREDICTED'` get `evidence_type='predicted'`;
  - normalise units (`mg/100g` = `mg/100 g`).
- **CTD:** `CTD_chemicals_diseases_curated.tsv` `ChemicalID` has no `MESH:` prefix, while `CTD_chemicals.tsv` does.
  `DirectEvidence='therapeutic'` → direction `beneficial`; `'marker/mechanism'` → direction `marker`.
- **Japan MEXT / Korea composition values:** `Tr`, `(x)` and `-` markers must be parsed. `(x)` means "estimated",
  and `-` means "not analysed".
