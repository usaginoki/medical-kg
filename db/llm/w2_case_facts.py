"""W2: structured facts from a patient case, for linking cases to graph ids (dishes / ingredients / conditions).

The model reads the case and the conclusion and returns demographics, place, symptoms, the conclusion's diagnosis in
English, and the foods / drinks / herbs / supplements the patient takes (with negation). `link()` then maps the
English names to graph ids with the build's resolvers (db/build/resolve_*.py).

  uv run db/llm/w2_run.py run | score | link
"""
from typing import Literal

from pydantic import BaseModel, Field

VERSION = "w2-v1"


class Food(BaseModel):
    name_en: str = Field(description="English name, singular, no quantity (e.g. 'camel milk', 'green tea', 'plov')")
    original: str = Field(description="the words in the case")
    kind: Literal["food", "dish", "drink", "herb", "supplement"]
    negated: bool


class CaseFacts(BaseModel):
    age_years: float | None
    sex: Literal["male", "female", "unknown"]
    country: str | None = Field(description="English country name where the patient lives or comes from")
    region_or_city: str | None
    ethnicity: str | None
    religious_practices: list[str]
    symptoms: list[str] = Field(description="English, short standard terms, at most 10")
    history: list[str] = Field(description="English names of past or current diagnoses stated in the case")
    diagnosis_en: str | None = Field(description="the CONCLUSION's main diagnosis in English (standard term)")
    foods: list[Food]
    drugs: list[str] = Field(description="English generic names of medicines the patient takes")


SYSTEM = """You extract structured facts from a patient case for linking it to a food-and-medicine knowledge graph.
The case may be in English, Russian, Kazakh, Chinese, Arabic or Persian; answer in English.
- age_years, sex: as stated (null / "unknown" if not stated). For a profile or a dish question, the person described.
- country: only if stated or unambiguous from a city/region (Tomsk -> Russia); a dataset's origin alone does not
  count. region_or_city: the most specific place stated. ethnicity: as stated, else null.
- religious_practices: e.g. "Ramadan fasting", "halal diet", "daily prayer"; [] if none.
- symptoms: the presenting complaints and key findings, standard English terms (e.g. "heartburn", "jaundice").
  For a TCM record also include tongue and pulse findings in English ("red tongue", "wiry pulse").
- history: diagnoses the case states the patient has or had (not the answer unless the case states it).
- diagnosis_en: the main diagnosis in the CONCLUSION, as a standard English disease name (ICD title for an ICD code;
  for a TCM syndrome give the TCM disease in English plus the syndrome, e.g. "asthma (heat wheezing syndrome)");
  for a dish question give the condition asked about; null for a pure medication question without a diagnosis.
- foods: every food, dish, drink, herb or supplement the patient eats, drinks or takes, or the dish asked about,
  plus herbs of a prescribed formula; negated = the case says the patient does not take it. Not drugs.
- drugs: medicines (generic English names). Copy nothing that is not in the text."""


def render(row):
    return f"DATASET: {row['source']}\nLANGUAGE: {row['lang']}\n\nCASE:\n{row['case']}\n\nCONCLUSION:\n{row['conclusion']}"
