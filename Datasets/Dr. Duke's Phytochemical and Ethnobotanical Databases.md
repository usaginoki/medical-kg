---
title: "Dr. Duke's Phytochemical and Ethnobotanical Databases"
slug: dr-dukes-phytochemical-and-ethnobotanical-databases
kind: [ingredient, compound]
version: "Ag Data Commons archival release v1 (2023-11-30); CSV tables last modified Dec 2015 – Jan 2016"
previous_versions: "No versioned predecessors as datasets. The data grew out of J. A. Duke's CRC handbooks (e.g. Handbook of phytochemical constituents of GRAS herbs, 1992) and the USDA-ARS web database (phytochem.nal.usda.gov, still online)."
papers: []
url: "https://phytochem.nal.usda.gov/"
license: "CC0 1.0 (public domain)"
availability: open-download
access_link: "https://agdatacommons.nal.usda.gov/articles/dataset/Dr_Duke_s_Phytochemical_and_Ethnobotanical_Databases/24660351"
accessed: true
access_method: [website-download, api]
access_date: 2026-09-30
access_notes: "Full download. File list and links read from the figshare API behind Ag Data Commons (api.figshare.com/v2/articles/24660351); Duke-Source-CSV.zip (6 MB, 16 CSV tables) and the preliminary data dictionary fetched with curl from ndownloader.figshare.com. No registration. The zip was deleted after unpacking. Added one derived file, ethnobot_country_counts.csv (our canonical-country mapping of ETHNOBOT.COUNTRY)."
countries: ["[[Afghanistan]]", "[[Algeria]]", "[[Angola]]", "[[Antigua and Barbuda]]", "[[Argentina]]", "[[Australia]]", "[[Austria]]", "[[Bahamas]]", "[[Barbados]]", "[[Belgium]]", "[[Belize]]", "[[Bolivia]]", "[[Botswana]]", "[[Brazil]]", "[[Bulgaria]]", "[[Burkina Faso]]", "[[Cambodia]]", "[[Cameroon]]", "[[Canada]]", "[[Central African Republic]]", "[[Chad]]", "[[Chile]]", "[[China]]", "[[Colombia]]", "[[Costa Rica]]", "[[Cuba]]", "[[Czech Republic]]", "[[Côte d'Ivoire]]", "[[Democratic Republic of the Congo]]", "[[Denmark]]", "[[Dominica]]", "[[Dominican Republic]]", "[[Ecuador]]", "[[Egypt]]", "[[El Salvador]]", "[[Eritrea]]", "[[Estonia]]", "[[Eswatini]]", "[[Ethiopia]]", "[[Fiji]]", "[[Finland]]", "[[France]]", "[[Gabon]]", "[[Gambia]]", "[[Germany]]", "[[Ghana]]", "[[Greece]]", "[[Grenada]]", "[[Guatemala]]", "[[Guinea]]", "[[Guyana]]", "[[Haiti]]", "[[Honduras]]", "[[Hungary]]", "[[Iceland]]", "[[India]]", "[[Indonesia]]", "[[Iran]]", "[[Iraq]]", "[[Ireland]]", "[[Israel]]", "[[Italy]]", "[[Jamaica]]", "[[Japan]]", "[[Kenya]]", "[[Kuwait]]", "[[Laos]]", "[[Latvia]]", "[[Lebanon]]", "[[Lesotho]]", "[[Liberia]]", "[[Libya]]", "[[Lithuania]]", "[[Madagascar]]", "[[Malawi]]", "[[Malaysia]]", "[[Mauritania]]", "[[Mauritius]]", "[[Mexico]]", "[[Micronesia]]", "[[Mongolia]]", "[[Morocco]]", "[[Mozambique]]", "[[Myanmar]]", "[[Nepal]]", "[[Netherlands]]", "[[New Zealand]]", "[[Nicaragua]]", "[[Niger]]", "[[Nigeria]]", "[[Norway]]", "[[Pakistan]]", "[[Panama]]", "[[Papua New Guinea]]", "[[Paraguay]]", "[[Peru]]", "[[Philippines]]", "[[Poland]]", "[[Portugal]]", "[[Romania]]", "[[Russia]]", "[[Saint Lucia]]", "[[Saint Vincent and the Grenadines]]", "[[Samoa]]", "[[Saudi Arabia]]", "[[Senegal]]", "[[Seychelles]]", "[[Sierra Leone]]", "[[Singapore]]", "[[Solomon Islands]]", "[[Somalia]]", "[[South Africa]]", "[[South Korea]]", "[[Spain]]", "[[Sri Lanka]]", "[[Sudan]]", "[[Suriname]]", "[[Sweden]]", "[[Switzerland]]", "[[Syria]]", "[[Taiwan]]", "[[Tanzania]]", "[[Thailand]]", "[[Togo]]", "[[Tonga]]", "[[Trinidad and Tobago]]", "[[Tunisia]]", "[[Turkey]]", "[[Uganda]]", "[[Ukraine]]", "[[United Kingdom]]", "[[United States]]", "[[Uruguay]]", "[[Vanuatu]]", "[[Venezuela]]", "[[Vietnam]]", "[[Yemen]]", "[[Zambia]]", "[[Zimbabwe]]"]
regions: ["[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[Central Asia]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "82,873 ethnobotanical use records (2,235 uses × 13,079 taxa, 139 countries) · 104,388 plant–chemical records (FARMACY_NEW; 2,315 plants, 24,771 chemicals) · 28,929 chemical–activity records (7,546 chemicals, 2,108 activities) · 29,585 chemicals · 1,627 toxicity/dose records"
size: "39 MB (16 CSVs + data dictionary)"
formats: [csv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "Three direct layers: (1) ETHNOBOT: plant → traditional use/indication by country or culture (e.g. Fever, Diuretic, Rheumatism), from ethnobotanical literature; (2) AGGREGAC: chemical → biological activity (e.g. CURCUMIN → Antiinflammatory, dose 1,200 mg/man/day), with an optional dose and reference; (3) DOSAGE: LD50/LDlo/ADI-type toxicity values per chemical. FARMACY_NEW links plant part → chemical with ppm ranges, so plant → chemical → activity chains are possible."
join_keys: [scientific name, CAS number, chemical name, common name]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients, search/compounds]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
  - region/global
  - region/middle-east
  - region/south-asia
---
# Dr. Duke's Phytochemical and Ethnobotanical Databases

> [!abstract] TL;DR
> A public-domain (CC0) USDA-ARS database compiled by James A. Duke, former chief of the USDA Economic
> Botany Laboratory. There are two parts. **Phytochemical**: 104,388 plant-part → chemical records with ppm
> ranges, and 28,929 chemical → biological-activity records. **Ethnobotanical**: 82,873 plant → traditional use
> records, **most of them labelled with a country or culture of use** (139 countries after normalisation). The
> dump is old (tables last edited 2015–2016) and the labels are messy. Even so, it is one of the few open
> resources that ties a plant to a *country-specific* folk use **and** to its chemicals and their activities.
> For the priority regions it has **Iraq (1,053 records, almost all from Al-Rawi's *Medicinal Plants of Iraq*),
> Turkey (4,815), India (6,837), China (13,469), Malaysia (3,220), Indonesia (2,211), Iran (100)**.
> The Arab Gulf and Central Asia are almost absent.

## Access
| | |
|---|---|
| Availability | open download (Ag Data Commons / figshare, CC0), plus the interactive web version at phytochem.nal.usda.gov |
| Link | https://agdatacommons.nal.usda.gov/articles/dataset/Dr_Duke_s_Phytochemical_and_Ethnobotanical_Databases/24660351 |
| Accessed? | yes: the full CSV dump |
| How | figshare API (`api.figshare.com/v2/articles/24660351`) → `curl` of `Duke-Source-CSV.zip` and `DrDukesDatabaseDataDictionary-prelim.csv` |
| Downloaded | `Data/dr-dukes-phytochemical-and-ethnobotanical-databases/`: 16 CSV tables (39 MB), the preliminary data dictionary, and our derived `ethnobot_country_counts.csv` |

## Tables & columns
Column meanings come from `DrDukesDatabaseDataDictionary-prelim.csv` (itself marked "in progress"; several
columns are "? (not used)"). The two main plant keys are `FNFNUM` (plant id used in the phytochemical tables,
resolved by `FNFTAX`) and the Latin binomial (`TAXON`, used in `ETHNOBOT`).

### `ETHNOBOT.csv` (82,873 rows): ethnobotanical uses
| column | type | meaning | example |
|---|---|---|---|
| `ETHNO` | int | id of the use record (plant + activity) | 22642 |
| `ACTIVITY` | str | the traditional use: indication, effect or disease (2,235 distinct; Fever 2,603, Diuretic 2,313, Tonic 1,738, Poison 1,654…) | Eruption |
| `GENUS`, `SPECIES`, `SPAUT`, `FAMILY` | str | taxonomy | Nigella, sativa, –, Ranunculaceae |
| `TAXON`, `TAXAUTHOR` | str | binomial (13,079 distinct) and authority | Nigella sativa |
| `CNAME` | str | local common name as given by the source | Habbat Soda |
| `COUNTRY` | str | "country name of ethno. usage; may have qualifier in parens., e.g. tribe, community, region" (98.8% filled, 442 raw values) | Iraq · India(Santal) · Elsewhere |
| `REFERENCE`, `LONGREF` | str | short / long reference (Uphof 7,079; Steinmetz 6,559; Bliss 5,343; Burkill 1966 4,530; Hartwell 4,340…) | Al-Rawi |
| `EFFECTIVE` | str | "effective as plant material vs. chemical extract?" (only 1,997 rows filled) | chemical |
| `SPRANK`, `SPXNAM`, `SPXAUT`, `USERID`, `CREATED`, `MODIFIED` | str | unused / bookkeeping | DUKE, 02-FEB-98 |

### `FARMACY_NEW.csv` (104,388 rows): plant part → chemical, with amounts
| column | type | meaning | example |
|---|---|---|---|
| `FNFNUM` | int | plant id (→ `FNFTAX.FNFNUM`; 2,315 plants) | 331 (*Curcuma longa*) |
| `CHEM`, `CHEMID` | str | chemical name (uppercase) and packed id (24,771 chemicals) | DESMETHOXYCURCUMIN |
| `PPCO` | str | plant part code (→ `PARTS.PPCO`: PL plant 18,723, LF leaf, FR fruit, SD seed, SH shoot…) | RH (rhizome) |
| `AMT_LO` / `AMT_OR_LO`, `AMT_HI` / `AMT_OR_HI` | str | lowest / highest measured ppm (current / original); a high value is present in 20,688 rows | 500, 28000 |
| `REFERENCE`, `REFYR` | str | source abbreviation and year | PAN AllHerb1998 PCF-I:180 |
| `CHEMCLASS`, `PLCO`, `EOPCT_*`, `QUANT_UNIT`, `TRACE`, `LT`, `INDIVIDUAL`, `NAPREF` | str | chemical class (sparse), plant code, essential-oil % (unused), unit, trace/less-than flags | – |

`FARMACY.csv` (68,844 rows, 20 columns) is the older version of the same table.

### `AGGREGAC.csv` (28,929 rows): chemical → biological activity
| column | type | meaning | example |
|---|---|---|---|
| `AGGNO` | int | aggregation number | 127155 |
| `CHEM` | str | chemical name (7,546 distinct) | CURCUMIN |
| `ACTIVITY` | str | bioactivity (2,108 distinct) | Antiinflammatory |
| `DOSAGE` | str | dose as LD50, LDlo, ED, RDA, ADI etc. (8,327 rows filled) | 1,200 mg/man/day |
| `REFERENCE` | str | source abbreviation | FT63(1):3 PCF:338 |
| `MAJORACT` | str | major activity (not used) | – |

### Lookup and auxiliary tables
| table | rows | content (key columns) |
|---|---|---|
| `CHEMICALS.csv` | 29,585 | `CHEM`, `CHEMID`, `CASNUM` (CAS number, only 97 filled) |
| `ACTIVITIES.csv` | 2,432 | `ACTIVITY`, `DEFINITION` (currently a copy of the name), `REFERENCE` |
| `SUPERACT.csv` | 5,358 | `SUPERACT` → `ACTIVITY`: 153 super-categories (e.g. AIDS/HIV → Anti-HIV-Integrase, AntiAIDS) |
| `DOSAGE.csv` | 1,627 | `CHEM`, `DOSAGE` (e.g. 1,8-CINEOLE "LD50=2,480 (orl rat)"), `REFERENCE` |
| `CHEM_MEANS.csv` | 3,832 | `chem_id`, `part_id`, `cnt` (number of species), `avg`, `std` (mean ppm per chemical × part) |
| `FNFTAX.csv` | 2,376 | plant id `FNFNUM` → `TAXON`, `GENUS`, `SPECIES`, `FAMILY`, `USEAGE` (e.g. F) |
| `COMMON_NAMES.csv` | 2,920 | `CNNAM` (English common name) → `FNFNUM` |
| `CODES.csv` | 8,926 | `PLNA` plant name → `PLCO` plant code |
| `PARTS.csv` | 115 | `PPCO` → `PPNA` (e.g. AN Anther) |
| `REFERENCES.csv` | 2,043 | `REFERENCE` → `LONGREF` full citation |
| `ASSAY.csv` | 2,630 | per-plant assay author / aggregation comments |
| `YIELDS.csv` | 2,824 | crop yield trials × site climate/soil (55 columns: `REPTRYLD`, `ANAVPRCP`, `BIOTEMP`, `PH`, fertiliser…); agronomy, not relevant here |

Sample: `Data/dr-dukes-phytochemical-and-ethnobotanical-databases/sample.csv` · full profile:
`Data/dr-dukes-phytochemical-and-ethnobotanical-databases/schema.md`

## Countries & cultures covered
Only `ETHNOBOT` has geography. `COUNTRY` has 442 raw spellings. We normalised them into
`ethnobot_country_counts.csv`: we stripped the parenthesised qualifier, merged sub-national places (Java,
Sumatra → Indonesia; Pahang, Perak, Malacca → Malaysia; Hainan, Tibet → China; Kashmir, Goa, Sikkim, Bengal →
India; Baluchistan → Pakistan), mapped old names (Upper Volta → Burkina Faso, Zaire → DR Congo, Burma →
Myanmar, Rhodesia → Zimbabwe, Malagasy → Madagascar, Ivory Coast → Côte d'Ivoire) and folded overseas
territories into the sovereign state (Hawaii, Puerto Rico, Guam → United States; Martinique, Réunion, Tahiti,
New Caledonia → France; Curaçao, Aruba → Netherlands; Bermuda → United Kingdom). Czechoslovakia was mapped to
Czech Republic (8 records).

Coverage breakdown of the 82,873 records:
- **61,914 rows (75%)** map to one of **139 countries**.
- **18,240 rows** carry region labels only. "Elsewhere" (= unspecified) 14,434; Africa 1,135; Europe 998;
  Latin America (South/Central America, West Indies, Guiana) 526; Southeast Asia (Indochina, Borneo, East
  Indies) 316; **Middle East 201 (Kurdistan 134, Arabic 24, Arab 23, Arabia 16, Jerusalem 4)**; Eurasia 171;
  Asia 102; USSR (unspecified) 95; Mediterranean 67; **Central Asia 1 (Turkistan)**.
- **1,325 rows** have a language/nationality word instead of a country: German 235, English 233, French 233,
  Dutch 168, Spanish 136, Italian 129, Chinese 122, Portuguese 42, Danish 20… Most come from Steinmetz and give
  a common name in that language.
- 1,033 rows are empty. 361 rows hold junk (mostly Malay plant names typed into the country field).

**Priority regions (records · distinct taxa):**
| country | records | taxa | main source / note |
|---|---|---|---|
| [[China]] | 13,469 | 1,559 | Bliss 5,328, "Hunan" 3,720, "Nas" 1,325 (reference codes) |
| [[India]] | 6,837 | 1,545 | incl. India(Santal) 2,651, India(Ayurvedic) 120, India(Hindu) 91, Gujarat 60, Punjab 19, **India(Unani) 12**; plus "Hindu" 93, "Sanscrit" 43 |
| [[Turkey]] | 4,815 | 824 | Steinmetz 4,664 (probably Turkish-language common names such as *Corekotu* for *Nigella sativa*; see Caveats) |
| [[Malaysia]] | 3,220 | 1,288 | Burkill 1966 |
| [[Indonesia]] | 2,211 | 847 | Java 1,795, Sumatra 167, Moluccas 63… |
| [[Iraq]] | 1,053 | 341 | **Al-Rawi 1,038**; Arabic common names (*Habbat Soda*, *Samm Al Ferakh*) |
| [[Japan]] | 759 | 288 | |
| [[Philippines]] | 752 | 425 | |
| [[Egypt]] | 673 | 178 | |
| [[Nepal]] | 323 | 95 | |
| [[Iran]] | 100 | 69 | Steinmetz 36 (Persian names like *Kust*, *Khok*), Uphof 28, Wealth of India (Woi) 23, Hartwell 12 |
| [[Cambodia]] · [[Vietnam]] · [[Thailand]] · [[Myanmar]] | 96 · 91 · 47 · 21 | | |
| [[Sri Lanka]] · [[Pakistan]] · [[Afghanistan]] | 51 · 35 · 14 | | |
| [[South Korea]] ("Korea") · [[Taiwan]] · [[Mongolia]] | 12 · 7 · 3 | | |
| [[Syria]] · [[Yemen]] · [[Kuwait]] · [[Lebanon]] · [[Israel]] · [[Saudi Arabia]] | 10 · 5 · 3 · 2 · 1 · 1 | | |
| [[Morocco]] · [[Algeria]] · [[Tunisia]] · [[Libya]] · [[Sudan]] | 20 · 10 · 5 · 4 · 351 | | |

**All countries (records):** China 13,469; India 6,837; Mexico 5,384; United States 4,964; Turkey 4,815;
Malaysia 3,220; Haiti 2,541; Indonesia 2,211; Trinidad and Tobago 1,847; Iraq 1,053; Lesotho 1,051;
Venezuela 1,025; Dominican Republic 839; Brazil 761; Japan 759; Philippines 752; Spain 748; Egypt 673;
Samoa 644; Ghana 583; Panama 477; Bahamas 392; Canada 375; Burkina Faso 369; Sudan 351; Guatemala 337;
Nepal 323; United Kingdom 296; France 233; South Africa 225; Netherlands 212; Argentina 198; Nigeria 188;
Tonga 181; Peru 159; Colombia 153; New Zealand 150; Solomon Islands 145; Fiji 143; Chile 140;
El Salvador 117; Cuba 112; Côte d'Ivoire 108; Germany 106; Italy 100; Iran 100; Cambodia 96; Madagascar 94;
Vietnam 91; Belgium 89; Australia 88; Paraguay 88; Ethiopia 82; Papua New Guinea 78; Greece 61; Honduras 58;
Sierra Leone 57; Tanzania 56; Ecuador 56; DR Congo 53; Sri Lanka 51; Thailand 47; Dominica 45;
Micronesia 38; Guinea 38; Liberia 36; Pakistan 35; Costa Rica 32; Central African Republic 30; Gabon 29;
Bolivia 29; Angola 28; Cameroon 25; Portugal 24; Jamaica 23; Singapore 23; Myanmar 21; Togo 21; Morocco 20;
Kenya 20; Senegal 20; Mauritius 20; Zimbabwe 17; Hungary 15; Vanuatu 15; Guyana 15; Afghanistan 14;
Gambia 13; Mozambique 12; South Korea 12; Malawi 12; Uruguay 12; Finland 11; Russia 11; Norway 10;
Algeria 10; Syria 10; Denmark 9; Austria 9; Iceland 9; Nicaragua 8; Suriname 8; Poland 8; Czech Republic 8;
Uganda 7; Belize 7; Taiwan 7; Lithuania 5; Eritrea 5; Tunisia 5; Yemen 5; Bulgaria 5; Libya 4; Chad 4;
Barbados 3; Ukraine 3; Kuwait 3; Laos 3; Somalia 3; Saint Lucia 3; Mongolia 3; Saint Vincent and the
Grenadines 3; Romania 2; Lebanon 2; Zambia 2; Antigua and Barbuda 1; Ireland 1; Eswatini 1; Botswana 1;
Estonia 1; Grenada 1; Latvia 1; Israel 1; Mauritania 1; Niger 1; Seychelles 1; Saudi Arabia 1; Sweden 1;
Switzerland 1.

## Inferring effects on the body
`body_effect: direct`. There are three layers, each with a different kind of evidence:
1. **Traditional claim by culture** (`ETHNOBOT`): plant → `ACTIVITY` (use/indication) + `COUNTRY`. Evidence:
   ethnobotanical literature (Uphof, Steinmetz, Burkill, Al-Rawi, Hartwell's cancer folklore…), not tested.
2. **Chemical activity** (`AGGREGAC` + `SUPERACT`): chemical → activity, sometimes with a dose. Evidence: mixed
   literature (pharmacology papers, reviews, Duke's own files). No assay type or effect size, only the claim.
3. **Toxicity / dose** (`DOSAGE`, `AGGREGAC.DOSAGE`): LD50 values (mostly rodent) and human doses.

Chain example, turmeric:
- `ETHNOBOT`: *Curcuma longa* → Colic, Congestion (China, Uphof); Cold, Conjunctivitis (Java, Burkill 1966);
  Dermatosis (Nepal, Singh); Dysentery (Malaya).
- `FARMACY_NEW` (FNFNUM 331): rhizome → DESMETHOXYCURCUMIN 500–28,000 ppm; BIS-DESMETHOXYCURCUMIN
  67–28,000 ppm; root → CURCUMINOIDS 30,000–80,000 ppm.
- `AGGREGAC`: CURCUMIN has 135 activity rows, e.g. 5-Lipoxygenase-Inhibitor, AntiHIV (IC50=40 uM),
  Antihepatotic, **Antiinflammatory (1,200 mg/man/day)**.

Priority-region example: *Nigella sativa* (black seed) → Eruption, Fever (Iraq, *Habbat Soda*, Al-Rawi);
Carminative, Digestive, Emmenagogue (Turkey, *Corekotu*, Steinmetz); Asthma, Cough, Diuretic (Elsewhere,
Wealth of India/Syria).

## Linking to other datasets
- **Scientific name** (`TAXON`, `FNFTAX.TAXON`) → [[CMAUP]], [[NPASS]], [[IMPPAT]], [[UNaProd]] (via its
  scientific names), and plant ingredients in [[FooDB]]. Binomials are mostly current but carry old synonyms,
  so normalise them through NCBI Taxonomy or GBIF first.
- **Chemical name** (uppercase, e.g. CURCUMIN) → [[FooDB]], [[NPASS]], [[CMAUP]], [[Phenol-Explorer]] by name
  matching. **CAS number** is filled for only 97 chemicals, so a real structure join needs name → PubChem
  resolution first. Note that NPASS 3.0 already imports Duke composition data (its quantity tables cite
  "Database [DUKE]"), which gives a ready-made name → NPASS id bridge for part of the chemicals.
- **Activities / uses** are free text; map them to MeSH/ICD before joining with [[CTD]].

## Versions
The Ag Data Commons item (version 1, published 2023-11-30) is an archival dump. The CSV files are dated
2015-12-06 to 2016-01-18, and the records inside were mostly created in 1997–2005. The live web database at
phytochem.nal.usda.gov may hold later edits that are not in the dump. No newer dataset version exists.

## Caveats
- **Old and uneven**: this is one person's lifetime compilation. There is no update after ~2016, and
  references are abbreviated codes (resolve them via `REFERENCES.csv`, 2,043 entries).
- **`COUNTRY` is noisy and mixes several things**: countries, sub-national places, regions, languages
  (Steinmetz's multilingual *Codex Vegetabilis* gives German, English, French… names), tribes (Santal), medical
  systems (Ayurvedic, Unani) and plain junk. Turkey's 4,815 records come almost entirely (4,664) from Steinmetz
  and may reflect **Turkish-language naming** rather than field-documented Turkish use. Iran's 100 records are
  mostly also from secondary compilations. Iraq (Al-Rawi) is the best-sourced Middle-East block.
- 17% of records are "Elsewhere". The Gulf states, Central Asia and Korea are nearly absent.
- `ACTIVITY` in ETHNOBOT mixes indications (Fever), effects (Diuretic) and uses (Cosmetic, Poison).
- No structure identifiers; CAS numbers are nearly empty.
- The data dictionary is preliminary: several column meanings are marked "?".
