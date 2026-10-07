---
title: "Bridging the Culture Gap: A Framework for LLM-Driven Socio-Cultural Localization of Math Word Problems in Low-Resource Languages"
citekey: "Azime2025"
authors: [Israel Abebe Azime, Tadesse Destaw Belay, Dietrich Klakow, Philipp Slusallek, Anshuman Chhabra]
year: 2025
published: 2025-08-13
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2508.14913"
arxiv: "2508.14913"
doi: ""
pdf: "[[Azime2025.pdf]]"
pdf_url: "https://arxiv.org/pdf/2508.14913"
datasets: []
topics: [kg-medical-eval]
questions: [Q8]
relevance: adjacent
found_by: [search/adaptation-methods]
added: 2026-10-07
cites:
  - "[[Adelani2024 - IrokoBench]]"
  - "[[Karim2025 - Cultural adaptation of GSM8K for six countries]]"
  - "[[Tomar2025 - Cultural perturbations of GSM8K]]"
  - "[[Yu2025 - INJONGO]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/adjacent
  - q/8
  - cue/country
  - adapt/localisation
  - adapt/template-swap
  - adapt/llm-rewrite
  - validity/automatic
  - eval/human
  - region/africa
---
# Bridging the Culture Gap: A Framework for LLM-Driven Socio-Cultural Localization of Math Word Problems in Low-Resource Languages

> [!abstract] TL;DR
> A controlled pipeline that replaces **person names, organisation names and currencies** in translated math word
> problems with native ones. An LLM only tags the entities and then copies a scripted English edit into the
> native-language sentence; a volunteer-curated dictionary supplies the replacements, and string-level checks reject
> bad outputs (fallback: keep the unlocalised item). On AfriMGSM (17 non-English languages + English) the pipeline
> localises almost every item where free LLM prompting localises under a third. The effect on model accuracy is small
> and mixed. Code, entity dictionary and data are public.

## What was built
- **Resource:** Localized-AfriMGSM test set (4,500 items = 250 problems × 18 languages) and a localised GSM8K training
  set (25,100 items). The paper says "18 African languages"; these are the 18 AfriMGSM languages, i.e. 16 African
  languages plus French and English. The figures show 17 (amh, ewe, fra, hau, ibo, kin, lin, lug, orm, sna, sot, swa,
  twi, wol, xho, yor, zul).
- **Entity types (3):** personal names, organisation names, currencies. "≈86% of the test set, includes at least one
  important entity."
- **Deliberately excluded:** food and animal names. "Replacing animal and food names tend to generate sentences that
  lack contextual meaning even though our pipeline can handle it easily."
