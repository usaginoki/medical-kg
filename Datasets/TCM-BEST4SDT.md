---
title: "TCM-BEST4SDT"
slug: tcm-best4sdt
kind: [case]
version: "figshare v8 (2026-02-09) = GitHub DYJG-research/TCM-BEST4SDT @ 60407f2 (2026-05-28); data files identical"
previous_versions: "figshare v1–v7 (v1 cited in the paper, Dec 2025); `TCM_SDT.json` is the 300-case file without the 5 later `外治法` lines"
papers: ["[[Li2025 - TCM-BEST4SDT syndrome differentiation benchmark]]"]
url: "https://doi.org/10.6084/m9.figshare.30615956"
license: "CC BY 4.0 (figshare record: data + evaluation scripts); GitHub mirror LICENSE: Apache-2.0"
availability: open-download
access_link: "https://api.figshare.com/v2/articles/30615956"
accessed: true
access_method: [figshare, api]
access_date: 2026-10-07
access_notes: "Listed the 25 files of figshare article 30615956 (version 8, 2026-02-09) with the public figshare API and downloaded all of them from ndownloader.figshare.com without login; every file matched its figshare MD5. The 5 data JSONs are byte-identical to the GitHub mirror (DYJG-research/TCM-BEST4SDT, last push 2026-05-28; Basic_Knowledge.json differs only in file-name case and whitespace). Evaluation code (*.py, requirements.txt, config_example.json) zipped to code.zip and figures moved to images/ so the profiler only sees data. The FangZheng-RM reward model (ModelScope) and the Qwen3-32B judge were not downloaded, so scores cannot be reproduced offline."
countries: ["[[China]]"]
regions: ["[[East Asia]]"]
n_records: "600 items: 300 SDT cases + 100 TCM basic-knowledge MCQs + 100 medical-ethics MCQs + 100 LLM content-safety MCQs"
size: "3.9 MB on disk (data JSON 2.2 MB)"
formats: [json]
join_keys: [herb names (Chinese), TCM syndrome names, TCM disease names]
case_type: [real, vignette]
conclusion_type: [syndrome, diagnosis, treatment, prescription, advice, mcq-answer]
languages: [zh]
n_cases: "300 syndrome-differentiation-and-treatment cases (150 rewritten classical case records, 50 dated modern clinical records, 100 short modern vignettes; split inferred from the text), each with a 19-field gold answer scored on 14 dimensions"
diet_relevance: central
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
  - region/east-asia
  - tradmed/tcm
  - access/accessed
  - access/open
---
# TCM-BEST4SDT

> [!abstract] TL;DR
> TCM-BEST4SDT (Li, Guo et al., China Academy of Chinese Medical Sciences + Beijing Wenge Technology, arXiv Dec 2025)
> is a Chinese **Traditional Chinese Medicine** benchmark of 600 items. Its core for Q4 is **300 patient cases → a
> full "syndrome differentiation and treatment" (辨证论治) answer**:
> - syndrome, nature and location of disease, and treatment principle as 10-option (4 for nature) choice questions;
> - free-text cause, pathogenesis, a **dosed herbal prescription**, decoction method, modifications and **precautions**.
>
> Cases come from Xiyuan Hospital clinical records (ethics approval 2025XLA135-2) and classical case records. Experts
> annotated them in three stages. Scoring mixes option accuracy, a Qwen3-32B judge and a prescription–syndrome reward
> model (FangZheng-RM). Three tasks without cases (basic knowledge, ethics, content safety; 100 MCQs each) complete the 600.
>
> Diet is unusually prominent:
> - the gold **Precautions** field gives diet advice in **262 / 300 cases** (mostly TCM food taboos while taking the medicine);
> - 74 case texts mention diet keywords;
> - every gold answer is a herb prescription, and 279 contain at least one medicine–food-homology item (licorice, Chinese yam, poria, jujube…).
>
> Gold herbs join [[SymMap]] (83% of mentions) and [[HERB]] (91%).

## Access
| | |
|---|---|
| Availability | open-download (figshare, CC BY 4.0; GitHub mirror, Apache-2.0) |
| Link | https://doi.org/10.6084/m9.figshare.30615956 · API https://api.figshare.com/v2/articles/30615956 · https://github.com/DYJG-research/TCM-BEST4SDT |
| Accessed? | true (complete) |
| How | figshare API file list → `curl` from ndownloader (25 files, MD5 verified); GitHub raw files only to compare |
| Downloaded | `Data/tcm-best4sdt/`: 5 data JSONs (2.2 MB), `README.md` / `README_zh.md`, `prompt_templates_bilingual.md` (all judge, reward and answer prompts in Chinese + English), `images/` (result figures), `code.zip` (evaluation scripts, not run) |

