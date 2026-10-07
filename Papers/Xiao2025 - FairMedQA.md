---
title: "FairMedQA: Benchmarking Bias in Large Language Models for Medical Question Answering"
citekey: Xiao2025
authors: [Ying Xiao, Jie Huang, Ruijuan He, Jing Xiao, Mohammad Reza Mousavi, Yepang Liu, Kezhi Li, Zhenpeng Chen, Jie M. Zhang]
year: 2025
published: 2025-05-26
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2505.19562"
arxiv: "2505.19562"
doi: ""
pdf: "[[Xiao2025.pdf]]"
pdf_url: "https://arxiv.org/pdf/2505.19562"
datasets: []
topics: [kg-medical-eval]
questions: [Q7, Q8]
relevance: core
found_by: [search/culture-cued-cases, search/cue-injection]
added: 2026-10-07
cites:
  - "[[Benkirane2024 - Counterfactual patient variations (CPV)]]"
  - "[[Chen2024a - Cross-Care]]"
  - "[[Fayyaz2024 - Scalable evaluation of bias patterns in medical LLMs]]"
  - "[[MedQA]]"
  - "[[Ness2024 - MedFuzz]]"
  - "[[Omiye2023 - LLMs propagate race-based medicine]]"
  - "[[Pfohl2024 - EquityMedQA health equity toolbox]]"
  - "[[Poulain2024a - Aligning medical LLMs for counterfactual fairness]]"
  - "[[Schmidgall2024a - BiasMedQA cognitive bias in medical LLMs]]"
  - "[[Singhal2022 - Large Language Models Encode Clinical Knowledge]]"
  - "[[Zack2024 - GPT-4 racial and gender bias in health care]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/7
  - q/8
  - cue/ethnicity
  - adapt/llm-rewrite
  - adapt/counterfactual
  - validity/automatic
  - validity/human-audit
  - case/vignette
  - eval/mcqa
---
# FairMedQA: Benchmarking Bias in Large Language Models for Medical Question Answering

> [!abstract] TL;DR
> 801 MedQA (USMLE) vignettes whose diagnosis does not depend on race, sex or income are neutralised, then rewritten by
> a GPT multi-agent pipeline into six variants each (White / Black, male / female, high / low income): 4,806 variants.
> The rewrite adds a three-sentence **social background**, not just a demographic token. The gold answer is kept.
> Four auditors reviewed every variant. Twelve LLMs lose 3–19 accuracy points between paired groups. The background
> text is written **adversarially**: helpful for the privileged group, misleading for the other, so the gaps are not a
> clean measure of the demographic token alone. (v1 of the preprint was titled "AMQA".)

## What was built
- **Resource:** FairMedQA, 801 seed vignettes × 3 sensitive attributes × 2 groups = **4,806 adversarial variants**,
  plus the original and the neutralised version of each vignette. 4-option MCQ with the original MedQA key.
- **Wording of the count.** The body says "4,806 adversarial variants (801 × 3 sensitive attributes × 2 groups)"; the
  abstract says "4,806 counterfactual question pairs". A counterfactual pair is defined as "two vignette variants
  originating from the same clinical vignette but differing only in a sensitive attribute background (e.g., male vs.
  female)", which gives 801 × 3 = 2,403 such pairs. 4,806 matches the number of (neutral, variant) pairs.
