---
title: "FAM-Bench"
slug: fam-bench
kind: [case]
version: "v1.0, anonymous GitHub repo @ abfaf02 (2026-06-08)"
previous_versions: ""
papers: ["[[Mao2026 - FAM-Bench food-as-medicine benchmark]]"]
url: "https://github.com/anonymous-research-artifact123/Food-as-medicine"
license: "README: code/ MIT (LICENSE-CODE), dataset/ + knowledge_base/ + figures/ CC BY 4.0 (LICENSE-DATA); neither licence file is in the repo"
availability: open-download
access_link: "https://github.com/anonymous-research-artifact123/Food-as-medicine"
accessed: true
access_method: [github]
access_date: 2026-10-07
access_notes: "git clone --depth 1 of the anonymous review repo (commit abfaf02 'v1.0', 2026-06-08) worked: both task files (1,500 + 1,000 items), knowledge base and Task 2 rule files, evaluation code. Snapshot kept in Data/fam-bench/ because the anonymous repo will be de-anonymised (moved) after review. Not included in the repo: dish images (only third-party image_url links; cached images 'not redistributed'), LICENSE-CODE / LICENSE-DATA files, figures/."
countries: ["[[United States]]"]
regions: ["[[North America]]"]
n_records: "2,500 items (1,500 dish × condition + 1,000 four-dish rankings) from 3,859 recipes"
size: "40 MB (dataset/ 39 MB)"
formats: [json]
has_ingredients: true
has_amounts: "yes"
has_cooking_method: steps
has_nutrition: true
join_keys: [canonical ingredient names (English), condition names (13), recipe URL, recipe_id]
case_type: [diet]
conclusion_type: [suitability, ranking, advice]
languages: [en]
n_cases: "2,500 (1,500 suitability + 1,000 ranking items)"
diet_relevance: central
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/global-cases, search/evaluation]
tags:
  - type/dataset
  - kind/case
  - q/4
  - case/diet
  - region/americas
  - access/accessed
  - access/open
---
# FAM-Bench

> [!abstract] TL;DR
> FAM-Bench (Mao et al., Univ. of South Florida + Copenhagen, arXiv May 2026, under double-blind review) is an
> English **food-as-medicine** benchmark: 2,500 nutrition-expert-verified items over **13 diet-related conditions**
> (cardiometabolic, GI, liver, kidney, bone). Task 1 (1,500): one dish (image URL + ingredient list + recipe +
> nutrition table) × one condition → `recommend` / `not recommend` + the ingredients that justify it. Task 2 (1,000):
> 1–3 conditions + 4 dishes → full ranking with per-dish labels and clinical-risk costs. The "case" is a diet
> scenario, not a patient record. It ships its own **condition → beneficial/limit/avoid food knowledge base**; injecting
> it raises Task 1 accuracy by 2.0–3.3 points (4.7 with CoT+KI for GPT-5.4 and Gemma). Recipes are US-heavy (mostly US health-portal recipes), with no
> cuisine labels in the released data.

## Access
| | |
|---|---|
| Availability | open-download (anonymous GitHub for review; README says CC BY 4.0 data / MIT code) |
| Link | https://github.com/anonymous-research-artifact123/Food-as-medicine |
| Accessed? | yes (all text data; images only as third-party URLs) |
| How | `git clone --depth 1` (commit `abfaf02`, 2026-06-08) — snapshot taken now because the repo will move after review |
| Downloaded | `Data/fam-bench/dataset/task1_dish_suitability.json` (8 MB), `dataset/task2_comparative_analysis.json` (32 MB), `knowledge_base/disease_food_kb.json`, `code/task2/ki_data/{condition_rules,nutrition_guidelines}.json`, code (`code/task1`, `code/task2`), README; `.git` dropped |

## Tables & columns
Meanings from the README, the paper (§3, Appendix D–G) and the files; "(inferred)" where we read it off the data.

