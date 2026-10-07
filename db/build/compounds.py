"""Stage `compounds`: one merged compound table + compound_xref.

Sources (candidates): CTD (chemicals in the curated chemical–disease file + nutrient MeSH ids), FooDB (compounds in
Content or CompoundsHealthEffect), HMDB (disease-linked or FooDB-linked metabolites), CMAUP (all ingredients),
NPASS (compounds of CMAUP plants / FooDB food taxa), Phenol-Explorer, FlavorDB2, IMPPAT, TM-MC, HERB and SymMap
(herb-linked ingredients), plus nutrient concepts from db/maps/nutrient_map.csv.

Merge (union–find over candidates), in priority order:
  1. same InChIKey (always merged);
  2. same PubChem CID, unless the two clusters carry different InChIKeys;
  3. explicit cross-source ids (HMDB.foodb_id / FlavorDB.fooddb_id -> FooDB public id, NPASS = CMAUP np_id,
     HERB.NPASS_id, HMDB.phenol_explorer_compound_id), unless InChIKey or CID conflict;
  4. same (check-digit-valid) CAS RN, unless InChIKey or CID conflict;
  5. CTD chemicals still unlinked: exact normalised name/synonym (unique on both sides) against the primary names
     of the other sources.
compound_id = IK:<InChIKey> | CID:<cid> | MESH:<id> | CAS:<cas> | NAME:<slug>, first available.

compound_xref dbs: source ids (foodb [FDB public id AND numeric Compound.id], hmdb, npass, cmaup, imppat,
phenol_explorer, ctd ['MESH:…'], flavordb [pubchem id], tmmc, herb, symmap), ctd_match (how the chosen mesh_id
was reached: inchikey | cid | xref | cas | name), and lookup-only dbs pubchem / cas / chebi / synonym.
"""
import csv, os, re, time
from collections import defaultdict

import pandas as pd

from common import data, DB_DIR, slug
from build.resolve_compounds import chem_norm, norm_cid, valid_cas, _IK

# source priority for choosing a field value inside a merged cluster
PRIO_CID = ["hmdb", "ctd", "phenol_explorer", "flavordb", "imppat", "tmmc", "cmaup", "npass", "herb", "symmap", "foodb", "nutrient"]
PRIO_CAS = ["ctd", "hmdb", "foodb", "phenol_explorer", "flavordb", "herb", "symmap", "imppat", "tmmc", "cmaup", "npass", "nutrient"]
PRIO_CHEBI = ["hmdb", "foodb", "imppat", "phenol_explorer", "ctd"]
PRIO_NAME = ["nutrient", "hmdb", "ctd", "phenol_explorer", "foodb", "flavordb", "imppat", "cmaup", "npass", "herb", "symmap", "tmmc"]
PRIO_IK = ["hmdb", "foodb", "ctd", "cmaup", "npass", "imppat", "tmmc", "herb", "phenol_explorer", "flavordb", "symmap"]
SOURCE_DBS = ["ctd", "foodb", "hmdb", "cmaup", "npass", "phenol_explorer", "flavordb", "imppat", "tmmc", "herb", "symmap"]

COLS = ["db", "xref_id", "name", "ik", "cid", "cas", "chebi", "mesh"]


def _log(msg):
    print(f"  [compounds] {msg}", flush=True)


def _s(x):
    if x is None:
        return None
    if isinstance(x, float) and x != x:
        return None
    s = str(x).strip()
    return None if s in ("", "n.a.", "NA", "nan", "None", "NULL", "-") else s


def _ik(x):
    s = _s(x)
    if not s:
        return None
    s = s.upper()
    if s.startswith("INCHIKEY="):
        s = s[9:]
    return s if _IK.match(s) else None


def _cas_list(x):
    s = _s(x)
    if not s:
        return []
    return [c for c in re.split(r"[|;,\s]+", s) if valid_cas(c)]


def _chebi(x):
    s = _s(x)
    if not s:
        return None
    s = s.upper()
    if s.endswith(".0"):
        s = s[:-2]
    if s.isdigit():
        s = "CHEBI:" + s
    return s if re.fullmatch(r"CHEBI:\d+", s) else None