## Tables & columns
Field meanings come from the README, the paper (Table 1) and the evaluation code (`data_loader.py`, `tcm_benchmark.py`, read but not run). All text is Simplified Chinese.

### `TCM-BEST4SDT.json` (600 rows): the complete benchmark
Two record shapes in one list. ids 1–100 basic knowledge, 101–200 medical ethics, **201–500 SDT cases**, 501–600 content safety.

**MCQ rows (300)**
| column | type | meaning | example |
|---|---|---|---|
| `id` | int | item id | `1` |
| `exam_type` | str | exam family: 医师考试 physician licensing, 药师考试 pharmacist, 医学考研 postgraduate entrance, 专业知识考试 professional knowledge, 护理考试 nursing, 安全测试 safety test | `医师考试` |
| `exam_class` | str | exam level, e.g. 执业助理医师 assistant physician, 主管中药师 senior TCM pharmacist | `执业助理医师` |
| `exam_subject` | str | exam or subject (45 values), e.g. 中医执业助理医师, 伤寒论 *Shanghan lun* | `中医执业助理医师` |
| `class` | str | task: 中医基础知识 TCM basic knowledge · 医学伦理 medical ethics · 安全问题 content safety | `中医基础知识` |
| `question` | str | stem | `九味羌活汤的功用是` "the action of Jiuwei Qianghuo decoction is" |
| `option` | dict A–E | answer options (profile: `option.A`…`option.E`) | `{"C": "发汗祛湿，兼清里热", …}` |
| `answer` | str | gold letter(s) | `C`, `ABDE` |
| `question_type` | str | 单项选择题 single choice (286) · 多项选择题 multiple choice (14) | |

**SDT case rows (300)**
| column | type | meaning |
|---|---|---|
| `id` | int | 201–500 |
| `instruction` | str | **the case**: patient description given to the model. Median 116 characters (52–1,560). |
| `output` | list of 19 (5 cases: 20) `"label：value"` strings | **the gold answer**, see below |
| `中医疾病诊断` | str | TCM disease name, e.g. 不寐 insomnia (15), 胁痛 hypochondriac pain (8), 痢疾 dysentery (5); 213 distinct. Not scored by the code. |
| `外治法` | str | external therapy (poultice with the herb dregs); only ids 452, 457, 461 |

**The 19 `output` fields** (label → meaning → how it is scored):
| label | meaning | scored by |
|---|---|---|
| `证型` / `证型答案` / `证型选项` | syndrome(s), gold letters, 10 options A–J | multi-select. 214 cases have 1 syndrome, 71 have 2, 15 have 3–4. 296 distinct strings (paper: 257 syndromes). |
| `病性` / `病性答案` / `病性选项` | nature of disease (实热证 excess heat, 本虚标实 root deficiency + branch excess…), 4 options | single choice in 298 cases |
| `病位` / `病位答案` / `病位选项` | location (organs: 肝 liver 102, 脾 spleen 92, 肾 kidney 78, 胃 stomach 71…), 10 options | multi-select, 1–4 answers |
| `治则治法` / `治则治法答案` / `治则治法选项` | treatment principles and methods, 10 options | multi-select, mostly 2 answers |
| `病因` | causative factors (free text) | Qwen3-32B judge vs gold |
| `病机` | pathogenesis (free text) | judge vs gold |
| `药物组成及用量` | **herbal prescription with doses** (mean 9.5 herbs) | not compared directly: FangZheng-RM scores how well the *model's* prescription fits the syndrome (0–100) |
| `方剂配伍规律` | rationale of the herb combination | not used as reference; the judge compares the model's text with a reference generated by the reward model |
| `随症加减` | modifications for accompanying symptoms | judge vs gold |
| `煎服方法` | decoction and administration (vessel, order, water, timing vs meals) | judge vs gold |
| `注意事项` | **precautions**: paper: "diet contraindications, potential side effects, activities to avoid, special warnings" | judge vs gold |
| `外治法` | external therapy (5 cases) | not scored |

The 14 outcome dimensions (paper Table 1) are the 4 choice dimensions, cause, pathogenesis, herbal composition and dosage, herb-combination principles, incompatibility (十八反/十九畏), pregnancy contraindications, safety of medicinal materials, preparation and administration, modification, and precautions. Two process dimensions (CoT completeness, CoT accuracy) are added for models that show their reasoning.

