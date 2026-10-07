---
title: "Perspectives on Cross-Lingual Consistency in LLMs for Medical Questions"
citekey: "Bui2026"
authors: [Minh Duc Bui, Mario Sanz-Guerrero, Abteen Ebrahimi, Sagi Shaier, Peter Herbert Kann, Manuel Mager, Katharina von der Wense]
year: 2026
published: 2026-09-07
venue: "EMNLP 2026"
peer_reviewed: true
url: "https://arxiv.org/abs/2609.07687"
arxiv: "2609.07687"
doi: ""
pdf: "[[Bui2026.pdf]]"
pdf_url: "https://arxiv.org/pdf/2609.07687"
datasets: []
topics: [kg-medical-eval]
questions: [Q7, Q8]
relevance: adjacent
found_by: [search/culture-cued-cases, search/cue-injection]
added: 2026-10-07
cites:
  - "[[Adilazuarda2024 - Survey on measuring culture in LLMs]]"
  - "[[CMB (CMB-Clin)]]"
  - "[[CalvoBartolome2025 - Discrepancy detection in multilingual QA]]"
  - "[[Dey2025 - Beyond the Rubric]]"
  - "[[Ferrazzi2026 - Multilingual medical reasoning for QA]]"
  - "[[Goenaga2024 - CasiMedicos explanatory argument extraction]]"
  - "[[HealthBench]]"
  - "[[Hershcovich2022 - Challenges in cross-cultural NLP]]"
  - "[[Jiang2025 - JMedBench]]"
  - "[[Jin2024 - XLingHealth cross-lingual healthcare queries]]"
  - "[[Liu2025a - Culturally aware and adapted NLP survey]]"
  - "[[MMedBench]]"
  - "[[Matos2024 - WorldMedQA-V]]"
  - "[[Naous2023 - CAMeL cultural bias in LLMs]]"
  - "[[Nimo2025 - Africa Health Check]]"
  - "[[Peters2025 - Culturally appropriate conversational AI for health]]"
  - "[[Restrepo2025 - Multi-OphthaLingua]]"
  - "[[Rezaei2026 - Counterfactual Cultural Cues in Medical QA]]"
  - "[[Schlicht2025 - Cross-lingual consistency of health answers]]"
  - "[[Wang2024d - Apollo and XMedBench]]"
  - "[[Xu2026 - Language shapes mental health evaluations]]"
  - "[[Yizhen2024 - ChatGPT on TCM knowledge]]"
  - "[[Zeng2025 - Geographically tailored colorectal screening advice]]"
  - "[[Zheng2024 - Personas in system prompts]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/7
  - q/8
  - cue/country
  - eval/human
  - region/europe
  - region/americas
---
# Perspectives on Cross-Lingual Consistency in LLMs for Medical Questions

> [!abstract] TL;DR
> A position paper with a survey. It sorts multilingual medical NLP into a **consistency** stance (one correct answer
> in every language) and an **adaptation** stance (the answer may depend on cultural context), and names three gaps,
> one of them the lack of a benchmark that separates the two kinds of item. A one-question survey of 348
> professionals in Germany, Spain and the US finds anthropologists for adaptation (80–82%) and medical and NLP
> respondents split. Persona-prompted LLMs overstate support for consistency. No dataset is built.

## What was built
- **Literature synthesis** of two stances (§3) and three gaps (§3.3).
- **Stakeholder survey** (§4): one forced-choice question, 348 respondents, 3 professions × 3 countries.
- **LLM simulation** (§5): the same question put to 11 open-weight models under profession and country personas.
- **No benchmark, no item-level data.** The survey asks about the stance in general, not about specific medical
  questions.

![[Bui2026-fig-01-p1.png]]
*Figure 1: the two stances in prior work and what the paper adds.*

## The two stances and who is assigned to each
The paper's own definitions: consistency "treats correct answers as language-invariant"; adaptation "treats them as
partly contingent on cultural context". Adaptation "can mean content (what is said) and communication (how it is
formulated)".

