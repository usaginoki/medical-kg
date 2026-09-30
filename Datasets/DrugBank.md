---
title: "DrugBank"
slug: drugbank
kind: [compound]
version: "DrugBank 6.0 knowledgebase (NAR 2024); download release 5.1.22 (2026-06-27)"
previous_versions: "DrugBank 5.0 (NAR 2018; 1,195 drug–food interactions); download releases 5.1.x up to 5.1.21"
papers: ["[[Knox2024 - DrugBank 6.0]]"]
url: "https://go.drugbank.com"
license: "Full database CC BY-NC 4.0 (free academic account); DrugBank Vocabulary and Open Structures CC0"
availability: registration
access_link: "https://go.drugbank.com/releases/latest"
accessed: partial
access_method: [scrape]
access_date: 2026-09-30
access_notes: "No account was registered. Every release download returned 403 'Forbidden. Academic downloads are currently disabled.' This included the CC0 Open Data vocabulary (all-drugbank-vocabulary) and open structures, which normally need no login. Public drug pages (Cloudflare JS challenge; loaded in a real browser via Playwright) are now teaser cards: IDs, mechanism, indication and targets, but no Food Interactions section (sign-in wall). Sample kept: 12 public drug cards (scraped 1.2 s apart) and the 2,784 DrugBank-derived food-interaction rows redistributed inside [[DDID]]."
countries: []
regions: ["[[Global]]"]
n_records: "Full DB: 11,891 drugs, 2,475 drug–food interactions (paper). Kept: 12 drug cards; 2,784 food-interaction rows for 525 DrugBank drugs (via DDID)"
size: "Full XML 204 MB zip (not downloaded); kept 0.7 MB"
formats: [xml, csv, sdf, json]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: direct
body_effect_how: "`food-interactions` = curated advice sentences per drug (avoid grapefruit / take with food / avoid licorice → hypokalaemia); plus targets, enzymes, transporters, indications, pathways per drug"
join_keys: [DrugBank ID, PubChem CID, InChIKey, ChEBI ID, ChEMBL ID, UNII, CAS, KEGG, ATC, RxNorm, UniProt]
topics: [cultural-food-health]
questions: [Q3]
relevance: adjacent
found_by: [search/compounds]
tags:
  - type/dataset
  - kind/compound
  - q/3
  - access/blocked
  - access/registration
  - region/global
---
# DrugBank

> [!abstract] TL;DR
> DrugBank (University of Alberta / OMx) is the reference drug knowledgebase. **DrugBank 6.0** covers 11,891 drugs and 1.41 M drug–drug interactions. It also has **2,475 drug–food interactions**, which are short curated advice sentences per drug such as "Avoid grapefruit products" or "Avoid licorice in large amounts (hypokalaemia)". For the agent, this field is the canonical, citable answer to "can I take drug X with food Y?", and DrugBank IDs are the hub linking [[DDID]], [[FooDrugs]] and PubChem.
>
> **We could not download it.** A free account is needed for the full data, and on 2026-09-30 even the CC0 open vocabulary returned "Academic downloads are currently disabled". Public pages no longer show food interactions. Our sample is 12 public drug cards plus 2,784 DrugBank food-interaction rows (525 drugs) that [[DDID]] redistributes.

## Access
| | |
|---|---|
| Availability | registration (free academic account; full DB CC BY-NC 4.0). Vocabulary and open structures are CC0 and nominally login-free |
| Link | https://go.drugbank.com/releases/latest (release 5.1.22, 2026-06-27) |
| Accessed? | partial. Sample only |
| How | 1) `curl` of `releases/5-1-22/downloads/all-drugbank-vocabulary` and `.../all-open-structures`: HTTP 403 "Academic downloads are currently disabled". 2) `curl` of `/drugs/DB00682`: 403 Cloudflare JS challenge. 3) Playwright browser: 12 drug pages fetched 1.2 s apart; they render only a teaser card, and "Food Interactions" does not appear on any of them. 4) DrugBank-sourced rows extracted from [[DDID]] |
| Downloaded | `Data/drugbank/public_drug_cards.csv` (12 drugs), `public_drug_pages_raw.json` (page text), `food_interactions_via_ddid.csv` (2,784 rows) |

> [!warning] Needs user
> The full data needs a DrugBank academic account: https://go.drugbank.com/releases/sign_up. Then download `https://go.drugbank.com/releases/5-1-22/downloads/all-full-database` (XML, 204 MB zip, contains `<food-interactions>`) and `.../all-drugbank-vocabulary` (CSV) into `Data/drugbank/`. Academic downloads may still be disabled even with an account.

## Tables & columns
### `food_interactions_via_ddid.csv` (2,784 rows)
These are the rows of [[DDID]] `interaction_information.csv` with `Relationship_classification = Drugbank`. DDID parsed them from the DrugBank dump and mapped each advice sentence to one or more foods or herbs.

| column | type | meaning | example |
|---|---|---|---|
| `drugbank_id` | str | DrugBank accession, taken from `Reference` (525 drugs) | DB00695 |
| `Drug_Name` | str | drug | Furosemide |
| `Food_Herb_Name` | str | food or herb DDID mapped the sentence to (182 distinct): Meal 340, Alcohol 156, Licorice 154, tea (*Camellia sinensis*) 156, Garlic 44, Ginger 44, Grapefruit 39… | Licorice |
| `Type` | str | Food / Herb | Herb |
| `Component` | str | constituent, if named (tyramine, vitamin C, furanocoumarins…) | Tyramine |
| `Result` | str | the DrugBank food-interaction sentence (391 distinct) | "Avoid licorice in large amounts, as it may lead to hypokalemia." |
| `Effect` | str | DDID grade: Possible 2,040 · Positive 549 · Negative 119 · No Effect 76 | Possible |
| `Conclusion` | str | short advice | "Take with foods containing vitamin C." |
| `Reference` | str | DrugBank drug URL | https://go.drugbank.com/drugs/DB00695 |

