---
title: "CCBENCH: Assessing LLM Cultural Competence via Implicitly Signaled Norms using Health Queries"
citekey: Varadarajan2026
authors: [Vasudha Varadarajan, Akhila Yerukola, Mona T. Diab, Maarten Sap]
year: 2026
published: 2026-06-08
venue: "arXiv preprint"
peer_reviewed: false
url: "https://arxiv.org/abs/2607.05405"
arxiv: "2607.05405"
doi: ""
pdf: "[[Varadarajan2026.pdf]]"
pdf_url: "https://arxiv.org/pdf/2607.05405"
datasets: []
topics: [kg-medical-eval]
questions: [Q4, Q5, Q7, Q8]
relevance: core
kind: [case]
availability: contact-authors
access_link: "https://arxiv.org/abs/2607.05405"
countries: "Afghan, Burmese, Chinese, Māori, Nepali, Vietnamese personas"
case_type: [synthetic, diet]
found_by: [search/regional-cases, search/global-cases, search/evaluation, search/culture-cued-cases, search/cue-injection]
added: 2026-10-07
cites:
  - "[[BLEnD (candidate)]]"
  - "[[Bhatt2024 - Extrinsic evaluation of cultural competence]]"
  - "[[Cheng2026 - Cultural Compass]]"
  - "[[Jin2024 - XLingHealth cross-lingual healthcare queries]]"
  - "[[Kantharuban2025 - Stereotype or personalisation]]"
  - "[[Neplenbroek2025 - Stereotypes in implicit personalisation]]"
  - "[[Pawar2025 - Names shape LLM responses]]"
  - "[[Rao2024 - NormAd]]"
  - "[[Singh2024a - Global MMLU]]"
cited_by_count: 0
tags:
  - type/paper
  - relevance/core
  - q/4
  - q/5
  - q/7
  - q/8
  - kind/case
  - case/synthetic
  - case/diet
  - cue/food-habit
  - cue/religion
  - cue/tradmed
  - adapt/generation
  - validity/automatic
  - inject/context
  - eval/open-ended
  - eval/llm-judge
  - eval/human
  - region/south-asia
  - region/southeast-asia
  - region/east-asia
  - region/oceania
  - tradmed/tcm
  - tradmed/ayurveda
---
# CCBENCH: Assessing LLM Cultural Competence via Implicitly Signaled Norms using Health Queries

> [!abstract] TL;DR
> CCBench-Health tests whether an LLM adapts health advice to cultural norms that a user only **signals implicitly**
> in earlier chats. Norms for six cultures come from Mosaica cultural health profiles. 60 synthetic personas each
> follow, avoid or are neutral to every norm; each has 18 generated background conversations and is asked 52 real
> forum health questions (3,120 interactions). A GPT-5.2 judge scores answers against a per-persona checklist. Models
> respect norms the persona *avoids* far more often than norms it *follows* (follow rate ≤ 6.5% from history alone),
> and giving the norms explicitly lifts the follow rate to at most 27%. No data or code link is given.

## What was built
- **Resource:** CCBench (a domain-agnostic framework) and its health instance **CCBench-Health**: 6 cultures × 10
  personas = **60 personas**, 18 background conversation sessions each, 52 health queries → **3,120** persona × query
  interactions. English.
- **Cultures:** Afghan, Burmese, Chinese, Māori, Nepali, Vietnamese. Only six because "high-quality cultural health
  profiles within Mosaica are still being curated".
- **Idea:** culture is "a continuum of norm adherence states rather than … a binary state of cultural belongingness".
  A persona never says where it is from; a model must infer its stance from behaviour in the chat history.

![[Varadarajan2026-fig-02-p4.png]]
*Figure 2: the CCBench-Health pipeline, from Mosaica health profiles to checklist-based evaluation.*

