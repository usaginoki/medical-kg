---
title: "LLM tagging after the rule screens: experiments and costs"
topics: [cultural-food-health, kg-medical-eval]
questions: [Q2, Q3, Q4, Q5, Q7]
updated: 2026-10-14
tags:
  - type/database
  - q/2
  - q/3
  - q/4
  - q/5
  - q/7
---
# LLM tagging after the rule screens: experiments and costs

> [!abstract] What it is
> The [[Unified database]] and the patient-case table ([[Export tables]]) were built with cheap keyword and rule filters.
> On 2026-10-14 those filters were audited and fixed (part A). The fixed filters now act as a **preliminary screen**.
> Five LLM workflows with structured output were then tested as the stricter step that runs after the screen (part B).
> - **Models:** Gemini 3.5 / 3.1 / 2.5 Flash-Lite and Gemma 4 (26B-A4B, 31B), all through `GOOGLE_API_KEY`.
> - **Scoring:** each workflow was scored against a hand-labelled reference sample. Every item that two or more
>   models answered differently from the reference was then re-checked by hand, and the scores below use the
>   reviewed labels (see *Review of the reference labels*).
> - **Recall of the screen:** a separate sample of 500 cases the screen rejects or ranks low was checked for missed
>   cues (see *False negatives of the case screen*).
> - **Spend:** the experiments cost about **$1.50** in total.
> - **Status:** experiments only. Nothing the LLMs produced is written into the exports yet.
>
> Code is in `db/llm/` (see `db/README.md`). Samples, reference labels, runs and the response cache are in
> `.cache/llm/`, which is git-ignored.

> [!tip] Recommendation
> | Workflow | Screen → LLM hand-off | Model | Main gain over the rules | Full run (standard / Batch) |
> |---|---|---|---|---|
> | W1 case cultural tags | strong / weak cue, diet or negated hit, or culture by construction (21,063 cases without MedArabiQ) | Gemini 3.1 Flash-Lite, 0-shot, no thinking | "does culture matter for the answer" F1 0.44 → 0.91; graph-answerable F1 0.63 → 0.95 | $8.2 / $4.1 |
> | W1b answer leak | same cases (or all gold cases) | Gemini 3.1 Flash-Lite, a separate narrow prompt | leak F1 0.19 (inside W1) → 0.68 | ≈ $4 / $2 |
> | W2 case facts | same cases | Gemini 3.1 Flash-Lite | food list F1 0.79; age 0.98; links cases to graph ids (≈ 80% of foods, 65% of diagnoses resolve) | $18 / $9 |
> | W3 ingredient lines | unmatched + `substring` / `fuzzy` lines (34,388 distinct) | Gemini 3.1 Flash-Lite, retrieve-then-choose | line → id accuracy 0.67 → 0.85; not-an-ingredient F1 0.92 | $6.6 / $3.3 |
> | W4 condition terms | terms the resolver leaves unmatched (3,672 distinct) | Gemini 3.5 Flash-Lite, generate-then-ground | resolver + LLM for its misses: F1 0.77 → 0.90 | $1.1 / $0.6 |
> | W5 dish check | dishes without a country, Food.com fusion candidates (or all 46,253) | Gemini 3.5 Flash-Lite | cuisine country accuracy 0.74 → 0.99 (0.20 → 0.96 where none was stored) | ≤ $11 / $5.6 |
>
> Running everything costs about **$50 at standard prices, or $25 with the Batch API**. Gemma 4 is free but limited
> to a few requests at a time (about 16–22 s per item with 3 workers). It suits small overnight jobs, not 20k-item runs.

## Part A: fixes to the cheap filters (the screen)
Every fix has a regression script in `db/checks/`, and all three pass on the rebuilt database: cues 50/50, ingredients
92/92, conditions 85/85. The database before the fixes is kept as `.cache/baseline/unified.duckdb` for comparison.

