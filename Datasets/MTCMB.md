---
title: "MTCMB"
slug: mtcmb
kind: [case]
version: "GitHub main @ faffd81 (2026-06-27) = Zenodo 10.5281/zenodo.20465629 (2026-05-31)"
previous_versions: "HF Bunnybeck/MTCMB (2025-05-28): same 7,100 items, no `source` field"
papers: ["[[Kong2025 - MTCMB multi-task TCM benchmark]]"]
url: "https://github.com/Wayyuanyuan/MTCMB"
license: "Apache-2.0 (GitHub repo, LICENSE.txt); CC-BY-4.0 (Zenodo data archive)"
availability: open-download
access_link: "https://github.com/Wayyuanyuan/MTCMB"
accessed: true
access_method: [github, huggingface]
access_date: 2026-10-07
access_notes: "git clone --depth 1 of the GitHub repo (commit faffd81, 2026-06-27) worked without login: all 12 JSONL sub-datasets (7,100 items) with gold answers. HF mirror Bunnybeck/MTCMB (not gated) also downloaded via `uv run hf download` for comparison only: same ids and answers, but no `source` field. Zenodo record not downloaded (README says it holds the same 12 files)."
countries: ["[[China]]"]
regions: ["[[East Asia]]"]
n_records: "7,100 items in 12 sub-datasets"
size: "3.2 MB (data/)"
formats: [jsonl]
join_keys: [herb names (Chinese), formula names (Chinese), TCM syndrome names, TCM disease names]
case_type: [real, vignette, synthetic]
conclusion_type: [diagnosis, syndrome, treatment, prescription, mcq-answer, safety]
languages: [zh]
n_cases: "800 case → conclusion items (200 real EMRs, 100 real case records, 100 dialogue vignettes, 400 textbook vignettes) + 554 vignette MCQs; 7,100 items in total"
diet_relevance: subset
topics: [kg-medical-eval]
questions: [Q4]
relevance: core
found_by: [search/regional-cases]
tags:
  - type/dataset
  - kind/case
  - q/4
  - case/real
  - case/vignette
  - case/synthetic
  - region/east-asia
  - tradmed/tcm
  - access/accessed
  - access/open
---
# MTCMB

> [!abstract] TL;DR
> MTCMB (Kong et al., Sun Yat-sen Univ. + Hunan Univ. of Chinese Medicine, arXiv June 2025) is a Chinese-language
> **Traditional Chinese Medicine** benchmark: 7,100 items in 12 sub-datasets over five dimensions (knowledge QA,
> language understanding, diagnosis, prescription, safety). The core for Q4 is 800 **case → conclusion** items: 200
> real hospital EMRs (CCL25-Eval) → TCM syndrome + disease, or → herb set; 100 published case records → structured
> entities incl. formula and herbs; 400 textbook vignettes → disease/syndrome, or → treatment principle + formula +
> herbs; 100 LLM-written doctor–patient dialogues → structured record. A further 554 exam MCQs are short case vignettes.
> Gold conclusions name **herbs and formulas**, which join to SymMap/HERB (84–93% of herb mentions match). Explicit
> diet content is small: 254 items (3.6%) contain a food/diet keyword, and 60 contain diet advice.

## Access
| | |
|---|---|
| Availability | open-download (GitHub, Apache-2.0; Zenodo, CC-BY-4.0; HF mirror) |
| Link | https://github.com/Wayyuanyuan/MTCMB |
| Accessed? | yes (complete) |
| How | `git clone --depth 1` (commit `faffd81`, 2026-06-27); HF mirror `uv run hf download Bunnybeck/MTCMB --repo-type dataset` only to compare |
| Downloaded | `Data/mtcmb/data/*.jsonl` (12 files, 7,100 rows, 3.2 MB), `dataset_info/*.md` (per-subset docs, Chinese), README, evaluation code (`evaluate/`, `make_answer/`, `mtcmb_datasets.py`); `.git` dropped |

## Tables & columns
All files are JSON Lines, one item per line, every item has `id` (int; MSDD and PR start at 1, the others at 0) and
`source` (provenance string, GitHub version only). Field meanings are from `dataset_info/*.md` and the paper. Gold
answers are in the same file; `mtcmb_datasets.load_records(purpose=benchmark)` blanks them for inference.