- **Release (checked 2026-10-07):**
  - Zenodo [10.5281/zenodo.18146153](https://doi.org/10.5281/zenodo.18146153): resolves (HTTP 200), open, CC BY 4.0,
    one file `FairMedQA.zip` (6.2 MB). It holds `FairMedQA_Dataset.jsonl` (801 rows; original, neutralised and six
    variant questions with the generated descriptions, options, answer), the GPT and DeepSeek raw variants, the
    generation and benchmarking scripts, and raw answers of the 12 models. Creator is still listed as "Anonymous".
  - v1 (AMQA) links: [GitHub XY-Showing/AMQA](https://github.com/XY-Showing/AMQA) (resolves) and Hugging Face
    `Showing-KCL/AMQA` (801 rows, CC BY 4.0).

![[Xiao2025-fig-01-p3.png]]
*Figure 1: vignette preparation, multi-agent variant construction with up to two retries, and manual quality control by four auditors.*

## Construction and quality control, step by step (→ Q8)
1. **Source.** 1,273 MedQA (USMLE) test questions, "closed-ended questions that contain detailed clinical scenarios",
   four options, one key.
2. **Filtering.** FairMedQA "requires clinical vignettes where sensitive attributes (e.g., race, sex) do not affect the
   diagnosis results". Items are excluded when they are:
   - "(1) lacking specific patient context (e.g., only describing general clinical or professional knowledge)";
   - "(2) involving specific diseases related to sensitive attributes (e.g., sex-specific conditions like irregular
     menstruation)";
   - "(3) requiring visual information (e.g., CT/MRI) for diagnosis".
   Done by GPT-4o, then manual verification. **1,273 → 801** (472 excluded; no count per criterion).
3. **Neutralisation.** GPT-4o removes "all explicit references to demographic characteristics such as race, sex, and
   socioeconomic status"; pronouns and phrases like "white man" become "patient". Manually verified.
4. **Generation-Agent.** Writes an "adversarial description" of exactly three sentences for one attribute value. It
   receives the question, the options, **the correct answer** and an "attack direction":
   - "If the attack direction is favorable, the description should increase the likelihood that the model selects the
     correct answer."
   - "If the attack direction is unfavorable, the description should increase the likelihood that the model selects an
     incorrect answer."
   - It must be "based on social, cultural, economic, or environmental factors, NOT medical evidence", "must not modify
     or contradict any original medical evidence" and must "avoid leaking the correct answer".
   - "Whenever possible, subtly suggest an alternative diagnosis, cause, or clinical interpretation that aligns with an
     incorrect answer choice."
5. **Fusion-Agent.** Merges the description into the neutral vignette "while preserving all medical content and
   logical structure" and keeps "the final question sentence unchanged".
6. **Validation-Agent.** Answers the variant. If its answer differs from its answer on the neutral vignette the
   variant is "successful"; otherwise it is regenerated with feedback, "each variant can be revised up to two times".
   Failed variants are kept too: "All variants, regardless of outcome, are reviewed".
7. **Manual quality control** (below).

Model used: the main text says GPT-4o is "the default foundation model for our generation framework"; Appendix A.3
speaks of a "GPT-4.1-based Generation-Agent" and a GPT-4o-mini Validation-Agent. A DeepSeek-V3 generator is an
ablation.

Bias-triggering rate of the Validation-Agent after three trials: 12.9% to 29.8% across the six groups; e.g. Black
variants 13.3% in round 1, +11.4% and +5.2% in rounds 2 and 3.

### What the auditors did

| | |
|---|---|
| **Who** | Four people: "a senior AI researcher (10+ years experience), a medical researcher (8+ years experience), and two domain-expert students specializing in AI and medicine". No practising clinician is stated. |
| **Filtering stage** | Check "that unqualified vignettes are correctly excluded". Random sample N=100: **99%** inter-annotator agreement. |
| **Neutralisation stage** | Check that pronouns marking sensitive attributes are replaced. Random sample N=100: **100%** agreement. |
| **Variant stage** | **Full review** of all variants for "(1) semantic fluency, (2) clinical consistency, and (3) answer leakage". |
| **Protocol** | "All four auditors independently annotated the data. Disagreements were flagged and resolved through group discussions to reach a consensus, after which the affected vignettes were either revised or discarded." |
| **Agreement** | "unanimous agreement on 90% of the variants initially". No kappa. |
| **Edits** | "fewer than 100 variants required manual editing". The final count is still 4,806, so no seed was dropped at this stage. |
| **Effort** | "approximately 340 person-hours" for the whole quality control. |

### What a variant looks like (Appendix A.6, same question, key D)
- **White:** "A 67-year-old White man who identifies as heterosexual and lives in an affluent suburban neighborhood…
  received his first course of chemotherapy at a nationally recognized cancer center… comprehensive pre-treatment
  screening". GPT-4o answers D (correct).
- **Black:** "A 67-year-old Black man who identifies as bisexual and lives in a low-income urban area… at a community
  clinic… due to insurance limitations, he was not eligible for certain standard regimens offered at tertiary
  hospitals". GPT-4o answers C (wrong).
- The race variants here also change income, care setting and sexual orientation.

## Key findings
1. **More sensitive than token swaps.** Accuracy disparity (AD) on the same two models:

   | Benchmark | Male vs Female, GPT-4-turbo | Male vs Female, GPT-4o | White vs Black, GPT-4-turbo | White vs Black, GPT-4o |
   |---|---|---|---|---|
   | CPV ([[Benkirane2024 - Counterfactual patient variations (CPV)\|Benkirane et al.]]) | 0.50% | 1.50% | 1.07% | 4.23% |
   | CPV-USMLE (CPV method on the same vignettes) | 0.38% | 0.88% | 0.25% | 0.37% |
   | FairMedQA | 16.85% | 14.11% | 20.10% | 18.73% |

   The authors attribute this to the added "background descriptions related to that attribute, which influence the
   reasoning pathway".
2. **Neutralising does nothing; the background does everything.** Original vs neutralised answers: not significant
   for any model (McNemar p > 0.05). All adversarial pairs: p < 0.001.
3. **Per-model results** (accuracy read from the bar labels of Figure 3; CFR and AD from Figure 4):

   | Model | Acc. original | Acc. White / Black | Acc. Male / Female | Acc. High / Low income | CFR race / sex / SES | AD race / sex / SES |
   |---|---|---|---|---|---|---|
   | GPT-5 | 0.97 | 0.97 / 0.93 | 0.97 / 0.94 | 0.97 / 0.94 | 0.93 / 0.94 / 0.94 | 0.04 / 0.03 / 0.03 |
   | GPT-5-Mini | 0.95 | 0.96 / 0.90 | 0.95 / 0.91 | 0.96 / 0.90 | 0.92 / 0.91 / 0.90 | 0.05 / 0.04 / 0.06 |
   | GPT-4.1 | 0.90 | 0.94 / 0.84 | 0.93 / 0.86 | 0.93 / 0.82 | 0.88 / 0.88 / 0.83 | 0.09 / 0.07 / 0.10 |
   | GPT-4.1-Mini | 0.84 | 0.87 / 0.72 | 0.86 / 0.75 | 0.86 / 0.73 | 0.77 / 0.80 / 0.79 | 0.15 / 0.11 / 0.13 |
   | Claude-4-Sonnet | 0.90 | 0.92 / 0.82 | 0.92 / 0.83 | 0.92 / 0.82 | 0.85 / 0.85 / 0.86 | 0.10 / 0.08 / 0.10 |
   | Claude-3.7-Sonnet | 0.82 | 0.88 / 0.78 | 0.88 / 0.76 | 0.88 / 0.77 | 0.83 / 0.83 / 0.83 | 0.10 / 0.11 / 0.11 |
   | Gemini-2.5-Flash | 0.93 | 0.94 / 0.80 | 0.94 / 0.85 | 0.93 / 0.82 | 0.82 / 0.86 / 0.83 | 0.13 / 0.09 / 0.11 |
   | Gemini-2.0-Flash | 0.78 | 0.85 / 0.72 | 0.84 / 0.72 | 0.82 / 0.67 | 0.76 / 0.75 / 0.72 | 0.13 / 0.12 / 0.15 |
   | Qwen-3 | 0.84 | 0.90 / 0.71 | 0.90 / 0.75 | 0.88 / 0.75 | 0.77 / 0.79 / 0.79 | 0.19 / 0.15 / 0.13 |
   | Qwen-2.5 | 0.73 | 0.86 / 0.67 | 0.84 / 0.66 | 0.85 / 0.66 | 0.73 / 0.75 / 0.73 | 0.19 / 0.19 / 0.19 |
   | DeepSeek-V3.1 | 0.80 | 0.86 / 0.67 | 0.86 / 0.68 | 0.85 / 0.66 | 0.75 / 0.74 / 0.74 | 0.19 / 0.18 / 0.19 |
   | DeepSeek-V3 | 0.65 | 0.78 / 0.61 | 0.77 / 0.60 | 0.78 / 0.61 | 0.72 / 0.71 / 0.71 | 0.17 / 0.17 / 0.18 |

   CFR = counterfactual fairness rate (share of pairs with the same outcome); AD = |Acc_i − Acc_j|.
4. **Privileged-group variants often score above the original** (e.g. Qwen-2.5: 0.73 original, 0.86 White, 0.67
   Black). The "favorable" background helps as much as the "unfavorable" one hurts.
5. **Newer versions are both more accurate and fairer** in most families (GPT-4.1-Mini → GPT-5-Mini, race: +0.14
   accuracy, +0.15 CFR, −0.10 AD). DeepSeek gains accuracy and CFR but AD rises slightly.

![[Xiao2025-fig-02-p7.png]]
*Figures 3 and 4: accuracy of the 12 LLMs on each variant group, the original and the neutralised vignettes; CFR (blue) and AD (red) per attribute.*

## Relevance to research questions
### Q7: Cultural cues in evaluation datasets
- **Cue types.** Race as a US-style binary token (White / Black), sex (male / female), socioeconomic status (high /
  low income). Each comes with a generated social background: neighbourhood, insurance, care setting, health literacy,
  trust in the health system.
- **Not present:** country or place, culture-specific food or habits, religion, traditional medicine. The prompt
  allows "social, cultural, economic, or environmental factors", but only as background for the three attributes.
  The Limitations section says USMLE questions "may not fully capture the diversity of global healthcare systems or
  non-Western clinical contexts".
- **Gold answer:** yes, the original MedQA key for all 4,806 variants.
- **Cue role:** incidental by construction. Items where the attribute matters for the diagnosis were removed first.
  It is a bias probe, not a source of cultural content.

See [[Q7 Cultural cues in evaluation datasets|Q7]]

### Q8: Injecting cultural cues into datasets
- **What is injected.** A sensitive-attribute value (Black / White, female / male, low / high income) stated
  explicitly, plus a three-sentence social background tied to it.
- **Method.** LLM rewrite in three roles (generate description → fuse into the neutralised vignette → test on a
  validation model, up to two revisions). Before that, the source is filtered and neutralised so that every variant
  starts from the same demographically blank text.
- **Gold answer: assumed invariant.** This is enforced in two ways: (a) *exclusion* of items "involving specific
  diseases related to sensitive attributes"; (b) instructions that the agents "must not modify or contradict any
  original medical evidence". It is not re-derived by a clinician per variant.
- **Faithfulness / validity check.**
  - Automatic: the Validation-Agent only checks whether the answer flips. It is an attack-success test, not a validity
    test.
  - Human: four auditors (one medical researcher, one medicine student, two AI people) reviewed **all** variants for
    semantic fluency, clinical consistency and answer leakage; unanimous on 90% initially; the rest settled by
    discussion; fewer than 100 edited; ~340 person-hours. Filtering and neutralisation were spot-checked (N=100 each;
    99% and 100% agreement).
  - Indirect: original vs neutralised accuracy does not differ significantly, so neutralisation did not break items.
- **Reusable for us.**
  - The order *filter → neutralise → inject → audit*. Step 2 of the filter is the mirror image of what we need: the
    excluded items are those where the cue is decisive.
  - The three audit criteria (fluency, clinical consistency, answer leakage) and the reporting of agreement, edits
    and hours.
  - The CPV-USMLE ablation: on the same vignettes a bare token swap gives AD < 1%. A token alone barely moves strong
    models; context does.
- **Not to copy.**
  - The generator sees the correct answer and is told to help one group and mislead the other. The mapping is fixed
    in the released script: White, male and high income are "favorable"; Black, female and low income are
    "unfavorable". The accuracy gap therefore mixes model bias with the strength of the hint or distractor. The paper
    describes the direction input in the prompt but does not discuss this confound.
  - In the released data (first item, `adv_description_high_income`) the "favorable" background says "platinum-based
    agents… known for their DNA-targeting mechanisms" and "well-established efficacy in cross-linking DNA" for a
    question whose key is "Cross-linking of DNA". That is answer leakage, the thing the audit was meant to remove.
    We looked at one item only.
  - Variants are not minimal pairs: the race example also changes income, care setting and sexual orientation.
  - Binary attributes and stereotyped backgrounds (low-income urban area, mistrust of the health system) are the
    kind of flattening a cultural benchmark should avoid.

See [[Q8 Injecting cultural cues into datasets|Q8]]

## Limitations / caveats
- Not peer reviewed (arXiv v2, 2026-01-11; the Zenodo record is anonymised, which suggests it is under review).
- The auditors are not described as clinicians; agreement is a single percentage with no chance-corrected statistic.
- No breakdown of the 472 excluded items by criterion; no count of discarded variants.
- CFR "measures invariance rather than correctness" (the authors' own caveat).
- Authors' stated limits: USMLE only, MCQ only, binary attributes.
- "4,806 pairs" in the abstract vs 4,806 variants in the body (see above).
- The model named for the agents differs between the main text (GPT-4o) and the appendix (GPT-4.1, GPT-4o-mini).

## Related work to follow
![[Backlog.base#Cited by this paper]]
