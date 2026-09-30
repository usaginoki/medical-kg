---
title: "BLEnD"
slug: blend
kind: [food]
version: "HF uilab/BLEnD, 2026-09-15 (adds SemEval-2026 Task 7 data for 17 language-culture pairs; MCQ file v1.1)"
previous_versions: "nayeon212/BLEnD (original HF repo, now redirects to uilab/BLEnD); 2024-06 release (16 cultures); 2024-12 translation fixes; MCQ v1 → v1.1 (2025-05)"
papers: ["[[Myung2024 - BLEnD]]"]
url: "https://github.com/nlee0212/BLEnD"
license: "CC-BY-SA-4.0"
availability: open-download
access_link: "https://huggingface.co/datasets/uilab/BLEnD"
accessed: true
access_method: [huggingface]
access_date: 2026-09-30
access_notes: "Candidate link nayeon212/BLEnD now 307-redirects to uilab/BLEnD. Downloaded all short-answer questions (CSV) and annotations for the 16 original cultures and the 17 SemEval-2026 cultures. The 180 MB English MCQ file (305,939 rows) was filtered to its food questions (85,148 rows) and only that subset kept; the SemEval MCQ split, questions_hf JSON duplicates and prompts were not downloaded. Not gated."
countries:
  - "[[Algeria]]"
  - "[[Australia]]"
  - "[[Azerbaijan]]"
  - "[[Bulgaria]]"
  - "[[China]]"
  - "[[Ecuador]]"
  - "[[Egypt]]"
  - "[[Ethiopia]]"
  - "[[France]]"
  - "[[Greece]]"
  - "[[India]]"
  - "[[Indonesia]]"
  - "[[Iran]]"
  - "[[Ireland]]"
  - "[[Japan]]"
  - "[[Mexico]]"
  - "[[Morocco]]"
  - "[[Nigeria]]"
  - "[[North Korea]]"
  - "[[Philippines]]"
  - "[[Saudi Arabia]]"
  - "[[Singapore]]"
  - "[[South Korea]]"
  - "[[Spain]]"
  - "[[Sri Lanka]]"
  - "[[Sweden]]"
  - "[[Taiwan]]"
  - "[[United Kingdom]]"
  - "[[United States]]"
