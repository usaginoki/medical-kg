---
title: "Traces: symptom → dish"
topics: [cultural-food-health]
questions: [Q1, Q2, Q3]
updated: 2026-09-30
tags:
  - type/database
  - q/1
  - q/2
  - q/3
---
# Traces: symptom → dish

Real traces from the [[Unified database]] (build of 2026-09-30). Each condition is expanded to its narrower terms,
its direct parents and the "actions" aimed at it (e.g. *antiemetic* → nausea). Ingredients are ranked by corroboration
and evidence; dishes are ranked **dose-aware** (ingredient score² × weight share), within one country's dishes.

## 4. Nausea: the whole database, with a warfarin check
`uv run db/trace.py condition "nausea" --top 8 --drug warfarin`

**Ingredients that may help**, in order: **ginger** (Duke, IMPPAT, SpiceRx, FooDB: gingerol, [8]-shogaol; ayurveda
and folk use), spearmint, clove (including [[UNaProd]]'s Persian materia medica), saffron, sage, rosemary and
turmeric. Pyridoxine (vitamin B6), a recognised antiemetic in pregnancy, is how spearmint, saffron and turmeric reach
nausea through CTD.

**Dishes that may help** (dose-aware):
- Japanese *ginger rice balls*, a carrot-and-ginger chutney, and an Andhra *allam pachadi* (ginger chutney);
- Goan *solkadhi*, and the Tamil coriander–ginger tea from [[Traces - dish to symptom|trace 2]].

The Osaka burdock stir-fry also appears, because burdock links to nausea through a CTD-curated tropane alkaloid (an
atropine relative) recorded in FooDB. That is a plausible data artefact, and it shows why the hop table must be read.

**Drug caveats for warfarin**, from DDID:
- **Harmful**: coconut and sesame (PMID 4479598), and honey (PMID 16553520);
- **Possible**, through CYP2C9/CYP3A4: coriander, fenugreek, ginger and turmeric (PMIDs 30678660, 36239716, 34062109);
- **No Effect** studies also exist for ginger (PMIDs 17050802, 15801937).

The *Associated (marker)* section of this output is noisy: it holds generic CTD mechanism links through vitamins and
minerals, e.g. shrimp dishes.

This is the kind of mixed evidence the agent should present openly.

> [!example]- Full output: nausea
> ## Condition → dishes: Nausea (`MESH:D009325`, symptom)
>
> Expanded to: Hyperthermia, Cutaneous, With Headaches And Nausea (disease); Postoperative Nausea and Vomiting (symptom); Signs and Symptoms, Digestive (symptom); Feeling Sick (symptom); Nausea (symptom); antiemetic (action)
>
> ### May help: ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | ginger | traditional | 6 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda,folk | Gingerol; (direct); [8]-Shogaol |
> | burdock | curated | 2 | [[CTD]], [[FooDB]] |  | (8-Methyl-8-Azabicyclo[3.2.1]Octan-3-Yl) 3-Hydroxy-2-Phenylpropanoate |
> | spearmint | traditional | 4 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda,folk | (direct); Pyridoxine |
> | saffron | traditional | 3 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | (direct); Pyridoxine |
> | clove | traditional | 3 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[IMPPAT]], [[UNaProd]] | folk,persian,ayurveda | (direct) |
> | common sage | traditional | 5 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] | folk | Pyridoxine; Camphor; (direct) |
> | arabica coffee | traditional | 3 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] | folk | Caffeine; (direct) |
> | common oregano | traditional | 3 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] | folk | Pyridoxine; (direct) |
>
> ### May help: dishes (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | ginger rice balls | JP |  | [[Food.com Recipes and Interactions]] | 14.75 | ginger 50%, rice 25% |
> | 若ごぼうの炒め煮 | JP | 大阪府 | [[Our Regional Cuisines (Japan MAFF)]] | 12.37 | burdock 77% |
> | Carrot and Ginger Chutney |  |  | [[CulinaryDB]] | 10.4 | ginger 20%, coriander 20%, lime 20%, coconut 20% |
> | Allam Pachadi Andhra Style \| Ginger Chutney for Pesarattu \| Allam Chutney With Red Chillies | IN | Andhra Pradesh | [[IndicRecipeNutri]] | 10.22 | ginger 40%, tamarind 7% |
> | Solkadhi Recipe \| Sol Kadi - Kokum Curry | IN | Goa | [[IndicRecipeNutri]] | 9.32 | coconut 80%, ginger 5%, coriander 10% |
> | Kothamalli thanni \| Coriander and ginger tea | IN | Tamil Nadu | [[IndicRecipeNutri]] | 9.3 | ginger 26%, coriander 32% |
> | Roasted Makhana Recipe \| Healthy Snack in Minutes | IN | Bihar | [[IndicRecipeNutri]] | 8.85 | lotus 98%, black-pepper 0% |
> | Coconut milk appam | IN | Kerala | [[IndicRecipeNutri]] | 8.85 | coconut 57%, rice 41%, cardamom 0% |
>
> ### Food–drug interactions with warfarin
>
> | ingredient | drug | effect | mechanism | PMIDs | source |
> |---|---|---|---|---|---|
> | coconut | Warfarin | Harmful |  | 4479598 | [[DDID]] |
> | honey | Warfarin | Harmful |  | 16553520 | [[DDID]] |
> | sesame | Warfarin | Harmful |  | 4479598 | [[DDID]] |
> | honey | Warfarin | Negative |  | 3541503 | [[DDID]] |
> | coriander | Warfarin | Possible | CYP3A4; CYP2C9; CYP2C8; CYP2C9; CYP3A4 | 30678660, 36239716 | [[DDID]] |
> | fenugreek | Warfarin | Possible | CYP3A4; CYP2C9; CYP2C8; CYP2C9; CYP3A4 | 30678660, 36239716 | [[DDID]] |
> | ginger | Warfarin | Possible | CYP3A4; CYP2C9; CYP2C8; CYP2C9; CYP3A4 | 30678660, 36239716 | [[DDID]] |
> | turmeric | Warfarin | Possible |  | 34062109 | [[DDID]] |
> | ginger | Warfarin | No Effect |  | 17050802, 15801937 | [[DDID]] |
>
> ### Associated (marker / mechanism): ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | cocoa bean | curated | 5 | [[CTD]] |  | Nicotinic acid; Copper; Caffeine; Theophylline |
> | garden tomato (var.) | curated | 5 | [[CTD]] |  | Lead; Nicotinic acid; Vitamin E; Copper |
> | almond | curated | 4 | [[CTD]] |  | Nicotinic acid; Vitamin E; Ethinyl Estradiol |
> | pepper (c. frutescens) | curated | 4 | [[CTD]] |  | Ascorbic acid; Nicotinic acid; Ethinyl Estradiol |
> | sunflower | curated | 4 | [[CTD]] |  | Nicotinic acid; Vitamin E; Copper |
> | cumin | curated | 4 | [[CTD]] |  | Nicotinic acid; Copper; Ethinyl Estradiol |
> | pine nut | curated | 4 | [[CTD]] |  | Nicotinic acid; Vitamin E; Copper |
> | anguilliformes | curated | 4 | [[CTD]] |  | Nicotinic acid; Vitamin E; 9-cis-Retinol |
>
> ### Associated (marker / mechanism): dishes (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Grilled Tandoori Style Shrimp with Mint Chutney |  |  | [[CulinaryDB]] | 8.82 | shrimp 98% |
> | 虾仁滑蛋 | CN |  | [[XiaChuFang Recipe Corpus]] | 8.04 | shrimp 89% |
> | Shrimp Madras |  |  | [[CulinaryDB]] | 7.65 | shrimp 85% |
> | Mangalore Fried Shrimp |  |  | [[CulinaryDB]] | 7.61 | shrimp 85% |
> | Korean Shrimp Cocktail | KR |  | [[CulinaryDB]] | 7.57 | shrimp 84% |
> | Poached Bamboo Shrimp | CN |  | [[CulinaryDB]] | 7.45 | shrimp 83% |
> | Indian Style Shrimp Fry |  |  | [[CulinaryDB]] | 7.36 | shrimp 82% |
> | New Year Shrimp | CN |  | [[CulinaryDB]] | 7.31 | shrimp 81% |
>
> ### Food–drug interactions with warfarin
>
> | ingredient | drug | effect | mechanism | PMIDs | source |
> |---|---|---|---|---|---|
> | coconut-milk | Warfarin | Harmful |  | 4479598 | [[DDID]] |
> | sesame | Warfarin | Harmful |  | 4479598 | [[DDID]] |
> | coriander | Warfarin | Possible | CYP3A4; CYP2C9; CYP2C8; CYP2C9; CYP3A4 | 30678660, 36239716 | [[DDID]] |
> | ginger | Warfarin | Possible | CYP3A4; CYP2C9; CYP2C8; CYP2C9; CYP3A4 | 30678660, 36239716 | [[DDID]] |
> | turmeric | Warfarin | Possible |  | 34062109 | [[DDID]] |
> | garlic | Warfarin | No Effect |  | 16484565 | [[DDID]] |
> | ginger | Warfarin | No Effect |  | 15801937, 17050802 | [[DDID]] |

