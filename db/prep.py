"""Turn downloaded raw files into the derived CSVs that db/build.py reads (PDF tables, Markdown, scrapes).

Usage:
  uv run db/prep.py                 # every step
  uv run db/prep.py maff sfct       # selected steps
  uv run db/prep.py --list

Run after db/fetch.py. Each step rewrites its outputs; the committed Data/<slug>/sample_*.csv files show the expected
format of each output and are the reference for checking it.
"""
import argparse, csv, os, re, subprocess, sys, traceback

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402

STEPS = {}


def step(fn):
    STEPS[fn.__name__] = fn
    return fn


def d(*parts):
    p = os.path.join(DATA, *parts)
    os.makedirs(p, exist_ok=True)
    return p


def write(df, path):
    df.to_csv(path, index=False, quoting=csv.QUOTE_MINIMAL)
    print(f"  wrote {os.path.relpath(path, DATA)}: {len(df):,} rows")


# ---- Japan MAFF "Our Regional Cuisines": Markdown pages → one row per dish ----------------------------------------

MAFF_SECTIONS = {
    "jpn": {"主な伝承地域": "lore_area", "主な使用食材": "main_ingredients", "歴史・由来・関連行事": "history_origin",
            "食習の機会や時季": "occasion_season", "飲食方法": "how_eaten", "保存・継承の取組": "preservation_efforts",
            "レシピ提供元": "recipe_provider", "材料": "ingredients_with_amounts", "作り方": "steps"},
    "eng": {"Main Lore Areas": "lore_area", "Main Ingredients Used": "main_ingredients",
            "History, Origin, and Related Events": "history_origin",
            "Opportunities and Times of Eating Habits": "occasion_season", "How to Eat": "how_eaten",
            "Efforts for Preservation and Succession": "preservation_efforts", "Provider Information": "recipe_provider",
            "Ingredients": "ingredients_with_amounts", "Recipe": "steps"},
}
MAFF_HEADER = {"jpn": [("郷土料理名", "dish_name"), ("都道府県", "prefecture")],
               "eng": [("Cuisine Name", "dish_name"), ("Region", "region_field")]}


def parse_maff_page(text, lang):
    row = {}
    for label, col in MAFF_HEADER[lang]:
        m = re.search(rf"^\*\*{re.escape(label)}\*\*:\s*(.*)$", text, re.M)
        row[col] = m.group(1).strip() if m else None
    row["servings"] = None
    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        head, _, body = block.partition("\n")
        m = re.match(r"^(.*?)\s*[（(](.*)[)）]\s*$", head.strip())
        title, paren = (m.group(1), m.group(2)) if m else (head.strip(), None)
        col = MAFF_SECTIONS[lang].get(title)
        if not col:
            continue
        row[col] = body.strip()
        if col == "ingredients_with_amounts" and paren:
            row["servings"] = paren
    return row


@step
def maff():
    base = d("our-regional-cuisines-japan-maff")
    for lang in ["jpn", "eng"]:
        raw = pd.read_csv(f"{base}/our_regional_cuisines_{lang}.csv")
        rows = [{"row_id": i, **parse_maff_page(t, lang)} for i, t in enumerate(raw.text)]
        cols = ["row_id", "dish_name", *[c for _, c in MAFF_HEADER[lang][1:]], "lore_area", "main_ingredients",
                "history_origin", "occasion_season", "how_eaten", "preservation_efforts", "recipe_provider",
                "ingredients_with_amounts", "servings", "steps"]
        write(pd.DataFrame(rows)[cols], f"{base}/parsed_{lang}.csv")


# ---- PDF helpers --------------------------------------------------------------------------------------------------

def pdf_text(pdf, page, layout=True):
    import subprocess
    args = ["pdftotext", "-f", str(page), "-l", str(page)] + (["-layout"] if layout else []) + [pdf, "-"]
    return subprocess.run(args, capture_output=True, text=True, check=True).stdout


def pdf_words(pdf):
    """{page: [(xMin, yMin, xMax, yMax, text)]} from `pdftotext -bbox`."""
    import html, subprocess
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"], capture_output=True, text=True, check=True).stdout
    pages, cur = {}, None
    for line in out.splitlines():
        if line.lstrip().startswith("<page"):
            cur = len(pages) + 1
            pages[cur] = []
        m = re.search(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*)</word>', line)
        if m and cur:
            pages[cur].append((*map(float, m.groups()[:4]), html.unescape(m.group(5))))
    return pages


def group_lines(words, tol=3.0):
    """Words → lines (top to bottom), each a list of words sorted left to right."""
    lines = []
    for w in sorted(words, key=lambda w: (w[1], w[0])):
        if lines and abs(lines[-1][0][1] - w[1]) <= tol:
            lines[-1].append(w)
        else:
            lines.append([w])
    return [sorted(l, key=lambda w: w[0]) for l in lines]


# ---- Saudi Food Composition Tables (SFDA 2025): recipe page + nutrient page per dish -------------------------------

SFCT_REGIONS = [(12, "Riyadh"), (34, "Makkah"), (80, "Al-Madinah"), (110, "Eastern"), (128, "Al-Qassim"),
                (144, "Aseer"), (160, "Hail"), (172, "Tabuk"), (196, "Al-Baha"), (226, "Northern Borders"),
                (240, "Al-Jawf"), (268, "Jazan"), (286, "Najran")]  # book's table of contents: first page per region
