# Cultural food & health datasets: research vault

An Obsidian vault that surveys the data an agent would need to give **culturally tuned medical advice and analysis**:
what people in different cultures eat, which ingredients they use, and what the compounds in those foods may do to
the body. Part of an MBZUAI project (Department of Natural Language Processing, supervised by Dr. Fajri Koto) on an
agentic system for medical advice augmented with cultural knowledge.

Built from [usaginoki/research-vault-template](https://github.com/usaginoki/research-vault-template) and adapted from a
paper-centric literature review to a **dataset-centric survey**.

## Research questions
| | Question | Note |
|---|---|---|
| Q1 | Which datasets describe the foods and dishes of different cultures, and do they give ingredients, amounts and cooking methods? | [Q1](Questions/Q1%20Cultural%20food%20datasets.md) |
| Q2 | Which datasets describe the ingredients (foods, spices, herbs, medicinal plants) of different cultures, and can their effect on the body be inferred? | [Q2](Questions/Q2%20Cultural%20ingredient%20datasets.md) |
| Q3 | Which datasets link foods and ingredients to chemical compounds, and those compounds to effects on the body? | [Q3](Questions/Q3%20Food%20compound%20%26%20health-effect%20datasets.md) |

**Priority regions:** Middle East / GCC, Central Asia, South Asia, East Asia and Southeast Asia.

## Where to start
1. **[Session summary](Sessions/2026-09-30%20Cultural%20food-health%20datasets%20-%20survey.md)**: the main
   takeaways, the datasets to read first, and the open next steps.
2. **The Q1–Q3 notes**: recommendations and comparison tables. Q3 also shows how to chain
   *dish → ingredient → compound → effect → food–drug safety*, and lists the licence constraints.
3. **`Datasets.base`**, opened in Obsidian: live tables of all datasets. Views: *Food* (ingredients / amounts /
   cooking method), *Ingredients & compounds* (effect on the body), *Access status*, *Needs contact*.
4. **`Countries/` and `Regions/`**: what data exists for each country, e.g. `Countries/Saudi Arabia.md`,
   `Regions/Central Asia.md`. `Regions/Global.md` covers the resources with no country labels.
5. **[Unified database](Database/Unified%20database.md)**: a DuckDB database linking dishes → ingredients →
   compounds → symptoms/diseases and back (`db/`), with worked traces in `Database/`.
6. **[Access requests](Access%20requests.md)**: datasets that need a person to act (an email, a form, an account).
   Drafts are in `Access-help/`, each tracked by a GitHub issue labelled `access-request`.

## What's in it (survey of 2026-09-30)
| | Count |
|---|---|
| Dataset notes (`Datasets/`): access status, tables and columns, countries, food and body-effect flags | 43 (29 fully downloaded, 13 partially, 1 not accessed) |
| Paper notes (`Papers/`): light notes on the papers behind the datasets | 36 |
| Candidates (`Backlog/`): datasets found but not yet processed | 143 (43 processed) |
| Country / region notes | 224 / 12 |

For each dataset the note records:
- whether the owners make it available (`availability`), and whether **we actually got it** (`accessed`, `access_method`);
- every table with its columns and what they mean;
- the countries and regions covered, with per-country counts;
- for food datasets: whether they list ingredients, whether amounts are given, and whether the cooking method is included;
- for ingredient and compound datasets: whether an effect on the body can be inferred (`direct` / `linkable`), and how.

Only the latest version of each dataset gets a note; earlier versions are described inside it.

## Layout
```
Datasets/     one note per dataset (main unit)    Templates/   Dataset, Country, Region, Paper, Candidate, Question, Session
Countries/    one note per country                 _tools/      scripts + README.md (conventions)
Regions/      one note per region (+ Global)       Data/<slug>/ downloaded data (ignored); schema.md + sample*.csv committed
Papers/       papers behind the datasets           Access-help/ drafts of access requests (emails, forms)
Questions/    Q1–Q3 living answers                 Datasets.base, Papers.base, Backlog.base   live tables
Sessions/     dated session summaries              Access requests.md, Backlog.md             hubs
Backlog/      candidate datasets
```
Conventions for properties, tags, topics and the workflow are in [`_tools/README.md`](_tools/README.md). Claude Code
follows [`CLAUDE.md`](CLAUDE.md), whose section *Dataset-centric topics* covers this survey.

## Setup
1. Clone, then run `uv sync`. This installs pandas/pyarrow, kagglehub, and docling with CPU-only torch (~1.5 GB in `.venv/`).
2. Open the folder as a vault in Obsidian. Bases is a core plugin; no community plugins are needed.
3. Raw data is **not in git**. Each dataset note explains how the data was obtained (link, method, date). Kaggle and
   Hugging Face downloads work without credentials, via `kagglehub` and `hf download`. FooDB and HMDB must be
   downloaded in a browser, because their sites block scripts with a Cloudflare challenge.

## Tools
| Command | What it does |
|---|---|
| `uv run _tools/profile_dataset.py <slug>` | Profiles every table in `Data/<slug>/` (csv/tsv/json/jsonl/parquet/xlsx/sqlite) and writes `schema.md` (rows, columns, dtypes, non-null share, examples) and `sample.csv` |
| `uv run db/build.py --fresh` | Builds the unified dish ↔ condition DuckDB (`db/unified.duckdb`, ~2 min); writes `db/build_report.md` |
| `uv run db/trace.py dish\|condition\|sql …` | Prints dish → condition or condition → dish traces with sources and evidence grades |
| `python3 _tools/build_geo.py [--check]` | Creates or refreshes `Countries/` and `Regions/` notes from the datasets' `countries` / `regions`. Only the generated block is rewritten; hand-written text is kept |
| `python3 _tools/check_vault.py` | Checks required properties, allowed values in dataset notes, country/region links, `schema.md` for accessed datasets, duplicate note names, and that links and embeds resolve |
| `uv run _tools/extract_all.py [citekey …]` | Downloads paper PDFs and extracts them with docling (template tool) |
| `uv run _tools/citations.py` | Fills in citation links from Semantic Scholar (template tool) |

## Data & licences
- `Data/**` is git-ignored except `Data/<slug>/schema.md` and `Data/<slug>/sample*.csv`. Browser downloads go to
  `Data/<slug>/raw/`.
- Many sources are **non-commercial** or restricted. Examples:
  - IMPPAT and KNApSAcK are CC BY-NC-ND;
  - GRAYU's terms forbid using it to provide medical advice;
  - NII Cookpad forbids sending its data to external LLM services;
  - CTD requires notification when its data is used.

  The full list is in [Q3 → *Licences & usage constraints*](Questions/Q3%20Food%20compound%20%26%20health-effect%20datasets.md).
  The committed samples are small excerpts kept for documentation, and this repository is private.

## Open work
Tracked in [GitHub issues](https://github.com/usaginoki/medical-kg/issues):
- #1: systematically review the FAO/INFOODS food composition directory
- #2–#7: dataset access requests

Further next steps (full crawls of web-only relation layers, priority-1 backlog candidates, a join layer on
InChIKey) are listed in the session summary.

## Obsidian settings included
- `Templates/`, `_tools/`, `Data/` and `.venv/` are excluded; `Backlog/` is filtered out of the graph.
- The graph colours notes by type: question, session, dataset, country, region.
- Obsidian skills from [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) are in `.claude/skills/`.
