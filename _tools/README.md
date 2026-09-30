# Vault conventions & workflow

## Folders
| folder / file | contents |
|---|---|
| `Datasets/` | one note per dataset, latest version only (`Templates/Dataset.md`), the main unit of this vault |
| `Countries/`, `Regions/` | one note per country / region summarising the data available for it (`Templates/Country.md`, `Region.md`) |
| `Data/<slug>/` | downloaded dataset files (git-ignored) + committed `schema.md` and `sample*.csv` from `profile_dataset.py` |
| `Papers/` | one note per processed paper (`Templates/Paper.md`), linked to the dataset(s) it introduces |
| `Questions/` | one note per research question, the living answer (`Templates/Question.md`) |
| `Sessions/` | one summary per research session, a dated snapshot (`Templates/Session.md`) |
| `Backlog/` + `Backlog.md` | one properties-only note per candidate paper (`Templates/Candidate.md`) + hub with views |
| `Attachments/<citekey>/` | PDFs (git-ignored) and the figures embedded in paper notes |
| `Datasets.base`, `Papers.base`, `Backlog.base` | Obsidian Bases: live tables of datasets / papers / candidates, embedded in other notes |
| `.cache/docling/<citekey>/` | full docling extraction (hidden from Obsidian, git-ignored) |
| `_tools/` | extraction and checking scripts (excluded from Obsidian) |

## Processing a paper (candidate → paper)
Papers enter the vault as candidate notes in `Backlog/` (see *Backlog*). To process one:
1. In its candidate note set `status: processing`, check `citekey` (`FirstAuthorSurnameYEAR`, ASCII,
   add `a`/`b` if the key is already used in `Papers/`) and `pdf_url`.
2. `uv run _tools/extract_all.py` → PDF in `Attachments/<key>/`, docling output in `.cache/docling/<key>/`
   (`<key>.md` full text, `figures.md` caption index, `tables.md` all tables, `figs/*.png`).
   Long PDFs are cut at 45 pages. Pass citekeys as arguments to (re-)extract specific papers.
3. Pick figures: `_tools/pick_figure.sh <key> fig-03-p5.png` → prints the `![[...]]` embed.
4. **Promote the same note**: move it to `Papers/`, rename to `<key> - <Short title>`, replace
   `type/candidate` with `type/paper` (+ `relevance/…`, facet tags), delete `status`/`priority`/`why`,
   add the remaining `Templates/Paper.md` properties (`questions`, `pdf`, `peer_reviewed`…) and body.
   Keep `found_by`/`cited_by`: they record where the paper came from. Obsidian updates links on rename.
5. Link it from the relevant `Questions/*.md` and summarise the session in `Sessions/` (see below).
6. `python3 _tools/check_vault.py` to verify properties, links and embeds.

## Paper note properties
| property | values |
|---|---|
| `title`, `citekey`, `authors`, `year` | |
| `published` | `YYYY-MM-DD` (arXiv v1 or journal date) |
| `venue` | e.g. `ICLR 2026`, `Nature`, `arXiv preprint` |
| `peer_reviewed` | `true` / `false` / `workshop` |
| `url`, `arxiv`/`doi`, `pdf`, `pdf_url` | `pdf: "[[<key>.pdf]]"`; `pdf_url` is what `extract_all.py` downloads |
| `topics` | list of topic slugs (a paper can serve several topics) |
| `questions` | list of question ids, e.g. `[Q1, Q2]` |
| `relevance` | `core` / `adjacent`; what counts as core is defined per topic (see Topics) |

## Topics
A topic is a research thread with its own questions. Every paper, question, session and candidate
note carries `topics: [...]`. Start a new topic by adding a row here and creating its question notes
from `Templates/Question.md`.

| topic slug | questions | `core` means |
|---|---|---|
| `cultural-food-health` | Q1–Q3 | the dataset carries explicit culture / cuisine / country labels **and** is food, ingredient or food-compound data (global resources without culture labels, e.g. FooDB, are `adjacent` unless they are the only link to health effects) |

## Tags (nested; add new leaves freely, keep the prefixes)
Generic (every topic):
- `type/` paper · candidate · question · session · backlog
- `relevance/` core · adjacent
- `q/` 1 · 2 · 3-1 … (question `Q3.1` → tag `q/3-1`; new question → new `q/…` + note in `Questions/`)
- `subject/` what was studied (e.g. `llm`, `agent`, `human`)

Topic-specific facets: add a prefix per topic when useful (e.g. `method/`, `dataset/`, `stressor/`)
and list its values here so later notes reuse them.

`cultural-food-health` facets:
- `kind/` food · ingredient · compound
- `access/` open · api · registration · request · contact · commercial · unavailable · accessed · blocked
- `region/` middle-east · central-asia · south-asia · east-asia · southeast-asia · europe · africa · americas · oceania · global
- `tradmed/` ayurveda · tcm · kampo · korean · unani · persian · jamu (traditional-medicine systems)

## Dataset notes
`Datasets/<Name>.md` from `Templates/Dataset.md`. One note per dataset, **latest version only**: older
versions and what the new one adds go in `previous_versions` and the *Versions* section. Datasets
without a paper are welcome; datasets with papers link them in `papers: ["[[<paper note>]]"]`, and the paper
note links back in `datasets:`.