QTY_RE = re.compile(r"^(\d|½|¼|¾|\(optional\)|to taste|as needed|pinch)", re.I)


def sfct_ingredients(words):
    """Parse the ingredient blocks (one or two columns, each with 'Quantity' headers) of a recipe page."""
    top = next(w[3] for w in words if w[4] == "Approximately")
    bottom = next((w[1] for w in words if w[4] == "Preparation" and w[1] > top), 1e9)
    area = [w for w in words if top < w[1] < bottom]
    qheads = sorted([w for w in area if w[4] == "Quantity"], key=lambda w: w[0])
    if not qheads:
        return []
    # column split: right of the left-most Quantity header, if any header sits clearly further right
    split = next((qheads[0][2] + 5 for q in qheads if q[0] > qheads[0][2] + 40), None)
    cols = [[w for w in area if split is None or w[0] < split]] + ([[w for w in area if w[0] >= split]] if split else [])
    out = []
    for cw in cols:
        if not cw:
            continue
        qx = min(q[0] for q in qheads if (split is None or (q[0] < split) == (cw[0][0] < split)))
        lines = [[w for w in l if w[4] != "Quantity"] for l in group_lines(cw)]
        lines = [l for l in lines if l]
        has_qty = lambda l: any(w[0] >= qx - 30 for w in l)
        text = lambda l: " ".join(w[4] for w in l)
        # headings end with "Ingredients"; a heading can wrap onto the line above it (around the Quantity label)
        head = {i for i, l in enumerate(lines) if text(l).endswith("Ingredients")}
        for i in sorted(head):
            if i > 0 and i - 1 not in head and not has_qty(lines[i - 1]) and lines[i][0][1] - lines[i - 1][0][1] < 25 \
                    and not text(lines[i - 1])[0].islower():
                head.add(i - 1)
        component, pending, last_y = None, [], -1e9
        for i, l in enumerate(lines):
            if i in head:
                pending.append(text(l))
                if text(l).endswith("Ingredients"):
                    component, pending = " ".join(pending), []
                continue
            name = " ".join(w[4] for w in l if w[0] < qx - 30).strip()
            qty = " ".join(w[4] for w in l if w[0] >= qx - 30).strip()
            close = l[0][1] - last_y < 20
            last_y = l[0][1]
            if not name and qty and out and close:
                out[-1]["quantity"] = (out[-1]["quantity"] + " " + qty).strip()
            elif name and not qty and out and close and out[-1]["component"] == component and (
                    name[0].islower() or name.startswith("(")):
                out[-1]["ingredient"] += " " + name  # wrapped ingredient name
            elif name and (qty or len(name) > 2):  # drops stray hidden-text fragments such as 'od'
                out.append({"component": component, "ingredient": name, "quantity": qty})
    return out


def sfct_steps(text):
    body = text.split("Preparation Method", 1)[1]
    steps = []
    for ln in body.splitlines():
        ln = ln.strip()
        if not ln or re.fullmatch(r"\d{1,3}", ln) or ln == "Saudi Food Composition Tables":
            continue
        if steps and not re.match(r"^\d+\.", ln) and not ln.endswith(":") and not steps[-1].endswith(":"):
            steps[-1] += " " + ln  # wrapped line
        else:
            steps.append(ln)
    return " | ".join(steps)


@step
def sfct():
    base = d("saudi-food-composition-tables")
    out = d("saudi-food-composition-tables", "extracted")
    pdf = f"{base}/SFCT-E.pdf"
    ref = pd.read_csv(f"{base}/sample_extracted_sfct_per100g_wide_csv.csv", nrows=0).columns[4:]
    analytes = [re.match(r"^(.*) \[(.*)\]$", c).groups() for c in ref]  # 49 (name, unit) in book order
    words = pdf_words(pdf)
    dishes, ings, nutr = [], [], []
    for page in sorted(words):
        if not any(w[4] == "Recipe" for w in words[page]) or "Recipe Name" not in pdf_text(pdf, page, layout=False):
            continue
        text = pdf_text(pdf, page)
        # a long recipe continues on the next page(s); the nutrient table follows it
        npage = page + 1
        while "nutritional content" not in pdf_text(pdf, npage, layout=False):
            text += "\n" + pdf_text(pdf, npage)
            npage += 1
        m = re.search(r"Recipe Name\s*\n\s*(.+?)\s{2,}Approximately\s+(\d+)\s+adults", text)
        if not m:
            print(f"  WARN p{page}: no dish name")
            continue
        did = len(dishes) + 1
        name = m.group(1).strip()
        region = [r for p, r in SFCT_REGIONS if p <= page][-1]
        dishes.append({"dish_id": did, "dish_name": name, "region": region, "serves_adults": int(m.group(2)),
                       "recipe_page": page, "preparation_steps": sfct_steps(text)})
        for r in sfct_ingredients(words[page]):
            ings.append({"dish_id": did, "dish_name": name, **r})
        ntext = pdf_text(pdf, npage)
        flat = re.sub(r"\s+", " ", ntext)
        for a, unit in analytes:
            # some pages letter-space names, one drops a ')', and one prints the unit column shifted by a row:
            # accept any printed unit and keep the analyte's canonical unit
            name_re = r"\s*".join(re.escape(ch) for ch in a.replace(" ", ""))
            if a.endswith(")"):
                name_re = name_re[:-2] + r"\)?"
            mm = re.search(rf"(?<![\w(-]){name_re} (-|[\d.,]+) (-|[\d.,]+) (?:kJ|kcal|g|mg|µg)(?![\w])", flat)
            nutr.append({"dish_id": did, "dish_name": name, "analyte": a, "per_100g": mm.group(1) if mm else None,
                         "full_recipe": mm.group(2) if mm else None, "unit": unit})
    dd, ii, nn = pd.DataFrame(dishes), pd.DataFrame(ings), pd.DataFrame(nutr)
    write(dd, f"{out}/sfct_dishes.csv")
    write(ii[["dish_id", "dish_name", "component", "ingredient", "quantity"]], f"{out}/sfct_ingredients.csv")
    write(nn, f"{out}/sfct_nutrients_long.csv")
    wide = nn.assign(col=nn.analyte + " [" + nn.unit + "]").pivot(index="dish_id", columns="col", values="per_100g")
    wide = dd[["dish_id", "region", "serves_adults", "dish_name"]].merge(wide[list(ref)], on="dish_id")
    write(wide, f"{out}/sfct_per100g_wide.csv")
    print(f"  missing nutrient values: {nn.per_100g.isna().sum()} of {len(nn)}")