## 5. Type 2 diabetes: India and Saudi Arabia
`uv run db/trace.py condition "type 2 diabetes" --country IN --top 10` and the same with `--country SA`

**Expansion.** The query covers *Diabetes Mellitus, Type 2*, its subtypes, and the parent *Diabetes Mellitus*,
because traditional sources say just "diabetes".

**Ingredients.** **Turmeric, ceylon cinnamon, cumin, cassia, coriander and black pepper** are each backed by 5
sources: [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] (Ayurveda) and
[[SpiceRx]]. Fenugreek is present too (CTD via its compounds, plus Duke), but with fewer independent sources.

**Dishes in India.** Coriander-heavy dishes and chutneys come first (dhaniya sabzi, kothamalli chutney), then ragi
dosa. Spice blends are excluded unless `--blends` is given; with it, rasam powder and garam masala lead.

**Dishes in Saudi Arabia.**
- *Arabic coffee / qahwa* (cardamom and saffron);
- a Saudi kofta and lentil stew;
- *machbous rubyan*;
- a traditional *kabsah*;
- the [[Saudi Food Composition Tables]] black-eyed pea stew from Jazan.

**Reading.** The same condition leads to culturally different dishes: the spices are shared, the vehicles differ.
This is the core use case for culturally tuned advice.