### `TCM_SDT.json` (300 rows), `Basic_knowledge.json`, `Medical_Ethics.json`, `LLM_Content_Safety.json` (100 rows each)
The per-task files of the paper's *Data Records*: same columns as above. `TCM_SDT.json` numbers the cases 1–300 and lacks the `外治法` line in 5 cases (ids 166, 203, 208, 210, 272 = 366, 403, 408, 410, 472). In `Basic_knowledge.json`, id 28 has no answer and id 90 no option E; the combined file is complete.
- Basic knowledge: classics, theory, materia medica and formulas, tongue/pulse diagnosis. 89 single + 11 multiple choice from licensing, postgraduate and herbal-pharmacist exams.
- Ethics: 97 + 3 MCQs from exam banks plus expert-written scenarios.
- Safety: 100 expert-written provocations. The gold is usually the refusal option ("我不能回答这个问题"). Topics include insults, crime and political questions such as Taiwan.

Sample: `Data/tcm-best4sdt/sample.csv` (first 50 rows of the combined file = basic-knowledge MCQs) + `sample_TCM_SDT_json.csv` (cases) · full profile: `Data/tcm-best4sdt/schema.md`

## Countries & cultures covered
[[China]] only: mainland TCM in Simplified Chinese.
- **Case sources** (paper): Xiyuan Hospital of the China Academy of Chinese Medical Sciences, Beijing, plus "classical case records". The paper gives no split.
- **Blocks visible in the text (our inference):**
  - ids **201–350 (150)**: classical case records retold in modern Chinese. ids 301–350 are first-person ("我今年四十五岁…湖北督署秘书").
    - Doses, herbs and wording point to Zhang Xichun's *Yixue Zhongzhong Canxi Lu* (Republican era): 生怀山药, 生杭芍, 生赭石, 野台参.
  - ids **351–400 (50)**: modern dated clinical records, 2006–2023, with labs and imaging.
    - 21 of them give the solar term of onset (发病节气).
    - Some name the clinic, e.g. Beijing Hospital of TCM, Prof. Liu Zhilong's clinic.
  - ids **401–500 (100)**: short modern vignettes with occupation and lifestyle ("programmer, stays up late", "likes fried chicken and chips"). Mostly without tongue/pulse data. They may be condensed clinical cases or expert-written; the paper does not say.
- Diseases span 20 ICD-11 chapters (paper Fig. 3b). Syndromes are grouped by the eight principles (Fig. 3a).

## Cases & conclusions
**One real case** (id 352, modern clinical record; our translation):
> *Input:* "Wang, male, 35, office worker, first visit 17 May 2021.
> - Chief complaint: obesity for more than 10 years; weight has risen steadily since he started work, never treated.
> - Now: heavy, uncomfortable body, fatigue, dream-disturbed sleep, epigastric upset with acid regurgitation.
>   **Habitually eats rich, fatty, sweet food** (嗜食肥甘厚味). Yellow urine; loose stool once a day.
> - Exam: height 182 cm, weight 122 kg, 'BMI 8 kg·m⁻²' [sic]. Red, swollen tongue with tooth marks, thick yellow
>   greasy coating; slippery pulse.
> - Labs: ALT 50 U/L, GGT 91 U/L, uric acid 587 μmol/L; glucose, blood pressure and creatinine normal."
>
> *Gold:*
> - **Syndrome:** B + G = 湿热内蕴证 damp-heat accumulating inside + 痰湿内阻证 phlegm-damp obstructing inside.
> - **Nature:** B, mainly excess. **Location:** liver, stomach, spleen.
> - **Principles:** clear heat and drain dampness; strengthen the spleen and transform phlegm; disperse accumulation.
> - **Cause:** "irregular diet damaging spleen and stomach; craving rich food generating turbid dampness".
> - **Prescription:** processed pinellia 10 g, tangerine peel 10 g, poria 20 g, Lycopus 10 g, patchouli 15 g, raw coix
>   seed 20 g, **corn silk 20 g**, smilax 15 g, Dioscorea hypoglauca 15 g, **lotus leaf 20 g**, coptis 6 g, **licorice 6 g**.
> - **Decoction:** taken on an empty stomach with ginger–jujube tea.
> - **Precautions:** "strictly control the diet, cut daily energy by 30–40%, avoid rich fatty food; ≥5 aerobic sessions a
>   week; … **during medication avoid 'fa wu' (发物) such as mutton and goose**".
> - **TCM disease:** 肥胖病 obesity.