# ---- Bahrain Food Composition Tables (MOH 2025): three dish tables (macronutrients, minerals, vitamins) -------------

BFCT_COLS = {
    "macronutrients": ["H2O (ml/100g)", "Energy (kcal/100g)", "CHO (g/100g)", "Fiber (g/100g)", "Sugar (g/100g)",
                       "Protein (g/100g)", "Fat (g/100g)", "SFA (g/100g)", "TFA (g/100g)", "MUFA (g/100g)",
                       "Cholesterol (mg/100g)", "Ash (g/100g)"],
    "minerals": ["Na (mg/100g)", "K (mg/100g)", "Ca (mg/100g)", "P (mg/100g)", "Mg (mg/100g)", "Fe (mg/100g)",
                 "Cu (mg/100g)", "Zn (mg/100g)", "Mn (mg/100g)", "B (mg/100g)", "Cr (mg/100g)", "Al (mg/100g)",
                 "I (mg/100g)", "Se (mcg/100g)", "Mo (mg/100g)"],
    "vitamins": ["Vitamin C ascorbic acid (mg/100g)", "Thiamin (mg/100g)", "Riboflavin (mg/100g)", "Niacin (mg/100g)",
                 "B6 (mg/100g)", "Folate (mcg/100g)", "B12 (mcg/100g)", "Vitamin A retinol (mg/100g as printed)",
                 "Vitamin E (mg/100g)", "Vitamin D (IU)"],
}
BFCT_SOURCE = {1: "Direct chemical analysis (MOH Bahrain)", 2: "FCT Kuwait", 3: "FCT Lebanon", 4: "FCT Oman",
               5: "FCT Jordan", 6: "FCT Pakistan", 7: "FCT UAE"}
ARABIC = re.compile(r"[؀-ۿ][؀-ۿ\s()]*[؀-ۿ)]")
VALUE = re.compile(r"<\s*[\d.]+|\bND\b|\bT\b|\d+(?:\.\d+)?")


def bfct_table(text):
    if "Cholesterol" in text and "Energy" in text:
        return "macronutrients"
    if "mcg/100" in text and re.search(r"\bMo\b", text):
        return "minerals"
    if "Thiamin" in text:
        return "vitamins"
    return None


@step
def bfct():
    base = d("bahrain-food-composition-tables")
    out = d("bahrain-food-composition-tables", "extracted")
    pdf = f"{base}/FCT-book-final-2025_ar.pdf"
    rows = {t: [] for t in BFCT_COLS}
    categories, table = {}, None
    for page in range(20, 52):
        text = pdf_text(pdf, page).replace("\u202b", "").replace("\u202c", "")
        table = bfct_table(text) or table
        if not table or not ARABIC.search(text):
            continue
        for r in bfct_page(text, len(BFCT_COLS[table]), categories if table == "macronutrients" else {}):
            rows[table].append({**{k: v for k, v in r.items() if isinstance(k, str)}, "table": table,
                                **{BFCT_COLS[table][k]: v for k, v in r.items() if isinstance(k, int)}})
    cat_name = {k: bfct_category(v) for k, v in categories.items()}
    from difflib import SequenceMatcher
    for table in ["minerals", "vitamins"]:  # same dishes in the same order as the macronutrient table
        if len(rows[table]) != len(rows["macronutrients"]):
            raise ValueError(f"{table}: {len(rows[table])} items vs {len(rows['macronutrients'])} macronutrients")
        for r, m in zip(rows[table], rows["macronutrients"]):
            sim = SequenceMatcher(None, r["english_name"].replace(" ", ""), m["english_name"].replace(" ", "")).ratio()
            if sim < 0.6:
                print(f"  WARN {table} {r['code']} '{r['english_name']}' aligned to {m['code']} '{m['english_name']}'")
            r["code"] = m["code"]
    macro = pd.DataFrame(rows["macronutrients"]).drop_duplicates("code").set_index("code")  # book prints 7.1 twice
    for table, rs in rows.items():
        df = pd.DataFrame(rs)
        # the three tables mark sources inconsistently (e.g. Chapati *****, ***, ********): use the macronutrient one
        df["source_stars"] = df.code.map(macro.source_stars).fillna(df.source_stars).astype(int)
        df["source"] = df.source_stars.map(lambda n: BFCT_SOURCE.get(n, f"{n} stars"))
        df["category"] = df.code.str.split(".").str[0].map(cat_name)
        cols = ["table", "category", "code", "english_name", "arabic_name", "source_stars", "source",
                *BFCT_COLS[table]]
        if table != "macronutrients":
            cols.remove("source_stars")
        write(df[cols], f"{out}/bfct_dishes_{table}.csv")


