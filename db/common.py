"""Shared helpers for the unified database build (db/build.py and db/build/*.py)."""
import os, re, unicodedata

import duckdb

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(VAULT, "Data")
DB_DIR = os.path.join(VAULT, "db")
# Each developer/agent can point at its own file to avoid DuckDB's single-writer lock.
DB_PATH = os.environ.get("UNIFIED_DB", os.path.join(DB_DIR, "unified.duckdb"))

EVIDENCE = [  # code, rank (1 = strongest), label
    ("clinical", 1, "clinical trial or meta-analysis"),
    ("curated_literature", 2, "curated from the literature / measured"),
    ("epidemiological", 3, "cohort or biomarker association"),
    ("traditional", 4, "traditional-medicine claim"),
    ("text_mined", 5, "text-mined from abstracts"),
    ("predicted", 6, "computationally predicted / inferred"),
]


def connect(path=None, read_only=False):
    return duckdb.connect(path or DB_PATH, read_only=read_only)


def init_schema(con):
    con.execute(open(os.path.join(DB_DIR, "schema.sql")).read())
    con.execute("INSERT OR REPLACE INTO evidence_type SELECT * FROM (VALUES "
                + ",".join(f"('{c}',{r},'{l}')" for c, r, l in EVIDENCE) + ")")


def add_source(con, source_id, dataset_note, name, version=None, license=None, access_date="2026-09-30"):
    con.execute("INSERT OR REPLACE INTO source VALUES (?,?,?,?,?,?)",
                [source_id, dataset_note, name, version, license, access_date])


def data(*parts):
    """Absolute path inside Data/."""
    return os.path.join(DATA, *parts)


def slug(text):
    """ASCII-ish lowercase slug for ids: 'Black cumin (seed)' -> 'black-cumin-seed'. Keeps CJK characters."""
    t = unicodedata.normalize("NFKC", str(text)).lower().strip()
    t = re.sub(r"[^\w]+", "-", t, flags=re.UNICODE)
    return t.strip("-_")


_QTY = re.compile(r"^[\d\s/.,½¼¾⅓⅔-]+(?:\s*(?:g|kg|mg|ml|l|cups?|tbsps?|tsps?|tablespoons?|teaspoons?|oz|lbs?|pounds?|"
                  r"pieces?|pcs|cloves?|pinch|handful|cans?|packets?)\b\.?)?\s*", re.I)
_PAREN = re.compile(r"\([^)]*\)|\[[^\]]*\]")
_DESCRIPTORS = re.compile(
    r"\b(fresh|freshly|dried|dry|ground|chopped|finely|coarsely|minced|sliced|diced|grated|crushed|whole|large|small|"
    r"medium|peeled|boiled|roasted|toasted|raw|cooked|optional|to taste|as needed|or more|about|approx\.?)\b", re.I)


def norm_text(text):
    """Normalise an ingredient/condition string for dictionary matching.

    NFKC, lowercase, drop parentheses, leading quantities/units, cooking descriptors and punctuation, crude
    singularisation of the last word. CJK text is only NFKC-normalised and stripped of digits/units.
    """
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", str(text)).strip().lower()
    if re.search(r"[぀-ヿ一-鿿가-힯]", t):  # Chinese / Japanese / Korean
        t = _PAREN.sub("", t)
        t = re.sub(r"[\d.,/]+\s*(g|kg|ml|克|千克|毫升|个|片|根|勺|大さじ|小さじ|本|枚|適量|少々|适量|少许)?", "", t)
        t = re.sub(r"适量|少许|適量|少々|お好みで|少量", "", t)  # amount words without a number
        return re.sub(r"[\s:：、,，。・]+", "", t)
    t = _PAREN.sub(" ", t)
    t = t.split(",")[0]  # "onion, chopped" -> "onion"
    t = _QTY.sub("", t)
    t = _DESCRIPTORS.sub(" ", t)
    t = re.sub(r"[^a-z\s'-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    words = t.split()
    if words:
        w = words[-1]
        if w.endswith("ies") and len(w) > 4:
            w = w[:-3] + "y"
        elif w.endswith(("oes", "ches", "shes")):
            w = w[:-2]
        elif w.endswith("s") and not w.endswith(("ss", "us")) and len(w) > 3:
            w = w[:-1]
        words[-1] = w
    return " ".join(words)
