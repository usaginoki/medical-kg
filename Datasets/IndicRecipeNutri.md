---
title: "IndicRecipeNutri"
slug: indicrecipenutri
kind: [food, ingredient]
version: "0.10.0 (GitHub, 2026-09-20)"
previous_versions: "0.9.0 (Zenodo 10.5281/zenodo.22729969, 2026-09-13); 0.3.0–0.8.x (Zenodo concept DOI 10.5281/zenodo.22512534)"
papers: []
url: "https://doi.org/10.5281/zenodo.22512534"
license: "data CC BY-NC-SA 4.0 (FlavorDB compound layer CC BY-NC-SA 3.0); code MIT"
availability: open-download
access_link: "https://github.com/Poshaka-Research-Lab/IndicRecipeNutri-dataset"
accessed: partial
access_method: [github]
access_date: 2026-09-30
access_notes: "Shallow git clone (git-lfs is not installed), then the Git-LFS parquet files were fetched from media.githubusercontent.com. Taken: all corpus tables except quality/rehydration/nutrition_derived, the whole KG (data/kg/*: kg_edges, kg_nodes, kg_edge_evidence, pairs_regional, substitutes_ours), data/kg_flavor/*, and enrichment/ingredients_weights (211 MB). Not taken (to stay under ~500 MB): provenance/field_history (62 MB), enrichment/ingredients_nutrition (110 MB) and the other 24 enrichment tables, data/interactions (synthetic users, 35 MB), benchmark. The recipe prose (instructions, descriptions, raw ingredient lines) is withheld by the authors; it can be rehydrated from source URLs with scripts/rehydrate.py for 214,579 rows (not done)."
countries: ["[[India]]", "[[United States]]", "[[United Kingdom]]", "[[Italy]]", "[[China]]", "[[France]]", "[[Thailand]]", "[[Mexico]]", "[[Japan]]", "[[Spain]]", "[[Greece]]", "[[South Korea]]", "[[Vietnam]]", "[[Malaysia]]", "[[Germany]]", "[[Indonesia]]", "[[Pakistan]]"]
regions: ["[[South Asia]]", "[[Middle East]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]"]
n_records: "219,384 recipes (378 source sites); 2,338,910 ingredient-weight rows; KG 222,537 nodes / 6,426,916 edges"
size: "~474 MB full release; 211 MB downloaded"
formats: [parquet, jsonl, csv]
has_ingredients: true
has_amounts: yes
has_cooking_method: tags
has_nutrition: true
body_effect: linkable
body_effect_how: "Recipe-level nutrition-derived health tags (HealthConditions, suitable_for → condition such as hypertension_friendly, renal_caution); ingredient → FlavorDB compound (PubChem id) → external bioactivity/disease resources; ingredient → FoodOn class."
join_keys: [PubChem CID, FoodOn id, recipe URL, ingredient name, USDA SR/FDC food id]
topics: [cultural-food-health]
questions: [Q1, Q2]
relevance: core
found_by: [search/food]
tags:
  - type/dataset
  - kind/food
  - kind/ingredient
  - q/1
  - q/2
  - access/accessed
  - access/open
---
# IndicRecipeNutri

> [!abstract] TL;DR
> IndicRecipeNutri is a 2026 release by the Poshaka Research Lab (Badgujar, Borde, Gurav; Ajeenkya D Y Patil
> University, Pune). It has **219,384 recipes from 378 Indian recipe sites and open datasets**, with parsed
> ingredients (English/Roman), **estimated gram weights per ingredient**, dish-level nutrition (35 nutrients),
> FSA traffic lights, 17-class allergens, diet, course and cooking-method tags. A **`Region` label has 27
> values, 21 of them Indian states or communities**. It also ships a typed knowledge graph of 6.43 M edges
> (recipes, ingredients, FlavorDB compounds, regions, health tags, conditions). It is the largest sub-national
> Indian food dataset in the vault (Q1, Q2). Most state labels are inferred rather than stated by the source,
> and nutrition is **USDA-grounded, not IFCT**.

## Access
| | |
|---|---|
| Availability | open download (GitHub with Git LFS; Zenodo snapshots) |
| Link | https://github.com/Poshaka-Research-Lab/IndicRecipeNutri-dataset |
| Accessed? | partial: all core tables and the KG, not every enrichment or provenance table |
| How | `git clone --depth 1`, then `curl` of LFS objects from `media.githubusercontent.com/media/…/main/<path>` |
| Downloaded | `Data/indicrecipenutri/` (211 MB): `data/corpus/{recipes_structured,recipes,labels,nutrition,allergens}.parquet`, `data/kg/*`, `data/kg_flavor/*`, `data/enrichment/ingredients_weights.parquet`, plus `README.md`, `CHANGELOG.md`, `CITATION.cff`, `docs/` (DATASHEET, DATA_DICTIONARY, VERSIONS…) |

