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
| `maps/*.csv` | small curated maps: nutrients, actions, manual ingredient matches (`ingredient_map_manual.csv`; rows with `scope=exact` are line fragments such as 'brown' → sugar that only match a whole residual line, never as aliases), grams per piece for count units (`piece_weights.csv`, mostly USDA household weights); `icd10_titles.csv` = WHO ICD-10 (2019) titles for the codes in RuMedPrime, taken from the `simple-icd-10` package, used by `cases.py` |
| `views.sql` | analysis views (`v_ingredient_condition_all`, `v_dish_condition`, `v_condition_dish`) |
| `export.py` | writes the 3 flat tables `dishes`, `ingredients`, `effects` to `export/` (Parquet + CSV) |
| `cases.py` | writes the patient-case table `cases` to `export/` (Parquet + CSV), see *Patient cases* below |
| `cues.py` | keyword patterns (EN / RU / KK / ZH / AR / FA) for cultural cues (place, ethnicity, religion, habit, food, traditional medicine) and diet content, with a stoplist of medical terms (India ink, FISH, 食物过敏史…), negation (before the match in the clause, or a denial after it) and weak / strong cue strength; `cases.py` calls `cues.tag`; run alone it counts them per dataset; a cheap screen, check with `--examples` |
| `checks/*_regress.py` | regression checks for the rule fixes of the 2026-10-14 audit: `cues_regress.py` (case cue screen, synthetic texts), `ingredients_regress.py`, `conditions_regress.py` (need `UNIFIED_DB`) |
| `llm/` | LLM tagging experiments after the rule screens (Gemini / Gemma via `GOOGLE_API_KEY` in `.env`): `client.py` (async structured output, workers, retries, SQLite cache in `.cache/llm/`, cost cap), one module per workflow (`w1_case_tags`, `w1b_leak`, `w2_case_facts`, `w3_ingredient_lines`, `w4_condition_terms`, `w5_dish_check`), `costs.py`, `fn_check.py` (recall of the case screen on rejected and weak-cue cases), `disagree.py` (items where 2+ models disagree with the reference, for manual review; verdicts in `.cache/llm/refs/w*_review.json` are applied by the scorers); full pass: `full_pass.py` (items per workflow, MedArabiQ excluded), `batch.py` (Gemini Batch API, $ cap), `store.py` (→ `export/llm/*.parquet`, see *LLM layer* below); results in `Database/LLM tagging experiments.md` |
| `prep_issai.py` | ISSAI dietary-profile parser, run by `prep.py issai` |
| `viewer/index.html` | browser viewer for the exported tables (the Cases tab appears when `cases.parquet` exists; LLM columns, filters and the *Line matches* / *Condition terms* tabs appear when `export/llm/*.parquet` exist): `uv run python -m http.server 8765 -d db` → http://localhost:8765/viewer/ |
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
| `cue_*`, `culture_by_construction`, `diet` | flags from `cues.py` and from the part (a negated match sets no flag) |
| `cue_strength`, `cue_hits`, `cues_negated` | strong / weak / none (weak = only race words or bare country, city or nationality names), and the matched words per cue type, kept and negated |
| `dup_group` | shared by versions of the same item (MedArabiQ ×3, ISSAI ×5), empty otherwise |
| `relevance`, `relevance_why` | high / medium / low for a culturally aware evaluation, and the reason (`relevance()` in `cases.py`; only strong cues count for high) |

38,301 rows from 11 datasets; per-source rules are in the docstring of each reader in `cases.py`, counts and examples in
`Database/Export tables.md`.
- **Texts are copied as they are.** When a source stores the case or the answer as fields, `cases.py` writes them one
  per line as `field: value`, with the source's own field names.
- **Left out:** the ISSAI profiles (answers are GPT-4 outputs, not gold); multiple-choice exam items (MTCMB exam sets,
  TCM-BEST4SDT knowledge questions, the other MedArabiQ files); FAM-Bench Task 2; NGQA's nutrition tags and edges
  (they are what the answer is checked against); MedCaseReasoning's `diagnostic_reasoning`.
