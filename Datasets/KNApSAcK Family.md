---
title: "KNApSAcK Family"
slug: knapsack-family
kind: [ingredient, compound]
version: "web databases, continuously updated (KNApSAcK World last update 2022-03-29; terms revised 2024-06-04)"
previous_versions: "Described in Afendi et al., Plant Cell Physiol 2012 (WorldMap 41,548 GZ–plant pairs, 222 zones, 15,240 plants; JAMU 5,310 formulae; KAMPO 336 formulae; Core 101,500 species–metabolite pairs)"
papers: ["[[Afendi2012 - KNApSAcK Family databases]]"]
url: "https://www.knapsackfamily.com/KNApSAcK_Family/"
license: "CC BY-NC-ND 4.0 (KNApSAcK Core terms of service, rev. 2024-06-04; cite Afendi 2012 + URL)"
availability: open-web
access_link: "https://www.knapsackfamily.com/KNApSAcK_World/top.php"
accessed: partial
access_method: [scrape]
access_date: 2026-09-30
access_notes: "No bulk download or API. Polite scrape (~49 requests, ≥1.1 s apart, browser UA): KNApSAcK World country pages for 36 priority countries (Middle East, North Africa, Central/South/East/Southeast Asia) = 25,326 of the 76,100 records; the full JAMU formula-name list (1 page); 8 Jamu formula detail searches; 2 Jamu herb-effect pages; 1 KNApSAcK Core organism page (ginger → 635 metabolites). One request hit a connection reset (the server drops connections under load) and was retried with backoff. Not scraped: the other ~190 country pages, KAMPO, Biological Activity, DietNavi/YAKUZEN/LunchBox and Core metabolite pages."
countries: ["[[Afghanistan]]", "[[Albania]]", "[[Algeria]]", "[[American Samoa]]", "[[Angola]]", "[[Antigua and Barbuda]]", "[[Argentina]]", "[[Armenia]]", "[[Aruba]]", "[[Australia]]", "[[Austria]]", "[[Azerbaijan]]", "[[Bahamas]]", "[[Bahrain]]", "[[Bangladesh]]", "[[Barbados]]", "[[Belarus]]", "[[Belgium]]", "[[Belize]]", "[[Benin]]", "[[Bermuda]]", "[[Bhutan]]", "[[Bolivia]]", "[[Bosnia and Herzegovina]]", "[[Botswana]]", "[[Brazil]]", "[[Brunei]]", "[[Bulgaria]]", "[[Burkina Faso]]", "[[Burundi]]", "[[Cambodia]]", "[[Cameroon]]", "[[Canada]]", "[[Cape Verde]]", "[[Cayman Islands]]", "[[Central African Republic]]", "[[Chad]]", "[[Chile]]", "[[China]]", "[[Colombia]]", "[[Comoros]]", "[[Cook Islands]]", "[[Costa Rica]]", "[[Croatia]]", "[[Cuba]]", "[[Cyprus]]", "[[Czech Republic]]", "[[Côte d'Ivoire]]", "[[Democratic Republic of the Congo]]", "[[Denmark]]", "[[Djibouti]]", "[[Dominica]]", "[[Dominican Republic]]", "[[Ecuador]]", "[[Egypt]]", "[[El Salvador]]", "[[Equatorial Guinea]]", "[[Eritrea]]", "[[Estonia]]", "[[Eswatini]]", "[[Ethiopia]]", "[[Falkland Islands]]", "[[Faroe Islands]]", "[[Fiji]]", "[[Finland]]", "[[France]]", "[[French Guiana]]", "[[French Polynesia]]", "[[Gabon]]", "[[Gambia]]", "[[Georgia]]", "[[Germany]]", "[[Ghana]]", "[[Greece]]", "[[Greenland]]", "[[Guadeloupe]]", "[[Guam]]", "[[Guatemala]]", "[[Guinea]]", "[[Guinea-Bissau]]", "[[Guyana]]", "[[Haiti]]", "[[Honduras]]", "[[Hong Kong]]", "[[Hungary]]", "[[Iceland]]", "[[India]]", "[[Indonesia]]", "[[Iran]]", "[[Iraq]]", "[[Ireland]]", "[[Israel]]", "[[Italy]]", "[[Jamaica]]", "[[Japan]]", "[[Jordan]]", "[[Kazakhstan]]", "[[Kenya]]", "[[Kiribati]]", "[[Kuwait]]", "[[Kyrgyzstan]]", "[[Laos]]", "[[Latvia]]", "[[Lebanon]]", "[[Lesotho]]", "[[Liberia]]", "[[Libya]]", "[[Liechtenstein]]", "[[Lithuania]]", "[[Luxembourg]]", "[[Madagascar]]", "[[Malawi]]", "[[Malaysia]]", "[[Maldives]]", "[[Mali]]", "[[Malta]]", "[[Marshall Islands]]", "[[Martinique]]", "[[Mauritania]]", "[[Mauritius]]", "[[Mexico]]", "[[Micronesia]]", "[[Moldova]]", "[[Monaco]]", "[[Mongolia]]", "[[Montenegro]]", "[[Montserrat]]", "[[Morocco]]", "[[Mozambique]]", "[[Myanmar]]", "[[Namibia]]", "[[Nauru]]", "[[Nepal]]", "[[Netherlands]]", "[[New Caledonia]]", "[[New Zealand]]", "[[Nicaragua]]", "[[Niger]]", "[[Nigeria]]", "[[Niue]]", "[[North Korea]]", "[[North Macedonia]]", "[[Northern Mariana Islands]]", "[[Norway]]", "[[Oman]]", "[[Pakistan]]", "[[Palau]]", "[[Palestine]]", "[[Panama]]", "[[Papua New Guinea]]", "[[Paraguay]]", "[[Peru]]", "[[Philippines]]", "[[Pitcairn]]", "[[Poland]]", "[[Portugal]]", "[[Puerto Rico]]", "[[Qatar]]", "[[Republic of the Congo]]", "[[Romania]]", "[[Russia]]", "[[Rwanda]]", "[[Réunion]]", "[[Saint Barthélemy]]", "[[Saint Kitts and Nevis]]", "[[Saint Lucia]]", "[[Saint Vincent and the Grenadines]]", "[[Samoa]]", "[[San Marino]]", "[[São Tomé and Príncipe]]", "[[Saudi Arabia]]", "[[Senegal]]", "[[Serbia]]", "[[Seychelles]]", "[[Sierra Leone]]", "[[Singapore]]", "[[Slovakia]]", "[[Slovenia]]", "[[Solomon Islands]]", "[[Somalia]]", "[[South Africa]]", "[[South Korea]]", "[[Spain]]", "[[Sri Lanka]]", "[[Sudan]]", "[[Suriname]]", "[[Sweden]]", "[[Switzerland]]", "[[Syria]]", "[[Taiwan]]", "[[Tajikistan]]", "[[Tanzania]]", "[[Thailand]]", "[[Timor-Leste]]", "[[Togo]]", "[[Tokelau]]", "[[Tonga]]", "[[Trinidad and Tobago]]", "[[Tunisia]]", "[[Turkey]]", "[[Turkmenistan]]", "[[Tuvalu]]", "[[Uganda]]", "[[Ukraine]]", "[[United Arab Emirates]]", "[[United Kingdom]]", "[[United States]]", "[[United States Virgin Islands]]", "[[Uruguay]]", "[[Uzbekistan]]", "[[Vanuatu]]", "[[Venezuela]]", "[[Vietnam]]", "[[Wallis and Futuna]]", "[[Western Sahara]]", "[[Yemen]]", "[[Zambia]]", "[[Zimbabwe]]"]
regions: ["[[Middle East]]", "[[North Africa]]", "[[Sub-Saharan Africa]]", "[[Central Asia]]", "[[South Asia]]", "[[East Asia]]", "[[Southeast Asia]]", "[[Europe]]", "[[North America]]", "[[Latin America]]", "[[Oceania]]"]
n_records: "World: 76,100 species–country records in 229 countries (30,133 edible / 45,967 medicinal); JAMU: 5,310 formulae (4,723 unique names); Core (2012): 101,500 species–metabolite pairs. Scraped: 25,326 World rows, 126 Jamu formula–herb rows, 635 ginger metabolites"
size: "6 MB scraped CSV"
formats: [html, csv, tsv]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: direct
body_effect_how: "World: species × country × purpose (edible / medicinal) from literature; JAMU: formula → efficacy text + effect group (Indonesian registrations) and herb → traditional effect; Core: species → metabolites (C_ID, CAS) linkable to activity DBs. Traditional-claim level only."
join_keys: [scientific name, CAS, KNApSAcK C_ID, ISO3 country code, Indonesian herb name]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients, search/regions, search/compounds]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
---
# KNApSAcK Family

