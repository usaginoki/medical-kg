"""IngredientResolver: map ids / taxa / scientific names / free text to `ingredient_id` (stage `ingredients`).

Interface (db/README.md): every lookup returns `(ingredient_id, match_method, score)` or `None`.

    r = IngredientResolver(con)
    r.by_xref('flavordb', 341)            -> ('ING:turmeric', 'xref', 1.0)
    r.by_taxon(94328)                     -> ('ING:ginger', 'taxon', 1.0)
    r.by_scientific('Curcuma longa L.')   -> ('ING:turmeric', 'scientific', 1.0)
    r.by_text('生姜', 'zh')                -> ('ING:ginger', 'manual', 1.0)

`by_text` runs these stages in order: exact-only rows of the manual map → exact alias (lower-cased) →
normalised alias (light key, then `common.norm_text`, then parenthesised content) → sub-phrases / CJK substrings
(method 'substring': a guess from part of the text) → fuzzy (English: rapidfuzz token_sort_ratio ≥ 92 against
food-source aliases, same first three letters, FUZZY_BLOCK pairs refused; CJK: character ratio ≥ 90). A hit on an alias that came from the curated map
`db/maps/ingredient_map_manual.csv` (source_id 'manual') is reported as method 'manual'. Map rows with
`scope=exact` are fragments of a line ('brown' → sugar, 'pinch' → salt): they are not aliases and only match when
the whole residual text equals the key.

`by_text_parts` additionally splits a line that names several ingredients ('salt and pepper', '土豆，面粉，鸡蛋')
into parts that each resolve; `/` and ' or ' separate alternatives, of which the first that resolves is kept.
"""
import re
import unicodedata

from common import norm_text

CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")

# languages whose aliases are searched for a query in `lang` (exact stage may also fall back to all languages)
LANG_GROUPS = {
    "en": ("en", "la", None),
    "zh": ("zh", "zh-Hant"),
    "ja": ("ja", "zh", "zh-Hant"),
    "ko": ("ko",),
}
# lower = preferred when two ingredients claim the same alias
SOURCE_RANK = {"manual": 0, "curated": 0, "culinarydb": 1, "indicrecipenutri": 2, "foodb": 3, "flavordb": 4, "ddid": 5,
               "symmap": 6, "herb": 6, "tmmc": 6, "spicerx": 6, "unaprod": 7, "imppat": 8, "knapsack": 9,
               "cmaup": 9, "duke": 10}
TYPE_RANK = {"canonical": 0, "common": 1, "scientific": 1, "zh": 1, "ja": 1, "pharmacopoeia": 2, "pinyin": 3}
# words that are weak heads when we fall back to a sub-phrase ("lamb meat" -> lamb, "onion powder" -> onion)
GENERIC = {"meat", "piece", "pieces", "powder", "paste", "leaves", "leaf", "seed", "seeds", "slice", "slices",
           "juice", "sauce", "flake", "flakes", "cube", "cubes", "mix", "strip", "strips",
           "fillet", "fillets", "stick", "sticks", "extract", "essence", "green", "red", "white", "black", "yellow",
           "sweet", "hot", "fresh", "light", "dark", "and", "or", "with", "of", "for", "in", "the", "a", "cut",
           "chunk", "chunks", "bone", "boneless", "skinless", "large", "small", "medium", "plain", "salted",
           "unsalted", "whole", "baby", "mixed", "wild", "cold", "warm", "soft", "hard", "thin", "thick", "long",
           "cooked", "canned", "frozen", "instant", "low", "fat", "free", "dry", "few", "pinch", "some", "to", "as",
           "required", "taste", "per", "slit", "split", "spring", "stalk", "string", "each", "bowl", "glass",
           "gram", "grams", "spoon", "nos"}
# heads that lose to a resolvable modifier in the sub-phrase stage ('besan flour' -> besan, not wheat flour), unless
# the modifier is a product ('bread flour', 'cake flour')
WEAK_HEAD = {"flour", "atta"}
WEAK_HEAD_NOT = {"bakery", "dish", "confectionery", "snack", "additive", "beverage", "alcoholic beverage", "dairy",
                 "meat", "fish", "baby food"}
