---
title: "TM-MC"
slug: tm-mc
kind: [ingredient, compound]
version: "2.0 (paper Jan 2024; download files updated 2026-06-15)"
previous_versions: "1.0 (2015; Kim et al., BMC Complement Altern Med 2015, PMID 26156871; 536 medicinal materials, 14,127 compound names, no structures, targets or prescriptions)"
papers: ["[[Kim2024 - TM-MC 2.0 Northeast Asian medicinal materials chemical database]]"]
url: "https://tm-mc.kr"
license: "not stated on the site; paper CC BY 4.0"
availability: open-download
access_link: "https://tm-mc.kr/download.jsp"
accessed: true
access_method: [website-download]
access_date: 2026-09-30
access_notes: "All 6 xlsx tables + README downloaded directly (no login), 68 MB. The candidate note listed it as open-web; there is in fact a bulk Download page. Not downloaded: per-compound SDF/JPG structure files (the SDF text is inside chemical_property.xlsx)."
countries: ["[[South Korea]]", "[[China]]", "[[Japan]]"]
regions: ["[[East Asia]]"]
n_records: "649 medicinal materials · 116,014 material–compound–PMID rows (23,948 compound IDs) · 581,190 compound–protein links · 1,042,955 protein–disease links · 49,163 prescription–material rows (2,535 prescription names)"
size: "68 MB (xlsx)"
formats: [xlsx]
has_ingredients: ""
has_amounts: ""
has_cooking_method: ""
has_nutrition: ""
body_effect: linkable
body_effect_how: "Material → compound (PubMed chromatography articles, PMID per row) → human protein (STITCH v5 combined score or PubChem) → disease (DisGeNET v7 score). All effect links are database-derived associations; there are no curated indications per material, and prescriptions have no indications in the download."
join_keys: [InChIKey, PubChem CID, PMID, Latin pharmacopoeial name, Korean/Hanja/Chinese/Pinyin/Japanese names, STITCH/Ensembl protein id (ENSP), UMLS CUI (DisGeNET)]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
found_by: [search/ingredients]
tags:
  - type/dataset
  - kind/ingredient
  - kind/compound
  - q/2
  - q/3
  - access/accessed
  - access/open
---
# TM-MC

> [!abstract] TL;DR
> TM-MC 2.0 (Korea Institute of Oriental Medicine) is a manually curated chemical database of the **medicinal
> materials in the Korean, Chinese and Japanese pharmacopoeias**. The current download has **649 materials**,
> each with Korean/Hanja/Chinese/Pinyin/Japanese/Kanji names. Materials are linked to **23,948 compound IDs**
> extracted from PubMed chromatography papers (every row has a PMID), with InChIKey/CID. Compounds link to
> STITCH targets and DisGeNET diseases. The download also has **2,535 Korean-medicine prescriptions with
> per-material dosages**. It is the only resource in this batch that covers **Korea and Japan** explicitly and
> gives **amounts** in formulae.