> [!example]- Full output: type 2 diabetes, India
> ## Condition → dishes: Diabetes Mellitus, Type 2 (`MESH:D003924`, disease)
>
> Expanded to: AREDYLD Syndrome (disease); Diabetes Mellitus (disease); Diabetes Mellitus, Lipoatrophic (disease); Diabetes Mellitus, Noninsulin-Dependent, 1 (disease); Diabetes Mellitus, Noninsulin-Dependent, 2 (disease); Diabetes Mellitus, Noninsulin-Dependent, 3 (disease); Diabetes Mellitus, Noninsulin-Dependent, Type 4 (disease); FANCONI RENOTUBULAR SYNDROME 4 WITH MATURITY-ONSET DIABETES OF THE YOUNG (disease); Mason-Type Diabetes (disease); Maturity-Onset Diabetes of the Young, Type 1 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 1 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 13 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 14 (disease); Maturity-Onset Diabetes of the Young, Type 2 (disease); Maturity-Onset Diabetes of the Young, Type 3 (disease); Maturity-Onset Diabetes of the Young, Type 4 (disease); Maturity-Onset Diabetes of the Young, Type 8, with Exocrine Dysfunction (disease); Maturity-Onset Diabetes Of The Young, Type 9 (disease); MODY, Type 6 (disease); Noninsulin-dependent diabetes mellitus with deafness (disease)
>
> ### May help: ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | turmeric | curated | 15 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Curcumin; 4-Methoxycinnamic acid; Nicotinic acid; D-Fructose; (direct); Pyridoxi |
> | basil | curated | 12 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Copper; Nicotinic acid; Tryptophan; Arginine; Potassium; (direct) |
> | cumin | curated | 9 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | (direct); Copper; Nicotinic acid; Potassium |
> | ceylon cinnamon | curated | 9 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | (direct); Chromium; Manganese; cis-Cinnamaldehyde |
> | cassia | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Coumarin; Manganese; (direct) |
> | coriander | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Nicotinic acid; (direct); Potassium |
> | black pepper | curated | 5 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | (direct); Potassium; Copper |
> | sunflower | curated | 15 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | Tryptophan; beta-Sitosterol; Copper; Nicotinic acid; Vitamin E; Pectic acid; (di |
> | fennel | curated | 14 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[SpiceRx]] |  | Potassium; Arginine; Myricetin; Salicylic acid; Tryptophan; (direct); Nicotinic  |
> | cocoa bean | curated | 13 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | siddha | Procyanidin B1; (+)-Catechin; Copper; Nicotinic acid; Caffeine; Procyanidin B2;  |
>
> ### May help: dishes in IN (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Dhaniya Ki Sabji Recipe (Healthy Coriander Sabzi) | IN | Rajasthan | [[IndicRecipeNutri]] | 56.64 | coriander 88%, turmeric 0% |
> | Teekha Chutney ( Mumbai Roadside Recipes ) Recipe | IN | Maharashtra | [[IndicRecipeNutri]] | 55.85 | coriander 87% |
> | Coriander Garlic Chutney Recipe (Dhaniya Lahsun Ki Chutney) | IN | Maharashtra | [[IndicRecipeNutri]] | 53.93 | coriander 84% |
> | Ragi Dosa \| Finger Millet Pancake | IN | Karnataka | [[IndicRecipeNutri]] | 52.33 | coriander 55%, onion 34%, sesame 1% |
> | Green Chutney (Faral ) Recipe (Phalahari Vrat Ki Chutney) | IN | Maharashtra | [[IndicRecipeNutri]] | 51.09 | coriander 80% |
> | Amma’s coriander chutney / kothamalli chutney/Malli chutney/ Recipe with video/ Side dish for idli and dosai | IN | South India | [[IndicRecipeNutri]] | 50.75 | coriander 79% |
> | Bengali Dhone Pata Bata (Roasted Fresh Coriander Paste) | IN | West Bengal | [[IndicRecipeNutri]] | 49.59 | coriander 77% |
> | Pyaz Ki Subzi Recipe (Indian Recipes) | IN | Rajasthan | [[IndicRecipeNutri]] | 48.55 | onion 98%, coriander 0%, fennel 0% |
> | bhavnagri kachori | IN |  | [[CulinaryDB]] | 48.43 | coriander 14%, black-pepper 14%, cumin 14%, sunflower 14%, fennel 14%, sesame 14% |
> | white chole | IN |  | [[CulinaryDB]] | 48.43 | coriander 14%, black-pepper 14%, cumin 14%, clove 14%, sunflower 14%, pomegranate 14% |
>
> ### Associated (marker / mechanism): ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | evening primrose | curated | 9 | [[CTD]], [[HMDB]] |  | Boron; Copper; Quercetin; Iron; Calcium; Manganese |
> | date | curated | 6 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; D-Fructose; Chloride ion; D-Mannose |
> | turmeric | curated | 6 | [[CTD]], [[HMDB]] |  | Iron; beta-D-Glucose; D-Fructose |
> | beer | curated | 5 | [[CTD]], [[HMDB]] |  | L-Lactic acid; Lead; Chloride ion; Glycerol |
> | onion | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; Ascorbic acid; D-Fructose |
> | european plum | curated | 5 | [[CTD]], [[HMDB]] |  | Boron; D-Mannose; beta-D-Glucose |
> | sugar apple | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; Boron; Manganese |
> | sour cherry | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; D-Mannose; Boron |
> | wild carrot | curated | 5 | [[CTD]], [[HMDB]] |  | Vitamin E; beta-D-Glucose; Boron |
> | carob | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; D-Fructose; Calcium |
>
> ### Associated (marker / mechanism): dishes in IN (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Carrot Semolina Phirni Recipe – Carrot Semolina Phirni (Recipe In Hindi) | IN | North India | [[IndicRecipeNutri]] | 15.96 | milk 100% |
> | Milk peda sandesh festival of sweets | IN | West Bengal | [[IndicRecipeNutri]] | 15.85 | milk 99% |
> | Pyaz Ki Subzi Recipe (Indian Recipes) | IN | Rajasthan | [[IndicRecipeNutri]] | 15.78 | onion 98%, coriander 0% |
> | Kashmiri Style Noon Chai Recipe | IN | Jammu & Kashmir | [[IndicRecipeNutri]] | 15.52 | milk 97%, cardamom 0% |
> | Raw Onion Chutney \| Pacha Vengaya Chutney | IN | South India | [[IndicRecipeNutri]] | 15.33 | onion 96% |
> | Anjeer Basundi Recipe: How To Make Anjeer Basundi At Home \| Homemade Anjeer Basundi Recipe | IN | Maharashtra | [[IndicRecipeNutri]] | 15.29 | milk 88%, fig 7%, cardamom 0% |
> | Dates payasam \| dates kheer recipe | IN | Kerala | [[IndicRecipeNutri]] | 15.24 | date 56%, milk 40% |
> | Basundi \| Homemade Basundi Recipe | IN | Maharashtra | [[IndicRecipeNutri]] | 15.17 | milk 95%, cardamom 0% |
> | Chhanar Payesh | IN | West Bengal | [[IndicRecipeNutri]] | 15.11 | milk 94%, cardamom 0% |
> | Besan Ka Sheera Recipe (Natural Cold Remedy) | IN | North India | [[IndicRecipeNutri]] | 15.05 | milk 94%, turmeric 0% |