The recipe prose (instructions, descriptions, raw ingredient lines) is **not redistributed**.
`rehydration_index.parquet` plus `scripts/rehydrate.py` re-fetch it from the source URLs (214,579 of 219,386
rows).

## Tables & columns
Column meanings come from `docs/DATA_DICTIONARY.md` and the README. The dictionary itself leaves meanings
blank where the authors did not document them; entries marked "(inferred)" are ours.

### `data/corpus/recipes_structured.parquet` (219,384 rows × 270 columns): the main wide table
| column | type | meaning | example |
|---|---|---|---|
| `recipe_id` | int | stable recipe id (join key for all tables) | 3938 |
| `RecipeName`, `URL`, `SourceSite` | str | title, source page, source site (cookpad 13,988 · pachakam 11,392 · archanaskitchen 7,500 · TarlaDalal 7,407…) | Aval Payasam…, hebbarskitchen |
| `IngredientsList` | str (JSON list) | parsed ingredient lines, English/Roman | ["2 tbsp ghee", "1 cup poha / avalakki", "1 litre milk", …] |
| `Region` | str | 27 values: state (Kerala, Punjab…), macro-region (North/South India) or `Pan-Indian` = unlabelled | Kerala |
| `Region_orig`, `region_inferred`, `region_src` | str/bool | the label before correction; whether it was inferred | |
| `Cuisine` | str | 53 cuisine labels (Indian, South Indian, Kerala, Punjabi… and American, Italian, Thai…) | South Indian |
| `cuisine_scope` | str | indian 171,404 · indian-adapted 23,769 · non-indian 23,285 · indo-fusion 868 · unknown 58 | indian |
| `Course` | str | 12 courses (Main Course 91,036; Dessert 37,043; Breakfast 19,421…) | Dessert |
| `Diet`, `diet_meat_class` | str | Vegetarian / Vegan / Non-Vegetarian / Eggetarian / unknown; meat class | Vegetarian |
| `CookingMethod` | str | `;`-joined method tags (fried, boiled, no_cook, baked, roasted…) | boiled;roasted |
| `Occasion`, `DietaryContext` | str | festival/occasion (644 values, e.g. eid, diwali) and context such as `jain_sattvic`, fasting | eid |
| `SpiceLevel`, `Difficulty`, `StepCount`, `PrepTimeMins`, `CookTimeMins`, `Servings` | mixed | recipe metadata | medium, 15 |
| `Nut_Calories` … `Nut_Manganese` (33 cols) | float | nutrients **per dish** (kcal, g, mg, µg) | 641.98 |
| `Nut_Tier`, `Nut_MatchCov`, `Nut_Confidence` | str/float | quality tier of the nutrition estimate (A 204,629; B 9,963; C 1,235; E 3,499) | A |
| `per100g_kcal`, `per100g_protein`, … `per100g_salt` | float | per-100 g values | 244.9 |
| `fsa_fat`, `fsa_saturates`, `fsa_sugars`, `fsa_salt` | str | UK FSA traffic lights (green/amber/red) | amber |
| `HealthGrade`, `HealthConditions`, `gl_bucket`, `GlycemicLoad_numeric` | str/float | rule-based A–E grade; comma-separated suitability tags; glycaemic-load bucket/value per serving | D; hypertension_friendly,renal_caution,high_energy |
| `DV_Protein` … `DV_Zinc` | float | % daily value per serving (inferred) | |
| `Allergens_v2`, `allergen_tier`, `contains_*` | str/bool | 17 allergen classes; `unknown` means *not assessed*, not *safe* | coconut:direct;milk:derived |
| `Split_v2`, `Split_v3` | str | benchmark splits | train |
| ~170 further columns | mixed | provenance and correction history (`*_orig`, `*_pre_*`, `*_uncorrected`, `badlist_*`, `title_*`, `dup_family_*`, `ing_weight_confident_frac`…) | |

### `data/corpus/labels.parquet` (219,384 × 21) · `nutrition.parquet` (219,384 × 36) · `recipes.parquet` (219,384 × 74) · `allergens.parquet` (3,729,528 × 3)
Narrow views of the wide table. `labels` holds Diet, Region, Cuisine, Course, CookingMethod, HealthConditions,
GlycemicLoad… `nutrition` holds `Nut_*` per dish plus `Nut_Tier`. `recipes` holds metadata and source
licence. `allergens` is long format: `recipe_id`, `allergen` (17 classes), `status` (present / absent / unknown).

