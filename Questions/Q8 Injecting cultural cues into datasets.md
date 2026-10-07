---
question: "Have any works accurately and faithfully injected cultural cues into medical datasets, and if not, which methods and source datasets could we use to do it?"
id: Q8
topics: [kg-medical-eval]
updated: 2026-10-07
tags:
  - type/question
  - q/8
---
# Q8: Have any works accurately and faithfully injected cultural cues into medical datasets, and if not, which methods and source datasets could we use to do it?

> [!summary] Short answer
> **Not in the sense we need.** No work found takes existing medical cases, injects food, habit or
> traditional-medicine cues, and re-derives the gold answer with clinical validation.
> [[Bui2026 - Cross-lingual consistency for medical questions|Bui et al. 2026]] state the same gap: there are "no
> benchmarks capable of distinguishing universally correct from culture-specific cases".
> - **What exists is bias auditing:** about 20 works add race, gender, income or religion to vignettes and require the
>   answer to stay the same. The one explicitly cultural study,
>   [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA|Rezaei & Shakeri 2026]], deliberately uses cues that do
>   not affect the answer.
> - **Answer-changing designs exist only in narrow forms:** location swaps in
>   [[Asiedu2024 - TRINDs tropical and infectious diseases|TRINDs]] and
>   [[Pfohl2024 - EquityMedQA health equity toolbox|EquityMedQA]], country-specific guidelines, Ramadan dosing, a
>   country-conditioned herbal answer in [[Nimo2025 - Africa Health Check|Africa Health Check]], persona norms in
>   [[Varadarajan2026 - CCBench|CCBench]].
> - **The method is available from general-domain localisation work:** typed slots → a curated, sourced per-culture
>   dictionary → deterministic substitution → automatic checks → human review
>   ([[Azime2025 - Socio-cultural localisation of math word problems|Azime et al. 2025]],
>   [[Karim2025 - Cultural adaptation of GSM8K for six countries|Karim et al. 2025]]). Free LLM rewriting is the
>   known-bad option. These pipelines swap names and currencies only; Azime et al. left food out on purpose.
> - **Medicine adds one check nobody has automated: clinical neutrality.** A food swap can change the answer
>   (grapefruit, vitamin K, tyramine, fasting). Our graph can test this, which is the part no existing work has.
> - **Sources for accurate cues:** our own dish tables, WHO GHO and GBD for plausibility, WHO STEPS and tobacco
>   surveys for habits, IDF-DAR for fasting rules, CPIC for ancestry-linked drug response, and the real cued cases
>   in [[MedCaseReasoning]] and [[PerMedCQA]] as a realism reference.

## Detailed answer

### 1. What "faithful injection" has to mean
Three separate properties, of which existing work checks at most two:
1. **Content preservation:** everything clinical that was not meant to change is unchanged (numbers, labs, drugs).
2. **Cultural accuracy:** a person from the culture finds the cue natural and correct (the right dish for the
   country, not Bangladeshi currency for an Indian Bengali).
3. **Clinical consistency:** the gold answer is still right. Either the cue is *inert* and the answer is unchanged,
   or the cue is *decisive* and the answer is re-derived from a cited rule.