def _name(x):
    s = _s(x)
    if not s or _IK.match(s):  # CMAUP/NPASS use the InChIKey as pref_name when there is no name
        return None
    return s


class Cands:
    """Accumulates candidate records, explicit link keys, extra ids and synonyms."""

    def __init__(self):
        self.rows, self.keys, self.extra, self.syn, self.alt_cas = [], [], [], [], []

    def add(self, db, xref_id, name=None, ik=None, cid=None, cas=None, chebi=None, mesh=None,
            keys=(), extra=(), syns=()):
        i = len(self.rows)
        cas_l = _cas_list(cas) if not isinstance(cas, list) else cas
        self.rows.append((db, str(xref_id), _name(name), _ik(ik), norm_cid(_s(cid)),
                          cas_l[0] if cas_l else None, _chebi(chebi), mesh))
        for c in cas_l[1:]:
            self.alt_cas.append((i, c))
        for k in keys:
            if k:
                self.keys.append((i, k))
        for e in extra:
            self.extra.append((i,) + tuple(e))
        for s in syns:
            s = _s(s)
            if s and len(s) < 300:
                self.syn.append((i, s))
        return i


# --------------------------------------------------------------------------------------- loaders
def load_ctd(con, C, nutrient_mesh):
    cur = con.execute("SELECT DISTINCT 'MESH:' || ChemicalID FROM read_csv(?, delim='\t', all_varchar=true, quote='')",
                      [data("ctd", "CTD_chemicals_diseases_curated.tsv")]).fetchall()
    keep = {r[0] for r in cur} | set(nutrient_mesh)
    df = con.execute("""SELECT ChemicalName, ChemicalID, CasRN, PubChemCID, InChIKey, MESHSynonyms, CTDCuratedSynonyms
                        FROM read_csv(?, delim='\t', all_varchar=true, quote='')""",
                     [data("ctd", "CTD_chemicals.tsv")]).df()
    # CTD-wide name index (all 179k chemicals) for the uniqueness check of name matching
    ctd_names = defaultdict(set)
    for name, mid, s1, s2 in zip(df.ChemicalName, df.ChemicalID, df.MESHSynonyms, df.CTDCuratedSynonyms):
        for s in [name] + (s1.split("|") if isinstance(s1, str) else []) + (s2.split("|") if isinstance(s2, str) else []):
            n = chem_norm(s)
            if len(n) >= 4:
                ctd_names[n].add(mid)
    sub = df[df.ChemicalID.isin(keep)]
    idx = {}
    for r in sub.itertuples(index=False):
        syns = (r.MESHSynonyms.split("|") if isinstance(r.MESHSynonyms, str) else []) + \
               (r.CTDCuratedSynonyms.split("|") if isinstance(r.CTDCuratedSynonyms, str) else [])
        idx[C.add("ctd", r.ChemicalID, r.ChemicalName, r.InChIKey, r.PubChemCID, r.CasRN, None, r.ChemicalID,
                  syns=syns[:50])] = [r.ChemicalName] + syns
    _log(f"CTD: {len(sub)} chemicals ({len(cur)} curated ids)")
    return ctd_names, idx


def load_foodb(con, C):
    t = time.time()
    content_ids = {r[0] for r in con.execute(
        "SELECT DISTINCT source_id FROM read_csv(?, all_varchar=true) WHERE source_type='Compound'",
        [data("foodb", "Content.csv")]).fetchall()}
    he_ids = {r[0] for r in con.execute(
        "SELECT DISTINCT compound_id FROM read_csv(?, all_varchar=true)", [data("foodb", "CompoundsHealthEffect.csv")]).fetchall()}
    want = content_ids | he_ids
    cols = ["id", "public_id", "name", "state", "annotation_quality", "description", "cas_number", "moldb_smiles",
            "moldb_inchi", "moldb_mono_mass", "moldb_inchikey", "moldb_iupac", "kingdom", "superklass", "klass", "subklass"]
    comp = pd.read_csv(data("foodb", "Compound.csv"), header=None, skiprows=1, names=cols, dtype=str,
                       usecols=[0, 1, 2, 6, 10], keep_default_na=False)
    comp = comp[comp.id.isin(want)]
    ext = pd.read_csv(data("foodb", "CompoundExternalDescriptor.csv"), dtype=str, usecols=["external_id", "compound_id"])
    chebi = ext[ext.external_id.str.match(r"^CHEBI:\d+$", na=False)].drop_duplicates("compound_id") \
        .set_index("compound_id").external_id.to_dict()
    syn = pd.read_csv(data("foodb", "CompoundSynonym.csv"), dtype=str, usecols=["synonym", "source_id", "source_type"])
    syn = syn[(syn.source_type == "Compound") & syn.source_id.isin(set(comp.id))]
    syns = syn.groupby("source_id").synonym.apply(list).to_dict()
    for r in comp.itertuples(index=False):
        C.add("foodb", r.public_id, r.name, r.moldb_inchikey, None, r.cas_number, chebi.get(r.id), None,
              keys=["FDB:" + r.public_id], extra=[("foodb", r.id)], syns=syns.get(r.id, [])[:50])
    _log(f"FooDB: {len(comp)} compounds (Content ids {len(content_ids)}, health-effect ids {len(he_ids)}) {time.time()-t:.1f}s")
    return content_ids