### 1. Where the norms come from
- **Source:** cultural health profiles from **Mosaica** (`my.mosaica.app/discover`, accessed Oct 2025), "a knowledge
  base of cross-cultural and religious insights, curated by culture experts over months of interviews and engagement
  with the communities". The health profile covers "healthcare approaches, communication, wellbeing challenges, diet
  and nutrition, family, women, and dying".
- **Extraction:** "Gemini-3.5-Pro" turns each report (a PDF) into norm–value pairs. The prompt asks for norms that
  people follow "as patients and not as providers", each starting with "The person …", with communication norms
  rewritten for talking to an AI, and a fixed value vocabulary derived from the whole document.
- **Verification:** "We manually verified all the norm-value pairs to ensure there were no values and norms
  hallucinated by the model." No count of corrections, no second source, no review by members of the cultures.
- **Two kinds of norm:** *communication* norms (shown only through style, e.g. saying "yes" to mean "I am listening")
  and *practice-based* norms (stated in content, e.g. halal diet, herbal remedies).

**Table 1: norms and values per culture, and average norm states per persona.**

| Culture | Values | Total norms | Comm. norms | Practice norms | avg Follow | avg Avoid | avg Neutral |
|---|---|---|---|---|---|---|---|
| Afghan | 9 | 13 | 5 | 8 | 3.2 | 3.6 | 6.2 |
| Burmese | 18 | 15 | 8 | 7 | 3.8 | 3.8 | 7.4 |
| Chinese | 8 | 20 | 6 | 14 | 7.8 | 7.9 | 4.3 |
| Māori | 10 | 19 | 8 | 11 | 4.7 | 4.3 | 10.0 |
| Nepali | 9 | 13 | 4 | 9 | 3.6 | 4.8 | 4.6 |
| Vietnamese | 10 | 15 | 5 | 10 | 7.0 | 3.9 | 4.1 |

**Diet, religion and traditional-medicine norms per culture** (from appendix Tables T1–T6; norm ids in brackets, wording shortened).

| Culture | Diet / food | Religion / spiritual | Traditional medicine / illness beliefs |
|---|---|---|---|
| Afghan | follows Halal dietary laws, "avoiding pork, alcohol, and non-halal meat" [8]; **fasts during Ramadan** and may need medication schedules adjusted [9]; diet high in carbohydrates and sugar, low water intake [10] | prefers a female-coded voice for sensitive matters "to maintain religious modesty boundaries" [3]; modesty rules in physical examination, e.g. keeping the hijab on [12] | none listed |
| Burmese | dietary restrictions from religion (e.g. Halal) or culture ("Ayurvedic heating/cooling foods") [13] | (same norm [13]); female-coded provider preferred, linked to "Religious Observance" [5] | traditional herbal remedies alongside Western advice [10]; distress as somatic complaints [8] and idioms such as "thinking too much" [9] |
| Chinese | dietary therapy by "hot" or "cold" food properties [7]; warm or room-temperature food and drink during illness, no cold or raw food [19] | avoids appointments on dates with 4, 14 or 24 [15]; prefers the body intact after death, reluctant about organ donation or autopsy [18] | illness as imbalance of Yin and Yang or Qi [6]; TCM (herbs, acupuncture) for the "root cause" alongside Western medicine [8]; stops Western medication when symptoms subside or cuts the dose [9]; Western medicine seen as "strong", herbs used to offset side effects [10] |
| Māori | strict separation of food (noa) from sacred items (tapu) "such as medication" [11]; prayer (karakia) before food, medication or procedures [15] | illness attributed to spiritual causes (mate Māori) or breaches of tapu [9]; the head is tapu [10]; return of body tissue (e.g. placenta) to the earth [18]; holistic view of health (Te Ao Māori) [5] | traditional plant medicine (Rongoā) or spiritual healing alongside Western medicine [12] |
| Nepali | diet and illness managed by Ayurvedic "hot" / "cold" classes of foods and medicines [6]; **fasting as spiritual cleansing**, may refuse oral medication or food in religious periods [10]; right hand "clean", left hand "polluted" for food [11] | illness attributed to karma, planetary alignments or supernatural forces [5]; purity rituals around menstruation and childbirth [9] | Ayurvedic principles [6]; reluctant to take long-term pharmaceuticals, prefers "natural" remedies [7]; expects immediate relief, sees injections as stronger than tablets [8] |
| Vietnamese | dietary therapy by "heating" or "cooling" food properties [7] | illness attributed to spirits, bad karma or past moral transgressions [12]; chronic pain in old age seen as natural or karma [15] | imbalance of Am/Duong, "wind" (Phong), hot/cold [6]; herbal medicine, coining (printed "coing" in the extraction), cupping alongside Western advice [8]; stops Western medication early [9]; Western medicine "too strong" or "hot", balanced with "cooling" remedies [14] |