def bfct_values(line, ncol):
    """(values, code, rest) if the line ends with ncol value tokens (optionally preceded by the item code)."""
    toks = re.findall(r"<\s*[\d.]+|\S+", ARABIC.sub(" ", line))
    run = 0
    while run < len(toks) and re.fullmatch(r"<\s*[\d.]+|ND|T|\d+(?:\.\d+)?g?", toks[len(toks) - 1 - run]):
        run += 1
    if run < ncol:
        return None
    head, vals = toks[:len(toks) - ncol], toks[len(toks) - ncol:]
    return [re.sub(r"(?<=\d)g$", "", v.replace(" ", "")) for v in vals], head


def bfct_page(text, ncol, categories):
    """One page of a dish table. Names (English and Arabic) wrap above and below their value line, with no blank line
    between items; the value line itself may hold only the code and the values."""
    lines = text.splitlines()
    start = next((i + 1 for i, l in enumerate(lines) if "/100" in l), 0)  # after the units header line
    stop = next((i for i, l in enumerate(lines) if l.strip().startswith("*Direct")), len(lines))
    vals, other, bars = [], [], []
    for i in range(start, stop):
        l = lines[i]
        if bfct_values(l, ncol):
            vals.append(i)
        elif re.match(r"^\s*\d+\s*$", l) and i + 1 < stop and re.match(r"^\s*[A-Z][A-Z_ \-&,]+$", lines[i + 1]):
            categories[l.strip()] = lines[i + 1].strip()  # '1' on its own line, name on the next
            bars += [i, i + 1]
        elif (m := re.match(r"^\s*(\d+)\s+([A-Z][A-Z_ \-&,]+)$", l)):
            categories[m.group(1)] = m.group(2).strip()
            bars.append(i)
        elif l.strip() and i not in bars:
            other.append(i)
    owner = {v: [v] for v in vals}
    for i in other:
        cands = [v for v in vals if not any(min(i, v) < b < max(i, v) for b in bars)]
        if not cands:
            continue
        best = min(abs(i - v) for v in cands)
        near = sorted(v for v in cands if abs(i - v) == best)
        if len(near) > 1:  # tie: a name ends with its source asterisks; a code starts an item
            near = [near[0]] if lines[i].rstrip().endswith("*") and not re.match(r"^\s*\d+\.\d+", lines[i]) \
                else [near[-1]]
        owner[near[0]].append(i)
    out = []
    for v in vals:
        values, head = bfct_values(lines[v], ncol)
        code, en, ar = None, [], []
        for i in sorted(owner[v]):
            words = head if i == v else ARABIC.sub(" ", lines[i]).split()
            for w in words:
                if code is None and re.fullmatch(r"\d+\.\d+\.?|\d+", w):
                    code = w.rstrip(".")
            en += [w for w in words if not re.fullmatch(r"\d+\.\d+\.?|\d+", w)]
            ar += [a.group(0).strip() for a in ARABIC.finditer(lines[i])]
        name = " ".join(en)
        stars = name.count("*")
        name = re.sub(r"\(\s*\)|\)\s*\(|(?<![A-Z(])\)|\((?![A-Z)])", " ", name.replace("*", ""))  # stray parens
        out.append({"table": None, "code": code, "english_name": re.sub(r"\s+", " ", name).strip(),
                    "arabic_name": " ".join(ar), "source_stars": stars, **dict(enumerate(values))})
    return out


def bfct_category(raw):
    t = raw.strip().lower().replace("_", "-")
    t = re.sub(r"^(ce[a-z]*al)", "cereal", t)
    t = re.sub(r"\s*-\s*", "-", t).replace("dished", "dishes").replace("milked", "milk")
    return t[0].upper() + t[1:]


# ---- Kyrgyzstan Food Composition Table (2022): 11 cooked dishes (3 nutrient tables) + their recipes ---------------

KFCT_TABLES = {  # PDF pages → (table, INFOODS columns in printed order)
    "proximates": ((67, 68), ["ENERC", "ENERC_2", "WATER", "PROT", "FAT", "CHOT", "CHO", "GLUS", "FRU", "SUCS",
                              "FIBT"]),
    "minerals": ((69, 70), ["CA", "FE", "MG", "P", "K", "ZN", "CU", "NA", "ASH", "OA"]),
    "vitamins": ((71, 72), ["VITA", "CAROT", "VITE", "THIA", "RIBF", "FOL", "VITC"]),
}
CYR = re.compile(r"[Ѐ-ӿ]")
NUM = re.compile(r"^\(?-?\d+(?:[.,]\d+)?\)?$")