def load_hmdb(con, C):
    if not os.path.exists(data("hmdb", "hmdb_metabolites.csv")):
        _log("HMDB: files missing (Data/hmdb/), skipped")
        return
    df = con.execute("""SELECT accession, name, cas_registry_number, inchikey, pubchem_compound_id, chebi_id, foodb_id,
                               phenol_explorer_compound_id
                        FROM read_csv(?, all_varchar=true)
                        WHERE foodb_id IS NOT NULL
                           OR accession IN (SELECT accession FROM read_csv(?, all_varchar=true))""",
                     [data("hmdb", "hmdb_metabolites.csv"), data("hmdb", "hmdb_metabolite_diseases.csv")]).df()
    for r in df.itertuples(index=False):
        C.add("hmdb", r.accession, r.name, r.inchikey, r.pubchem_compound_id, r.cas_registry_number, r.chebi_id, None,
              keys=[("FDB:" + r.foodb_id) if _s(r.foodb_id) else None,
                    ("PE:" + r.phenol_explorer_compound_id) if _s(r.phenol_explorer_compound_id) else None])
    _log(f"HMDB: {len(df)} metabolites")


def load_cmaup_npass(con, C):
    cm = con.execute("""SELECT np_id, coalesce(CASE WHEN pref_name NOT SIMILAR TO '[A-Z]{14}-[A-Z]{10}-[A-Z]' THEN pref_name END,
                                              NULLIF(iupac_name, 'n.a.')) AS pref_name, pubchem_cid, InChIKey FROM read_csv(?, delim='\t', all_varchar=true, quote='')""",
                     [data("cmaup", "CMAUPv2.0_download_Ingredients_All.txt")]).df()
    for r in cm.itertuples(index=False):
        C.add("cmaup", r.np_id, r.pref_name, r.InChIKey, r.pubchem_cid, keys=["NPC:" + r.np_id])
    np_ = con.execute("""
        WITH cp AS (SELECT * FROM read_csv(?, delim='\t', all_varchar=true, quote='')),
             fd AS (SELECT DISTINCT CAST(ncbi_taxonomy_id AS VARCHAR) tax FROM read_csv(?, all_varchar=true)
                    WHERE ncbi_taxonomy_id IS NOT NULL),
             si AS (SELECT * FROM read_csv(?, delim='\t', all_varchar=true, quote='')),
             orgs AS (SELECT org_id FROM si
                      WHERE org_id IN (SELECT Plant_ID FROM cp)
                         OR species_tax_id IN (SELECT Species_Tax_ID FROM cp WHERE Species_Tax_ID <> 'NA')
                         OR org_tax_id IN (SELECT tax FROM fd) OR species_tax_id IN (SELECT tax FROM fd)),
             nps AS (SELECT DISTINCT np_id FROM read_csv(?, delim='\t', all_varchar=true, quote='')
                     WHERE org_id IN (SELECT org_id FROM orgs))
        SELECT g.np_id, coalesce(CASE WHEN g.pref_name NOT SIMILAR TO '[A-Z]{14}-[A-Z]{10}-[A-Z]' THEN g.pref_name END,
                                 NULLIF(g.iupac_name, 'n.a.')) AS pref_name, g.pubchem_id, g.inchikey
        FROM read_csv(?, delim='\t', all_varchar=true, quote='', null_padding=true) g JOIN nps USING (np_id)""",
                      [data("cmaup", "CMAUPv2.0_download_Plants.txt"), data("foodb", "Food.csv"),
                       data("npass", "NPASS3.0_species_info.txt"), data("npass", "NPASS3.0_naturalproducts_species_pair.txt"),
                       data("npass", "NPASS3.0_naturalproducts_generalinfo.txt")]).df()
    for r in np_.itertuples(index=False):
        C.add("npass", r.np_id, r.pref_name, r.inchikey, r.pubchem_id, keys=["NPC:" + r.np_id])
    _log(f"CMAUP: {len(cm)} ingredients; NPASS: {len(np_)} products of CMAUP plants / FooDB food taxa")


