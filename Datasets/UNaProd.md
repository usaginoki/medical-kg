---
title: "UNaProd"
slug: unaprod
kind: [ingredient]
version: "1.2 Beta (website, 3,413 monographs; accessed 2026-09-30)"
previous_versions: "1.0 (Naghizadeh et al. eCAM 2020: 2,696 monographs, then at jafarilab.com/unaprod; the site's 'Old Version' link)"
papers: ["[[Naghizadeh2020 - UNaProd Iranian traditional medicine materia medica database]]"]
url: "https://unaprod.com/"
license: "not stated (paper: 'freely available to all users with no restriction'; © 2020 UnaProd)"
availability: open-web
access_link: "https://unaprod.com/database"
accessed: partial
access_method: [scrape, api]
access_date: 2026-09-30
access_notes: "No bulk download, no GitHub/Zenodo release found. The site's DataTables backend (POST /databasetable, with the page's CSRF token) returned the full monograph index in 4 requests: 3,413 rows × ID, DrugName, Pronunciation, Origin, Status, MizajType. The per-monograph JSON endpoint (GET /databasedetail/<ID>, used by the page's JavaScript) returns all 16 attributes plus IrGO and CMAUP links; we fetched 38 monographs at 1 req/s (22 well-known herbs/spices/foods plus 16 evenly spaced herbal entries). A full crawl would be ~3,413 requests (about 1 hour at 1 req/s); not done, so accessed = partial. jafarilab.com/unaprod now redirects to the lab homepage."
countries: ["[[Iran]]"]
regions: ["[[Middle East]]", "[[South Asia]]"]
n_records: "3,413 monographs (2,516 herbal, 426 animal, 349 mineral, 116 compound, 6 unidentified); full index downloaded, 38 full monographs"
size: "0.6 MB (CSV)"
formats: [csv, json]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Each monograph gives traditional (Persian medicine) claims: Mizaj (temperament: hot/cold × wet/dry with degree 1–4), actions (ActionType, e.g. Diuretic, Galactagogue, Carminative), target organs, diseases treated (DiseaseType, mapped to IrGO terms), adverse effects, corrective agent (Refinement), dose and substitute. Herbal monographs link by scientific name to CMAUP plant pages, which gives a route to compounds and targets."
join_keys: [scientific name, CMAUP plant id, IrGO id, Persian name, English common name]
topics: [cultural-food-health]
questions: [Q2]
relevance: core
found_by: [search/ingredients, search/compounds, search/regions]
tags:
  - type/dataset
  - kind/ingredient
  - q/2
  - access/accessed
  - access/open
  - region/middle-east
  - tradmed/persian
  - tradmed/unani
---
# UNaProd

> [!abstract] TL;DR
> UNaProd (Universal Natural Product Database) is a database of the **materia medica of Iranian (Persian)
> traditional medicine**, built by the School of Persian Medicine at Tehran University of Medical Sciences
> (Jafari and Karimi labs). It text-mines and manually curates *Makhzan al-Advieh* (Mohammad Hossein Aghili
> Khorasani, 1769 CE), the latest and largest classical Persian drug encyclopedia. The live site (v1.2 Beta)
> holds **3,413 monographs**: herbs, animal products, minerals and compound drugs. Each has up to 16 attributes:
> **Mizaj (temperament) type and degree, actions and medicinal uses, adverse effects, refinement (corrective),
> substitute, dosage**, synonyms in ~70 languages, and scientific and common names. Many entries are everyday
> foods and spices of the region (saffron, black seed, fenugreek, cumin, pomegranate, dates, garlic, onion,
> olive, walnut). It is the only structured source we have for the **hot/cold food-temperament beliefs** that
> shape dietary advice in Iran and, through Unani medicine, in South Asia (Q2).

## Access
| | |
|---|---|
| Availability | open web only (browse/search, 7 interface languages: English, Persian, Arabic, Chinese, Kannada, Hindi, Urdu); no bulk download |
| Link | https://unaprod.com/database |
| Accessed? | partial: full index (3,413 rows) + 38 complete monographs |
| How | The page's own JSON endpoints: `POST /databasetable` (DataTables server-side, CSRF token from the page, `length=1000`, 4 requests) and `GET /databasedetail/<ID>` (one monograph per request, 1 req/s) |
| Downloaded | `Data/unaprod/unaprod_drug_list.csv` (index), `Data/unaprod/unaprod_monographs_sample.csv` (38 monographs, 28 flattened columns) |

## Tables & columns
Field meanings come from the paper (Section 3) and the site's field labels.