def kfct_dishes(pdf, pages, cols):
    rows, cur = [], None
    for page in pages:
        for ln in pdf_text(pdf, page).splitlines():
            toks = ln.split()
            if len(toks) >= 2 and toks[0] == "13" and re.fullmatch(r"13\d{3}", toks[1]):
                vals = [t for t in toks[2:] if NUM.match(t)]
                names = [t for t in toks[2:] if not NUM.match(t)]
                cur = {"page": page, "food_group_code": 13, "food_code": toks[1],
                       "name_kyrgyz": [t for t in names if CYR.search(t)],
                       "name_english": [t for t in names if not CYR.search(t)], "vals": vals}
                rows.append(cur)
            elif cur and toks and not any(NUM.match(t) for t in toks) and len(toks) <= 4:
                cur["name_kyrgyz"] += [t for t in toks if CYR.search(t)]  # wrapped names
                cur["name_english"] += [t for t in toks if not CYR.search(t)]
            elif not toks:
                continue
            else:
                cur = None
    out = []
    for r in rows:
        if "ASH" in cols and len(r["vals"]) == len(cols) - 1:
            r["vals"].insert(cols.index("ASH"), "")  # 13005-13011 print no ash value (blank column)
        if len(r["vals"]) != len(cols):
            print(f"  WARN {r['food_code']}: {len(r['vals'])} values for {len(cols)} columns: {r['vals']}")
        out.append({"page": r["page"], "food_group_code": r["food_group_code"], "food_code": r["food_code"],
                    "name_kyrgyz": " ".join(r["name_kyrgyz"]), "name_english": " ".join(r["name_english"]),
                    **dict(zip(cols, r["vals"]))})
    return pd.DataFrame(out)


def kfct_recipes(pdf):
    text = "\n".join(pdf_text(pdf, p) for p in range(15, 28))
    rows = []
    for block in re.split(r"Recipe №\s*", text)[1:]:
        lines = [l for l in block.splitlines()]
        no = int(re.match(r"\d+", lines[0].strip()).group())
        head = lines[:next(i for i, l in enumerate(lines) if l.strip().startswith("Method"))]
        words = " ".join(head).split()[1:]  # drop the recipe number
        name = " ".join(w for w in words if not CYR.search(w))  # English name; the Kyrgyz one is Cyrillic
        start = next(i for i, l in enumerate(lines) if l.strip().startswith("List of ingredients"))
        prev = None
        for l in lines[start + 1:]:
            s = l.strip()
            if not s or re.fullmatch(r"\d{1,3}", s) or s.startswith("(only edible") or s.startswith("Recipes for") \
                    or s.startswith("Traditional"):
                continue
            m = re.match(r"^(.*?)\s{2,}([\d.]+)(?:\s+([\d.]+))?\s*$", s)
            if m:
                ing, a, b = m.group(1).strip(), m.group(2), m.group(3)
                raw, edible = (a, b) if b else (None, a)
                prev = {"recipe_no": no, "food_code": f"{13000 + no}", "dish_name": name, "ingredient": ing,
                        "raw_weight_g": raw, "edible_weight_g": edible}
                rows.append(prev)
            elif prev is not None and not NUM.match(s):
                prev["ingredient"] += " " + s  # wrapped name ('Mass of coo' / 'ked noodles')
    return pd.DataFrame(rows)


@step
def kfct():
    base = d("kyrgyzstan-food-composition-table")
    out = d("kyrgyzstan-food-composition-table", "extracted")
    pdf = f"{base}/Kyrgyzstan_FCT_06072022.pdf"
    for name, (pages, cols) in KFCT_TABLES.items():
        write(kfct_dishes(pdf, pages, cols), f"{out}/dishes_{name}.csv")
    write(kfct_recipes(pdf), f"{out}/dish_recipes_ingredients.csv")


# ---- small scraped files whose committed sample is the complete file (row counts checked against schema.md) -------

COMPLETE_SAMPLES = {  # target (relative to Data/) ← committed sample; full row count in the source's schema.md
    "drugbank/public_drug_cards.csv": ("drugbank/sample_public_drug_cards_csv.csv", 12),
    "unaprod/unaprod_monographs_sample.csv": ("unaprod/sample_unaprod_monographs_sample_csv.csv", 38),
    "knapsack-family/jamu_herb_effect_examples.csv": ("knapsack-family/sample_jamu_herb_effect_examples_csv.csv", 2),
    "spicerx/spices.csv": ("spicerx/sample_spices_csv.csv", 29),
    "flavordb2/entities.csv": ("flavordb2/sample_entities_csv.csv", 48),
    "herb/scrape/clinical_herb.csv": ("herb/sample_scrape_clinical_herb_csv.csv", 46),
    "symmap/scrape/herb_syndrome_relations.csv": ("symmap/sample_scrape_herb_syndrome_relations_csv.csv", 45),
}


@step
def samples():
    for target, (src, n) in COMPLETE_SAMPLES.items():
        df = pd.read_csv(os.path.join(DATA, src), dtype=str, keep_default_na=False)
        if len(df) != n:
            raise ValueError(f"{src}: {len(df)} rows, expected the complete {n}")
        os.makedirs(os.path.dirname(os.path.join(DATA, target)), exist_ok=True)
        write(df, os.path.join(DATA, target))