**Scoring** (README, paper, code):
- **Choice questions** (syndrome, nature, location, principles) are asked 3 times with shuffled options.
  - Single choice counts only if all 3 runs are correct.
  - Multi-select score is S = |A∩B| / (|A| + |Ā∩B|), where A = gold set and B = selected set, averaged over the 3 runs.
- **Judge:** Qwen3-32B with expert-written prompts gives 0–100 for cause, pathogenesis, decoction, precautions and modifications against the gold text.
- **Reward model:** FangZheng-RM (Qwen3-14B fine-tuned on 10k expert-rated syndrome × 6-prescription samples) scores prescription–syndrome fit. It also generates the references for the four herb-safety dimensions.
- **Totals:** SDT score = mean of the dimension means. Overall = SDT 40% + basic knowledge 30% + ethics 15% + safety 15%.
- **Results** (README v8 Table 1, total / SDT): Gemini 3 Pro 0.871 / 0.834 · GPT-5.2 0.787 / **0.842** · Kimi-K2 0.832 / 0.837 · Qwen3-32B 0.814 / 0.824 · DeepSeek-R1 0.814 / 0.788 · ShizhenGPT-32B (TCM) 0.783 / 0.798 · Zhongjing-13B (TCM) 0.421 / 0.522.

**Food, diet, herbs, food–drug.** Keyword counts by our script (Chinese substrings, 300 SDT cases):
| keyword set / pattern | cases | where |
|---|---|---|
| 饮食 食疗 食物 膳食 药膳 忌口 宜食 忌食 in the **case input** | **74** | 饮食 51, 食物 26 |
| same keywords anywhere in the **gold** | **267** | 注意事项 254, 煎服方法 42, 病因 38. Per keyword: 忌食 188, 饮食 123, 食物 58 |
| input **or** gold | 277 | |
| **diet advice in gold Precautions** (忌食/宜食/清淡/忌辛辣·生冷·油腻/少食/戒酒…) | **262** | by block: classical 134/150, clinical 47/50, vignettes 90/100 |
| **food taboo while taking the medicine** (服药期间…忌/避免 + food) | **81** | mostly "avoid spicy, greasy, raw-cold food during medication" |
| taboo on 发物 / seafood / mutton | 28 | |
| alcohol in Precautions | 19 | |
| dosing relative to meals (饭前/饭后/空腹) in Decoction | 88 | 饭后 after meals 72, 空腹 empty stomach 39 |
| named drink–medicine warnings (浓茶 strong tea, 咖啡 coffee) | 2 | ids 391, 471 |
| dietary habit or trigger in the input (嗜食, 过食, 肥甘, 辛辣, 生冷, 饮酒, 瓜果…) | 72 | e.g. id 203 "ate too much cold melon and fruit" |
| gold cause names a dietary factor (饮食不节, 食积, 肥甘, 酒, 生冷…) | 54 | |
| prescription contains a **medicine–food-homology** item (our list of 78 names from the NHC catalogue incl. 2019/2023 additions) | **279** | 甘草 licorice 182, 山药 Chinese yam 93, 茯苓 poria 83, 当归 angelica 69, 黄芪 astragalus 41, 党参 codonopsis 38, 陈皮 tangerine peel 32 |
| prescription contains a plain food (粳米 rice, 葱白 scallion, 鸡子黄 egg yolk, 蜂蜜 honey, 大枣 jujube, 生姜 ginger, 荷叶 lotus leaf, 玉米须 corn silk, 薏苡仁 coix…) | 151 | |

In the 300 MCQs, 5 items mention diet: 4 basic-knowledge items, e.g. foods that stain the tongue coating; 1 ethics item on nitrite food poisoning.

**diet_relevance: central.**
- Every gold answer is a herb prescription, and 87% carry diet advice in a dimension that is scored.
- The advice is generic TCM food-property taboos: 辛辣 pungent, 油腻 greasy, 生冷 raw/cold, 燥热 dry-hot, 发物 "aggravating foods".
- For the classical cases these precautions are modern expert annotations, not in the source record.
- Food–drug content is TCM-style (avoid tea, alcohol or 发物 with the decoction), not pharmacological interactions.

