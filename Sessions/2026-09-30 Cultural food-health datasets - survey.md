---
title: "Session 2026-09-30: cultural-food-health - dataset survey"
date: 2026-09-30
session: dataset-survey
topics: [cultural-food-health]
questions: [Q1, Q2, Q3]
tags:
  - type/session
  - q/1
  - q/2
  - q/3
---
# Session 2026-09-30: cultural-food-health (dataset survey)

> [!question] Questions addressed in this session
> - [[Q1 Cultural food datasets|Q1]]: Which datasets describe the foods and dishes of different cultures, and do they give ingredients, amounts and cooking methods?
> - [[Q2 Cultural ingredient datasets|Q2]]: Which datasets describe the ingredients used by different cultures, and can their effect on the human body be inferred?
> - [[Q3 Food compound & health-effect datasets|Q3]]: Which datasets link foods and ingredients to compounds, and compounds to effects on the body?

**Research question:** what data can augment an agent for culturally tuned medical advice and analysis with knowledge of
what different cultures eat, which ingredients they use, and what those do to the body. The project is by Artur Pak
(MBZUAI NLP, supervised by Fajri Koto). Priority regions: Middle East/GCC, Central Asia, South & East Asia.

**Corpus / scope:**
- **Search:** 4 parallel search strands (food, ingredients, compounds, priority regions), run on 2026-09-30, produced
  **143 candidates** in [[Backlog]].
- **Processing:** **43 datasets** were processed into `Datasets/`. For each, access was tried for real, data downloaded
  to `Data/<slug>/`, and every table profiled (`schema.md`, `sample.csv`). There are 36 light paper notes.
- **Geography:** country and region notes cover 224 countries and 12 regions.
- **Vault changes:** new note types for datasets, countries and regions; `Datasets.base`; `_tools/profile_dataset.py`;
  `_tools/build_geo.py`; dataset checks in `check_vault.py`.

