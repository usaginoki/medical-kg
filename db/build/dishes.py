"""Stage `dishes`: dish + dish_ingredient for the priority regions (Gulf, Central Asia, South Asia, East Asia).

Sources: Saudi FCT, Bahrain FCT (dish list only; no ingredient table), Kyrgyz FCT, INDB, Japan MAFF regional
cuisines, CulinaryDB (priority cuisines), an IndicRecipeNutri subset (sub-national Region, sampled per region),
a XiaChuFang subset (non-empty `dish`), Food.com (priority-region cuisine tags).

dish_ingredient.raw_text → ingredient: 1 xref (CulinaryDB entity id, INDB USDA/UK/IFCT code) → 2 exact alias →
3 normalised alias → 4 fuzzy (rapidfuzz ≥ 90, same language) → 5 manual map (db/maps/ingredient_map_manual.csv,
loaded as aliases with source_id 'manual' and reported as match_method 'manual').

`dish_nutrient` is NOT filled here (it needs the nutrient compounds); `iter_dish_nutrients()` yields
(dish_id, nutrient_key, source_id, amount_per_100g, unit) rows from the Saudi / Bahrain / Kyrgyz / INDB tables
for the stage that does.
"""
import ast
import hashlib
import json
import re
import unicodedata
from collections import Counter, defaultdict

import pandas as pd

from common import data
from build.resolve_ingredients import CJK, IngredientResolver, key_norm

IRN_PER_REGION = 1500          # IndicRecipeNutri: max recipes per sub-national Region
IRN_SKIP_REGIONS = {"Pan-Indian", None}
XCF_N = 5000                    # XiaChuFang recipes
XCF_WESTERN = set("""蛋糕 烘焙 面包 烤箱 饼干 吐司 西式 沙拉 披萨 三明治 西式早餐 曲奇 冰淇淋 布丁 慕斯 甜点 果酱 日式 韩式 马卡龙
司康 布朗尼 泡芙 蛋挞 戚风 芝士 奶油 欧包 贝果 玛芬 可颂 意面 汉堡 咖啡 奶茶 酸奶 巧克力 牛排 焗 奶酪 黄油 甜品 下午茶
婴幼儿 宝宝 辅食 预拌粉 冰棒 雪糕""".split())
XCF_REGION = [("川", "Sichuan"), ("四川", "Sichuan"), ("重庆", "Chongqing"), ("湘", "Hunan"), ("湖南", "Hunan"),
              ("粤", "Guangdong"), ("广式", "Guangdong"), ("广东", "Guangdong"), ("潮汕", "Guangdong (Chaoshan)"),
              ("东北", "Northeast China"), ("新疆", "Xinjiang"), ("陕西", "Shaanxi"), ("西安", "Shaanxi"),
              ("北京", "Beijing"), ("老北京", "Beijing"), ("上海", "Shanghai"), ("本帮", "Shanghai"),
              ("云南", "Yunnan"), ("贵州", "Guizhou"), ("山西", "Shanxi"), ("山东", "Shandong"), ("鲁", "Shandong"),
              ("福建", "Fujian"), ("闽", "Fujian"), ("杭州", "Zhejiang"), ("浙", "Zhejiang"), ("苏式", "Jiangsu"),
              ("淮扬", "Jiangsu"), ("江西", "Jiangxi"), ("湖北", "Hubei"), ("武汉", "Hubei"), ("河南", "Henan"),
              ("台湾", "Taiwan"), ("台式", "Taiwan"), ("港式", "Hong Kong"), ("客家", "Hakka"), ("兰州", "Gansu"),
              ("内蒙", "Inner Mongolia"), ("广西", "Guangxi"), ("桂林", "Guangxi"), ("海南", "Hainan"),
              ("天津", "Tianjin"), ("宁夏", "Ningxia"), ("青海", "Qinghai"), ("西藏", "Tibet"), ("安徽", "Anhui"),
              ("徽", "Anhui")]