The other norms (not in the table) are about communication and family: deference to authority, indirectness, "silent
compliance", stoicism, somatic expression of distress, same-gender preference, family or elder decision-making.

### 2. How norm adherence is sampled per persona
- Each culture has values V and norms N; each norm maps to one or more values (e.g. Afghan norm 9, Ramadan fasting →
  "Religious Adherence (Islamic Principles)").
- For each persona, every **value** is randomly set to adhere (+1) or not adhere (−1).
- A **norm's** score is the mean of its values' scores: positive → **Follow**, negative → **Avoid**, zero →
  **Neutral**.
- "by sampling 10 unique adherence combinations per culture, the benchmark avoids monolithic identity assumptions".
- Our reading of the design: norms tied to one value are never neutral and move together (an Afghan persona follows
  or avoids halal and Ramadan fasting as a pair); norms tied to two values are neutral whenever the values disagree.

### 3. How cues are signalled implicitly
- **Background histories:** GPT-5.2 role-plays persona ↔ assistant conversations, conditioned on the persona's norm
  states and a **starter query**. Per persona: 15 sessions seeded with first turns from WildChat-1M (clustered with
  all-MiniLM-L6-v2; coding, essay and similar clusters dropped) and 3 seeded with hand-picked health and lifestyle
  prompts written with GPT-4.
- **Generation rule (prompt F4):** "Never directly state or explicitly label the persona's background, culture, or
  values—allow these elements to be inferred only from the persona's choices, cues, references, and behaviors."
- **Communication norms** "emerged stylistically"; **practice-based norms** "were stated directly".
- **Filtering:** explicit identity statements ("I am from [country]") are removed; "cultural greetings (e.g.,
  Namaste) or religious artifacts (e.g., I eat halal food) were retained as implicit cues". In the verification
  prompt, "practices, foods, or traditions like yoga or Ramadan are implicit references unless the speaker explicitly
  identifies a cultural group or identity (e.g., 'I am Indian' or 'I am Muslim')".
- **Automatic check (GPT-5.2, prompt F8):** per norm, is it inferrable from the conversation, does the behaviour
  match the assigned state, is culture explicitly revealed. Result (Table 2): conversational norm adherence 0.947
  overall (Afghan .93, Burmese .93, Chinese .95, Māori .90, Nepali .98, Vietnamese .99); explicit reveal 0.000.
- Many WildChat-seeded sessions surface no norm at all; this is intended, to make the history realistic.

![[Varadarajan2026-fig-08-p27.png]]
*Figure F6: a health-seeded background conversation in which an Afghan persona reveals a diet norm (rice, bread, sweet tea, little water) without naming a culture.*

### 4. Health queries
- From the eHealth Forum and iCliniq question–answer data (Regin 2017, GitHub `LasseRegin/medical-question-answer-data`).
- 12 health categories derived by hand from existing tags (e.g. Disease, Mental Health, Reproductive Health).
- GPT-5.2 annotates each query's relevance to the extracted norms; only queries "relevant to over 90% of norms" are
  kept, then stratified over the 12 topics → **52 queries**. The same 52 are asked of every persona.
- The forums' original doctor answers are not used as references.