- **Licences:** MedArabiQ (100 rows) allows internal research only, so `export/` must never be committed or shared;
  MedicationQA and FAM-Bench answers quote third-party websites.

## LLM layer (stored results, not part of the graph)
The full LLM pass runs the workflows of `Database/LLM tagging experiments.md` over what the rule screens hand off, through
the Gemini Batch API (half price; `LLM_BATCH_MAX_USD`, default 40), and stores the answers as separate tables:
```
uv run db/llm/full_pass.py items        # items per workflow -> .cache/llm/full/ (MedArabiQ excluded, GitHub issue #11)
uv run db/llm/full_pass.py submit       # batch jobs (cached items skipped); status / collect / costs
uv run db/llm/store.py                  # -> export/llm/llm_*.parquet
uv run db/build.py --only llm           # -> llm_* tables in unified.duckdb
```
| Table | Key | Contents |
|---|---|---|
| `llm_case_tags` | case_id | culture_reason (1–2 English sentences), culture_role, diet_relevant, graph_answerable, cues[] (type, text, negated, about) (W1, prompt `w1-v3`) |
| `llm_case_facts` | case_id | age, sex, country, region_or_city, ethnicity, religious_practices, symptoms, history, diagnosis_en, foods[] (with ingredient_id, dish_ids), drugs, condition ids for diagnosis / symptoms / history (W2) |
| `llm_ingredient_lines` | raw_text (lower-cased) | current match vs LLM kind, name_en, choice, fit, llm_ingredient_id, agrees (W3) |
| `llm_condition_terms` | source + term | kind, meaning, evidence_level, conditions[] (name, relation, condition_id) (W4) |
| `llm_dishes` | dish_id | stored vs LLM cuisine country, kind, name_en, style (W5) |