@step
def drugbank():
    """DrugBank food interactions as redistributed by DDID (DrugBank's own downloads need an account)."""
    ddid = pd.read_csv(os.path.join(DATA, "ddid", "interaction_information.csv"), dtype=str, keep_default_na=False,
                       encoding="utf-8-sig")
    x = ddid[ddid.Relationship_classification == "Drugbank"].copy()
    x["drugbank_id"] = x.Reference.str.extract(r"(DB\d{5})", expand=False)
    cols = ["drugbank_id", "Drug_Name", "Food_Herb_Name", "Type", "Component", "Result", "Effect", "Conclusion",
            "Reference"]
    write(x[cols], f"{d('drugbank')}/food_interactions_via_ddid.csv")


# ---- polite scrapes (1 request/s, raw responses cached under Data/<slug>/raw/) -------------------------------------

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
_last = [0.0]


def fetch(slug, key, url, data=None, headers=None, session=None, pause=1.0):
    """GET (or POST with `data`) url, cached as Data/<slug>/raw/<key>; returns text."""
    import time, urllib.request, urllib.parse
    path = os.path.join(d(slug, "raw"), key)
    if os.path.exists(path):
        return open(path, encoding="utf-8").read()
    wait = pause - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    for attempt in range(3):
        try:
            if session is not None:
                r = session.post(url, data=data, headers=headers, timeout=90) if data is not None else \
                    session.get(url, headers=headers, timeout=90)
                r.raise_for_status()
                text = r.text
            else:
                body = urllib.parse.urlencode(data).encode() if isinstance(data, dict) else data
                req = urllib.request.Request(url, data=body, headers={"User-Agent": UA, **(headers or {})})
                text = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace")
            break
        except Exception as e:
            if attempt == 2:
                raise
            print(f"  retry {key}: {e}")
            time.sleep(5 * (attempt + 1))
    _last[0] = time.time()
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    return text


@step
def flavordb2():
    """Molecules of the 48 FlavorDB2 ingredients in entities.csv (no bulk download; undocumented JSON endpoint)."""
    import json
    base = d("flavordb2")
    ents = pd.read_csv(f"{base}/entities.csv", dtype=str)
    pairs, mols = [], {}
    for eid in ents.entity_id:
        j = json.loads(fetch("flavordb2", f"entity_{eid}.json",
                             f"https://cosylab.iiitd.edu.in/flavordb2/entities_json?id={eid}"))
        for m in j.get("molecules", []):
            pairs.append({"entity_id": eid, "pubchem_id": m["pubchem_id"]})
            mols.setdefault(m["pubchem_id"], m)
    cols = pd.read_csv(f"{base}/sample_molecules_csv.csv", nrows=0).columns
    write(pd.DataFrame(pairs), f"{base}/entity_molecules.csv")
    write(pd.DataFrame(list(mols.values())).reindex(columns=cols), f"{base}/molecules.csv")


@step
def spicerx():
    """Page 1 (top-10 diseases with all PMIDs) of each of the 29 spices in spices.csv."""
    import html as H
    base = d("spicerx")
    spices = pd.read_csv(f"{base}/spices.csv", dtype=str)
    assoc, refs = [], []
    dis_re = re.compile(r'<td><a[^>]*href="/spicerx/get_disease\?page=1&id=(MESH:\w+)">([^<]+)</a></td>\s*<td>\s*'
                        r'<strong style="color: green">(\d+)</strong>,\s*<strong style="color: red">(\d+)</strong>')
    # reference rows sit in the collapsed block after their disease row; negative rows have no disease link
    ref_re = re.compile(r'<tr style="background-color: #(\w+);">\s*<td><a[^>]*pubmed/(\d+)">\d+</a></td>\s*'
                        r'<td>(?:<a[^>]*>)?[^<]*(?:</a>)?</td>\s*<td[^>]*title="([^"]*)">.*?</td>\s*'
                        r'<td[^>]*title="([^"]*)">.*?</td>\s*<td>(\d*)</td>', re.S)
    for r in spices.itertuples():
        page = fetch("spicerx", f"plant_{r.tax_id}.html",
                     f"https://cosylab.iiitd.edu.in/spicerx/search_plants?page=1&id={r.tax_id}")
        hits = list(dis_re.finditer(page))
        for k, m in enumerate(hits):
            mesh, dis, pos, neg = m.groups()
            dis = H.unescape(dis.strip())
            assoc.append({"tax_id": r.tax_id, "spice": r.common_name, "mesh_id": mesh, "disease": dis,
                          "n_positive": int(pos), "n_negative": int(neg)})
            block = page[m.end():hits[k + 1].start() if k + 1 < len(hits) else len(page)]
            block = block.split("Linked Ph")[0]  # the phytochemical tables follow the last disease
            for color, pmid, title, journal, year in ref_re.findall(block):
                refs.append({"tax_id": r.tax_id, "spice": r.common_name, "mesh_id": mesh, "disease": dis, "pmid": pmid,
                             "polarity": "positive" if color.lower() == "bfffbf" else "negative",
                             "title": H.unescape(title), "journal": H.unescape(journal), "year": year})
    write(pd.DataFrame(assoc), f"{base}/spice_disease_associations.csv")
    write(pd.DataFrame(refs), f"{base}/spice_disease_references.csv")