# Food.com cuisine tags kept → (ISO2 or None, subregion)
FOODCOM_TAGS = {
    "indian": ("IN", None), "pakistani": ("PK", None), "nepalese": ("NP", None), "middle-eastern": (None, None),
    "lebanese": ("LB", None), "turkish": ("TR", None), "iranian-persian": ("IR", None), "saudi-arabian": ("SA", None),
    "iraqi": ("IQ", None), "palestinian": ("PS", None), "egyptian": ("EG", None), "chinese": ("CN", None),
    "szechuan": ("CN", "Sichuan"), "cantonese": ("CN", "Guangdong"), "hunan": ("CN", "Hunan"),
    "beijing": ("CN", "Beijing"), "japanese": ("JP", None), "korean": ("KR", None), "thai": ("TH", None),
    "vietnamese": ("VN", None), "indonesian": ("ID", None), "filipino": ("PH", None), "malaysian": ("MY", None),
    "cambodian": ("KH", None), "laotian": ("LA", None), "mongolian": ("MN", None),
}
# CulinaryDB cuisines kept → ISO2 (None = region label only)
CULINARYDB_CUISINES = {"Indian Subcontinent": None, "Middle East": None, "China": "CN", "Japan": "JP",
                       "Korea": "KR", "Thailand": "TH", "South East Asia": None}
JP_PREF_EN = {"北海道": "Hokkaido", "青森": "Aomori", "岩手": "Iwate", "宮城": "Miyagi", "秋田": "Akita", "山形": "Yamagata",
              "福島": "Fukushima", "茨城": "Ibaraki", "栃木": "Tochigi", "群馬": "Gunma", "埼玉": "Saitama", "千葉": "Chiba",
              "東京": "Tokyo", "神奈川": "Kanagawa", "新潟": "Niigata", "富山": "Toyama", "石川": "Ishikawa", "福井": "Fukui",
              "山梨": "Yamanashi", "長野": "Nagano", "岐阜": "Gifu", "静岡": "Shizuoka", "愛知": "Aichi", "三重": "Mie",
              "滋賀": "Shiga", "京都": "Kyoto", "大阪": "Osaka", "兵庫": "Hyogo", "奈良": "Nara", "和歌山": "Wakayama",
              "鳥取": "Tottori", "島根": "Shimane", "岡山": "Okayama", "広島": "Hiroshima", "山口": "Yamaguchi",
              "徳島": "Tokushima", "香川": "Kagawa", "愛媛": "Ehime", "高知": "Kochi", "福岡": "Fukuoka", "佐賀": "Saga",
              "長崎": "Nagasaki", "熊本": "Kumamoto", "大分": "Oita", "宮崎": "Miyazaki", "鹿児島": "Kagoshima",
              "沖縄": "Okinawa"}

# grams per unit (volume units at density 1; approximate)
UNIT_G = {"g": 1, "gm": 1, "gms": 1, "gram": 1, "grams": 1, "gr": 1, "kg": 1000, "kgs": 1000, "mg": 0.001,
          "ml": 1, "cc": 1, "l": 1000, "ltr": 1000, "litre": 1000, "liter": 1000, "litres": 1000, "liters": 1000,
          "tsp": 5, "teaspoon": 5, "teaspoons": 5, "tbsp": 15, "tablespoon": 15, "tablespoons": 15, "tbs": 15,
          "cup": 240, "cups": 240, "c": 240, "oz": 28.35, "ounce": 28.35, "ounces": 28.35, "lb": 453.6,
          "lbs": 453.6, "pound": 453.6, "pounds": 453.6, "pinch": 0.3, "dash": 0.5, "drops": 0.05, "drop": 0.05,
          "sprig": 1, "sprigs": 1,
          "克": 1, "千克": 1000, "公斤": 1000, "斤": 500, "两": 50, "毫升": 1, "升": 1000,
          "大さじ": 15, "小さじ": 5, "カップ": 200, "合": 180}
EN_UNITS = ("kg|kgs|g|gm|gms|grams?|gr|mg|ml|cc|l|ltr|lit(?:re|er)s?|tsps?|teaspoons?|tbsps?|tablespoons?|tbs|cups?|"
            "oz|ounces?|lbs?|pounds?|pinch(?:es)?|dash(?:es)?|drops?|sprigs?|cloves?|pieces?|pcs|cans?|packages?|"
            "packets?|slices?|sticks?|bunch(?:es)?|heads?|stalks?|large|medium|small|whole")
