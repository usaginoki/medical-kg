---
title: "DDID"
slug: ddid
kind: [compound, ingredient]
version: "web release accessed 2026-09-30 (content as described in Hong et al. 2024: 23,950 interactions)"
previous_versions: ""
papers: ["[[Hong2024 - DDID diet-drug interactions]]"]
url: "https://bddg.hznu.edu.cn/ddid/"
license: "Free download, no login; no explicit data licence on the site (paper is CC BY 4.0)"
availability: open-download
access_link: "https://bddg.hznu.edu.cn/ddid/download/"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "All 7 CSVs from the download page, fetched with curl and a browser User-Agent. The server is very slow: `NP Information.csv` timed out once, was reset mid-transfer (curl 56), and completed with `curl -C -` resume."
countries: ["[[China]]"]
regions: ["[[Global]]", "[[East Asia]]"]
n_records: "23,950 interactions; 1,516 drugs; 270 foods; 1,068 herbs; 43,668 herb–compound rows; 1,356 drug–target rows; 1,694 drug–indication rows"
size: "27 MB"
formats: [csv]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: direct
body_effect_how: "Each row is a food/herb × drug experiment with Result (PK numbers or outcome), Effect class (Positive/Negative/No Effect/Harmful/Possible), Potential_Target (CYP3A4, P-gp, OATP…) and a PMID/FDA-label/DrugBank citation; herbs carry TCM Function/Indication/Toxicity"
join_keys: [DrugBank ID, PubChem CID, InChIKey, ChEBI ID, TTD ID, FooDB id, NCBI taxon, scientific name, HERB id, SymMap id, NPASS id, UniProt, PMID]
topics: [cultural-food-health]
questions: [Q3, Q2]
relevance: core
found_by: [search/compounds]
tags:
  - type/dataset
  - kind/compound
  - kind/ingredient
  - q/3
  - q/2
  - access/accessed
  - access/open
  - tradmed/tcm
  - region/east-asia
  - region/global
---
# DDID

> [!abstract] TL;DR
> The Diet-Drug Interactions Database (Hangzhou Normal Univ. / Zhejiang Univ., *Brief Bioinform* 2024) is a manually curated table of **23,950 food/herb–drug interaction records**. It covers 1,516 drugs, 270 foods and meal types, and 1,068 herbs, most of them Chinese materia medica with Pinyin/Chinese names and TCM properties. Each record gives the dose, the species, the PK result, an **effect grade** (positive, negative, no effect, harmful, possible), the target (CYP/P-gp/OATP) and a PMID, FDA label or DrugBank reference. For the agent it answers a practical question: *"I eat X every day (grapefruit, liquorice, green tea, turmeric, fenugreek, black seed, dates, jujube, ginseng) and take drug Y. Should I worry?"* It includes the 2,784 DrugBank food-interaction statements, which makes it our open proxy for DrugBank's gated field.

## Access
| | |
|---|---|
| Availability | open-download (7 CSVs on the Download page, no login) |
| Link | https://bddg.hznu.edu.cn/ddid/download/ |
| Accessed? | yes. All 7 files |
| How | `curl -L -A "<browser UA>" "https://bddg.hznu.edu.cn/ddid/static/download/<X>%20Information.csv"` |
| Downloaded | `Data/ddid/`: `interaction_information.csv` (18.4 MB), `drug_information.csv`, `food_information.csv`, `herb_information.csv`, `target_information.csv`, `disease_information.csv`, `np_information.csv` (≈27 MB total) |

The site's HTTP server is very slow and drops connections, but it does not block downloads.

## Tables & columns
### `interaction_information.csv` (23,950 rows)
One row per (drug, food/herb, experimental condition). 26 columns.

