---
title: "TM-MC 2.0: an enhanced chemical database of medicinal materials in Northeast Asian traditional medicine"
citekey: "Kim2024"
authors: ["Sang-Kyun Kim", "Myung-Ku Lee", "Ho Jang", "Jeong-Ju Lee", "Sanghun Lee", "Yunji Jang", "Hyunchul Jang", "Anna Kim"]
year: 2024
published: 2024-01-16
venue: "BMC Complementary Medicine and Therapies 24:40"
peer_reviewed: true
url: "https://doi.org/10.1186/s12906-023-04331-y"
arxiv: ""
doi: "10.1186/s12906-023-04331-y"
pdf: ""
pdf_url: "https://europepmc.org/articles/PMC10790428?pdf=render"
datasets: ["[[TM-MC]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites: []
cited_by: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# TM-MC 2.0: an enhanced chemical database of medicinal materials in Northeast Asian traditional medicine

> [!abstract] TL;DR
> The Korea Institute of Oriental Medicine updates TM-MC, a manually curated database of the chemical compounds
> in medicinal materials listed in the Korean, Chinese and Japanese pharmacopoeias. Compounds are extracted by
> Korean-medicine experts from PubMed chromatography papers. Version 2.0 adds structures for every identified
> compound, ADME properties, STITCH targets, DisGeNET diseases and 5,075 prescriptions from Korean-medicine
> textbooks.

## What was built
- **Dataset(s):** [[TM-MC]]
- **Sources & construction:** PubMed was searched with pharmacopoeial material names plus chromatography
  keywords (PMIDs up to 32 M; up to 35 M for 45 materials). Experts read 10,373 articles and extracted compound
  names. Structures were drawn in ChemDraw and de-duplicated by InChIKey. PubChem CIDs were matched by InChIKey;
  properties computed with ChemAxon (QED drug-likeness, Veber's-rule OB). Targets come from STITCH v5.0 (Homo
  sapiens, matched on the first 14 InChIKey characters); diseases from DisGeNET v7.0. Prescriptions come from 2
  prescription and 5 internal-medicine textbooks used in Korean-medicine universities.
- **Size & coverage:** 635 materials (556 in the Chinese pharmacopoeia, 454 Korean, 192 Japanese), 34,107
  compounds (21,306 unique identified), 13,992 targets, 27,997 diseases, 5,075 prescriptions (2,393 unique names).
- **Evaluation / applications:** compared with TCMSP 2.3 and TCMID 2.0 on 387 shared materials, and on 350
  Chinese-pharmacopoeia marker compounds. Use case: compound–target–disease networks for prescriptions.

## Key findings
1. 16,030 of 21,306 identified compounds match a PubChem InChIKey exactly, and 18,317 on the first 14
   characters. 2,989 are newly reported compounds not found in PubChem.
2. 3,257 compound names could not be identified (typos or missing information). 9,544 compounds share IDs as
   synonyms.
3. Of 350 marker compounds, TM-MC misses 9, TCMSP 63 and TCMID 55.
4. 10,134 compounds are only in TM-MC; 5,449 of them come from articles published after 2014.
5. The three databases overlap little even for licorice and ginseng. TCMSP and TCMID contain compounds not
   retrievable from PubMed chromatography articles.

## Relevance to research questions
### Q2: Cultural ingredient datasets
The only resource here that names each material in Korean, Chinese and Japanese. It covers many foods used as
medicine in Northeast Asia (ginger, jujube, goji, cinnamon, hawthorn, turmeric, yam), with Korean-medicine
prescriptions that give dosages (e.g. ginger 3 pieces + jujube 2 pieces).

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
Literature-backed material → compound links (PMID per row) with InChIKey/CID, then STITCH targets and DisGeNET
diseases. The effect layer is predicted, not clinical.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- Only compounds reported in PubMed chromatography studies. Materials studied mainly in Chinese-language
  journals are under-covered.
- Targets and diseases are database-derived (STITCH/DisGeNET) rather than curated per material.
- Prescription indications were not yet included ("will be supplemented").
- The paper counts differ from the current download (649 materials in June 2026); the site updates monthly.

## Related work to follow
![[Backlog.base#Cited by this paper]]