NUM = r"(?:\d+\s+\d+/\d+|\d+/\d+|\d+(?:\.\d+)?|[½¼¾⅓⅔⅛])"
EN_QTY = re.compile(rf"^\s*({NUM})(?:\s*(?:-|to)\s*{NUM})?\s*({EN_UNITS})?\b\.?\s*(?:\([^)]*\)\s*)?", re.I)
FRAC = {"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 1 / 3, "⅔": 2 / 3, "⅛": 0.125}
ZH_NUM = {"半": 0.5, "一": 1, "两": 2, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
ZH_UNITS = ("千克|公斤|kg|KG|克|g|G|斤|两|毫升|ml|ML|升|L|个|只|片|瓣|根|勺|汤勺|汤匙|大勺|小勺|茶匙|匙|碗|杯|把|颗|块|条|段|滴|撮|张|粒|"
            "朵|包|袋|盒|罐|棵|支|枚|小把|小块|小段|小碗|大碗|大块|厘米|cm|个半|份|盎司|磅|束|听|瓶|头|尾|捆")
ZH_AMT = re.compile(rf"^\s*(适量|少许|少量|若干|一些|一点|一小撮|随意|按需|酌量)?\s*"
                    rf"((?:\d+(?:\.\d+)?(?:\s*[-~～到]\s*\d+(?:\.\d+)?)?|[半一两二三四五六七八九十]+)(?:\s*/\s*\d+)?)?\s*"
                    rf"({ZH_UNITS})?\s*(左右)?")
JA_AMT = re.compile(r"(大さじ|小さじ|カップ)\s*(" + NUM + r"(?:と" + NUM + r")?)|(" + NUM + r"(?:と" + NUM +
                    r")?)\s*(kg|g|ml|cc|l|ℓ|合|個|本|枚|切れ|片|尾|丁|束|袋|株|玉|房|粒|つ|杯|匹|缶|パック|膳|cm)?", re.I)


# ---------------------------------------------------------------------------------------------- helpers
def num(x):
    if x is None:
        return None
    x = unicodedata.normalize("NFKC", str(x)).strip()
    if x in FRAC:
        return FRAC[x]
    x = x.replace("⁄", "/")
    m = re.fullmatch(r"(\d+)\s+(\d+)/(\d+)", x) or re.fullmatch(r"(\d+)と(\d+)/(\d+)", x)
    if m:
        return int(m.group(1)) + int(m.group(2)) / int(m.group(3))
    m = re.fullmatch(r"(\d+)/(\d+)", x)
    if m:
        return int(m.group(1)) / int(m.group(2)) if int(m.group(2)) else None
    m = re.fullmatch(r"(\d+(?:\.\d+)?)\s*[-~～到]\s*(\d+(?:\.\d+)?)", x)
    if m:
        return (float(m.group(1)) + float(m.group(2))) / 2
    if x and all(ch in ZH_NUM for ch in x):
        if x == "十":
            return 10
        if len(x) == 2 and x[0] == "十":
            return 10 + ZH_NUM[x[1]]
        if len(x) == 2 and x[1] == "十":
            return ZH_NUM[x[0]] * 10
        return ZH_NUM.get(x[0])
    try:
        return float(x)
    except ValueError:
        return None


def grams_of(q, unit):
    if q is None or unit is None:
        return None
    f = UNIT_G.get(unit.lower() if unit.isascii() else unit)
    return round(q * f, 3) if f is not None else None


def parse_en(text):
    """'1 1/2 cups basmati rice' -> (1.5, 'cups', 360, 'basmati rice')"""
    t = unicodedata.normalize("NFKC", str(text)).strip()
    m = EN_QTY.match(t)
    if not m or not m.group(0).strip():
        return None, None, None, t
    q = num(m.group(1))
    unit = (m.group(2) or "").lower() or None
    rest = t[m.end():].strip(" ,.-")
    rest = re.sub(r"^of\s+", "", rest)
    return q, unit, grams_of(q, unit), rest or t


def parse_zh(text):
    """'1kg羊肉' -> (1, 'kg', 1000, '羊肉'); '适量花椒' -> (None, None, None, '花椒')"""
    t = unicodedata.normalize("NFKC", str(text)).strip()
    t = re.sub(r"[（(][^）)]*[）)]", "", t).strip()
    m = ZH_AMT.match(t)
    q = unit = None
    rest = t
    if m and m.group(2) and re.fullmatch(r"[半一两二三四五六七八九十]+", m.group(2)) and not m.group(3):
        # a Chinese numeral without a unit is part of the name ('八角', '五香粉', '十三香'); keep only a leading 适量
        m = ZH_AMT.match(t[:len(m.group(1))]) if m.group(1) else None
    if m and m.group(0).strip():
        q = num(m.group(2)) if m.group(2) else None
        unit = m.group(3)
        rest = t[m.end():].strip()
    else:  # trailing amount: '羊肉500克', '盐 适量'
        m2 = re.search(rf"\s*((?:\d+(?:\.\d+)?|[半一两二三四五六七八九十]+))\s*({ZH_UNITS})\s*(左右)?$|\s*(适量|少许|少量|若干)$", t)
        if m2 and m2.start() > 0:
            q = num(m2.group(1)) if m2.group(1) else None
            unit = m2.group(2)
            rest = t[:m2.start()].strip()
    if unit in ("个半",):
        q = (q or 1) + 0.5
        unit = "个"
    return q, unit, grams_of(q, unit) if unit else None, rest or t


def parse_ja_line(line):
    """'- 【タレ】 醤油: 大さじ2' -> ('醤油', 2, '大さじ', 30, '【タレ】 醤油: 大さじ2')"""
    t = unicodedata.normalize("NFKC", line).strip().lstrip("-・*").strip()
    raw = t
    t = re.sub(r"(\d+)月(\d+)日", lambda m: f"{int(m.group(1))}/{int(m.group(2))}", t)  # '1/2' mangled into a date
    name, _, amt = t.rpartition(":") if ":" in t else (t, "", "")
    name = re.sub(r"^[【\[][^】\]]*[】\]]\s*", "", name).strip()
    q = unit = g = None
    m = JA_AMT.search(amt or "")
    if m:
        if m.group(1):
            unit, q = m.group(1), num(m.group(2))
        else:
            q, unit = num(m.group(3)), (m.group(4) or None)
        g = grams_of(q, unit) if unit else None
    return name, q, unit, g, raw


def h(x):
    return int(hashlib.md5(str(x).encode()).hexdigest()[:8], 16)


def s(x):
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    t = str(x).strip()
    return t or None


class Acc:
    def __init__(self):
        self.dishes, self.lines = [], []

    def dish(self, source_id, rec_id, name, *, name_local=None, lang="en", iso2=None, subregion=None, cuisine=None,
             servings=None, steps=None, has_amounts=False):
        did = f"{source_id}:{rec_id}"
        self.dishes.append(dict(dish_id=did, name=s(name), name_local=s(name_local), lang=lang, country_iso2=iso2,
                                subregion=s(subregion), cuisine_label=s(cuisine), source_id=source_id,
                                source_record_id=str(rec_id), servings=s(servings), steps_text=s(steps),
                                has_amounts=bool(has_amounts)))
        return did

    def line(self, did, raw, name, lang, source_id, q=None, unit=None, g=None, xref=None):
        self.lines.append(dict(dish_id=did, raw_text=s(raw), name=s(name) or s(raw), lang=lang, quantity=q,
                               unit=s(unit), grams=g, source_id=source_id, xref=xref))


# ---------------------------------------------------------------------------------------------- loaders
def load_saudi(A):
    d = pd.read_csv(data("saudi-food-composition-tables", "extracted", "sfct_dishes.csv"), dtype=str)
    for r in d.itertuples():
        A.dish("sfct", r.dish_id, r.dish_name, iso2="SA", subregion=r.region, cuisine="Saudi",
               servings=f"{r.serves_adults} adults" if s(r.serves_adults) else None, steps=r.preparation_steps,
               has_amounts=True)
    li = pd.read_csv(data("saudi-food-composition-tables", "extracted", "sfct_ingredients.csv"), dtype=str)
    for r in li.itertuples():
        q, unit, g, _ = parse_en(r.quantity or "")
        A.line(f"sfct:{r.dish_id}", r.ingredient, r.ingredient, "en", "sfct", q, unit, g)


def load_bahrain(A):
    base = data("bahrain-food-composition-tables", "extracted")
    d = pd.concat([pd.read_csv(f"{base}/bfct_dishes_{p}.csv", dtype=str) for p in ("macronutrients", "minerals",
                                                                                      "vitamins")])
    d = d.drop_duplicates("code")
    for r in d.itertuples():
        A.dish("bfct", r.code, r.english_name.title() if s(r.english_name) else None, name_local=r.arabic_name,
               lang="ar", iso2="BH", cuisine=f"Bahraini ({r.category})")


def load_kyrgyz(A):
    base = data("kyrgyzstan-food-composition-table", "extracted")
    names = pd.read_csv(f"{base}/dishes_proximates.csv", dtype=str).set_index("food_code")
    li = pd.read_csv(f"{base}/dish_recipes_ingredients.csv", dtype=str)
    for code, g in li.groupby("food_code", sort=False):
        nk = names.name_kyrgyz.get(code) if code in names.index else None
        A.dish("kfct", code, g.dish_name.iloc[0], name_local=nk, iso2="KG", cuisine="Kyrgyz", has_amounts=True)
        for r in g.itertuples():
            ing = s(r.ingredient)
            if not ing or not s(r.raw_weight_g) or re.search(r"^(the )?mass|total|weight of|cooked weight", ing, re.I):
                continue  # intermediate yields ('Mass of dough', 'TOTAL COOKED WEIGHT')
            name = re.sub(r"^for the [^:]+:\s*", "", ing, flags=re.I)
            name = re.sub(r"\b(an|a)\s+", "", name, flags=re.I)
            grams = float(r.raw_weight_g)
            A.line(f"kfct:{code}", ing, name, "en", "kfct", grams, "g raw", grams)


def load_indb(A):
    base = data("indian-nutrient-databank-indb")
    names = pd.read_excel(f"{base}/recipes_names.xlsx", dtype=str)
    for r in names.itertuples():
        A.dish("indb", r.recipe_code, r.recipe_name, iso2="IN", cuisine="Indian (INDB)", has_amounts=True)
    li = pd.read_excel(f"{base}/recipes.xlsx", dtype={"food_code_org": str, "food_code": str})
    for r in li.itertuples():
        code = s(r.food_code_org) or ""
        xref = None
        if code.startswith("US-"):
            xref = ("usda_fdc", code[3:])
        elif code.startswith("UK-"):
            xref = ("uk_cofid", code[3:])
        elif re.fullmatch(r"[A-Z]\d{3}", code):
            xref = ("ifct", code)
        q = r.amount if pd.notna(r.amount) else None
        unit = s(r.unit)
        A.line(f"indb:{r.recipe_code}", r.ingredient_name_org, r.ingredient_name_org, "en", "indb", q, unit,
               grams_of(q, unit) if unit else None, xref=(xref, s(r.food_name)))


def _maff_pairs(jp, en):
    """Pair JP and EN MAFF rows (no shared id) on identical ingredient-amount signatures."""
    def sig(txt):
        vals = re.findall(r"(\d+(?:\.\d+)?)\s*(?:g|ml|cc)", unicodedata.normalize("NFKC", str(txt)), re.I)
        return tuple(sorted(vals))
    es = defaultdict(list)
    for r in en.itertuples():
        k = sig(r.ingredients_with_amounts)
        if len(k) >= 3:
            es[k].append(r)
    pairs = {}
    js = Counter(sig(r.ingredients_with_amounts) for r in jp.itertuples())
    for r in jp.itertuples():
        k = sig(r.ingredients_with_amounts)
        if len(k) >= 3 and js[k] == 1 and len(es.get(k, [])) == 1:
            pairs[r.row_id] = es[k][0].dish_name
    return pairs


def load_maff(A):
    base = data("our-regional-cuisines-japan-maff")
    jp = pd.read_csv(f"{base}/parsed_jpn.csv", dtype=str)
    en = pd.read_csv(f"{base}/parsed_eng.csv", dtype=str)
    pairs = _maff_pairs(jp, en)
    for r in jp.itertuples():
        pref = s(r.prefecture)
        en_name = pairs.get(r.row_id)
        did = A.dish("maff", r.row_id, en_name or r.dish_name, name_local=r.dish_name, lang="ja", iso2="JP",
                     subregion=pref, cuisine="Japanese regional (郷土料理)", servings=r.servings, steps=r.steps,
                     has_amounts=True)
        for ln in str(r.ingredients_with_amounts or "").splitlines():
            if not ln.strip().startswith("-"):
                continue
            name, q, unit, g, raw = parse_ja_line(ln)
            if name:
                A.line(did, raw, name, "ja", "maff", q, unit, g)
    return len(pairs)


def load_culinarydb(A):
    base = data("culinarydb")
    rd = pd.read_csv(f"{base}/01_Recipe_Details.csv", dtype=str)
    rd = rd[rd.Cuisine.isin(CULINARYDB_CUISINES)]
    keep = {}
    for r in rd.itertuples():
        iso = CULINARYDB_CUISINES[r.Cuisine]
        if r.Cuisine == "Indian Subcontinent" and r.Source == "TARLA_DALAL":
            iso = "IN"  # Tarla Dalal is an Indian recipe site
        keep[r._1] = A.dish("culinarydb", r._1, r.Title, iso2=iso, cuisine=r.Cuisine)
    li = pd.read_csv(f"{base}/04_Recipe-Ingredients_Aliases.csv", dtype=str)
    li = li[li["Recipe ID"].isin(keep)]
    for rid, raw, aliased, eid in li.itertuples(index=False):
        q, unit, g, _ = parse_en(raw or "")
        A.line(keep[rid], raw, (aliased or raw or "").strip(), "en", "culinarydb", q, unit, g,
               xref=("culinarydb", eid) if s(eid) else None)
    ids_with_amounts = {l["dish_id"] for l in A.lines if l["source_id"] == "culinarydb" and l["quantity"] is not None}
    for d in A.dishes:
        if d["source_id"] == "culinarydb" and d["dish_id"] in ids_with_amounts:
            d["has_amounts"] = True


def load_irn(A, con):
    base = data("indicrecipenutri", "data")
    lab = con.execute(f"""
        SELECT l.recipe_id, l.Region, l.Cuisine, r.RecipeName, r.Lang_base, r.Servings
        FROM '{base}/corpus/labels.parquet' l JOIN '{base}/corpus/recipes.parquet' r USING (recipe_id)
        WHERE l.Region IS NOT NULL AND l.Region <> 'Pan-Indian'
        QUALIFY row_number() OVER (PARTITION BY l.Region ORDER BY hash(l.recipe_id)) <= {IRN_PER_REGION}
    """).df()
    for r in lab.itertuples():
        A.dish("indicrecipenutri", r.recipe_id, r.RecipeName, lang=(r.Lang_base or "en"), iso2="IN",
               subregion=r.Region, cuisine=r.Cuisine, servings=r.Servings, has_amounts=True)
    ids = lab.recipe_id.tolist()
    con.register("irn_ids", pd.DataFrame({"recipe_id": ids}))
    w = con.execute(f"""SELECT w.recipe_id, w.ing_index, w.name, w.quantity, w.unit, w.grams, w.tier
                        FROM '{base}/enrichment/ingredients_weights.parquet' w JOIN irn_ids USING (recipe_id)
                        ORDER BY 1, 2""").df()
    con.unregister("irn_ids")
    for r in w.itertuples():
        if not s(r.name):
            continue
        tier = f" [weight tier {r.tier}]" if s(r.tier) else ""
        A.line(f"indicrecipenutri:{r.recipe_id}", f"{r.name}{tier}", r.name, "en", "indicrecipenutri",
               None if pd.isna(r.quantity) else float(r.quantity), s(r.unit),
               None if pd.isna(r.grams) else float(r.grams))


def load_xcf(A):
    path = data("xiachufang-recipe-corpus", "recipe_corpus_full_first80MB.jsonl")
    cands = []
    with open(path, encoding="utf-8", errors="replace") as f:
        for i, ln in enumerate(f):
            try:
                o = json.loads(ln)
            except json.JSONDecodeError:
                continue
            dish = (o.get("dish") or "").strip()
            if not dish or dish == "Unknown" or not o.get("recipeIngredient"):
                continue
            kws = set((o.get("keywords") or [])[5:])
            text = (o.get("name") or "") + dish
            if kws & XCF_WESTERN or any(w in text for w in XCF_WESTERN):
                continue
            cands.append((h(i), i, o))
    cands.sort()
    for _, i, o in cands[:XCF_N]:
        name = o.get("name")
        sub = next((reg for k, reg in XCF_REGION if k in (name or "") or k in o["dish"]), None)
        kws = [k for k in (o.get("keywords") or [])[5:] if k]
        did = A.dish("xiachufang", i, o["dish"], name_local=name, lang="zh", iso2="CN", subregion=sub,
                     cuisine="Chinese home cooking" + (f" ({', '.join(kws[:3])})" if kws else ""),
                     steps=" | ".join(o.get("recipeInstructions") or []), has_amounts=True)
        for raw in o["recipeIngredient"]:
            q, unit, g, nm = parse_zh(raw)
            A.line(did, raw, nm, "zh", "xiachufang", q, unit, g)


def load_foodcom(A, con):
    path = data("food-com-recipes-and-interactions", "RAW_recipes.csv")
    tags_re = "|".join(re.escape(f"'{t}'") for t in FOODCOM_TAGS)
    df = con.execute(f"""SELECT id, name, tags, steps, ingredients FROM read_csv('{path}', all_varchar=true)
                         WHERE regexp_matches(tags, ?)""", [tags_re]).df()
    for r in df.itertuples():
        tags = ast.literal_eval(r.tags)
        hit = [t for t in tags if t in FOODCOM_TAGS]
        # most specific first: country / city tags before region tags
        hit.sort(key=lambda t: (FOODCOM_TAGS[t][1] is None, FOODCOM_TAGS[t][0] is None))
        iso, sub = FOODCOM_TAGS[hit[0]]
        try:
            steps = " | ".join(ast.literal_eval(r.steps))
        except (ValueError, SyntaxError):
            steps = r.steps
        did = A.dish("foodcom", r.id, r.name, iso2=iso, subregion=sub, cuisine=hit[0], steps=steps)
        for ing in ast.literal_eval(r.ingredients):
            A.line(did, ing, ing, "en", "foodcom")


# ---------------------------------------------------------------------------------------------- matching
def match_lines(A, R):
    """fills ingredient_id / match_method / match_score for every line (memoised on (name, lang))."""
    memo = {}
    xref_learn = Counter()
    for ln in A.lines:
        x = ln.pop("xref")
        res = None
        extra_name = None
        if isinstance(x, tuple) and len(x) == 2 and (x[0] is None or isinstance(x[0], tuple)):
            x, extra_name = x  # INDB: (code xref, standard food name)
        if x:
            res = R.by_xref(*x)
        if not res:
            key = (ln["name"], ln["lang"])
            if key not in memo:
                memo[key] = R.by_text(ln["name"], ln["lang"]) if ln["name"] else None
            res = memo[key]
            if (not res or res[2] < 0.9) and extra_name:
                k2 = (extra_name, ln["lang"])
                if k2 not in memo:
                    memo[k2] = R.by_text(extra_name, ln["lang"])
                if memo[k2] and (not res or memo[k2][2] > res[2]):
                    res = memo[k2]
            if res and x and res[1] in ("exact", "normalised", "manual") and res[2] >= 0.9:
                xref_learn[(res[0], x[0], x[1])] += 1
        if res:
            ln["ingredient_id"], ln["match_method"], ln["match_score"] = res
        else:
            ln["ingredient_id"], ln["match_method"], ln["match_score"] = None, "unmatched", None
    # one ingredient per code (the most frequent text match)
    best = {}
    for (iid, db, code), n in xref_learn.most_common():
        best.setdefault((db, code), iid)
    return [(iid, db, code) for (db, code), iid in best.items()]


# ---------------------------------------------------------------------------------------------- build
def build(con):
    con.execute("DELETE FROM dish_ingredient")
    con.execute("DELETE FROM dish")
    con.execute("DELETE FROM ingredient_xref WHERE db IN ('ifct', 'uk_cofid', 'usda_fdc')")
    A = Acc()
    load_saudi(A)
    load_bahrain(A)
    load_kyrgyz(A)
    load_indb(A)
    n_pairs = load_maff(A)
    load_culinarydb(A)
    load_irn(A, con)
    load_xcf(A)
    load_foodcom(A, con)
    R = IngredientResolver(con)
    learned = match_lines(A, R)
    dd = pd.DataFrame(A.dishes).drop_duplicates("dish_id")
    con.execute("INSERT INTO dish SELECT dish_id, name, name_local, lang, country_iso2, subregion, cuisine_label,"
                " source_id, source_record_id, servings, steps_text, has_amounts FROM dd")
    li = pd.DataFrame(A.lines)
    li = li[["dish_id", "ingredient_id", "raw_text", "quantity", "unit", "grams", "match_method", "match_score",
             "source_id", "name", "lang"]]
    li["quantity"] = pd.to_numeric(li["quantity"], errors="coerce")
    li["grams"] = pd.to_numeric(li["grams"], errors="coerce")
    li["match_score"] = pd.to_numeric(li["match_score"], errors="coerce")
    con.execute("INSERT INTO dish_ingredient SELECT dish_id, ingredient_id, raw_text, quantity, unit, grams,"
                " match_method, match_score, source_id FROM li")
    if learned:
        xdf = pd.DataFrame(learned, columns=["ingredient_id", "db", "xref_id"])
        con.execute("INSERT INTO ingredient_xref SELECT * FROM xdf")
    # report
    st = li.assign(m=li.ingredient_id.notna(), g=li.grams.notna()).groupby("source_id").agg(
        lines=("m", "size"), matched=("m", "mean"), grams=("g", "mean"))
    print(f"  [dishes] {len(dd)} dishes, {len(li)} ingredient lines; MAFF EN names paired: {n_pairs}; "
          f"INDB code xrefs learned: {len(learned)}")
    for src, r in st.iterrows():
        print(f"  [dishes]   {src:17s} lines={int(r.lines):7d} matched={r.matched:6.1%} grams={r.grams:6.1%}")
    globals()["_last_lines"] = li  # for interactive inspection


# ---------------------------------------------------------------------------------------------- nutrients
def iter_dish_nutrients():
    """Yield (dish_id, nutrient_key, source_id, amount_per_100g, unit) from the composition tables.

    nutrient_key is the analyte label as printed by the source (Saudi 'Total Protein', Bahrain 'Protein',
    Kyrgyz INFOODS tagname 'PROT', INDB column stem 'protein'); the unit comes from the source. Values that are
    missing, 'ND', 'T'/'Tr' (trace) or '<x' (below detection) are skipped.
    """
    def val(x):
        t = s(x)
        if t is None or t.upper() in ("ND", "T", "TR", "-", "NA", "N/A") or t.startswith("<"):
            return None
        try:
            return float(t.replace(",", ""))
        except ValueError:
            return None

    sf = pd.read_csv(data("saudi-food-composition-tables", "extracted", "sfct_nutrients_long.csv"), dtype=str)
    for r in sf.itertuples():
        v = val(r.per_100g)
        if v is not None:
            yield (f"sfct:{r.dish_id}", r.analyte, "sfct", v, r.unit)
    for part in ("macronutrients", "minerals", "vitamins"):
        b = pd.read_csv(data("bahrain-food-composition-tables", "extracted", f"bfct_dishes_{part}.csv"), dtype=str)
        for col in b.columns[6:]:
            m = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", col)
            if not m or col in ("source_stars",):
                continue
            key, unit = m.group(1).strip(), m.group(2).replace("/100g", "").replace(" as printed", "").strip()
            for code, x in zip(b.code, b[col]):
                v = val(x)
                if v is not None:
                    yield (f"bfct:{code}", key, "bfct", v, unit)
    kunits = dict(ENERC="kJ", ENERC_2="kcal", WATER="g", PROT="g", FAT="g", CHOT="g", CHO="g", GLUS="g", FRU="g",
                  SUCS="g", FIBT="g", CA="mg", FE="mg", MG="mg", P="mg", K="mg", ZN="mg", CU="mg", NA="mg", ASH="g",
                  OA="g", VITA="µg", CAROT="µg", VITE="mg", THIA="mg", RIBF="mg", FOL="µg", VITC="mg")
    for part in ("proximates", "minerals", "vitamins"):
        k = pd.read_csv(data("kyrgyzstan-food-composition-table", "extracted", f"dishes_{part}.csv"), dtype=str)
        for col in k.columns[5:]:
            for code, x in zip(k.food_code, k[col]):
                v = val(x)
                if v is not None:
                    yield (f"kfct:{code}", col, "kfct", v, kunits.get(col))
    ind = pd.read_excel(data("indian-nutrient-databank-indb", "INDB.xlsx"), dtype=str)
    for col in ind.columns[3:]:
        m = re.match(r"^(.*)_(kj|kcal|g|mg|ug)$", col)
        if not m:
            continue
        unit = {"ug": "µg"}.get(m.group(2), m.group(2))
        for code, x in zip(ind.food_code, ind[col]):
            v = val(x)
            if v is not None:
                yield (f"indb:{code}", m.group(1), "indb", v, unit)