### 2. Medical work that injects cues and keeps the answer fixed (bias audits)
| Work | What is injected | Method | Faithfulness check |
|---|---|---|---|
| [[Rezaei2026 - Counterfactual Cultural Cues in Medical QA\|Rezaei & Shakeri 2026]] | cultural identifier, context cue or both; 3 groups incl. Middle-Eastern Muslim | LLM few-shot rewrite, "no new clinical information" (the model is not named) | one clinician reviewed every item (no credentials, rejections or agreement reported); neutral-sentence control |
| [[Xiao2025 - FairMedQA\|FairMedQA]] | a generated social background for race, sex or income (4,806 variants of 801 vignettes) | LLM generation agent that sees the correct answer and an "attack direction", plus a validation agent, on neutralised vignettes | 4 auditors (AI researcher, medical researcher, 2 students; no practising clinician stated) on all variants, 90% initial unanimity, ~340 person-hours, <100 variants edited; attribute-dependent items excluded first |
| [[Rawat2024 - DiversityMedQA\|DiversityMedQA]] | gender, ethnicity sentence | template | GPT-4 judges whether the change matters clinically, then manual cleaning |
| [[Loge2021 - Q-Pain\|Q-Pain]] | name, race, gender slots | template | two physicians rated every vignette |
| [[Shaier2023 - Demographic effects on biomedical QA\|Shaier et al. 2023]] | ethnicity, sex, orientation | template | 100 vignettes verified by two medical experts |
| [[Benkirane2024 - Counterfactual patient variations (CPV)\|CPV]] | gender, ethnicity | rewrite | rule-based exclusion (pregnancy, stated ethnicity) |
| [[Ness2024 - MedFuzz\|MedFuzz]] | patient characteristics chosen adversarially | attacker LLM | instruction that a clinician would keep the answer |
| [[Testoni2026 - Religion and sexual-orientation markers in medical QA\|Testoni et al. 2026]] | religion, sexual orientation | one templated sentence | none on the items |
| [[Omar2025 - Sociodemographic biases in LLM medical decisions\|Omar et al. 2025]] | 31 sociodemographic groups | variants of 1,000 ED cases | physician-derived baseline (abstract only) |

Lessons:
- **Validation ranges from every item re-read by clinicians to nothing.** The strongest is
  [[Gourabathina2025 - MedPerturb|MedPerturb]], where three clinicians re-answer every perturbed context (7,200
  reads); the weakest add a sentence and assume invariance.
- **"Is the cue clinically relevant?" is handled by exclusion.** Items where sex or ethnicity matters are dropped,
  not modelled. Testoni et al. concede that "some identity cues may be statistically associated with particular
  conditions".
- **An LLM rewrite can smuggle in a hint.** FairMedQA's generator is told to push "favourable" groups (White, male,
  high income) toward the correct answer and the others toward a wrong option, so its 3–19 point gaps mix model bias
  with hint strength; a bare token swap on the same vignettes gives under 1%. One released item leaks the answer
  ("efficacy in cross-linking DNA" where the key is "Cross-linking of DNA"). Its automatic validation tests whether
  the answer flips, not whether the variant is clinically valid.
- **One reviewer is not enough.** Reading the released Rezaei items against the originals, our paper-note pass found
  variants where the answer is no longer protected: item 80 replaces the original "African-American", on which the
  melanoma answer rests; item 141 adds a dye-factory history that gives away "aromatic amines"; context variants are
  light paraphrases, not pure insertions. Its accuracy drop (3.1–6.7 points with identifier + context, option-only
  prompting) is significant in only 3 of 15 model × group comparisons, and its neutral sentence alone moves accuracy
  by up to 4 points.
- **A paraphrase control is required.** [[Yang2026 - Baselines for counterfactual prompting|Yang et al. 2026]] show a
  gender swap flips 14.9% of MedQA answers while a plain paraphrase flips 14.1%.
- **Already in our data:** [[MedArabiQ]]'s `multiple-choice-withbias.csv` has 13 of 100 MCQs with an injected
  "cultural" biasing sentence (e.g. "in some cultures a change of voice in women is attributed to age or smoking");
  the gold answer is unchanged. It is a bias probe of the same kind, in Arabic.

### 3. Medical work where the cue legitimately changes the answer
- **Place → diagnosis.** [[Asiedu2024 - TRINDs tropical and infectious diseases|TRINDs]] swaps the endemic location
  for San Francisco and accuracy falls. [[Pfohl2024 - EquityMedQA health equity toolbox|EquityMedQA]]'s CC-Manual set
  mixes pairs with the same ideal answer and pairs where "change in geographical location changes the most likely
  diagnosis", and its rubric's first question is "Do the ideal answers to these questions differ?".
  - Raters said yes for most pairs: physicians 57%, health-equity experts 68% (our tally of the released
    `ratings_counterfactual.csv`, 1,012 ratings).
  - **They often disagree on it:** Randolph's κ is 0.466 among physicians and 0.255 among equity experts. Whether a
    cue should change the answer is itself a hard judgement.
  - The pairs carry no gold answer and no "should differ" label, and only two CC-Manual seeds vary the city. The
    LLM-generated pairs (CC-LLM) passed only LLM quality filters.
