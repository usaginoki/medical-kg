---
title: "Improved food image recognition by leveraging deep learning and data-driven methods with an application to Central Asian Food Scene"
citekey: "Karabay2025"
authors: ["Aknur Karabay", "Huseyin Atakan Varol", "Mei-Yen Chan"]
year: 2025
published: 2025-04-23
venue: "Scientific Reports"
peer_reviewed: true
url: "https://doi.org/10.1038/s41598-025-95770-9"
arxiv: ""
doi: "10.1038/s41598-025-95770-9"
pdf: ""
pdf_url: "https://www.nature.com/articles/s41598-025-95770-9.pdf"
datasets: ["[[Central Asian Food Dataset]]"]
topics: [cultural-food-health]
questions: [Q1]
relevance: core
cites:
  - "[[Central Asian Food Dataset (candidate)]]"
cited_by:
  - "[[Omarova2025 - Central Asian Visual Food Atlas]]"
cited_by_count: 1
tags:
  - type/paper
  - relevance/core
  - q/1
  - kind/food
  - region/central-asia
---
# Improved food image recognition by leveraging deep learning and data-driven methods with an application to Central Asian Food Scene

> [!abstract] TL;DR
> The Central Asian Food Scenes Dataset (CAFSD) extends CAFD from single-dish classification to multi-item food scenes. It has 21,306 images with 69,856 bounding-box instances in 239 fine classes grouped into 18 coarse classes. The ontology was benchmarked on the FAO/WHO GIFT food categories. The dataset covers local Kazakh/Central Asian dishes and the Western, Mediterranean, Chinese and other foods eaten in the region. YOLOv8 detectors reach test mAP50 of 0.677.

## What was built
- **Dataset(s):** [[Central Asian Food Dataset]] (CAFSD is the scene/detection extension of CAFD; see [[Karabay2023 - Central Asian Food Dataset]])
- **Sources & construction:** 15,939 web-scraped images (Google, YouTube, Yandex), 2,324 of the authors' own everyday-life photos and 3,043 video frames at 1 fps. Duplicates were removed with Hash Image, and images under 30 kB were replaced by further scraping. Annotation was done in two stages in Roboflow: first 18 coarse classes (vegetables, baked flour products, cooked dishes, fruits, herbs, meat dishes, desserts, salads, sauces, drinks, dairy, fast food, soups, sides, nuts & seeds, pickled/fermented, egg products, cereals), then 239 fine classes. The ontology follows the FAO/WHO Global Individual Food consumption data Tool (GIFT).
- **Size & coverage:** 21,306 images and 69,856 instances (the introduction says 69,865). There are 40–3,050 instances per class, and most scenes have fewer than 15 boxes. The split is 17,046 / 2,084 / 2,176 images (55,422 / 7,062 / 7,381 instances), with at least 5 instances per class in each split. There is no per-country breakdown. The discussion benchmarks against Kazakhstan national consumption statistics.
- **Evaluation / applications:** YOLOv8 n/s/m/l/x, pretrained on COCO, trained for 150 epochs at 640 px on a V100. The paper also analyses the class distribution in meat and dairy categories.

## Key findings
1. The best model is YOLOv8x (about 68 M parameters), with mAP50 0.699 / 0.677 and mAP50-95 0.601 on the test set (validation / test). Accuracy rises with model size, and validation and test scores are close.
2. Among meat instances, beef/lamb shashlik is 11.9%, chicken shashlik 9.5%, sausages 8.8%, fried beef/lamb 8.4% and horse-meat kazy-karta 6.9%. This matches beef being the most consumed meat in Kazakhstan (24.68 kg per capita in 2023).
3. Among dairy instances, smetana is 18.4%, kurt 15.7%, kymyz/kymyran 15.6%, cheese 14.4%, irimshik 9.2%, butter 8.1%, suzbe 6.7% and airan-katyk 5.6%. Kazakhstan's per capita dairy consumption was 227.2 kg in 2023.
4. mAP falls as the number of boxes per image grows and as boxes shrink. Intra-class variation (cooking styles) is the main source of error.
5. Planned next steps: link images to regional food composition databases and a codebook of macro/micronutrients, portion size and preparation method.

## Relevance to research questions
### Q1: Cultural food datasets
CAFSD gives a 239-class Central Asian food vocabulary in a GIFT-aligned hierarchy. It mixes national dishes (beshbarmak, kazy-karta, kuyrdak, naryn, baursak, kurt, irimshik, kymyz, shorpa) with the imported foods people in the region actually eat. This is useful for recognising what a Central Asian user eats from a photo and for mapping to FAO/WHO GIFT food groups. Like CAFD, it has no recipe, amount or nutrient fields.

See [[Q1 Cultural food datasets]]

## Limitations / caveats
- The images are mostly web-scraped, with no country or ethnicity labels. Classes are unbalanced (40–3,050 instances).
- Beef and lamb are merged because they cannot be told apart visually. Nutrition is not yet linked.
- The article is CC BY-NC-ND 4.0. The HF dataset card says CC BY 4.0 (the dataset licence differs from the article licence).

## Related work to follow
![[Backlog.base#Cited by this paper]]