### Patient-case cues (`db/cues.py`, `db/cases.py`)
**False positives found**
- Negated mentions counted as cues: 112 of 127 "recent travel" hits read "denied recent travel"; RuMedBench has the template line "Выезд за пределы … отрицает".
- Medical terms that contain a cue word: India ink, Japanese (B) encephalitis, MERS, the FISH test, TACO, `diet\w*` matching diethylcarbamazine, "fasting glucose".
- Russian body-part and organ words: "молочных желез" (mammary glands), "пищевод" (oesophagus).
- Chinese template lines: 否认食物过敏史, 发病节气, 久居本地, the COVID 旅居史 line, and 中医望闻切诊 headers.
- Bare tongue and pulse findings (舌, 脉) counted as traditional medicine.
- Word-boundary errors: the Kazakh ет ("meat") matched inside қажет, and "Пловец" (swimmer) matched as plov.
- Arabic matching required a whole word, so forms with an attached prefix were missed (للطعام, بالأعشاب).

**Fixes**
- A stoplist of these medical terms and template lines is blanked out before matching.
- Negation is checked before the match in the same clause and in a denial after it, with lists for EN, RU, KK, ZH, AR and FA. A negated match sets no flag and is listed in `cues_negated`.
- Every match is now kept in `cue_hits`, not only the first.
- `cue_strength` separates **weak** cues (race words, bare country, city or nationality names) from **strong** ones.
- Lexicon additions: Middle Eastern, Mediterranean, Cajun and other groups; more countries and cities; travel and residence phrases; prayer and festivals; Russian foreign travel; more cuisine dishes.
- `relevance()` now needs a strong cue for *high*.
- `dup_group` marks the MedArabiQ ×3 and ISSAI ×5 copies of the same item.

**Effect on the case table** (including the recall fixes below)
- MedCaseReasoning *high* cases: 361 → 122.
- *High* cases overall: 1,902 → 1,700.
- RuMedBench place cues stay at 0.4%, now with the template line negated.

### False negatives of the case screen
**The question:** which cases does the screen drop that should count as relevant? The 143-case reference sample has
only about 20 rejected cases, too few to measure recall.

**The check**
- **Sample:** 500 cases drawn from two groups.
  - Cases the screen **rejects** outright, with no cue, no diet word, no negated hit and no culture by construction: 250 of the 10,711 MedCaseReasoning cases, 120 of the 5,572 RuMedBench cases and 50 of the 655 MedicationQA cases.
  - 80 of the 2,371 MedCaseReasoning cases with **only weak cues** (race or nationality words), which can never reach *high*.
- **Model pass:** two models (3.1 and 3.5 Flash-Lite, $0.40) tagged every case with W1, and I reviewed every case either one flagged.
- **Unflagged cases:** because the models themselves miss about 15% of "culture matters" cases, I also read a random set of unflagged ones. That covered 20 RuMedBench and MedicationQA cases in full, plus all 246 unflagged MedCaseReasoning cases, using a word scan for exposure, origin, food and remedy words.

| Group | Real misses | Est. in population | What was missed |
|---|---|---|---|
| rejected MedCaseReasoning | 2 / 250 (0.8%) | ≈ 85 | a named herbal drug ("Tripterygium glycosides"); "a 78-year-old **Swiss-born** woman" with *M. bovis* infection |
| rejected RuMedBench | 6 / 120 (5%) | ≈ 280 | sweets ("отказался от сладкого", "употребляет много сладкого"), infant feeding ("введение прикорма"), Lent fasting ("во время поста"), supplements named by brand (Холекальциферол, Аквадетрим, Сорбифер) |
| rejected MedicationQA | 1 / 50 (2%) | ≈ 13 | minerals asked about ("what does magnesium do to your body") |
| weak cues only, MedCaseReasoning | 5 / 80 (6%) | ≈ 150 | origin that does matter (see below) |

**What the models flagged but I did not count**
- **Generic alcohol and smoking** are left out by the definitions.
- **Parental consanguinity** is not a cue type. Should it be one? It is culturally patterned and decisive for recessive diseases.
- **Model errors:** the Sinopharm vaccine taken as traditional medicine, marijuana taken as a cultural habit, and rivaroxaban painkillers.