Every row has `model`, `prompt_version`, `stored_at`. The stage `llm` owns these tables only; no graph table, view or
export reads them (GitHub issue #12 tracks whether and how to integrate them). The files are git-ignored like `cases`.

## Contract between stages
- **Ownership.** Each stage owns the tables it fills. It first deletes its own rows (`DELETE FROM t WHERE source_id IN (...)`,
  or the whole table if it owns all of it), so re-running a stage is safe.
- **Ids.** Ids are deterministic, following the conventions in `schema.sql`. That lets a later stage build an id
  without querying, e.g. `'ING:' + slug(name)` or `'MESH:D003474'`.
- **Resolvers.** Each entity stage writes its resolver class in its own `build/resolve_<entity>.py` (re-exported by `build/resolve.py`). A resolver loads its lookup tables from
  the DB once and returns ids or `None`:
  - `ConditionResolver(con).by_mesh(id)`, `.by_umls(cui)`, `.by_icd11(code)`, `.by_text(text, lang='en')` →
    `condition_id | None`. Free text is matched against aliases (normalised with `cond_keys`), then all-caps
    acronyms (case-sensitive: 'PTSD', not 'face' → FACE), then the action map, then fuzzy (ratio ≥ 93; numbers, sex,
    acute/chronic and hyper/hypo must agree). When an alias names several conditions, `alias_score` decides:
    curated (`condition_synonyms.csv`) > MEDIC's own synonym > SymMap > HERB > CMAUP/DDID alias, then MEDIC row,
    primary name, MeSH descriptor (`D`) before supplementary concept (`C`) / OMIM. Lay and organ words from
    HERB/SymMap ('Heat', 'Wind', 'Tongue, unspecified') and 1–3 letter aliases are not matched (`noisy_alias`).
    The same ranking picks the ICD-11 `same_as` twin.
  - `CompoundResolver(con).by_inchikey()`, `.by_cid()`, `.by_cas()`, `.by_mesh()`, `.by_name()`,
    `.by_xref(db, id)` → `compound_id | None`. `by_name` never maps a class word ('RESIN', 'SUGARS') to a single
    molecule that lists it as a synonym, returns None for isomer-less names ('PINENE', 'CAROTENE'), and lets synonym
    hits compete with a structured primary-name hit only when they have the same InChIKey.
  - `IngredientResolver(con).by_xref(db, id)`, `.by_taxon(taxid)`, `.by_scientific(name)`,
    `.by_text(text, lang)` → `(ingredient_id, match_method, score) | None`. Methods: `exact`, `normalised`, `manual`
    (curated map), `substring` (a guess from part of the text: English sub-phrase, CJK substring where the longest
    alias wins and generic heads such as 肉 / 里脊 → pork lose to '牛' words), `fuzzy` (English: token-sort ≥ 92, same
    first three letters, food-source aliases only, `FUZZY_BLOCK` pairs refused). `.by_text_strict` stops before the
    guesses; `.by_text_parts` splits a line that names several ingredients ('salt and pepper', '土豆，面粉，鸡蛋',
    'ginger green chillies garlic') where every part resolves, and keeps the first resolvable alternative of
    'besan / gram flour', 'ghee or oil'.
- **Provenance.** Every row carries `source_id`, a code registered in `build/sources.py`. Every link row carries an
  `evidence_type` from `evidence_type` (ranks: clinical 1, curated_literature 2, epidemiological 3, traditional 4,
  text_mined 5, in_vitro 6, predicted 7). `compound_condition.note` and `ingredient_condition.note` keep the source
  term ('Antitumor', 'Breast cancer', CTD's 'therapeutic' / 'marker/mechanism'); the note of a link to an animal-model
  condition (`condition.animal_model`: MeSH '…, Experimental' and descendants) starts with 'animal model; '.
  `v_ingredient_condition_all` and the `effects` export carry the compound note on via-compound paths.
- **Regression checks.** `UNIFIED_DB=<path> uv run db/checks/conditions_regress.py` asserts the condition, compound
  and link fixes of the 2026-10-14 audit; `db/checks/ingredients_regress.py` does the same for ingredient and
  dish-line matching (fragment rows, CJK meats, fuzzy false friends, CulinaryDB entity ids, splits, junk lines, units).
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
  `DirectEvidence='therapeutic'` → direction `beneficial`; `'marker/mechanism'` → direction `marker`, shown by
  `trace.py` as "Marker / mechanism" because it mostly means the chemical induces or worsens the disease.
- **Dr. Duke AGGREGAC / FooDB health effects:** Duke's chemical activities are reported pharmacology (mostly in vitro or
  animal) → `evidence_type='in_vitro'`. FooDB `CompoundsHealthEffect` cites Duke for 10,930 of 11,062 rows; those
  are stored as source `duke` (note '… (via FooDB)'), so they merge with AGGREGAC rows instead of counting as a second
  source; only the ChEBI rows stay `foodb`.
- **Dish ingredient lines (`build/dishes.py`):**
  - website menus ('home', 'recipes', 'gardening'), notes, unit conversions ('1 cup = 235 ml'), bare numbers and
    section headers ('for tempering:', '#调料', '馅料：') are dropped (`junk_line`; counts in the build log);
  - IndicRecipeNutri grams are kept with their tier in `dish_ingredient.weight_tier` (A–E; D/E are default weights for
    lines without a stated amount, E is 20 g) and `weight_confident`; count units ('2 eggs', '3瓣蒜', '1 large onion')
    get grams from `maps/piece_weights.csv` (`weight_tier='piece'`); 勺/汤匙 = 15 g, 小勺/茶匙 = 5 g;
  - a line split into several ingredients gives one row per part (`split_part` 1..n, `ingredient_text` = the part)
    with quantity, unit and grams NULL, because the amount belongs to the whole line;
  - CulinaryDB's entity id is its own aliasing of the line and is often coarse or wrong ('kaffir lime leaves' →
    Bantu beer, 'oyster sauce' → oyster, 'sunflower oil' → sunflower): a strict text match of the original line to a
    different ingredient wins (entities 10, 141, 980 always defer to the text);
  - IndicRecipeNutri dish names lose their SEO tails ('… Recipe | … Recipe - How to make …').
- **Japan MEXT / Korea composition values:** `Tr`, `(x)` and `-` markers must be parsed. `(x)` means "estimated",
  and `-` means "not analysed".
