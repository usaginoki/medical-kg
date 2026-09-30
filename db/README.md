# Unified dish ↔ condition database

A DuckDB database that links **dishes → ingredients → compounds → conditions** (symptoms and diseases) and back,
built from the datasets documented in `Datasets/`. Human-facing documentation is in `Database/Unified database.md`,
and example traces are in `Database/Traces - *.md`.

```
uv run db/build.py --fresh          # full build → db/unified.duckdb (git-ignored)
uv run db/trace.py dish "Kabsa" --country SA
uv run db/trace.py condition "nausea" --country IN --drug warfarin
```

## Layout
| Path | Contents |
|---|---|
| `schema.sql` | all tables; the header comment defines the **id conventions** |
| `common.py` | `connect()`, `init_schema()`, `add_source()`, `data()`, `slug()`, `norm_text()` |
| `build.py` | orchestrator; runs the stages in `STAGES` order |
| `build/<stage>.py` | one module per stage, each exposing `build(con)` |
| `build/resolve_*.py` | shared resolvers, one file per entity stage, re-exported by `build/resolve.py` |
| `maps/*.csv` | small curated maps: nutrients, actions, manual ingredient matches |
| `views.sql` | analysis views (`v_ingredient_condition_all`, `v_dish_condition`, `v_condition_dish`) |
| `trace.py` | CLI that prints dish → condition and condition → dish traces |
| `build_report.md` | generated: row counts, match rates, orphan checks |
| `presentation/` | interactive presentation: `uv run db/presentation/export.py` (after a build) writes `Database/presentation/index.html` from the DB, `content.py` (curated dataset text) and `template.html` |

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