### `dataset/task1_dish_suitability.json` (1,500 items; one JSON list)
| column | type | meaning | example |
|---|---|---|---|
| `title`, `url` | str | recipe title and source page (54 domains; 1,382 distinct URLs) | `Butternut squash casserole`, bbcgoodfood.com |
| `image_url` | str | third-party dish image, fetched live in vision modes | images.immediate.co.uk/… |
| `meal_type` | list (34 rows: plain str, 90 null) | source meal/course tags | `["dinner"]` |
| `dietary_tags` | list | source tags, e.g. gluten-free, low sodium, vegetarian, diabetes-friendly, **Coumadin-safe** (209 rows carry a Coumadin tag) | `["vegetarian"]` |
| `servings`, `serving_size` | int, str | portions | `4`, `1 serving (about 1/4 of recipe)` |
| `ingredients` | list[str] | ingredient lines with amounts | `225 g sweet potato, cubed` |
| `instructions` | list[str] | preparation steps | `In a large pan, heat the olive oil…` |
| `nutrition` | dict (22 keys) | published per-serving nutrition: calories, total/saturated/trans/poly/mono fat, cholesterol, sodium, carbohydrate, fibre, sugars, added sugars, protein, K, Ca, Fe, Mg, P, vitamins A, C, D, K (many null) | `{"sodium": "185 mg", …}` |
| `notes` | str | source editorial notes (1,363 non-null; culinarymedicine.org notes include allergen and "Coumadin® (warfarin): safe" lines) | |
| `recommended_for` | list[{`condition`, `ingredients`}] | the dish's full annotation a(d): conditions it suits, with canonical ingredients that drive it | `{"condition": "hypertension", "ingredients": ["squash","tomato","bulgur"]}` |
| `not_recommended_for` | list[{`condition`, `ingredients`}] | conditions it conflicts with | `{"condition": "ibs", "ingredients": ["onion","garlic"]}` |
| `question` | str | the prompt (46 phrasings) | `Is this dish suitable for someone managing IBS?` |
| `standard answer.decision` | str | **gold label**: `recommend` (775) / `not recommend` (725) | `not recommend` |
| `standard answer.rationale_ingredients` | list[{`condition`, `ingredients`, `reasoning`}] | gold rationale: ingredients (mean 2.5) + one-sentence reason | `onion, garlic` — "common fermentable triggers…" |
| `standard answer.difficulty` | str | easy 37 / medium 1,037 / hard 426 | `medium` |
| `standard answer.is_counterintuitive` | bool | label goes against a naive reading (380 true) (inferred) | `false` |
| `q2_v3_provenance` | dict | annotation provenance: `model` (gpt-5.5 for all 1,500), `focal_conditions` (1 condition in 1,116 items, 2 in 384), `rule_llm_conflict_count`, `fallback_ingredient_fills`, `references` (guideline URLs, e.g. NIDDK, NHS) | |

The profiler flattens this file to 124 columns (`nutrition.*`, `standard answer.*`, `q2_v3_provenance.*`).

### `dataset/task2_comparative_analysis.json` (`metadata` dict + 1,000 `questions`)
| column | meaning |
|---|---|
| `question_id` | `crmcq_001` … `crmcq_1000` |
| `question_type` / `_label` | `health_condition_discrimination` 450, `ranking_among_clinically_eligible` 300, `ingredient_coverage_discrimination` 200, `combined_constraint_discrimination` 50 |
| `prompt` | `conditions` (1–3, e.g. `hypertension + type 2 diabetes`), `condition_labels`, `available_ingredients` (2–4 that the dish must use), `age_group` (`14-18` in all 1,000), `meal` (all null), `question_text` |
| `options[]` (4) | `letter`, `recipe_id`, `title`, `url`, `image_url`, `key_ingredients`, `full_ingredients` (≤25 lines), `matched_ingredient_lines`, `nutrition` (kcal, fibre, saturated fat, sodium, sugar), `app_scores` (`health_score` 0–1, guideline hits), `failure_mode` / `option_role` (valid, condition_violation, ingredient_miss, …), `gold` (`decision_label`, `clinical_risk` {avoid_terms, avoid_violation, false_recommend_cost 0/5, risk_level, risk_reasons}, `rationale_targets` {condition_attribution_targets: (condition, term, beneficial/limit/avoid, source)}), `validation`, `cached_image_*` (paths not shipped) |
| `answer` | `letter`, `recipe_id`, `title`, `selection_basis` |
| `gold` | `ranking` (e.g. B > D > C > A), `top_choice`, `decision_labels` per option, `avoid_list_violations`, `false_recommend_costs`, `metrics_supported` (12: top-1, MRR, Kendall τ, inversion rate, false-recommend rate, clinical-risk score, avoid-violation@k, ingredient-in-recipe rate, condition-attribution accuracy, …) |
| `answer_policy`, `distractor_policy`, `task_bundle`, `validation`, `task_type` | generation policies and checks (strings) |
| `metadata` | 47 keys: generator, seed, source recipe index (4,329 recipes after dedup of 5,717), answer letters balanced 250 each, condition-count distribution, … |