> [!example]- Full output: type 2 diabetes, Saudi Arabia
> ## Condition → dishes: Diabetes Mellitus, Type 2 (`MESH:D003924`, disease)
>
> Expanded to: AREDYLD Syndrome (disease); Diabetes Mellitus (disease); Diabetes Mellitus, Lipoatrophic (disease); Diabetes Mellitus, Noninsulin-Dependent, 1 (disease); Diabetes Mellitus, Noninsulin-Dependent, 2 (disease); Diabetes Mellitus, Noninsulin-Dependent, 3 (disease); Diabetes Mellitus, Noninsulin-Dependent, Type 4 (disease); FANCONI RENOTUBULAR SYNDROME 4 WITH MATURITY-ONSET DIABETES OF THE YOUNG (disease); Mason-Type Diabetes (disease); Maturity-Onset Diabetes of the Young, Type 1 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 1 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 13 (disease); MATURITY-ONSET DIABETES OF THE YOUNG, TYPE 14 (disease); Maturity-Onset Diabetes of the Young, Type 2 (disease); Maturity-Onset Diabetes of the Young, Type 3 (disease); Maturity-Onset Diabetes of the Young, Type 4 (disease); Maturity-Onset Diabetes of the Young, Type 8, with Exocrine Dysfunction (disease); Maturity-Onset Diabetes Of The Young, Type 9 (disease); MODY, Type 6 (disease); Noninsulin-dependent diabetes mellitus with deafness (disease)
>
> ### May help: ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | turmeric | curated | 15 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Nicotinic acid; D-Fructose; Curcumin; 4-Methoxycinnamic acid; Potassium; (direct |
> | basil | curated | 12 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Tryptophan; Copper; Nicotinic acid; (direct); Potassium; Arginine |
> | cumin | curated | 9 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | (direct); Copper; Nicotinic acid; Potassium |
> | ceylon cinnamon | curated | 9 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | (direct); Manganese; Chromium; cis-Cinnamaldehyde |
> | coriander | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Nicotinic acid; Potassium; (direct) |
> | cassia | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Manganese; Coumarin; (direct) |
> | black pepper | curated | 5 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | ayurveda | Potassium; (direct); Copper |
> | sunflower | curated | 15 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | Copper; Nicotinic acid; Vitamin E; Tryptophan; beta-Sitosterol; Arginine; Pectic |
>
> ### May help: dishes in SA (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | arabic coffee  the saudi way | SA |  | [[Food.com Recipes and Interactions]] | 24.5 | saffron 25%, cardamom 25% |
> | arabic qahwa | SA |  | [[Food.com Recipes and Interactions]] | 24.5 | cardamom 25%, saffron 25% |
> | sweet coffee   or saffron infusion  qahwat al hilo | SA |  | [[Food.com Recipes and Interactions]] | 24.5 | cardamom 25%, saffron 25% |
> | saudi chicken kofta and lentil stew  gluten free | SA |  | [[Food.com Recipes and Interactions]] | 23.6 | coriander 13%, cumin 7%, turmeric 7%, onion 7%, cardamom 7% |
> | machbous rubyan  rice with shrimps | SA |  | [[Food.com Recipes and Interactions]] | 22.82 | turmeric 6%, coriander 6%, black-pepper 6%, onion 6%, curry-powder 6%, cardamom 6%, almond 6% |
> | mom s grilled chicken  aka chicken delicious | SA |  | [[Food.com Recipes and Interactions]] | 20.71 | coriander 7%, black-pepper 7%, cumin 7%, clove 7%, cardamom 7% |
> | the traditional saudi kabssah | SA |  | [[Food.com Recipes and Interactions]] | 20.71 | cumin 7%, coriander 7%, black-pepper 7%, onion 7%, cardamom 7% |
> | Black-Eyed Pea Stew | SA | Jazan | [[Saudi Food Composition Tables]] | 20.42 | onion 42% |
>
> ### Associated (marker / mechanism): ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | evening primrose | curated | 9 | [[CTD]], [[HMDB]] |  | Quercetin; Iron; Calcium; Manganese; Boron; Copper |
> | turmeric | curated | 6 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; D-Fructose; Iron |
> | date | curated | 6 | [[CTD]], [[HMDB]] |  | Chloride ion; D-Mannose; D-Fructose; beta-D-Glucose |
> | sugar apple | curated | 5 | [[CTD]], [[HMDB]] |  | Boron; Manganese; beta-D-Glucose |
> | wild carrot | curated | 5 | [[CTD]], [[HMDB]] |  | Boron; beta-D-Glucose; Vitamin E |
> | beer | curated | 5 | [[CTD]], [[HMDB]] |  | Glycerol; L-Lactic acid; Lead; Chloride ion |
> | european plum | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; Boron; D-Mannose |
> | onion | curated | 5 | [[CTD]], [[HMDB]] |  | beta-D-Glucose; Ascorbic acid; D-Fructose |
>
> ### Associated (marker / mechanism): dishes in SA (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Ruwakah | SA | Aseer | [[Saudi Food Composition Tables]] | 13.66 | milk 85% |
> | Al-Bukayla | SA | Al-Jawf | [[Saudi Food Composition Tables]] | 12.55 | date 78% |
> | Haisah | SA | Al-Madinah | [[Saudi Food Composition Tables]] | 10.32 | date 64%, cardamom 0% |
> | Makhameer | SA | Riyadh | [[Saudi Food Composition Tables]] | 9.93 | milk 59%, onion 3% |
> | Shaa’thah | SA | Riyadh | [[Saudi Food Composition Tables]] | 8.86 | date 55% |
> | Al-Daleekah | SA | Al-Madinah | [[Saudi Food Composition Tables]] | 8 | date 50%, turmeric 0% |
> | Black-Eyed Pea Stew | SA | Jazan | [[Saudi Food Composition Tables]] | 6.67 | onion 42% |
> | bedouin fresh date sweet  rangina   gluten free | SA |  | [[Food.com Recipes and Interactions]] | 6.25 | date 25%, cardamom 25% |

