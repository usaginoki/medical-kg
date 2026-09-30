---
question: "Which datasets describe the ingredients (foods, spices, herbs, medicinal plants) used by different cultures, and can their effect on the human body be inferred?"
id: Q2
topics: [cultural-food-health]
updated: 2026-09-30
tags:
  - type/question
  - q/2
---
# Q2: Which datasets describe the ingredients (foods, spices, herbs, medicinal plants) used by different cultures, and can their effect on the human body be inferred?

> [!summary] Short answer
> There are three layers. **National food composition tables** give nutrients per ingredient or dish with lab evidence, but no health fields. The effect is only *linkable* through nutrient guidance or scientific names. **Traditional-medicine herb databases** give *direct*, culture-specific claims about the body, and most also link plants to compounds and targets. **Spice and flavour databases** tie cooking ingredients to molecules and to text-mined disease links. For the agent, start with [[Saudi Food Composition Tables]], [[Korean Food Composition Table]], [[Standard Tables of Food Composition in Japan]] and [[USDA FoodData Central]] for nutrients. Then add one herb database per medical system: [[IMPPAT]] (Ayurveda/Siddha/Unani, 4,154 plants, open), [[HERB]] (TCM, 8,558 clinical trials), [[TM-MC]] (Korean/Chinese/Japanese pharmacopoeias), [[UNaProd]] (Persian Mizaj hot/cold rules) and [[KNApSAcK Family]] (Jamu, plus an edible-vs-medicinal flag per country). Finally add [[SpiceRx]] (8,957 spice–disease associations) for the spices that define Middle Eastern and South Asian cooking. [[CMAUP]] and [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] are the cross-cultural bridges. They record which countries or systems use each plant (7,865 plants; 82,873 folk uses in 139 countries) and join to compounds by scientific name or PubChem CID.

## Detailed answer

### 1. National food composition tables (ingredient → nutrients)
All of these are `body_effect: linkable`. Nutrients map to reference intakes, and scientific names or FoodOn/NCBI ids map to compound databases.

- [[Saudi Food Composition Tables]]: 130 Saudi dishes with 1,154 ingredient lines and lab-measured values for 49 components. Typical regional ingredients appear often: ghee (70 lines), whole and cracked wheat (56), lamb (37), cardamom (25), dates (16), dried black lime (12), saffron (6), camel meat (4), desert truffle (2). There are no food codes, so joins go by ingredient name.
- [[Bahrain Food Composition Tables]]: 82 dishes and 113 market products. The nutrients were chosen for Bahrain's deficiency diseases (iron, iodine, vitamin D) and NCD risks (SFA, TFA, cholesterol, sodium).
- [[Kyrgyzstan Food Composition Table]]: 41 strongly local raw foods (koumiss, mare/yak/hainak milk, horse fat, Ozgon rice, wild *Malus sieversii*, sea buckthorn, barberry) with INFOODS tagnames and scientific names. Sea buckthorn β-carotene is 14,200 µg/100 g and barberry vitamin C 244 mg/100 g.
- [[Indian Nutrient Databank (INDB)]]: 332 ingredient food codes across 1,014 recipes, linked to IFCT, UK CoFID and USDA FDC codes. Ingredient botanical names lead on to [[IMPPAT]] and [[FooDB]].
- [[IndicRecipeNutri]]: 927 ingredient nodes with estimated grams and state labels. A knowledge graph links ingredients to 1,607 FlavorDB compounds (PubChem CID). Its health tags are rule-based on nutrients, not evidence.
- [[Korean Food Composition Table]]: 3,366 foods × 132 components, including 18 kimchi types, jang, ginseng and 683 seafood items. 2,090 foods have scientific names. Example: baechu kimchi has Na 551 mg/100 g.
- [[Standard Tables of Food Composition in Japan]]: 2,538 foods, with amino-acid, fatty-acid and carbohydrate companion tables. Examples: natto VITK 600 µg/100 g, which is relevant to warfarin; light miso Na 4,900 mg/100 g. The Korean and Japanese tables share INFOODS tagnames.
- [[USDA FoodData Central]]: 469 Foundation foods and 7,793 SR Legacy foods, CC0. It carries FoodOn and NCBI taxon ids and is the hub most tables and recipe datasets crosswalk to ([[RecipeDB2]], INDB, IndicRecipeNutri). It has **no curcuminoids**, and its phytochemical columns are sparse.

