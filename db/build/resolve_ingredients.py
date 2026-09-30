"""IngredientResolver: map ids / taxa / scientific names / free text to `ingredient_id` (stage `ingredients`).

Interface (db/README.md): every lookup returns `(ingredient_id, match_method, score)` or `None`.

    r = IngredientResolver(con)
    r.by_xref('flavordb', 341)            -> ('ING:turmeric', 'xref', 1.0)
    r.by_taxon(94328)                     -> ('ING:ginger', 'taxon', 1.0)
    r.by_scientific('Curcuma longa L.')   -> ('ING:turmeric', 'scientific', 1.0)
    r.by_text('生姜', 'zh')                -> ('ING:ginger', 'manual', 1.0)

`by_text` runs these stages in order: exact alias (lower-cased) → normalised alias (light key, then
`common.norm_text`, then parenthesised content, then sub-phrases / CJK substrings) → fuzzy (rapidfuzz
token_sort_ratio ≥ 90 against aliases of the same language). A hit on an alias that came from the curated
map `db/maps/ingredient_map_manual.csv` (source_id 'manual') is reported as method 'manual'.
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
           "required", "taste", "per", "slit", "split", "spring", "stalk", "string", "each", "bowl", "glass"}
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
    r"pieces?|nos?|number|\d+(?:\.\d+)?|tsp|tbsp|cups?|teaspoons?|tablespoons?|grams?|gm|kg|ml|inch|cm)\b",
    re.I)


def clean_en(text):
    t = unicodedata.normalize("NFKC", str(text)).lower()
    t = re.sub(r"\([^)]*\)", " ", t)
    t = t.split(",")[0] if not t.startswith(",") else t
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
    """lower-cased raw_norm keys of db/maps/ingredient_map_manual.csv (hits on these report method 'manual')."""
    import csv
    import os
    from common import DB_DIR
    out = set()
    try:
        with open(os.path.join(DB_DIR, "maps", "ingredient_map_manual.csv"), encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("raw_norm"):
                    out.add(unicodedata.normalize("NFKC", row["raw_norm"]).lower().strip())
    except FileNotFoundError:
        pass
    return out


def _rank(source_id, alias_type):
    return (SOURCE_RANK.get(source_id, 11), TYPE_RANK.get(alias_type, 4))


class IngredientResolver:
    def __init__(self, con):
        self.con = con
        rows = con.execute("SELECT ingredient_id, canonical_name, scientific_name, ncbi_taxon_id FROM ingredient").fetchall()
        self.ids = {r[0] for r in rows}
        self.name = {r[0]: r[1] for r in rows}
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
        self.manual_keys_pre = _manual_keys()
        arows = con.execute("SELECT ingredient_id, alias, lang, alias_type, source_id FROM ingredient_alias").fetchall()
        for iid, alias, lang, atype, src in arows:
            if not alias:
                continue
            rk = _rank(src, atype)
            a = unicodedata.normalize("NFKC", alias).lower().strip()
            src = "manual" if (src == "manual" and a in self.manual_keys_pre) else ("curated" if src == "manual" else src)
            self._put(self.exact, lang, a, rk, iid, src)
            self._put(self.keyn, lang, key_norm(alias), rk, iid, src)
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

    def _ret(self, hit, method, score):
        rk, iid, src = hit
        return (iid, "manual" if src == "manual" else method, score)

    def _by_text(self, text, lang, fuzzy):
        raw = unicodedata.normalize("NFKC", str(text)).lower().strip()
        if not raw:
            return None
        cjk = bool(CJK.search(raw))
        hit = self._lookup(self.exact, raw, lang, all_langs=True)
        if hit:
            return self._ret(hit, "exact", 1.0)
        k = key_norm(raw)
        hit = self._lookup(self.keyn, k, lang, all_langs=cjk)
        if hit:
            return self._ret(hit, "normalised", 0.95)
        if not cjk:
            ce = clean_en(raw)
            if ce and ce != raw:
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
                    cands.append(hit)
            if cands:
                return self._ret(cands[0], "normalised", round(0.6 + 0.3 * size / L, 2))
        return None

    def _cjk_sub(self, s, lang):
        L = len(s)
        minlen = 1 if L <= 3 else 2
        for size in range(L - 1, minlen - 1, -1):
            for i in range(L - size, -1, -1):  # prefer the right end (head noun in zh/ja)
                sub = s[i:i + size]
                if not CJK.search(sub):
                    continue
                hit = self._lookup(self.keyn, sub, lang, all_langs=True)
                # substrings only against curated / seed aliases: short katakana plant names from herb sources
                # ('チャ' tea, 'キビ' millet) and single characters ('酱', '桃') would match inside unrelated words
                if hit and hit[0][0] <= 4 and (size >= 2 or hit[2] in ("manual", "curated")):
                    return self._ret(hit, "normalised", round(0.6 + 0.3 * size / L, 2))
        return None

    def _fuzzy(self, q, lang):
        if not q or len(q) < 5:
            return None
        from rapidfuzz import fuzz, process
        lg = lang if lang in self.keyn else None
        if lg is None:
            return None
        if lg not in self.fuzzy_choices:
            keys = [k for k in self.keyn[lg] if len(k) >= 3]
            self.fuzzy_choices[lg] = keys
        keys = self.fuzzy_choices[lg]
        scorer = fuzz.ratio if CJK.search(q) else fuzz.token_sort_ratio
        m = process.extractOne(q, keys, scorer=scorer, score_cutoff=90)
        if not m:
            return None
        hit = self.keyn[lg][m[0]]
        return (hit[1], "fuzzy", round(m[1] / 100, 3))
