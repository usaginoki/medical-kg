---
title: "Counterfactual Cultural Cues Reduce Medical QA Accuracy in LLMs: Identifier vs Context Effects"
citekey: Rezaei2026
authors: [Amirhossein Haji Mohammad Rezaei, Zahra Shakeri]
year: 2026
published: 2026-01-27
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2601.20102"
arxiv: "2601.20102"
doi: ""
pdf: "[[Rezaei2026.pdf]]"
pdf_url: "https://arxiv.org/pdf/2601.20102"
datasets: []
topics: [kg-medical-eval]
questions: [Q7, Q8]
relevance: core
kind: [case]
manipulation: "cultural identifier, context cue or both added to 150 MedQA items for 3 groups (Indigenous Canadian, Middle-Eastern Muslim, Southeast Asian) + neutral control; LLM rewrite"
outcome: "accuracy and answer flips of 5 LLMs; culture-referential rationales"
found_by: [search/culture-cued-cases, search/cue-injection]
added: 2026-10-07
cites:
  - "[[MedQA]]"
  - "[[Nimo2025 - Africa Health Check]]"
  - "[[Omar2025 - Sociodemographic biases in LLM medical decisions]]"
  - "[[Pfohl2024 - EquityMedQA health equity toolbox]]"
cited_by:
  - "[[Bui2026 - Cross-lingual consistency for medical questions]]"
cited_by_count: 1
tags:
  - type/paper
  - relevance/core
  - q/7
  - q/8
  - kind/case
  - case/vignette
  - cue/ethnicity
  - cue/religion
  - cue/country
  - cue/food-habit
  - adapt/llm-rewrite
  - adapt/counterfactual
  - validity/clinician
  - eval/mcqa
  - eval/llm-judge
  - region/middle-east
  - region/southeast-asia
  - region/americas
---
# Counterfactual Cultural Cues Reduce Medical QA Accuracy in LLMs: Identifier vs Context Effects