### Case → conclusion files
| file (rows) | input field | gold field | meaning | source |
|---|---|---|---|---|
| `TCM-MSDD.jsonl` (100) | `disease_case` (dict) | `answer` = {`证型` syndrome, `疾病` disease}; several labels joined by `\|` | multi-label TCM syndrome (10 classes, e.g. 气虚血瘀证 qi-deficiency blood-stasis) + disease (4 cardiovascular/vertigo classes: 胸痹心痛病, 心衰病, 眩晕病, 心悸病) | real EMRs, CCL25-Eval Task 9 subtask 1 (= [[TCM-TBOSD]]) |
| `TCM-PR.jsonl` (100) | `disease_case` (dict) | `answer` = Python-list string of herb names (5–30 herbs, mean 15.5) | herbal prescription as a set | real EMRs, CCL25-Eval Task 9 subtask 2 |
| `TCM-Diagnosis.jsonl` (200) | `question` = normalised symptom/sign/tongue/pulse list | `answer` = {`疾病名称` disease, `病位证素` location elements, `病性证素` nature elements, `证名` syndrome name} | structured TCM diagnosis | "13th Five-Year Plan" textbooks of internal, external, gynaecological and paediatric TCM (50 cases each) |
| `TCM-FRD.jsonl` (200) | same `question` as TCM-Diagnosis (parallel ids) | `answer` = {`治法` treatment principle, `方剂` formula, `药物组成` herbs without doses} | treatment plan | same textbooks |
| `TCM-CHGD.jsonl` (100) | `dialogue` = doctor–patient consultation written by DeepSeek-R1 from an official case summary | `answer` = free text with fields 中医疾病诊断, 中医证候诊断, 辨病辨证依据 (reasoning), 中医治法, 方剂名称, 药物组成 | structured medical record | licensing practical-skills case bank (国家中医执业（助理）医师资格考试实践技能题库) |
| `TCMeEE.jsonl` (100) | `Medical_case` = classical/modern case record (医案) with its own prescription | `answer` = JSON string with `Symptoms`, `Disease Name`, `TCM Disease Name`, `TCM Pattern`, `Cause and Mechanism of Disease`, `Method of Treatment`, `Formulas`, `Medicinals` | entity extraction (the conclusion is in the text) | 中医智库 zhongyigen.com (95), practitioner submissions (5); reference by DeepSeek-R1, expert-reviewed |

`disease_case` keys (MSDD and PR, all 12 present in every row): `性别` sex, `职业` occupation, `年龄` age, `婚姻` marital
status, `病史陈述者` history given by, `发病节气` **solar term of onset** (24 jieqi; a TCM-specific seasonal feature),
`主诉` chief complaint, `症状` symptoms, `中医望闻切诊` inspection/auscultation/palpation incl. tongue and pulse, `病史`
history (present, past, allergies, personal, marital, menstrual, family), `体格检查` physical exam, `辅助检查` lab/ECG/imaging.

### Exam, knowledge, reading and safety files
| file (rows) | columns | meaning | scoring |
|---|---|---|---|
| `TCM-ED-A.jsonl` (1,200) | `question`, `options` (dict A–E), `answer` (letter) | attending-physician exam MCQs, 100 per discipline × 12 (tuina, paediatrics, ENT, gynaecology, proctology, orthopaedics, internal medicine, dermatology, general practice, surgery, ophthalmology, acupuncture) | accuracy |
| `TCM-ED-B.jsonl` (4,800) | `question`, `options` (list `"A.…"`), `answer` | 8 full mock licensing exams × 600 MCQs | accuracy |
| `TCM-FT.jsonl` (100) | `question`, `points` (bulleted key points, DeepSeek-R1 extracted) | open questions from 《中医学问答题库》 (1988) | BERTScore vs `points` |
| `TCM-LitData.jsonl` (100) | `text` (passage), `annotations` (list of {`Q`, `A`} span answers) | reading comprehension of classical/modern texts (Tianchi dataset 86895) | BLEU + ROUGE |
| `TCM-SE-A.jsonl` (50) | `question` (cloze), `answer` (pharmacopoeia term) | herb toxicity, dose, incompatibility (配伍禁忌), pregnancy contraindications; DeepSeek-R1 written from the 2020 Chinese Pharmacopoeia | GLM-4-Air judge |
| `TCM-SE-B.jsonl` (50) | `question`, `options` (one string "A. … B. …"), `answer` | same safety records as MCQs | accuracy |

Sample: `Data/mtcmb/sample.csv` (TCM-ED-B) + `sample_data_*.csv` per file · full profile: `Data/mtcmb/schema.md`