- **Country → guideline.** [[Zeng2025 - Geographically tailored colorectal screening advice|Zeng et al. 2025]] ask the
  same 54 cases for four countries and score against each national guideline (40.7–63.0% correct).
  [[Bazerbachi2026 - Cultural bias in neuroradiology guidelines|Bazerbachi et al. 2026]] find models follow the US
  guideline in 27 of 30 conflicting cases.
- **Religious practice → dosing.** [[RamadanSafeQA]] and
  [[Alomair2026 - Ramadan medication advice by chatbots|Alomair et al. 2026]] score advice against the IDF-DAR
  guideline; 11% of chatbot answers were harmful.
- **Country → traditional remedy.** [[Nimo2025 - Africa Health Check|Africa Health Check]] generates MCQs from a
  curated country–remedy table with no-context, full-context and misleading-context variants.
- **Persona norms → advice.** [[Varadarajan2026 - CCBench|CCBench]] samples norm-adherence states per persona and
  signals them implicitly in chat history. Models honour a norm the persona follows at most 6.5% of the time from
  history alone, and at most 26.7% even when the norms are stated explicitly. The norms come from Mosaica cultural
  health profiles and were manually verified; the reference checklist is LLM-written, the judge agrees with humans
  62–64% of the time, and no clinician checked the adapted advice.
- **Gold answers themselves are culture-bound.**
  [[Dey2025 - Beyond the Rubric|Dey et al. 2025]] show HealthBench rubrics marking correct Indian diet advice wrong;
  [[Hisada2025 - HealthBench for the Japanese medical system|Hisada et al. 2025]] find over 60% of HealthBench rubric
  criteria need localisation for Japan. Keeping the original gold after localisation is unsafe.

In every one of these the "rule" that changes the answer is a guideline or a curated table. None uses a food or
ingredient knowledge base, and none covers Central Asia.

### 4. LLMs do not do this faithfully on their own
- Models asked to write an answer-changing minimal edit produce a valid one 25.3% of the time
  ([[Purkayastha2026 - Counterfactual fragility in clinical evaluation|Purkayastha et al. 2026]]).
- LLM-synthetic Indian consultations drift "toward US-like interaction"
  ([[Shailya2026 - Cultural perspective on doctor-patient conversations|Shailya et al. 2026]]).
- Three LLMs adapting the same problem agree on the specific substitute in 33.5% of cases, lose diversity, and mix up
  neighbouring cultures ([[Suchdev2026 - Auditing cultural translation of math word problems|Suchdev et al. 2026]]).
- A bare nationality or persona token gives surface variation, instability and stereotypes
  ([[Bhatt2024 - Extrinsic evaluation of cultural competence|Bhatt & Diaz 2024]],
  [[Beck2023 - Deconstructing sociodemographic prompting|Beck et al. 2023]],
  [[Wang2024a - LLMs misportray and flatten identity groups|Wang et al. 2024]],
  [[Zhang2026a - Cultural alignment vs diversity trade-off|Zhang et al. 2026]]).