> [!important] Main takeaways
> 1. **Access is better than expected.** 29 of 43 datasets were fully downloaded and 13 partially (web-only databases
>    sampled politely, huge files subset). Only [[NII Cookpad Dataset]] could not be touched at all. Nine datasets
>    needed the user: see [[Access requests]]. FooDB and HMDB are resolved by browser download; email drafts for the
>    rest are in `Access-help/`.
> 2. **The best priority-region food data comes from government composition tables, not ML datasets.**
>    - [[Saudi Food Composition Tables]]: 130 dishes with gram amounts, numbered steps, 49 lab analytes and the
>      region of origin.
>    - [[Kyrgyzstan Food Composition Table]]: 11 national dishes.
>    - [[Bahrain Food Composition Tables]]: 82 dishes, but only 27 are Bahrain's own lab analyses.
>
>    ML-style datasets give breadth rather than depth: [[WorldCuisines]] and [[FmLAMA]] have a few dishes per Gulf state,
>    and [[ArabCulture]] has 53–59 food items per Arab country.
> 3. **India, China and Japan are rich, with open recipe corpora plus traditional-medicine databases.**
>    - India: [[IndicRecipeNutri]] (219k recipes, gram weights), [[IMPPAT]] 3.0, [[GRAYU]].
>    - China: [[XiaChuFang Recipe Corpus]] (1.52M recipes), [[HERB]], [[SymMap]], [[TM-MC]].
>    - Japan: [[Our Regional Cuisines (Japan MAFF)]] and the [[Standard Tables of Food Composition in Japan]].
>
>    **Central Asia and the smaller GCC states (UAE, Qatar, Oman, Kuwait) are the weakest.** They have dish images,
>    portion sizes, one 11-dish composition table, and no Emirati dish composition data.
> 4. **The compound → effect layer is global and must be joined.** The chain runs
>    [[FooDB]]/[[Phenol-Explorer]] (food → compound) → [[CTD]] (curated chemical → disease) / [[HMDB]] /
>    [[Exposome-Explorer]] (human biomarkers), with [[DDID]] for graded food–drug safety. Join on PubChem CID or InChIKey
>    (see [[Q3 Food compound & health-effect datasets#How to chain food → ingredient → compound → effect]]).
>    FooDB lacks regional staples: nigella, sumac, camel milk, za'atar, ghee, labneh.
> 5. **Licences constrain the agent design.**
>    - [[GRAYU]]'s terms forbid providing medical advice, so it can only be used for offline research.
>    - [[NII Cookpad Dataset]] forbids external LLM services.
>    - [[IMPPAT]] and [[KNApSAcK Family]] are CC BY-NC-ND.
>    - [[CTD]] requires notification.
>    - [[World Wide Dishes]] forbids prompt-template generation.
>
>    Full list: [[Q3 Food compound & health-effect datasets#Licences & usage constraints]].

## Q1: foods & dishes → [[Q1 Cultural food datasets]]
- Recipes with amounts and steps:
  - [[IndicRecipeNutri]]: India, state labels
  - [[XiaChuFang Recipe Corpus]]: China
  - [[Our Regional Cuisines (Japan MAFF)]]: Japan, 47 prefectures
  - [[Food.com Recipes and Interactions]]: 69 countries via tags, US-biased
  - [[RecipeDB2]]: 99 countries; needs an email for bulk access
- Composition tables that include dishes (Gulf and Central Asia): Saudi, Bahrain, Kyrgyzstan.
- Culture knowledge bases and benchmarks: [[WorldCuisines]], [[FmLAMA]], [[World Wide Dishes]], [[BLEnD]], [[ArabCulture]].

## Q2: ingredients → [[Q2 Cultural ingredient datasets]]
- National composition tables: [[Korean Food Composition Table]], [[Standard Tables of Food Composition in Japan]],
  [[USDA FoodData Central]] and the Gulf/Kyrgyz tables. For all of these, the effect on the body is *linkable*, not direct.
- One traditional-medicine database per system:
  - Ayurveda, Siddha, Unani: [[IMPPAT]]
  - TCM: [[HERB]] and [[SymMap]]
  - Northeast Asia: [[TM-MC]]
  - Persian: [[UNaProd]]
  - Jamu, and an edible-vs-medicinal flag per country: [[KNApSAcK Family]]
- Bridges across cultures: [[CMAUP]] and [[Dr. Duke's Phytochemical and Ethnobotanical Databases]].
- Spices: [[SpiceRx]], [[FlavorDB2]].

## Q3: compounds & effects → [[Q3 Food compound & health-effect datasets]]
- Food → compound: [[FooDB]] (5.1M content rows, 64% predicted), [[Phenol-Explorer]], [[NPASS]] and [[FoodAtlas]]
  (needs an API key).
- Compound → disease or target: [[CTD]] (109,665 curated chemical–disease rows), [[HMDB]] and [[Exposome-Explorer]].
- Food–drug interactions: [[DDID]] (23,950 graded rows), [[FooDrugs]] and [[DrugBank]] (blocked).

## Most important datasets to read first
| Why | Dataset |
|---|---|
| Best Gulf dish data (ingredients, amounts, steps, nutrients, regions) | [[Saudi Food Composition Tables]] |
| Largest open culture-labelled recipe corpus with amounts | [[IndicRecipeNutri]] |
| Dish → country map for 186 countries | [[WorldCuisines]] |
| Everyday food customs per Arab country, native-written | [[ArabCulture]] |
| Food → compound backbone with health effects | [[FooDB]] |
| Curated compound → disease | [[CTD]] |
| Graded food/herb–drug safety | [[DDID]] |
| Traditional medicine with clinical-trial evidence | [[HERB]] |
| Persian food-as-medicine (Mizaj) | [[UNaProd]] |

## Verification
- `python3 _tools/check_vault.py` reports no problems (36 paper, 43 dataset, 224 country, 12 region, 143 candidate
  notes).
- Spot-checked numbers against `Data/*/schema.md`:
  - Saudi FCT: 130 dishes, 1,154 ingredient lines, 6,370 nutrient values ✅
  - IMPPAT: 4,154 plant rows (4,133 unique ids, so ~21 duplicates) and 18,314 phytochemicals ✅
  - Kyrgyz FCT: 11 dishes, 162 recipe lines, 41 foods (its proximates table has 40 rows) ✅
  - ArabCulture: 724 food items ✅
- Known data problems, recorded in the dataset notes:
  - FooDB: `Compound.csv` header is misaligned; 343k content rows point to compound ids that don't exist.
  - Bahrain: borrowed values.
  - XiaChuFang: only a 4.3% head subset was downloaded.

## Open gaps / next steps
1. **Send the access requests** in `Access-help/`: RecipeDB2 (+FlavorDB2/SpiceRx), GRAYU, the FoodAtlas API key,
   the NII Cookpad inquiry, the Central Asian Atlas permission, and a DrugBank account.
2. **Decide on full crawls** of web-only relation layers. These are needed for a knowledge graph but go beyond polite
   sampling:
   - [[SymMap]] (~4.2k requests) and [[HERB]] (~6.9k) relations
   - [[UNaProd]] (3,413 monographs)
   - [[CMAUP]] plant pages ("used in medicines by country")
   - [[NPASS]] composition
   - [[FlavorDB2]] and [[SpiceRx]]
   - [[KNApSAcK Family]] World (~190 countries)
3. **Process the priority-1 candidates left in the Backlog:**
   - [[China Medicine-Food Homology List]]: the food flag for TCM databases
   - [[China Health and Nutrition Survey (CHNS)]] and [[KNHANES]]: diet linked to health outcomes
   - [[Indian Food Composition Tables (IFCT 2017)]] (site down)
   - [[EMFID (Eastern Mediterranean Food Information Data Bank)]] and [[Lebanon traditional dishes composition]]
   - [[Wikidata dishes]]
4. **Fill the Gulf gap:** the UAE nutrient dataset (contact authors), [[Arabic myfood24 FCDB]], and Kuwaiti dish tables.
5. **Build the join layer:** done on branch `unified-db`, as the [[Unified database]] (dish ↔ ingredient ↔ compound ↔
   condition, DuckDB), with traces in [[Traces - dish to symptom]] and [[Traces - symptom to dish]].

## Datasets in this topic
![[Datasets.base#All datasets]]

## Backlog for this topic
![[Backlog.base#This topic]]