> [!abstract] TL;DR
> KNApSAcK Family (Kanaya lab, NAIST, Japan, with IPB Indonesia) is a set of linked web databases keyed on
> **species names**. The relevant ones are: **KNApSAcK World**, a plant/food × country usage map (76,100 records,
> 229 countries) where each record is labelled **edible** or **medicinal**; **JAMU**, 5,310 Indonesian Jamu
> products with composition, efficacy text and effect group; and **KNApSAcK Core**, species → metabolites. The
> edible/medicinal label per country is the closest thing to a **medicine-food flag** in this batch. Ginger,
> cinnamon, jujube, goji and fenugreek are recorded as *edible* in some countries and *medicinal* in others (or
> both). It is web-only; we scraped the 36 priority countries.

## Access
| | |
|---|---|
| Availability | open web (browse/search pages only; no download, no API) |
| Link | https://www.knapsackfamily.com/KNApSAcK_World/top.php · https://www.knapsackfamily.com/jamu/top.php |
| Accessed? | partial: scrape of 36 countries + Jamu samples + one Core page |
| How | `KNApSAcK_World/search.php?cn=<ISO3>&wd=&flg=` (1 page per country, all rows); `jamu/datalist.php`; POST `jamu/haigou.php` (`hword=<jamu name>`); `jamu/effect.php?sid=`; `knapsack_core/result.php?sname=organism&word=Zingiber officinale` |
| Downloaded | `Data/knapsack-family/`: `world_country_species.csv`, `world_country_counts.csv`, `jamu_names.tsv`, `jamu_formula_herbs.csv`, `jamu_herb_effect_examples.csv`, `core_zingiber_officinale_metabolites.csv` (+ 3 raw HTML pages) |