## Linking to the vault's KG
Measured on the local copies:
- **Herb names.** From `药物组成及用量` we parsed 2,857 mentions and 537 distinct names, then stripped doses and brackets and removed prefixes such as 生, 炒, 炙, 怀, 杭, 潞.
  - **[[SymMap]]** `SMHB.Chinese_name` + aliases: 339 / 537 names, **83% of mentions**.
    - Unmatched are mostly Zhang Xichun's regional names (生杭芍 53, 净萸肉 18, 大甘枸杞 14, 广三七 14, 野台参 11) and short forms (生地, 丹皮, 熟地), plus 粳米 rice and 杏仁 apricot kernel.
  - **[[HERB]]** `Herb_cn_name` / `Herb_alias_name`: 416 names, **91% of mentions**.
  - **Unified DB** `ingredient_alias` (lang zh, via `norm_text`): 77 names = **22% of mentions**, 49 ingredient ids; 265 cases have ≥ 1 linked herb.
  - As for [[MTCMB]], adding SymMap/HERB Chinese names as `ingredient` aliases would lift this to ~85–90%. A map of regional classical names (杭芍 → 白芍, 台参 → 人参/党参, 萸肉 → 山茱萸) is also needed.
- **Syndromes / TCM diseases → `condition`.**
  - 47 of 295 syndrome strings match a Chinese `condition_alias` (mostly SymMap `tcm_syndrome` rows); 42 match SymMap `SMSY.Syndrome_name` directly.
  - 74 of 173 TCM disease names (194 cases) match, e.g. 感冒 → `TCM:SMTS00306`, 痢疾 → `TCM:SMTS00615`, 胁痛 → `TCM:SMTS01316`.
  - Only one label carries a Western name (粉刺 → 痤疮 acne). Linking to MeSH needs the SymMap/HERB TCM → MeSH mappings (`condition_relation` `tcm_maps_to`).
- **Diet advice ↔ our TCM properties.** The taboos are food-property classes (生冷/寒凉 cold, 燥热/辛辣 hot, 油腻/肥甘 rich). `ingredient_property` (system `tcm`, property `nature`, 297 rows) could test whether a model's advice avoids foods whose nature clashes with the syndrome. Example: avoid cold-natured foods in 虚寒 deficiency-cold syndromes.
- **Licorice** is in 182 gold prescriptions. The DB links `ING:licorice` to hypertension (SpiceRx `harmful`) and to drugs such as amlodipine and hydrochlorothiazide ([[DDID]] `Possible`). This would let a KG-augmented model add a Western food–drug warning that the TCM gold lacks.
- **Evaluation idea:** give the model the SymMap/HERB herb → syndrome/symptom links and our `nature` properties, then score with and without KG context:
  - syndrome and principle choices (choice accuracy is deterministic and needs no judge);
  - herb overlap with the gold prescription, our own metric since the official one needs the reward model.

## Versions
- **figshare** 10.6084/m9.figshare.30615956: 8 versions; **v8 (2026-02-09)** used here. The paper (arXiv v1, 2025-12-02) cites v1 and lists 5 JSON files; v8 adds the prompt templates, bilingual READMEs and figures.
- **GitHub** DYJG-research/TCM-BEST4SDT (Apache-2.0, last push 2026-05-28): same 5 data files as figshare v8.
- **Results differ by version.** The paper v1 evaluated GPT-5 and Gemini 2.5 Pro and reported that some TCM models beat general ones. The v8 README re-runs with GPT-5.2 and Gemini 3 Pro and reports that base Qwen2.5 models beat their TCM fine-tunes (32B: 0.808 vs ShizhenGPT 0.783).
- `TCM_SDT.json` vs the combined file: 295 cases identical; 5 cases gain an extra `外治法` line in the combined file.

## Caveats
- **Licence:** CC BY 4.0 (data) and Apache-2.0 (GitHub code) allow redistribution with attribution, so the samples are committed. Exam questions come from Chinese exam banks; whether the authors could relicense them is unclear.
- **Mixed case types:** half the cases are classical records retold in modern Chinese (some first-person) and a third are short vignettes. Only ~50 are full modern clinical records.
- **Gold prescriptions are not used for scoring:** the official score depends on the FangZheng-RM reward model and a Qwen3-32B judge (both need GPU serving). The four herb-safety dimensions are judged against references that the reward model writes.
- **Contamination:** classical cases (e.g. Zhang Xichun) and exam MCQs are widely available online.
- **Label noise seen:** id 352 gives "BMI 8 kg·m⁻²" (should be ~36.8). Syndrome strings mix "…证" and bare forms (气阴两虚 / 气阴两虚证).
- **Small set:** 300 cases over 213 diseases and ~257 syndromes, so most labels occur once.
- The 300 MCQs are not cases; the content-safety set includes political-refusal items that are irrelevant here.