def load_small(con, C):
    pe = pd.read_csv(data("phenol-explorer", "compounds.csv"), dtype=str, keep_default_na=False)
    for r in pe.itertuples(index=False):
        C.add("phenol_explorer", r.id, r.name, None, r.pubchem_compound_id, r.cas_number, r.chebi_id,
              keys=["PE:" + r.id], syns=[s.strip() for s in r.synonyms.split(";")] if r.synonyms else [])
    fl = pd.read_csv(data("flavordb2", "molecules.csv"), dtype=str, keep_default_na=False,
                     usecols=["pubchem_id", "common_name", "cas_id", "fooddb_id"])
    for r in fl.itertuples(index=False):
        fdb = _s(r.fooddb_id)
        C.add("flavordb", norm_cid(r.pubchem_id) or r.pubchem_id, r.common_name, None, r.pubchem_id, r.cas_id,
              keys=["FDB:" + fdb] if fdb and fdb.startswith("FDB") else [])
    im = pd.read_csv(data("imppat", "Chemical_Information_IMPPAT_Phytochemicals.tsv"), sep="\t", dtype=str,
                     keep_default_na=False, quoting=csv.QUOTE_NONE,
                     usecols=["IMPPAT_Phytochemical_identifier", "Phytochemical name_standardised",
                              "Synonymous chemical names", "Pubchem_CID", "ChEBI", "InChIKey"])
    im.columns = ["pid", "name", "syn", "cid", "chebi", "ik"]
    for r in im.itertuples(index=False):
        C.add("imppat", r.pid, r.name, r.ik, r.cid, None, r.chebi, syns=list(dict.fromkeys(r.syn.split("|")))[:30])
    _log(f"Phenol-Explorer {len(pe)}, FlavorDB {len(fl)}, IMPPAT {len(im)}")

    # TM-MC: every chemical_property ID is linked to a medicinal material in medicinal_compound
    tp = pd.read_excel(data("tm-mc", "chemical_property.xlsx"), usecols=["ID", "INCHIKEY", "CID"], dtype=str)
    mc = pd.read_excel(data("tm-mc", "medicinal_compound.xlsx"), usecols=["ID", "COMPOUND"], dtype=str)
    linked = set(mc.ID)
    names = mc.drop_duplicates(["ID", "COMPOUND"]).groupby("ID").COMPOUND.apply(list).to_dict()
    tp = tp[tp.ID.isin(linked)]
    for r in tp.itertuples(index=False):
        nm = names.get(r.ID, [])
        C.add("tmmc", r.ID, nm[0] if nm else None, r.INCHIKEY, r.CID, syns=nm[1:20])
    # HERB: ingredients linked to herbs (only the scraped herb→ingredient table exists locally)
    hi = pd.read_csv(data("herb", "scrape", "herb_ingredient.csv"), dtype=str)
    hl = set(hi["Ingredient id"])
    he = pd.read_csv(data("herb", "HERB_ingredient_info_v2.txt"), sep="\t", dtype=str, quoting=csv.QUOTE_NONE,
                     keep_default_na=False, usecols=["Ingredient_id", "Ingredient_name", "InChIKey", "CAS_id", "PubChem_id", "NPASS_id"])
    he = he[he.Ingredient_id.isin(hl)]
    for r in he.itertuples(index=False):
        np_ = _s(r.NPASS_id)
        C.add("herb", r.Ingredient_id, r.Ingredient_name, r.InChIKey, r.PubChem_id, r.CAS_id,
              keys=["NPC:" + np_] if np_ and np_.startswith("NPC") else [])
    # SymMap: SMIT ingredients linked to herbs (scraped herb→ingredient relations)
    sm = pd.read_csv(data("symmap", "scrape", "herb_ingredient_relations.csv"), dtype=str, keep_default_na=False)
    sm = sm.drop_duplicates("MOL_id")
    for r in sm.itertuples(index=False):
        C.add("symmap", r.MOL_id, r.Molecule_name, None, r.PubChem_CID, r.CAS_id)
    _log(f"TM-MC {len(tp)}, HERB {len(he)} (of {len(hl)} linked), SymMap {len(sm)}")


