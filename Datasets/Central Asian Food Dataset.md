---
title: "Central Asian Food Dataset"
slug: central-asian-food-dataset
kind: [food]
version: "CAFSD (Central Asian Food Scenes Dataset, 2025): 21,306 images, 69,865 boxes, 239 classes. Also covers its predecessor CAFD (2023, 42 classes)."
previous_versions: "CAFD v1 (2023): 16,499 images (16,402 on HF), 42 dish classes, classification crops; GitHub IS2AI/Central-Asian-Food-Dataset (formerly Kazakh-Food-Dataset), HF issai/Central_Asian_Food_Dataset"
papers: ["[[Karabay2023 - Central Asian Food Dataset]]", "[[Karabay2025 - Central Asian Food Scenes Dataset]]"]
url: "https://huggingface.co/datasets/issai/Central_Asian_Food_Scenes_Dataset"
license: "CAFSD: CC BY 4.0 (HF card). CAFD: CC BY-NC 4.0 (HF card); the GitHub repo LICENSE and paper say MIT."
availability: open-download
access_link: "https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/CAFSD/CAFSD.zip"
accessed: partial
access_method: [huggingface, website-download, github]
access_date: 2026-09-30
access_notes: "Images were deliberately not bulk-downloaded (CAFSD.zip 3.1 GB, HF repo 8.9 GB; CAFD.zip 1.0 GB). We took all 21,306 CAFSD YOLO label files by HTTP range requests on CAFSD.zip: the label members sit in 3 contiguous byte ranges (~2 MB), which we parsed locally. We also took the class list (data.yaml), the full CAFD file manifest from the HF API (16,402 images with split/class), and 10 sample images (6 CAFD, 4 CAFSD). HF per-file label download was rate-limited (~6.5k files in 15 min), so we switched to the zip."
countries: ["[[Kazakhstan]]", "[[Uzbekistan]]", "[[Kyrgyzstan]]", "[[Tajikistan]]", "[[Turkmenistan]]"]
regions: ["[[Central Asia]]"]
n_records: "CAFSD 21,306 images / 69,865 box annotations / 239 classes; CAFD 16,402 images (HF) / 42 classes"
size: "~12 MB downloaded (labels CSV 9 MB, labels tar 2.6 MB, manifests, 10 images); full images 3.1 GB (CAFSD zip) + 1.0 GB (CAFD zip)"
formats: [jpg, yolo-txt, csv]
has_ingredients: false
has_amounts: "no"
has_cooking_method: "no"
has_nutrition: false
body_effect: ""
body_effect_how: ""
join_keys: [class name (transliterated dish name, e.g. beshbarmak, kuyrdak, naryn, kymyz-kymyran), FAO/WHO GIFT coarse class]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
found_by: [search/food, search/regions]
tags:
  - type/dataset
  - kind/food
  - q/1
  - access/accessed
  - access/open
  - region/central-asia
---
# Central Asian Food Dataset

> [!abstract] TL;DR
> Food-image datasets from ISSAI (Nazarbayev University, Astana), the only substantial Central Asian dish inventory in the vault.
> - **CAFD (2023):** 16.5k cropped images of **42 national dishes**, e.g. beshbarmak with/without kazy, kuyrdak, naryn, plov, manty, samsa, lagman variants, baursak, kurt, irimshik, kymyz/shubat, chak-chak, sheep head, nauryz kozhe.
> - **CAFSD (2025), the latest:** extends it to **21,306 real meal-scene photos with 69,865 bounding boxes over 239 classes**. The classes follow the FAO/WHO GIFT ontology (18 coarse groups) and cover all 42 CAFD dishes plus ingredients, sides and drinks seen on Central Asian tables (tomato, parsley, bread, tea, tomato-cucumber salad achichuk, taba-nan, hinkali, borsch, olivie, vareniki, pickles).
>
> There are no recipes or nutrients, but it tells the agent **which dishes and co-occurring foods appear on real Kazakh and wider Central Asian plates**, and CAFSD's co-occurrence gives meal composition.

## Access
| | |
|---|---|
| Availability | open-download. CAFSD: HF `issai/Central_Asian_Food_Scenes_Dataset` + direct zip. CAFD: HF `issai/Central_Asian_Food_Dataset` + direct zip. Pretrained weights (ResNet152, EfficientNet-b4, YOLOv8n–x) are also offered. |
| Link | https://huggingface.co/datasets/issai/Central_Asian_Food_Scenes_Dataset · https://github.com/IS2AI/Central-Asian-Food-Dataset · https://issai.nu.edu.kz/wp-content/themes/issai-new/data/models/CAFSD/CAFSD.zip |
| Accessed? | partial (all annotations and class lists; images only as a sample) |
| How | `git clone --depth 1` (CAFD repo: README, train/test scripts). HF API → file manifests + `data.yaml`. `remotezip` central directory + 3 HTTP range requests on CAFSD.zip → 21,306 label files. `curl` for 10 sample images. |
| Downloaded | `Data/central-asian-food-dataset/`: `cafsd_annotations.csv`, `cafsd_class_counts.csv`, `cafsd_labels_yolo.tar.gz`, `hf/cafsd_classes.csv`, `hf/cafsd_data.yaml`, `hf/cafd_image_manifest.csv`, `hf/cafd_class_counts.csv`, `hf/sample_images/{cafd,cafsd}/` |

