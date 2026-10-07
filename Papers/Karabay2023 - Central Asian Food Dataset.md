---
title: "A Central Asian Food Dataset for Personalized Dietary Interventions"
citekey: "Karabay2023"
authors: ["Aknur Karabay", "Arman Bolatov", "Huseyin Atakan Varol", "Mei-Yen Chan"]
year: 2023
published: 2023-03-31
venue: "Nutrients"
peer_reviewed: true
url: "https://doi.org/10.3390/nu15071728"
arxiv: ""
doi: "10.3390/nu15071728"
pdf: ""
pdf_url: "https://www.mdpi.com/2072-6643/15/7/1728/pdf?version=1680263206"
datasets: ["[[Central Asian Food Dataset]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/1
  - kind/food
  - region/central-asia
---
# A Central Asian Food Dataset for Personalized Dietary Interventions

> [!abstract] TL;DR
> The Central Asian Food Dataset (CAFD) is the first image dataset of Central Asian dishes: 16,499 images in 42 classes, such as plov, beshbarmak, manty, kazy-karta, kurt and kymyz. It was built at Nazarbayev University (ISSAI, Astana) by scraping search engines, social media and YouTube frames, then cropping by bounding box. It was released with ImageNet-transfer classifiers (best: ResNet152, 88.70% Top-1). It is a dish inventory of the region, but it has no ingredients, amounts or nutrients.

## What was built
- **Dataset(s):** [[Central Asian Food Dataset]] (CAFD; later extended by CAFSD, see [[Karabay2025 - Central Asian Food Scenes Dataset]])
- **Sources & construction:** The process had five steps. (1) The authors listed the most popular foods eaten in Central Asia. (2) They scraped Bing, Google, YouTube, Yandex, Instagram and Facebook with multilingual queries. Selenium scripts were used, and YouTube recipe videos were sampled at 1 fps with Roboflow to boost rare classes such as sheep head, asip and nauryz-kozhe. Exact duplicates were removed with HashImage. (3) Two annotators drew bounding boxes in Roboflow. (4) The boxes were cropped to one food per image. (5) The data was split about 70/15/15, by original image and by video so that no video leaks across splits.
- **Size & coverage:** 16,499 images, 42 classes and 99–922 images per class. The split is 11,008 train / 2,763 validation / 2,728 test. The classes are "national dishes unique to this region" (Kazakh-centred naming: beshbarmak, kazy-karta, kuyrdak, nauryz-kozhe, shelpek, irimshik, kurt, baursak, plus shared dishes such as plov, lagman, manty, samsa and shashlyk variants). The paper gives no per-country label for each class.
- **Evaluation / applications:** 10 CNNs (VGG-16, SqueezeNet, ResNet50/101/152, ResNeXt50, Wide ResNet-50, DenseNet-121, EfficientNet-b4) were trained on CAFD, on Food1K and on the combined CAFD+Food1K (1,042 classes).

## Key findings
1. ResNet152 was best on CAFD, with 88.70% Top-1 and 98.59% Top-5. EfficientNet-b4 was best on CAFD+Food1K, with 87.75% Top-1 and 98.01% Top-5.
2. Adding CAFD to Food1K slightly improved accuracy (for example ResNet50: 82.44% → 83.22% Top-1). The authors read this as no substantial class overlap: Central Asian dishes are missing from existing food datasets.
3. Some classes were recognised best: sushki, achichuk, sheep head, naryn and plov (precision 0.93–0.96). Visually similar shashlik variants (precision 0.66–0.79), asip vs kazy-karta, and lagman without soup were worst.
4. The authors stress why fine-grained classes matter for nutrition. Per 100 g, lean beef shashlik has 250 kcal and 15 g fat, chicken shashlik 180 kcal and 7 g fat, and mutton shashlik 290 kcal and 20 g fat.

## Relevance to research questions
### Q1: Cultural food datasets
CAFD is one of the few dish inventories of Central Asia (Kazakhstan-centred). It gives a canonical list of 42 regional dish names, with transliterations the agent can match on, and an image classifier for photo-based food logging. It carries no recipes, ingredients or nutrients, so it must be joined by dish name to composition data such as [[Kyrgyzstan Food Composition Table]] (beshbarmak, manty, lagman, plov, oromo) to support dietary advice.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- There are only 42 classes and they are unbalanced (99–922 images). The images are web-scraped; the paper's own figure images are CC BY-NC-ND, while the repo code is MIT (the HF card says CC BY-NC 4.0).
- There is no country-of-origin label for each dish, and no ingredients, portions or nutrients.
- Classes for similar-looking foods (shashlyk variants, lagman types) are confusable, which limits calorie estimation.

## Related work to follow
![[Backlog.base#Cited by this paper]]