def load_nutrients(C, have_mesh):
    """Nutrient concepts not already present as CTD chemicals (e.g. Dietary Proteins, omega-9)."""
    nm = pd.read_csv(os.path.join(DB_DIR, "maps", "nutrient_map.csv"), dtype=str, keep_default_na=False)
    mesh_set, extra = set(nm.mesh_id[nm.mesh_id != ""]), []
    seen = set()
    for r in nm.itertuples(index=False):
        key = r.mesh_id or ("NAME:" + slug(r.compound_name) if r.compound_name else None)
        if not key or key in seen:
            continue
        seen.add(key)
        if r.mesh_id and r.mesh_id in have_mesh:
            continue
        extra.append(C.add("nutrient", key, r.compound_name, mesh=r.mesh_id or None))
    return mesh_set, extra


# ----------------------------------------------------------------------------------------- merge
class UF:
    def __init__(self, rows):
        n = len(rows)
        self.p = list(range(n))
        self.ik = [{r[3]} if r[3] else set() for r in rows]
        self.cid = [{r[4]} if r[4] else set() for r in rows]
        self.has_ctd = [r[0] == "ctd" for r in rows]
        self.has_other = [r[0] not in ("ctd", "nutrient") for r in rows]

    def find(self, a):
        p = self.p
        while p[a] != a:
            p[a] = p[p[a]]
            a = p[a]
        return a

    def compatible(self, a, b, check_cid=True):
        if self.ik[a] and self.ik[b] and not (self.ik[a] & self.ik[b]):
            return False
        if check_cid and self.cid[a] and self.cid[b] and not (self.cid[a] & self.cid[b]):
            return False
        return True

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a == b:
            return a
        if a > b:
            a, b = b, a
        self.p[b] = a
        self.ik[a] |= self.ik[b]
        self.cid[a] |= self.cid[b]
        self.has_ctd[a] = self.has_ctd[a] or self.has_ctd[b]
        self.has_other[a] = self.has_other[a] or self.has_other[b]
        return a

    def group_merge(self, members, force=False, check_cid=True):
        roots = []
        for m in members:
            r = self.find(m)
            if r in roots:
                continue
            for i, q in enumerate(roots):
                q = self.find(q)
                if force or self.compatible(q, r, check_cid):
                    roots[i] = self.union(q, r)
                    break
            else:
                roots.append(r)