### 5. How responses are judged
- **Checklist:** for every norm the persona follows or avoids (neutral norms are skipped), GPT-5.2 writes "a specific
  recommendation" for how the answer to this query should accommodate following (+1) or avoiding (−1) the norm.
  Example from the judge prompt: norm "Accommodate fasting during Ramadan in medication schedules" → recommendation
  "Adjust patient's medication time to after sunset to respect fasting practices."
- **Judge:** GPT-5.2 marks each recommendation `adherence: true/false` with reasoning; it is told to "lean towards
  false unless full alignment can be justified". The score is the proportion of satisfied items.
- **Metrics:** Follow Rate ("Cultural Sensitivity"), Avoid Rate ("Stereotype Resistance"), Overall Norm Adaptation
  (all Follow and Avoid items), and **Cultural Competency Score (CCS)** = harmonic mean of Follow and Avoid rates.
- **Settings:** *None* (query only) · *Hist.* (background history + query) · *C-CoT* (history + instruction to first
  identify cultural cues, then tailor the advice) · *Norms* (ground-truth norm definitions and adherence states in
  the system prompt, "a theoretical upper bound").
- **Models:** GPT-5.2, Gemini-2.5-Pro, DeepSeek-R1, Llama (90B), Qwen-3.5-397B in the tables; temperature 0.7.

### 6. Human agreement
| What was checked | Sample | Agreement |
|---|---|---|
| Background-conversation verifier: does the persona follow or avoid the norm? (Table T7) | 50 sessions, one norm each, Neutral cases dropped | annotator 1 vs 2: 100.0% (κ 1.0); annotator 1 vs LLM: 78.8%; annotator 2 vs LLM: 87.5% (κ 0.6) |
| Explicit reveal of culture | same sample | annotator 1 vs 2: 98.0%; vs LLM: 100.0% and 98.0% |
| Checklist judge: is the response competent ("direct alignment with the persona's preference")? | 50 responses | annotator 1 vs 2: 74% raw; LLM vs annotator 1: 64%; LLM vs annotator 2: 62% |

- Two annotators; who they are (cultural background, clinical training) is not stated.
- No chance-corrected agreement is given for the checklist judge.

## Key findings
1. **Low competence everywhere.** Best CCS from history alone is .115 (GPT-5.2); with C-CoT .172; with explicit
   norms .318 (Gemini-2.5-Pro). Overall Norm Adaptation is .198–.287 from history and at most .361 with explicit
   norms; this is the "20–30%" of the abstract.
2. **Follow ≪ Avoid.** GPT-5.2 with history: Avoid Rate 51.7%, Follow Rate 6.5%. Without any context the Avoid Rate
   is already 47.3%, so most of the "stereotype resistance" is the default culture-free answer. The authors call
   this a "Western default".
3. **Explicit norms are not enough.** Follow Rate with the norms in the system prompt: Gemini .267, DeepSeek .237,
   GPT-5.2 .222, Llama .145.