A full World crawl would be about 190 more pages. Keep it polite: the server resets connections under load.

## Tables & columns
All tables are our parse of the HTML (column names are ours; meanings from the page headers).

### `world_country_species.csv` (25,326 rows, 36 countries)
| column | type | meaning | example |
|---|---|---|---|
| `country_code`, `country` | str | ISO3 code of the flag page; official English name | SAU, Kingdom of Saudi Arabia |
| `species` | str | scientific name (15,670 distinct) | Trigonella foenum-graecum |
| `upper_class` | str | "UpperClassification (Region ; Classification)": plants 18,420, seafood 1,580, mushrooms 1,039, insects 324, meats 278; sometimes with part/use, e.g. "plants(leaves,flowers : Vegetable)" | plants |
| `family` | str | family | Fabaceae |
| `common_name` | str | English common name(s), ` \| `-separated (18%) | Fenugreek |
| `purpose` | str | **edible** (9,711) or **medicinal** (15,615) | edible |
| `upper_class_ja`, `family_ja`, `common_name_ja` | str | Japanese equivalents | フェネグリーク \| コロハ |
| `reference` | str | literature source of the record | U. P. Hedrick, Sturtevant's Edible Plants of the World (1919) |

`world_country_counts.csv` (36 rows): the page header counts `matched`, `edible`, `medicinal` and
`rows_parsed` (equal to `matched` for every country).