| column | type | meaning | example |
|---|---|---|---|
| `Drug_ID` | str | DDID drug id → `drug_information.FHDI_Drug_ID` | D00572 |
| `Drug_Name` | str | drug name | Simvastatin |
| `Brand_Name` | str | brand (21% filled) | FARYDAK (panobinostat) |
| `Drug_Dose` / `Dosage_Form` | str | drug dose and route | 100 mg / Oral |
| `Food_Herb_ID` | str | F… → `food_information`, H… → `herb_information` | F00001 |
| `Food_Herb_Name` | str | food, herb or meal type (1,385 distinct strings) | Pomegranate |
| `Type` | str | `Food` (4,865) or `Herb` (19,085) | Food |
| `Component` | str | active constituent, if named (84% filled) | Glycyrrhizin |
| `Dose` / `Note` / `Time` | str | food/herb dose, preparation (juice, extract), timing | 900 ml/d / Juice / 3 days pretreatment |
| `Result` | str | quantitative outcome (AUC, Cmax, INR…) or a text statement | "Cmax … AUC0-t (95% CI) = 128%…" |
| `Experimental_Species` | str | Rat 12,335 · Homo Sapiens 3,647 · Rabbit 893 · Dog 334 · Mice 277… | Homo Sapiens |
| `Experimental_Design` / `Experimental_Individuals_Number` | str/int | trial design and n | Open-label, randomized / 12 |
| `Test_Method` / `Test_Sample` | str | assay and matrix | HPLC / Plasma |
| `Effect` | str | graded effect: Possible 17,827 · No Effect 2,374 · Positive 1,915 · Negative 1,437 · Harmful 393 (+4 lower-case "possible") | Harmful |
| `Potential_Target` / `Target_ID` | str | enzyme/transporter mediating it; UniProt id | CYP2C9 / P11712 |
| `Conclusion` | str | curated one-line conclusion | "pomegranate juice … had no effect on CYP2C9 activity" |
| `PMID` / `Reference` / `DOI` | str | citation (PMID 77% filled; DrugBank or FDA URLs for label-derived rows) | 23047652 |
| `Relationship_classification` | str | source class: HFDI (literature) 17,670 · Drugbank 2,784 · FDI-Package Insert 1,666 · Dietary Effect-Package Insert 1,009 · Dietary effects 821 | HFDI |

"Positive" and "Negative" mean the drug's exposure or efficacy went up or down (bioequivalence outside 80–125%), not good or bad for the patient. "Harmful" marks adverse clinical events.

### `drug_information.csv` (1,516 rows)
`FHDI_Drug_ID`, `Drug_Name`, `Synonyms`, `Drug_Type` (1,363 small molecules), `Company`, `Summary` (one-line use), `Formula`, `Canonical_SMILES`, `InChI`, `InChIKey`, `TTD_ID`, `DrugBank_ID` (98% filled, 1,475 unique), `PubChem_Compound_ID`, `PubChem_Substance_ID`, `ChEBI_ID`, `CAS_Number`, `ADReCS_Drug_ID` (adverse-reaction DB).

### `food_information.csv` (270 rows)
| column | type | meaning | example |
|---|---|---|---|
| `FHDI_Food_ID` | str | id | F00235 |
| `Food_Name` / `Scientific_Name` / `Common_Name` | str | names | Date / Phoenix dactylifera |
| `Description` | str | encyclopaedic description | "The pomegranate … is used in cooking, baking, juices…" |
| `Group` / `Subgroup` | str | FooDB-style group: Fruits 61, Vegetables 49, Food combination 44 (meal types), Spices 22… | Fruits / Tropical fruits |
| `ITIS_ID`, `FoodB_ID`, `DTU_ID`, `Taxonomy_ID` | id | links to ITIS, FooDB (68%), DTU Frida, NCBI Taxonomy | FOOD00135 |
| `Superkingdom` … `Genus` | str | NCBI lineage | Arecaceae / Phoenix |
| `Drug homologous food` | str | note if on China's "medicine-food homology" list (15%) | "Pepper is one of the commonly used seasonings…" |

### `herb_information.csv` (1,068 rows)
| column | type | meaning | example |
|---|---|---|---|
| `FHDI_Herb_ID` | str | id | H00001 |
| `Herb_Latin_Name` / `Herb_English_Name` / `Herb_Pinyin_Name` / `Herb_Chinese_Name` | str | names (Chinese names 95% filled) | Acacia nilotica / Gum-arabic Tree / A LA BO JIAO JIN HE HUAN / 阿拉伯胶金合欢 |
| `Properties` / `Meridians ` | str | TCM nature/flavour and meridian tropism (≈35%) | Warm; Pungent; Bitter / Spleen; Stomach; Liver |
| `Use_Part` | str | part used | balsam |
| `Function ` / `Indication` | str | TCM function and indications (≈70%) | "To transform concretion and disperse accumulation, kill worms…" |
| `Toxicity ` | str | toxicity class (3%) | Extremely Toxic |
| `Therapeutic_Class` / `Therapeutic _Class_Chinese` | str | TCM class | Food digestion / 消食 |
| `HERB_ID`, `SymMap_ID`, `NPASS_ID`, `Taxonomy_ID` | id | links to HERB, SymMap, NPASS, NCBI Taxonomy | HERB000018 |
| lineage + `Drug homologous food` | str | taxonomy; food–medicine homology note (8%) | Fabaceae |