4. **C-CoT helps a little** (GPT-5.2 CCS .115 → .172; Gemini .088 → .172). Qwen breaks with extra context ("failed
   to produce final outputs in 50% of cases").
5. **Culture differences** (Figure 4, all models): Follow 0.7–7.4% in every culture; Avoid from 71.2% (Māori) to
   15.6% (Afghan). Afghan average CCS is 0.088.
6. **The more norms a persona follows, the less the models adapt** (Figure 3).
7. **Style vs practice** (Figure 5): communication norms are met more often than practice norms for Afghan
   (.19 vs .04) and Nepali (.57 vs .26) personas; the reverse for Māori (.28 vs .52).
8. **Topic** matters little; Relationships and Addiction score best.

![[Varadarajan2026-fig-04-p7.png]]
*Figure 4: Follow vs Avoid adherence by culture, averaged over models.*

![[Varadarajan2026-fig-05-p8.png]]
*Figure 5: average adaptation to communication (implicit) vs practice-based (explicit) norms by culture.*

**Table 3 (two of four panels).** Columns: no context · history · Culture-CoT · explicit norms.

| Model | CCS None | Hist. | C-CoT | Norms | Follow None | Hist. | C-CoT | Norms |
|---|---|---|---|---|---|---|---|---|
| GPT-5.2 | .036 | .115 | .172 | .309 | .035 | .065 | .103 | .222 |
| Gemini-2.5-Pro | .023 | .088 | .172 | .318 | .021 | .049 | .105 | .267 |
| DeepSeek-R1 | .031 | .080 | .092 | .255 | .023 | .044 | .051 | .237 |
| Llama-90B | .025 | .049 | .069 | .185 | .018 | .026 | .038 | .145 |
| Qwen-3.5-397B | .019 | .109 | .087 | .009 | .014 | .062 | .064 | .009 |

| Model | Avoid None | Hist. | C-CoT | Norms | Overall None | Hist. | C-CoT | Norms |
|---|---|---|---|---|---|---|---|---|
| GPT-5.2 | .473 | .517 | .525 | .509 | .248 | .287 | .307 | .361 |
| Gemini-2.5-Pro | .382 | .453 | .469 | .394 | .197 | .245 | .278 | .326 |
| DeepSeek-R1 | .382 | .460 | .464 | .277 | .219 | .247 | .251 | .249 |
| Llama-90B | .397 | .379 | .390 | .255 | .203 | .198 | .207 | .191 |
| Qwen-3.5-397B | .286 | .437 | .136 | .009 | .147 | .242 | .098 | .008 |

## Data-release status
- The paper (v1, 34 pages) contains **no link** to data or code and no release statement. The only resource URLs are
  Mosaica and the forum-question repository.
- All prompts are printed in the appendix (F1 norm extraction, F4 history generation, F8 verification, F9 checklist
  judging), and all 95 norms with their values are in Tables T1–T6. The personas, conversations, the 52 queries and
  the checklists are not included.
- So the norm inventory can be reused now; the benchmark itself would have to be requested from the authors or
  regenerated.

## Relevance to research questions
### Q4: Patient case-conclusion datasets
- **Case:** a synthetic user (norm states + 18 chat sessions) plus a real forum health question. **Conclusion:** not
  a diagnosis or a medical answer but a per-persona **checklist of cultural accommodations** written by GPT-5.2.
- Diet is central for part of it (halal, Ramadan fasting and medication timing, hot/cold foods, sweet tea and low
  water intake), so it fits `case/diet`.
- 3,120 interactions, 52 distinct questions, English, six cultures. **Not obtainable today.**
- It is the closest existing design to "advice must change because of a food or religious practice", but medical
  correctness of the advice is not scored.

See [[Q4 Patient case-conclusion datasets|Q4]]

### Q5: Evaluating KG-augmented medical LLMs
- The **Norms** setting is knowledge injection in its simplest form: the relevant cultural facts are placed in the
  system prompt. It is an oracle (no retrieval error), and the best three models still follow only 22–27% of the norms a persona
  holds (Llama 14.5%). So for a cultural KG, **supplying the right knowledge does not guarantee that it is used**; evaluation must
  score use of the knowledge in the answer, not only retrieval.
- A ready-made ladder of conditions: no context → implicit history → history + cue-focused reasoning → explicit
  knowledge. A KG condition would sit between the last two.
- **Checklist scoring** fits open-ended advice: one checklist item per relevant fact, judged true/false, with separate
  rates for "should apply" and "should not apply". The Avoid Rate is a useful control against over-applying
  cultural knowledge (stereotyping), which a KG-augmented model is at risk of.
- Weak point to improve on: judge–human agreement is only 62–64% (humans 74%), and the checklist is LLM-written.

See [[Q5 Evaluating KG-augmented medical LLMs|Q5]]

### Q7: Cultural cues in evaluation datasets
- **Cues present:** culture-specific food and diet habits, religious practice (halal, Ramadan and other fasting,
  modesty, karakia), traditional medicine (TCM, Ayurveda hot/cold, Rongoā, herbal remedies, coining, cupping), and
  communication style. Country and ethnicity are **deliberately absent** from the text.
- **Cue form:** implicit, spread over a multi-session dialogue history; the norm states are known per persona, so
  each item has structured labels (norm id, Follow / Avoid / Neutral).
- **Does the cue change the expected answer?** Yes: the checklist depends on the persona's states.
- **Gold answer:** an LLM-generated checklist of cultural accommodations, not a medical conclusion. There is no check
  that the accommodated advice is clinically right.
- **Access:** not released. The 95 norms in the appendix are usable as a cue inventory for six cultures; none of
  them is from the Gulf or Central Asia (Afghan is the nearest).

See [[Q7 Cultural cues in evaluation datasets|Q7]]

### Q8: Injecting cultural cues into datasets
- **What is injected:** a persona's stance (follow or avoid) on expert-sourced health norms, expressed as behaviour
  in generated background conversations that are prefixed to an unchanged real health question.
- **Method:** generation, not rewriting. Mosaica profile → LLM-extracted norm–value pairs → random value states →
  derived norm states → GPT-5.2 role-play seeded with real WildChat openers → LLM filter for consistency and for
  explicit identity statements. The health question itself is not edited.
- **Gold answer:** **re-derived per persona.** There is no invariant answer; the reference is a checklist generated
  by GPT-5.2 from the non-neutral norms and the query. Clinical correctness is neither assumed nor checked.
- **Faithfulness / validity checks:**
  - norm–value pairs: manual check by the authors against the Mosaica reports (no numbers);
  - conversations: GPT-5.2 verifier, 0.947 norm-adherence consistency and 0.000 explicit reveal; on 50 sessions the
    two annotators agree with each other 100% (κ 1.0) and with the LLM 78.8% and 87.5% (κ 0.6);
  - checklist judging: 50 responses, human–human 74%, LLM–human 64% and 62%;
  - the ethics statement says all norm curation, history generation and checklist evaluations "were manually
    reviewed", without detail;
  - **no clinician** and no member of the six cultures is reported as a rater.
- **Reusable ideas:** (1) take cues from an expert-curated cultural health source instead of letting the LLM invent
  them; (2) sample adherence per person so that the cue is not a stereotype, and include *avoid* cases as controls;
  (3) keep the cue implicit and filter out explicit identity; (4) store structured labels for every injected cue.
- **Gap for us:** the method changes the *patient*, not the clinical case, and has no medically verified reference.
  Our injection needs a cue that changes a checkable medical conclusion (e.g. a fasting-related dosing rule or a
  food–drug interaction).

See [[Q8 Injecting cultural cues into datasets|Q8]]

## Limitations / caveats
- **Model list is inconsistent:** the setup text names Claude-3.5-Sonnet, the result tables show DeepSeek-R1.
- Figure F6 is labelled "Session 6 of 25", while the text says 18 sessions per persona.
- The text says "four distinct prompting configurations", then "three settings", and lists four.
- GPT-5.2 generates the conversations and the checklists and judges the answers, and is also the best-scoring model.
- The judge is told to lean towards false, and agreement with humans (62–64%) is below human–human agreement (74%).
- Personas are simulated from one source (Mosaica); the authors note they "could inadvertently contain stereotypical
  phrases or artifacts".
- Every norm counts equally: a medication-timing norm during Ramadan weighs the same as a greeting norm.
- Norm extraction is credited to "Gemini-3.5-Pro"; evaluated models include "Gemini-2.5-Pro" (as printed).
- **Date:** the arXiv abs page says "Submitted on 8 Jun 2026" (v1, only version), although the identifier prefix is
  2607. `published` records the abs-page date.
- Not peer reviewed (arXiv preprint, primary category cs.CY, comment "34 pages"; no venue stated).

## Related work to follow
![[Backlog.base#Cited by this paper]]