### `data/enrichment/ingredients_weights.parquet` (2,338,910 rows × 11): ingredient amounts
| column | type | meaning | example |
|---|---|---|---|
| `recipe_id`, `ing_index` | int | recipe and ingredient position | 3938, 4 |
| `name` | str | normalised ingredient name | poha / avalakki |
| `quantity`, `unit` | float, str | parsed amount | 1.0 cup |
| `grams` | float | estimated mass | 156.0 |
| `confident`, `tier` | bool, str | estimate confidence; tier A 1,224,959 · B 325,111 · C 50,913 · D 316,271 · E 420,909 (D/E = default weights with no stated quantity) | True, A |
| `quantity_observed`, `unit_observed`, `weight_status` | mixed | amount as found in the source; `estimated` for 2,337,017 rows | estimated |

### `data/kg/kg_nodes.parquet` (222,537 × 44) · `kg_edges.parquet` (6,426,916 × 3) · `kg_edge_evidence.parquet` (236,315 × 4)
Nodes have `node_id` (`type::key`), `type`, `name`, nutrient columns `n_*` for recipes, and `pubchem_id` for
compounds. Node types: recipe 219,384 · compound 1,607 · ingredient 927 · foodclass 363 (FoodOn) · cuisine 53 ·
occasion 44 · healthtag 30 · region 27 · nutrient 22 · allergen 18 · condition 13 · course 12 · method 11 ·
category 11 · diet 8 · zone 5 · context 2.
Edges are `head`, `rel`, `tail`. Relations: has_ingredient 1,916,036 · has_health_tag 1,725,100 · suitable_for
895,452 · contains_allergen 485,055 · cooked_by 404,145 · has_diet 256,132 · in_cuisine / is_course /
from_region 219,347 each · for_occasion 33,356 · **has_compound 25,748** (ingredient → FlavorDB compound) ·
shares_flavor 13,670 · rich_in 2,935 (ingredient → nutrient) · grounded_as 369 (ingredient → FoodOn) ·
typical_region 48 · substitute_for 30…

### `data/kg/pairs_regional.parquet` (1,847 × 9) · `substitutes_ours.parquet` (3,411 × 11) · `data/kg_flavor/flavor_nodes.parquet` (1,607 × 4) · `flavor_edges.parquet` (39,998 × 5)
Region-specific ingredient pairings, ingredient substitutions, and the separable FlavorDB compound layer.

Sample: `Data/indicrecipenutri/sample.csv` · full profile: `Data/indicrecipenutri/schema.md` · authors' dictionary: `Data/indicrecipenutri/docs/DATA_DICTIONARY.md`

## Countries & cultures covered
**[[India]]**: 171,404 recipes scoped `indian`, 23,769 `indian-adapted` and 868 `indo-fusion`.

**Per-state / sub-national counts (`Region`, all 219,384 recipes):**
| Region label | recipes | | Region label | recipes |
|---|---:|---|---|---:|
| Pan-Indian (= unlabelled) | 135,018 | | Bihar | 771 |
| North India (macro) | 12,112 | | Telangana | 743 |
| South India (macro) | 11,579 | | Jammu & Kashmir | 457 |
| Kerala | 11,527 | | Uttar Pradesh | 393 |
| Tamil Nadu | 11,375 | | Sindhi (community) | 306 |
| Punjab | 10,502 | | Parsi (community) | 149 |
| West Bengal | 6,431 | | Odisha | 80 |
| Maharashtra | 5,016 | | Assam | 65 |
| Karnataka | 4,788 | | Himachal Pradesh | 52 |
| Gujarat | 3,677 | | Uttarakhand | 8 |
| Andhra Pradesh | 1,862 | | Nagaland | 8 |
| Goa | 1,545 | | East India (macro) | 8 |
| Rajasthan | 871 | | West India (macro) | 3 |
| | | | Manipur | 1 |
| | | | *(missing)* | 37 |

Sub-regional `Cuisine` labels add detail: Mughlai 403, Mangalorean 378, Hyderabadi 368, Kashmiri 247,
Chettinad 237, Awadhi 145, Konkani 98, Malvani 11, Garhwali 1, Naga 2, Indo-Chinese 868.

