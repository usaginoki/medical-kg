---
title: "Session 2026-10-07: kg-medical-eval - cultural cues in evaluation datasets"
date: 2026-10-07
session: literature-review
topics: [kg-medical-eval]
questions: [Q7, Q8]
tags:
  - type/session
  - q/7
  - q/8
---
# Session 2026-10-07: kg-medical-eval (cultural cues in evaluation datasets)

> [!question] Questions addressed in this session
> - [[Q7 Cultural cues in evaluation datasets|Q7]]: Which evaluation-relevant medical datasets contain cultural cues:
>   the patient's country or place, race or ethnicity, culture-specific foods, habits or religious practices, or
>   traditional medicine?
> - [[Q8 Injecting cultural cues into datasets|Q8]]: Have any works accurately and faithfully injected cultural cues
>   into medical datasets, and if not, which methods and source datasets could we use to do it?

**Research question:** the case table from the [[2026-10-07 KG medical evaluation - survey|earlier session]]
(37,631 cases → gold conclusion) is meant to test a *culturally aware* medical agent. Do those cases, or any others,
actually contain culture? If not, can cues be added without breaking the cases?

**Corpus / scope:**
- **Scope agreed with the user:** Q7–Q8 stay in the topic `kg-medical-eval`; standard depth; all four cue types count
  (place, race / ethnicity, food-habits-religion, traditional medicine).
- **Search:** 3 parallel strands on 2026-10-07: culture-cued medical datasets; cue injection in medicine;
  general-domain adaptation methods and cue sources.
- **Candidates:** 87 new candidate notes from the strands (67 papers and datasets, 20 source resources) and 28 from
  the processed papers' reference lists, all in [[Backlog]]; 13 existing candidates were re-tagged for Q7 / Q8.
  Semantic Scholar snowballing failed in one strand (HTTP 429).
- **Processed (6 full paper notes):**
  [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA|Rezaei & Shakeri 2026]],
  [[Varadarajan2026 - CCBench|CCBench]], [[Pfohl2024 - EquityMedQA health equity toolbox|EquityMedQA]],
  [[Xiao2025 - FairMedQA|FairMedQA]],
  [[Azime2025 - Socio-cultural localisation of math word problems|Azime et al. 2025]],
  [[Bui2026 - Cross-lingual consistency for medical questions|Bui et al. 2026]].
- **Local analysis:** `db/cues.py` counts cue keywords (EN / RU / ZH / AR) in the case table; a rough Persian count
  was run on [[PerMedCQA]] (downloaded to a scratch folder, not added as a dataset note).
- **No new datasets were added to `Datasets/`.**

> [!important] Main takeaways
> 1. **Our case table is culturally thin.** 20.7% of cases match some cue, but that is nationality or race words in
>    [[MedCaseReasoning]] (10.3% place, 8.9% ethnicity), cuisine names on the *dish* in [[NGQA]] and [[FAM-Bench]],
>    and traditional medicine by construction in the two TCM sets. [[RuMedBench]], [[MedArabiQ]] and
>    [[MedicationQA]] state a cue in under 3% of cases: they are regional by language only.
> 2. **Purpose-built culture-cued medical sets are small, synthetic or unreleased.** Only Rezaei & Shakeri's 1,350
>    released MedQA variants have a clinical gold answer, and their cues are designed not to matter.
> 3. **No dataset has a culturally decisive cue with a clinician gold at scale.** The decisive cases in hand are a
>    thin tail: camel milk, khat, injera and Kampo cases in MedCaseReasoning, diet precautions in [[TCM-BEST4SDT]],
>    a few hundred Ramadan and herbal questions in PerMedCQA.
> 4. **Nobody has faithfully injected food, habit or traditional-medicine cues into medical cases.** About 20 works
>    inject race, gender or religion tokens as bias audits with the answer held fixed. Answer-changing designs exist
>    only for location, national guidelines, Ramadan dosing and one African herbal set.
> 5. **Even the careful injection papers have validity holes.** Reading the released items: Rezaei's variants
>    sometimes delete the decisive cue or leak the answer; FairMedQA's generator is told which way to push the
>    model. One reviewer, or reviewers who are not clinicians, is the norm.
> 6. **The method exists outside medicine, minus the part we need.** Slot → curated dictionary → scripted swap →
>    automatic checks → human review works for names and currencies; Azime et al. left food out on purpose. Free LLM
>    rewriting and bare persona tokens are documented failures.
> 7. **The graph is the missing piece.** It can tell whether a dish swap is clinically neutral (no interaction or
>    condition edge hit) or decisive (an edge is hit, so the answer must be re-derived). No existing work has this.
> 8. **Central Asia has nothing** on either question; the Gulf has only tiny or synthetic sets.