# categories of a run of names that may be split on spaces ('ginger green chillies garlic')
SEGMENT_CATS = {"spice", "herb", "vegetable", "fruit", "legume", "nut/seed"}
# last words that make a run of names one product ('onion tomato masala', 'sesame ginger salad dressing')
PRODUCT_HEAD = {"oil", "noodle", "dressing", "chutney", "sauce", "masala", "paste", "powder", "water", "juice", "milk",
                "flour", "butter", "cream", "mix", "curry", "soup", "stock", "broth", "vinegar", "syrup", "tea", "bread",
                "rice", "seasoning", "pickle", "jam", "salad", "cake", "chip"}
# CJK aliases that are generic heads ('肉' meat → pork): any other substring of the line wins over them
# (cuts that default to pork: '牛里脊肉' is beef, '羊排' lamb)
CJK_GENERIC = {"肉", "肉片", "肉末", "肉丝", "肉馅", "肉沫", "肉糜", "肉块", "肉丁", "瘦肉", "里脊", "里脊肉", "排骨", "排骨肉",
               "肋排", "五花", "五花肉", "花肉", "肥肠", "酱", "粉", "汁", "菜", "汤"}
# sources whose English names are foods (fuzzy targets); herb / ethnobotany sources carry many plant names
FOOD_SOURCES = {"manual", "curated", "culinarydb", "indicrecipenutri", "foodb", "flavordb"}
# fuzzy pairs that look alike but are different foods (query key, alias key)
FUZZY_BLOCK = {("leaves", "leaven"), ("fruity", "fruit"), ("crisco", "cisco"), ("marsala", "masala"),
               ("sambal powder", "sambar powder"), ("pimenton", "pimento"), ("craisin", "raisin")}
# separators of a line that lists several ingredients; alternatives ('ghee / oil', 'besan or gram flour')
LIST_SEP = re.compile(r"\s*[、，,;；+＋&]\s*|\s+and\s+")
ALT_SEP = re.compile(r"\s*[/／或]\s*|\s+or\s+")
IRREG_PLURAL = {"leaves": "leaf", "halves": "half", "loaves": "loaf", "knives": "knife", "calves": "calf",
                "tomatoes": "tomato", "potatoes": "potato", "mangoes": "mango", "chillies": "chilli",
                "radishes": "radish", "dishes": "dish", "anchovies": "anchovy", "cherries": "cherry"}
# filler phrases in English ingredient lines ('salt as required', 'oil for deep frying', 'a few curry leaves')
EN_FILLER = re.compile(
    r"\b(as (?:per|required|needed|reqd|req)(?: (?:taste|requirement|need))?|to taste|according to taste|"
    r"for (?:deep |shallow )?(?:frying|fry|greasing|tempering|garnish(?:ing)?|seasoning|dusting|brushing|"
    r"serving|decoration|coating|cooking|the [a-z ]+|boiling|soaking|kneading)|(?:a )?(?:few|little|handful|"
    r"pinch|dash|bunch|sprig|some)(?: of)?|optional|or more|or less|approx(?:imately)?|about|little|"
    r"plus extra|plus more|if needed|if required|if available|or as required|at room temperature|"
    r"cut into [a-z ]+|finely|roughly|thinly|freshly|chopped|sliced|minced|diced|grated|crushed|ground|"
    r"pieces?|nos?|number|\d+(?:\.\d+)?|tsp|tbsp|cups?|teaspoons?|tablespoons?|grams|gms?|kg|ml|inch|cm)\b",
    re.I)


def clean_en(text):
    t = unicodedata.normalize("NFKC", str(text)).lower()
    t = re.sub(r"\([^)]*\)", " ", t)
    t = t.split(",")[0] if not t.startswith(",") else t
    t = re.sub(r"^\s*no\.\s?s(?=[a-z])", "", t)  # 'no.stomato' (IndicRecipeNutri 'nos' glued to the name)
    t = EN_FILLER.sub(" ", t)
    t = re.sub(r"[^a-z\s'-]", " ", t)
    t = re.sub(r"\b(of|or|and|with|for)\s*$", " ", t.strip())
    t = re.sub(r"^\s*(of|or|and|a|an|to)\b", " ", t)
    t = re.sub(r"^\s*(of|or|and|a|an|to)\b", " ", t)
    return re.sub(r"\s+", " ", t).strip()


SCI_RANKS = {"var.", "var", "subsp.", "subsp", "ssp.", "ssp", "f.", "cv.", "convar.", "forma"}