## Tables & columns
### `cafsd_annotations.csv` (69,865 rows = one bounding box each; built from the YOLO label files)
| column | type | meaning | example |
|---|---|---|---|
| `split` | str | train 55,422 / valid 7,062 / test 7,381 boxes (17,046 / 2,084 / 2,176 images) | `train` |
| `image_label_file` | str | YOLO label file name (= image name with `.txt`; Roboflow export names) | `…mp4-10_jpg.rf.2a68….txt` |
| `class_id` | int | index into the 239 names in `data.yaml` | `14` |
| `class_name` | str | fine class | `bauyrsak` |
| `x_center`, `y_center`, `width`, `height` | float | YOLO box, normalised 0–1 | `0.42`, `0.48`, `0.54`, `0.78` |

### `cafsd_class_counts.csv` (239 rows)
- Columns: `class_id`, `class_name`, `instances`, `images`.
- Most frequent: tomato 3,050 · parsley 2,186 · salad fresh 1,487 · onion 1,291 · bread 1,208 · bauyrsak 941 · taba-nan 911 · tea 888 · plov 845.
- Rarest: karta 31 · pumpkin seeds 36.

### `hf/cafd_image_manifest.csv` (16,402 rows) and `hf/cafd_class_counts.csv` (42 rows)
- Columns: `path` (`train/plov/…jpg`), `split` (train/val/test), `class`.
- The 42 CAFD classes range from sheep-head (96 images) to taba-nan (919).
- The paper reports 16,499 images; the HF copy has 16,402 jpgs (excluding `__MACOSX` artefacts).

### `hf/cafsd_classes.csv` (239 rows)
`class_id`, `class_name`.

Sample: `Data/central-asian-food-dataset/sample.csv` · full profile: `Data/central-asian-food-dataset/schema.md`

## Countries & cultures covered
- **No per-image country label.**
  - The authors describe CAFD as dishes of **Central Asia**. The companion atlas paper lists [[Kazakhstan]], [[Uzbekistan]], [[Kyrgyzstan]], [[Tajikistan]] and [[Turkmenistan]].
  - Class names are Kazakh-centred transliterations: beshbarmak, kuyrdak, kazy-karta, nauryz-kozhe, shelpek, talkan-zhent, irimshik, kurt, kymyz-kymyran, taba-nan, kattama-nan, tushpara, sorpa/shorpa.
  - Images were scraped with multilingual queries (Kazakh, Russian, English…) from Google, Bing, Yandex, YouTube, Instagram and Facebook, plus own photos.
- **CAFD 42 dish classes:**
  - Achichuk, airan-katyk, asip, bauyrsak, beshbarmak (with/without kazy), chak-chak, cheburek, doner (lavash/nan), hvorost, irimshik
  - Kattama-nan, kazy-karta, kurt, kuyrdak, kymyz-kymyran, lagman (fried/with soup/without soup), manty, naryn, nauryz-kozhe, orama, plov, samsa
  - Shashlyk (chicken, chicken-v, kuskovoi, kuskovoi-v, minced meat), sheep-head, shelpek, shorpa, soup-plain, sushki, suzbe, taba-nan, talkan-zhent, tushpara (fried/with soup/without soup)
- **CAFSD adds 197 classes:**
  - Russian/Soviet dishes: borsch, olivie, okroshka, vareniki, syrniki, brizol
  - Caucasian: hachapuri, hinkali
  - Global foods: pizza, sushi, hamburger
  - Fruits, vegetables, herbs, nuts, dairy, drinks, sauces
  - Kazakh consumption context in the paper: kazy-karta is 6.9% of meat instances; kurt 15.7% and kymyz 15.6% of dairy instances.

## Ingredients, amounts, cooking method
- None as recipes. CAFSD boxes list the foods co-present in a scene: dish + bread + salad + tea + herbs. This is a proxy for meal composition, not ingredients.
- Some class names encode preparation: `lagman-fried` vs `lagman-w-soup`, `tushpara-fried`, `boiled chicken`, `fried fish`, `pickled cabbage`, `smoked fish`.

## Linking to other datasets
- Class names ↔ [[Kyrgyzstan Food Composition Table]] dishes (beshbarmak, manty, lagman, plov, oromo=orama, shorpo=shorpa, koumiss=kymyz) for per-100 g nutrients.
- Class names ↔ [[Central Asian Digital Visual Food Atlas]] portion weights. The atlas items were selected from the CAFD/CAFSD class lists, so names largely match: plov/pilaf, beshbarmak, naryn, kuyrdak, orama, achichuk, bauyrsak, irimshik, qurt, kymyz.
- Generic classes (tomato, onion, walnut, pomegranate…) ↔ [[USDA FoodData Central]] / [[FooDB]].

## Versions
- **CAFD (2023, Nutrients):** 42 classes, single-dish crops for classification. ResNet152 reaches 88.70% top-1. HF card license CC BY-NC 4.0.
- **CAFSD (2025, Scientific Reports):** scene images with multi-object boxes, 239 fine / 18 coarse classes, a superset of the CAFD dishes. YOLOv8x reaches mAP50 0.677 on test. HF card CC BY 4.0.
  - Images: 15,939 web-scraped, 2,324 everyday photos, 3,043 video frames.
  - This note describes CAFSD as the latest, with CAFD kept as the dish-classification predecessor.

## Caveats
- Images were not downloaded in bulk; get `CAFSD.zip` (3.1 GB) / `CAFD.zip` (1.0 GB) if the images themselves are needed.
- Most images are web-scraped, so this is not a dietary survey. Class frequencies reflect web and photo availability plus annotation choices, not intake.
- The licenses conflict: CAFD is MIT (repo/paper) vs CC BY-NC 4.0 (HF). The CAFSD article is CC BY-NC-ND vs the dataset card's CC BY 4.0.
- The smallest CAFSD class in the labels has 31 boxes (karta), below the paper's stated minimum of 40.
- Country attribution is at the regional level only and is Kazakhstan-centred.