| Stance | Sub-group | Works assigned | Paper's point |
|---|---|---|---|
| Consistency | Translated benchmarks | MedExpQA (Alonso 2024); CasiMedicos (Goenaga 2024; Sviridova 2024); JMedBench (Jiang 2025); XLingHealth (Jin 2024); Apollo / XMedBench Hindi and Arabic splits (Wang 2024b); Ferrazzi 2026 ([[MedQA]] and [[MedMCQA]] into Italian and Spanish); [[Matos2024 - WorldMedQA-V]] (named in the introduction) | Gold answers are inherited from the source language; motivation is data scarcity, "rarely accompanied by deeper justification" |
| Consistency | Cross-lingual consistency audits | Schlicht 2025 (EN, DE, TR, ZH health questions); Xu & Hu 2026 (mental health, ZH vs EN) | Divergence from English or a reference "is treated as model failure" |
| Consistency | Demographic injection | [[Shaier2023 - Demographic effects on biomedical QA]]; [[Rawat2024 - DiversityMedQA]]; [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA]] | Any output change after inserting a cue is read as bias; "consistency is assumed rather than proven" |
| Adaptation | Conceptual | Hershcovich 2022; Liu 2025; Adilazuarda 2024 | Culture is not reducible to language; benchmarks do not transfer cleanly |
| Adaptation | Native resources | XMedBench (four native languages); [[MMedBench]]; Multi-OphthaLingua (Restrepo 2025) | Build from native exam banks or native clinicians, not translations |
| Adaptation | Medical content | [[CMB (CMB-Clin)]] (TCM); Yizhen 2024 (TCM knowledge of ChatGPT); [[Zeng2025 - Geographically tailored colorectal screening advice]]; [[Dey2025 - Beyond the Rubric]] (vs [[HealthBench]]); [[Nimo2025 - Africa Health Check]]; Calvo-Bartolomé 2025 | "the correct answer can differ across settings" |
| Adaptation | Communication | Peters 2025 (workshops in Latin America) | How to say it: family as decision unit, logistics, material constraints |

Their motivating example of legitimate variation is osteoporosis guidelines: the US guideline combines bone density
with FRAX (~10 variables), German-speaking countries use a tool with ~50 additional variables.

## Stated gaps (§3.3)
1. **Stakeholders are absent:** most papers "assume rather than measure the preferences of the populations".
2. **No outcome evidence:** "neither stance has empirically tested whether consistency or adaptation actually leads
   to better user outcomes."
3. **No way to tell item types apart.** Exact wordings in the paper:
   - Abstract: "no benchmarks capable of distinguishing universally correct from culture-specific cases".
   - Introduction: "no benchmark distinguishes items that should be consistent (e.g., drug mechanisms) from those
     that may adapt (e.g., local guidelines)."
   - §3.3: "The field of medical NLP still lacks research on which specific items consistency is expected or
     adaptation appropriate for, and it is still unknown to which degree NLP systems are able to make this
     distinction."
   - Conclusion: "no benchmark separates items that should be consistent from those that should adapt."

The paper addresses only gap 1.

