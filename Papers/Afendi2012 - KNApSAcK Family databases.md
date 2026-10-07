---
title: "KNApSAcK family databases: integrated metabolite-plant species databases for multifaceted plant research"
citekey: "Afendi2012"
authors: ["F. M. Afendi", "T. Okada", "M. Yamazaki", "A. Hirai-Morita", "Y. Nakamura", "K. Nakamura", "S. Ikeda", "H. Takahashi", "M. Altaf-Ul-Amin", "L. K. Darusman", "K. Saito", "S. Kanaya"]
year: 2012
published: 2011-11-28
venue: "Plant and Cell Physiology 53(2):e1"
peer_reviewed: true
url: "https://doi.org/10.1093/pcp/pcr165"
arxiv: ""
doi: "10.1093/pcp/pcr165"
pdf: ""
pdf_url: "https://academic.oup.com/pcp/article-pdf/53/2/e1/17115220/pcr165.pdf"
datasets: ["[[KNApSAcK Family]]"]
topics: [cultural-food-health]
questions: [Q2, Q3]
relevance: core
cites: []
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/2
  - q/3
---
# KNApSAcK family databases: integrated metabolite-plant species databases for multifaceted plant research

> [!warning] Read from the abstract only
> The OUP PDF and HTML (bronze OA) returned HTTP 403 to scripted requests, and the article is not in PMC. This
> note uses the Europe PMC abstract. For the full text, save the PDF manually to
> `Attachments/Afendi2012/Afendi2012.pdf`.

> [!abstract] TL;DR
> The NAIST (Kanaya lab) team describes the KNApSAcK family: the **Core** species–metabolite database plus
> "multifaceted plant usage" databases keyed on species names. These are a WorldMap of medicinal/edible plants
> by geographic zone, a Biological Activity DB, and the formula databases of Japanese **Kampo** and Indonesian
> **Jamu** medicine. Linking them lets a plant's cultural use be traced to its metabolites.

## What was built
- **Dataset(s):** [[KNApSAcK Family]]
- **Sources & construction:** species–metabolite relationships and plant usage collected from the scientific
  literature; all databases linked through species names (details in the full text, not read).
- **Size & coverage (2012):** Core 101,500 species–metabolite relationships (20,741 species, 50,048
  metabolites); WorldMap 41,548 zone–plant pairs (222 geographic zones, 15,240 medicinal/edible plants);
  KAMPO 336 formulae with 278 medicinal plants; JAMU 5,310 formulae with 550 medicinal plants; Biological
  Activity DB 2,418 activities and 33,706 plant–activity pairs.
- **Evaluation / applications:** metabolite search by accurate mass, formula, name or MS spectra; degree
  distribution analysis of the binary relations.

## Key findings
1. The Core DB links 20,741 species to 50,048 metabolites through 101,500 relationships.
2. WorldMap relates 15,240 medicinal/edible plants to 222 geographic zones (41,548 pairs).
3. JAMU has 5,310 formulae using 550 plants; KAMPO has 336 formulae using 278 plants.
4. From the degree distributions, the authors predict at least 1,060,000 metabolites across all plants.

## Relevance to research questions
### Q2: Cultural ingredient datasets
WorldMap/KNApSAcK World records, per country, whether a species is used as **food** or **medicine**. Today it
has 76,100 records in 229 countries. JAMU gives Indonesian formula compositions.

See [[Q2 Cultural ingredient datasets]]

### Q3: Food compound & health-effect datasets
Species → metabolites (Core) and plant → biological activity, plus Jamu efficacy claims. A traditional-claim
and metabolite-presence layer, joinable by species name or CAS.

See [[Q3 Food compound & health-effect datasets]]

## Limitations / caveats
- Full text not read (403). Methods and quality control are unverified here.
- The web databases are browse-only, with no bulk download. Licence is CC BY-NC-ND 4.0 per the current terms.
- Statistics are from 2011 and have grown since (see [[KNApSAcK Family]]).

## Related work to follow
![[Backlog.base#Cited by this paper]]