### `jamu_formula_herbs.csv` (126 rows)
| column | type | meaning | example |
|---|---|---|---|
| `company` | str | manufacturer or reference | Air Mancur |
| `jamu_name` | str | product name | Jamu Batuk |
| `jamu_effect` | str | efficacy text | Cure cough |
| `jamu_effect_group` | str | effect category | Respiratory disease |
| `herb_name`, `herb_name_indonesia`, `herb_name_en_cn` | str | crude drug; Indonesian; English/Chinese name | Zingiber officinale Rhizoma; Jahe; GINGER |
| `scientific_name`, `plant_part` | str | species, part | Zingiber officinale Rosc; Rhizome |
| `herb_effect_sid` | str | id of the herb-effect page | S01128 |
| `percent` | str | proportion; always "Incl." (included) in our sample, so **no amounts** | Incl. |

Also: `jamu_names.tsv` (4,723 unique product names out of 5,310 entries), `jamu_herb_effect_examples.csv` (herb
→ traditional effect text, e.g. ginger rhizome: "belly salve, cough medicine, rheumatism, antidote"), and
`core_zingiber_officinale_metabolites.csv` (635 rows: `C_ID`, `CAS_ID`, `metabolite_name`,
`molecular_formula`, `mw`, `organism`; e.g. C00002748 (S)-6-Gingerol, CAS 23513-14-6).

Sample: `Data/knapsack-family/sample.csv` · full profile: `Data/knapsack-family/schema.md`

## Countries & cultures covered
The World map has flag pages for 227 codes (the site says 229 countries). `countries` lists every
flag that maps to a country or territory (218; excluded: Antarctica, BIOT, South Georgia, plus non-ISO codes ALS
Alaska, HAW Hawaii, QLS, ROD Rodrigues, SCG Serbia and Montenegro, SML). Record counts per country, from the
scraped pages (matched / edible / medicinal):

| country | code | records | edible | medicinal |
|---|---|---|---|---|
| [[United Arab Emirates]] | ARE | 7 | 6 | 1 |
| [[Saudi Arabia]] | SAU | 71 | 53 | 18 |
| [[Oman]] | OMN | 8 | 4 | 4 |
| [[Qatar]] | QAT | 11 | 1 | 10 |
| [[Kuwait]] | KWT | 11 | 4 | 7 |
| [[Bahrain]] | BHR | 23 | 4 | 19 |
| [[Yemen]] | YEM | 13 | 9 | 4 |
| [[Iran]] | IRN | 150 | 60 | 90 |
| [[Iraq]] | IRQ | 107 | 19 | 88 |
| [[Jordan]] | JOR | 386 | 22 | 364 |
| [[Syria]] | SYR | 163 | 137 | 26 |
| [[Lebanon]] | LBN | 532 | 101 | 431 |
| [[Israel]] | ISR | 273 | 150 | 123 |
| [[Turkey]] | TUR | 569 | 201 | 368 |
| [[Egypt]] | EGY | 487 | 190 | 297 |
| [[Morocco]] | MAR | 263 | 154 | 109 |
| [[Kazakhstan]] | KAZ | 8 | 7 | 1 |
| [[Uzbekistan]] | UZB | 20 | 11 | 9 |
| [[Kyrgyzstan]] | KGZ | 39 | 39 | 0 |
| [[Tajikistan]] | TJK | 18 | 8 | 10 |
| [[Turkmenistan]] | TKM | 99 | 6 | 93 |
| [[Afghanistan]] | AFG | 34 | 21 | 13 |
| [[Pakistan]] | PAK | 230 | 147 | 83 |
| [[India]] | IND | 3,685 | 742 | 2,943 |
| [[Bangladesh]] | BGD | 768 | 147 | 621 |
| [[Nepal]] | NPL | 1,035 | 328 | 707 |
| [[Sri Lanka]] | LKA | 91 | 54 | 37 |
| [[China]] | CHN | 5,090 | 1,643 | 3,447 |
| [[South Korea]] | KOR | 442 | 85 | 357 |
| [[Japan]] | JPN | 3,492 | 2,835 | 657 |
| [[Mongolia]] | MNG | 252 | 91 | 161 |
| [[Indonesia]] | IDN | 2,127 | 786 | 1,341 |
| [[Malaysia]] | MYS | 865 | 376 | 489 |
| [[Thailand]] | THA | 2,554 | 705 | 1,849 |
| [[Vietnam]] | VNM | 440 | 83 | 357 |
| [[Philippines]] | PHL | 963 | 482 | 481 |