> [!abstract] TL;DR
> 150 MedQA (USMLE) test items are rewritten by an LLM into 9 cultural variants each: an **identifier** ("Muslim man
> living in a large Middle Eastern city"), a **context** cue ("after evening prayers at the mosque") or **both**, for
> three groups (Indigenous Canadian, Middle-Eastern Muslim, Southeast Asian), plus a neutral control sentence. The
> cues are meant to be clinically irrelevant, so the gold answer is kept. Five LLMs lose 3–7 points of accuracy when
> identifier and context appear together. The 1,350 cultural variants are on GitHub (no licence); our inspection finds
> that a few rewrites do change clinical content.

## What was built
- **Resource:** a counterfactual benchmark, 150 MedQA test items × (3 groups × 3 cue types) = **1,350 cultural
  variants**, + 150 originals + 150 neutral controls = **1,650 items** (paper's count). 5-option MCQ, English.
- **Groups:** Indigenous Canadian (C1), Middle-Eastern Muslim (C2), Southeast Asian (C3). Chosen as "minority
  cultural backgrounds that often face biased and inequitable treatment in society and in AI systems".
- **Cue types (paper's definitions):**
  - *cultural identifiers* (Id): "explicit references to a cultural group (e.g., 'a 35-year old Muslim man living in
    a large Middle Eastern city')"; only "the first sentence and the patient identifier" are changed.
  - *cultural contextual cues* (Ctx): "culturally related situational details embedded in the narrative (e.g.,
    'symptoms began during evening prayer at a mosque')".
  - Id+Ctx: both.
- **Neutral control:** the fixed sentence "The patient arrived with a family member and provided ID at registration"
  is put at the start of each question, to separate the effect of culture from the effect of length.
- **Construction:** an LLM (not named in the paper) rewrites each item under few-shot prompting, with the instruction
  "not to introduce new clinical information". 150 items were sampled at random from the MedQA test set.
- **Diversity check:** added sentences embedded with all-MiniLM-L6-v2; mean pairwise cosine similarity within a group
  is 0.3142.
- **Evaluation:** GPT-5.2, Llama-3.1-8B, DeepSeek-R1, MedGemma-4B and -27B; two prompts (option only; 2–3 sentence
  explanation + option). Metrics: accuracy, flip rate, harmful flip rate (correct → wrong), Cochran's Q, bootstrap
  95% CIs (n = 2000). GPT-5.2 as LLM-judge flags explanations that refer to identity or region.

![[Rezaei2026-fig-02-p3.png]]
*Figure 2: one MedQA item and its nine cultural variants. Note that the original "at a local bar" is replaced by the context cue.*

## What is in the released data (inspected 2026-10-07)
Repository: [HIVE-UofT/Evaluating-Cultural-Cues-Medical-LLMs](https://github.com/HIVE-UofT/Evaluating-Cultural-Cues-Medical-LLMs)
(the URL printed in the paper, `Evaluatiog-Cultural-Clues-…`, is an older name that still redirects). Last push
2026-02-01. **No licence file** (GitHub reports `license: null`), so reuse terms are undefined.

| file in `Data/` | content |
|---|---|
| `final_augment_test_questions.json` (1.3 MB) | list of **150** records: `original_question`, `options` (A–E), `answer`, `answer_idx`, and `t1_question` / `t2_question` / `t3_question`, each a dict with keys `i`, `c`, `ic` (full rewritten question text) |
| `test.jsonl` (1.3 MB) | not opened; by name and size the MedQA test file |
| `Final_<model>_option_augment_answers.json`, `…_short_augment_answers.json` | model answers for the 5 models, both prompts |
| `Final_<model>_judge.json` | LLM-judge labels (the GPT file is named `Final_GPT5.1_judge.json`) |

- `t1` = Indigenous Canadian, `t2` = Middle-Eastern Muslim, `t3` = Southeast Asian (from the content).
- 150 × 9 = 1,350 cultural variants are present. The **neutral variant is not stored** (it is a fixed sentence, so it
  can be rebuilt). The augmentation prompt is not in the repository listing (`Code/` holds inference and judge
  scripts only), although the paper says "We release prompts and augmentations".
- The cue is not marked up: each variant is a full rewritten question. We recovered the inserted text with a
  word-level diff against the original.
- Size of the edit (our diff): about 9 added words per identifier variant, ~28 per context variant, ~37 per combined
  variant. The combined variant is the identifier variant plus the context variant.
- One variant is identical to the original (item 90, Southeast Asian, identifier).

**Real examples (inserted text in bold, item index in brackets).**

| group | cue | example |
|---|---|---|
| Middle-Eastern Muslim | identifier | "A 61-year-old **Muslim** man has decreased urinary output…" [0] · "**from a Middle Eastern Muslim family**" [24, 35] · "**Muslim** woman **living in an urban area in the Gulf region**" [20] |
| Middle-Eastern Muslim | context | "…fall and hit her head **while going down the stairs to join the family for evening tea after Maghrib prayer**" [124] · "**He says his symptoms have made it difficult for him to attend evening prayers at the mosque.**" [9] · "…worsens with large meals and spicy foods**, especially after late evening family dinners following congregational prayers,**" [134] |
| Middle-Eastern Muslim | both | "A 39-year-old **Muslim** man **living in a large Middle Eastern city** presents … chest pain and nausea that started **30 minutes earlier while he was sitting with friends at a late-night café**" [3] · "**Muslim** woman **living in a large Middle Eastern city** … **days, including during recent family gatherings after evening prayers**" [66] |
| Southeast Asian | identifier | "**from a rural village in Southeast Asia**" [27, 125] · "girl **from a rural village in northern Thailand**" [73] · "a 61-year-old man **who lives with his extended family in a multigenerational household**" [0] |
| Southeast Asian | context | "…has refused medical help**, preferring to rest at home with herbal remedies suggested by relatives**" [83] · "dental caries**, including one shortly after attending a relative's wedding banquet**" [57] · "**which she noticed while helping her get ready for a neighborhood temple and market visit**" [81] |
| Southeast Asian | both | "**living with his family in a busy urban neighborhood in Southeast Asia** … **The rash started a day after the family attended a crowded temple festival.**" [147] · "**from a rural village in Southeast Asia** … **She was brought in by her family after the contractions began while she was helping prepare food for a community gathering.**" [8] |

**What the cues are made of** (our substring counts over the inserted text, 150 items per cell):

| group | identifier variants | context variants |
|---|---|---|
| Middle-Eastern Muslim | "Muslim" 146, "Middle East…" 125 | "prayer" 73, "family" 69, "mosque" 57, "meal" 11, "Ramadan" 7, "Friday" 7, "alcohol" 7, "Eid" 4 |
| Southeast Asian | "Southeast Asia…" 146 (one "Thailand", one "Filipino") | "family" 79, "festival" 32, "market" 26, "food" 13, "temple" 11, "rice" 6, "herbal" 3 |
| Indigenous Canadian | "First Nations" 120, "Cree" 90 | "family" 38, "reserve" 20, "tradition…" 11 |

- Context cues are mostly **place and occasion** (mosque, prayer time, family gathering, market, festival, type of
  hospital). Food, fasting and traditional medicine are rare: Ramadan in 7 of 150, herbal remedies in 3 of 150.
- Southeast Asia is treated as one group; almost no country is named.

**Edits that are not clinically neutral** (found by reading the diffs; not reported in the paper):
- Item 80 (gold: acral lentiginous melanoma): the original patient is "African-American", the fact the answer rests
  on. All identifier variants **replace** it ("Middle Eastern Muslim woman", "Southeast Asian woman", "Indigenous
  woman from a Cree community"), and "travels to the Carribean" becomes "a sunny coastal region … often during Eid
  breaks". The gold answer is unchanged in the file.
- Item 141 (gold: aromatic amines): all three context variants **add the exposure history that is the answer**, e.g.
  "for decades he worked in a textile factory … where he regularly mixed and applied synthetic dyes".
- Items 20 and 134: the original race word ("African American", "Caucasian") is replaced by the new identifier.
- Item 3: "at a local bar" is replaced ("late-night café" for the Muslim variant), as in Figure 2.
- Item 90 (gold: delirium): context adds "she becomes more restless after sunset" and "weekly despite generally
  avoiding social gatherings with alcohol" (Muslim) or "a shared room with frequent nighttime noise" (SE Asian).
- Many context variants also reword other parts of the vignette (typos fixed, "states" → "says"), so a context
  variant is a light paraphrase plus a cue, not a pure insertion.

## Key findings
1. **Identifier + context together cost accuracy in every model.** Mean change vs the original, option-only prompt:
   Llama −6.67, GPT-5.2 −6.23, DeepSeek-R1 −5.78, MedGemma-4B −3.67, MedGemma-27B −3.11 points. With a short
   explanation the drop is smaller: DeepSeek-R1 −5.22, MedGemma-4B −4.53, GPT-5.2 −2.72, Llama −1.15,
   MedGemma-27B −0.57.
2. **One cue alone has a small, mixed effect.** Option-only: identifier −4.67 to +1.11, context −3.34 to +0.44.
   With explanation several models go *up* slightly (GPT-5.2 +0.68 Id, +0.45 Ctx).
3. **The neutral sentence is not always neutral.** Option-only accuracy, original → neutral: Llama 64.67 → 60.67,
   GPT-5.2 92.67 → 90.67, MedGemma-4B 54.00 → 52.67, MedGemma-27B 72.00 → 72.67, DeepSeek-R1 92.67 → 94.00. With
   explanations, original and neutral are identical for four models.
4. **Flips (explanation prompt):** Id+Ctx gives the highest flip rate in every model and group: Llama 30.61–32.65%,
   MedGemma-4B 16.33–19.05%, MedGemma-27B 12.93–14.97%, DeepSeek 8.84–12.24%, GPT 6.80–9.52%. Harmful flips
   (correct → wrong) under Id+Ctx: Llama 16.49–18.56%, GPT 3.73–6.72%.
5. **Culture-referential explanations are often wrong.** Of the explanations the judge flags as culturally grounded,
   44–77% end in a wrong answer (Table III; above half in 14 of 15 cells). DeepSeek-R1 produces by far the most (331 under Id, 335 under Id+Ctx).
6. **Failure modes (manual review):** "unsupported generalization about higher prevalence in a group" and symptoms
   attributed "to presumed diet or lifestyle without support in the question stem".
7. **Statistics:** Cochran's Q significant for all models (p < 10⁻¹⁴ per the caption). With bootstrap CIs
   (Figure 5, Id+Ctx vs original; the values match the explanation prompt) only three of fifteen model × group effects exclude 0: DeepSeek-R1
   Middle-Eastern −5.4 [−9.5, −1.4] and SE Asian −5.4 [−10.2, −0.7], MedGemma-4B SE Asian −6.1 [−10.9, −0.7].

![[Rezaei2026-fig-04-p5.png]]
*Figure 4: mean change in accuracy vs the original for identifier only, context only and both (the values match Table II, the explanation prompt).*

![[Rezaei2026-fig-05-p6.png]]
*Figure 5: accuracy change of Id+Ctx vs the original per model and group, with bootstrapped 95% CIs; bold = interval excludes 0.*

## Key tables
**Table I (option-only prompt), accuracy in %.** Δ columns are the mean over the three groups, vs original / vs neutral.

| Model | Orig. | Neutral | Indig. Id | Ctx | Id+Ctx | Mid-East. Id | Ctx | Id+Ctx | SE Asian Id | Ctx | Id+Ctx | Δ Id | Δ Ctx | Δ Id+Ctx |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Llama-3.1-8B | 64.67 | 60.67 | 60.00 | 60.00 | 58.67 | 62.00 | 60.67 | 58.00 | 58.00 | 63.33 | 57.33 | −4.67 / −0.67 | −3.34 / +0.66 | −6.67 / −2.67 |
| GPT-5.2 | 92.67 | 90.67 | 90.00 | 89.33 | 87.33 | 90.00 | 90.67 | 85.33 | 91.33 | 92.00 | 86.67 | −2.23 / −0.23 | −1.67 / +0.33 | −6.23 / −4.23 |
| MedGemma-4B | 54.00 | 52.67 | 51.33 | 52.67 | 49.33 | 52.00 | 54.00 | 50.67 | 52.67 | 53.33 | 50.00 | −2.00 / −0.67 | −0.56 / +0.78 | −3.67 / −2.34 |
| MedGemma-27B | 72.00 | 72.67 | 68.00 | 70.67 | 66.67 | 70.00 | 70.00 | 69.33 | 70.67 | 72.00 | 70.67 | −2.44 / −3.11 | −1.11 / −1.78 | −3.11 / −3.78 |
| DeepSeek-R1 | 92.67 | 94.00 | 92.00 | 92.67 | 87.33 | 94.67 | 94.00 | 86.67 | 94.67 | 94.00 | 86.67 | +1.11 / −0.22 | +0.44 / −0.67 | −5.78 / −7.11 |

**Table III, culture-referential explanations that end in a wrong answer** (wrong / flagged, pooled over the three groups).

| Model | Identity | Context | Identity + Context |
|---|---|---|---|
| Llama | 42/63 (66.67%) | 27/40 (67.50%) | 63/82 (76.83%) |
| GPT-5.2 | 18/35 (51.43%) | 21/39 (53.85%) | 24/43 (55.81%) |
| MedGemma-4B | 42/62 (67.74%) | 15/34 (44.12%) | 55/85 (64.71%) |
| MedGemma-27B | 47/75 (62.67%) | 25/46 (54.35%) | 52/85 (61.18%) |
| DeepSeek-R1 | 193/331 (58.31%) | 75/143 (52.45%) | 210/335 (62.69%) |

## Relevance to research questions
### Q7: Cultural cues in evaluation datasets
- **What cues the items contain:** religion ("Muslim", mosque, prayer times, a few Ramadan and Eid mentions), region
  ("a large Middle Eastern city", "a rural village in Southeast Asia"), Indigenous identity (First Nations, Cree,
  reserve), and everyday settings (family gatherings, markets, festivals, temples).
- **Gold answer:** yes, the MedQA key. The cue is **irrelevant to the answer by design**, so the set measures
  robustness to a cue, not the ability to use one.
- **For our purpose (a cue that should change the conclusion) it has almost nothing.** Culture-specific food,
  fasting and traditional medicine appear in a handful of items and never drive the answer.
- **Size and access:** 1,350 cultural variants of 150 items in one JSON file on GitHub, no licence. English only.
  Regions: Middle East and Southeast Asia as blocks, plus Canada; no country level.
- **Useful as a format reference:** one record per source item with nested variants per group and cue type is easy
  to join to results.

See [[Q7 Cultural cues in evaluation datasets|Q7]]

### Q8: Injecting cultural cues into datasets
- **What is injected:** (a) an identity phrase in the first sentence, (b) one or more situational clauses in the
  narrative, (c) both; plus a fixed neutral sentence as control.
- **Method:** LLM rewrite with few-shot examples and the rule "not to introduce new clinical information". The
  rewriting model and the prompt are not given. No template, no knowledge source: the LLM invents the cues.
- **Gold answer:** **assumed invariant**, not re-derived. The design depends on the cue being "non-medically-decisive".
- **Faithfulness / validity check:** "A clinician reviewed each augmented item and confirmed that the added text did
  not change the clinically correct answer." One clinician; no credentials, no count of rejected or edited items, no
  second rater, no agreement figure. Cultural plausibility was not rated by members of the groups. The only
  agreement number in the paper (Cohen's κ = 0.76, two annotators, 50 explanations) validates the **LLM-judge
  rubric** for culture-referential explanations, not the injected items.
- **What our inspection adds:** the invariance claim does not hold for every item. Rewrites sometimes replace an
  existing demographic fact that the answer depends on (item 80), add the answer's key fact (item 141), or remove a
  clue (item 3, "local bar"). So a single unblinded clinician pass is not enough; a check should compare the variant
  with the original field by field, and source items that already carry race or a lifestyle clue should be excluded
  or handled separately.
- **Lessons for our own injection:**
  - Separate identifier and context: the paper's main effect appears only when both are present.
  - Keep a length-matched neutral control, but test it: here it moves accuracy by up to 4 points on its own.
  - Store the inserted span, not only the rewritten text, so the edit can be audited.
  - LLM-invented context collapses to a few scenes (prayer or mosque in about half of the Middle-Eastern items;
    the authors note repeated "family gathering" settings). A curated source of cues would give more variety and
    cues that matter clinically.

See [[Q8 Injecting cultural cues into datasets|Q8]]

## Limitations / caveats
- 150 items: one item is 0.67 points, and most per-group confidence intervals include 0.
- Explanation-prompt results use 147 items per setting (outputs without a parsable option were dropped).
- The text says identifiers "contribute more" to errors; this rests on Table III (error rate among flagged
  explanations). In the accuracy tables, identifier-only and context-only effects are both small.
- The text names the Indigenous condition as DeepSeek-R1's significant decline, but in Figure 5 that interval is
  −4.8 [−9.5, +0.7]; the bold (significant) rows are Middle-Eastern and SE Asian.
- The Cochran's Q columns are not readable in the extraction; only the caption's p < 10⁻¹⁴ is used here.
- The paper cites a South Asian bias study as support for the "Southeast Asian" group.
- Authors' own limits: inference cost limited the number of source items; LLM augmentation repeats contexts; few
  model families.
- Not peer reviewed (arXiv v1 only, primary category cs.CL, IEEE-style layout, no venue or comment on the abs page).

## Related work to follow
![[Backlog.base#Cited by this paper]]