### 2. Traditional-medicine herb databases, by system
These are `body_effect: direct`, but the evidence is mainly **traditional claims**, which must be kept apart from trial or target evidence.

**Ayurveda / Siddha / Unani (India)**
- [[IMPPAT]] 3.0 (September 2026): 4,154 plants, 18,314 phytochemicals, 1,544 therapeutic uses (from 100+ traditional texts) and 1,576 Ayurvedic formulations. It adds 38,842 experimentally supported phytochemical–human-target links. Plants per system: Ayurveda 1,328, Siddha 1,151, Unani 813. Turmeric alone has 263 therapeutic-use rows.
- [[GRAYU]]: an Ayurvedic knowledge graph with 1,039 formulations, 12,743 plants, 129,542 phytochemicals and 13,480 diseases (MeSH/DOID/ICD-11). Every plant–disease edge records its evidence type (trial, target overlap, text). Plants carry the Indian states where they are found. It is browse-only, bulk data needs the authors' agreement, and **its ToS forbid using it to provide medical advice**.

**TCM (China)**
- [[HERB]] 2.0: 6,892 herbs, 44,595 ingredients and 6,743 formulae, with **8,558 clinical trials and 8,032 meta-analyses**. Many "herbs" are everyday foods (green tea 67 trials, olive 64, pomegranate 42, turmeric 32). Example: cinnamon lowered HbA1c by 0.83% in trial NCT00445354.
- [[SymMap]] 2.0: 698 pharmacopoeia herbs → 2,285 TCM symptoms → 1,148 modern-medicine symptoms (expert-mapped) → 14,086 diseases. It is the cleanest resource for the *traditional claim → modern symptom* step, e.g. fresh ginger → 呕吐 → *Emesis*. Relations are web-only (we scraped 8 herbs).

**Korean / Kampo (Northeast Asia)**
- [[TM-MC]] 2.0: 649 medicinal materials from the Korean, Chinese and Japanese pharmacopoeias, with 23,948 compound ids (one PMID per row) and **2,535 Korean-medicine prescriptions with per-material doses**. Ginger is in 489 of the 2,535 prescriptions. Effects are only inferred (STITCH → DisGeNET).
- KAMPO (336 formulae in the 2012 paper) belongs to [[KNApSAcK Family]] but was not scraped.

**Persian / Unani (Iran, and through Unani South Asia)**
- [[UNaProd]]: 3,413 monographs from *Makhzan al-Advieh* (1769). Each has **Mizaj** (hot/cold × wet/dry, degree 1–4), actions, diseases, adverse effects, correctives and dose. Example: the black-seed dose is 2 dirhams for cold-tempered people and ½ dirham for hot-tempered people. It is the only structured source of hot/cold food beliefs. We hold the full index but only 38 full monographs.

**Jamu (Indonesia)**
- [[KNApSAcK Family]] JAMU: 5,310 Indonesian Jamu formulae with efficacy text and effect group. KNApSAcK World adds 76,100 species × country records in 229 countries, each labelled **edible (30,133) or medicinal (45,967)**. It is the only per-country medicine-food flag we have: ginger is medicinal in Saudi Arabia, but edible and medicinal in China, India and Japan.

**Cross-system bridges**
- [[CMAUP]] 2.0: 7,865 plants → 60,222 ingredients → 765,266 plant–ICD-11 disease associations. It covers medicinal plants per system (TCM 2,490, Indian Folk 681, Ayurveda 397, Siddha 367, Unani 274, Sowa-Rigpa 153, Kampo 91) and plants per country for 153 countries. The geography and system fields are web-only, and the country counts reflect where plants grow, not where they are used.
- [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] (CC0): 82,873 folk-use records, 75% of which map to 139 countries. Examples: Iraq 1,053 (Al-Rawi), Turkey 4,815, India 6,837, China 13,469. It also has 104,388 plant-part → chemical records with ppm ranges and 28,929 chemical → activity records. Example: *Nigella sativa* is used for eruption and fever in Iraq, and as a carminative in Turkey.