### 5. Transferable methods from general-domain localisation
- **Pipeline** ([[Azime2025 - Socio-cultural localisation of math word problems|Azime et al. 2025]]): LLM tags
  entities → replacement from a volunteer-curated native entity dictionary → scripted substitution in the English
  pivot → one-shot LLM edit of the native sentence → automatic checks, with fallback to the unlocalised text on any
  failure.
  - Checks: no overlapping replacements, one currency per problem, same length as the translation, original entities
    absent and replacements present, similarity > 0.8 (the released code defaults to 0.7).
  - It localises ~243 of ~250 items against ~70 for free prompting (read off the paper's Figure 2).
  - **Its human check is narrow:** three annotators judged only whether English-centric entities were replaced in the
    English text (kappa 0.79 for the pipeline set, 0.84 for the prompting baseline). Nobody rated native-language
    fluency, cultural fit or answer preservation.
  - **Its dictionary is small and has errors:** 6–14 names, 5–19 organisations and 1 currency per language in the
    released file, and the Kinyarwanda entry lists Nigerian organisations and "naira".
  - **Food names were deliberately excluded** because swaps "tend to generate sentences that lack contextual
    meaning". Food is the cue we most want, so this part does not transfer and needs the graph.
- **Deterministic variant** ([[Karim2025 - Cultural adaptation of GSM8K for six countries|Karim et al. 2025]]):
  placeholders for 54 entity types, hand-built per-country dictionaries, scripted one-to-one substitution. Annotators
  still judged only 73.8% and 79.2% of sampled items correct before fixes, so the dictionary itself needs native
  review.
- **Quality rubric** ([[Singh2024 - LLMs for intralingual cultural adaptation|Singh et al. 2024]]): per-item (edited?
  correct? localisation level) and per-text 1–5 scales for localisation, naturalness, content preservation,
  offensiveness and stereotyping; human scores correlate with an LLM judge. Its typical failure is a substitute that
  breaks the item's function, which in medicine is a substitute that changes the clinical function.
- **Ontology-driven swap** ([[Gallifant2024 - RABBITS drug-name swaps|RABBITS]]): brand ↔ generic drug names via
  RxNorm with two rounds of physician review. The same recipe fits local drug and food names.
- **Tag before adapting** ([[Singh2024a - Global MMLU|Global MMLU]]): label items as culturally sensitive or
  agnostic first; 28% of MMLU needs cultural knowledge.
- **Graded cue strength** ([[Rao2024 - NormAd|NormAd]]): country only → abstract value → explicit norm, for ablations.
- **Entity lists and item inventories:** [[Naous2023 - CAMeL cultural bias in LLMs|CAMeL]] (20,368 Arab vs Western
  entities incl. food and drink), [[Sahoo2025 - DIWALI culture-specific items for India|DIWALI]] (~8k items for 36
  Indian sub-regions).

### 6. Source datasets for accurate cues
| Cue | Source | Coverage of our regions | Access |
|---|---|---|---|
| dishes and ingredients per country | our unified database ([[Unified database]]): [[Saudi Food Composition Tables]], [[Bahrain Food Composition Tables]], [[Kyrgyzstan Food Composition Table]], [[Central Asian Food Dataset]], [[Indian Nutrient Databank (INDB)]], [[Our Regional Cuisines (Japan MAFF)]], [[XiaChuFang Recipe Corpus]]; native-written [[BLEnD]], [[ArabCulture]], [[World Wide Dishes]] | Saudi, Bahrain, Kyrgyz, Indian, Japanese, Chinese | local ✅ |
| is the condition plausible for the country, age, sex | [[WHO Global Health Observatory]]; [[Global Burden of Disease (GBD) results]] | all | open API; free account |
| habits (smokeless tobacco, waterpipe, salt, alcohol) | [[WHO NCD Microdata Repository (STEPS, GATS)]] | STEPS: Kyrgyzstan, Uzbekistan, Tajikistan, Kuwait, Qatar, Iraq, Jordan, Bangladesh, Nepal… **none for Saudi Arabia, UAE, Bahrain, Oman, Kazakhstan, India, China, Japan, Korea** | STEPS on request; tobacco surveys open |
| what is eaten, how much | [[Global Dietary Database]] (modelled); [[FAOSTAT Food Balance Sheets]] (supply); [[KNHANES]], [[China Health and Nutrition Survey (CHNS)]] | all (modelled); Korea; China | account; open; registration |
| fasting rules that change dosing | [[IDF-DAR Diabetes and Ramadan Practical Guidelines 2021]] | Muslim-majority populations | free PDF |
| ancestry → drug response | [[CPIC and ClinPGx (PharmGKB)]] | group level (East Asian, Central/South Asian, Near Eastern) | open API |
| traditional remedies and herb–drug interactions | vault: [[SymMap]], [[HERB]], [[IMPPAT]], [[GRAYU]], [[UNaProd]], [[TM-MC]], [[DDID]], [[FooDrugs]]; which system per country: [[WHO Global Report on Traditional and Complementary Medicine 2019]] | China, India, Iran, Korea, Japan | local ✅; PDF |
| cultural habit statements | [[CANDLE cultural commonsense]], [[CultureAtlas]] | global, web-derived: verify before use | open |
| how clinicians actually write cues | real cued cases in [[MedCaseReasoning]] (2,761 with a cue, [[Q7 Cultural cues in evaluation datasets\|Q7]]), [[PerMedCQA]], [[PMC-Patients]] | global; Iran | open |

Not found: a structured dataset of food taboos or postpartum food practices by country, or of traditional-remedy use
prevalence. These would have to be compiled from survey papers. Do not cite Storhaug 2017 for lactose malabsorption
by country: it was retracted in 2025.

### 7. A recipe for our case table
1. **Tag** each of the 37,631 cases: already located (leave alone: RuMedBench's opisthorchiasis visits, TCM cases) vs
   culture-agnostic (safe to adapt); mark slots (name, place, food, drink, habit, remedy, religious practice).
2. **Build a sourced slot table per target country** from the sources in section 6. Every entry carries its source.
   Have a native reviewer check the table itself.
3. **Decide inert or decisive per injection.**
   - *Inert* (a neutral local dish, a city): query the graph for the dish's ingredients against the case's drugs and
     conditions; reject the dish if any interaction or condition edge is hit. Gold unchanged → robustness test.
   - *Decisive* (Ramadan fasting on a sulfonylurea, grapefruit-like interactions from [[DDID]], raw camel milk, a
     herb from [[HERB]] with a drug): pick the cue *because* an edge is hit, and re-derive the gold from the cited
     rule → cultural-competence test. This is the set no existing work has.
4. **Sample cues from distributions** (GBD/GHO, intake data), not from a model's idea of the typical patient. The LLM
   only rewrites the sentence around fixed slot values, under a "no new clinical information" instruction.
5. **Automatic checks:** numbers, labs, drugs and diagnosis unchanged; one country per case; graph interaction
   check; similarity threshold.
6. **Controls:** a length-matched neutral sentence (Rezaei) and a paraphrase (Yang 2026) for every item.
7. **Human validation:** a clinician from the region reviews all decisive items and a sample of inert ones with the
   Singh rubric plus "should the conclusion change?" (EquityMedQA); report agreement on the items themselves.

## Comparison table
| Approach | Example | Cue may change the answer? | Gold after injection | Validation | Covers food / tradmed? |
|---|---|---|---|---|---|
| template token | DiversityMedQA, Testoni 2026 | no | kept | LLM filter or none | no |
| LLM rewrite + audit | FairMedQA, Rezaei 2026 | no | kept | 4 non-clinician auditors; one clinician | religion and "heavy meal" context only |
| clinicians re-answer | MedPerturb | either | re-derived by humans | 3 reads per item | no |
| curated pairs + rubric | EquityMedQA CC-Manual | both kinds mixed | none; raters judge | physicians, equity experts | no |
| location swap | TRINDs | yes | label fixed, support removed | clinician-reviewed labels | no |
| guideline per country | Zeng 2025, Ramadan studies | yes | from the guideline | investigators | fasting only |
| table-driven generation | Africa Health Check | yes | from the remedy table | first author | herbal remedies (Africa) |
| persona norms | CCBench | yes | persona checklist | annotators (cultural only) | halal, Ramadan, dietary therapy |
| slot dictionary + script | Azime 2025, Karim 2025 (math) | no | kept | automatic checks; annotators only confirm the swap happened (kappa 0.79) | no: food excluded on purpose |
| **graph-checked injection (proposed)** | — | both, declared per item | kept or re-derived from a graph edge | automatic + regional clinician | yes |

## Gaps & open questions
1. **No one has done decisive food, habit or traditional-medicine injection with a clinical check.** This is an open
   contribution, and the graph is what makes the neutrality check automatic.
2. **Slot tables for the Gulf and Kazakhstan lack survey grounding** (no STEPS, no GIFT). Use GHO indicators, modelled
   GDD intakes and our dish tables, and say so.
3. **Who validates?** Every credible work uses clinicians; for cultural accuracy, natives of the culture. We need at
   least one clinician per target region.
4. **How big is the decisive set?** Bounded by the food–drug and food–condition edges that match drugs and conditions
   present in the cases; a first count against the case table would size it.
5. **Open data to inspect next:** Rezaei's augmented items (GitHub) and EquityMedQA (Figshare) as format references;
   neither is downloaded yet.

## Papers
![[Papers.base#This question]]
