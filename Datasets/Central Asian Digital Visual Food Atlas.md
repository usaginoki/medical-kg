---
title: "Central Asian Digital Visual Food Atlas"
slug: central-asian-digital-visual-food-atlas
kind: [food]
version: "Atlas.pdf as committed 2025 (commit 0ab8965, 122 pages, 190.9 MB); later removed from the repo head (commit b516739 'Delete Atlas.pdf')"
previous_versions: "An earlier LFS upload (commit edd8f04, 190.8 MB) was deleted in 2de3402 and re-added in 0ab8965"
papers: ["[[Omarova2025 - Central Asian Visual Food Atlas]]"]
url: "https://github.com/Central-Asian-Food-Innovation-Lab/Central-Asian-Digital-Visual-Food-Atlas"
license: "No license file in the repo; README asks users to cite Omarova et al. 2025; the article is CC BY 4.0"
availability: open-download
access_link: "https://media.githubusercontent.com/media/Central-Asian-Food-Innovation-Lab/Central-Asian-Digital-Visual-Food-Atlas/0ab8965/Atlas.pdf"
accessed: true
access_method: [github]
access_date: 2026-09-30
access_notes: "The repo head holds only a README; the .gitattributes still declares Atlas.pdf as a Git LFS file. The git history shows the PDF was added via LFS (edd8f04), deleted, re-added (0ab8965) and deleted again (b516739). We fetched the LFS object of commit 0ab8965 from media.githubusercontent.com (190.9 MB, 122 pages) and parsed all 115 items to CSV. The owners removed the file from the head, so ask the authors (yen.chan@nu.edu.kz, ISSAI/NU) before redistributing."
countries: ["[[Kazakhstan]]", "[[Uzbekistan]]", "[[Kyrgyzstan]]", "[[Tajikistan]]", "[[Turkmenistan]]"]
regions: ["[[Central Asia]]"]
n_records: "115 items (95 foods × 3 portion sizes + 20 beverages × 1 serving)"
size: "190.9 MB PDF; 25 KB CSV"
formats: [pdf, csv]
has_ingredients: false
has_amounts: partial
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [item name (English), local names in Kazakh/Uzbek/Kyrgyz/Tajik/Turkmen, CAFD/CAFSD class name]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
  - region/central-asia
---
# Central Asian Digital Visual Food Atlas

> [!abstract] TL;DR
> A portion-size photo atlas from the Central Asian Food Innovation Lab (ISSAI, Nazarbayev University; Omarova et al., Nutrients 2025). It covers **115 foods and drinks eaten in Central Asia**:
> - **95 foods** are photographed at **small, average and large portions with measured weights**, e.g. pilaf 192/385/580 g, beshbarmak 194/365/541 g, lagman 173/343/515 g.
> - **20 beverages** are shown at one serving in ml, e.g. kymyz 206 ml, shubat 166 ml.
> - Each item has **local names in Kazakh, Uzbek, Kyrgyz, Tajik and Turkmen** plus a one-line description.
>
> It has no nutrients, but it is the only source of **typical serving weights** for Central Asian dishes. Combined with per-100 g tables ([[Kyrgyzstan Food Composition Table]]) it lets the agent estimate nutrients per plate, and its multilingual names are a synonym table for 5 countries.

## Access
| | |
|---|---|
| Availability | open-download (GitHub, but the PDF was removed from the repo head and is only in git history / LFS) |
| Link | https://github.com/Central-Asian-Food-Innovation-Lab/Central-Asian-Digital-Visual-Food-Atlas |
| Accessed? | true |
| How | `git clone` + `git fetch --unshallow` → `git log -- Atlas.pdf` → LFS pointer of commit `0ab8965` → `curl https://media.githubusercontent.com/media/<org>/<repo>/<sha>/Atlas.pdf` → `pdftotext -layout` per page → parser |
| Downloaded | `Data/central-asian-digital-visual-food-atlas/Atlas.pdf` (122 pp), `extracted/atlas_items.csv`, `pages/p-008.png` (sample page render) |