**Fixes to the screen**
- **English:** "Swiss" and the pattern "X-born" are added.
- **Herbal products:** a list of herbal products named in case reports (Tripterygium, ginkgo, St John's wort, kava, ephedra, comfrey, black cohosh, garcinia, senna…).
- **Minerals:** counted only as supplements ("taking magnesium", "zinc tablets") or in consumer questions. In case reports, "magnesium" mostly sits in lab lists.
- **Russian:** sweets, starchy, fried and smoked food, drinks, infant feeding (прикорм, вскармливание), vitamin D and iron brands, omega-3, probiotics and fasting phrases.
- **Russian negation:** "не менее" ("no less than") no longer negates the match that follows. It had hidden "не менее даже во время поста" (no less even during Lent).

The fixes moved 156 RuMedBench cases, 82 MedCaseReasoning cases and 8 MedicationQA cases out of "rejected". A sample of
the new hits showed only supplement or diet mentions.

**Weak cues are mostly incidental, but not always**
- In 5 of 80 weak-only cases the origin supports the diagnosis:
  - Thai → nasopharyngeal carcinoma;
  - African American → sarcoidosis;
  - East Timor → urogenital tuberculosis;
  - Kurdish / Iraqi / Yemenite ancestry → Behçet disease;
  - Middle Eastern, first-cousin parents → factor V deficiency.
- Keywords cannot tell these from "a 71-year-old Caucasian man". The rules rank them *low* or *medium*, and W1 picks them out.
- So the proposed hand-off passes weak-cue cases to the LLM instead of dropping them.

### Ingredients and dishes (`db/build/ingredients.py`, `resolve_ingredients.py`, `dishes.py`)
**Fixes to the curated map and matching**
- One-word rows of the manual map (meat → stock, ginger → garlic, "lamb or" → beef) only match a whole leftover line now, never as aliases.
- ING:gram is split into chana dal and urad dal.
- CJK matching: the longest match wins and generic heads (肉, 里脊) rank last. 牛肉片, 羊肉片 and 鸭肉 no longer become pork.
- Fuzzy matching now needs a score of at least 92, the same first three letters, and a food-source alias. Known false pairs (marsala/masala, leaves/leaven) are blocked.
- Bad inherited aliases and CulinaryDB entity ids are overridden when a text match disagrees: jalapeño → bell pepper (97 lines), kaffir lime → Bantu beer (96), oyster sauce → clam (161) and paprika → bell pepper (861 → 29) are all fixed.

**Fixes to line parsing**
- Website junk and section headers are dropped: 2,545 lines, which carried 75.6 kg of invented grams.
- The weight tier is a column now, not text appended to the line.
- Chinese spoon units are added, and `maps/piece_weights.csv` gives grams per piece (11,114 more lines have grams).
- Lines that list several ingredients are split into one row per ingredient.

**Effect**
- Exact matches 187k → 210k; unmatched lines 10,492 → 8,538.
- Guesses from part of the text now have their own `substring` label (69k lines), so they can be reviewed.
- Lines with grams: XiaChuFang 21% → 42%, CulinaryDB 53% → 60%.

### Conditions, compounds and links (`resolve_conditions.py`, `resolve_compounds.py`, `links_*.py`)
- **Alias ranking:** when an alias names several conditions, the ranking now looks at who wrote it (curated > MEDIC > SymMap > HERB…) and puts MeSH D before MeSH C. Exposome cancers now map to the neoplasm descriptors, not "familial" variants, and Duke "Sore" maps to Skin Ulcer.
- **Acronyms:** acronyms are case-sensitive, so PTSD and IBS no longer hit rare syndromes.
- **Lay and organ words:** these words from HERB and SymMap no longer match (tongue → Tongue Neoplasms, heat → Thermal Energy).
- **Fuzzy matches:** a fuzzy match must agree on numbers, sex and acute/chronic.
- **Splitting labels:** labels with several conditions are split, so HERB trial conditions resolved go from 20/42 to 32/42.
- **Action map:** 21 rows added.
- **New evidence type `in_vitro`:** used for Dr. Duke's chemical activities. FooDB health effects copied from Duke are now merged with them instead of counting as a second source, and `effects` shrinks from 6.08M to 5.47M rows.
- **Animal models and source terms:** links to animal-model conditions are flagged, and `compound_condition.note` keeps the source term.
- **Compound names:** class words (RESIN, SUGARS) no longer resolve to one molecule.

The full row counts are in `db/build_report.md`, and `git diff` of it shows the before and after.

## Part B: LLM workflows
### Shared setup
- **Client:** one async client (`db/llm/client.py`).
  - **Structured output:** `response_schema` with a pydantic model. All five models accepted it, including Gemma 4, and 100% of the Gemini outputs were valid.
  - **Workers:** 24 parallel workers for Gemini and 3 for Gemma.
  - **Retries:** tenacity retries on 429 and 5xx errors.
  - **Cache:** a SQLite response cache, so re-runs are free.
  - **Spend cap:** a hard cap, `LLM_MAX_USD`.
- **Prices:** USD per 1M input / output tokens, from ai.google.dev on 2026-10-14. The Batch API is half price.

  | Model | Input | Output |
  |---|---|---|
  | Gemini 3.5 Flash-Lite | 0.30 | 2.50 |
  | Gemini 3.1 Flash-Lite | 0.25 | 1.50 |
  | Gemini 2.5 Flash-Lite | 0.10 | 0.40 |
  | Gemma 4 | free | free |

- **Reference labels:** written by Claude subagents that followed the same definitions as the prompts. They are not human expert labels (see *Caveats*).

### W1: cultural tags of a case (`w1_case_tags.py`)
- **Input:** the case, its conclusion and the keyword hits.
- **Output:**
  - `cues[]`, each with type, exact text, negated, and `about` (patient / family / other / name of a test or disease / template field);
  - `culture_role`: none, incidental, supportive or decisive for the conclusion;
  - `diet_relevant`, `graph_answerable` and `answer_leak`.
- **Reference:** 143 cases stratified by dataset and screen outcome (MedArabiQ left out, see *Caveats*).

Scores against the reviewed reference labels. The values before the review are in brackets. "Origin" counts
place and ethnicity as one cue type, because nationality words ("a Japanese man") fit both definitions.

| Run | "Culture matters" F1 (P / R) | Role accuracy | Cue-type F1 (origin merged) | Diet F1 | Graph-answerable F1 | Leak F1 | $ / 1k | s / item |
|---|---|---|---|---|---|---|---|---|
| keyword screen | 0.44 (0.38 / 0.52) [0.47] | 0.55 | 0.86 (0.87) | 0.85 | 0.63 | 0 | 0 | 0 |
| **3.1 Flash-Lite, 0-shot** | **0.91** (0.97 / 0.86) [0.87] | **0.87** | 0.85 (0.93) | 0.92 | **0.95** | 0.19 | 0.47 | 1.9 |
| 3.1 Flash-Lite, 0-shot, thinking low | 0.85 [0.81] | 0.84 | 0.86 (0.92) | 0.92 | 0.94 | 0.30 | 0.65 | 2.2 |
| 3.1 Flash-Lite, 1-shot | 0.82 [0.79] | 0.83 | 0.82 (0.89) | 0.89 | 0.89 | 0.42 | 0.61 | 2.0 |
| 3.5 Flash-Lite, 0-shot | 0.73 [0.69] | 0.78 | 0.86 (0.87) | **0.93** | **0.96** | 0.30 | 0.61 | 2.0 |
| 3.5 Flash-Lite, 0-shot, thinking low | 0.75 [0.72] | 0.82 | 0.90 (0.90) | 0.87 | 0.95 | 0.21 | 0.59 | 1.7 |
| 2.5 Flash-Lite, 0-shot | 0.68 [0.64] | 0.68 | 0.68 (0.69) | 0.82 | 0.65 | 0 | 0.22 | 2.2 |
| Gemma 4 31B, 0-shot (141 valid) | 0.72 [0.69] | 0.80 | **0.93 (0.94)** | 0.93 | 0.84 | 0.46 | free | 22 |
| Gemma 4 26B-A4B, 0-shot (121 valid) | 0.62 [0.62] | 0.67 | 0.69 (0.71) | 0.90 | 0.74 | 0 | free | 54 |

**What the table shows**
- **What the LLM adds:** the keyword screen already finds cue *types* well (F1 0.83). The LLM's value is judging whether a cue matters for the answer, and whether food knowledge could help.
- **Few-shot and thinking:** neither helped. Differences of ±0.05 are within noise at n = 143.
- **Where 3.1 still errs, after the review:** its misses are cases where the cue needs regional medical knowledge:
  - Surinamese descent → histoplasmosis;
  - river fish in Tomsk → opisthorchiasis as a cause of biliary disease;
  - Central Asian diet plans in the ISSAI profiles, judged incidental.

### W1b: answer leakage (`w1b_leak.py`)
- **Why a separate prompt:** inside W1 the small models almost never set `answer_leak`.
- **The prompt:** quote the evidence first, then choose explicit, partial or none.
- **Results:**
  - 3.1 Flash-Lite, counting "explicit" only: P 0.62, R 0.76, F1 **0.68**, at $0.21 per 1k.
  - 3.5 Flash-Lite: F1 0.64.
  - 2.5 Flash-Lite: F1 0.50.
  - Counting "partial" as a leak catches every leak (R 1.0) but has low precision (0.40).
- **General lesson:** split a hard field into its own narrow prompt instead of adding it to a large schema.

### W2: structured facts of a case (`w2_case_facts.py`)
- **Output:**
  - age and sex;
  - country and city;
  - ethnicity and religious practices;
  - symptoms and history;
  - the conclusion's diagnosis in English;
  - foods, dishes, drinks, herbs and supplements, each with a negated flag;
  - drugs.
- **Reference:** 64 cases.

| Model | Age | Sex | Country | Foods P / R / F1 | Symptoms F1 | Diagnosis ≈ reference | $ / 1k |
|---|---|---|---|---|---|---|---|
| **3.1 Flash-Lite** | **0.98** | 0.84 | 0.77 | **0.80 / 0.78 / 0.79** | 0.64 | 0.69 | 0.76 |
| 3.5 Flash-Lite | 0.97 | 0.83 | **0.89** | 0.60 / 0.85 / 0.70 | 0.64 | 0.70 | 1.30 |
| 2.5 Flash-Lite | 0.95 | 0.86 | 0.77 | 0.41 / 0.78 / 0.54 | 0.61 | 0.66 | 0.30 |
| Gemma 4 31B (63/64 valid) | 0.98 | **0.92** | 0.67 | 0.71 / 0.87 / 0.79 | 0.64 | **0.71** | free |

**Linking to the graph.** This is the step [[Export tables]] calls the next step for the case table. The extracted
names were run through the build's own resolvers.

| Names | Share that resolves |
|---|---|
| Foods → ingredient ids | about 81–85% |
| Diagnoses → condition ids | about 61–65% (the reference labels themselves reach 62%) |
| Symptoms → condition ids | about 65% |

**Gaps this exposes**
- **Dishes:** Central Asian dishes (manti, samsa, shashlik, baklava) are not ingredients and need a lookup in the `dish` table.
- **A wrong alias:** "halva" resolves to fenugreek.
- **TCM diagnoses:** TCM syndromes have no MeSH condition.
- **Next step:** resolve case foods against both `ingredient` and `dish`, and add TCM / Ayurveda concept nodes.

### W3: ingredient line → ingredient id (`w3_ingredient_lines.py`)
- **Method:** retrieve-then-choose. rapidfuzz proposes 8 candidates (for CJK lines, aliases contained in the line come first). The model picks one or NONE, gives the kind of line, and names the ingredient in English. That English name is then resolved exactly as a fallback.
- **Reference:** 150 distinct lines (60 unmatched, 70 `substring`, 20 `fuzzy`).

| Run | Line → id accuracy | On food lines | Wrong ids on food lines | Not-food F1 | Unmatched recovered | `substring` correct | $ / 1k |
|---|---|---|---|---|---|---|---|
| rule matcher | 0.67 [0.65] | 0.62 | 11 | n/a | 0.37 | 0.84 | 0 |
| **3.1 Flash-Lite** | **0.85** [0.81] | **0.84** | 4 | **0.92** | **0.72** | **0.93** | 0.19 |
| 3.5 Flash-Lite | 0.80 [0.77] | 0.78 | 4 | 0.90 | 0.65 | 0.87 | 0.25 |
| 2.5 Flash-Lite | 0.79 [0.76] | 0.77 | 5 | 0.79 | 0.68 | 0.83 | 0.07 |

- **Limit on accuracy:** retrieval. For 17 of 150 lines the right id was not among the candidates (三文鱼 → salmon, 红苋菜 → amaranth, 蛋挞皮 → tart shell).
- **Other errors:** the rest are literal readings (干辣面, chili flakes, read as noodles; loobikka read as dried lime).
- **Better retrieval:** embedding-based retrieval, or a second "name it in English, then look it up" round, would raise the ceiling.

### W4: source term → conditions (`w4_condition_terms.py`)
- **Method:** generate-then-ground. The model names the conditions in MeSH-style English, and `ConditionResolver` maps the names to ids, so the model never makes up an id. It also returns the kind of term (condition / symptom / pharmacological action / organ use / property / TCM–Ayurveda concept) and an evidence level.
- **Population:** 5,641 distinct terms from Duke ETHNOBOT, Duke AGGREGAC and IMPPAT. 3,672 of them (41k rows) stay unmatched after the rule fixes.
- **Reference:** 150 terms (80 unmatched, 70 matched).

| Run | Ids P / R / F1 | Unmatched terms recovered | Agrees on matched terms | Kind accuracy | Evidence accuracy | $ / 1k |
|---|---|---|---|---|---|---|
| rule resolver | 0.96 / 0.64 / 0.77 | 0 / 36 | 66 / 70 | n/a | n/a | 0 |
| 3.5 Flash-Lite | 0.90 / 0.86 / 0.88 | 25 / 36 | 65 / 70 | 0.82 | 0.95 | 0.31 |
| 3.1 Flash-Lite | 0.77 / 0.91 / 0.83 | 29 / 36 | 65 / 70 | 0.87 | 0.94 | 0.24 |
| **resolver, then 3.5 for its misses** | **0.91 / 0.89 / 0.90** | 25 / 36 | 66 / 70 | n/a | n/a | 0.31 on misses only |

- **Why the hybrid:** the resolver is precise, and the LLM fills in what it cannot match lexically:
  - Sternutatory → Sneezing;
  - Gunshot → Wounds, Gunshot.
- **Grounding misses:** a proposed name that no alias knows stays unmatched (Natriuretic → "Natriuresis").
- **What the LLM's `kind` adds:** it separates properties (Tonic, Antioxidant, Pesticide) that should stay unlinked from real indications.

### W5: dish record check (`w5_dish_check.py`)
- **Output:** is it a dish; a clean English name; the cuisine's country; and traditional, adapted, fusion or international.
- **Reference:** 80 dishes (Food.com, CulinaryDB without a country, XiaChuFang, IndicRecipeNutri, MAFF).

| Run | Kind | Cuisine country | …where none was stored (25) | Style | Fusion / international F1 | $ / 1k |
|---|---|---|---|---|---|---|
| stored value | n/a | 0.74 | 0.20 | n/a | n/a | 0 |
| **3.5 Flash-Lite** | 0.96 | **0.99** | **0.96** | 0.68 | 0.43 | 0.24 |
| 3.1 Flash-Lite | 1.00 | 0.96 | 0.88 | 0.69 | 0.43 | 0.17 |
| 2.5 Flash-Lite | 0.98 | 0.94 | 0.84 | 0.65 | 0.20 | 0.06 |

The "style" judgement (traditional vs adapted) is subjective, and the labeller marked 32 of 80 as low-confidence.
Treat it as a soft tag.

## Review of the reference labels
**What was reviewed:** every item where two or more models disagreed with the reference. The list is written by
`uv run db/llm/disagree.py`, and I re-read each case in full. That came to:
- W1: 91 field-level disputes on 58 cases;
- W3: 33 lines;
- W4: 26 terms, compared by resolved condition ids, since names differ while ids may not;
- W5: 6 dishes.

**How verdicts are applied:** they are stored in `.cache/llm/refs/w*_review.json`, and the scorers apply them. A label
judged wrong is corrected; an ambiguous item either accepts both answers (W3–W5) or is left out of that one field
(W1).

| Workflow | Disputed | Reference right (models wrong) | Reference wrong | Ambiguous under the definitions |
|---|---|---|---|---|
| W1 | 91 items / 58 cases | 60 | 9 | 15, plus 7 that only differ in place vs ethnicity for a nationality word |
| W3 | 33 | 26 | 0 | 7 |
| W4 | 26 | 17 | 1 | 8 |
| W5 | 6 | 2 | 0 | 4 |

**Reference errors corrected (W1)**
- **Culture over-credited:**
  - "Caucasian" in giant cell arteritis;
  - Turkish origin in AA amyloidosis, where the case gives untreated periodontitis as the cause;
  - an allergy to herbal drugs in pollen rhinitis.
- **`graph_answerable` labelled true although the answer is a diagnosis code that food knowledge cannot inform:** T2DM E11.2; noninfective colitis after a negative parasite work-up.
- **Admission boilerplate taken as TCM use:** "为求进一步中西医结合诊疗" was tagged as traditional medicine in two TCM records.
- **Ginkgo tablets for hypertension:** counted as diet-relevant to 尿浊.
- **A festival date as a religion cue:** "中秋节后" was tagged although the same phrase was not tagged in a similar case.

**Reference errors corrected (W4)**
- Natriuretic should map to Edema / Hypertension, as the action map does for diuretics.

**Where the reference held and the models were wrong.** These are useful failure types to know about:
- **Product names read as foods or cuisines:** "Natural Green Tea" mouthwash, Dijon mustard.
- **Negated or boilerplate cues counted:** "denied recent travel".
- **Regional medicine missed:** river fish in Tomsk → opisthorchiasis.
- **Literal translations in W3:** 干辣面 read as noodles.
- **Retrieval misses in W3:** the right id was not among the candidates.
- **Over-broad W4 terms:** Favus → Tinea capitis instead of *Tinea favosa*; "spermatocidal agents" → infertility.

**Definition gaps to settle**
- Is alcohol, or a food-triggered symptom ("pain after fatty food"), diet content?
- Is a nationality word a place or an ethnicity cue? Scoring the two as one "origin" type removes most of that noise.
- Should consanguinity be a cue type?
- Is herbal tea a drink or traditional medicine?
- Which of two ingredients on one line counts as the "main" one?
- **Vocabulary duplicate:** ING:jowar and ING:sorghum are the same grain.

**Effect on the scores:** the review raised every model's scores by about 0.02–0.05, and the ranking of models did not
change. The rule baselines barely moved: W1's "culture matters" F1 even dropped from 0.47 to 0.44. So the gap between
the rules and the LLM step is larger than first reported.

## Proposed pipeline
```
rule screen (db/cues.py, resolvers)          LLM step (db/llm/)                          stored as
───────────────────────────────────          ─────────────────                           ─────────
case: strong/weak cue, diet, negated,   →    W1 tags + W1b leak + W2 facts         →    case_llm_tags, case_facts
      (weak-cue cases included: ~6% matter)
      culture by construction                (3.1 Flash-Lite, Batch)                    (+ links via resolvers)
dish line: unmatched / substring / fuzzy →   W3 choose among candidates            →    ingredient_map_llm.csv (reviewed)
condition term: unmatched               →    W4 generate-then-ground (3.5 FL)      →    condition_synonyms_llm.csv
dish: no country / fusion tags          →    W5 dish check (3.5 FL)                →    dish_llm (country, style, name_en)
```
- **Write as reviewable map files:** W3 and W4 output could go into versioned map files, so the deterministic build reads them like the current curated maps. A person spot-checks the low-confidence rows.
- **Write as separate tables:** case and dish tags would go into sidecar tables keyed by id, carrying model and prompt version.

## Caveats
- **Reference labels:**
  - Claude subagents wrote them, following the same written definitions as the prompts, and noted their low-confidence items.
  - They are neither human expert labels nor multi-annotator labels, so agreement with them is an upper bound on precision against a human.
  - The second pass (the review above) was also done by Claude, by me, and it saw the models' answers. So it only checks the disputed items. Items where the reference and every model agree but are wrong would not be found.
  - Splits between close classes such as supportive vs incidental are noisy.
  - In W4, the reference names were chosen so that they ground with the same resolver.
- **Sample sizes:** 64–150 items per workflow. Differences under about 0.05 are not meaningful.
- **MedArabiQ:** it was left out of every API call because its licence allows internal research only. Decide whether sending it to the Gemini API is acceptable before running W1 or W2 on it.
- **Gemma 4:**
  - It is free with no paid tier. The free tier allowed about 3 parallel requests at 16–50 s each.
  - Gemma 4 26B-A4B returned 121 of 143 W1 items and is clearly weaker than the 31B model.
  - Gemma 4 31B's 1-shot run is partial (102 of 143).
- **Cost estimates:** they extrapolate the sample's tokens per item, per dataset for the case workflows, and use 2026-10-14 prices. Gemini 3.8 / 3.6 Flash prices double on 2027-01-01; the Flash-Lite prices have no announced change.

Related: [[Q7 Cultural cues in evaluation datasets]] · [[Q4 Patient case-conclusion datasets]] ·
[[Q5 Evaluating KG-augmented medical LLMs]] · [[Unified database]] · [[Export tables]]
