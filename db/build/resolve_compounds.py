"""CompoundResolver: look up compound ids built by stage `compounds` (see db/README.md, *Contract between stages*).

All lookups return a `compound_id` or None. The index is loaded from the DB once:
  compound (inchikey, pubchem_cid, cas, chebi_id, mesh_id, name) and
  compound_xref: source ids (foodb, hmdb, npass, cmaup, imppat, phenol_explorer, ctd, flavordb, tmmc, herb, symmap)
  plus the lookup-only dbs written by the stage: pubchem, cas, chebi, synonym (all ids/names seen across members).
Nutrients go through db/maps/nutrient_map.csv (nutrient_key, source) -> mesh_id / compound_name.
"""
import csv, os, re, unicodedata
from collections import defaultdict

from common import DB_DIR, slug

NUTRIENT_MAP = os.path.join(DB_DIR, "maps", "nutrient_map.csv")

_GREEK = {"α": "alpha", "β": "beta", "γ": "gamma", "δ": "delta", "ε": "epsilon", "κ": "kappa", "ω": "omega",
          "μ": "mu", "ψ": "psi"}
_IK = re.compile(r"^[A-Z]{14}-[A-Z]{10}-[A-Z]$")


def chem_norm(text):
    """Normalise a chemical name for exact dictionary matching.

    NFKC, lowercase, Greek letters spelt out, then everything except [a-z0-9+] removed, so
    'beta-Carotene' == 'β carotene' == 'Beta Carotene' and '(-)-Epicatechin' == 'epicatechin'.
    """
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", str(text)).lower().strip()
    for g, r in _GREEK.items():
        t = t.replace(g, r)
    return re.sub(r"[^a-z0-9+]", "", t)


def norm_cid(x):
    if x is None:
        return None
    s = str(x).strip().upper()
    for p in ("CID:", "CID_", "CID"):
        if s.startswith(p):
            s = s[len(p):]
    s = s.strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s if s.isdigit() and int(s) > 0 else None


def norm_mesh(x):
    if x is None:
        return None
    s = str(x).strip()
    if not s:
        return None
    s = s.upper()
    if not s.startswith("MESH:"):
        s = "MESH:" + s
    return s


def valid_cas(s):
    """True if s looks like a CAS RN with a correct check digit."""
    if not s or not re.fullmatch(r"\d{2,7}-\d{2}-\d", s):
        return False
    digits = s.replace("-", "")
    body, check = digits[:-1], int(digits[-1])
    return sum(int(d) * (i + 1) for i, d in enumerate(reversed(body))) % 10 == check