@step
def unaprod():
    """Full monograph index (3,413 rows) from the site's DataTables backend (POST /databasetable, CSRF token)."""
    import json, requests
    base = d("unaprod")
    s = requests.Session()
    s.headers["User-Agent"] = UA
    tok = re.search(r'csrf-token" content="([^"]+)"', s.get("https://unaprod.com/database", timeout=60).text).group(1)
    rows, start, total = [], 0, None
    while True:
        form = {"draw": 1, "start": start, "length": 1000, "search": "", "order[0][column]": 0, "order[0][dir]": "asc",
                **{f"columns[{i}][data]": i for i in range(6)}}
        j = json.loads(fetch("unaprod", f"databasetable_{start}.json", "https://unaprod.com/databasetable", data=form,
                             headers={"X-CSRF-TOKEN": tok, "X-Requested-With": "XMLHttpRequest"}, session=s))
        rows += j["data"]
        total = total if start else j["recordsTotal"]  # later pages report recordsTotal minus the offset
        start += 1000
        if start >= total:
            break
    clean = lambda v: "; ".join(x.strip() for x in re.split(r"<br\s*/?>", v or "") if x.strip()) or None
    df = pd.DataFrame([{"ID": r[0], "DrugName": r[1], "Pronunciation": r[2], "Origin": r[3], "Status": clean(r[4]),
                        "MizajType": clean(r[5])} for r in rows])
    write(df, f"{base}/unaprod_drug_list.csv")


@step
def knapsack():
    """KNApSAcK World pages of the 36 countries in the committed world_country_counts sample, and the Jamu formula
    search for "Jamu Batuk" (the only search term recorded; the other 7 original searches were not documented)."""
    import html as H
    base = d("knapsack-family")
    countries = pd.read_csv(f"{base}/sample_world_country_counts_csv.csv", dtype=str)
    cell = lambda x: " | ".join(p.strip() for p in re.split(r"<br\s*/?>", H.unescape(re.sub(r"<a[^>]*>.*?</a>", "", x)))
                                if re.sub(r"<[^>]+>", "", p).strip()) if x else None
    strip = lambda x: re.sub(r"<[^>]+>", "", x or "").strip() or None
    rows, counts = [], []
    for c in countries.itertuples():
        page = fetch("knapsack-family", f"world_{c.country_code}.html",
                     f"https://www.knapsackfamily.com/KNApSAcK_World/search.php?cn={c.country_code}&wd=&flg=")
        n = 0
        for tr in re.findall(r"<tr><td class=rs1>(.*?)</td></tr>", page, re.S):
            td = re.split(r"</td>\s*<td class=rs1>", tr)
            if len(td) != 9:
                continue
            f = [strip(cell(x)) if i else strip(re.sub(r"<a[^>]*>.*?</a>", "", td[0])) for i, x in enumerate(td)]
            rows.append({"country_code": c.country_code, "country": c.country, "species": f[0], "upper_class": f[1],
                         "family": f[2], "common_name": f[3], "purpose": f[4], "upper_class_ja": f[5],
                         "family_ja": f[6], "common_name_ja": f[7], "reference": f[8]})
            n += 1
        m = re.search(r"matched data : (\d+) / Number of edible data : (\d+) / Number of medicinal data : (\d+)", page)
        counts.append({"country_code": c.country_code, "country": c.country, "matched": m and int(m.group(1)),
                       "edible": m and int(m.group(2)), "medicinal": m and int(m.group(3)), "rows_parsed": n})
    write(pd.DataFrame(rows), f"{base}/world_country_species.csv")
    write(pd.DataFrame(counts), f"{base}/world_country_counts.csv")

    jamu = []
    for term in ["Jamu Batuk"]:
        page = fetch("knapsack-family", f"jamu_{term.replace(' ', '_')}.html",
                     "https://www.knapsackfamily.com/jamu/haigou.php", data={"hword": term})
        for t in re.findall(r'<table class="res">(.*?)</table>', page, re.S):
            head = {k: strip(v) for k, v in re.findall(r'<th class="res">([^<]+)</th><td colspan="7">(.*?)</td>', t)}
            for tr in re.findall(r'<tr><td class="wb170">(.*?)</tr>', t, re.S):
                td = re.split(r"</td>\s*<td[^>]*>", tr)
                sid = re.search(r"sid=(S\d+)", tr)
                jamu.append({"company": head.get("Company or Reference"), "jamu_name": head.get("Jamu Name"),
                             "jamu_effect": head.get("Jamu Effect"), "jamu_effect_group": head.get("Jamu Effect Group"),
                             "herb_name": strip(td[0]), "herb_name_indonesia": strip(td[1]),
                             "herb_name_en_cn": strip(td[2]), "scientific_name": strip(re.sub(r"<a.*?</a>", "", td[3])),
                             "plant_part": strip(td[4]), "herb_effect_sid": sid and sid.group(1),
                             "percent": strip(td[6])})
    write(pd.DataFrame(jamu), f"{base}/jamu_formula_herbs.csv")


SYMMAP_HERBS = {  # the 8 herbs of the original scrape (Datasets/SymMap.md), labels as in the committed samples
    "SMHB00367": "Shengjiang (fresh ginger)", "SMHB00136": "Ganjiang (dried ginger)", "SMHB00090": "Dazao (jujube)",
    "SMHB00143": "Gouqizi (goji)", "SMHB00340": "Rougui (cassia bark)", "SMHB00198": "Jianghuang (turmeric)",
    "SMHB00515": "Shanzha (hawthorn)", "SMHB00359": "Shanyao (yam)"}
