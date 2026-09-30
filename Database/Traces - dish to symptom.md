---
title: "Traces: dish → symptom"
topics: [cultural-food-health]
questions: [Q1, Q2, Q3]
updated: 2026-09-30
tags:
  - type/database
  - q/1
  - q/2
  - q/3
---
# Traces: dish → symptom

Real traces from the [[Unified database]] (build of 2026-09-30), produced by `db/trace.py`. For each one there is a
short reading, the exact command, and the full output (expand the callout).

**How to read a trace**
- **Ingredients**: the dish's lines as matched, with grams.
- **May help / May aggravate / Associated**: conditions reached through *characteristic* paths only. Columns:
  - `sources`: the number of independent sources behind the strongest single ingredient;
  - `characteristic ingredients`: how many of the dish's ingredients support it.
- **Strongest characteristic paths**: hop by hop, *ingredient → compound (mg/100 g) → condition*, with every source
  and PMID.
- **Lab-measured nutrients**: shown only when the dish is above the UK FSA "high" threshold.
- **Food–drug interactions**: from [[DDID]].

Evidence grades: clinical > curated > epidemiological > traditional > text-mined > predicted (see
[[Unified database#Evidence grading and direction]]).

## 1. Timman Rice (Saudi Arabia, Hail) with a warfarin check
`uv run db/trace.py dish "Timman Rice" --country SA --top 6 --drug warfarin`

**Ingredients.** [[Saudi Food Composition Tables]] dish `sfct:68`: lamb, rice, vegetables, ghee, cumin (10 g),
turmeric (5 g), dried black lime (7 g) and black pepper (2 g). All 20 lines are matched, all with grams.

**What the paths show.** The broad "may help" conditions (inflammation, pain, edema, diabetes) are carried by the
spices:
- turmeric → **curcumin 2,507 mg/100 g** ([[FooDB]]; 2,214 in [[Phenol-Explorer]]) → [[CTD]] *therapeutic* for
  edema, inflammation, neoplasms and obesity, with PMIDs;
- black pepper → **piperine 5,350 mg/100 g** → CTD *therapeutic* for neoplasms;
- cumin → cuminaldehyde 1,000 mg/100 g → traditional antifungal claims (Duke).

**Harmful side.** These are traditional warnings from Duke's ethnopharmacology, attached to the same compounds:
piperine as abortifacient, and eucalyptol and β-pinene as allergens.

**Drug check.** For a patient on warfarin, DDID flags turmeric as a *Possible* interaction (PMID 34062109).

**Reading.** The dish's plausible health relevance comes from its **spice fraction** (about 30 g of 1.3 kg), not its
bulk. The trace makes that explicit and shows the dose: curcumin is about 2.5% of dried turmeric, so 5 g of turmeric
carries roughly 125 mg of curcumin.

> [!example]- Full output: Timman Rice
> ## Dish → conditions: Timman Rice
>
> `sfct:68` · SA · Hail · cuisine: Saudi · source: [[Saudi Food Composition Tables]]
>
> ### Ingredients
>
> | line | ingredient | g | match | score |
> |---|---|---|---|---|
> | Water | ING:water | 1500 | exact | 1 |
> | Lamb with bone, cut into medium pieces | ING:lamb | 350 | normalised | 0.7 |
> | Timman rice, washed and soaked | ING:rice | 300 | normalised | 0.75 |
> | Ground tomatoes | ING:tomato | 200 | normalised | 0.92 |
> | Eggplant, cut into large longitudinal pieces | ING:eggplant | 150 | normalised | 0.92 |
> | Whole zucchini | ING:zucchini | 100 | normalised | 0.9 |
> | Pumpkin, cut into medium cubes | ING:pumpkin | 100 | normalised | 0.92 |
> | Onion, finely chopped | ING:onion | 100 | normalised | 0.92 |
> | Rendered fat (waddak) | ING:tail-fat | 50 | manual | 0.95 |
> | Green chili pepper | ING:chili-pepper | 20 | normalised | 0.8 |
> | Tomato paste | ING:tomato-paste | 20 | exact | 1 |
> | Melted ghee (for garnish) | ING:ghee | 20 | normalised | 0.75 |
> | Mixed spices | ING:spice | 10 | normalised | 0.75 |
> | Ground cumin | ING:cumin | 10 | normalised | 0.92 |
> | Salt | ING:salt | 10 | exact | 1 |
> | Sarar Hail spice blend | ING:spice | 5 | normalised | 0.67 |
> | Ground turmeric | ING:turmeric | 5 | normalised | 0.92 |
> | Ground dried black lime | ING:dried-lime | 5 | normalised | 0.92 |
> | Ground black pepper | ING:black-pepper | 2 | normalised | 0.92 |
> | Ground dried black lime (for garnish) | ING:dried-lime | 2 | normalised | 0.92 |
>
> ### May help
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Neoplasms | disease | curated | 6 | 8 | ING:black-pepper, ING:tomato, ING:lamb, ING:cumin, ING:rice, ING:onion, ING:eggplant, ING:turmeric |  |
> | Inflammation | finding | curated | 5 | 8 | ING:onion, ING:rice, ING:cumin, ING:lamb, ING:tomato, ING:turmeric, ING:eggplant, ING:black-pepper |  |
> | Diabetes Mellitus | disease | curated | 5 | 7 | ING:turmeric, ING:eggplant, ING:lamb, ING:cumin, ING:rice, ING:onion, ING:black-pepper |  |
> | Edema | symptom | curated | 5 | 7 | ING:black-pepper, ING:onion, ING:turmeric, ING:eggplant, ING:lamb, ING:rice, ING:cumin |  |
> | Pain | symptom | curated | 5 | 7 | ING:onion, ING:lamb, ING:rice, ING:cumin, ING:turmeric, ING:eggplant, ING:black-pepper |  |
> | Fever | symptom | curated | 5 | 6 | ING:black-pepper, ING:eggplant, ING:turmeric, ING:onion, ING:cumin, ING:rice |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Diabetes Mellitus | turmeric | Potassium | 2416.03 | curated | [[CTD]], [[FooDB]] |  | 18981326 |  |
> | Diabetes Mellitus | cumin | Potassium | 1863.9 | curated | [[CTD]], [[FooDB]] |  | 18981326 |  |
> | Diabetes Mellitus | black-pepper | Potassium | 1259 | curated | [[CTD]], [[FooDB]] |  | 18981326 |  |
> | Edema | turmeric | Curcumin | 2507.01 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[Phenol-Explorer]] |  | 30138604\|19413659 |  |
> | Edema | turmeric | Demethoxycurcumin | 1982.5 | curated | [[CTD]], [[FooDB]] |  | 18449507 |  |
> | Edema | turmeric | demethoxycurcumin | 1982.5 | curated | [[CTD]], [[Phenol-Explorer]] |  | 18449507 |  |
> | Inflammation | turmeric | Curcumin | 2507.01 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[Phenol-Explorer]] |  | 34272803\|2062949\|19594223\|19413659\|18403 |  |
> | Inflammation | lamb | Methionine | 400 | curated | [[CTD]], [[FooDB]] |  | 25712622 |  |
> | Inflammation | onion | Ascorbic acid | 203.82 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 34089294 |  |
> | Neoplasms | black-pepper | Piperine | 5350 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  | 22542552 |  |
> | Neoplasms | turmeric | Curcumin | 2507.01 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[Phenol-Explorer]] |  | 21397623 |  |
> | Neoplasms | cumin | Calcium | 1086.03 | curated | [[CTD]], [[FooDB]] |  | 21443188 |  |
>
> ### May aggravate / harmful
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Infertility | disease | traditional | 3 | 4 | ING:black-pepper, ING:turmeric, ING:cumin, ING:rice |  |
> | Abortion, Spontaneous | disease | traditional | 3 | 3 | ING:cumin, ING:black-pepper, ING:onion |  |
> | Vomiting | symptom | traditional | 3 | 3 | ING:rice, ING:lamb, ING:turmeric |  |
> | Hypersensitivity | disease | traditional | 2 | 5 | ING:turmeric, ING:eggplant, ING:lamb, ING:cumin, ING:onion |  |
> | Chemical and Drug Induced Liver Injury | disease | traditional | 2 | 4 | ING:onion, ING:lamb, ING:cumin, ING:turmeric |  |
> | Cardiotoxicity | disease | traditional | 2 | 3 | ING:cumin, ING:black-pepper, ING:turmeric |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Abortion, Spontaneous | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
> | Abortion, Spontaneous | cumin | beta-Bisabolene | 21 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Abortion, Spontaneous | cumin | (direct) |  | traditional | [[IMPPAT]] | ayurveda |  | abortifacient agents |
> | Hypersensitivity | turmeric | Eucalyptol | 480.25 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Hypersensitivity | cumin | beta-Pinene | 332.4 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Hypersensitivity | turmeric | linalool | 160 | traditional | [[FooDB]] |  |  |  |
> | Infertility | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
> | Infertility | cumin | Kaempferol | 38.6 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[Phenol-Explorer]] |  |  |  |
> | Infertility | turmeric | p-coumaric acid | 34.5 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Vomiting | turmeric | Curcumenol | 2130 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Vomiting | lamb | Methionine | 400 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Vomiting | rice | Methionine | 153 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
>
> ### Associated (marker / mechanism)
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Colorectal Neoplasms | disease | curated | 2 | 7 | ING:onion, ING:turmeric, ING:chili-pepper, ING:black-pepper, ING:rice, ING:cumin, ING:lamb |  |
> | Alzheimer Disease | disease | curated | 2 | 6 | ING:onion, ING:black-pepper, ING:cumin, ING:lamb, ING:rice, ING:turmeric |  |
> | Schizophrenia | disease | curated | 2 | 6 | ING:turmeric, ING:black-pepper, ING:lamb, ING:rice, ING:cumin, ING:onion |  |
> | Non-alcoholic Fatty Liver Disease | disease | curated | 2 | 6 | ING:onion, ING:cumin, ING:lamb, ING:rice, ING:black-pepper, ING:turmeric |  |
> | Liver Cirrhosis | disease | curated | 2 | 6 | ING:onion, ING:turmeric, ING:black-pepper, ING:rice, ING:lamb, ING:cumin |  |
> | Diabetes Mellitus, Type 1 | disease | curated | 2 | 5 | ING:black-pepper, ING:cumin, ING:turmeric, ING:onion, ING:tomato |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Alzheimer Disease | cumin | Iron | 55.75 | curated | [[CTD]], [[FooDB]] |  | 26721301\|21423579\|18307039\|16640825\|1656 |  |
> | Alzheimer Disease | turmeric | Iron | 35.41 | curated | [[CTD]], [[FooDB]] |  | 26721301\|21423579\|18307039\|16640825\|1656 |  |
> | Alzheimer Disease | black-pepper | Iron | 25.1 | curated | [[CTD]], [[FooDB]] |  | 26721301\|21423579\|18307039\|16640825\|1656 |  |
> | Colorectal Neoplasms | black-pepper | Copper | 1.13 | curated | [[CTD]], [[FooDB]] |  | 37400750 |  |
> | Colorectal Neoplasms | cumin | Copper | 1.06 | curated | [[CTD]], [[FooDB]] |  | 37400750 |  |
> | Colorectal Neoplasms | turmeric | beta-D-Glucose | 28000 | epidemiological | [[FooDB]], [[HMDB]] |  | 28587349\|7482520\|21773981\|27107423\|23940 |  |
> | Non-alcoholic Fatty Liver Disease | lamb | Epicholesterol | 76500 | curated | [[CTD]], [[FooDB]] |  | 29486218 |  |
> | Non-alcoholic Fatty Liver Disease | onion | 3h-Sucrose | 11425 | curated | [[CTD]], [[FooDB]] |  | 40952780\|39746502\|33408299\|31175915\|2312 |  |
> | Non-alcoholic Fatty Liver Disease | onion | D-Fructose | 11410 | curated | [[CTD]], [[FooDB]] |  | 39967315\|32259528\|29416063\|40952780\|3799 |  |
> | Schizophrenia | lamb | Methionine | 400 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 22257447\|17440431\|2415198\|7711000\|238231 |  |
> | Schizophrenia | rice | Methionine | 153 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 22257447\|17440431\|2415198\|7711000\|238231 |  |
> | Schizophrenia | black-pepper | Copper | 1.13 | curated | [[CTD]], [[FooDB]] |  | 16842975 |  |
>
> ### Associated
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Hematoma, Subdural, Chronic | disease | clinical | 3 | 1 | ING:turmeric |  |
> | Breast Cancer, Familial | disease | clinical | 2 | 8 | ING:onion, ING:tomato, ING:eggplant, ING:turmeric, ING:cumin, ING:rice, ING:lamb, ING:black-pepper |  |
> | Pain | symptom | clinical | 2 | 7 | ING:turmeric, ING:eggplant, ING:tomato, ING:onion, ING:black-pepper, ING:cumin, ING:rice |  |
> | Schizophrenia | disease | clinical | 2 | 7 | ING:eggplant, ING:turmeric, ING:tomato, ING:onion, ING:black-pepper, ING:rice, ING:cumin |  |
> | Bipolar Disorder | disease | clinical | 2 | 7 | ING:black-pepper, ING:tomato, ING:onion, ING:cumin, ING:rice, ING:eggplant, ING:turmeric |  |
> | Kidney Failure, Chronic | disease | clinical | 2 | 6 | ING:cumin, ING:black-pepper, ING:eggplant, ING:turmeric, ING:tomato, ING:onion |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Breast Cancer, Familial | turmeric | (direct) |  | clinical | [[CMAUP]], [[HERB]] |  |  | NCT03980509 Breast Cancer |
> | Breast Cancer, Familial | onion | Ascorbic acid | 203.82 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Breast Cancer, Familial | lamb | Heptadecanoic acid | 133 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Hematoma, Subdural, Chronic | turmeric | (direct) |  | clinical | [[CMAUP]], [[HERB]], [[SymMap]] |  |  | Subdural Hematoma Chronic; By_MM_symptom; FDR(BH) 1.11374e-0 |
> | Pain | turmeric | (direct) |  | clinical | [[CMAUP]], [[HERB]] |  |  | Pain, unspecified; NCT04946981 |
> | Pain | eggplant | (direct) |  | predicted | [[CMAUP]] |  |  | Pain, unspecified; by target |
> | Pain | cumin | (direct) |  | predicted | [[CMAUP]] |  |  | Pain, unspecified; by target |
> | Schizophrenia | turmeric | (direct) |  | clinical | [[CMAUP]], [[SymMap]] |  |  | Schizophrenia; NCT02104752 |
> | Schizophrenia | rice | (direct) |  | predicted | [[CMAUP]] |  |  | Schizophrenia; by target |
> | Schizophrenia | tomato | (direct) |  | predicted | [[CMAUP]] |  |  | Schizophrenia; by target |
>
> ### Food–drug interactions with warfarin
>
> | ingredient | drug | effect | mechanism | PMIDs | source |
> |---|---|---|---|---|---|
> | turmeric | Warfarin | Possible |  | 34062109 | [[DDID]] |

