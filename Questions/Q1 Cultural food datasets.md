---
question: "Which datasets describe the foods and dishes of different cultures, and do they give ingredients, amounts and cooking methods?"
id: Q1
topics: [cultural-food-health]
updated: 2026-09-30
tags:
  - type/question
  - q/1
---
# Q1: Which datasets describe the foods and dishes of different cultures, and do they give ingredients, amounts and cooking methods?

> [!summary] Short answer
> For the priority regions, start with the **national composition tables that list dishes with recipes**. [[Saudi Food Composition Tables]] has 130 lab-analysed Saudi dishes from 13 regions, with gram amounts, steps and 49 analytes. [[Bahrain Food Composition Tables]] has 82 Gulf dishes, [[Kyrgyzstan Food Composition Table]] 11 Central Asian dishes, and [[Indian Nutrient Databank (INDB)]] 1,014 Indian recipes. For scale and everyday cooking, use one open recipe corpus per region: [[IndicRecipeNutri]] (219,384 Indian recipes with gram weights and 21 state or community labels), [[XiaChuFang Recipe Corpus]] (1.52 M Chinese recipes with steps) and [[Our Regional Cuisines (Japan MAFF)]] (1,355 Japanese regional dishes with amounts, steps and eating occasions). [[Food.com Recipes and Interactions]] (231,637 recipes, cuisine tags for 69 countries) covers the cross-cultural gaps. The richest structured corpus, [[RecipeDB2]] (128,942 recipes with amounts, steps and USDA-linked nutrition), and [[NII Cookpad Dataset]] (~1.72 M Japanese recipes) need the owners' permission. For the dish → country map, use [[WorldCuisines]] (2,414 dishes, 186 countries) and [[FmLAMA]] (2,818 Wikidata dishes with ingredients). For what people typically eat, use [[BLEnD]] (33 cultures) and [[ArabCulture]] (724 Arab meal scenarios, including Saudi and Emirati).

## Detailed answer

### 1. Large recipe corpora (ingredients, amounts, steps)
These give the agent **how dishes are actually cooked**. None of them covers the Gulf states or Central Asia properly.

- [[RecipeDB2]] is the most complete schema. It has 128,942 recipes and 35,474 ingredients from 99 countries. Each ingredient has quantity, unit and state and links to a USDA SR Legacy `ndb_id`, which gives about 150 nutrient keys per recipe. Recipes also have ordered instructions, processes and utensils. **The data is not released** ("institutional copyright"). We hold 43 v2 recipes and 375 v1 records. The v1 region counts include Middle Eastern 3,905, Indian Subcontinent 6,464, Chinese and Mongolian 5,896, Japanese 2,041, Southeast Asian 1,940 and Korean 668. There is nothing for Central Asia.
- [[Food.com Recipes and Interactions]] has 231,637 open recipes with ingredient names (no amounts), full ordered steps and computed %DV nutrition. It is US-centric (31,596 US-tagged), but it has usable priority-region sets: India 2,708, China 2,008, Thailand 1,208, Japan 851, Lebanon 308, Turkey 286, Iran 252, Pakistan 141, Saudi Arabia 102. It also tags 279 recipes `ramadan`. Tags are user-assigned on an American site.
- [[CulinaryDB]] has 45,772 recipes in 22 regions plus 4 small "Misc." groups: Indian Subcontinent 4,058, Middle East 993, China 941, Thailand 667, South East Asia 611, Japan 580, Korea 301. Each ingredient is normalised to 930 basic and 103 compound entities keyed by FlavorDB entity id. Amounts only appear inside the raw ingredient line, and there are no steps or nutrition.
- [[IndicRecipeNutri]] is the largest sub-national corpus: 219,384 Indian recipes from 378 sites and 2,338,910 ingredient-weight rows with estimated grams. It has 33 nutrients per dish and cooking-method tags; the step text is withheld. `Region` labels cover Kerala 11,527, Tamil Nadu 11,375, Punjab 10,502, West Bengal 6,431 and more, but 61.5% are "Pan-Indian" (unlabelled). Nutrition is USDA-grounded, not IFCT.
- [[XiaChuFang Recipe Corpus]] has 1,520,327 Chinese home recipes, 1.24 M of them mapped to 30,060 canonical dishes. Ingredients carry fused, unstructured amounts ("1kg羊肉", "适量花椒"), and every recipe has ordered steps. There is no nutrition and no province field. We hold the first 64,742 recipes.
- [[NII Cookpad Dataset]] has ~1.72 M Japanese recipes and ~36k meals (main and side dishes combined), with structured quantities, steps and ~10 M cook reports. Access needs an institutional application with a sealed contract, and we have **not** accessed it.
- [[Our Regional Cuisines (Japan MAFF)]] is small but curated. It has 1,355 dishes (~30 per prefecture, all 47) with amounts, numbered steps, history and **when and on what occasion each dish is eaten**. 885 dishes are in English.