## 6. Hypertension: Japan
`uv run db/trace.py condition "hypertension" --country JP --top 12`

**Ingredients that may help:**
- basil, cumin, oregano, rosemary, black pepper, spearmint and roselle (hibiscus): mostly CTD + Duke + IMPPAT;
- olive (oleuropein; Unani tradition).

Japanese dishes that may help include an Osaka burdock stir-fry (若ごぼうの炒め煮, from [[Our Regional Cuisines (Japan MAFF)]]).

**May aggravate:**
- black pepper, cocoa, coffee, ginger and alcoholic drinks: traditional "hypertensive" activities of piperine,
  caffeine, gingerol and ethanol (Duke).

**Conflicting evidence on licorice**, kept side by side:

| Source | Claim | Evidence |
|---|---|---|
| [[IMPPAT]] | licorice for hypertension, *beneficial* | traditional (Ayurveda) |
| [[SpiceRx]] | licorice → hypertension, **12 positive / 57 negative** papers, so *harmful*; licorice → hypokalaemia 0 / 50 | text-mined, PMIDs 2522135, 15478032, … |
| [[CMAUP]] | licorice ↔ hypokalaemia | clinical-trial association |

**Sodium.** CTD labels dietary sodium → hypertension as *marker/mechanism*, not "harmful", so sodium sits in the
*Associated* section. There it is outranked by generic mineral and fat paths, which are noisy (see the full output).
It is clearest with a direct query:

```sql
-- uv run db/trace.py sql "…"
SELECT i.canonical_name, round(ic.mg_per_100g) AS sodium_mg_100g, cc.direction, cc.source_id, cc.pmids
FROM ingredient_compound ic JOIN ingredient i USING (ingredient_id) JOIN compound cp USING (compound_id)
JOIN compound_condition cc USING (compound_id)
WHERE cp.mesh_id = 'MESH:D012964' AND cc.condition_id = 'MESH:D006973'
  AND i.ingredient_id IN ('ING:soy-sauce', 'ING:miso', 'ING:salt');
```

| ingredient | sodium mg/100 g | CTD | FooDB/Duke |
|---|---|---|---|
| salt | 38,700 | marker (PMIDs 9247761, 1324617, 2992854, 12600921) | harmful |
| soy sauce | 5,637 | marker | harmful |
| miso | 2,950 | marker | harmful |

**1,734 of the 2,719 Japanese dishes (64%)** in the database contain soy sauce or miso.

**Reading.** For a Japanese patient with hypertension, the culturally relevant advice is about seasonings (soy sauce,
miso), not exotic herbs. The trace makes both visible, with their evidence grades.

> [!example]- Full output: hypertension, Japan
> ## Condition → dishes: Hypertension (`MESH:D006973`, disease)
>
> Expanded to: Adams Nance syndrome (disease); Alveolar capillary dysplasia (disease); Arterial Occlusive Disease, Progressive, with Hypertension, Heart Defects, Bone Fragility, and Brachysyndactyly (disease); Brachydactyly with hypertension (disease); Cirrhosis, Familial, with Pulmonary Hypertension (disease); Eclampsia (disease); Egg and banana sign (disease); Essential Hypertension (disease); Familial Primary Pulmonary Hypertension (disease); Faye-Petersen Ward Carey syndrome (disease); HELLP Syndrome (disease); Hemangiomatosis, familial pulmonary capillary (disease); Hypertension, Diastolic, Resistance to (disease); Hypertension, Early-Onset, Autosomal Dominant, with Severe Exacerbation in Pregnancy (disease); Hypertension, Malignant (disease); Hypertension, Pregnancy-Induced (disease); Hypertension, Pulmonary (disease); Hypertension, Renal (disease); Hypertension, Renovascular (disease); Hypertension Resistant to Conventional Therapy (disease)
>
> ### May help: ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | basil | curated | 16 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]], [[SpiceRx]] | folk,ayurveda | Tryptophan; Benzyl acetate; (direct); Nicotinic acid; Calcium; Arginine; Potassi |
> | rosemary | curated | 14 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | homeopathy | Potassium; Oleanolic acid; Calcium; Naringin; Eucalyptol; Ursolic acid; (direct) |
> | cumin | curated | 14 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | Potassium; Nicotinic acid; (direct); Kaempferol; Calcium |
> | common oregano | curated | 14 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | Nicotinic acid; Vitamin E; Potassium; Calcium; Thymoquinone; Ursolic acid; (dire |
> | black pepper | curated | 13 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[SpiceRx]] |  | Potassium; Piperine; Calcium; (direct) |
> | spearmint | curated | 11 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda | Potassium; (direct); Tryptophan; Eucalyptol; Calcium |
> | roselle | curated | 10 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | folk,ayurveda | Chromium; Anthocyanins; (direct); Nicotinic acid; Calcium |
> | olive | curated | 8 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | unani | Quercitrin; oleuropein; Acteoside; Oleuropein; (direct) |
> | common buckwheat | curated | 8 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda,folk | Rutin; Nicotinic acid; Tryptophan; (direct) |
> | burdock | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | homeopathy | (direct); Chromium; (8-Methyl-8-Azabicyclo[3.2.1]Octan-3-Yl) 3-Hydroxy-2-Phenylp |
> | sesame | curated | 6 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[SpiceRx]] |  | (direct); Tryptophan; Nicotinic acid; Arginine |
> | breadfruit | curated | 5 | [[CTD]], [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]], [[IMPPAT]] | ayurveda,folk | Potassium; (direct) |
>
> ### May help: dishes in JP (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | 若ごぼうの炒め煮 | JP | 大阪府 | [[Our Regional Cuisines (Japan MAFF)]] | 37.87 | burdock 77% |
> | Kombu Celery | JP |  | [[CulinaryDB]] | 24.5 | sesame 50% |
> | ミヌダル | JP | 沖縄県 | [[Our Regional Cuisines (Japan MAFF)]] | 21.3 | sesame 43% |
> | Eggplant Salad with Miso Ginger Dressing | JP |  | [[CulinaryDB]] | 19.8 | basil 10%, olive 10%, black-pepper 10%, soybean 10% |
> | wasabi sesame tuna | JP |  | [[Food.com Recipes and Interactions]] | 19.6 | sesame 20%, black-pepper 20% |
> | Tonkatsu Shoyu Ramen (Pork Cutlet Soy Sauce Ramen) | JP |  | [[CulinaryDB]] | 19 | sesame 13%, basil 7%, olive 7%, black-pepper 7%, kombu 7% |
> | 納豆餅 | JP | 京都府 | [[Our Regional Cuisines (Japan MAFF)]] | 18.99 | natto 76% |
> | Sesame Seared Tuna | JP |  | [[CulinaryDB]] | 18.38 | sesame 25%, olive 13% |
> | Teriyaki Sauce and Marinade | JP |  | [[CulinaryDB]] | 18.38 | black-pepper 25%, sesame 13% |
> | Japanese 7 Spice | JP |  | [[CulinaryDB]] | 18.05 | sesame 21%, black-pepper 16% |
> | Spaghettini with Fish Roe Dressing | JP |  | [[CulinaryDB]] | 17.8 | basil 20%, kombu 20% |
> | Miso-Glazed Sea Bass with Asparagus | JP |  | [[CulinaryDB]] | 17.67 | black-pepper 11%, olive 11%, soybean 11%, striped-bass 11% |
>
> ### May aggravate / harmful: ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | black pepper | traditional | 4 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Piperine |
> | cocoa bean | traditional | 4 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Caffeine; Theophylline |
> | ginger | traditional | 3 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Gingerol; [8]-Shogaol |
> | energy drink | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Caffeine |
> | cocoa powder | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Caffeine |
> | coffee mocha | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Caffeine |
> | other alcoholic beverage | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Ethanol |
> | whisky | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Ethanol |
> | liquor | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Ethanol |
> | grape wine | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Ethanol |
> | oats | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Dopamine |
> | port wine | traditional | 2 | [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[FooDB]] |  | Ethanol |
>
> ### May aggravate / harmful: dishes in JP (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Chagome | JP | 徳島県 | [[Our Regional Cuisines (Japan MAFF)]] | 2.45 | broad-bean 61%, salt 0% |
> | oil free teriyaki marinade | JP |  | [[Food.com Recipes and Interactions]] | 2.25 | ginger 25%, sherry 25%, soy-sauce 25% |
> | Bob's Teriyaki Sauce and Marinade | JP |  | [[CulinaryDB]] | 2.23 | sake 44%, soy-sauce 44%, ginger 0% |
> | Ice Cold Saketini | JP |  | [[CulinaryDB]] | 2 | vodka 25%, sake 25% |
> | ginger rice balls | JP |  | [[Food.com Recipes and Interactions]] | 2 | ginger 50% |
> | Coffee Gelatin Dessert | JP |  | [[CulinaryDB]] | 1.95 | coffee 49% |
> | せんざんき | JP | 愛媛県 | [[Our Regional Cuisines (Japan MAFF)]] | 1.86 | sake 14%, ginger 14%, black-pepper 14%, soy-sauce 14% |
> | 山葵漬け | JP | 静岡県 | [[Our Regional Cuisines (Japan MAFF)]] | 1.8 | sake 40%, salt 20% |
> | ginger soy tempura sauce | JP |  | [[Food.com Recipes and Interactions]] | 1.8 | ginger 20%, black-pepper 20%, soy-sauce 20% |
> | Sake-Steamed Chicken and Kabocha Squash | JP |  | [[CulinaryDB]] | 1.8 | sake 20%, ginger 20%, salt 20% |
> | Arame maki | JP | 三重県 | [[Our Regional Cuisines (Japan MAFF)]] | 1.77 | sake 41%, soy-sauce 12% |
> | Japanese Salmon Over Linguine | JP |  | [[CulinaryDB]] | 1.75 | sake 13%, ginger 13%, black-pepper 13%, olive 13%, soy-sauce 13% |
>
> ### Associated (marker / mechanism): ingredients
>
> | ingredient | best evidence | paths | sources | tradition | via |
> |---|---|---|---|---|---|
> | common sage | curated | 9 | [[CTD]], [[HMDB]] |  | Iron; Calcium; Niacinamide; Potassium; Ethinyl Estradiol; Linolenic acid |
> | summer savory | curated | 5 | [[CTD]], [[HMDB]] |  | Potassium; Iron; Calcium; Linolenic acid |
> | beer | curated | 5 | [[CTD]], [[HMDB]] |  | Lead; Agmatine; Nitrate |
> | barley | curated | 5 | [[CTD]], [[HMDB]] |  | Cobalt; Creatinine; Putrescine; (2S)-2-Amino-5-[​[Amino(Dimethylamino)Methylidene |
> | anchovy | curated | 5 | [[CTD]], [[HMDB]] |  | Sucrose; Arachidonic acid; 3h-Sucrose; Epicholesterol; Doconexent |
> | oats | curated | 5 | [[CTD]], [[HMDB]] |  | Creatinine; (2S)-2-Amino-5-[​[Amino(Dimethylamino)Methylidene]Amino]Pentanoic Aci |
> | cottonseed | curated | 4 | [[CTD]], [[HMDB]] |  | Silicon Dioxide; Vitamin E; Arachidonic acid |
> | rape | curated | 4 | [[CTD]], [[HMDB]] |  | Linolenic acid; Vitamin E |
> | wheat (genus) | curated | 4 | [[CTD]], [[HMDB]] |  | (2S)-2-Amino-5-[​[Amino(Dimethylamino)Methylidene]Amino]Pentanoic Acid; Histamine |
> | vegetable oil | curated | 4 | [[CTD]], [[HMDB]] |  | Linolenic acid; Vitamin E |
> | swiss chard | curated | 4 | [[CTD]], [[HMDB]] |  | Creatinine; Dopamine; (2S)-2-Amino-5-[​[Amino(Dimethylamino)Methylidene]Amino]Pen |
> | chia | curated | 3 | [[CTD]], [[HMDB]] |  | Calcium; Linolenic acid |
>
> ### Associated (marker / mechanism): dishes in JP (dose-aware)
>
> | dish | country | subregion | source | score | contributing ingredients (weight share) |
> |---|---|---|---|---|---|
> | Japanese Salted Chicken Wings | JP |  | [[CulinaryDB]] | 14.74 | vegetable-oil 50%, chicken 42% |
> | Gingery Ground Chicken | JP |  | [[CulinaryDB]] | 14.13 | chicken 88% |
> | Tuna Tartare | JP |  | [[CulinaryDB]] | 14.08 | bonito 88% |
> | Japanese-Style Deep Fried Chicken | JP |  | [[CulinaryDB]] | 13.46 | chicken 84% |
> | Chicken Karaage (Japanese Fried Chicken) | JP |  | [[CulinaryDB]] | 13.45 | chicken 49%, vegetable-oil 35% |
> | Shoyu Chicken | JP |  | [[CulinaryDB]] | 11.91 | chicken 74% |
> | Juicy Chicken | JP |  | [[CulinaryDB]] | 11.26 | chicken 70% |
> | Spicy Glazed Eggplant | JP |  | [[CulinaryDB]] | 8.83 | eggplant 86%, vegetable-oil 7% |
> | Sauteed Baby Eggplants | JP |  | [[CulinaryDB]] | 8.69 | eggplant 89%, vegetable-oil 4% |
> | Tsukune (Japanese Chicken Meatballs) | JP |  | [[CulinaryDB]] | 8.46 | chicken 52%, vegetable-oil 1% |
> | とろろまんま | JP | 秋田県 | [[Our Regional Cuisines (Japan MAFF)]] | 8.2 | bonito 20%, anchovy 20%, kombu 20% |
> | Whole Grilled Japanese Eggplant with Lemon and Soy Sauce | JP |  | [[CulinaryDB]] | 8 | bonito 50%, eggplant 0% |

## What the traces show about the database
1. **Both directions work end to end**, with provenance at every hop: dish → ingredient (grams) → compound (mg/100 g)
   → condition (PMIDs) → drug.
2. **Culture changes the answer.** For the same condition, the dishes differ by country: Saudi coffee and kabsa, Indian
   chutneys and dosa, Japanese burdock and seasonings.
3. **Evidence is uneven.** Most compound → condition links are CTD lab/animal findings. Traditional claims are
   numerous. Human clinical evidence is thin: CMAUP trials, HERB trials for turmeric and cassia.
4. **Next improvements:**
   - direction-aware nutrient rules (e.g. "high sodium → harmful for hypertension");
   - the TCM-symptom → modern-symptom mapping from SymMap;
   - resolving the pending [[Access requests]] (FoodAtlas, RecipeDB2);
   - validating the ranking against clinical guidelines.