## Q7: cultural cues in evaluation datasets → [[Q7 Cultural cues in evaluation datasets]]
- Cue counts for the 8 downloaded case sets, with what the matches actually are.
- Six purpose-built sets (Rezaei, CCBench, RamadanSafeQA, Tibbe-AG, Africa Health Check, Samiksha) and TRINDs.
- Structured fields are rare: `country` in [[NutriBench]], travel region in [[DDXPlus]], Age / Sex / Weight in
  PerMedCQA. No religion or diet-pattern field anywhere.
- PerMedCQA (67,791 real Iranian questions): about 4% carry a free-text cue.
- CCBench's 95 norms are printed in the paper and tabulated in our note, although its data is not released.

## Q8: injecting cultural cues → [[Q8 Injecting cultural cues into datasets]]
- Three properties of a faithful injection: content preservation, cultural accuracy, clinical consistency.
- Tables of bias-audit injections and of answer-changing designs, with how each was validated.
- Transferable pipeline, rubric and controls; sources for accurate cues per cue type, with coverage gaps
  (no WHO STEPS survey for Saudi Arabia, UAE, Bahrain, Oman, Kazakhstan, India, China, Japan or Korea).
- A seven-step recipe for our case table that separates inert from decisive cues using the graph.

## Most important papers to read first
| Why | Paper |
|---|---|
| The only cultural-cue injection into medical QA; also shows what goes wrong | [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA\|Rezaei & Shakeri 2026]] |
| Diet, religion and traditional-medicine norms that should change health advice, per culture | [[Varadarajan2026 - CCBench\|CCBench]] |
| The rubric question "do the ideal answers differ?", and how much raters disagree on it | [[Pfohl2024 - EquityMedQA health equity toolbox\|EquityMedQA]] |
| The most documented rewrite-and-audit pipeline, and its confound | [[Xiao2025 - FairMedQA\|FairMedQA]] |
| A localisation pipeline to copy, and its limits | [[Azime2025 - Socio-cultural localisation of math word problems\|Azime et al. 2025]] |
| Framing: when should an answer stay the same across cultures | [[Bui2026 - Cross-lingual consistency for medical questions\|Bui et al. 2026]] |

## Open gaps / next steps
1. **Size the decisive set:** match the drugs and conditions in the case table against food–drug and food–condition
   edges of the [[Unified database]]; this bounds how many answer-changing injections are possible.
2. **Mine the real seed set:** the cue-bearing rows are marked by the `cue_*` and `relevance` columns of
   `db/export/cases.parquet`; pull the decisive ones from MedCaseReasoning and add PerMedCQA as a dataset.
3. **Tag with a model, not keywords:** the counts are a lower bound and do not separate decisive from incidental.
4. **Build slot tables** for Saudi Arabia / Gulf and Kazakhstan / Kyrgyzstan from our dish tables, with habits and
   plausibility from WHO GHO, GBD and the tobacco surveys; get a native reviewer for each table.
5. **Find clinicians per region** for validation; every credible work relies on them.
6. **Download as format references:** Rezaei's augmented items and EquityMedQA (both open).
7. **Ask the authors** for CCBench, Samiksha, RamadanSafeQA and Africa Health Check data ([[Access requests]]).
8. **Unverified:** the MENST dataset's sociocultural-context field; NigBench's content; the PerMedCQA keyword count
   (needs a Persian reader).

## Papers in this topic
![[Papers.base#This topic]]

## Backlog for this topic
![[Backlog.base#This topic]]