SYMMAP_TABLES = {"TCM_symptom": "tcm_symptom", "MM_symptom": "mm_symptom", "Syndrome": "syndrome", "Mol": "ingredient",
                 "Gene": "target", "Disease": "disease"}


@step
def symmap():
    """Relations of the 8 documented herbs (POST /related_components/). Afterwards, run the committed
    db/build/links_symmap_scrape.py, which appends 6 more herbs for 4 of the tables."""
    import json
    base = d("symmap", "scrape")
    for table, name in SYMMAP_TABLES.items():
        cols = list(pd.read_csv(f"{DATA}/symmap/sample_scrape_herb_{name}_relations_csv.csv", nrows=0).columns)
        rows = []
        for herb, label in SYMMAP_HERBS.items():
            j = json.loads(fetch("symmap", f"{herb}_{table}.json", "http://www.symmap.org/related_components/",
                                 data={"rrid": herb, "table_name": table, "filter": 0}))
            for r in j.get("data") or []:
                rows.append({"source_herb_id": herb, "source_herb": label,
                             **{k: ("" if v is None else v) for k, v in r.items()}})
        write(pd.DataFrame(rows).reindex(columns=cols), f"{base}/herb_{name}_relations.csv")


HERB_HERBS = ["HERB001164", "HERB001787", "HERB001915", "HERB002840", "HERB004694", "HERB005017"]  # the 6 herbs of
# the original scrape (their detail pages are the committed Data/herb/sample_scrape_herb_detail_<id>_json.csv files)


@step
def herb():
    """Herb → ingredient links from the HERB 2.0 detail API for the 6 documented herbs."""
    import json
    base = d("herb", "scrape")
    rows = []
    for hid in HERB_HERBS:
        j = json.loads(fetch("herb", f"herb_detail_{hid}.json", "http://47.92.70.12/chedi/api/",
                             data=json.dumps({"func_name": "detail_api", "key_id": hid, "label": "Herb"}).encode(),
                             headers={"Content-Type": "application/json"}))
        pinyin = j["summary"][1][1]
        head, *body = j["herb_ingredient"]
        for r in body:
            vals = [x["title"] if isinstance(x, dict) else ("" if x in (None, "NA") else x) for x in r]
            rows.append({"source_herb_id": hid, "source_herb": pinyin, **dict(zip(head, vals))})
    write(pd.DataFrame(rows), f"{base}/herb_ingredient.csv")


NPASS_COMPOUNDS = ["crocin", "piperine", "thymoquinone", "glycyrrhizin", "quercetin", "allicin", "cinnamaldehyde",
                   "cuminaldehyde", "capsaicin", "eugenol", "thymol", "carvacrol", "apigenin", "rosmarinic acid",
                   "bisdemethoxycurcumin", "limonene", "anethole"]  # the 17 compounds listed in Datasets/NPASS.md


def demojibake(t):
    """The NPASS pages double-encode UTF-8 ('Â±' for '±'); undo it where that round-trips."""
    try:
        return t.encode("latin-1").decode("utf-8") if "Â" in t or "Ã" in t else t
    except UnicodeError:
        return t


@step
def npass():
    """'NP Quantity Composition' table (web only) of the 17 documented compounds; ids from the downloaded generalinfo."""
    base = d("npass")
    g = pd.read_csv(f"{base}/NPASS3.0_naturalproducts_generalinfo.txt", sep="\t", dtype=str, quoting=3,
                    on_bad_lines="skip")
    rows = []
    for name in NPASS_COMPOUNDS:
        hit = g[g.pref_name.str.lower() == name]
        if len(hit) != 1:
            raise ValueError(f"{name}: {len(hit)} NPASS ids")
        npc, pref = hit.np_id.iloc[0], hit.pref_name.iloc[0]
        page = fetch("npass", f"compound_{npc}.html", f"https://bidd.group/NPASS/compound.php?compoundID={npc}")
        table = page[page.find('<table id="NPQuantity"'):]
        table = table[:table.find("</table>")]
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", table.split("<tbody>", 1)[-1], re.S):
            td = [demojibake(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", c)).strip())
                  for c in re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)]
            if len(td) == 9:
                rows.append({"np_id": npc, "pref_name": pref, "org_id": td[0], "org_name": td[1],
                             "material_preparation": td[2], "org_part": td[3], "quantity_standard": td[4],
                             "quantity_min": td[5], "quantity_max": td[6], "quantity_unit": td[7],
                             "reference": td[8]})
    write(pd.DataFrame(rows), f"{base}/scraped_np_quantity_sample.csv")


@step
def issai():
    """ISSAI dietary profiles: 5 zips of prompt + profile + GPT-4 answer texts -> derived/*.csv (db/prep_issai.py)."""
    subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "prep_issai.py"),
                    d("issai-dietary-recommendation")], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("steps", nargs="*")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        print("\n".join(STEPS))
        return
    bad = [s for s in a.steps if s not in STEPS]
    if bad:
        sys.exit(f"unknown steps: {bad}; see --list")
    failed = []
    for name in a.steps or STEPS:
        print(f"[{name}]", flush=True)
        try:
            STEPS[name]()
        except Exception as e:
            traceback.print_exc()
            failed.append(f"{name}: {e}")
    print("\nFAILED:\n  " + "\n  ".join(failed) if failed else "\nall done")


if __name__ == "__main__":
    main()