## Tables & columns
### `extracted/atlas_items.csv` (115 rows)
| column | type | meaning | example |
|---|---|---|---|
| `page` | int | atlas page | `8` |
| `section` | str | 9 sections: main dishes 19, beverages 20, salads 15, desserts 13, meat dishes 12, bakery & bread 12, soups 10, snacks 10, side dishes 4 | `MAIN DISHES` |
| `item` | str | English item name | `Pilaf` |
| `name_kazakh` / `name_uzbek` / `name_kyrgyz` / `name_tajik` / `name_turkmen` | str | "Alternative/Local names" with language tags Kaz/Uzb/Kir/Tgk/Tuk (present for 83–85 items) | `Palau` / `Osh` / `Paloo` / `Oshi palav` / `Palaw` |
| `description` | str | one-line description | `A flavorful rice dish cooked with meat, vegetables, and spices` |
| `small`, `average`, `large` | float | portion weights (small ≈ 0.5×, large ≈ 1.5× average per the paper) | `192`, `385`, `580` |
| `unit` | str | `g` (95 foods) or `ml` (20 beverages; only `average` filled) | `g` |

Sample: `Data/central-asian-digital-visual-food-atlas/sample.csv` · full profile: `Data/central-asian-digital-visual-food-atlas/schema.md`

## Countries & cultures covered
- The atlas is regional, with no per-item country; local names are given for all 5 countries on 83–85 items: [[Kazakhstan]], [[Uzbekistan]], [[Kyrgyzstan]], [[Tajikistan]], [[Turkmenistan]].
- **Traditional Central Asian items:** pilaf/plov, beshbarmak, lagman, fried lagman, dumplings (tushpara/chuchvara), naryn, kuyrdak, orama, kazan kebab, koktal, shashlyk, lula kebab, shorpa, kespe, manpar, sorpa, achichuk salad, tandyr nan, bauyrsak, samsa, zheti kulshe, bukteme, qurt, irimshik, balqaymaq, zhent, chak-chak, kymyz, shubat, tan.
- **Russian/Soviet items:** borscht, okroshka, golubtsy, beef stroganov, vinegret, olivier, herring salad, syrniki, bliny, kompot, kefir, cottage cheese.
- **Global items:** pizza, burger, ramen, udon, tom yam, Caesar salad, doner, sodas, cappuccino.

## Ingredients, amounts, cooking method
- **Amounts:** serving weights per whole dish (g/ml), not per ingredient (`has_amounts: partial`).
  - Examples: kuyrdak 192/373/487 g · samsa 110/204/292 g · beshbarmak 194/365/541 g · kymyz 206 ml.
- **Ingredients:** only implicit in descriptions, e.g. "finely chopped boiled meat, noodles, and onion sauce".
- **Cooking method:** none.
- **Nutrition:** none; the paper says it is "in progress".

## Linking to other datasets
- Items were chosen from the [[Central Asian Food Dataset]] (CAFD/CAFSD) class lists, so names map almost 1:1 (plov, beshbarmak, naryn, kuyrdak, orama, achichuk, bauyrsak, samsa, irimshik, kurt/qurt, kymyz). The atlas turns an image-recognised dish into grams.
- Grams × per-100 g composition from [[Kyrgyzstan Food Composition Table]] (beshbarmak, lagman, manty, plov, oromo, shorpo, koumiss) gives nutrients per serving.
- Local-name columns can resolve dish mentions in other datasets (e.g. [[WorldCuisines]], [[BLEnD]]) across Kazakh/Uzbek/Kyrgyz/Tajik/Turkmen spellings.

## Versions
- There is one atlas edition (2025). The PDF was uploaded twice via Git LFS (commits edd8f04 and 0ab8965, slightly different sizes); we used the later one. It is currently deleted from the repo head.

## Caveats
- The file was removed from the public head of the repository. Its status (withdrawn? moved?) is unclear, so confirm with the authors before sharing or publishing derived data.
- Parsing notes:
  - Beverage names were separated from descriptions heuristically.
  - A few local-name cells are imperfect, e.g. bauyrsak's Kyrgyz cell merges "(Kaz" text.
  - Weights with decimals are as printed (e.g. eastern sweets 126.9/254.2/381.8 g).
- Portions are standardised multiples (0.5×/1.5×), not survey-derived. Bones and inedible parts are not separated.
