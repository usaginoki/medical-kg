"""ConditionResolver: map ids and free text to `condition.condition_id` (stage `conditions`).

Lookups are loaded from the DB once. All methods return a condition_id or None.

  by_mesh('D009325' | 'MESH:D009325' | 'MeSH:D009325')
  by_umls('C0027497')          # also CUIs recorded as xref aliases (HERB/SymMap merges)
  by_icd11('DD91.1')           # returns the 'ICD11:' id; follow same_as for the MEDIC/UMLS twin
  by_text(text, lang='en')     # exact normalised alias -> action map -> conservative fuzzy
  expand(condition_id)         # id + is_a descendants + same_as / tcm_maps_to / action_targets neighbours

Cross-reference ids that are not primary columns (extra UMLS CUIs, ICD-10, HPO, OMIM, DOID, SymMap ids) live in
`condition_alias` with lang='xref' and alias '<DB>:<id>' (e.g. 'UMLS:C0000729'); they are never used for text.
"""
import re, unicodedata

from common import norm_text

_CJK = re.compile(r"[぀-ヿ一-鿿가-힯]")
_BRIT = [("oedema", "edema"), ("oesoph", "esoph"), ("haem", "hem"), ("aemia", "emia"), ("tumour", "tumor"),
         ("paed", "ped"), ("oea", "ea"), ("ischaem", "ischem"), ("leukaem", "leukem"), ("anaesth", "anesth"),
         ("foetal", "fetal"), ("coeliac", "celiac"), ("orrhoea", "orrhea")]
_TAIL = re.compile(r"(,\s*(nos|unspecified|not elsewhere classified|other specified|nec))+\s*$")
VOCAB_RANK = {"medic": 0, "symmap": 1, "herb": 2, "icd11": 3, "action_map": 4, "free_text": 5}


def _singular(w):
    if w.endswith("ies") and len(w) > 4:
        return w[:-3] + "y"
    if w.endswith(("oes", "ches", "shes")):
        return w[:-2]
    if w.endswith("s") and not w.endswith(("ss", "us", "is")) and len(w) > 3:
        return w[:-1]
    return w


def _clean(t):
    t = t.replace("'s ", " ").replace("’s ", " ")
    t = re.sub(r"'s$", "", t)
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    words = t.split()
    if words:
        words[-1] = _singular(words[-1])
    return " ".join(words)


def cond_keys(text):
    """Normalised match keys for a condition string (1–2 keys: as written, and un-inverted MeSH form).

    CJK text uses common.norm_text. Latin text: NFKC, lowercase, British→American spelling, drop ', NOS' /
    ', unspecified', punctuation→space, singularise the last word (same rule as common.norm_text). Parenthesised
    words are kept as words. 'Diabetes Mellitus, Type 2' also yields 'type 2 diabetes mellitus'.
    """
    if text is None:
        return []
    t = unicodedata.normalize("NFKC", str(text)).strip()
    if not t:
        return []
    if _CJK.search(t):
        k = norm_text(t)
        return [k] if k else []
    t = t.lower()
    for a, b in _BRIT:
        t = t.replace(a, b)
    t = _TAIL.sub("", t)
    keys = []
    k = _clean(t)
    if k:
        keys.append(k)
    parts = [p.strip() for p in t.split(",")]
    if len(parts) == 2 and all(parts) and "(" not in t:
        k2 = _clean(parts[1] + " " + parts[0])
        if k2 and k2 not in keys:
            keys.append(k2)
    return keys


def cond_key(text):
    ks = cond_keys(text)
    return ks[0] if ks else ""


def action_key(text):
    """'Anti-inflammatory agents' / 'anti inflammatory' / 'Antiinflammatory' -> 'antiinflammatory'."""
    t = unicodedata.normalize("NFKC", str(text or "")).lower()
    t = re.sub(r"\[[^\]]*\]", " ", t)
    t = re.sub(r"\b(agents?|drugs?|activity|effects?|properties)\b", " ", t)
    t = re.sub(r"[^a-z0-9]", "", t)
    if t.endswith("s") and not t.endswith(("ss", "us", "is")) and len(t) > 4:
        t = t[:-1]
    return t