**Non-Indian cuisine labels (`Cuisine`)**, mapped to countries: American 12,718 → [[United States]] · Italian 978 →
[[Italy]] · British 950 → [[United Kingdom]] · Chinese 692 → [[China]] · French 650 → [[France]] · Thai 484 →
[[Thailand]] · Mexican 467 → [[Mexico]] · Japanese 118 → [[Japan]] · Spanish 115 → [[Spain]] · Greek 107 →
[[Greece]] · Korean 96 → [[South Korea]] · Vietnamese 93 → [[Vietnam]] · Malaysian 65 → [[Malaysia]] · German 63 →
[[Germany]] · Indonesian 46 → [[Indonesia]].
Region-level labels: Middle Eastern 388 (→ Middle East), Mediterranean 169, European 303, Asian 346,
African 104, International 2,307, Continental 2,025.
Sindhi (Region 306 / Cuisine 180) is the cuisine of Sindh, now in [[Pakistan]], as cooked by the Sindhi
diaspora in India. It is listed under Pakistan with that caveat.

## Ingredients, amounts, cooking method
- **Ingredients: yes**, parsed and normalised to English/Roman (927 ingredient nodes in the KG).
- **Amounts: yes.** Every ingredient row has `quantity`/`unit` where the source stated one and an estimated
  `grams`, with a confidence tier. About 32% of rows are tier D/E (default weights).
  Example: *Aval Payasam* (Kerala, hebbarskitchen) = ghee 2 tbsp (27 g), coconut 2 tbsp (30 g), raisins 2 tbsp
  (20 g), cashew 14.6 g, poha 1 cup (156 g), moong dal ½ cup (78 g), milk 1 litre (1,000 g), jaggery 1 cup
  (144 g), cardamom ½ tsp (1.05 g). That gives 642 kcal per dish, 245 kcal/100 g, HealthGrade D, tags
  `hypertension_friendly, pregnancy_friendly, renal_caution, high_energy`.
- **Cooking method: tags** (`CookingMethod`, 11 method nodes, e.g. `boiled;roasted`). The step text is
  withheld; only `StepCount` is given.
- **Nutrition: yes**, 33 nutrients per dish plus per-100 g values, FSA lights, glycaemic load and % daily values.

## Inferring effects on the body
`body_effect: linkable`. Recipe-level tags (`HealthConditions`, KG `suitable_for` → 13 `condition` nodes such as
weight_loss, low_cholesterol, renal_caution) are **rule-based on estimated nutrients**, not evidence of effect.
The compound route: ingredient → `has_compound` → FlavorDB compound with `pubchem_id` (e.g. thiamine = CID
1130; 3,4-dihydroxybenzoic acid = CID 72) → [[FooDB]], [[CTD]] or [[IMPPAT]] for targets and disease links.
These are flavour compounds only (1,607), not a full phytochemical profile.

## Linking to other datasets
- **PubChem CID** (compound nodes) → [[FlavorDB2]], [[FooDB]], [[PubChem]], [[IMPPAT]], [[CTD]].
- **FoodOn ids** (`foodclass::FOODON_…`) → [[FoodKG]] and other FoodOn-grounded resources.
- **Nutrition source**: USDA SR Legacy (97.5% of composition rows) plus the 198 UK/US rows from
  [[Indian Nutrient Databank (INDB)]] → [[USDA FoodData Central]]. It does *not* use
  [[Indian Food Composition Tables (IFCT 2017)]] (the README says this explicitly).
- **Upstream recipe sources** include the 3A2M corpus and the TarlaDalal dataset, which overlap with
  [[6000+ Indian Food Recipes]], [[RecipeNLG]] and [[Indian Food 101]]. Deduplicate before combining.

## Versions
Semantic-versioned releases, with a detailed `CHANGELOG.md` and `docs/VERSIONS.md`. The concept DOI
10.5281/zenodo.22512534 resolves to the latest Zenodo snapshot, **0.9.0** (2026-09-13, 379 MB zip). GitHub `main`
is at **0.10.0** (2026-09-20), which re-sourced 58 recipes whose text belonged to another dish and applied
owner-reviewed allergen corrections (46 false positives removed). 0.7.0 replaced the synthetic interaction
sets (incompatible ids). The internal master went from 224,003 rows (v6–v14) to 220,188 (v15, non-recipe pages
removed) to 219,384 now.

## Caveats
- **`Pan-Indian` is 61.5% of recipes and means "unlabelled".** Many state labels are inferred
  (`region_inferred`). Use only state-level rows for cultural work, as the authors advise.
- **Nutrition is USDA-grounded (Western composition values)**, even though the schema is the IFCT one.
  Per-ingredient weights are often defaults (tiers D/E).
- Allergen `unknown` must not be read as "safe". Health tags are heuristic.
- Some labels look noisy. For example, 83,952 recipes are tagged `Vegan`, which is implausibly high for Indian
  cuisine where ghee, milk and curd are common. Check before using.
- The interaction log (not downloaded) is **synthetic**.
- There is no peer-reviewed paper yet (Zenodo/GitHub dataset only).
- CC BY-NC-SA: non-commercial, share-alike.