### 2. National food composition tables that include dishes
These are the **authoritative per-dish nutrient values** for the priority regions. Each has only a few hundred dishes or fewer.

- [[Saudi Food Composition Tables]] (SFDA, 1st ed.) is the best GCC resource. It has 130 dishes from all 13 regions (Makkah 22, Al-Madinah 13, Al-Baha 13 …), each with a standardised recipe (1,154 ingredient lines in g/ml), numbered steps, and ISO 17025 lab analysis of 49 components per 100 g and per recipe. For example, Lamb Kabsa has 158 kcal, 6.1 g fat and 497 mg Na per 100 g. We parsed the whole PDF. The web tool fd.sfda.gov.sa is geo-blocked from our host.
- [[Bahrain Food Composition Tables]] (MOH 2025) has 82 traditional and composite dishes (machboos, harees, balaleet, qouzi…) and 113 market products. It gives 12 macronutrient, 15 mineral and 10 vitamin columns. Only 27 dish rows are Bahraini lab analyses; about 56 values are borrowed from the Kuwait, Oman, Lebanon, Jordan and UAE tables. The ingredient annex has grams (Machboos dajaj: 500 g rice, 100 g chicken, 5 g turmeric, 10 g dry lemon…), but its PDF text layer is garbled and it is not in CSV.
- [[Kyrgyzstan Food Composition Table]] (2022) is the only Central Asian FCT. It has 41 raw foods (koumiss, yak and horse fat, wild fruits) and 11 dishes (beshbarmak, plov with barberry, 3 manty variants, lagman, shorpo…), with gram recipes, short method text and calculated composition.
- [[Indian Nutrient Databank (INDB)]] has 1,014 standard Indian recipes with g/ml/tsp amounts linked to IFCT codes and 41 nutrients per 100 g and per serving. It has no steps and no state labels.
- [[Central Asian Digital Visual Food Atlas]] is a companion source, not an FCT. It gives **serving weights** for 115 Central Asian foods and drinks (e.g. beshbarmak 194/365/541 g; kymyz 206 ml) with names in 5 local languages. Grams from the atlas × per-100 g values from the Kyrgyz FCT give nutrients per plate.

### 3. Culture knowledge bases and benchmarks
These tell the agent **which dishes belong to which culture and what people typically eat**. They have no amounts or steps.

- [[WorldCuisines]] is the broadest dish → country map: 2,414 Wikipedia dishes in 186 countries, with descriptions that name the main ingredients. Coverage: Iran 65, Turkey 69, Saudi Arabia 24, and every GCC state ≥ 10, but those are mostly shared dishes (other GCC states have 0 single-country dishes). Central Asia has only 5–10 dishes per country.
- [[FmLAMA]] has 2,818 Wikidata dishes from 122 countries with "has part" ingredients in up to 248 languages. The mean is 2.1 ingredients per English dish, i.e. main ingredients only. It is strong for Japan 189, India 149, Indonesia 113, Turkey 105 and China 103. The UAE, Qatar, Kuwait and Oman have 0 dishes.
- [[World Wide Dishes]] has 765 community-written home dishes in 99 countries, with free-text ingredient lists and eating context (time of day, occasions such as Ramadan and Eid, drink). It is Africa-heavy (501 of 765); Saudi Arabia has 2 dishes and the UAE 1.
- [[BLEnD]] asks the same 500 questions in 33 language-culture pairs, 105 of them about food (breakfast, snacks, festival food, most common spice, cooking oil). It is the best source of *everyday* habits for Iran, Saudi Arabia, Egypt, Assam, Sri Lanka, China, the Koreas, Japan, Taiwan, Indonesia, Singapore and the Philippines.
- [[ArabCulture]] (MBZUAI) has 724 Food items across 13 Arab countries: breakfast, lunch, iftar, sahoor, desserts and more. Examples: a Saudi breakfast after Fajr is ful with bread; Emiratis break the fast with dates and coffee. It is the only resource with **Emirati** meal patterns (59 food items).
- [[Central Asian Food Dataset]] (CAFD/CAFSD) has 21,306 real meal photos with 69,865 boxes over 239 classes, including 42 national dishes. It shows which dishes and side foods appear together on Central Asian plates. There are no recipes.
- [[ArSyra Food and Culture]] is a commercial dialect sample. Our 50-record preview comes from one Syrian speaker. It is not a dish database and has low value.