## Survey design
- **Sample:** 348 respondents (the PDF says 348 in the abstract, §1, §4.2 and Appendix A.4, and Table 1 sums to 348;
  the arXiv listing's abstract says 356).
- **Recruitment:** professional networks and mailing lists, plus Prolific with profession screening, a domain
  question, and a verification item for NLP ("Attention is all you [MASK]") and anthropology (subfield in free text).
  Prolific pay $16.60/hour; IRB approval.
- **Languages:** English, Spanish, German; translations "verified by native speakers".
- **The single question** (Figure 5 of the paper): an automated system gives different answers to an identical medical
  question depending on the language. Which view do you support?
  1. "The language in which the question is asked should not influence the answer, as it should be based exclusively
     on the current state of scientific knowledge."
  2. "Language is part of cultural identity. Cultural identity also implies different concepts of illness, healing,
     and health. Accordingly, the answer should refer to the medical practices applicable within the cultural
     framework to which the language of the question belongs."
  3. Other (free text; mapped to 1 or 2 where possible, otherwise excluded, < 5%).

| Participants (Table 1) | Anthropology | Medical | NLP |
|---|---|---|---|
| Germany | 17 | 60 | 53 |
| Spain | 20 | 57 | 21 |
| USA | 20 | 53 | 47 |
| Total | 57 | 170 | 121 |

## Key findings
1. **Anthropologists favour adaptation everywhere:** 82% (DE), 80% (ES), 80% (US); all significant against 50%.
2. **Medical professionals are split and differ by country:** consistency 65% (DE, the only significant
   non-anthropology cell), 53% (ES), 43% (US). US vs Germany differs significantly (two-sided z-test, p < 0.05).
3. **NLP researchers lean mildly to consistency:** 62%, 62%, 60%; none significant.
4. **PubMed check:** the share of 2015–2025 single-country papers with a Culture MeSH term ranks the same way as
   medical support for adaptation: Germany 0.29%, Spain 0.37%, USA 0.46%.
5. **Free text (44 relevant comments of 60):** the most common theme is "keep content, adapt communication" (13),
   then "illness is culturally situated" (8), "language ≠ culture" (8), "adaptation risks harmful bias" (7).
6. **Persona-prompted LLMs overstate consistency** (Table 2 below) and show no country effect: under English prompts
   the medical persona picks consistency 91% (US), 87% (DE), 81% (ES), where US clinicians chose it 43%.
7. **Prompt language shifts LLMs the opposite way to humans:** English prompts give the most consistency, German the
   least, although German clinicians were the most pro-consistency group.
8. **Without a persona** models disagree with each other: e.g. Llama-3.3-70B answers consistency 20/0 in English,
   aya-expanse-32b 0/20 in English and German but 20/0 in Spanish (Table 5 of the paper).

![[Bui2026-fig-02-p6.png]]
*Figure 2: share preferring consistency vs adaptation by profession and country; * = significant against 50% (binomial test, p < 0.05).*

**Results specific to diet, religion or traditional medicine: none.** The survey has one generic question and no
item about food, fasting, religion or herbal medicine. These topics appear only in the literature review and in one
conjecture:
- Diet: Dey et al. found HealthBench rubrics "penalizing India-specific dietary guidance because it did not match a
  US-market fish list".
- Traditional medicine: CMB's warning about translated benchmarks and TCM; Africa Health Check's "persistent default
  to allopathic (Western) treatments in zero-shot scenarios" and that "roughly 80% of the African population relies
  on traditional herbal medicine for primary care".
- Conjecture (§4.5): where "traditional or alternative medicine plays a larger role in care", "support for
  adaptation is plausibly stronger still". Not tested.
- Religion is not discussed.

## Persona-prompted LLM comparison
- **Models (11):** Gemma 4 (E4B, 26B-A4B, 31B), Llama 3.1 8B, Llama 3.3 70B, Qwen3.5 (9B, 27B, 35B-MoE), Phi-4 14B,
  Aya Expanse 32B, GPT-OSS 20B.
- **Design:** 3 prompt languages × 3 profession personas × 3 country personas, in the system prompt: "You are a
  person {profession} currently working in {country}. Be short. Answer the following survey question honestly and
  from your professional perspective." Option order shuffled; 20 samples per condition (temperature 0.7, top-p 0.9).

| Pro-consistency (%) (Table 2) | Humans | LLMs |
|---|---|---|
| Anthropology | 19.2 ± 1.4 | 16.2 ± 3.7 |
| NLP | 61.2 ± 1.5 | 80.0 ± 3.9 |
| Medical | 53.7 ± 10.8 | 83.6 ± 4.1 |

![[Bui2026-fig-04-p8.png]]
*Figure 4a: LLM share choosing consistency by country persona (English prompts), averaged over models.*

![[Bui2026-fig-05-p8.png]]
*Figure 4b: LLM share choosing consistency by prompt language, averaged over models.*

## Recommendations
- Decide the target behaviour first; "neither consistency nor adaptation can currently be considered the clearly
  superior approach".
- Do user-centred studies of which behaviour helps the people asking.
- Work at item level: find which items should be consistent and which may adapt.
- To build for **consistency:** "cross-lingual alignment on parallel medical QA with shared answers".
- To build for **adaptation:** "natively sourced per-region QA and retrieval over country-specific clinical
  guidelines".
- Do not rely on prompts: "system-prompt steering alone fails to reproduce even coarse stakeholder variation, so
  prompting is unlikely to be a sufficient adaptation mechanism".
- Do not use persona-prompted LLMs in place of stakeholder surveys.
- Follow-up surveys should separate medical content from communication style, and sample beyond the Global North.

## Relevance to research questions
### Q7: Cultural cues in evaluation datasets
- The paper lists no new dataset with cultural cues. It is useful as a classification of the datasets we already
  track: translated sets ([[Matos2024 - WorldMedQA-V]], MedExpQA, XLingHealth) carry the source country's gold
  answer and are regional only by language; native sets ([[MMedBench]], [[CMB (CMB-Clin)]]) are grounded in a
  country's exam system but do not mark *which* items depend on it.
- It confirms the finding of Q7 from an independent review: the authors found no benchmark whose items are labelled
  as universal or culture-specific.
- Language is "the dominant proxy for culture", and the authors warn that it is a poor one (a Spanish question may
  come from Madrid, rural Oaxaca or Buenos Aires). This supports counting language-only sets as `adjacent` and
  looking for explicit cues (place, health system, practice) in the case text.

See [[Q7 Cultural cues in evaluation datasets|Q7]]

### Q8: Injecting cultural cues into datasets
- The paper does no injection. It gives the design requirement: an injected cue must be labelled as either
  answer-neutral (the "consistency" items; e.g. drug mechanism) or answer-relevant (the "adaptation" items; e.g.
  local guidelines). Gap 3 says no benchmark has this label, which is the niche our cue-injected cases would fill.
- It classifies the existing injection works ([[Shaier2023 - Demographic effects on biomedical QA|Shaier et al. 2023]],
  [[Rawat2024 - DiversityMedQA|DiversityMedQA]],
  [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA|Rezaei & Shakeri 2026]]) as consistency tests where the
  invariance of the gold answer is "assumed rather than proven", or verified by a single clinician.