class CompoundResolver:
    def __init__(self, con):
        self.con = con
        self._ik, self._cid, self._cas, self._mesh, self._chebi = {}, {}, {}, {}, {}
        self._xref = {}
        self._mesh_any = {}  # mesh -> compounds carrying it (the CTD chemical's own row + secondary matches)
        self._rank = {}  # compound_id -> (has mesh, n source xrefs) for tie-breaking
        n_src = defaultdict(int)
        rows = con.execute("SELECT compound_id, name, inchikey, pubchem_cid, cas, chebi_id, mesh_id FROM compound").fetchall()
        xrefs = con.execute("SELECT compound_id, db, xref_id FROM compound_xref").fetchall()
        for cid_, db, x in xrefs:
            if db not in ("synonym", "pubchem", "cas", "chebi", "ctd_match"):
                n_src[cid_] += 1
        for cid_, name, ik, pc, cas, chebi, mesh in rows:
            self._rank[cid_] = (mesh is not None, n_src.get(cid_, 0))
        # primary identifiers first (they win over secondary ones)
        self._names = defaultdict(set)      # norm name -> compounds whose primary name matches
        self._syn = defaultdict(set)        # norm name -> compounds with that synonym
        for cid_, name, ik, pc, cas, chebi, mesh in rows:
            if ik:
                self._ik.setdefault(ik, cid_)
            if pc is not None:
                self._put(self._cid, str(pc), cid_)
            if cas:
                self._put(self._cas, cas, cid_)
            if chebi:
                self._put(self._chebi, chebi, cid_)
            if mesh:
                self._mesh_any.setdefault(mesh, []).append(cid_)
            n = chem_norm(name)
            if n:
                self._names[n].add(cid_)
        sec_cid, sec_cas, sec_chebi = {}, {}, {}
        for cid_, db, x in xrefs:
            if db == "synonym":
                n = chem_norm(x)
                if n:
                    self._syn[n].add(cid_)
            elif db == "pubchem":
                self._put(sec_cid, x, cid_)
            elif db == "cas":
                self._put(sec_cas, x, cid_)
            elif db == "chebi":
                self._put(sec_chebi, x, cid_)
            elif db == "ctd":
                self._mesh[x] = cid_  # the compound that holds the CTD chemical itself
                self._xref[("ctd", x)] = cid_
            elif db != "ctd_match":
                self._xref.setdefault((db, x), cid_)
        for m, cs in self._mesh_any.items():
            if m not in self._mesh:
                self._mesh[m] = max(sorted(cs), key=lambda c: self._rank.get(c, (False, 0)))
        for prim, sec in ((self._cid, sec_cid), (self._cas, sec_cas), (self._chebi, sec_chebi)):
            for k, v in sec.items():
                prim.setdefault(k, v)
        self._nut = None

    def _put(self, d, key, cid_):
        """Keep the best-ranked compound for a secondary key."""
        cur = d.get(key)
        if cur is None or self._rank.get(cid_, (False, 0)) > self._rank.get(cur, (False, 0)):
            d[key] = cid_

    # -- lookups ---------------------------------------------------------------------------------
    def by_inchikey(self, ik):
        if not ik:
            return None
        ik = str(ik).strip().upper()
        if ik.startswith("INCHIKEY="):
            ik = ik[9:]
        return self._ik.get(ik)

    def by_cid(self, cid):
        c = norm_cid(cid)
        return self._cid.get(c) if c else None

    def by_cas(self, cas):
        return self._cas.get(str(cas).strip()) if cas else None

    def by_mesh(self, mesh):
        m = norm_mesh(mesh)
        return self._mesh.get(m) if m else None

    def all_by_mesh(self, mesh):
        """Every compound whose mesh_id is this MeSH id (CTD chemical row + secondary inchikey_skeleton/name matches)."""
        return list(self._mesh_any.get(norm_mesh(mesh), []))

    def by_chebi(self, chebi):
        if not chebi:
            return None
        s = str(chebi).strip().upper()
        if not s.startswith("CHEBI:"):
            s = "CHEBI:" + s
        return self._chebi.get(s)

    def by_name(self, name, strict=False):
        """Exact normalised name match (chem_norm) against primary names and synonyms.

        strict=True: a unique primary-name hit, else a unique synonym hit, else None.
        Default: if several compounds match, the one backed by most source records wins (a primary-name hit counts
        as one extra record; then MeSH id presence breaks ties), e.g. '6-gingerol' -> the InChIKey compound shared by
        CMAUP/NPASS/IMPPAT/TM-MC/HERB/SymMap rather than a single-source record that happens to be named '[6]-Gingerol'.
        """
        n = chem_norm(name)
        if len(n) < 2:
            return None
        prim, syn = self._names.get(n, set()), self._syn.get(n, set())
        if strict:
            for hits in (prim, syn):
                if hits:
                    return next(iter(hits)) if len(hits) == 1 else None
            return None
        hits = prim | syn
        if not hits:
            return None

        def key(c):
            has_mesh, n_src = self._rank.get(c, (False, 0))
            return (n_src + (1 if c in prim else 0), c in prim, has_mesh)
        return max(sorted(hits), key=key)

    def by_xref(self, db, xref_id):
        if xref_id is None:
            return None
        x = str(xref_id).strip()
        if db == "ctd":
            return self.by_mesh(x)
        if db in ("pubchem", "flavordb"):
            c = norm_cid(x)
            return self._xref.get((db, c)) or (self.by_cid(c) if db == "pubchem" else None)
        if db == "chebi":
            return self.by_chebi(x)
        if db == "cas":
            return self.by_cas(x)
        return self._xref.get((db, x))

    def nutrient(self, nutrient_key, source):
        """nutrient_map.csv (nutrient_key, source) -> compound_id, None for non-compounds (energy, water, ash...)."""
        if self._nut is None:
            self._nut = {}
            with open(NUTRIENT_MAP, newline="", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    self._nut[(r["nutrient_key"], r["source"])] = (r["mesh_id"], r["compound_name"])
        hit = self._nut.get((str(nutrient_key), source))
        if not hit:
            return None
        mesh, cname = hit
        if mesh:
            return self.by_mesh(mesh)
        if cname:
            cid_ = "NAME:" + slug(cname)
            return cid_ if cid_ in self._rank else None
        return None