## 2. Kothamalli thanni: coriander and ginger tea (India, Tamil Nadu)
`uv run db/trace.py dish "Coriander and ginger tea" --top 6`

**Ingredients.** [[IndicRecipeNutri]] `indicrecipenutri:15191`, a Tamil home remedy: coriander seeds (18.9 g), ginger
(15 g), palm sugar (12.6 g) and honey (7 g). All weights are tier A (high confidence).

**What the paths show.** The top conditions are **cough, common cold, pain, diarrhoea and edema**. Each is supported by
5 independent sources (CTD, Duke, FooDB, IMPPAT, SpiceRx) through ginger and coriander. For example:
- coriander → camphor 70 mg/100 g → CTD (cough, pain);
- coriander and ginger → traditional anti-cold/antitussive activities (Duke).

**Reading.** This matches what the recipe is traditionally used for. It also shows a limit: honey and palm sugar
add *diabetes* links through their sugars, via Duke/CTD mechanism claims. Direction and dose have to be read from the
hop table; the database does not collapse them into one verdict.

> [!example]- Full output: coriander and ginger tea
> ## Dish → conditions: Kothamalli thanni | Coriander and ginger tea
>
> `indicrecipenutri:15191` · IN · Tamil Nadu · cuisine: Indian · source: [[IndicRecipeNutri]]
>
> ### Ingredients
>
> | line | ingredient | g | match | score |
> |---|---|---|---|---|
> | coriander seeds [weight tier A] | ING:coriander | 18.9 | normalised | 0.95 |
> | ginger [weight tier A] | ING:ginger | 15 | manual | 1 |
> | palm sugar crystals [weight tier A] | ING:sugar | 12.6 | normalised | 0.7 |
> | honey [weight tier A] | ING:honey | 7.06 | exact | 1 |
> | lemon juice [weight tier A] | ING:lemon-juice | 5.04 | exact | 1 |
>
> ### May help
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Diabetes Mellitus | disease | curated | 5 | 3 | ING:honey, ING:ginger, ING:coriander |  |
> | Pain | symptom | curated | 5 | 3 | ING:coriander, ING:ginger, ING:honey |  |
> | Diarrhea | symptom | curated | 5 | 2 | ING:coriander, ING:ginger |  |
> | Inflammation | finding | curated | 5 | 2 | ING:coriander, ING:ginger |  |
> | Edema | symptom | curated | 5 | 2 | ING:ginger, ING:coriander |  |
> | Common Cold | disease | curated | 5 | 2 | ING:coriander, ING:ginger |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Diabetes Mellitus | coriander | Potassium | 1267 | curated | [[CTD]], [[FooDB]] |  | 18981326 |  |
> | Diabetes Mellitus | coriander | Nicotinic acid | 2.13 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 12200755 |  |
> | Diabetes Mellitus | honey | D-Fructose | 38800 | traditional | [[FooDB]] |  |  |  |
> | Diarrhea | ginger | Gingerol | 187.3 | curated | [[CTD]], [[FooDB]] |  | 28421826 |  |
> | Diarrhea | ginger | [6]-Gingerol | 187.3 | curated | [[CTD]], [[Phenol-Explorer]] |  | 28421826 |  |
> | Diarrhea | ginger | (direct) |  | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[IMPPAT]], [[SymMap]], [[UNaProd]] | tcm,folk,persian,ayurveda |  | diarrhea |
> | Inflammation | coriander | cis-Ferulic acid | 29 | curated | [[CTD]], [[FooDB]] |  | 18068289 |  |
> | Inflammation | ginger | caffeic acid | 15.5 | curated | [[CTD]], [[Phenol-Explorer]] |  | 22036979 |  |
> | Inflammation | coriander | Nicotinic acid | 2.13 | curated | [[CTD]], [[FooDB]] |  | 20167660\|19420110 |  |
> | Pain | honey | D-Mannose | 33900 | curated | [[CTD]], [[FooDB]] |  | 10481420 |  |
> | Pain | coriander | Camphor | 70 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 29655911 |  |
> | Pain | coriander | Nicotinic acid | 2.13 | curated | [[CTD]], [[FooDB]] |  | 21121498 |  |
>
> ### May aggravate / harmful
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Hypersensitivity | disease | traditional | 2 | 2 | ING:coriander, ING:ginger |  |
> | Infertility | disease | traditional | 2 | 2 | ING:coriander, ING:ginger |  |
> | Seizures | symptom | traditional | 2 | 2 | ING:ginger, ING:coriander |  |
> | Chemical and Drug Induced Liver Injury | disease | traditional | 2 | 1 | ING:coriander |  |
> | Spasm | symptom | traditional | 2 | 1 | ING:ginger |  |
> | Vomiting | symptom | traditional | 2 | 1 | ING:coriander |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Chemical and Drug Induced Liver Injury | coriander | Nicotinic acid | 2.13 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Hypersensitivity | coriander | linalool | 1048 | traditional | [[FooDB]] |  |  |  |
> | Hypersensitivity | ginger | citronellol | 325.1 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Hypersensitivity | ginger | Eucalyptol | 251.65 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Infertility | coriander | p-coumaric acid | 17.3 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Infertility | ginger | (direct) |  | traditional | [[IMPPAT]] | ayurveda |  | contraceptive agents |
> | Seizures | ginger | Eucalyptol | 251.65 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Seizures | coriander | Camphor | 70 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
>
> ### Associated (marker / mechanism)
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Prostatic Neoplasms | disease | curated | 2 | 2 | ING:coriander, ING:ginger |  |
> | Alcoholism | disease | curated | 2 | 1 | ING:coriander |  |
> | Non-alcoholic Fatty Liver Disease | disease | curated | 1 | 4 | ING:ginger, ING:coriander, ING:sugar, ING:honey |  |
> | Depressive Disorder | disease | curated | 1 | 4 | ING:ginger, ING:sugar, ING:honey, ING:coriander |  |
> | Hypertrophy | finding | curated | 1 | 4 | ING:sugar, ING:honey, ING:coriander, ING:ginger |  |
> | Insulin Resistance | disease | curated | 1 | 4 | ING:honey, ING:coriander, ING:ginger, ING:sugar |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Alcoholism | coriander | Calcium | 709 | curated | [[CTD]], [[FooDB]] |  | 27890540 |  |
> | Alcoholism | coriander | Nicotinic acid | 2.13 | epidemiological | [[FooDB]], [[HMDB]] |  | 3410397\|9717263\|2779169\|8723414\|16959481 |  |
> | Depressive Disorder | sugar | Sucrose | 97810 | curated | [[CTD]], [[FooDB]] |  | 30629985 |  |
> | Depressive Disorder | honey | Sucrose | 75100 | curated | [[CTD]], [[FooDB]] |  | 30629985 |  |
> | Depressive Disorder | ginger | Ethinyl Estradiol | 4270 | curated | [[CTD]], [[FooDB]] |  | 7750278\|10574641 |  |
> | Non-alcoholic Fatty Liver Disease | sugar | Sucrose | 97810 | curated | [[CTD]], [[FooDB]] |  | 21462320\|37992649\|31273855\|40952780\|3974 |  |
> | Non-alcoholic Fatty Liver Disease | sugar | 3h-Sucrose | 97095 | curated | [[CTD]], [[FooDB]] |  | 40952780\|39746502\|33408299\|31175915\|2312 |  |
> | Non-alcoholic Fatty Liver Disease | honey | Sucrose | 75100 | curated | [[CTD]], [[FooDB]] |  | 21462320\|37992649\|31273855\|40952780\|3974 |  |
> | Prostatic Neoplasms | ginger | Ethinyl Estradiol | 4270 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 8766519\|3779655\|3396013\|30387366\|2208075 |  |
> | Prostatic Neoplasms | coriander | Ethinyl Estradiol | 1200 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 8766519\|3779655\|3396013\|30387366\|2208075 |  |
>
> ### Associated
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Colonic Neoplasms | disease | clinical | 2 | 2 | ING:coriander, ING:ginger |  |
> | Migraine Disorders | disease | clinical | 2 | 2 | ING:ginger, ING:coriander |  |
> | Asthma | disease | clinical | 2 | 2 | ING:coriander, ING:ginger |  |
> | Diabetes Mellitus, Type 2 | disease | clinical | 2 | 2 | ING:ginger, ING:coriander |  |
> | Motion Sickness | symptom | clinical | 2 | 1 | ING:ginger |  |
> | Hypercholesterolemia | disease | traditional | 2 | 2 | ING:honey, ING:sugar |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Asthma | ginger | (direct) |  | clinical | [[CMAUP]], [[SymMap]] |  |  | Asthma; NCT03705832 |
> | Asthma | coriander | (direct) |  | predicted | [[CMAUP]] |  |  | Asthma; by target |
> | Colonic Neoplasms | ginger | (direct) |  | clinical | [[CMAUP]], [[SymMap]] |  |  | Colorectal cancer; NCT03268655 |
> | Colonic Neoplasms | coriander | (direct) |  | predicted | [[CMAUP]] |  |  | Colon cancer; by target; Colorectal cancer; by target |
> | Diabetes Mellitus, Type 2 | ginger | (direct) |  | clinical | [[CMAUP]], [[SymMap]] |  |  | Type 2 diabetes mellitus; NCT02666807,NCT02289235 |
> | Diabetes Mellitus, Type 2 | coriander | (direct) |  | predicted | [[CMAUP]] |  |  | Type 2 diabetes mellitus; by target |
> | Migraine Disorders | ginger | (direct) |  | clinical | [[CMAUP]], [[SymMap]] |  |  | Migraine; NCT02568644,NCT02570633 |
> | Migraine Disorders | coriander | (direct) |  | predicted | [[CMAUP]] |  |  | Migraine; by target |
>
> ### Food–drug interactions (harmful / negative)
>
> | ingredient | drug | effect | mechanism | PMIDs | source |
> |---|---|---|---|---|---|
> | ginger | Crizotinib | Harmful | CYP3A4; CYP2C9; P‐gp | 30701569 | [[DDID]] |
> | ginger | Dabigatran | Harmful | P-gp | 31508385 | [[DDID]] |
> | honey | Phenytoin | Harmful | Pyridoxal-phosphate dependent enzyme | 55569 | [[DDID]] |
> | honey | Warfarin | Harmful |  | 16553520 | [[DDID]] |
> | coriander | Midazolam | Negative | CYP3A5 | 21680781 | [[DDID]] |
> | ginger | Midazolam | Negative | CYP3A5 | 21680781 | [[DDID]] |
> | ginger | Clevidipine | Negative |  | 28892755 | [[DDID]] |
> | honey | Warfarin | Negative |  | 3541503 | [[DDID]] |
> | honey | Levodopa | Negative |  | 34200493 | [[DDID]] |