| property | values |
|---|---|
| `slug` | lowercase-hyphenated; also the folder name in `Data/` |
| `kind` | list of `food` / `ingredient` / `compound` |
| `availability` | what the authors/owners offer: `open-download` · `open-api` · `open-web` (browse/search pages only, no bulk file) · `registration` (free account) · `on-request` (form/email documented) · `contact-authors` (no link or dead link) · `commercial` · `unavailable` |
| `accessed` | whether **we** got the data: `true` · `partial` (subset, web pages only, sample) · `false` |
| `access_method` | how we got it: `github` · `kaggle` · `huggingface` · `zenodo` · `figshare` · `website-download` · `api` · `scrape` |
| `access_date`, `access_link`, `access_notes` | when, the link used, what blocked or limited access |
| `countries`, `regions` | wikilinks to `Countries/` and `Regions/` notes; use the country's common English name (`[[United Arab Emirates]]`, `[[China]]`) |
| `has_ingredients` (bool), `has_amounts` (`yes`/`partial`/`no`), `has_cooking_method` (`steps`/`tags`/`no`), `has_nutrition` (bool) | food datasets |
| `body_effect` (`direct`/`linkable`/`no`), `body_effect_how` | ingredient/compound datasets: `direct` = the dataset itself has health/disease/indication/target fields; `linkable` = its ids join to a resource that has them |
| `join_keys` | ids usable for joins: `PubChem CID`, `InChIKey`, `FooDB id`, `USDA FDC id`, `NCBI taxon`, `scientific name`, … |

Accessed datasets: download to `Data/<slug>/` (≤ ~500 MB; otherwise a subset), then
`uv run _tools/profile_dataset.py <slug>` writes `schema.md` + `sample.csv`. The note's *Tables & columns*
explains what each column means. Kaggle downloads work without credentials via `kagglehub`
(`uv run python -c "import kagglehub; print(kagglehub.dataset_download('owner/name'))"`), and
Hugging Face via `hf download --repo-type dataset`.

## Country & region notes
`Countries/<Country>.md` (`Templates/Country.md`), `Regions/<Region>.md` (`Templates/Region.md`). A dataset
lists every country it has data for; region-only labels (e.g. "Middle Eastern cuisine") go in `regions`.
Sub-national cuisines (Punjabi, Sichuan) are described inside the country note. Each country note embeds
`![[Datasets.base#This country]]`.

## Question notes
`Questions/Qx <short name>.md` from `Templates/Question.md`, properties `id: Qx`, `topics`, tags
`type/question`, `q/x`. Question ids are global across topics: keep numbering upward. Cite papers inline as
`[[<citekey> - <short title>|Author et al. YEAR]]` (inside tables escape the pipe: `\|`). Each embeds
`![[Papers.base#This question]]`, which lists every paper whose `questions` contains the note's `id`.

## Session notes
Each research session gets a summary in `Sessions/YYYY-MM-DD <Topic> - <kind>.md` from
`Templates/Session.md`: properties `date`, `session`, `topics`, `questions` plus matching `q/…` tags
and `type/session`, and a "Questions addressed" callout at the top. Session notes are snapshots; the
living answers are in `Questions/`.

## Backlog
One note per candidate in `Backlog/`, properties only (`Templates/Candidate.md`), browsed through the
views in `Backlog.base` (embedded in `Backlog.md`, in session notes and in every paper note).

| property | values |
|---|---|
| `status` | `candidate` → `processing` → *(promoted to `Papers/`)* or, for datasets, `processed` (+ `dataset: "[[<dataset note>]]"`) · `rejected` (+ `reason`) |
| `priority` | 1 = process next · 2 = relevant · 3 = peripheral / background |
| `topics`, `relevance` | as for papers; `relevance` is the first guess (core / adjacent) |
| `manipulation`, `outcome`, `why` | what the paper varies, what it measures, one-line reason |
| `found_by` | provenance tags such as `search/<strand>` |
| `cited_by` | links to processed papers whose reference lists include it (feeds the *Cited by this paper* view) |
| `pdf_url`, `url`, `arxiv`, `citekey`, `published`, `added` | |

Filenames are `<citekey> - <short title>`. Rejected candidates stay with `status: rejected` so later
searches don't resurface them. Before adding a candidate, search the vault for its arXiv id
(`check_vault.py` also flags duplicate arXiv ids). `Backlog/` is hidden from the graph (`-path:Backlog`).

## Citations
`uv run _tools/citations.py` fetches each paper's full reference list from Semantic Scholar (cached in
`.cache/citations/`) and matches it against `Papers/` and `Backlog/` by arXiv id, DOI or title. It owns
these properties (recomputed on every run, don't edit by hand):
- papers: `cites` (vault notes it cites), `cited_by` + `cited_by_count` (processed papers citing it)
- candidates: `cited_by` (merged with hand-added entries) + `cited_by_count`

It also prints references *not* in the vault that several processed papers cite (backward snowball;
`--add-min N` turns those cited by ≥ N papers into candidate notes with `found_by: [citations/backward]`),
and with `--forward` papers citing several processed papers. Views: `Backlog.base#Most cited`,
`Papers.base#Most cited in vault`. Rerun after processing new papers. Set `S2_API_KEY` (in `~/.zshrc` or a
git-ignored `.env`) to use a Semantic Scholar API key; without one it paces requests at 1 per 3 s.


## Git
PDFs (`Attachments/**/*.pdf`) and the docling cache (`.cache/`) are git-ignored (most papers may not be
redistributed). After a fresh clone run `uv sync && uv run _tools/extract_all.py` to re-download and
re-extract them from each note's `pdf_url`. PDFs behind bot protection (e.g. SSRN) must be saved
manually to `Attachments/<key>/<key>.pdf` first; the script then reuses them.
