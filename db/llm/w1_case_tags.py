"""W1: cultural tagging of a patient case (after the keyword screen in db/cues.py).

The model reads the case, the dataset's conclusion and the keyword hits, and returns which cultural cues are really
there (with negation and who they are about), whether culture matters for the conclusion, and whether food / diet /
herb knowledge could help. The definitions in SYSTEM are also the labelling guide for the reference set.
"""
from typing import Literal

from pydantic import BaseModel, Field

VERSION = "w1-v1"

CueType = Literal["place", "ethnicity", "religion", "habit", "food", "tradmed"]


class Cue(BaseModel):
    type: CueType
    text: str = Field(description="the words in the case, copied exactly (short)")
    negated: bool = Field(description="the case says it is absent / denied")
    about: Literal["patient", "family", "other", "name_of_test_or_disease", "template_field"]


class CaseTags(BaseModel):
    cues: list[Cue]
    culture_role: Literal["none", "incidental", "supportive", "decisive"]
    diet_relevant: bool
    graph_answerable: bool
    answer_leak: bool


SYSTEM = """You tag patient cases for an evaluation of a culturally aware medical assistant. Each item has a CASE
(what the model under test sees), the dataset's CONCLUSION (gold answer) and KEYWORD HITS from a cheap regex screen
(may be wrong or incomplete). The case may be in English, Russian, Kazakh, Chinese, Arabic or Persian.

Return JSON:
cues: every cultural cue stated in the CASE (not the conclusion). Types:
  place      country, city, region, nationality, migration, travel or residence abroad / in an endemic area
  ethnicity  race or ethnic group
  religion   religion or religious practice (fasting, halal, prayer, pilgrimage, festivals)
  habit      culture-linked substance or habit (betel, khat, hookah, naswar, kumys, taste preferences like 嗜食辛辣)
  food       food, drink or dish tied to a cuisine or local practice (raw camel milk, kimchi, fermented fish, plov);
             in a dish dataset, the dish's cuisine
  tradmed    traditional / folk / herbal medicine the patient used or asks about (herbal remedy, TCM decoction,
             cupping, Ayurveda)
  For each: text = the exact words, negated = the case says it is absent/denied ("denied recent travel", "否认…"),
  about = patient | family | other | name_of_test_or_disease (India ink, Japanese encephalitis, Mediterranean
  fever as a disease name) | template_field (fixed form lines such as "久居本地", "Выезд за пределы … отрицает").
  Generic foods (rice, milk, fruit), generic diet words and ordinary Western drugs are NOT cues.
culture_role: does a cultural cue matter for reaching the CONCLUSION?
  decisive    the conclusion depends on a cue; without it a clinician would likely miss or change it (raw camel
              milk -> brucellosis; travel to an endemic area -> malaria; Ramadan fasting -> hypoglycaemia; betel ->
              oral cancer; Ashkenazi -> Gaucher disease; herbal remedy -> hepatotoxicity)
  supportive  a cue raises or lowers the likelihood of the conclusion or shapes the advice, but the conclusion is
              reachable without it; also cases whose whole framework is a traditional medicine system (TCM syndrome /
              formula, Persian temperament) where the conclusion is in that system's terms
  incidental  cues are present but do not bear on the conclusion ("a 71-year-old Japanese man" with appendicitis)
  none        no non-negated cue about the patient
diet_relevant: the patient's own food, drink, diet, supplement or herb intake is described (not negated) and is
  plausibly part of the problem or the advice; or the case is a dish / diet question.
graph_answerable: knowledge of foods, ingredients, their chemical compounds, herbs or food-drug interactions
  could plausibly help reach or improve the CONCLUSION (diet advice, a food- or herb-caused condition, a TCM formula
  of herbs, nutrient deficiency). False when the conclusion is a diagnosis that food knowledge cannot inform.
answer_leak: the CASE already states the conclusion (the diagnosis name, ICD code or formula) so the item is
  trivial.
Be strict and literal; do not invent cues."""


def render(row):
    """The user message for one case row (columns of db/export/cases.parquet)."""
    hits = row.get("cue_hits") or "none"
    neg = row.get("cues_negated") or "none"
    return (f"DATASET: {row['source']} ({row['origin']})\nLANGUAGE: {row['lang']}\n"
            f"KEYWORD HITS: {hits}\nKEYWORD HITS JUDGED NEGATED: {neg}\n\nCASE:\n{row['case']}\n\n"
            f"CONCLUSION:\n{row['conclusion']}")


# Few-shot examples (synthetic, so they do not overlap the reference set)
SHOTS = [
    ({"source": "MedCaseReasoning", "origin": "published case report", "lang": "en", "cue_hits": "ethnicity: Caucasian",
      "cues_negated": "place: recent travel",
      "case": "A 71-year-old Caucasian man presented with right lower quadrant pain and fever. He denied recent "
              "travel. CT showed an inflamed appendix.", "conclusion": "Acute appendicitis"},
     CaseTags(cues=[Cue(type="ethnicity", text="Caucasian", negated=False, about="patient"),
                    Cue(type="place", text="recent travel", negated=True, about="patient")],
              culture_role="incidental", diet_relevant=False, graph_answerable=False, answer_leak=True)),
    ({"source": "MedCaseReasoning", "origin": "published case report", "lang": "en", "cue_hits": "ethnicity: Bedouin",
      "cues_negated": "", "case": "A 34-year-old Bedouin shepherd from southern Israel had 3 weeks of fever, night "
      "sweats and knee pain. He regularly drinks unpasteurized camel milk from his herd.",
      "conclusion": "Brucellosis"},
     CaseTags(cues=[Cue(type="ethnicity", text="Bedouin", negated=False, about="patient"),
                    Cue(type="place", text="southern Israel", negated=False, about="patient"),
                    Cue(type="food", text="unpasteurized camel milk", negated=False, about="patient")],
              culture_role="decisive", diet_relevant=True, graph_answerable=True, answer_leak=False)),
    ({"source": "RuMedBench", "origin": "outpatient visit, Tomsk", "lang": "ru", "cue_hits": "",
      "cues_negated": "place: Выезд за пределы",
      "case": "Жалобы: изжога после еды, особенно после жирной и острой пищи. Анамнез: Выезд за пределы *РЕГИОН* и "
              "*СТРАНА* и контакт с инфекционными больными отрицает.", "conclusion": "ICD-10: K21 (Gastro-oesophageal reflux disease)"},
     CaseTags(cues=[Cue(type="place", text="Выезд за пределы *РЕГИОН* и *СТРАНА*", negated=True, about="template_field")],
              culture_role="none", diet_relevant=True, graph_answerable=True, answer_leak=False)),
]


def few_shot_system():
    import json
    parts = [SYSTEM, "\nExamples:"]
    for row, out in SHOTS:
        parts.append(f"\n--- INPUT ---\n{render(row)}\n--- OUTPUT ---\n{json.dumps(out.model_dump(), ensure_ascii=False)}")
    return "\n".join(parts)