## Access
| | |
|---|---|
| Availability | open download (Download page, "updated on June 15, 2026") + browse/search site |
| Link | https://tm-mc.kr/download.jsp |
| Accessed? | yes: all 6 tables |
| How | `curl https://tm-mc.kr/download/<file>.xlsx` |
| Downloaded | `Data/tm-mc/`: `medicinal_material`, `medicinal_compound`, `chemical_property`, `chemical_protein`, `protein_disease`, `prescription` (.xlsx) + `README.md` (the site's README.txt, renamed so the profiler skips it) |

## Tables & columns
Column meanings are from the site's README (copied to `Data/tm-mc/README.md`).

### `medicinal_material.xlsx` (649 rows)
| column | type | meaning | example |
|---|---|---|---|
| `LATIN` | str | Latin pharmacopoeial name; the material identifier | Zingiberis Rhizoma Recens |
| `COMMON` | str | English name from the pharmacopoeia (32%) | Raw Ginger |
| `KOREAN`, `HANJA` | str | Korean name (100%), hanja | 생강, 生薑 |
| `CHINESE`, `PINYIN` | str | Chinese name (88%), pinyin | 生姜, Shengjiang |
| `JAPANESE`, `KANJI` | str | Japanese name (30%), kanji | ショウキョウ, 生姜 |

### `medicinal_compound.xlsx` (116,014 rows)
| column | type | meaning | example |
|---|---|---|---|
| `LATIN` | str | material | Zingiberis Rhizoma Recens |
| `ID` | int | TM-MC compound ID; **0 = compound not identified** (3,998 rows) | 559528 |
| `COMPOUND` | str | compound name as written in the article | 6-gingerol |
| `PMID` | int | PubMed article it was curated from (11,405 distinct) | 8492294 |

### `chemical_property.xlsx` (23,948 rows)
| column | type | meaning | example |
|---|---|---|---|
| `ID` | int | TM-MC compound ID | 559528 |
| `INCHIKEY`, `INCHI`, `SMILES`, `SDF` | str | structure | NLDDIKRKFXEWBK-AWEZNQCLSA-N |
| `CID` | str | PubChem CID (97%) | 442793 |
| `FORMULA`, `MW`, `EXACT_MW` | | formula, weights | C17H26O4 |
| `LOGP`, `TPSA`, `ATOM`, `HBA`, `HBD`, `ROTB`, `AROM`, `ALERTS` | num | ChemAxon physicochemical descriptors, structural alerts | |
| `DL` | float | drug-likeness (QED) | 0.647 |
| `OB` | Y/N | oral bioavailability by Veber's rule | Y |

### `chemical_protein.xlsx` (581,190 rows)
`ID` (compound), `PROTEINID` (STITCH v5 / Ensembl protein, ENSP…), `PREFERRED_NAME` (gene symbol, e.g. TP53),
`SOURCE` (STITCH 428,820 · PubChem 152,370), `SCORE` (STITCH combined score; 0 for PubChem rows).

### `protein_disease.xlsx` (1,042,955 rows)
`PROTEIN_ID` (ENSP), `PREFERRED_NAME`, `DISEASEID` (DisGeNET v7 UMLS CUI, e.g. C0019196), `DISEASENAME`
(Hepatitis C), `SCORE` (DisGeNET GDA score 0–1).

### `prescription.xlsx` (49,163 rows)
| column | type | meaning | example |
|---|---|---|---|
| `ENGLISH` | str | romanised Korean prescription name | Gyejitang |
| `KOREAN`, `HANJA`, `CHINESE`, `PINYIN` | str | names | 계지탕, 桂枝湯, 桂枝汤, Gui Zhi Tang |
| `WRITTEN`, `CHAPTER` | str | classical source text and chapter (67% / 37%) | 傷寒論 (Shanghan lun), 東醫寶鑑 (Donguibogam) |
| `TEXTBOOK`, `PAGE` | str | Korean-medicine textbook it was extracted from (8 textbooks) | 方劑學, p. 72 |
| `LATIN` | str | medicinal material | Zingiberis Rhizoma Recens |
| `SEQ` | int | order of the material in the prescription | 4 |
| `PROCESS` | str | processing method (14%) | 切 (sliced), 炙 (honey-fried) |
| `DOSAGE`, `UNIT` | str | amount (93%) and unit: g 43,666 · 개 (pieces) 1,646 · 각등분 (equal parts) 1,442 · 合 · L | 9 g |

The same prescription name appears several times (different textbooks/pages and compositions): 5,468
name–textbook–page variants for 2,535 names.

Sample: `Data/tm-mc/sample.csv` · full profile: `Data/tm-mc/schema.md`

## Countries & cultures covered
Per-country coverage is given by which name columns are filled (the pharmacopoeia a material is listed in is not
a separate column):
- **[[South Korea]]**: all 649 materials have a Korean name; all prescriptions come from Korean-medicine
  textbooks (e.g. 東醫方劑 處方解說 16,878 rows, 肺系內科學 9,192, 脾系內科學 5,812) and classical sources
  including the Korean *Donguibogam* (東醫寶鑑).
- **[[China]]**: 572 materials with a Chinese name (the paper: 556 of 635 are in the Chinese pharmacopoeia).
- **[[Japan]]**: 195 materials with a Japanese name (paper: 192 in the Japanese pharmacopoeia).
- The paper counts 454 materials in the Korean pharmacopoeia. There are no food or culinary labels.
- **Medicine-food homology is not flagged**, but the everyday foods are all there under their pharmacopoeial
  names: ginger (Zingiberis Rhizoma Recens, 647 compound rows; dried Zingiberis Rhizoma), jujube (Zizyphi
  Fructus), goji (Lycii Fructus), cinnamon (Cinnamomi Cortex/Ramulus), hawthorn (Crataegi Fructus), turmeric
  (Curcumae Longae Rhizoma, ウコン), Chinese yam (Dioscoreae Rhizoma). Ginger appears in 489 of 2,535
  prescriptions, typically as "3 pieces of raw ginger + 2 jujubes", the classic food pairing (e.g. 桂枝湯
  Gyejitang: Cinnamomi Ramulus 12 g, Paeoniae Radix 8 g, Glycyrrhiza 4 g, Zingiberis Rhizoma Recens 3 개,
  Zizyphi Fructus 2 개).

## Inferring effects on the body
`body_effect: linkable`. The dataset gives chemistry plus predicted mechanisms, not indications:
- **Material → compound**: literature-curated (chromatographic identification), with a PMID per row. Strong
  evidence of *presence*, but no concentrations.
- **Compound → protein**: STITCH v5 (text-mined, experimental and predicted channels combined; `SCORE`) or
  PubChem bioassay targets.
- **Protein → disease**: DisGeNET v7 gene–disease associations (`SCORE`).
- The chain material → disease is therefore **inferred**. For clinical or traditional-use evidence, join to
  [[HERB]] (trials) or [[SymMap]] (TCM symptoms) by Latin name or InChIKey/CID.

Example: **Raw ginger 생강/生姜 (Zingiberis Rhizoma Recens)** → **6-gingerol** (ID 559528; 6 PMIDs incl.
8492294; InChIKey NLDDIKRKFXEWBK-AWEZNQCLSA-N; CID 442793; DL 0.65; OB = Y) → 117 protein links, top TP53 (STITCH
0.824), ATP2A1 (0.786), MMP9 (0.725) → DisGeNET: MMP9 → myocardial infarction, COPD, hypertensive disease
(0.6); TP53 → breast/liver carcinoma (1.0).

## Linking to other datasets
- `INCHIKEY` / `CID` → [[HERB]] (`InChIKey`, `PubChem_id`), [[SymMap]] (`PubChem_CID`), [[FooDB]], [[IMPPAT]],
  [[CTD]], [[DrugBank]]. For ginger the 6-gingerol InChIKey is identical in TM-MC and HERB.
- `LATIN` → [[SymMap]] `Latin_name` and [[HERB]] `Herb_latin_name` (same pharmacopoeial naming; string match
  works for most).
- `DISEASEID` (UMLS CUI) → [[HERB]] `DisGeNET_id`, [[SymMap]] `UMLS_id`, [[CTD]] (via MeSH/UMLS).
- `PROTEINID` (ENSP) → Ensembl → HGNC/UniProt → [[CTD]], [[DrugBank]].

## Versions
| | materials | compounds | prescriptions | targets | diseases |
|---|---|---|---|---|---|
| TM-MC 1.0 (2015) | 536 | 14,127 names (no structures) | – | – | – |
| 2.0 (paper, Jan 2024) | 635 | 34,107 (21,306 identified, de-duplicated) | 5,075 (2,393 by name) | 13,992 | 27,997 |
| **2.0 download, 2026-06-15** | **649** | **23,948 IDs** | **2,535 names** | **18,676 proteins** in `chemical_protein` | **29,847** in `protein_disease` |

2.0 over 1.0: a structure (InChIKey/SMILES/SDF) for every identified compound, PubChem matching, ADME
descriptors, STITCH targets, DisGeNET diseases, prescriptions, and a timeline of first appearance in PubMed. The
site says it updates monthly. The current file adds PubChem-sourced targets (`SOURCE = PubChem`) and more
materials than the paper.

## Caveats
- No concentrations; presence only. Compound lists depend on what was analysed by chromatography in PubMed.
  Some materials with mostly Chinese-language literature are under-covered (the paper says so).
- Targets and diseases are predicted or database-derived (STITCH/DisGeNET), not curated for the herb.
- Prescription indications are not in the download ("treatment symptom data will be supplemented").
- Units are mixed (g, pieces 개, equal parts 각등분, 合); some rows repeat a material with two dosage schemes.
- 3,998 compound rows have `ID = 0` (unidentified names).