def merge(C, ctd_names, ctd_syns):
    rows = C.rows
    uf = UF(rows)
    prio = {d: i for i, d in enumerate(SOURCE_DBS + ["nutrient"])}
    order = sorted(range(len(rows)), key=lambda i: prio[rows[i][0]])

    def groups(col):
        g = defaultdict(list)
        for i in order:
            v = rows[i][col]
            if v:
                g[v].append(i)
        return g

    how = {}  # candidate index -> merge step through which it joined (for CTD members)
    for step, col, kw in (("inchikey", 3, dict(force=True)), ("cid", 4, dict(check_cid=False))):
        for mem in groups(col).values():
            if len(mem) > 1:
                uf.group_merge(mem, **kw)
    kg = defaultdict(list)
    for i, k in sorted(C.keys, key=lambda x: prio[rows[x[0]][0]]):
        kg[k].append(i)
    for mem in kg.values():
        if len(mem) > 1:
            uf.group_merge(mem)
    for mem in groups(5).values():
        if len(mem) > 1:
            uf.group_merge(mem)
    # step 5: CTD chemicals still alone → unique exact name/synonym match against other sources' primary names
    target = defaultdict(set)
    for i, r in enumerate(rows):
        if r[0] not in ("ctd", "nutrient") and r[2]:
            n = chem_norm(r[2])
            if len(n) >= 4:
                target[n].add(i)
    n_name = 0
    for i, names in ctd_syns.items():
        ri = uf.find(i)
        if uf.has_other[ri]:
            continue
        for nm in names:
            n = chem_norm(nm)
            if len(n) < 4 or len(ctd_names.get(n, ())) != 1:
                continue
            roots = {uf.find(j) for j in target.get(n, ())}
            if len(roots) != 1:
                continue
            rt = roots.pop()
            if uf.has_ctd[rt] or not uf.compatible(rt, ri):
                continue
            uf.union(rt, ri)
            how[i] = "name"
            n_name += 1
            break
    _log(f"name-matched CTD chemicals: {n_name}")
    root = [uf.find(i) for i in range(len(rows))]
    return root, how