## Countries & cultures covered
[[China]] only; mainland TCM as taught for the national licensing exams and practised in (unnamed) Chinese hospitals.
Everything is in Simplified Chinese with TCM terminology (syndrome patterns, tongue/pulse, solar terms, classical
formulas). There is no English version.

## Cases & conclusions
**What a case looks like** (TCM-Diagnosis id 1 = TCM-FRD id 1, textbook vignette; our translation):

> *Input:* "Cough, coarse breathing, hoarse cough, dry larynx, dry and sore throat, sticky yellow sputum that is hard
> to cough up, sweating when coughing, yellow nasal discharge, thirst, headache, aversion to wind, fever, red tongue,
> thin yellow coating, floating, rapid, slippery pulse."
> *Gold (Diagnosis):* disease 咳嗽 cough; location 表、肺 exterior, lung; nature 外风、热 external wind, heat; syndrome
> **风热犯肺 wind-heat invading the lung**.
> *Gold (FRD):* principle 疏风清热，宣肺止咳 "disperse wind, clear heat, diffuse the lung, stop cough"; formula
> **桑菊饮 Sang Ju Yin**; herbs 桑叶、菊花、杏仁、连翘、薄荷、桔梗、芦根、甘草 (mulberry leaf, chrysanthemum, apricot
> kernel, forsythia, mint, platycodon, reed rhizome, licorice).

A real-EMR case (TCM-PR id 1) is much longer: 87-year-old retired woman, "paroxysmal chest tightness and wheezing for
21 years, worse for 2 days", CHD and chronic heart failure, full history, exam, labs, solar term 处暑 → gold = a
30-herb set (玄参, 麦冬, 天花粉, 甘草, …).

**Gold conclusions and scoring.**
| conclusion | sub-datasets | metric |
|---|---|---|
| TCM syndrome + disease | MSDD (multi-label), Diagnosis (structured text) | MSDD: share of gold labels hit, averaged; Diagnosis: mean of BLEU, ROUGE-L, BERTScore |
| treatment principle + formula + herbs | FRD, CHGD (+ diagnosis and reasoning) | mean of BLEU, ROUGE-L, BERTScore |
| herb set | PR | mean of Jaccard, F1 and size agreement (also P/R) |
| MCQ letter | ED-A, ED-B (554 vignette items, see below), SE-B | accuracy |
| safety term | SE-A | GLM-4-Air-250414 judge |

The paper reports that n-gram/BERTScore metrics correlate with expert 1–10 ratings (Pearson r 0.59 CHGD, 0.68
Diagnosis, 0.87 FRD, on 20 items each). Best published scores: diagnosis dimension 50.0 (Qwen3-235B few-shot),
prescription 48.5, versus 91.8 for knowledge QA.

**Case counts.** 800 case → conclusion items: real EMRs 200 (MSDD 100, PR 100), real published case records 100
(TCMeEE), synthetic dialogues built on exam case summaries 100 (CHGD), textbook vignettes 400 (Diagnosis 200, FRD
200; same 200 cases). In addition, 554 exam MCQs open with a patient vignette (regex `患者|患儿|男|女 … N岁`: ED-A 74,
ED-B 480).

**Food, diet, herbs, food–drug (keyword counts, our script, Chinese substrings over all fields except `source`;
"食物…过敏" allergy-history boilerplate removed):**
| keyword set | items | where |
|---|---|---|
| food/diet: 饮食, 食疗, 食物, 膳食, 药膳, 食养, 忌口, 食忌, 宜食, 忌食 | **254 / 7,100 (3.6%)** | ED-B 93, CHGD 71, LitData 34, ED-A 13, MSDD 8, PR 8, Diagnosis 7, FT 7, TCMeEE 7, FRD 6, SE 0 |
| diet advice / dietary therapy: 忌口, 忌食, 食疗, 膳食, 药膳, 食忌, 食养, 宜食, 饮食宜, 饮食禁忌, 饮食调 | 60 | CHGD 47 (all in the LLM-written dialogue, not in the gold record), LitData 11, ED-A 2 |
| food–drug / taking medicine: 服药期间, 服药时忌, 同服, 忌茶, 忌酒, 药食同源, 食物相克, 与食物 | 7 | CHGD dialogues only |
| herbs in the gold conclusion | 500 | PR 100, FRD 200, CHGD 100, TCMeEE 100 (+100 herb-safety items in SE-A/B) |