### 3. Spice and flavour databases
- [[SpiceRx]]: 188 spices and herbs; 8,957 text-mined spice–disease associations (8,172 positive, 783 negative) over 848 MeSH diseases, with PMIDs; and 866 phytochemicals. Its dictionary leans towards South Asian and Middle Eastern spices (ajwain, asafoetida, fenugreek, sumac, golpar, mastic, black cumin). Examples: turmeric → inflammation 60 positive / 1 negative; fenugreek → diabetes 75 / 0; saffron → depression 22 / 0.
- [[FlavorDB2]]: 25,595 flavour molecules, of which 2,254 are linked to 936 natural ingredients with PubChem CID and FooDB id. It is sensory chemistry only, and **curcumin is not in its turmeric list**. It is the compound layer under [[CulinaryDB]], whose 930 basic and 103 compound ingredients carry FlavorDB entity ids.

### 4. Which ingredients cultures actually use
- [[BLEnD]] asks "most common spice/herb", "cooking oil" and "indispensable seasoning" per culture. Iran answered turmeric 4, saffron 3, cinnamon 2. Saudi Arabia answered cinnamon 2, turmeric, bay leaves, red pepper. China answered cumin 2 and star anise 2.
- [[FmLAMA]] (873 English ingredients from Wikidata) and [[World Wide Dishes]] (free-text ingredient lists) give dish → ingredient links per country.
- [[Food.com Recipes and Interactions]] (a Q1 dataset) shows usage rates: turmeric is in 44.0% of `pakistani`, 37.3% of `indian`, 22.6% of `iranian-persian` and 12.7% of `saudi-arabian` recipes.
- [[FoodAtlas]] and [[DDID]] are covered in [[Q3 Food compound & health-effect datasets|Q3]]. DDID's food list includes the priority-region items dates, pomegranate, fenugreek, black seed, turmeric and liquorice.

## Comparison table
%% dataset · cultures/countries · #ingredients · composition/nutrients · body effect (direct/linkable/no) + how · join keys · availability · accessed %%
Availability: open = bulk download · web = browse only · registration · contact. Accessed: ✅ yes · partial 🟡 · ❌ no.