def build(con):
    t0 = time.time()
    C = Cands()
    nm = pd.read_csv(os.path.join(DB_DIR, "maps", "nutrient_map.csv"), dtype=str, keep_default_na=False)
    nutrient_mesh = set(nm.mesh_id[nm.mesh_id != ""])
    ctd_names, ctd_syns = load_ctd(con, C, nutrient_mesh)
    content_ids = load_foodb(con, C)
    load_hmdb(con, C)
    load_cmaup_npass(con, C)
    load_small(con, C)
    have_mesh = {r[7] for r in C.rows if r[0] == "ctd"}
    _, nut_idx = load_nutrients(C, have_mesh)
    _log(f"{len(C.rows)} candidates loaded in {time.time()-t0:.1f}s")

    root, how = merge(C, ctd_names, ctd_syns)
    cand = pd.DataFrame(C.rows, columns=COLS)
    cand["root"] = root
    cand["i"] = range(len(cand))

    def pick(col, prio_list, df=cand):
        p = {d: i for i, d in enumerate(prio_list)}
        s = df[df[col].notna()].copy()
        s["_p"] = s.db.map(lambda d: p.get(d, 99))
        return s.sort_values(["_p", "i"]).drop_duplicates("root").set_index("root")[col]

    agg = pd.DataFrame(index=pd.Index(sorted(set(root)), name="root"))
    agg["inchikey"] = pick("ik", PRIO_IK)
    agg["cid"] = pick("cid", PRIO_CID)
    agg["cas"] = pick("cas", PRIO_CAS)
    agg["chebi"] = pick("chebi", PRIO_CHEBI)
    # name: the normalised name most members agree on (FooDB has some mislabelled records), ties by source priority
    pn = {d: i for i, d in enumerate(PRIO_NAME)}
    nm_ = cand[cand.name.notna()][["root", "db", "name", "i"]].copy()
    nm_["_n"] = nm_.name.map(chem_norm)
    nm_["_p"] = nm_.db.map(lambda d: pn.get(d, 99))
    nm_["_c"] = nm_.groupby(["root", "_n"]).i.transform("size")
    nm_["_nut"] = nm_.db != "nutrient"
    agg["name"] = nm_.sort_values(["root", "_nut", "_c", "_p", "i"], ascending=[True, True, False, True, True]) \
        .drop_duplicates("root").set_index("root").name

    # mesh: choose among CTD members by how they joined, then D-descriptor over C-supplementary
    ctd = cand[cand.db.isin(["ctd", "nutrient"]) & cand.mesh.notna()].copy()
    ik_of, cid_of = agg.inchikey.to_dict(), agg.cid.to_dict()
    multi = cand.groupby("root").db.agg(lambda s: bool(set(s) - {"ctd", "nutrient"}))

    oc = cand[~cand.db.isin(["ctd", "nutrient"]) & cand.cas.notna()]
    other_cas = set(zip(oc.root, oc.cas))

    def method(r):
        if r.i in how:
            return how[r.i]
        if not multi.get(r.root):
            return "self"
        if r.ik and r.ik == ik_of.get(r.root):
            return "inchikey"
        if r.cid and r.cid == cid_of.get(r.root):
            return "cid"
        if r.cas and (r.root, r.cas) in other_cas:
            return "cas"
        return "xref"
    rank = {"self": 0, "inchikey": 1, "cid": 2, "xref": 3, "cas": 4, "name": 5}
    ctd["method"] = [method(r) for r in ctd.itertuples(index=False)]
    ctd["_r"] = ctd.method.map(rank)
    ctd["_d"] = ~ctd.mesh.str.startswith("MESH:D")
    best = ctd.sort_values(["_r", "_d", "i"]).drop_duplicates("root").set_index("root")
    agg["mesh"] = best.mesh
    agg["mesh_method"] = best.method
    # Secondary CTD linkage (no merge; the CTD chemical keeps its own compound row). For compounds still without a
    # mesh_id: (a) same InChIKey skeleton (first block = connectivity; stereo/charge variants) as exactly one loaded CTD
    # chemical, (b) a member's primary name equals a CTD name/synonym that is unique across all of CTD.
    loaded = cand[cand.db == "ctd"]
    skel = defaultdict(set)
    for ik, m in zip(loaded.ik, loaded.mesh):
        if isinstance(ik, str):
            skel[ik[:14]].add(m)
    loaded_mesh = set(loaded.mesh)
    sec_mesh, sec_how = {}, {}
    for r, ik in agg.inchikey[agg.mesh.isna() & agg.inchikey.notna()].items():
        ms = skel.get(ik[:14], ())
        if len(ms) == 1:
            sec_mesh[r], sec_how[r] = next(iter(ms)), "inchikey_skeleton"
    nomesh = set(agg.index[agg.mesh.isna()]) - set(sec_mesh)
    pn = {d: i for i, d in enumerate(PRIO_NAME)}
    sub = cand[cand.root.isin(nomesh) & cand.name.notna() & (cand.db != "nutrient")]
    sub = sub.assign(_p=sub.db.map(lambda d: pn.get(d, 99))).sort_values(["_p", "i"])
    for r, nm_ in zip(sub.root, sub.name):
        if r in sec_mesh:
            continue
        n = chem_norm(nm_)
        ms = ctd_names.get(n, ()) if len(n) >= 4 else ()
        if len(ms) == 1:
            m = next(iter(ms))
            if m in loaded_mesh:
                sec_mesh[r], sec_how[r] = m, "name"
    agg.loc[list(sec_mesh), "mesh"] = pd.Series(sec_mesh)
    agg.loc[list(sec_how), "mesh_method"] = pd.Series(sec_how)
    _log(f"secondary CTD linkage: {pd.Series(sec_how).value_counts().to_dict()}")
    # compound_id must not use a MESH id that belongs to the CTD chemical's own row
    agg["mesh_primary"] = agg.mesh.where(~agg.index.isin(list(sec_mesh)))

    nut_roots = {root[i] for i in nut_idx} | set(cand.root[cand.mesh.isin(nutrient_mesh)])
    agg["is_nutrient"] = agg.index.isin(nut_roots)

    def cid_of_row(r):
        if isinstance(r.inchikey, str):
            return "IK:" + r.inchikey
        if isinstance(r.cid, str):
            return "CID:" + r.cid
        if isinstance(r.mesh_primary, str):
            return r.mesh_primary
        if isinstance(r.cas, str):
            return "CAS:" + r.cas
        s = slug(r.name) if isinstance(r.name, str) else ""
        return "NAME:" + s if s else None
    agg["compound_id"] = [cid_of_row(r) for r in agg.itertuples()]
    # fallbacks for clusters with no usable name
    miss = agg.compound_id.isna()
    if miss.any():
        first = cand.drop_duplicates("root").set_index("root")
        agg.loc[miss, "compound_id"] = ["NAME:" + slug(f"{first.db[r]}-{first.xref_id[r]}") for r in agg.index[miss]]
    cand["compound_id"] = cand.root.map(agg.compound_id)

    comp = agg.reset_index().drop_duplicates("compound_id")
    comp["pubchem_cid"] = pd.to_numeric(comp.cid, errors="coerce").astype("Int64")
    comp = comp[["compound_id", "name", "inchikey", "pubchem_cid", "cas", "chebi", "mesh", "is_nutrient"]]
    comp.columns = ["compound_id", "name", "inchikey", "pubchem_cid", "cas", "chebi_id", "mesh_id", "is_nutrient"]
    # a compound_id collision (rare: different clusters, same NAME/CAS id) keeps one row; flags/ids OR-ed
    nutr = agg.groupby("compound_id").is_nutrient.any()
    comp["is_nutrient"] = comp.compound_id.map(nutr)

    # xrefs ----------------------------------------------------------------------------------------
    cid_by_i = cand.compound_id.values
    x = [(cid_by_i[r.i], r.db, r.xref_id) for r in cand.itertuples(index=False) if r.db != "nutrient"]
    x += [(cid_by_i[i], db, xid) for i, db, xid in C.extra]
    x += [(cid_by_i[r.i], "pubchem", r.cid) for r in cand.itertuples(index=False) if r.cid]
    x += [(cid_by_i[r.i], "cas", r.cas) for r in cand.itertuples(index=False) if r.cas]
    x += [(cid_by_i[i], "cas", c) for i, c in C.alt_cas]
    x += [(cid_by_i[r.i], "chebi", r.chebi) for r in cand.itertuples(index=False) if r.chebi]
    x += [(cid_by_i[r.i], "synonym", r.name) for r in cand.itertuples(index=False) if r.name]
    x += [(cid_by_i[i], "synonym", s) for i, s in C.syn]
    mm = agg[agg.mesh_method.notna() & (agg.mesh_method != "self")]
    x += [(c, "ctd_match", m) for c, m in zip(mm.compound_id, mm.mesh_method)]
    xref = pd.DataFrame(x, columns=["compound_id", "db", "xref_id"]).dropna().drop_duplicates()

    con.execute("DELETE FROM compound_xref")
    con.execute("DELETE FROM compound")
    con.register("comp_df", comp)
    con.execute("INSERT INTO compound SELECT * FROM comp_df")
    con.register("xref_df", xref)
    con.execute("INSERT INTO compound_xref SELECT * FROM xref_df")
    con.unregister("comp_df")
    con.unregister("xref_df")
    _log(f"compound {len(comp)} rows, compound_xref {len(xref)} rows ({time.time()-t0:.1f}s)")
    report(con, content_ids)