Other countries were not scraped; their counts are on their flag pages. **Jamu** is [[Indonesia]] (Indonesian
products and herb names). **KAMPO** (not scraped) is [[Japan]].

## Inferring effects on the body
`body_effect: direct` (traditional claims), plus `linkable` via Core metabolites:
- **World**: species × country × `purpose`. This is **usage**, not effect, but it is the only per-country
  edible-vs-medicinal signal we have. 1,212 species appear as both edible and medicinal across the 36 countries;
  856 species × country pairs are both edible and medicinal *in the same country*. Examples:
  - *Zingiber officinale* (ginger): medicinal in Saudi Arabia, Oman, Yemen, Iraq, Jordan, Lebanon, Egypt,
    Morocco, Bangladesh, Korea, Vietnam, Malaysia, Indonesia; edible **and** medicinal in China, India, Japan,
    Nepal, Thailand, Philippines.
  - *Trigonella foenum-graecum* (fenugreek): edible in the UAE, Egypt, Morocco, India, Japan; medicinal in Iran,
    Iraq, Israel, Jordan, Lebanon, Turkmenistan, China and others.
  - *Ziziphus jujuba* (jujube): edible + medicinal in China and India; medicinal in Jordan and Lebanon.
    *Lycium* (goji): medicinal in Korea and Mongolia; edible + medicinal in China (*L. chinense*) and Japan. *Nigella sativa*:
    medicinal across the Middle East, edible in Egypt.
- **JAMU**: formula → `jamu_effect` and `jamu_effect_group` (registered product claims), and herb →
  traditional effect text (`effect.php`).
- **Core**: species → metabolites (C_ID/CAS). Effects of the metabolites come from KNApSAcK Biological Activity /
  Metabolite Activity (not scraped) or by joining CAS/name to [[HERB]], [[TM-MC]], [[FooDB]].

Example chain: **ginger** (*Zingiber officinale*; edible + medicinal in China, India, Japan…; medicinal in Saudi
Arabia) → Jamu: *Jahe* rhizome in "Jamu Batuk" (Air Mancur; effect "Cure cough", group *Respiratory disease*)
and "Jamu Pilek" (colds). Herb effect: "belly salve, cough medicine, rheumatism, antidote" → Core metabolite
**(S)-6-Gingerol** (C00002748, CAS 23513-14-6) → joins to 6-gingerol in [[HERB]] (HBIN012366) and [[TM-MC]]
(ID 559528).

## Linking to other datasets
- **Scientific name** → [[IMPPAT]], [[FooDB]], [[TM-MC]]/[[SymMap]]/[[HERB]] (after mapping pharmacopoeial Latin
  names such as *Zingiberis Rhizoma* to binomials), and to food datasets' ingredient names via common names.
- **CAS** (Core) → [[HERB]] `CAS_id`, [[SymMap]] `CAS_id`; metabolite names → PubChem.
- **ISO3 country code** → the vault's country notes; KNApSAcK World is a candidate source for "which plants
  are eaten vs used medicinally in country X".

## Versions
There are no numbered releases. Statistics have grown since the 2012 paper: World 41,548 GZ–plant pairs in 222
zones (2012) → 76,100 records in 229 countries (site, last update 2022-03-29). JAMU 5,310 formulae (unchanged).
Other family members added since 2012 include DietNavi, YAKUZEN (medicinal cuisine), LunchBox, TeaPot, DietDish,
FoodProcessor and MetaboliteEcology (links on the family top page; not examined).

## Caveats
- **CC BY-NC-ND 4.0**: no commercial use and no derivatives; a merged KG would need permission.
- Web-only. Our copy covers 36 of 229 countries. A full scrape needs about 190 more pages; ask whether that
  is acceptable under the terms.
- Records are literature-derived and heterogeneous (1919 Sturtevant through FAO reports). `purpose` is binary.
  A species can have several rows per country (different references).
- Jamu composition has no percentages in our sample ("Incl."). Efficacy groups look inconsistent (e.g. "Jamu
  Napsu Makan", an appetite product, is grouped as musculoskeletal).
- Country names are official long forms ("Kingdom of Saudi Arabia"); use `country_code` for joins.