### `unaprod_drug_list.csv` (3,413 rows): index of all monographs
| column | type | meaning | example |
|---|---|---|---|
| `ID` | int | UNaProd monograph id (URL `database/<ID>`) | 1012 |
| `DrugName` | str | Persian/Arabic name as in *Makhzan al-Advieh* | شونیز |
| `Pronunciation` | str | IPA transcription (76% filled) | ʃoniz |
| `Origin` | str | herbal 2,516 / animal 426 / mineral 349 / compound 116 / unidentified 6 | herbal |
| `Status` | – | always empty | |
| `MizajType` | str | temperament type(s), `;`-joined when several scholars disagree (59% filled; Hot-and-Dry 1,301, Cold-and-Dry 396, Hot-and-Wet 178, Cold-and-Wet 137, Hot 97, Morakkab al-Ghovaa 57…) | Unbalanced Hot And Dry Mizaj |

### `unaprod_monographs_sample.csv` (38 rows): full monographs
| column | type | meaning | example (black seed, ID 1012) |
|---|---|---|---|
| `ID`, `DrugName`, `Pronunciation`, `Origin` | | as above | 1012, شونیز, ʃoniz, herbal |
| `Commonname` | str | English common name (from the corrected edition's appendix) | Black cumin |
| `SciName1`, `SciName1_link` | str | scientific name from SciResource1 (Ghahreman & Okhovvat) and its CMAUP plant-page link when matched | Nigella sativa |
| `SciName2`, `SciName2_link` | str | scientific name(s) from SciResource2 (corrected edition), often with synonyms and family | Pimpinella anisum L. (Apiaceae) Syn: … |
| `MizajType`, `MizajType_IrGO` | str | temperament type and IrGO ontology id | Unbalanced Hot And Dry Mizaj, IrGO_0003963 |
| `MizajDegree` | str | degree of each quality (First–Fourth; DNS = degree not specified) | DryThird; HotThird |
| `ActionType`, `ActionType_IrGO` | str | pharmacological actions (English IrGO terms) | Heating; Drying; Theriac; Diuretic; Galactagogue; Emmenagogue; Lithontriptic; … |
| `OrganType` | str | organs/body fluids acted on | urine; milk; menstruation; stomach; kidney; … |
| `DiseaseType`, `DiseaseType_IrGO` | str | conditions treated (English, with transliterated ITM terms such as *Nazleh*, *Qoulanj*) | nausea; long-term fever; cough; dropsy; jaundice; kidney stone; … |
| `WeightType` | str | dose units used (Dirham, Miskal, Dam, Danar…) | Dirham |
| `CommonName2` | str | Persian/Arabic common name | سياه دانه |
| `TextExpression` | str | Persian text: pronunciation and naming remarks | به ضم شین و سکون واو … |
| `Synonyms` | list | names in other languages as `language: name` | 'عربی: حبه السودا' (Arabic), 'یونانی: سنو' (Greek), 'هندی: کلونجی' (Hindi *kalonji*) |
| `TextIdentity` | str | Persian text: what the drug is, varieties, where it grows | تخم نباتی است شبیه به رازیانه … |
| `TextMizaj` | str | Persian text of the temperament statement | در سوم گرم و خشک |
| `EffectsAndMedicinalUses` | str | Persian text: actions and uses by organ system | مسخن و مجفف رطوبات … جهت سرفه بارده و درد سینه … |
| `AdverseEffect` | str | Persian text: who or what organ it harms | مضر گرده (harmful to the kidney) |
| `Refinement` | str | Persian text: corrective to counter the harm | مصلح آن کثیرا (corrected by tragacanth) |
| `Dosage` | str | Persian text: dose, sometimes lethal dose | تا دو درم در مبرودین و در محرورین تا نیم درم (up to 2 dirhams for cold-tempered people, ½ dirham for hot-tempered) |
| `Substitute` | str | Persian text: replacement drug and proportion | بدل آن انیسون و نصف وزن آن تخم شبت (anise, or half its weight of dill seed) |

Site-wide fill rates (statistics page, 3,413 rows): Identity 2,581; Mizaj 2,044; Actions & Medicinal Uses
2,610; Adverse effect 1,114; Refinement 912; Dosage 712; Substitute 459; SciName1 646; SciName2 376.

Sample: `Data/unaprod/sample.csv` · full profile: `Data/unaprod/schema.md`

## Countries & cultures covered
- **[[Iran]]**: the source is the canonical Persian (Iranian traditional medicine, ITM) materia medica. The
  same Greco-Arabic humoral tradition underlies **Unani** medicine, practised today in India and Pakistan, so
  the Mizaj and action labels also bear on [[South Asia]]. This is why `regions` includes South Asia. The
  database itself has no per-country labels.
- **Synonym languages** show the cultural reach of each drug. The paper says about 70 languages and dialects
  are used, mostly Persian, Arabic, "Indian" and Greek. In our 38 monographs the tags were: Hindi (هندی) 28,
  Persian 17, Greek (یونانی) 12, Syriac 8, Arabic 8, Rumi/Byzantine 7, Turkish 4, plus Isfahani, Shirazi,
  Gilaki, Shami (Levantine), Sindhi, Bengali and Frankish.
- `TextIdentity` often names the places a drug comes from (per the paper). It is free Persian text and was not
  extracted.

## Inferring effects on the body
`body_effect: direct`, as **traditional claims** (classical text, 1769, with earlier scholars quoted). This is
not clinical evidence.
- **Mizaj**: type and degree predict the effect on a person's temperament. ITM advice pairs food temperament
  with the eater's temperament: the black-seed dose is 2 dirhams for cold-tempered (*mabrudin*) and ½ dirham
  for hot-tempered (*mahrurin*) people. This is the kind of culturally specific rule a diet agent needs.
- **Actions, organs, diseases**: English IrGO-coded lists (e.g. black seed: Diuretic, Galactagogue,
  Emmenagogue, Lithontriptic; cough, chest pain, dropsy, jaundice, kidney/bladder stone, headache).
- **Adverse effects + Refinement + Substitute**: harms and their correctives (black seed: harmful to the kidney,
  corrected by tragacanth; excess causes throat swelling in hot-tempered people, corrected by soaking in
  vinegar).
- **Route to compounds**: `SciName1_link` / `SciName2_link` point to [[CMAUP]] plant pages, e.g. saffron →
  `NPO9445` (*Crocus sativus*). From there, [[CMAUP]] and [[NPASS]] give ingredients (crocin, safranal), targets
  and measured activity.

Example, saffron (ID 827, *Crocus sativus*): Mizaj Unbalanced Hot And Dry. Actions include Elating,
Intoxicating, Nauseating, Weakening of food appetence. Diseases include brain obstruction, spleen obstruction,
difficult delivery, alcohol withdrawal. Persian uses begin "مفرح قوی" (strong exhilarant). The adverse effect is
"مضر گرده و مضعف اشتها و مغثی" (harms the kidney, weakens appetite, nauseating).

## Linking to other datasets
- **CMAUP plant links** (built into the monographs) → [[CMAUP]] → [[NPASS]] (shared NPO/NPC ids) for
  compounds, targets, diseases and composition.
- **Scientific name** → [[Dr. Duke's Phytochemical and Ethnobotanical Databases]] (e.g. *Nigella sativa* folk
  uses in Iraq and Turkey), [[IMPPAT]] (Unani/Ayurvedic uses in India), [[FooDB]].
- **Persian/Arabic/English common names** → food datasets for the Middle East, such as
  [[Saudi Food Composition Tables]], [[Bahrain Food Composition Tables]] and [[ArabCulture]]. The name matching
  is manual.
- **IrGO ids** → the IrGO ontology (ir-go.net) for English definitions of ITM concepts.

## Versions
| | 1.0 (paper, 2020) | **1.2 Beta (site, 2026-09-30)** |
|---|---|---|
| monographs | 2,696 (1,741 primary + secondary tuples) | **3,413** |
| with Mizaj | 1,976 | 2,044 |
| with scientific name | 1,822 in total / 851 in the statistics figure | SciName1 646, SciName2 376 |
| interface | Persian/English | 7 languages; interactive Mizaj plot; comparison page |

There is no published changelog. Compared with the paper, we observed 717 more monographs and IrGO-coded
English lists of actions, organs and diseases in the monograph JSON. The 2020 paper had listed English IrGO
linking as future work; it only had Mizaj linked to IrGO.

## Caveats
- **Not downloadable**: the full data need a crawl of 3,413 JSON pages. We have the full index and 38 full
  monographs. Ask the lead whether to run the full crawl (≈1 h at 1 req/s).
- The core text fields are **classical Persian** (18th-century register, Arabic medical vocabulary). Only the
  IrGO-coded fields (Mizaj, actions, organs, diseases) are in English.
- Scientific-name coverage is limited (646 + 376 of 3,413) and mappings of historical names are uncertain,
  e.g. SciName2 for شیرخشت lists several candidate genera.
- These are traditional claims from 1769, not evidence. Some are unsafe (abortifacients, "lethal toxin",
  opium poppy as narcotic).
- Some DiseaseType terms are transliterated ITM concepts with no biomedical equivalent (*Sadar*, *Khonnaq*,
  *Nazleh*).