## Comparison table
%% dataset · cultures/countries · #dishes · ingredients · amounts · cooking method · nutrition · availability · accessed %%
Availability: open = bulk download · web = browse only · request = application · contact = ask the authors · commercial. Accessed: ✅ yes · partial 🟡 · ❌ no.

| dataset | cultures/countries | #dishes / records | ingredients | amounts | cooking method | nutrition | availability | accessed |
|---|---|---|---|---|---|---|---|---|
| [[Saudi Food Composition Tables]] | [[Saudi Arabia]], 13 regions | 130 dishes | ✅ 1,154 lines | yes (g/ml) | steps | lab, 49 analytes | open | ✅ |
| [[Bahrain Food Composition Tables]] | [[Bahrain]] | 82 dishes + 113 products | annex (PDF only) | partial | no | 12 macro + 15 mineral + 10 vitamin | open | ✅ |
| [[Kyrgyzstan Food Composition Table]] | [[Kyrgyzstan]] | 11 dishes + 41 raw foods | ✅ 162 lines | yes | steps (prose) | calculated | open | ✅ |
| [[Indian Nutrient Databank (INDB)]] | [[India]] | 1,014 recipes | ✅ | yes | no | 41 nutrients | open | ✅ |
| [[Central Asian Digital Visual Food Atlas]] | 5 Central Asian countries | 115 items | descriptions only | serving weights | no | no | open (removed from repo head) | ✅ |
| [[Central Asian Food Dataset]] | Central Asia (Kazakh-centred) | 42 dish classes / 239 classes | no | no | no | no | open | partial 🟡 |
| [[RecipeDB2]] | 99 countries | 128,942 recipes | ✅ | yes | steps | ~150 nutrient keys (USDA) | contact | partial 🟡 |
| [[Food.com Recipes and Interactions]] | 69 countries (tags) | 231,637 recipes | ✅ | no | steps | computed %DV | open | ✅ |
| [[CulinaryDB]] | 22 regions + 4 misc | 45,772 recipes | ✅ | partial (raw line) | no | no | open | ✅ |
| [[IndicRecipeNutri]] | [[India]] (21 states/communities) + 15 cuisine countries | 219,384 recipes | ✅ | yes (est. grams) | tags | 33 nutrients | open | partial 🟡 |
| [[XiaChuFang Recipe Corpus]] | [[China]] | 1,520,327 recipes | ✅ | partial | steps | no | open | partial 🟡 |
| [[NII Cookpad Dataset]] | [[Japan]] | ~1.72 M recipes, ~36k meals | ✅ | yes | steps | no | request | ❌ |
| [[Our Regional Cuisines (Japan MAFF)]] | [[Japan]], 47 prefectures | 1,355 dishes | ✅ | yes | steps | no | open | ✅ |
| [[WorldCuisines]] | 186 countries | 2,414 dishes | prose only | no | no | no | open | partial 🟡 |
| [[FmLAMA]] | 122 countries | 2,818 dishes | ✅ (mean 2.1) | no | no | no | open | ✅ |
| [[World Wide Dishes]] | 99 countries | 765 dishes | ✅ free text | no | no (recipe URLs) | no | open (terms) | ✅ |
| [[BLEnD]] | 33 cultures / 29 countries | 105 food questions per culture | spice/oil answers | no | no | no | open | ✅ |
| [[ArabCulture]] | 13 Arab countries | 724 food items | implicit | no | no | no | open | ✅ |
| [[ArSyra Food and Culture]] | 15 countries claimed (preview: Syria) | 50 preview / 4,579 claimed | no | no | no | no | commercial | partial 🟡 |