### `knowledge_base/disease_food_kb.json` (27 conditions; Task 1 knowledge injection)
`conditions.<name>` → `recommend` / `not_recommend` food lists, `sources` (Mayo Clinic "disease foods" and a
condition-rules sheet: `beneficial`, `limit_as_not_recommend`, `avoid_as_not_recommend`, `references`), counts. Covers
e.g. cardiovascular disease, hypertension, T2D, stroke, obesity, metabolic syndrome, cholesterol, bone health
osteoporosis, gout, cancers, allergies, celiac. The profiler sees only the 5 top-level keys.

### `code/task2/ki_data/condition_rules.json` (63 conditions) and `nutrition_guidelines.json` (90 rules)
Task 2 knowledge: per condition `beneficial` / `limit` / `avoid` foods and concepts (e.g. CVD: avoid cold cuts, cured
meats, pizza…; limit butter, cheese, red meat, soda), `references`, `guideline_aliases`; and nutrient targets
(`condition`, `population`, `nutrient`, `target_type` min/max, `min`, `max`, `unit`, `basis`, `source_url`, e.g. sodium
≤ 2,300 mg/day, Dietary Guidelines for Americans).

Sample: `Data/fam-bench/sample.csv` (Task 1) + `sample_*.csv` · full profile: `Data/fam-bench/schema.md`

## Countries & cultures covered
No country or cuisine field in the released data. The paper's Figure 3 ("recipe counts by country", basis not
stated; the bars sum to 4,864 > 3,859 recipes): [[United States]] 2,748, Mexico 597, Italy 417, India 283, United
Kingdom 269, China 214, Other 187, France 136, Canada 81, Morocco 67, Tunisia 65. Sources are 74.6% health-information
portals (Task 1 URLs: mds.culinarymedicine.org 601, recipes.heart.org 196, diabetesfoodhub.org 185, …) and 26.3% food
publications (bbcgoodfood.com 126, eatingwell.com 82, …). Dietary rules come from US guidelines (AHA, NIH, Harvard,
American Liver Foundation, Mayo Clinic). The authors call the corpus "U.S.-heavy". Only `countries: [[United States]]`
is recorded here.

## Cases & conclusions
**One case** (Task 1, first item):
> *Dish:* Butternut squash casserole (BBC Good Food) — olive oil, onion, garlic, cumin, paprika, sweet potato, red
> pepper, butternut squash, canned tomatoes, red wine, vegetable stock, bulgur, Greek yogurt, cheddar; 313 kcal,
> 185 mg sodium per serving. *Question:* "Is this dish suitable for someone managing IBS?"
> *Gold:* **not recommend**; rationale ingredients **onion, garlic** — "Onion and garlic are common fermentable triggers
> that may worsen IBS symptoms." (difficulty medium). The same dish is annotated `recommended_for` hypertension,
> T2D, stroke etc. and `not_recommended_for` GERD (tomato, wine, onion, garlic) and CKD.

**Gold and how it is made.** GPT-5.5 proposes the per-condition annotation, a rule check against the knowledge base
(ingredient concepts, nutrient-threshold vetoes, fallbacks) drops conflicts, and nutrition experts confirm or correct
every (condition, ingredients) entry (paper §3.3).