### `public_drug_cards.csv` (12 rows)
One row per public teaser card: warfarin, atorvastatin, simvastatin, felodipine, cyclosporine, tacrolimus, levothyroxine, metformin, ciprofloxacin, curcumin, glycyrrhizic acid, EGCG.

| column | type | meaning | example |
|---|---|---|---|
| `drugbank_id`, `name` | str | accession, name | DB13751, Glycyrrhizic acid |
| `header_tags` | str | groups, type and categories run together with the start of the description (scraped text) | ApprovedInvestigationalSmall molecule… |
| `mechanism`, `primary_indication` | str | first 800 chars of the mechanism; indication | "Glycyrrhizic acid is widely applied in foods as a natural sweetener." |
| `formula_weight`, `first_approval`, `also_known_as` | str | | C42H62O16 · 822.942 g/mol |
| `UNII`, `CAS`, `ChEMBL`, `ChEBI`, `PubChem`, `KEGG`, `RxNorm`, `ATC`, `PharmGKB`, `InChIKey`, `SMILES` | str | cross-references ("Resolves to" box) | 6FO62043WK, CHEMBL441687, A05BA08 |
| `Targets`, `Transporters`, `Enzymes` | str | UniProt accession + gene symbol, concatenated | P28845HSD11B1 |
| `n_drug_interactions_listed` | str | DDI count shown (details behind login) | 89 |
| `food_interactions_section_visible` | bool | whether a Food Interactions section was on the public page (always False) | False |

Sample: `Data/drugbank/sample.csv` · full profile: `Data/drugbank/schema.md`

## Countries & cultures covered
None. It is a global drug resource (`countries: []`). The DrugBank 6.0 product data covers regulators in the US, Canada, EU, Austria, Italy, **Turkey**, Colombia, **Indonesia**, **Malaysia**, **Thailand** and **Singapore**. That covers marketed products, not diet.

## Inferring effects on the body
**Direct.** The `food-interactions` element is curated advice about the effect of food on a drug. Each drug also has targets, enzymes (CYP3A4, …), transporters and indications, which give the mechanism. Evidence type: curator-written statements distilled from labels and literature, with no per-sentence citation or grade.

Examples for priority-region foods (from `food_interactions_via_ddid.csv`):
- **Liquorice** (154 rows). Furosemide DB00695: "Avoid licorice in large amounts, as it may lead to hypokalemia." Propranolol DB00571: "Natural licorice inhibits the metabolism of propranolol, increasing drug exposure." Amlodipine DB00381: "Avoid natural licorice."
- **Grapefruit** (39 rows). Bortezomib DB00188: "Grapefruit inhibits CYP3A4 metabolism, which may increase the serum concentration of bortezomib." Cabergoline DB00248 is similar.
- **Tea / caffeine** (≈156 rows). Lorazepam DB00186: "Limit caffeine intake."
- **Garlic, ginger, ginseng** (44 / 44 / 35 rows). Lepirudin DB00001: "Avoid herbs and supplements with anticoagulant/antiplatelet activity. Examples include chamomile, garlic, ginger, ginkgo and ginseng."
- **Dairy**. Valproic acid DB00313: "Avoid milk and dairy products."
- Turmeric, fenugreek, dates and pomegranate have **no** DrugBank food-interaction rows in this subset. For those foods, use [[DDID]] literature rows or [[FooDrugs]].

The public cards confirm the mechanism layer. For example, glycyrrhizic acid DB13751 lists the targets TNF, CASP3, LPL and HSD11B1, and curcumin DB11672 lists ABCB1 (P-gp) as a transporter.

## Linking to other datasets
- **DrugBank ID** is the hub. [[DDID]] `drug_information.DrugBank_ID` covers 1,475 of 1,516 drugs, and [[FooDrugs]] `texts.link` has 285 DrugBank documents.
- Public cards and the vocabulary give PubChem CID, InChIKey, ChEBI, ChEMBL, UNII, CAS, ATC and RxNorm. These join to any compound resource (FooDB, PubChem-keyed phytochemical DBs).

## Versions
- **DrugBank 6.0** (Knox et al., NAR 2024): drug–food interactions went from 1,195 to 2,475, DDIs from 365,984 to 1,413,413, and approved drugs from 2,646 to 4,563. New drug–food interaction checker.
- The download releases continue the numbering 5.1.x. The latest is **5.1.22 (2026-06-27)**. The web cards say "as of September 23, 2026".
- **DrugBank 5.0** (2018) had 1,195 food interactions. [[DDID]] cites that figure, but its 2,784 DrugBank rows suggest it parsed a newer dump.

## Caveats
- Access is gated and was disabled at the time we checked. The redistributed DDID rows are a lossy remapping: one sentence is copied to every plausible food (e.g. caffeine advice attached to *Fructus Evodiae*), and drugs without a DDID-mapped food are missing.
- The food interactions are advice sentences with no food IDs, dose, evidence level or citation.
- CC BY-NC: non-commercial use only.