| dataset | cultures/countries | #ingredients | composition / nutrients | body effect + how | join keys | availability | accessed |
|---|---|---|---|---|---|---|---|
| [[Saudi Food Composition Tables]] | [[Saudi Arabia]] | 1,154 ingredient lines (130 dishes) | lab, 49 analytes / 100 g | linkable: nutrients → guidance | dish / ingredient name | open | ✅ |
| [[Bahrain Food Composition Tables]] | [[Bahrain]] | 82 dishes + 113 products | 12 macro, 15 mineral, 10 vitamin | linkable: nutrients (Fe, I, vit D, Na, SFA) | BFCT code, dish name | open | ✅ |
| [[Kyrgyzstan Food Composition Table]] | [[Kyrgyzstan]] | 41 raw foods + 11 dishes | per 100 g, INFOODS | linkable: scientific names → FooDB | food code, INFOODS tag, scientific name | open | ✅ |
| [[Indian Nutrient Databank (INDB)]] | [[India]] | 332 ingredient codes | 41 nutrients | no (nutrients only) | IFCT code, USDA FDC id | open | ✅ |
| [[IndicRecipeNutri]] | [[India]] (states) | 927 ingredient nodes | 33 nutrients per dish (USDA-based) | linkable: rule-based tags; → 1,607 FlavorDB compounds | PubChem CID, FoodOn, USDA id | open | partial 🟡 |
| [[Korean Food Composition Table]] | [[South Korea]] | 3,366 foods | 132 components | linkable: scientific names → FooDB | RDA code, INFOODS tag, scientific name | open (survey) | ✅ |
| [[Standard Tables of Food Composition in Japan]] | [[Japan]] | 2,538 foods | macros, 15 minerals, vitamins, 20 amino acids, ~50 fatty acids | linkable: nutrients → DRIs | MEXT food number, INFOODS tag | open | ✅ |
| [[USDA FoodData Central]] | [[United States]] | 469 + 7,793 foods | 474–477 components | linkable: FoodOn / NCBI taxon → FooDB | FDC id, NDB, FoodOn, NCBI taxon | open | ✅ |
| [[IMPPAT]] | [[India]] (Ayurveda, Siddha, Unani, Sowa Rigpa) | 4,154 plants | 18,314 phytochemicals (no amounts) | direct: 1,544 traditional uses; 38,842 targets | PubChem CID, InChIKey, scientific name | open | ✅ |
| [[GRAYU]] | [[India]] (Ayurveda) | 12,743 plants, 1,039 formulations | 129,542 phytochemicals | direct: plant → 13,480 diseases with evidence type | PubChem, InChIKey, NCBI taxon, MeSH/DOID/ICD-11 | web | partial 🟡 |
| [[HERB]] | [[China]] (TCM) | 6,892 herbs | 44,595 ingredients | direct: 8,558 trials, 8,032 meta-analyses, TCM function | PubChem, InChIKey, SymMap id, NCT | open | ✅ |
| [[SymMap]] | [[China]] (TCM) | 698 herbs | 26,035 ingredients | direct: herb → TCM symptom → modern symptom → disease | PubChem, CAS, HERB id, UMLS | open (entities only) | ✅ |
| [[TM-MC]] | [[South Korea]], [[China]], [[Japan]] | 649 materials, 2,535 prescriptions | 23,948 compounds (presence) | linkable: STITCH → DisGeNET | InChIKey, CID, Latin name | open | ✅ |
| [[KNApSAcK Family]] | 229 countries; Jamu ([[Indonesia]]) | 76,100 species × country; 5,310 Jamu formulae | Core species → metabolites | direct (traditional): edible/medicinal, Jamu efficacy | scientific name, CAS, C_ID, ISO3 | web | partial 🟡 |
| [[UNaProd]] | [[Iran]] (Persian; Unani) | 3,413 monographs | none (→ CMAUP) | direct (traditional): Mizaj, actions, diseases, adverse effects | scientific name, CMAUP id, IrGO | web | partial 🟡 |
| [[CMAUP]] | 153 countries (web); 8 medicine systems | 7,865 plants | 60,222 ingredients | direct: 765,266 plant → ICD-11 disease | PubChem, InChIKey, NCBI taxon, NPO | open | ✅ |
| [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] | 139 countries | 13,079 taxa (ethnobotany); 2,315 plants (chemistry) | 104,388 plant–chemical rows (ppm) | direct: folk use by country; chemical activity | scientific name, chemical name, CAS | open | ✅ |
| [[SpiceRx]] | global (South Asian / Middle Eastern spice list) | 188 spices/herbs | 866 phytochemicals | direct: 8,957 spice → disease (text-mined) | NCBI taxon, PubChem, MeSH | web | partial 🟡 |
| [[FlavorDB2]] | global | 936 ingredients | 25,595 flavour molecules | linkable: PubChem / FooDB id → CTD, FooDB | PubChem CID, FooDB id, entity id | web | partial 🟡 |
| [[CulinaryDB]] | 22 regions | 930 basic + 103 compound | none | linkable: → FlavorDB2 | FlavorDB entity id | open | ✅ |
| [[FoodAtlas]] | global | 1,430 foods | 3,610 chemicals with concentration | direct: chemical → disease (CTD) | FoodOn, FDC, NCBI taxon, PubChem | registration | partial 🟡 |
| [[DDID]] | global foods; [[China]] (TCM herbs) | 270 foods, 1,068 herbs | 43,668 herb–compound rows | direct: 23,950 food/herb–drug interactions | DrugBank ID, PubChem, FooDB id, NCBI taxon | open | ✅ |
| [[BLEnD]] | 33 cultures | spice / oil / seasoning answers | none | no | answer text | open | ✅ |
| [[FmLAMA]] | 122 countries | 873 English ingredients | none | no (Wikidata ids resolvable) | Wikidata QID | open | ✅ |
| [[World Wide Dishes]] | 99 countries | free-text lists (765 dishes) | none | no | ingredient name | open | ✅ |