## Priority regions
| region | what exists | best source |
|---|---|---|
| **GCC** | Two national dish FCTs: Saudi Arabia (130) and Bahrain (82). Meal-pattern sentences for Saudi Arabia (53 food items) and the UAE (59) in [[ArabCulture]]. Saudi Arabia only in [[BLEnD]]. Mostly shared dishes in [[WorldCuisines]] (Saudi Arabia 24; UAE 12, Kuwait 12, Bahrain 11, Qatar 10, Oman 10). Food.com 102 Saudi recipes; RecipeDB v1 ~100. | [[Saudi Food Composition Tables]] for dishes and nutrients, plus [[ArabCulture]] for meal slots and Ramadan. |
| **Levant / Iran / Turkey** | Iran 65 and Turkey 69 dishes in [[WorldCuisines]]; Turkey 105 and Iran 22 in [[FmLAMA]]; Iran in [[BLEnD]]; Food.com Lebanon 308, Turkey 286, Iran 252; Levant in [[ArabCulture]] (Jordan, Lebanon, Palestine, Syria). No national dish FCT or recipe corpus for any of them. | [[WorldCuisines]] + [[Food.com Recipes and Interactions]] |
| **Central Asia** | Images ([[Central Asian Food Dataset]], 239 classes), portion weights ([[Central Asian Digital Visual Food Atlas]], 115 items), one FCT with 11 dishes ([[Kyrgyzstan Food Composition Table]]); 5–10 dishes per country in WorldCuisines and 3–7 in FmLAMA. No recipe corpus. | [[Kyrgyzstan Food Composition Table]] × the atlas weights |
| **South Asia** | India is well covered: [[IndicRecipeNutri]] (state labels), [[Indian Nutrient Databank (INDB)\|INDB]], CulinaryDB Indian Subcontinent 4,058, Food.com India 2,708. Pakistan, Bangladesh and Sri Lanka appear only in knowledge bases or as small tag sets. | [[IndicRecipeNutri]] + [[Indian Nutrient Databank (INDB)]] |
| **East Asia** | China: [[XiaChuFang Recipe Corpus]]. Japan: [[Our Regional Cuisines (Japan MAFF)]] and [[NII Cookpad Dataset]] (on request). Korea: only 301 CulinaryDB recipes, 253 Food.com recipes and 69 WorldCuisines dishes. | XiaChuFang (China), MAFF (Japan) |
| **Southeast Asia** | No national corpus or FCT. Multi-country resources only: WorldCuisines (Indonesia 143, Philippines 133, Malaysia 78), FmLAMA (Indonesia 113), Food.com (Thailand 1,208), BLEnD (Indonesia, Singapore, Philippines). | [[WorldCuisines]] + [[BLEnD]] |

## Gaps & open questions
- **There is no dish composition table for the UAE, Qatar, Kuwait or Oman.** The Gulf is represented by Saudi Arabia (130 dishes) and Bahrain (82, of which about 56 values are borrowed from other Arab tables). FmLAMA has 0 dishes for these four states, and WorldCuisines and World Wide Dishes list only shared dishes.
- **Central Asia has only images, portion sizes and one 11-dish FCT.** No recipe corpus has amounts or steps, and RecipeDB2, CulinaryDB, Food.com and BLEnD have no Central Asian label.
- **Iran and Turkey have no recipe corpus of their own.** The largest sets are Food.com's 252 Iranian and 286 Turkish recipes, which are American-site, user-tagged adaptations.
- **Southeast Asia has no national FCT or recipe corpus** in the vault.
- **The best structured corpora are gated.** [[RecipeDB2]] needs an email to the authors (NEEDS USER). [[NII Cookpad Dataset]] needs an institutional application, and its terms forbid feeding the data to external LLM services. The Saudi web tool is geo-blocked, and the Arabic Saudi PDF was not obtained.
- **Most culture labels are coarse or inferred.** Examples: CulinaryDB "Middle East" (993 recipes) is not split by country; 61.5% of IndicRecipeNutri recipes are "Pan-Indian"; Food.com tags cover only 39% of recipes.
- Open: should we add the China Food Composition Tables and IFCT 2017 (must be requested from ICMR-NIN)? Should we parse the Bahrain ingredient annex by OCR?
- Licence constraints for all datasets are collected in [[Q3 Food compound & health-effect datasets#Licences & usage constraints]].

## Datasets
![[Datasets.base#This question]]

## Papers
![[Papers.base#This question]]