- **Released (checked 2026-10-07):** <https://github.com/IsraelAbebe/Auto-Localizer> resolves (HTTP 200, Apache-2.0,
  last push 2026-04-07). It holds `auto_localizer/localize.py`, `auto_localizer/entities.json` (the entity
  database) and a `localize` CLI. The README links a
  [Hugging Face collection](https://huggingface.co/collections/israel/cultural-localilzation-687e392f6be2aaa0b7c7831c)
  for data and models (resolves).

![[Azime2025-fig-01-p1.png]]
*Figure 1: the same problem in English, in direct Swahili translation, and auto-localised (Camari, Julani, shilingi). The model answers the localised version wrongly.*

## The pipeline, step by step
Inputs per item: the English problem `x_en` and its translation `x_trans`. The stages are the paper's Table 1.

| # | Stage | Done by | Detail |
|---|---|---|---|
| 1–2 | English + translation | given | AfriMGSM: human translations. GSM8K train: NLLB-200-3.3B, kept only if SSA-COMET > 0.65, then top 1,500 per language |
| 3 | Entity classification | LLM (structured output) | Each word of `x_en` is classified as personal name / organisation name / currency. Output e.g. `{'personal_names': ['Mandy','Benedict'], 'currencies': ['$'], 'organization_names': []}`. spaCy NER and POS tagging were tried and judged less robust to spelling and casing |
| 4 | Replacement dictionary | script | `fn(entities, database)`: each extracted entity is mapped to one database entry of the same type, e.g. `{'Mandy': 'Camari', 'Benedict': 'Julani', '$': 'shilingi', 'dollar': 'shilingi'}` |
| 5 | Entity-replaced English `x_ent` | script | String substitution in the **English** text. `x_ent` is shared by all languages |
| 6 | Auto-localisation | LLM, one-shot | Shown `(x_en, x_trans)` as the example pair and asked to apply the same edit to produce the native version of `x_ent` |
| 7 | Quality check | script + humans | See below. On failure return `x_trans` unchanged |

**Native entity database**
- Collected by "a team of volunteers" who curated "unisex personal names, organization names, and representative
  currency values for each language". Unisex names avoid wrong pronouns after a swap.
- The paper gives no size, source or review procedure. The released `entities.json` is small: per language 6–14
  names, 5–19 organisations and exactly 1 currency (188 names and 219 organisations over 18 languages; our count).
- The released file has at least one visible error: the Kinyarwanda entry lists Hausa / Nigerian organisations
  ("Kano State Government", "Hausa Language Board") and the currency "naira" (our reading of the file, not stated in
  the paper).

**LLM prompt constraints (step 6, Appendix D)**
- "DO NOT re-translate the entire sentence. Only replace the specific words that were changed in the English version."
- "Preserve the original grammar and structure of the native sentence as much as possible."
- "Ensure the final Modified Native sentence is natural and grammatically correct in {native_lang}."
- "Respond with ONLY the Modified Native sentence and nothing else."
- One worked example (Janet → Andrea, French). Gemini-1.5-pro for the pipeline evaluation, Gemini-2.5-pro for the
  final data.
- The direct-prompting baseline instead asks the LLM to find and replace the entities itself, and allows "If an
  entity does not have a direct cultural equivalent or is already culturally neutral, it may remain unchanged."

**Automatic checks**

| Check | Threshold / rule | Source |
|---|---|---|
| No overlapping or inconsistent replacements | rule | §3.1 |
| Single currency type per problem "to avoid conversion errors" | rule | §3.1 |
| Length of localised output equals length of the direct translation | `length(x_loc) == length(x_trans)` | Table 1 |
| Original key entities absent from the output | rule | Table 1 |
| Replacement entities present in the output | rule | Table 1 |
| Similarity between localised and translated text (`difflib`) | `> 0.8` | Table 1 |
| Translation quality (training data only) | SSA-COMET `> 0.65` | §3.2 |
| Fallback | any failure → return `x_trans` | Table 1 |

The released code differs slightly: the similarity check is `difflib.SequenceMatcher(...).ratio() >= 0.7` by default,
computed after removing the replacement words, with up to 3 retries that feed the failure back into the prompt.

**Human validation**
- Three independent annotators labelled each instance "as either a valid or invalid localization". Cohen's kappa:
  **0.79 for the auto-localised set and 0.84 for the direct-prompting set** (two values for two sets, not a range).
- What they judged (Appendix C): whether "English-centric names, currencies, or organization names had been replaced"
  in the English `x_ent` → *Culturally Localized* / *Not Localized*. It was done once and "applied across all
  languages".
- Not judged by these annotators: native-language fluency, cultural fit of the chosen entity, or whether the answer
  is preserved. Who the annotators were is not stated.
- Test set: "verified through manual inspection by the authors" (Table 1: full human verification for the test set,
  sampled for the training set).

## Key findings
1. **Controlled pipeline beats free prompting on coverage.** Of ~250 annotated sentences, the pipeline localised
   ~243 and left ~6; direct prompting localised ~70 and left ~180 (read off Figure 2). Direct prompting "often
   returns the original translation rather than a properly localized version".
2. **Accuracy effect on native-language problems is small.** In Figure 3 most models score slightly lower on the
   localised set. For GPT-4o-mini the largest gaps are ~3 points (Xhosa ~15 → ~11.5, Swahili ~27 → ~24.5), and a
   few languages go up (Ewe, French, Hausa). All scores are low (under ~30% numeric match). The introduction states
   "as much as 9% (numeric match) drop in performance for GPT-4o-mini"; no table or figure in the paper shows a
   9-point gap.
3. **In English the direction reverses for some models** (Figure 4). With native entities inserted into the English
   problems, GPT-4o-mini rises from ~23% to ~29–32% and LLaMA-3-70B from ~34.5% to ~38–41%; Aya-expanse-32b falls
   from ~31% to ~23–27%.
4. **Fine-tuning on localised data helps a little** (Table 3, ∆NM = NM localised − NM translated). Languages with
   positive ∆ out of 17: LLaMA-3-8B 6 (translated data), 4 (English entity-replaced), 10 (auto-localised), 14 (all
   data); Gemma-2-9b-it 5, 8, 15, 16. All ∆ values lie within about ±2.3 points, and the table picks a different
   training size per language.
5. **Many items have nothing to localise.** In the training data ~145–220 of 1,500 selected items per language had
   no entity replacement (Figure 5).

![[Azime2025-fig-02-p5.png]]
*Figure 2: human labels for auto-localisation vs direct prompting with Gemini-1.5-pro (sentences labelled Culturally Localized / Not Localized).*

![[Azime2025-fig-03-p6.png]]
*Figure 3: numeric match on translated (AfriMGSM) vs localised (Localized-AfriMGSM) problems, six models, 17 languages.*

**Error categories and failure modes**
- *Not localised:* "names or organization names the pipeline was not able to capture and fallback output because
  quality checker".
- *Wrong entity type:* organisation names containing a personal name (e.g. "Dr. Wertz's School") are treated as
  person names or swapped for another kind of organisation, "thereby distorting the original meaning". Authors'
  advice: prioritise "well-defined entities such as person names and currencies".
- *Non-numeric model outputs* (Table 5; 17 languages × 3 prompts × 250 items = 12,750 answers per prompt):
  Aya-expanse-32b gives 7,281 non-numeric answers on prompt 2, LLaMA-3-70B 1,141 on prompt 3, GPT-4o-mini at most 80,
  Gemma-2-27b-it at most 16. Because of this the native-language results use the best prompt, not the average.
- The authors' own scope statement: the data "is best utilized as a scalable resource for augmenting training data,
  rather than as a fully reliable source of semantically precise transformations."

## Relevance to research questions
### Q8: Injecting cultural cues into datasets
This is the most complete general-domain recipe for controlled cue injection, and its structure fits our case table:
keep the LLM away from *choosing* the cue, let a curated source choose it, and let scripts verify the result.

**What transfers to medical cases**
- The split of roles: LLM tags slots → dictionary (for us, the food ↔ ingredient ↔ compound ↔ condition graph and
  the dish tables) picks the replacement → script substitutes → LLM only smooths the sentence.
- Editing a shared pivot text first, so humans review one replacement dictionary instead of every output.
- Hard string invariants: old cue absent, new cue present, length and similarity close to the source, and
  "return the original if any check fails", so the pipeline never adds noise silently.
- One value per slot type per case (their single-currency rule) to avoid internal contradictions.
- Reporting a direct-prompting baseline: free LLM localisation left most items unchanged.
- Unisex or otherwise attribute-neutral replacements to avoid breaking agreement elsewhere in the text.

**What does not transfer**
- Their slots are answer-neutral by construction. Food, habit, fasting and herbal cues can change the correct
  diagnosis or advice, so we need a clinical-neutrality (or answer re-derivation) check that this paper has no
  counterpart for. The authors avoided food swaps for a weaker reason (loss of contextual meaning).
- Their human validation only asks "was the entity replaced?". It does not test plausibility, cultural fit or answer
  preservation, and it is not by clinicians. The kappa values say nothing about faithfulness.
- The entity database is tiny and unsourced, and the released file contains a wrong-country entry. A medical cue
  dictionary needs provenance per entry.
- Length equality and `difflib` similarity suit one-token swaps. A dish with ingredients, or a habit described in a
  clause, will fail these thresholds; they need to be replaced by slot-level checks.
- The measured accuracy effects are within a few points and unsupported by significance tests, so the paper does not
  show that this kind of cue changes model behaviour reliably.

See [[Q8 Injecting cultural cues into datasets|Q8]]

## Key figures & tables
![[Azime2025-fig-04-p7.png]]
*Figure 4: English problems with native entities (bars) vs default English entities (red line), numeric match.*

Table 2 of the paper (datasets):

| source | split | #source | #localized | #lang. |
|---|---|---|---|---|
| GSM8K | train | 8,790 | 25,100 | 18 |
| Localized-AfriMGSM | test | 4,500 | 4,500 | 18 |

Table 3 of the paper, bottom row (number of languages, out of 17, where the fine-tuned model scores higher on the
localised than on the translated benchmark):

| fine-tuning data | LLaMA-3-8B-Instruct | Gemma-2-9b-it |
|---|---|---|
| translated (`x_trans`) | 6 | 5 |
| English entity-replaced (`x_ent`) | 4 | 8 |
| auto-localised (`x_loc`) | 10 | 15 |
| all data | 14 | 16 |

## Limitations / caveats
- Preprint (arXiv v4, 2026-04-20), no venue listed on arXiv. Some loose ends: both appendix prompts are titled
  "Prompt 3", a figure reference is "Appendix ??", and Figures 3–4 label a model "Gemma-3-27b-it" where the text says
  Gemma-2-27b-it.
- "Three annotators" with "Cohen's kappa" (a two-rater statistic); how it was aggregated is not stated.
- No size, source or validation for the entity database in the paper.
- The headline "9%" drop is not traceable to a table or figure; no confidence intervals or significance tests.
- Final-answer numeric match only; low absolute scores make small differences hard to interpret.
- The authors say the pipeline "is not intended to replace human annotation".
- Related localisation work in the vault: [[Karim2025 - Cultural adaptation of GSM8K for six countries|Karim et al. 2025]],
  [[Tomar2025 - Cultural perturbations of GSM8K|Tomar et al. 2025]] (both cited by this paper).

## Related work to follow
![[Backlog.base#Cited by this paper]]
