"""Regression checks for the keyword cue screen (db/cues.py): the false positives and negatives found in the audit
of 2026-10-14, as short texts with the expected flags. Run: uv run db/checks/cues_regress.py"""
import os, sys

import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import cues  # noqa: E402

# (source, lang, text, {column: expected value}); a "-word" in m_<cue> means the word must not be matched
CASES = [
    # negation
    ("MedCaseReasoning", "en", "He denied recent travel, animal exposures or sick contacts.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "She denied cough, dyspnea, chest pain, or recent travel.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "Travel history was negative.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "A man from the Philippines, with no history of TB, presented to a Canadian hospital.",
     {"cue_place": True}),
    ("MedCaseReasoning", "en", "A 33-year-old Brazilian man with no past medical history, employed as airline crew, "
                               "returned from South Africa.", {"cue_strength": "strong"}),
    ("MedCaseReasoning", "en", "A non-Hispanic white woman.", {"m_ethnicity": ["white woman"]}),
    ("MedCaseReasoning", "en", "She denied taking herbal supplements or over-the-counter drugs.",
     {"cue_tradmed": False, "diet": False}),
    ("MedCaseReasoning", "en", "She had been taking an herbal supplement for weight loss.", {"cue_tradmed": True}),
    # medical terms that contain a cue word
    ("MedCaseReasoning", "en", "CSF was negative on India ink and cryptococcal antigen.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "Japanese B encephalitis IgM was negative.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "Middle East respiratory syndrome was suspected.", {"cue_place": False}),
    ("MedCaseReasoning", "en", "FISH confirmed EWSR1 gene rearrangement.", {"diet": False}),
    ("MedCaseReasoning", "en", "He developed TACO after transfusion.", {"cue_food": False}),
    ("MedCaseReasoning", "en", "Treated with diethylcarbamazine.", {"diet": False}),
    ("MedCaseReasoning", "en", "Fasting glucose was 140 mg/dL after fasting for 9 hours.", {"diet": False}),
    ("MedCaseReasoning", "en", "Coffee-ground emesis and tea-colored urine.", {"diet": False}),
    # weak vs strong
    ("MedCaseReasoning", "en", "A 71-year-old Caucasian man presented with fever.", {"cue_strength": "weak"}),
    ("MedCaseReasoning", "en", "A 40-year-old Bedouin woman who drinks raw camel milk.", {"cue_strength": "strong"}),
    ("MedCaseReasoning", "en", "A Middle Eastern man with familial Mediterranean fever.", {"cue_place": True}),
    ("MedCaseReasoning", "en", "Four years earlier in Beijing he had surgery.", {"cue_place": True, "cue_strength": "weak"}),
    ("Rezaei2026", "en", "She has been performing daily prayers and attended a religious festival.",
     {"cue_religion": True}),
    # dish datasets
    ("FAM-Bench", "en", "title: Greek yogurt parfait\ningredients: Greek yogurt; honey", {"cue_food": False}),
    ("FAM-Bench", "en", "title: Cajun shrimp\ningredients: kosher salt; shrimp", {"cue_food": True}),
    ("NGQA", "en", "food: Empanada, beef", {"cue_food": True}),
    # false negatives found in the 2026-10-14 review of rejected cases
    ("MedCaseReasoning", "en", "A 78-year-old Swiss-born woman presented with weight loss.", {"cue_place": True}),
    ("MedCaseReasoning", "en", "He has since been treated with Tripterygium Glycosides 20 mg.", {"cue_tradmed": True}),
    ("MedicationQA", "en", "what does magnesium do to your body", {"diet": True}),
    ("MedCaseReasoning", "en", "Serum magnesium was 1.8 mg/dL and magnesium sulfate was given.", {"diet": False}),
    ("MedCaseReasoning", "en", "Phosphate, magnesium, calcium and potassium were normal.", {"diet": False}),
    ("MedCaseReasoning", "en", "She was taking magnesium and zinc tablets for cramps.", {"diet": True}),
    ("RuMedBench", "ru", "Вес 100 кг, не менее даже во время поста.", {"cue_religion": True}),
    ("RuMedBench", "ru", "введение прикорма ( кабачок брокколи) 3 недели назад", {"diet": True}),
    ("RuMedBench", "ru", "Повторный прием: отказался от сладкого.", {"diet": True}),
    ("RuMedBench", "ru", "Холекальциферол 10 000 МЕ в нед, Хелатное железо.", {"diet": True}),
    # Russian
    ("RuMedBench", "ru", "Образование в молочной железе справа.", {"diet": False}),
    ("RuMedBench", "ru", "ЭГДС: кандидоз пищевода.", {"diet": False}),
    ("RuMedBench", "ru", "Выезд за пределы *РЕГИОН* и *СТРАНА* и контакт с инфекционными больными отрицает.",
     {"cue_place": False}),
    ("RuMedBench", "ru", "Выезд за границу отр.", {"cue_place": False}),
    ("RuMedBench", "ru", "Месяц назад вернулся из Таиланда, ел сырую рыбу.", {"cue_place": True, "cue_food": True}),
    ("RuMedBench", "ru", "Пловец, тренируется ежедневно.", {"cue_food": False}),
    ("RuMedBench", "ru", "Ест отварными овощами.", {"cue_tradmed": False}),
    ("RuMedBench", "ru", "Пьёт отвар шиповника.", {"cue_tradmed": True}),
    # Kazakh
    ("ISSAI Dietary Recommendation profiles", "kk", "Дәрігерге қажет болды, бір рет келді.", {"diet": False}),
    ("ISSAI Dietary Recommendation profiles", "kk", "Ет пен сүт ішеді, қымыз ұнатады.",
     {"diet": True, "cue_habit": True}),
    # Chinese
    ("MTCMB", "zh", "个人史，生于原籍，久居本地，否认食物过敏史，舌红苔黄，脉弦。", {"cue_place": False, "cue_tradmed": False,
                                                              "diet": False}),
    ("MTCMB", "zh", "小便黄如浓茶似的。发病节气：立春。", {"diet": False, "cue_habit": False}),
    ("MTCMB", "zh", "之前吃中药能好些，平素嗜食辛辣。", {"cue_tradmed": True, "cue_habit": True}),
    ("MTCMB", "zh", "该病发生于秋季。", {"cue_place": False}),
    # Arabic clitics
    ("MedArabiQ", "ar", "هل يوجد علاج بالأعشاب للطعام الحار؟", {"cue_tradmed": True, "diet": True}),
    ("MedArabiQ", "ar", "ألم مستمر في البطن", {"cue_food": False, "diet": False}),
]


def main():
    df = pd.DataFrame([{"source": s, "lang": lang, "case": t} for s, lang, t, _ in CASES])
    out = cues.tag(df, keep_matches=True)
    bad = 0
    for i, (s, lang, text, want) in enumerate(CASES):
        r = out.iloc[i]
        for col, exp in want.items():
            got = r[col]
            if isinstance(exp, list):
                ok = list(got) == exp
            else:
                ok = got == exp
            if not ok:
                bad += 1
                print(f"FAIL [{lang}] {text[:70]!r}: {col} = {got!r}, expected {exp!r}  (hits: {r.cue_hits!r}; "
                      f"negated: {r.cues_negated!r})")
    print(f"{len(CASES) - bad if bad < len(CASES) else 0}/{len(CASES)} texts checked, {bad} failed checks")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