## 3. Chicken Kabsa (Saudi Arabia, Al-Baha): lab-measured sodium
`uv run db/trace.py dish "Chicken Kabsa" --country SA --top 6`

**The nutrient.** The Saudi table's lab analysis gives **666 mg sodium per 100 g**, above the FSA "high" threshold of
600 mg. So this dish carries a *measured* nutrient path: dish → sodium (MeSH D012964) → [[CTD]] curated links
including **hypertension** (marker/mechanism, 4 PMIDs), kidney diseases and metabolic syndrome.

**Drug check.** DDID flags a *Harmful* interaction between chicken and spironolactone (PMID 31816944).

**Reading.** This is the one path in the database built on **lab measurements of the whole cooked dish**, not
ingredient estimates. The Gulf composition tables are the only sources that allow it (Saudi Arabia 130 dishes,
Bahrain 82, Kyrgyzstan 11, INDB 1,014). 5 Saudi dishes are above the sodium threshold, led by Matboukhah from Tabuk (730 mg).

> [!example]- Full output: Chicken Kabsa
> ## Dish → conditions: Chicken Kabsa
>
> `sfct:96` · SA · Al-Baha · cuisine: Saudi · source: [[Saudi Food Composition Tables]]
>
> Other matches: `foodcom:190220` chicken kabsah
>
> ### Ingredients
>
> | line | ingredient | g | match | score |
> |---|---|---|---|---|
> | Water | ING:water | 1500 | exact | 1 |
> | Chicken, cut into medium pieces | ING:chicken | 667 | normalised | 0.92 |
> | Short-grain rice, washed | ING:rice | 600 | normalised | 0.7 |
> | Tomato, chopped | ING:tomato | 213 | normalised | 0.92 |
> | Onion, chopped | ING:onion | 93 | normalised | 0.92 |
> | Fat (tail fat), chopped | ING:tail-fat | 80 | manual | 0.95 |
> | Salt | ING:salt | 36 | exact | 1 |
> | Ground black pepper | ING:black-pepper | 5 | normalised | 0.92 |
>
> ### May help
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Pain | symptom | curated | 5 | 4 | ING:onion, ING:rice, ING:black-pepper, ING:chicken |  |
> | Diabetes Mellitus | disease | curated | 5 | 4 | ING:onion, ING:rice, ING:black-pepper, ING:chicken |  |
> | Fever | symptom | curated | 5 | 3 | ING:black-pepper, ING:onion, ING:rice |  |
> | Hypercholesterolemia | disease | curated | 4 | 5 | ING:chicken, ING:tomato, ING:black-pepper, ING:onion, ING:rice |  |
> | Neoplasms | disease | curated | 4 | 5 | ING:black-pepper, ING:onion, ING:chicken, ING:rice, ING:tomato |  |
> | Inflammation | finding | curated | 4 | 5 | ING:chicken, ING:black-pepper, ING:rice, ING:onion, ING:tomato |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Diabetes Mellitus | black-pepper | Potassium | 1259 | curated | [[CTD]], [[FooDB]] |  | 18981326 |  |
> | Diabetes Mellitus | chicken | Nicotinic acid | 8.62 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 12200755 |  |
> | Diabetes Mellitus | onion | Nicotinic acid | 4.32 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 12200755 |  |
> | Fever | onion | beta-D-Glucose | 13030 | curated | [[CTD]], [[FooDB]] |  | 15615417 |  |
> | Fever | black-pepper | Piperine | 5350 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  | 22542552 |  |
> | Fever | onion | Ascorbic acid | 203.82 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Hypercholesterolemia | chicken | Nicotinic acid | 8.62 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 8593127\|8124850\|3680913\|3174043\|12788145 |  |
> | Hypercholesterolemia | onion | Nicotinic acid | 4.32 | curated | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | 8593127\|8124850\|3680913\|3174043\|12788145 |  |
> | Hypercholesterolemia | rice | Lignin | 15015 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Pain | chicken | Nicotinic acid | 8.62 | curated | [[CTD]], [[FooDB]] |  | 21121498 |  |
> | Pain | onion | Nicotinic acid | 4.32 | curated | [[CTD]], [[FooDB]] |  | 21121498 |  |
> | Pain | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
>
> ### May aggravate / harmful
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Infertility | disease | traditional | 2 | 2 | ING:black-pepper, ING:rice |  |
> | Vomiting | symptom | traditional | 2 | 2 | ING:rice, ING:chicken |  |
> | Hypertension | disease | traditional | 2 | 2 | ING:black-pepper, ING:salt |  |
> | Abortion, Spontaneous | disease | traditional | 2 | 2 | ING:onion, ING:black-pepper |  |
> | Chemical and Drug Induced Liver Injury | disease | traditional | 2 | 2 | ING:chicken, ING:onion |  |
> | Hypersensitivity | disease | traditional | 2 | 2 | ING:chicken, ING:onion |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Abortion, Spontaneous | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
> | Abortion, Spontaneous | black-pepper | (direct) |  | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] | folk |  | Abortifacient (Malaya) |
> | Abortion, Spontaneous | onion | (direct) |  | traditional | [[IMPPAT]] | ayurveda |  | abortifacient agents |
> | Hypertension | salt | Sodium | 38700 | traditional | [[FooDB]] |  |  |  |
> | Hypertension | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
> | Infertility | black-pepper | Piperine | 5350 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[NPASS]] |  |  |  |
> | Infertility | black-pepper | Copper | 1.13 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Infertility | rice | (direct) |  | traditional | [[IMPPAT]] | ayurveda |  | contraceptive agents |
> | Vomiting | chicken | Methionine | 495 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
> | Vomiting | rice | Methionine | 153 | traditional | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  |  |  |
>
> ### Associated (marker / mechanism)
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Colorectal Neoplasms | disease | curated | 2 | 4 | ING:onion, ING:black-pepper, ING:chicken, ING:rice |  |
> | Alzheimer Disease | disease | curated | 2 | 4 | ING:onion, ING:black-pepper, ING:chicken, ING:rice |  |
> | Schizophrenia | disease | curated | 2 | 4 | ING:chicken, ING:onion, ING:black-pepper, ING:rice |  |
> | Liver Cirrhosis | disease | curated | 2 | 4 | ING:black-pepper, ING:onion, ING:chicken, ING:rice |  |
> | Gout | disease | curated | 2 | 3 | ING:black-pepper, ING:onion, ING:chicken |  |
> | Epilepsy | disease | curated | 2 | 3 | ING:black-pepper, ING:chicken, ING:rice |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Alzheimer Disease | black-pepper | Iron | 25.1 | curated | [[CTD]], [[FooDB]] |  | 26721301\|21423579\|18307039\|16640825\|1656 |  |
> | Alzheimer Disease | rice | Cer(d18:1/12:0) | 1.5 | curated | [[CTD]], [[FooDB]] |  | 15223066 |  |
> | Alzheimer Disease | black-pepper | Copper | 1.13 | curated | [[CTD]], [[FooDB]] |  | 25542178\|20640797\|17119284\|16962711\|2535 |  |
> | Colorectal Neoplasms | black-pepper | Copper | 1.13 | curated | [[CTD]], [[FooDB]] |  | 37400750 |  |
> | Colorectal Neoplasms | onion | beta-D-Glucose | 13030 | epidemiological | [[FooDB]], [[HMDB]] |  | 28587349\|7482520\|21773981\|27107423\|23940 |  |
> | Colorectal Neoplasms | black-pepper | Piperine | 5350 | epidemiological | [[FooDB]], [[HMDB]], [[NPASS]] |  | 28587349\|7482520\|21773981\|27107423\|23940 |  |
> | Liver Cirrhosis | chicken | Epicholesterol | 75000 | curated | [[CTD]], [[FooDB]] |  | 31877369 |  |
> | Liver Cirrhosis | onion | D-Fructose | 11410 | curated | [[CTD]], [[FooDB]] |  | 39967315\|31672515 |  |
> | Liver Cirrhosis | chicken | Methionine | 495 | curated | [[CTD]], [[FooDB]] |  | 38042390\|30745416\|29097836\|31678261\|2816 |  |
> | Schizophrenia | chicken | Methionine | 495 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 22257447\|17440431\|2415198\|7711000\|238231 |  |
> | Schizophrenia | rice | Methionine | 153 | curated | [[CTD]], [[FooDB]], [[HMDB]] |  | 22257447\|17440431\|2415198\|7711000\|238231 |  |
> | Schizophrenia | black-pepper | Copper | 1.13 | curated | [[CTD]], [[FooDB]] |  | 16842975 |  |
>
> ### Associated
>
> | condition | type | best evidence | sources | characteristic ingredients | via | lab nutrient |
> |---|---|---|---|---|---|---|
> | Breast Cancer, Familial | disease | epidemiological | 2 | 5 | ING:black-pepper, ING:chicken, ING:tomato, ING:rice, ING:onion |  |
> | Prostate cancer, familial | disease | epidemiological | 2 | 5 | ING:black-pepper, ING:chicken, ING:tomato, ING:rice, ING:onion |  |
> | Urinary Bladder Neoplasms | disease | epidemiological | 2 | 4 | ING:rice, ING:onion, ING:tomato, ING:black-pepper |  |
> | Adenocarcinoma of Lung | disease | epidemiological | 2 | 4 | ING:black-pepper, ING:onion, ING:rice, ING:tomato |  |
> | Pancreatic carcinoma, familial | disease | epidemiological | 2 | 4 | ING:onion, ING:tomato, ING:black-pepper, ING:rice |  |
> | Ovarian Neoplasms | disease | epidemiological | 2 | 3 | ING:onion, ING:rice, ING:tomato |  |
>
> Strongest characteristic paths:
>
> | condition | ingredient | compound | mg/100 g | evidence | sources | tradition | PMIDs | note |
> |---|---|---|---|---|---|---|---|---|
> | Adenocarcinoma of Lung | onion | Ascorbic acid | 203.82 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Adenocarcinoma of Lung | tomato | Lycopene | 5.11 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Adenocarcinoma of Lung | onion | (direct) |  | predicted | [[CMAUP]] |  |  | Lung cancer; by target; Non-small cell lung cancer; by targe |
> | Breast Cancer, Familial | onion | Ascorbic acid | 203.82 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Breast Cancer, Familial | chicken | Arachidonic acid | 87 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Breast Cancer, Familial | tomato | Lycopene | 5.11 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Prostate cancer, familial | onion | Ascorbic acid | 203.82 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Prostate cancer, familial | chicken | Arachidonic acid | 87 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Prostate cancer, familial | tomato | Lycopene | 5.11 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Urinary Bladder Neoplasms | onion | Ascorbic acid | 203.82 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Urinary Bladder Neoplasms | tomato | Lycopene | 5.11 | epidemiological | [[Exposome-Explorer]], [[FooDB]] |  |  |  |
> | Urinary Bladder Neoplasms | black-pepper | (direct) |  | predicted | [[CMAUP]] |  |  | Malignant neoplasms of bladder; by transcriptome |
>
> ### Lab-measured nutrients above the FSA "high" threshold
>
> | nutrient | per 100 g | unit | high ≥ (mg) | CTD conditions (sample) | source |
> |---|---|---|---|---|---|
> | sodium | 666 | mg | 600.0 | Heart Diseases; Herpesviridae Infections; Hypotension; Neuralgia, Postherpetic; Acute Kidney Injury; Heart Failure; Myelinolysis, Central Pontine; Water-Electro | [[Saudi Food Composition Tables]] |
>
> ### Food–drug interactions (harmful / negative)
>
> | ingredient | drug | effect | mechanism | PMIDs | source |
> |---|---|---|---|---|---|
> | chicken | Spironolactone | Harmful |  | 31816944 | [[DDID]] |

## Observations across the dish traces
- **Spices carry the signal.** Characteristic compounds with measured amounts (curcumin, piperine, cuminaldehyde,
  gingerols) connect a dish to specific evidence. Without the salience rule, every dish reaches the same generic CTD
  terms through minerals and sugars.
- **Lab-measured dish nutrients** exist only for the Gulf, Kyrgyz and Indian composition tables. For every other
  dish, nutrient effects are only indirect, through ingredients.
- **Mixed directions for one condition** are shown, not resolved. The agent should explain them with the evidence
  grade.