Most food/diet hits are symptoms (不思饮食 "no appetite") or causes (饮食内伤/饮食内停 "dietary injury/food
retention"). Direct diet questions exist but are few, e.g. ED-A id 97 "胸痹患者应忌食的是" ("what should chest-bi
patients avoid eating?" → C, fatty meat, fat, organ meats) or ED-B id 203 "富含嘌呤的食物是" ("which food is rich in
purines?" → C, organ meats). A wider list (adding 营养, 粥, 生冷, 辛辣, 油腻, 食欲, 食积, …) gives
618 items, but 营养 is mostly the exam phrase 营养良好 "well nourished". **diet_relevance: subset** — diet is marginal,
but herbs are central and many herbs are also foods (medicine–food homology, e.g. 桑叶, 菊花, 薄荷, 甘草 above).

## Linking to the vault's knowledge graph
Measured with our scripts on the local copies (herb strings from the PR/FRD/CHGD/TCMeEE gold answers: 722 distinct
names and 5,325 mentions after dropping notes in brackets; prefix-stripping removes processing words such as 炒, 炙,
麸炒, 盐, 制, 生):
- **Herbs → [[SymMap]]** `SMHB.Chinese_name`/`Alias`: 385 of 722 distinct names, **84% of mentions**; → [[HERB]]
  `Herb_cn_name`/`Herb_alias_name`: 522 names, **93% of mentions**; → [[TM-MC]] `medicinal_material.CHINESE`: 334
  names, 78%. Unmatched are mostly short or old names (熟地, 丹皮, 生地, 麦门冬) and powders/slices (三七粉, 人参片).
- **Herbs → unified DB** `ingredient_alias` (lang `zh`, via `norm_text`): only 93 of 727 raw names, 20% of mentions — the DB's Chinese alias list is
  the bottleneck; adding SymMap/HERB Chinese names as aliases would lift this to the figures above.
- **Formulas → HERB** `HERB_formula_info.Formula_cn_name`: 141 of 191 distinct formula names (after removing 加减);
  149 with [[TM-MC]] `prescription.CHINESE` added. HERB formulas carry `Syndromes_in_Chinese` and `Indications`.
- **Syndromes / TCM diseases → condition table**: 94 of 329 distinct labels (Diagnosis + MSDD) match a Chinese
  `condition_alias` (mostly TCM disease names: 感冒, 咳嗽, 胸痹, 不寐, 胃痛); SymMap `SMSY.Syndrome_name` matches only
  23 of 174 syndrome names exactly (naming differs: 风热犯肺 vs SymMap phrasing). MeSH/ICD would need a TCM→Western map.
- Evaluation idea for the KG: give the model the SymMap/HERB herb→syndrome/symptom links for TCM-FRD/PR and score the
  herb-set overlap (PR metric) with and without KG context.

## Versions
- **GitHub (latest, used here):** commit `faffd81` (2026-06-27), 12 JSONL + `source` field, unified `data/` folder
  (older `data_few_shot/` and `evaluate/standard_answer*/` copies removed; few-shot ids are derived in code).
- **Zenodo** 10.5281/zenodo.20465629 (2026-05-31, CC-BY-4.0): same 12 sub-datasets, files named `1.TCM_ED_A.jsonl` etc.
- **HF `Bunnybeck/MTCMB`** (2025-05-28): same 7,100 items; ids and answers identical for every file we compared
  (ED-A, ED-B, Diagnosis, FRD, PR, MSDD, SE-B), but no `source`.
- Paper v1 (2025-06-02) says "eleven sub-datasets" in one place and twelve elsewhere; the release has 12.

## Caveats
- **Licence:** code Apache-2.0, data CC-BY-4.0 (Zenodo) — redistribution with attribution is allowed. But the exam
  items come from a commercial question bank (才识教育科技标准化题库) and textbooks; the authors' licence may not cover
  third-party copyright.
- **Contamination:** exam banks, Tianchi competition data (MSDD, PR, LitData) and zhongyigen.com cases are on the web.
- **Synthetic parts:** CHGD dialogues, TCMeEE references, TCM-FT key points and both safety sets were generated by
  DeepSeek-R1, then expert-reviewed.
- **Label noise seen:** MSDD id 1 is a foot-gangrene case labelled 心悸病/痰热蕴结证; the README example for ED-A gives
  answer A where the data says D.
- **Duplicates:** 43 of 1,200 ED-A items and 254 of 4,800 ED-B items repeat another item's stem and options
  (e.g. ED-A ids 97 and 912).
- **Size:** the clinical subsets are small (100–200 each); scores on them have wide error bars.
- Diet advice in CHGD sits in the LLM-written input dialogue, not in the gold record, so it cannot be scored.