regions: ["[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "33 cultures × 500 questions (16,500 short-answer questions; 3,465 food); 14,081 food answer clusters; 85,148 food MCQs (original 16 cultures)"
size: "61 MB downloaded (43 MB is the food MCQ subset)"
formats: [csv, json]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [question ID (shared template across cultures, e.g. Al-en-01), culture/country, answer text (dish / food / spice names)]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# BLEnD

> [!abstract] TL;DR
> BLEnD (Myung et al., NeurIPS 2024 Datasets & Benchmarks) asks the same 500 everyday-life questions in 16
> countries/regions, in the local language, and records the answers of ~5 native annotators each, with vote counts;
> in Sept 2026 the maintainers added 17 more language-culture pairs collected for SemEval-2026 Task 7 (incl. Saudi
> Arabia, Egypt, Morocco, Japan, Taiwan, Singapore ×3, Sri Lanka, Philippines). **105 of the 500 questions are about
> food** (common breakfast, snack, spice/herb, cooking oil, festival food, fruit, drinks…), so each culture has a small
> human-voted "what people here typically eat/use" profile. For the agent it is the best source here of *everyday*
> food habits (not dish catalogues) for Iran, Azerbaijan, Saudi Arabia, Egypt, Assam (India), Sri Lanka, China,
> Koreas, Indonesia/West Java — no Central Asia and no GCC state besides Saudi Arabia.

## Access
| | |
|---|---|
| Availability | open-download (HF, CC-BY-SA-4.0; code on GitHub) |
| Link | https://huggingface.co/datasets/uilab/BLEnD (was nayeon212/BLEnD) |
| Accessed? | yes (all short-answer data; MCQ only the food subset) |
| How | `hf download uilab/BLEnD --repo-type dataset --include data/questions/* data/annotations_hf/* data_SemEval/questions/* data_SemEval/annotations_hf/* …` |
| Downloaded | `Data/blend/data/{questions,annotations_hf}/` (16 cultures), `Data/blend/data_SemEval/{questions,annotations_hf}/` (17), `Data/blend/mc_questions_v1.1_food.csv` (food rows of `mc_questions_file_v1.1.json`), `Data/blend/food_answers_long.csv` (derived, see below), README |

## Tables & columns
### `data/questions/<Culture>_questions.csv`, `data_SemEval/questions/<Lang>_<Culture>_questions.csv` (500 rows each × 6)
| column | type | meaning | example |
|---|---|---|---|
| (unnamed) | int | row index | 0 |
| `ID` | str | question template id, shared across cultures | `Al-en-01` |
| `Topic` | str | one of Food (105), Holidays/Celebration/Leisure (92), Sport (88), Education (84), Work life (68), Family (63) | `Food` |
| `Source` | str | culture/language whose annotators proposed the template | `English (US)` |
| `Question` | str | question in the local language | `یک میان وعده معمول برای بچه‌های پیش دبستانی درایران چیست؟` |
| `Translation` | str | English version | `What is a common snack for preschool kids in Iran?` |

### `…/annotations_hf/<Culture>_data.json` (500 rows each)
| column | type | meaning | example |
|---|---|---|---|
| `ID` | str | question id | `Al-en-01` |
| `question` / `en_question` | str | local / English question | `What is a common snack for preschool kids in Iran?` |
| `annotations` | list of {`answers`, `en_answers`, `count`} | annotator answers grouped into variant clusters (local and English variants) with the number of annotators (of ~5) giving it | `{"answers": ["میوه"], "en_answers": ["fruit"], "count": 3}` |
| `idks` | dict | counts of `no-answer`, `idk`, `not-applicable` (+ free-text "other" reasons, hence the many sparse `idks.*` columns in schema.md) | `{"no-answer": 1, "idk": 0, "not-applicable": 0}` |

### `food_answers_long.csv` (14,081 rows × 8) — derived by us
Food questions only, one row per answer cluster: `subset` (BLEnD-2024 / SemEval-2026), `culture` (file key),
`ID`, `en_question`, `en_answer` (first English variant), `en_answer_variants`, `local_answers`, `count` (votes).
Built from the annotation JSONs by filtering `Topic == Food`.

### `mc_questions_v1.1_food.csv` (85,148 rows × 7) — food subset of the English MCQ
`MCQID`, `ID`, `country` (16 original cultures), `prompt` (full English prompt), `choices` (A–D JSON),
`choice_countries` (which culture each option comes from), `answer_idx`. Only 90 of the 105 food templates survive
the MCQ filtering (paper §3: questions with "not applicable" or no majority are dropped).

Sample: `Data/blend/sample.csv` · full profile: `Data/blend/schema.md`

## Countries & cultures covered
33 language-culture files → 29 countries (Assam → India, West Java → Indonesia, Northern Nigeria → Nigeria,
Basque Country → Spain; Singapore has Malay, Mandarin and Tamil files; Indonesia has Indonesian + West Java). Every
file has the same 500 templates, so each culture has **105 food questions**; the last column is how many answer
clusters those food questions received (a proxy for how much food knowledge was collected).

| subset | culture file | country | priority region | all questions | food questions | food answer clusters (rows in `food_answers_long.csv`) |
|---|---|---|---|---|---|---|
| BLEnD-2024 | `Algeria` | [[Algeria]] |  | 500 | 105 | 331 |
| BLEnD-2024 | `Assam` | [[India]] | South Asia | 500 | 105 | 546 |
| BLEnD-2024 | `Azerbaijan` | [[Azerbaijan]] | Caucasus | 500 | 105 | 346 |
| BLEnD-2024 | `China` | [[China]] | East Asia | 500 | 105 | 485 |
| BLEnD-2024 | `Ethiopia` | [[Ethiopia]] |  | 500 | 105 | 317 |
| BLEnD-2024 | `Greece` | [[Greece]] |  | 500 | 105 | 476 |
| BLEnD-2024 | `Indonesia` | [[Indonesia]] | Southeast Asia | 500 | 105 | 528 |
| BLEnD-2024 | `Iran` | [[Iran]] | Middle East | 500 | 105 | 466 |
| BLEnD-2024 | `Mexico` | [[Mexico]] |  | 500 | 105 | 563 |
| BLEnD-2024 | `North_Korea` | [[North Korea]] | East Asia | 500 | 105 | 437 |
| BLEnD-2024 | `Northern_Nigeria` | [[Nigeria]] |  | 500 | 105 | 339 |
| BLEnD-2024 | `South_Korea` | [[South Korea]] | East Asia | 500 | 105 | 366 |
| BLEnD-2024 | `Spain` | [[Spain]] |  | 500 | 105 | 503 |
| BLEnD-2024 | `UK` | [[United Kingdom]] |  | 500 | 105 | 461 |
| BLEnD-2024 | `US` | [[United States]] |  | 500 | 105 | 518 |
| BLEnD-2024 | `West_Java` | [[Indonesia]] | Southeast Asia | 500 | 105 | 414 |
| SemEval-2026 | `Arabic_Egypt` | [[Egypt]] | Middle East | 500 | 105 | 576 |
| SemEval-2026 | `Arabic_Morocco` | [[Morocco]] |  | 500 | 105 | 199 |
| SemEval-2026 | `Arabic_SaudiArabia` | [[Saudi Arabia]] | Middle East | 500 | 105 | 420 |
| SemEval-2026 | `Basque_BasqueCountry` | [[Spain]] |  | 500 | 105 | 413 |
| SemEval-2026 | `Bulgarian_Bulgaria` | [[Bulgaria]] |  | 500 | 105 | 387 |
| SemEval-2026 | `English_Australia` | [[Australia]] |  | 500 | 105 | 504 |
| SemEval-2026 | `French_France` | [[France]] |  | 500 | 105 | 482 |
| SemEval-2026 | `Irish_Ireland` | [[Ireland]] |  | 500 | 105 | 314 |
| SemEval-2026 | `Japanese_Japan` | [[Japan]] | East Asia | 500 | 105 | 446 |
| SemEval-2026 | `Malay_Singapore` | [[Singapore]] | Southeast Asia | 500 | 105 | 485 |
| SemEval-2026 | `Mandarin_Singapore` | [[Singapore]] | Southeast Asia | 500 | 105 | 437 |
| SemEval-2026 | `Mandarin_Taiwan` | [[Taiwan]] | East Asia | 500 | 105 | 465 |
| SemEval-2026 | `Spanish_Ecuador` | [[Ecuador]] |  | 500 | 105 | 492 |
| SemEval-2026 | `Swedish_Sweden` | [[Sweden]] |  | 500 | 105 | 382 |
| SemEval-2026 | `Tagalog_Philippines` | [[Philippines]] | Southeast Asia | 500 | 105 | 373 |
| SemEval-2026 | `Tamil_Singapore` | [[Singapore]] | Southeast Asia | 500 | 105 | 375 |
| SemEval-2026 | `Tamil_SriLanka` | [[Sri Lanka]] | South Asia | 500 | 105 | 235 |

**Priority regions:** Middle East — [[Iran]], [[Saudi Arabia]], [[Egypt]] (105 food questions each); Caucasus —
[[Azerbaijan]]; South Asia — [[India]] (Assam only), [[Sri Lanka]] (Tamil); East Asia — [[China]], [[Japan]],
[[South Korea]], [[North Korea]], [[Taiwan]]; Southeast Asia — [[Indonesia]] (2 files), [[Singapore]] (3 files),
[[Philippines]]. **Not covered:** UAE, Qatar, Kuwait, Bahrain, Oman, Kazakhstan, Uzbekistan, Tajikistan,
Kyrgyzstan, Turkmenistan, Pakistan, Bangladesh.

## Ingredients, amounts, cooking method
Not a recipe dataset: `has_ingredients: false`. But several food templates ask directly for culture-level
ingredient habits, useful for Q2:
- "What is the most common spice/herb used in dishes from X?" — Iran: turmeric 4, saffron 3, cinnamon 2;
  Saudi Arabia: cinnamon 2, turmeric, bay leaves, red pepper; China: cumin 2, star anise 2; Sri Lanka (Tamil):
  curry leaves 2, chilli powder.
- "What oil is usually used for cooking in X?", "What seasoning is indispensable…?", "What cooking utensil…?".
- Other food templates: breakfast, school-cafeteria food, snacks for kids, delivery food, festival food, most
  popular fruit/vegetable, morning drink, meal times (HH:MM). Saudi Arabia snack for nursery kids: cornflakes 5,
  toast 2, eggs 2.
- Amounts, cooking steps, nutrition: none.

## Linking to other datasets
- Answer strings are dish/food/spice names in English and local script; they can be matched to dish names in
  [[WorldCuisines]] / [[FmLAMA]] and to ingredient names in ingredient/compound resources (string matching only;
  no ids).
- Question `ID` aligns the same question across all 33 cultures, making cross-culture comparison trivial.

## Versions
- 2024-06: 16 cultures, 13 languages, 52.6k QA pairs (paper). 2024-12: translation fixes. 2025-05: MCQ file v1.1.
- **2026-09-15 (latest, used here):** SemEval-2026 Task 7 data — 17 new language-culture pairs (Arabic: Egypt,
  Morocco, Saudi Arabia; Basque; Bulgarian; English: Australia; French; Irish; Japanese; Malay/Mandarin/Tamil:
  Singapore; Mandarin: Taiwan; Spanish: Ecuador; Swedish; Tagalog: Philippines; Tamil: Sri Lanka), plus a
  `semeval` MCQ split. The repo also moved from `nayeon212/BLEnD` to `uilab/BLEnD`.

## Caveats
- ~5 annotators per culture (sometimes from one locality); answers are majority opinions, not measured consumption.
- Sub-national cultures (Assam, West Java, Northern Nigeria, Basque Country) should not be read as national profiles.
- Some templates are culturally odd for some places ("popular food to go with beer in Saudi Arabia" has no
  answers).