class ConditionResolver:
    def __init__(self, con):
        self.con = con
        rows = con.execute("SELECT condition_id, name, type, mesh_id, umls_cui, icd11, source_vocab FROM condition").fetchall()
        self.info = {r[0]: r for r in rows}
        rank = {r[0]: (VOCAB_RANK.get(r[6], 9), 0 if r[2] in ("symptom", "disease") else 1) for r in rows}
        self.mesh, self.umls, self.icd11 = {}, {}, {}
        for cid, _n, _t, mesh, cui, icd, _v in rows:
            if mesh:
                self._put(self.mesh, mesh.split(":")[-1].upper(), cid, rank)
            if cui:
                self._put(self.umls, cui.upper(), cid, rank)
            if icd and cid.startswith("ICD11:"):
                self.icd11[icd.upper()] = cid
        # xref aliases: extra CUIs / MeSH recorded on merged rows
        for cid, alias in con.execute("SELECT condition_id, alias FROM condition_alias WHERE lang='xref'").fetchall():
            db, _, x = alias.partition(":")
            if db == "UMLS":
                self._put(self.umls, x.upper(), cid, rank)
            elif db == "MESH":
                self._put(self.mesh, x.upper(), cid, rank)
        # text index: key -> best condition (vocab rank, primary name first, symptom/disease first)
        best = {}
        for cid, alias, is_name, src in con.execute("""
                SELECT a.condition_id, a.alias, a.alias = c.name, a.source_id FROM condition_alias a
                JOIN condition c USING (condition_id) WHERE a.lang <> 'xref' AND c.type <> 'action'""").fetchall():
            # curated synonyms (db/maps/condition_synonyms.csv) win, then MEDIC > SymMap > HERB > ICD-11
            score = (0 if src == "manual" else 1, rank[cid][0], 0 if is_name else 1, rank[cid][1], cid)
            for k in cond_keys(alias):
                if k not in best or score < best[k]:
                    best[k] = score
        # action index: every alias of an ACT: condition, keyed by action_key
        self.action = {}
        for cid, alias in con.execute("""SELECT a.condition_id, a.alias FROM condition_alias a JOIN condition c USING (condition_id)
                                          WHERE c.type = 'action' AND a.lang <> 'xref'""").fetchall():
            self.action.setdefault(action_key(alias), cid)
        # a curated action beats a non-MEDIC alias that happens to spell the same word (e.g. HERB 'Hemolytic')
        self.text = {k: v[-1] for k, v in best.items()
                     if not (action_key(k) in self.action and self.info[v[-1]][6] != "medic")}
        self.direction = {}
        self._load_direction_csv()
        self._fuzzy_keys = [k for k in self.text if len(k) >= 5 and not _CJK.search(k)]
        rel = con.execute("SELECT from_id, to_id, rel FROM condition_relation").fetchall()
        self.children, self.nbr_out, self.nbr_in = {}, {}, {}
        for f, t, r in rel:
            if r == "is_a":
                self.children.setdefault(t, []).append(f)
            else:
                self.nbr_out.setdefault((f, r), []).append(t)
                self.nbr_in.setdefault((t, r), []).append(f)

    @staticmethod
    def _put(d, k, cid, rank):
        if k not in d or rank[cid] < rank[d[k]]:
            d[k] = cid

    def _load_direction_csv(self):
        import csv, os
        from common import slug
        p = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "maps", "action_map.csv")
        if os.path.exists(p):
            for r in csv.DictReader(open(p)):
                self.direction[("ACT:" + slug(r["action"]), r["condition_id"])] = r["direction"]

    # ---- id lookups ---------------------------------------------------------------------------------------
    def by_mesh(self, mesh_id):
        if not mesh_id:
            return None
        return self.mesh.get(str(mesh_id).strip().split(":")[-1].upper())

    def by_umls(self, cui):
        if not cui:
            return None
        return self.umls.get(str(cui).strip().split(":")[-1].upper())

    def by_icd11(self, code):
        if not code:
            return None
        c = fix_icd11(str(code).strip().replace("ICD11:", "").replace("ICD-11:", "").strip())
        return self.icd11.get(c.upper()) if c else None

    # ---- text ---------------------------------------------------------------------------------------------
    def _variants(self, text):
        t = str(text).strip()
        out = [t]
        m = re.match(r"^\s*([^()]+?)\s*\(([^()]+)\)\s*$", t)  # Duke style 'Ache(Stomach)' -> 'Stomach ache', 'Stomachache'
        if m:
            head, inner = m.group(1), m.group(2)
            out += [f"{inner} {head}", f"{inner}{head}".replace(" ", ""), head if len(inner) < 3 else f"{inner} {head}"]
        if "/" in t:
            out += [p for p in t.split("/") if p.strip()]
        return out

    def by_text(self, text, lang="en"):
        if not text or not str(text).strip():
            return None
        variants = self._variants(text)
        for v in variants:  # 1. exact normalised alias
            for k in cond_keys(v):
                if k in self.text:
                    return self.text[k]
        for v in variants:  # 2. action map
            a = self.action.get(action_key(v))
            if a:
                return a
        if _CJK.search(str(text)):
            return None
        try:  # 3. conservative fuzzy
            from rapidfuzz import fuzz, process
        except ImportError:
            return None
        k = cond_key(variants[0])
        if len(k) < 5:
            return None
        hit = process.extractOne(k, self._fuzzy_keys, scorer=fuzz.ratio, score_cutoff=93)
        return self.text[hit[0]] if hit else None

    def by_text_scored(self, text, lang="en"):
        """Like by_text but returns (condition_id, match_method, score) | None."""
        if not text or not str(text).strip():
            return None
        variants = self._variants(text)
        for v in variants:
            for k in cond_keys(v):
                if k in self.text:
                    return self.text[k], "exact", 1.0
        for v in variants:
            a = self.action.get(action_key(v))
            if a:
                return a, "action_map", 1.0
        if _CJK.search(str(text)):
            return None
        from rapidfuzz import fuzz, process
        k = cond_key(variants[0])
        if len(k) < 5:
            return None
        hit = process.extractOne(k, self._fuzzy_keys, scorer=fuzz.ratio, score_cutoff=93)
        return (self.text[hit[0]], "fuzzy", hit[1] / 100) if hit else None

    # ---- graph --------------------------------------------------------------------------------------------
    def action_targets(self, act_id):
        return list(self.nbr_out.get((act_id, "action_targets"), []))

    def action_direction(self, act_id, target_id):
        """'beneficial' | 'harmful' | None, from db/maps/action_map.csv."""
        return self.direction.get((act_id, target_id))

    def descendants(self, cid):
        out, stack = set(), [cid]
        while stack:
            for c in self.children.get(stack.pop(), []):
                if c not in out:
                    out.add(c)
                    stack.append(c)
        return out

    def expand(self, condition_id):
        """The id, its is_a descendants, and one-hop same_as / tcm_maps_to / action_targets neighbours.

        For an ACT: id the action's targets (and their descendants) are included. For a condition, the ACT: ids
        that target it are included; their direction is given by action_direction().
        """
        if not condition_id:
            return set()
        seeds = {condition_id} | set(self.action_targets(condition_id))
        out = set(seeds)
        for s in seeds:
            out |= self.descendants(s)
        for c in list(out):
            for r in ("same_as", "tcm_maps_to"):
                out.update(self.nbr_out.get((c, r), []))
                out.update(self.nbr_in.get((c, r), []))
            out.update(self.nbr_in.get((c, "action_targets"), []))
        return out


_XLS = re.compile(r"^(\d)\.0+E\+(\d+)$", re.I)


def fix_icd11(code):
    """Undo Excel's scientific-notation mangling ('2.00E+86' -> '2E86'); drop 'N.A.'."""
    if code is None:
        return None
    c = str(code).strip()
    if c.upper() in ("", "NA", "N.A.", "N/A", "NAN"):
        return None
    m = _XLS.match(c)
    if m:
        c = f"{m.group(1)}E{m.group(2)}"
    return c