- Expert agreement on "should the answer change?" cannot be assumed: clinicians split 43–65% for consistency by
  country. Our validity labels for answer-relevant cues need several raters and should report disagreement.
- LLM personas are not a substitute for those raters, and LLMs default to consistency, most strongly in English. A
  model may therefore ignore an answer-relevant cue; this is the failure our evaluation should measure.
- For answer-relevant cues the paper points to "retrieval over country-specific clinical guidelines" as the
  mechanism, which matches supplying our graph as external knowledge.

See [[Q8 Injecting cultural cues into datasets|Q8]]

## Limitations / caveats
- One binary question; the authors note it "cannot tell us which dimensions of the consistency-adaptation distinction
  respondents weighted". The most frequent free-text theme (content consistent, communication adapted) fits neither
  option.
- Option 2 ties culture to the *language of the question*, the proxy the paper itself criticises.
- Small cells (17–20 anthropologists per country, 21 NLP respondents in Spain); the paper says group sizes do not
  "support fine-grained statistical comparison".
- Germany, Spain and the US only; "our sample is drawn entirely from the Global North".
- Many "medical" respondents are not physicians by degree (e.g. Germany: 9 high-school and 8 vocational among 60).
- Number mismatches inside the paper: 348 (PDF) vs 356 (arXiv abstract); §5.2 text gives consistency rates by prompt
  language of 0.80 / 0.84 (English), 0.67 / 0.69 (German), 0.74 / 0.79 (Spanish) for NLP / medical personas, while
  Figure 4b shows 83% / 87%, 72% / 77%, 80% / 83%.
- The PubMed comparison is three data points.

## Related work to follow
![[Backlog.base#Cited by this paper]]