**Scoring.** Task 1: decision accuracy; rationale macro-/micro-F1 between cited and gold ingredients. Task 2: top-1
accuracy, MRR, cross-task consistency (does the ranking respect the model's own Task 1 labels). Best published:
Task 1 82.8% (Gemini 2.5 Pro + KI), rationale macro-F1 only 0.26 (GPT-5.4 CoT+KI); Task 2 top-1 29–42%.

**Food, diet, herbs, food–drug.** Diet is the whole dataset: 2,500 / 2,500 items (**diet_relevance: central**). No
herbs or traditional medicine. Food–drug keywords (`coumadin`, `warfarin`, `grapefruit`, `medication`, `drug`,
`interact`, `maoi`, `tyramine`, `statin`, `anticoagul`, `blood thinner`; case-insensitive; `vitamin k` excluded because
every row has a `vitamin K` nutrition key) hit **246 Task 1 items and 16 Task 2 items**, all in recipe metadata
(`dietary_tags` "Coumadin-safe", culinarymedicine.org notes "Coumadin® (warfarin): safe") and **0 in any gold answer**:
none of the 13 conditions is a drug interaction.

## Linking to the vault's knowledge graph
- **Ingredients → unified DB `ingredient`**: the 183 distinct canonical rationale terms in `recommended_for` /
  `not_recommended_for` match `ingredient_alias` (en, via `norm_text`) for 150 terms = **86% of 44,555 mentions**; the
  rest are nutrient descriptors (low sodium, no salt, fat free yogurt, whole grain). Raw `ingredients` lines can go
  through `IngredientResolver.by_text`.
- **Conditions → condition table / MeSH**: 11 of the 13 condition strings hit `condition_alias` (en), usually several
  ids each (ICD-11 + MeSH), so a curated 13-row map is needed; "high ldl cholesterol hyperlipidemia" and "obesity
  weight management" need rewriting first (Hyperlipidemias, Obesity).
- **KG test design:** our dish → ingredient → compound → condition paths (and [[FooDrugs]] / [[DDID]] for the
  Coumadin items) can be injected in place of their `disease_food_kb.json` (KI mode) and compared with it; their
  `condition_rules.json` / `nutrition_guidelines.json` are themselves guideline-grade ingredient → condition rules
  that could be loaded into the KG.
- **KI gap we found:** re-implementing the released Task 1 reference selection (`_select_reference_conditions`, exact
  alias match on the question text; we did not run their code) gives **514 / 1,500 items with no KB entry** — IBS,
  GERD, CKD, heart failure and NAFLD questions get no injected knowledge. A KG covering those conditions is an easy
  win to test.
- Related candidates: [[NGQA]] (food-healthiness graph QA), [[NutriBench]].

## Versions
One release: anonymous repo v1.0 (2026-06-08) for the arXiv v1 paper (2026-05-29). The README says it will be
de-anonymised upon acceptance, so the URL will change; our snapshot is commit `abfaf02`. Task 2 `metadata` records a
cache repair (17 questions regenerated because images were unreachable) and a later `full_ingredients` enrichment.

## Caveats
- **Licence:** README table — `code/` "MIT (`LICENSE-CODE`)"; `dataset/`, `knowledge_base/`, `figures/` "CC BY 4.0
  (`LICENSE-DATA`)" — but the licence files are missing and the GitHub API reports no licence. Recipe text, ingredient
  lists, notes and image URLs are copied from third-party sites (BBC Good Food, AHA, EatingWell, …) whose terms CC BY
  cannot override; our `sample.csv` contains 50 such recipes.
- **LLM-made labels:** GPT-5.5 proposed every annotation before rule checks and expert review; using GPT-family models
  as test-takers is circular to some degree.
- **Images:** vision runs fetch third-party URLs live; links rot, so image results drift. Recipe text carries most of
  the signal (text-only ≈ text+image in the paper's ablation).
- Task 2 prompts all say age group 14–18 and give no meal; `meal_type` is sometimes a plain string.
- Binary suitability ignores portion size and medication; one condition at a time in Task 1 (two focal conditions in
  384 items).
- US-centric terminology and guidelines; no cuisine label to select regional dishes.