def key_norm(text):
    """Light normalisation used for alias keys: NFKC, lower, parentheses dropped, punctuation → space,
    last word singularised. Unlike `norm_text` it keeps descriptors ('dried lime' stays 'dried lime')."""
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower().strip()
    if CJK.search(t):
        t = re.sub(r"\([^)]*\)|（[^）]*）|【[^】]*】|\[[^\]]*\]", "", t)
        return re.sub(r"[\s:：、,，。・/／\-_~～·.!！?？\"'“”‘’]+", "", t)
    t = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", t)
    t = t.replace("&", " and ")
    t = re.sub(r"[^a-z0-9\s]", " ", unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode())
    words = t.split()
    if words:
        w = words[-1]
        if w in IRREG_PLURAL:
            w = IRREG_PLURAL[w]
        elif w.endswith("ies") and len(w) > 4:
            w = w[:-3] + "y"
        elif w.endswith(("oes", "ches", "shes", "xes")) and len(w) > 4:
            w = w[:-2]
        elif w.endswith("s") and not w.endswith(("ss", "us", "is")) and len(w) > 3:
            w = w[:-1]
        words[-1] = w
    return " ".join(words)


FUZZY_BLOCK_N = {(key_norm(a), key_norm(b)) for a, b in FUZZY_BLOCK}


def sci_parse(name):
    """'Allium cepa var. cepa L.' -> ('allium cepa var. cepa', 'allium cepa'); returns (None, None) if no binomial."""
    if not name or not isinstance(name, str):
        return None, None
    t = unicodedata.normalize("NFKC", name).replace("×", "x").strip()
    t = re.sub(r"[\"'‘’]", "", t)
    toks = re.split(r"\s+", t)
    if len(toks) < 2 or not re.fullmatch(r"[A-Za-z][a-zA-Z-]+", toks[0]):
        return None, None
    genus = toks[0].lower()
    i = 1
    if toks[i].lower() in ("x",) and len(toks) > 2:
        sp = "x " + toks[2].lower()
        i = 3
    else:
        sp = toks[i].lower()
        i = 2
    if not re.fullmatch(r"(x )?[a-z][a-z-]+", sp) or sp in ("sp", "sp.", "spp", "spp."):
        return None, None
    binom = f"{genus} {sp}"
    full = binom
    while i < len(toks) - 1:
        if toks[i].lower() in SCI_RANKS and re.fullmatch(r"[a-z][a-z-]+", toks[i + 1].lower()):
            rank = toks[i].lower().rstrip(".") + "."
            if rank == "ssp.":
                rank = "subsp."
            full = f"{binom} {rank} {toks[i + 1].lower()}"
            break
        i += 1
    return full, binom