def report(con, content_ids=None):
    q = lambda s: con.execute(s).fetchall()
    _log("ids: " + ", ".join(f"{k}={v}" for k, v in q(
        "SELECT split_part(compound_id, ':', 1), count(*) FROM compound GROUP BY 1 ORDER BY 2 DESC")))
    _log("xrefs: " + ", ".join(f"{k}={v}" for k, v in q(
        "SELECT db, count(*) FROM compound_xref GROUP BY 1 ORDER BY 2 DESC")))
    _log("with mesh_id: " + str(q("SELECT count(mesh_id), count(*) FILTER (WHERE is_nutrient) FROM compound")[0]))
    for db, n, m in q("""SELECT x.db, count(DISTINCT x.xref_id), count(DISTINCT x.xref_id) FILTER (WHERE c.mesh_id IS NOT NULL)
                         FROM compound_xref x JOIN compound c USING (compound_id)
                         WHERE x.db IN ('foodb','hmdb','phenol_explorer','cmaup','npass','flavordb','imppat','tmmc','herb','symmap')
                           AND NOT (x.db = 'foodb' AND x.xref_id NOT LIKE 'FDB%')
                         GROUP BY 1 ORDER BY 1"""):
        _log(f"CTD-joinable {db}: {m}/{n} = {m / n:.1%}")
    _log("ctd_match: " + ", ".join(f"{k}={v}" for k, v in q(
        "SELECT xref_id, count(*) FROM compound_xref WHERE db='ctd_match' GROUP BY 1 ORDER BY 2 DESC")))
    if content_ids:
        got = {r[0] for r in q("SELECT xref_id FROM compound_xref WHERE db='foodb' AND xref_id NOT LIKE 'FDB%'")}
        _log(f"FooDB Content compound ids resolved: {len(content_ids & got)}/{len(content_ids)} "
             f"= {len(content_ids & got) / len(content_ids):.1%}")
