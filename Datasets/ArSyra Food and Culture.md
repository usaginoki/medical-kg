---
title: "ArSyra Food and Culture"
slug: arsyra-food-and-culture
kind: [food]
version: "2026.03.31 export (Kaggle aqlomate/arsyra-food, kagglehub version 9)"
previous_versions: "Kaggle versions 1–8 (not inspected)"
papers: []
url: "https://www.kaggle.com/datasets/aqlomate/arsyra-food"
license: "CC-BY-NC-SA-4.0 (preview); full data sold under ArSyra academic (from $29) / commercial (from $99) licenses"
availability: commercial
access_link: "https://www.kaggle.com/datasets/aqlomate/arsyra-food"
accessed: partial
access_method: [kaggle]
access_date: 2026-09-30
access_notes: "kagglehub downloaded the free preview (12.5 kB zip): 50 records in data/all.jsonl (duplicated as data/food_culture.jsonl), metadata.json and README.md. The full 4,579 records require purchase at arsyra.com/datasets.html (Stripe checkout). The HF-style README also describes a gated 'Request Access' form. We did not buy or request anything."
countries: ["[[Syria]]", "[[Tunisia]]", "[[Morocco]]", "[[Palestine]]", "[[Iraq]]", "[[Egypt]]", "[[Algeria]]", "[[Saudi Arabia]]", "[[Jordan]]", "[[Lebanon]]", "[[United Arab Emirates]]", "[[Sudan]]", "[[Yemen]]", "[[Libya]]", "[[Kuwait]]"]
regions: ["[[Middle East]]", "[[North Africa]]"]
n_records: "50 preview records (full: 4,579 claimed, 3,679 native-speaker + 900 synthetic)"
size: "47 KB (preview)"
formats: [jsonl, json]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [country (ISO-2), dialect_group, question_code]
topics: [cultural-food-health]
questions: [Q1]
relevance: adjacent
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/commercial
  - region/middle-east
---
# ArSyra Food and Culture

> [!abstract] TL;DR
> This is a commercial Arabic-dialect NLP sample from the ArSyra crowdsourcing platform (arsyra.com). Speakers answer fixed prompts in their dialect, e.g. "How do you order falafel from a street cart in your dialect?", "What ingredients must always be in your kitchen?". **It is not a dish or recipe database.** The Kaggle download is a **50-record preview, all from one Syrian (Levantine) speaker**. The claimed full set (4,579 records, 17 "countries" incl. placeholders `EU` and `XX`, 20% synthetic) is sold from $29. Value for the agent is low: some dialect food vocabulary and restaurant phrases, with unverifiable provenance.

## Access
| | |
|---|---|
| Availability | commercial (a free 50-record preview on Kaggle; full data paid) |
| Link | https://www.kaggle.com/datasets/aqlomate/arsyra-food · https://arsyra.com/datasets.html |
| Accessed? | partial (preview only) |
| How | `uv run python -c "import kagglehub; print(kagglehub.dataset_download('aqlomate/arsyra-food'))"` |
| Downloaded | `Data/arsyra-food-and-culture/`: `data/all.jsonl` (50 rows), `data/food_culture.jsonl` (identical copy), `metadata.json`, `README.md` |

## Tables & columns
### `data/all.jsonl` (50 rows × 15)
| column | type | meaning | example |
|---|---|---|---|
| `question_code` | str | prompt id (42 distinct in the preview) | `FC-0002` |
| `category` | str | always `food_culture` | `food_culture` |
| `subcategory` | str | `cooking` 19, `restaurant` 18, `traditional_food` 13 | `traditional_food` |
| `question_text` | str | prompt in MSA | `كيف تطلب فلافل من عربة الشارع بلهجتك؟` ("How do you order falafel from a street cart in your dialect?", our translation) |
| `answer_text` | str | speaker's dialect answer | `اريد فلالفل` ("I want falafel", sic) |
| `response_time_ms` | int | answer time | `7258` |
| `quality_score` / `quality_grade` | int / str | automatic score 0–100 (mean 98.9) / grade | `100` / `A` |
| `country` | str | speaker country (ISO-2) | `SY` (all 50) |
| `dialect_group` | str | dialect group | `levantine` (all 50) |
| `difficulty` | str | prompt level | `beginner` (all 50) |
| `is_synthetic` / `data_source` | bool / str | native vs synthetic | `false` / `native_speaker` |
| `speaker_hash` | str | anonymised speaker | `anon-d2ViLTE3` (**1 speaker for all 50**) |
| `answered_at` | datetime | timestamp | `2026-02-20T11:13:58Z` (all on one day) |

The README documents a different schema (`text`, `msa_text`, `context`) than the actual file. There is no `msa_text` in the preview.

### `metadata.json`
- Export metadata: name, version `2026.03.31`, `totalRecords` 4,579, `nativeSpeakerRecords` 3,679, `syntheticRecords` 900, `accessModel: preview`.
- Country codes: SY, EU, TN, MA, PS, XX, IQ, EG, DZ, SA, JO, LB, AE, SD, YE, LY, KW.
- Dialect groups: levantine, maghrebi, iraqi, egyptian, gulf, sudanese, other.

Sample: `Data/arsyra-food-and-culture/sample.csv` · full profile: `Data/arsyra-food-and-culture/schema.md`

## Countries & cultures covered
- **In the data we have:** [[Syria]] 50 records (Levantine).
- **Claimed for the full product (metadata, no counts given):**
  - [[Syria]], [[Tunisia]], [[Morocco]], [[Palestine]], [[Iraq]], [[Egypt]], [[Algeria]], [[Saudi Arabia]], [[Jordan]], [[Lebanon]], [[United Arab Emirates]], [[Sudan]], [[Yemen]], [[Libya]], [[Kuwait]]
  - plus `EU` (diaspora?) and `XX` (unknown)
  - GCC countries claimed: Saudi Arabia, UAE, Kuwait (Gulf dialect group).
- These countries are listed on the owner's word only; per-country counts are unknown.

## Ingredients, amounts, cooking method
- There are no structured ingredients. Some answers name foods or ingredients in dialect, e.g. the "what ingredients are always in your kitchen" prompt → `سكر شاي` ("sugar, tea"). Answers are short and sometimes misspelled (`فلالفل`).

## Linking to other datasets
- No IDs. It could only be matched by country and dialect to [[ArabCulture]] (same countries; MBZUAI, expert-written, openly licensed), which is the better Arab food-culture resource.

## Versions
- Kaggle shows version 9 (2026-03-31 export). Earlier versions were not inspected.

## Caveats
- **Provenance and quality flags:**
  - vendor-produced marketing sample with no paper
  - preview from a single speaker on a single day
  - near-uniform auto quality scores (98.9 mean) despite visibly low-effort answers
  - 20% synthetic records in the full set
  - country list includes the placeholders `EU` and `XX`
  - README schema does not match the files
  - Kaggle title says "1,000+ records" while metadata says 4,579
- The license is conflicting: the preview is CC-BY-NC-SA-4.0, but the README forbids redistribution and sells licenses.
- Recommendation: do not buy for this project unless dialect food-term normalisation becomes a need. Relevance is set to `adjacent`.