def _manual_keys():
    """db/maps/ingredient_map_manual.csv → (lower-cased raw_norm keys of alias rows (hits on these report method
    'manual'), {lang: {key: ingredient_id}} of the `scope=exact` rows)."""
    import csv
    import os
    from common import DB_DIR
    out, exact = set(), {}
    try:
        with open(os.path.join(DB_DIR, "maps", "ingredient_map_manual.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not row.get("raw_norm") or not row.get("ingredient_id"):
                    continue
                k = unicodedata.normalize("NFKC", row["raw_norm"]).lower().strip()
                if (row.get("scope") or "").strip() == "exact":
                    exact.setdefault(row.get("lang") or None, {})[k] = row["ingredient_id"]
                else:
                    out.add(k)
    except FileNotFoundError:
        pass
    return out, exact


def _rank(source_id, alias_type):
    return (SOURCE_RANK.get(source_id, 11), TYPE_RANK.get(alias_type, 4))


class IngredientResolver:
    def __init__(self, con):
        self.con = con
        rows = con.execute("SELECT ingredient_id, canonical_name, scientific_name, ncbi_taxon_id FROM ingredient").fetchall()
        self.ids = {r[0] for r in rows}
        self.name = {r[0]: r[1] for r in rows}
        self.cat = dict(con.execute("SELECT ingredient_id, category FROM ingredient").fetchall())
        self.taxon, self.sci_full, self.sci_bin = {}, {}, {}
        for iid, _, sci, tax in rows:
            if tax is not None:
                self.taxon.setdefault(int(tax), iid)
        # scientific names from ingredient.scientific_name (rank 0) and scientific aliases (rank 1)
        sci_rows = [(iid, sci, 0, tax is not None) for iid, _, sci, tax in rows if sci]
        sci_rows += [(iid, a, 1, False) for iid, a in con.execute(
            "SELECT ingredient_id, alias FROM ingredient_alias WHERE alias_type='scientific'").fetchall()]
        cand_full, cand_bin = {}, {}
        for iid, sci, rk, has_tax in sci_rows:
            full, binom = sci_parse(sci)
            if not full:
                continue
            cand_full.setdefault(full, []).append((rk, not has_tax, iid))
            cand_bin.setdefault(binom, []).append((rk, 0 if full == binom else 1, not has_tax, iid))
        self.sci_full = {k: sorted(v)[0][-1] for k, v in cand_full.items()}
        for k, v in cand_bin.items():
            v = sorted(v)
            ids = {x[-1] for x in v}
            # ambiguous binomial (e.g. several Brassica oleracea varieties) only resolves if one row is the plain binomial
            if len(ids) == 1 or v[0][1] == 0:
                self.sci_bin[k] = v[0][-1]
        for (tax, iid) in con.execute("SELECT xref_id, ingredient_id FROM ingredient_xref WHERE db='ncbi_taxon'").fetchall():
            try:
                self.taxon.setdefault(int(tax), iid)
            except ValueError:
                pass
        self.xref = {}
        for db, xid, iid in con.execute("SELECT db, xref_id, ingredient_id FROM ingredient_xref").fetchall():
            self.xref.setdefault((db, self._xnorm(db, xid)), iid)
        # alias indexes: {lang: {key: (rank, iid, source)}}
        self.exact, self.keyn, self.normn, self.fuzzy_choices = {}, {}, {}, {}
        self.pharma = {}
        self.manual_keys_pre, exact_only = _manual_keys()
        self.exact_only = {lg: {k: v for k, v in d.items() if v in self.ids} for lg, d in exact_only.items()}
        self.food_keys = {}  # {lang: set of key_norm aliases from food sources} (fuzzy targets)
        arows = con.execute("SELECT ingredient_id, alias, lang, alias_type, source_id FROM ingredient_alias").fetchall()
        for iid, alias, lang, atype, src in arows:
            if not alias:
                continue
            rk = _rank(src, atype)
            a = unicodedata.normalize("NFKC", alias).lower().strip()
            src = "manual" if (src == "manual" and a in self.manual_keys_pre) else ("curated" if src == "manual" else src)
            self._put(self.exact, lang, a, rk, iid, src)
            self._put(self.keyn, lang, key_norm(alias), rk, iid, src)
            if src in FOOD_SOURCES:
                self.food_keys.setdefault(lang, set()).add(key_norm(alias))
            n = norm_text(alias)
            # a descriptor-stripped key ('dried lime' -> 'lime') loses to aliases that are literally that key
            self._put(self.normn, lang, n, (rk[0] + (0 if n == a else 20), rk[1]), iid, src)
            if atype == "pharmacopoeia":
                self.pharma.setdefault(a, iid)
        self._cache = {}

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _put(index, lang, key, rk, iid, src):
        if not key:
            return
        d = index.setdefault(lang, {})
        cur = d.get(key)
        if cur is None or rk < cur[0]:
            d[key] = (rk, iid, src)

    @staticmethod
    def _xnorm(db, xid):
        s = str(xid).strip()
        if s.endswith(".0") and s[:-2].isdigit():
            s = s[:-2]
        if db == "symmap":
            m = re.fullmatch(r"(?:SMHB)?0*(\d+)", s, re.I)
            if m:
                return f"SMHB{int(m.group(1)):05d}"
        if db in ("usda_fdc",):
            s = re.sub(r"^US-", "", s)
        return s

    def _langs(self, lang):
        return LANG_GROUPS.get(lang, (lang,))

    def _lookup(self, index, key, lang, all_langs=False):
        best = None
        langs = list(self._langs(lang))
        if all_langs:
            langs += [lg for lg in index if lg not in langs]
        for lg in langs:
            hit = index.get(lg, {}).get(key)
            if hit and (best is None or hit[0] < best[0]):
                best = hit
            if best and lg == langs[0]:
                break  # first-choice language wins outright
        return best

    # ------------------------------------------------------------------ interface
    def by_xref(self, db, xref_id):
        iid = self.xref.get((db, self._xnorm(db, xref_id)))
        return (iid, "xref", 1.0) if iid else None

    def by_taxon(self, taxid):
        try:
            iid = self.taxon.get(int(float(taxid)))
        except (TypeError, ValueError):
            return None
        return (iid, "taxon", 1.0) if iid else None

    def by_scientific(self, name):
        full, binom = sci_parse(name)
        if full and full in self.sci_full:
            return (self.sci_full[full], "scientific", 1.0)
        if binom and binom in self.sci_bin:
            return (self.sci_bin[binom], "scientific", 0.95 if full != binom else 1.0)
        if isinstance(name, str):
            iid = self.pharma.get(unicodedata.normalize("NFKC", name).lower().strip())
            if iid:
                return (iid, "pharmacopoeia", 0.9)
        # longer strings that contain a binomial ("Rhizoma of Zingiber officinale Rosc.")
        if isinstance(name, str):
            toks = name.split()
            for i in range(len(toks) - 1):
                if toks[i][:1].isupper() and toks[i + 1][:1].islower():
                    f, b = sci_parse(" ".join(toks[i:i + 4]))
                    if b and b in self.sci_bin and i > 0:
                        return (self.sci_bin[b], "scientific", 0.85)
        return None

    def by_text(self, text, lang="en", fuzzy=True):
        if text is None:
            return None
        ck = (text, lang, fuzzy)
        if ck in self._cache:
            return self._cache[ck]
        res = self._by_text(text, lang, fuzzy)
        self._cache[ck] = res
        return res

    def by_text_strict(self, text, lang="en"):
        """exact / normalised stages only (no sub-phrase, substring or fuzzy guess)"""
        if text is None:
            return None
        ck = ("strict", text, lang)
        if ck not in self._cache:
            self._cache[ck] = self._by_text(text, lang, fuzzy=False, loose=False)
        return self._cache[ck]

    def by_text_parts(self, text, lang="en"):
        """→ [(part_text, (ingredient_id, match_method, score) | None), …]: one element unless the line names several
        ingredients ('ginger, garlic and chillies', '土豆，面粉，鸡蛋'), which are split where every part resolves."""
        if text is None:
            return [(text, None)]
        ck = ("parts", text, lang)
        if ck not in self._cache:
            whole = self._by_text(text, lang, fuzzy=False, loose=False, strict_upto="keyn")
            parts = None if whole else self._split(text, lang)
            self._cache[ck] = parts or [(text, whole or self.by_text(text, lang))]
        return self._cache[ck]

    def _ret(self, hit, method, score):
        rk, iid, src = hit
        return (iid, "manual" if src == "manual" else method, score)

    def _exact_only(self, raw, lang):
        for lg in self._langs(lang):
            d = self.exact_only.get(lg, {})
            iid = d.get(raw) or d.get(key_norm(raw))
            if iid:
                return (iid, "manual", 1.0)
        return None

    def _by_text(self, text, lang, fuzzy, loose=True, strict_upto=None, parts=False):
        """loose=False stops before the sub-phrase / substring / fuzzy guesses; strict_upto='keyn' stops after the
        exact and light-key stages (used before trying to split a line); parts=True (a part of a split line) skips
        the exact-only fragments ('8 large eggs, chilled' is not eggs + water)."""
        raw = unicodedata.normalize("NFKC", str(text)).lower().strip()
        if not raw:
            return None
        res = None if parts else self._exact_only(raw, lang)
        if res:
            return res
        cjk = bool(CJK.search(raw))
        hit = self._lookup(self.exact, raw, lang, all_langs=True)
        if hit:
            return self._ret(hit, "exact", 1.0)
        k = key_norm(raw)
        hit = self._lookup(self.keyn, k, lang, all_langs=cjk)
        if hit:
            return self._ret(hit, "normalised", 0.95)
        if strict_upto == "keyn":
            return None
        if not cjk:
            # the name before a comma as written ('crushed red pepper, ground'), before fillers are removed
            head = raw.split(",")[0].strip()
            if head and head != raw:
                hit = self._lookup(self.keyn, key_norm(head), lang)
                if hit:
                    return self._ret(hit, "normalised", 0.93)
            ce = clean_en(raw)
            if ce and ce != raw:
                # fragments also match the line without fillers ('a pinch of red color'), not a comma head
                res = None if (parts or "," in raw) else self._exact_only(ce, lang)
                if res:
                    return res
                hit = self._lookup(self.keyn, key_norm(ce), lang)
                if hit:
                    return self._ret(hit, "normalised", 0.92)
                raw_c = ce
            else:
                raw_c = raw
        else:
            raw_c = raw
        n = norm_text(raw_c)
        hit = self._lookup(self.normn, n, lang) or self._lookup(self.keyn, n, lang)
        if hit:
            return self._ret(hit, "normalised", 0.9)
        # content of parentheses: 'Dried lime (loomi)' -> 'loomi'
        for inner in re.findall(r"[(（]([^)）]+)[)）]", raw):
            hit = self._lookup(self.keyn, key_norm(inner), lang, all_langs=cjk)
            if hit:
                return self._ret(hit, "normalised", 0.85)
        if not loose:
            return None
        if cjk:
            res = self._cjk_sub(k or raw, lang)
            if res:
                return res
        else:
            res = self._sub_phrase(key_norm(raw_c) or n, lang)
            if res:
                return res
        if fuzzy:
            return self._fuzzy(n or key_norm(raw_c) if not cjk else k, lang)
        return None

    # ------------------------------------------------------------------ multi-ingredient lines
    def _part(self, text, lang):
        """a part of a split line: strict stages only (CJK parts may also use the substring stage); generic words
        ('chopped', 'juice', 'gram') never count as a part."""
        t = text.strip(" .:-–")
        if not t or clean_en(t) in GENERIC or key_norm(t) in GENERIC:
            return None
        res = self._by_text(t, lang, fuzzy=False, loose=False, parts=True)
        if not res and CJK.search(t):
            res = self._cjk_sub(key_norm(t), lang)
        return res

    def _alts(self, text, lang):
        """'besan / gram flour', 'ghee or oil' → the first alternative that resolves (whole text first)."""
        res = self._part(text, lang)
        if res:
            return text, res
        for alt in ALT_SEP.split(text):
            res = self._part(alt, lang) if alt.strip() else None
            if res:
                return alt.strip(), res
        return None

    def _split(self, text, lang):
        t = unicodedata.normalize("NFKC", str(text)).strip()
        cjk = bool(CJK.search(t))
        sep = re.compile(LIST_SEP.pattern + (r"|\s+" if cjk else ""))
        chunks = [c for c in sep.split(t) if c and c.strip()]
        out = []
        if len(chunks) >= 2 and not cjk and re.search(r"\sor\s", t):
            # 'Lamb, horse or beef meat': the commas list alternatives too
            for c in re.split(r"\s*,\s*|\s+or\s+", t):
                r = self._part(c, lang) if c.strip() else None
                if r:
                    return [(c.strip(), r)]
            return None
        if len(chunks) == 2 and not cjk and "," in t and self._part(f"{chunks[1]} {chunks[0]}", lang):
            # INDB-style inverted names: 'Sugar, Icing' is icing sugar
            return [(t, self._part(f"{chunks[1]} {chunks[0]}", lang))]
        if len(chunks) >= 2:
            for i, c in enumerate(chunks):
                r = self._alts(c, lang)
                # a later chunk with a participle is preparation, not another ingredient ('2 eggs, chilled',
                # '1 head garlic, cloves peeled'), unless it is an alias as written
                if r and i and not cjk and re.search(r"[a-z]ed\b", c.lower()) and r[1][1] not in ("exact", "manual"):
                    r = None
                if not r:
                    out = []
                    break
                out.append(r)
        elif ALT_SEP.search(t):
            r = self._alts(t, lang)
            return [r] if r else None
        elif not cjk:
            out = self._segment(t, lang)
        # drop repeated ingredients; a split needs at least two different ones
        seen, parts = set(), []
        for p, r in out:
            if r[0] not in seen:
                seen.add(r[0])
                parts.append((p, r))
        return parts if len(parts) >= 2 else ([parts[0]] if parts and len(out) >= 2 else None)

    def _segment(self, text, lang):
        """space-separated run of ingredient names ('ginger green chillies garlic') → ≥ 3 known names covering all
        words (fewest segments); anything less is left to the sub-phrase stage."""
        words = key_norm(text).split()
        if not 3 <= len(words) <= 10:
            return []
        best = {0: []}
        for j in range(1, len(words) + 1):
            for i in range(max(0, j - 4), j):
                if i not in best:
                    continue
                seg = words[i:j]
                if all(w in GENERIC for w in seg):
                    continue
                hit = self._lookup(self.keyn, key_norm(" ".join(seg)), lang)
                if not hit or self.cat.get(hit[1]) not in SEGMENT_CATS:
                    continue
                cand = best[i] + [(" ".join(seg), self._ret(hit, "normalised", 0.9))]
                if j not in best or len(cand) < len(best[j]):
                    best[j] = cand
        segs = best.get(len(words), [])
        # a product named after its ingredients ('rice bran oil', 'mint coriander chutney') is one ingredient
        if words[-1] in PRODUCT_HEAD:
            return []
        return segs if len(segs) >= 3 and len({r[0] for _, r in segs}) == len(segs) else []

    # ------------------------------------------------------------------ guesses
    def _sub_phrase(self, n, lang):
        words = n.split()
        if len(words) < 2:
            return None
        L = len(words)
        for size in range(L - 1, 0, -1):
            cands = []
            for i in range(L - size, -1, -1):  # rightmost (head noun) first
                phrase = words[i:i + size]
                if size == 1 and phrase[0] in GENERIC:
                    continue
                if all(w in GENERIC for w in phrase):
                    continue
                hit = self._lookup(self.keyn, key_norm(" ".join(phrase)), lang)
                if hit:
                    cands.append((size == 1 and phrase[0] in WEAK_HEAD, hit))
            if cands:
                pick = cands[0][1]
                if cands[0][0]:
                    pick = next((h for _, h in cands[1:] if self.cat.get(h[1]) not in WEAK_HEAD_NOT), pick)
                return (pick[1], "substring", round(0.6 + 0.3 * size / L, 2))
        return None

    def _cjk_sub(self, s, lang):
        """longest alias found anywhere in the text; ties go to the right end (head noun in zh/ja); generic heads
        ('肉' → pork, '里脊', '酱') only when nothing else is found ('牛肉片' → beef, not '肉片' → pork)."""
        L = len(s)
        minlen = 1 if L <= 3 else 2
        cands = []
        for size in range(L - 1, minlen - 1, -1):
            for i in range(L - size, -1, -1):
                sub = s[i:i + size]
                if not CJK.search(sub):
                    continue
                hit = self._lookup(self.keyn, sub, lang, all_langs=True)
                # substrings only against curated / seed aliases: short katakana plant names from herb sources
                # ('チャ' tea, 'キビ' millet) and single characters ('酱', '桃') would match inside unrelated words
                if hit and hit[0][0] <= 4 and (size >= 2 or hit[2] in ("manual", "curated")):
                    cands.append((sub in CJK_GENERIC, -size, -i, hit))
        if not cands:
            return None
        _, size, _, hit = min(cands)
        return (hit[1], "substring", round(0.6 + 0.3 * -size / L, 2))

    def _fuzzy(self, q, lang):
        if not q or len(q) < 5:
            return None
        from rapidfuzz import fuzz, process
        lg = lang if lang in self.keyn else None
        if lg is None:
            return None
        cjk = bool(CJK.search(q))
        if (lg, cjk) not in self.fuzzy_choices:
            # English targets only from food sources (herb / ethnobotany names: 'Cisco' whitefish, 'Pimento')
            food = self.food_keys.get(lg, set())
            self.fuzzy_choices[(lg, cjk)] = [k for k in self.keyn[lg] if len(k) >= 3 and (cjk or k in food)]
        keys = self.fuzzy_choices[(lg, cjk)]
        qk = key_norm(q)
        # English: ≥ 92 and the same first three letters ('leaves' ≠ 'leaven'); CJK keeps character ratio ≥ 90
        for m in process.extract(q, keys, scorer=fuzz.ratio if cjk else fuzz.token_sort_ratio,
                                 score_cutoff=90 if cjk else 92, limit=5):
            if (not cjk and m[0][:3] != q[:3]) or (qk, key_norm(m[0])) in FUZZY_BLOCK_N:
                continue
            hit = self.keyn[lg][m[0]]
            return (hit[1], "fuzzy", round(m[1] / 100, 3))
        return None