(Several column names have trailing spaces in the file: `Meridians `, `Function `, `Toxicity `.)

### `np_information.csv` (43,668 rows)
Herb → natural-product constituents, taken from NPASS. It covers 681 herbs and 20,309 distinct compounds.

| column | type | meaning | example |
|---|---|---|---|
| `org_id` | str | NPASS organism id (= `herb_information.NPASS_ID`) | NPO30143 |
| `np_id` | str | NPASS compound id | NPC220825 |
| `FHDI_Herb_ID` | str | herb | H00001 |
| `SMILES`, `pref_name`, `pubchem_cid` (98% filled), `Molecular_Weight` | | compound structure, name, PubChem CID, MW | Epigallocatechin, 72277, 306.27 |

For example, liquorice/*Glycyrrhiza* herbs have 958 constituent rows (formononetin, licoagroisoflavone, quercetin…), *Nigella* 14, ginseng 89. Turmeric is a *food* in DDID and has no constituent rows here.

### `target_information.csv` (1,356 rows) · `disease_information.csv` (1,694 rows)
Target rows: `TTD_ID`, `Target_ID`, `Target_Name` (e.g. P2Y purinoceptor 12 (P2RY12)), `Highest_status`, `MOA(Mechanisms of Action)`, `FHDI_Drug_ID`. These are the drugs' therapeutic targets from TTD. Disease rows: `TTD_ID`, `Indication` (with ICD-11 code, e.g. "Constipation [ICD-11: DD91.1]"), `State`, `FHDI_Drug_ID`.

Sample: `Data/ddid/sample.csv` · full profile: `Data/ddid/schema.md`

## Countries & cultures covered
The rows carry no country labels. The data is about foods and herbs, not populations.
- **China / TCM**: 1,016 of 1,068 herbs have Chinese, Pinyin and HERB ids. About a third carry TCM properties and meridians, and some are flagged as "medicine-food homology" items (China NHC list). The most frequent herbs include TCM materia medica such as Fructus Evodiae, Dan Shen, Semen Oroxyli, Radix Notoginseng and jujube.
- **Middle East / South Asia–relevant foods and spices**: dates, pomegranate, fenugreek, black seed (*Nigella sativa*), turmeric, liquorice, cinnamon, saffron-type spices, green and black tea, hibiscus tea, yogurt. 
- **Global**: meal types (high-fat meal, standard meal) and alcohol from FDA labels.

So `countries: [[China]]` reflects the TCM herb layer only. There are no per-country record counts.

## Inferring effects on the body
**Direct.** Every row is itself a health-relevant statement: food/herb → drug with a measured PK change, a mechanism and an effect grade. Evidence types:
- **human PK/clinical trials and case reports**: `Experimental_Species = Homo Sapiens`, 3,647 rows, many with AUC/Cmax
- **animal/in-vitro studies**: 13,800+ rows, mostly graded "Possible"
- **label statements**: FDA package inserts (2,675 rows) and DrugBank advice sentences (2,784 rows)

Concrete examples for priority-region diets:

| food/herb (rows) | drug | species | effect | result / conclusion (abridged) | ref |
|---|---|---|---|---|---|
| Grapefruit (397) | Cyclosporine | human | Positive | GFJ 250 ml: Cmax 1,340 vs 936 ng/ml (water); raises oral bioavailability via gut CYP3A | PMID 7768070 |
| Grapefruit | Caffeine | human | Positive | AUC 128% (111–146%); CYP1A2 inhibited but "should not cause clinically significant" effects | PMID 8485024 |
| Liquorice / *Glycyrrhiza* (≈490 across name variants) | Omeprazole | human | Negative | glycyrrhizin 300 mg/d ×14 d lowers omeprazole via CYP3A4 induction | PMID 20350051 |
| Licorice | Cortisone acetate | human | Positive | licorice 24 g raises serum-cortisol AUC | PMID 21896619 |
| Licorice (DrugBank row) | Furosemide | label | Possible | "Avoid licorice in large amounts, as it may lead to hypokalemia" | DrugBank DB00695 |
| Green tea / *Camellia sinensis* (≈300) | Fluorouracil | human cells | Possible | EGCG lowers 5-FU IC50 from 40 to 5 µM in HCT-116 | PMID 30741544 |
| Turmeric (12) | Tacrolimus | human (case) | **Harmful** | worsening oedema, creatinine up to 4.2 mg/dL; curcumin reduces intestinal CYP3A | PMID 28104136 |
| Turmeric | drug listed as "Vitamin K" (an anticoagulation case; likely a vitamin K antagonist, inferred) | human (case) | **Harmful** | INR up to 6.5, no bleeding; curcumin prolongs PT/aPTT | PMID 25230280 |
| Fenugreek (9) | Theophylline | dog | Possible | 25 g fenugreek: Cmax −28%, AUC −22% | PMID 25243874 |
| *Nigella sativa* (6) | Phenytoin | dog | Possible | black seed markedly alters phenytoin disposition | PMID 23401262 |
| Date (3) | Doxorubicin | rat | Possible | *Phoenix dactylifera* extract protects against DOX cardio- and nephrotoxicity | PMID 31929900 |
| Pomegranate (32) | Metformin | human | Possible | + juice lowers liver enzymes and HOMA-IR in T2DM | PMID 35581639 |
| Jujube (74) | Phenacetin | rat | Possible | *Ziziphus jujuba* extract induces CYP1A2 | PMID 26253491 |

The chain to follow is food/herb → `Component` (or all constituents via `np_information`) (e.g. glycyrrhizin, EGCG, furanocoumarins) → `Potential_Target` (CYP3A4, P-gp, OATP1A2) → effect on the drug. `disease_information` then gives the drug's indication, which tells the agent which patient group is affected.

## Linking to other datasets
- **Drugs**: `DrugBank_ID`, `PubChem_Compound_ID`, `InChIKey`, `ChEBI_ID`, `TTD_ID` join to [[DrugBank]] and to any PubChem-keyed compound resource. The 2,784 `Relationship_classification = Drugbank` rows reproduce DrugBank's food-interaction field; a copy with DrugBank IDs is in `Data/drugbank/food_interactions_via_ddid.csv`.
- **Foods**: `FoodB_ID` (179 foods) joins to FooDB; `Taxonomy_ID` and `Scientific_Name` join to NCBI-taxon-keyed ingredient datasets.
- **Herbs**: `HERB_ID`, `SymMap_ID` and `NPASS_ID` join to the TCM databases HERB, SymMap and NPASS. `np_information.pubchem_cid` gives herb → compound (PubChem CID), which can be joined to any compound–target or compound–health resource.
- **Literature**: `PMID` joins to the documents in [[FooDrugs]] `texts` (via its `link` column) for text-mined context.

## Versions
Only one public release. The paper (published May 2024) and the site describe the same 23,950 interactions, and the downloaded interaction file has exactly 23,950 rows. There is no version number or changelog on the site.

## Caveats
- Food/herb names are not normalised. The same item appears under several names: "Licorice" vs "Liquorice" vs "Radix Glycyrrhizae…"; "Green Tea" vs "Camellia sinensis [Syn. Thea sinensis]" vs "Folium camelliae sinensis"; "High-Fat Meal" with and without a trailing space. Group on `Food_Herb_ID` or scientific name.
- DrugBank-derived rows spread one generic sentence over many foods. For example, "Limit caffeine intake" is attached to every caffeine-containing plant (Fructus Evodiae, *Ilex*, coffee species, *Paullinia*), which inflates counts.
- Three quarters of the rows are "Possible", mostly animal studies. Filter to `Experimental_Species = Homo Sapiens` and Effect in {Positive, Negative, Harmful} for clinically actionable advice.
- There is no licence statement for the data.