## Priority regions
| region | what exists | best source |
|---|---|---|
| **GCC** | Nutrients: Saudi (130 dishes) and Bahrain (82) FCTs. Traditional/medicinal use is very thin: KNApSAcK World has Saudi Arabia 71 records, Bahrain 23, Qatar 11, Kuwait 11, Oman 8, UAE 7; Dr. Duke's has Saudi Arabia 1 and Kuwait 3; CMAUP has Saudi Arabia 62 plants and Qatar 3, with no UAE or Bahrain entry. HERB meta-analyses from Saudi Arabia: 49. | [[Saudi Food Composition Tables]] + [[SpiceRx]] / [[KNApSAcK Family]] |
| **Levant / Iran / Turkey** | Persian medicine: [[UNaProd]] (3,413 monographs). Iraq is the best-sourced Middle-East block in Dr. Duke's (1,053 records); Turkey has 4,815 (mostly Steinmetz names). KNApSAcK World: Lebanon 532, Turkey 569, Jordan 386, Iran 150. HERB: 577 meta-analyses from Iran. There is no national FCT. | [[UNaProd]] + [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] |
| **Central Asia** | [[Kyrgyzstan Food Composition Table]] (41 raw foods). KNApSAcK World: Turkmenistan 99, Kyrgyzstan 39, Uzbekistan 20, Tajikistan 18, Kazakhstan 8. CMAUP: Kazakhstan 127, Turkmenistan 105, Uzbekistan 90, Tajikistan 90 plants, no Kyrgyzstan entry. Dr. Duke's has 1 "Turkistan" record. | [[Kyrgyzstan Food Composition Table]] + [[CMAUP]] |
| **South Asia** | Richest: [[IMPPAT]], [[GRAYU]], [[Indian Nutrient Databank (INDB)\|INDB]], [[IndicRecipeNutri]], SpiceRx, plus KNApSAcK World India 3,685, Nepal 1,035, Bangladesh 768, Pakistan 230. | [[IMPPAT]] (+ [[SpiceRx]]) |
| **East Asia** | TCM: [[HERB]], [[SymMap]]. Korea/Japan: [[TM-MC]]. National FCTs for Korea and Japan. KNApSAcK World China 5,090, Japan 3,492. | [[HERB]] + [[TM-MC]] + [[Korean Food Composition Table]] / [[Standard Tables of Food Composition in Japan]] |
| **Southeast Asia** | Jamu formulae (5,310). KNApSAcK World Thailand 2,554, Indonesia 2,127. Dr. Duke's Malaysia 3,220, Indonesia 2,211. No national FCT in the vault. | [[KNApSAcK Family]] |

## Gaps & open questions
- **There is no Gulf or Arab traditional-medicine database.** Dr. Duke's has almost no Gulf records (Saudi Arabia 1), and KNApSAcK World has fewer than 100 records per GCC state. Persian ([[UNaProd]]) and Iraqi (Al-Rawi in Dr. Duke's) sources are the closest.
- **FooDB lacks key regional ingredients:** nigella/black seed, sumac, camel milk, za'atar, ghee and labneh (see [[FooDB]]). USDA FDC has no curcuminoids, and FlavorDB2's turmeric list has no curcumin. For nigella, use [[NPASS]] (thymoquinone 22.6–42.4% of the oil, web only), [[Dr. Duke's Phytochemical and Ethnobotanical Databases]], [[UNaProd]] or [[DDID]].
- **Central Asia has only one FCT (41 raw foods)** and no traditional-medicine database; KNApSAcK has 8 records for Kazakhstan.
- **No medicine-food flag in the TCM databases** ([[SymMap]], [[HERB]], [[TM-MC]]). The only per-country edible/medicinal signal is KNApSAcK World, and we scraped only 36 of 229 countries.
- **Several key sources are only partly accessed:** UNaProd (38 of 3,413 monographs), SpiceRx (29 spices, first result page only), FlavorDB2 (48 ingredients), GRAYU (query excerpt; bulk data needs an email to the authors), CMAUP geography (11 plant pages). Open question: are full polite crawls acceptable under each site's terms?
- **The evidence levels differ and must be labelled for the agent:** traditional text (IMPPAT uses, UNaProd, SymMap symptoms, Jamu), text-mined (SpiceRx), predicted (TM-MC, CMAUP target overlap) and trials (HERB). Composition tables need an external nutrient → outcome resource (DRIs), which is not yet in the vault.
- IFCT 2017 (the Indian raw-ingredient table) must be requested from ICMR-NIN. Southeast Asian national FCTs are missing.

## Datasets
![[Datasets.base#This question]]

## Papers
![[Papers.base#This question]]
