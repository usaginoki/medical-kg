---
title: "UNaProd: A Universal Natural Product Database for Materia Medica of Iranian Traditional Medicine"
citekey: "Naghizadeh2020"
authors: ["Ayeh Naghizadeh", "Donya Hamzeheian", "Shaghayegh Akbari", "Fahimeh Mohammadi", "Tohid Otoufat", "Saeme Asgari", "Azadeh Zarei", "Samane Noroozi", "Najmeh Nasiri", "Mahdi Salamat", "Reza Karbalaei", "Mehdi Mirzaie", "Hossein Rezaeizadeh", "Mehrdad Karimi", "Mohieddin Jafari"]
year: 2020
published: 2020-05-13
venue: "Evidence-Based Complementary and Alternative Medicine 2020:3690781"
peer_reviewed: true
url: "https://doi.org/10.1155/2020/3690781"
arxiv: ""
doi: "10.1155/2020/3690781"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC7243028?pdf=render"
datasets: ["[[UNaProd]]"]
topics: [cultural-food-health]
questions: [Q2]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - tradmed/persian
  - region/middle-east
---
# UNaProd: A Universal Natural Product Database for Materia Medica of Iranian Traditional Medicine

> [!abstract] TL;DR
> The authors digitise *Makhzan al-Advieh* (Aghili, 1769), the largest classical Persian drug encyclopedia,
> into a database of 2,696 monographs (herbal, animal, mineral, compound). They combine text mining of the
> Persian text with manual review by a committee of Persian-medicine specialists. Each monograph records Mizaj
> (temperament), actions and uses, adverse effects, correctives, dose and substitutes. Monographs are linked to
> the IrGO ontology (for Mizaj) and to CMAUP (for molecular data on plants).

## What was built
- **Dataset(s):** [[UNaProd]] (the paper describes v1.0; the vault note describes the live v1.2 Beta with 3,413 monographs)
- **Sources & construction:** the text of *Makhzan al-Advieh* was normalised with the Hazm Persian NLP package.
  Monographs and their sections were split with regular expressions keyed on the author's section words
  (identity, Mizaj, actions & uses, adverse effects, refinement, dosage, substitute). Synonyms were extracted
  after language or scholar names. Origin was assigned by keyword frequency in the identity text. Scientific
  names came from two sources: SciResource1 (Ghahreman & Okhovvat, *Matching the Old Medicinal Plant Names with
  Scientific Terminology*) and the appendix of the corrected edition. Mizaj type and degree were mapped to IrGO.
  Plants with scientific names were linked to CMAUP. Everything was then manually checked against the
  lithograph print.
- **Size & coverage:** 1,741 primary monographs, expanded to 2,696 tuples by splitting parts and preparations
  (e.g. quince blossom, seed, sweet/sour fruit, oil). Culture: Iranian (Persian) traditional medicine. Synonyms
  span ~70 languages and dialects, mainly Persian, Arabic, Indian and Greek.
- **Evaluation / applications:** descriptive statistics only (origins, Mizaj distribution, plant families); a
  PHP/MySQL web interface with search. It is intended as a base for an ITM systems-pharmacology platform
  (drug → target → disease).

## Key findings
1. Herbs dominate. Animal-origin and mineral-origin drugs are about **17%** and **14%** of monographs; 6
   drugs (0.4%) have other or ambiguous origins.
2. Aghili gives a Mizaj for **1,421 of 1,741** primary monographs (including 384 views quoted from other
   scholars). **1,976 of 2,696** tuples carry Mizaj information.
3. Mizaj distribution: **hot-dry 55.7%**, cold-dry 16.5%, hot-wet 8.1%, cold-wet 5.4%, balanced 4.8%, hot 3.6%,
   Morakkab al-Ghovaa 2.3%, dry 1.7%, cold 1.6%, wet 0.4%. Animal drugs are mostly hot-wet; minerals are dry,
   cold-dry or balanced.
4. **851** monographs have scientific names in the figure (621 herbal, 181 animal, 49 mineral). The text also
   reports 1,822 monographs with a name from at least one resource. Plant names fall into 66 (SciName1) and
   114 (SciName2) families, led by Leguminosae, Compositae, Lamiaceae and Apiaceae.
5. Degrees are often missing: of 1,249 hotness and 441 coldness degrees, 448 and 227 are unspecified. Of 1,480
   dryness and 386 wetness degrees, 442 and 148 are unspecified.

## Relevance to research questions
### Q2: Cultural ingredient datasets
This is the only structured source for the **Persian humoral classification of foods and medicinal
ingredients** (hot/cold, wet/dry, with degrees), along with correctives and temperament-dependent dosing.
Those beliefs still shape everyday dietary advice in Iran, and through Unani medicine in South Asia. Many
monographs are common foods and spices, so an agent can use them to explain or respect local beliefs about why
a food suits or harms a person. Molecular grounding goes through the CMAUP links.

See [[Q2 Cultural ingredient datasets]]

## Key figures & tables
*Table 1 (paper): ITM definitions. Qualities (hot, cold, wet, dry); active qualities (hot/cold) vs passive
(wet/dry); Mizaj type = balanced or unbalanced, one quality or an active + passive pair; Mizaj degree 1–4, each
min/medium/max; DNS = degree not specified.*

## Limitations / caveats
- The core text fields are in classical Persian. At the time of the paper only Mizaj was linked to English
  ontology terms.
- It relies on a single 18th-century source, supplemented by quoted scholars. The claims are traditional, not
  clinically validated.
- Scientific-name matching of historical drug names is uncertain and incomplete.
- The URL given in the paper (jafarilab.com/unaprod) no longer hosts the database; it moved to unaprod.com. No
  bulk download is offered.

## Related work to follow
![[Backlog.base#Cited by this paper]]
