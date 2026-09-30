"""Stage `conditions`: condition, condition_alias, condition_relation.

Layers, in order (later layers merge into earlier ones by id before creating new rows):
  1. CTD MEDIC (MeSH + OMIM) backbone, is_a edges from ParentIDs.
  2. SymMap: modern symptoms (SMMS) and diseases (SMDE) merged by MeSH (SMDE also by single OMIM), else 'UMLS:<cui>';
     TCM symptoms 'TCM:SMTSnnnnn' and syndromes 'TCMSY:SMSYnnnnn'.
  3. HERB disease vocabulary (DisGeNET CUIs) merged by MeSH then UMLS; new rows only for 'Sign or Symptom' terms or
     terms with a MeSH/DO id.
  4. ICD-11 codes used by CMAUP (plant–disease) and DDID (drug indications): 'ICD11:<code>', same_as to the
     MEDIC/UMLS condition with an exact normalised name/alias match.
  5. db/maps/action_map.csv: 'ACT:<slug>' conditions (type 'action') with action_targets edges;
     db/maps/condition_synonyms.csv: curated folk/organ synonyms added as aliases.

Extra cross-reference ids go into condition_alias with lang='xref', alias '<DB>:<id>' (UMLS, MESH, OMIM, DOID, HPO,
ICD10CM, ICD10, SYMMAP, HERB). The resolver uses them for by_umls/by_mesh; they are never matched as text.
"""
import csv, gzip, os, re
from collections import Counter

import pandas as pd

from common import DB_DIR, data, slug
from build.resolve_conditions import VOCAB_RANK, cond_keys, fix_icd11

# spelling / phrasing variants of the actions in action_map.csv (variant -> canonical action)
ACTION_VARIANTS = {
    "antiemetic": ["anti emetic", "antiemetics"],
    "antipyretic": ["antipyretics", "anti pyretic"],
    "diaphoretic": ["sudorific", "sweating/diaphoretic"],
    "anti-inflammatory": ["antiinflammatory", "anti inflammatory agents"],
    "hypnotic": ["hypnotics and sedatives", "anti insomniac"],
    "sedative": ["central nervous system depressant", "cns-depressant", "calmative"],
    "emmenagogue": ["menstruation-inducing agents"],
    "galactagogue": ["galactogogue", "galactogogues", "lactogogue", "lactagogue", "lactagog"],
    "anthelmintic": ["anthelminthic", "anti helmintic", "antihelmintic", "antinematodal agents", "antinematodal"],
    "taenifuge": ["taenicide"],
    "antipsoriatic": ["antipsoriac"],
    "antialzheimer": ["antialzheimeran", "anti alzheimeran"],
    "hemostatic": ["hemostat", "hemostatics", "haemostatic", "hemostasis"],
    "antidote": ["alexiteric", "antidotes"],
    "antiatherosclerotic": ["anti atherogenic", "antiatherogenic"],
    "antiallergic": ["anti allergenic", "antiallergenic"],
    "appetite stimulant": ["apertif", "aperitif", "appetizer", "stomachic tonic"],
    "hepatoprotective": ["antihepatotic", "liver protective"],
    "cholagogue": ["cholagogues and choleretics"],
    "antitumor": ["anticarcinomic", "antineoplastic agents", "antitumour"],
    "cancer preventive": ["anticarcinogenic", "cancer-preventive"],
    "antibacterial": ["antibiotic", "anti-bacterial agents", "bactericide", "bacteristat"],
    "antiseptic": ["anti-infective agents", "anti-infective agents, local", "antimicrobial", "disinfectant"],
    "antifungal": ["fungicide", "fungistat", "antifungal agents", "antimycotic"],
    "antimalarial": ["plasmodicide", "antimalarials"],
    "trypanocide": ["antitrypanosomic"],
    "antiaggregant": ["antiplatelet", "platelet aggregation inhibitor"],
    "antiarrhythmic": ["anti-arrhythmia agents", "antiarrhythmia"],
    "antidepressant": ["antidepressive agents", "antidepressive"],
    "antiobesity": ["anti-obesity agents"],
    "antifertility": ["contraceptive", "contraceptive agents", "spermicide", "spermatocidal agents"],
    "fertility agent": ["fertility agents", "anti infertility", "antiinfertility"],
    "vulnerary": ["wound healing"],
    "antiparasitic": ["parasiticide", "antiparasitic agents"],
    "hypolipidemic": ["hypolipidemic agents", "antihyperlipidemic"],
    "antitussive": ["antitussive agents"],
    "antianemic": ["anti anemic", "hematinic"],
    "anti-hiv": ["antiaids"],
    "anti-ebv": ["anti epstein-barr virus", "antiebv"],
    "antidiabetic": ["anti-diabetic", "antidiabetes"],
    "antihypertensive": ["antihypertensive agents"],
    "anticonvulsant": ["anticonvulsants"],
    "antirheumatic": ["antirheumatic agents"],
    "antiviral": ["antiviral agents"],
    "stomachic": ["stomachics"],
    "laxative": ["laxatives"],
    "purgative": ["purgatives"],
    "aperient": ["aperients"],
    "anticoronary": ["anti coronary"],
}


def _first(v, sep="|"):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return None
    v = str(v).strip()
    if not v or v.upper() in ("NA", "NAN"):
        return None
    return v.split(sep)[0].strip() or None


def _split(v, sep="|"):
    if v is None or (isinstance(v, float) and pd.isna(v)):
        return []
    return [x.strip() for x in str(v).split(sep) if x.strip() and x.strip().upper() not in ("NA", "NAN")]


class Builder:
    def __init__(self):
        self.cond = {}      # id -> dict
        self.alias = {}     # (id, alias, lang) -> source
        self.rel = set()
        self.mesh, self.umls, self.omim = {}, {}, {}
        self.stats = Counter()

    def add(self, cid, name, type_, vocab, **kw):
        row = dict(condition_id=cid, name=name, type=type_, mesh_id=None, umls_cui=None, icd11=None, icd10cm=None,
                   doid=None, hpo=None, mesh_tree=None, source_vocab=vocab)
        row.update({k: v for k, v in kw.items() if v})
        self.cond[cid] = row
        if row["mesh_id"]:
            self.mesh.setdefault(row["mesh_id"].split(":")[-1], cid)
        if row["umls_cui"]:
            self.umls.setdefault(row["umls_cui"], cid)
        return row

    def fill(self, cid, field, value, xref_db=None):
        """Fill an empty column; if already set to something else, keep it as an xref alias."""
        if not value:
            return
        row = self.cond[cid]
        if not row[field]:
            row[field] = value
        elif row[field] != value and xref_db:
            self.xref(cid, xref_db, value)
        if field == "umls_cui":
            self.umls.setdefault(value, cid)

    def al(self, cid, alias, lang, source):
        if alias is None or (isinstance(alias, float) and pd.isna(alias)):
            return
        a = str(alias).strip()
        if a and (cid, a, lang) not in self.alias:
            self.alias[(cid, a, lang)] = source

    def xref(self, cid, db, x, source=None):
        if not x:
            return
        x = str(x).strip()
        if db == "UMLS":
            self.umls.setdefault(x, cid)
        elif db == "MESH":
            self.mesh.setdefault(x, cid)
        self.al(cid, f"{db}:{x}", "xref", source or self.cond[cid]["source_vocab"])


# ---------------------------------------------------------------------------------------------------------------
def load_medic(b):
    rows = [l.rstrip("\n").split("\t") for l in gzip.open(data("ctd", "CTD_diseases.tsv.gz"), "rt", encoding="utf-8")
            if not l.startswith("#")]
    for name, did, alt, _defn, parents, trees, _ptrees, syns, _slim in rows:
        tl = [t for t in trees.split("|") if t]
        if did.startswith("MESH:D") and any(t.startswith("C23.888") for t in tl):
            typ = "symptom"
        elif did.startswith("MESH:D") and tl and all(t.startswith("C23") for t in tl):
            typ = "finding"  # pathological conditions/processes (C23.550, C23.300 …) outside Signs and Symptoms
        else:
            typ = "disease"
        alts = _split(alt)
        doid = next((a.replace("DO:", "") for a in alts if a.startswith("DO:")), None)
        b.add(did, name, typ, "medic", mesh_id=did if did.startswith("MESH:") else None, doid=doid,
              mesh_tree="|".join(tl) or None)
        if did.startswith("OMIM:"):
            b.omim.setdefault(did[5:], did)
        for a in alts:
            if a.startswith("OMIM:"):
                b.omim.setdefault(a[5:], did)
                b.xref(did, "OMIM", a[5:], "medic")
            elif a.startswith("DO:") and a.replace("DO:", "") != doid:
                b.xref(did, "DOID", a.replace("DO:DOID:", ""), "medic")
        b.al(did, name, "en", "medic")
        for s in _split(syns):
            b.al(did, s, "en", "medic")
        for p in _split(parents):
            b.rel.add((did, p, "is_a"))
    b.stats["medic"] = len(rows)


def _xl(name):
    return pd.read_excel(data("symmap", f"symmap_v2_{name}.xlsx"), dtype=str)


def load_symmap(b):
    # modern symptoms ----------------------------------------------------------------------------------------
    ms = _xl("SMMS")
    key = _xl("SMMS_key")
    sid2cid = {}
    for r in ms.itertuples(index=False):
        smid = f"SMMS{int(r.MM_symptom_id):05d}"
        cui = _first(r.UMLS_id)
        meshes = _split(r.MeSH_id)
        cid = next((f"MESH:{m}" for m in meshes if f"MESH:{m}" in b.cond), None)
        if cid:
            b.stats["smms_merged_mesh"] += 1
        elif cui and cui in b.umls:
            cid = b.umls[cui]
            b.stats["smms_merged_umls"] += 1
        else:
            cid = f"UMLS:{cui}"
            b.add(cid, r.MM_symptom_name, "symptom", "symmap", umls_cui=cui,
                  mesh_id=f"MESH:{meshes[0]}" if meshes else None, mesh_tree=r.MeSH_tree_numbers
                  if isinstance(r.MeSH_tree_numbers, str) else None)
            b.stats["smms_new"] += 1
        b.fill(cid, "umls_cui", cui, "UMLS")
        b.xref(cid, "UMLS", cui, "symmap")
        icds, hpos = _split(r.ICD10CM_id), _split(r.HPO_id)
        if icds:
            b.fill(cid, "icd10cm", icds[0], "ICD10CM")
        if hpos:
            b.fill(cid, "hpo", hpos[0], "HPO")
        for x in icds[1:]:
            b.xref(cid, "ICD10CM", x, "symmap")
        for x in hpos[1:]:
            b.xref(cid, "HPO", x, "symmap")
        for m in meshes:
            b.xref(cid, "MESH", m, "symmap")
        b.xref(cid, "SYMMAP", smid, "symmap")
        b.al(cid, r.MM_symptom_name, "en", "symmap")
        sid2cid[r.MM_symptom_id] = cid
    for r in key.itertuples(index=False):
        cid = sid2cid.get(r.MM_symptom_id)
        if not cid:
            continue
        if r.Field_name == "UMLS_id":
            b.xref(cid, "UMLS", r.Field_context, "symmap")
        else:
            b.al(cid, r.Field_context, "en", "symmap")

    # diseases -------------------------------------------------------------------------------------------------
    de = _xl("SMDE")
    dkey = _xl("SMDE_key")
    did2cid, linked = {}, {}
    for r in de.itertuples(index=False):
        if r.Suppress == "1":
            if isinstance(r.Link_disease_id, str):
                linked[r.Disease_id] = str(int(float(r.Link_disease_id)))
            continue
        cuis = _split(r.UMLS_id)
        meshes = _split(r.MeSH_id)
        omims = sorted(set(_split(r.OMIM_id)))
        cid = next((f"MESH:{m}" for m in meshes if f"MESH:{m}" in b.cond), None)
        if cid:
            b.stats["smde_merged_mesh"] += 1
        elif len(omims) == 1 and omims[0] in b.omim:
            cid = b.omim[omims[0]]
            b.stats["smde_merged_omim"] += 1
        elif cuis and cuis[0] in b.umls:
            cid = b.umls[cuis[0]]
            b.stats["smde_merged_umls"] += 1
        elif cuis:
            cid = f"UMLS:{cuis[0]}"
            b.add(cid, r.Disease_Name, "disease", "symmap", umls_cui=cuis[0],
                  mesh_id=f"MESH:{meshes[0]}" if meshes else None)
            b.stats["smde_new"] += 1
        else:
            b.stats["smde_skipped_no_id"] += 1
            continue
        for c in cuis:
            b.xref(cid, "UMLS", c, "symmap")
        if cuis:
            b.fill(cid, "umls_cui", cuis[0], "UMLS")
        icds = _split(r.ICD10CM_id)
        if icds:
            b.fill(cid, "icd10cm", icds[0], "ICD10CM")
        for x in icds[1:]:
            b.xref(cid, "ICD10CM", x, "symmap")
        for m in meshes:
            b.xref(cid, "MESH", m, "symmap")
        for o in omims:
            b.xref(cid, "OMIM", o, "symmap")
        b.xref(cid, "SYMMAP", f"SMDE{int(r.Disease_id):05d}", "symmap")
        b.al(cid, r.Disease_Name, "en", "symmap")
        did2cid[r.Disease_id] = cid
    for sup, tgt in linked.items():
        if tgt in did2cid:
            did2cid[sup] = did2cid[tgt]
            b.xref(did2cid[tgt], "SYMMAP", f"SMDE{int(sup):05d}", "symmap")
    for r in dkey.itertuples(index=False):
        cid = did2cid.get(r.Disease_id)
        if cid:
            b.al(cid, r.Field_context, "en", "symmap")

    # TCM symptoms ----------------------------------------------------------------------------------------------
    ts = _xl("SMTS")
    for r in ts.itertuples(index=False):
        cid = f"TCM:SMTS{int(r.TCM_symptom_id):05d}"
        b.add(cid, r.TCM_symptom_name, "tcm_symptom", "symmap")
        b.al(cid, r.TCM_symptom_name, "zh", "symmap")
        b.al(cid, r.Symptom_pinYin, "pinyin", "symmap")
    tkey = _xl("SMTS_key")
    for r in tkey.itertuples(index=False):
        cid = f"TCM:SMTS{int(r.TCM_symptom_id):05d}"
        if cid in b.cond:
            b.al(cid, r.Field_context, "pinyin" if r.Field_name == "Symptom_pinYin" else "zh", "symmap")
    # syndromes -------------------------------------------------------------------------------------------------
    sy = _xl("SMSY")
    for r in sy.itertuples(index=False):
        cid = f"TCMSY:SMSY{int(r.Syndrome_id):05d}"
        en = r.Syndrome_English if isinstance(r.Syndrome_English, str) else None
        b.add(cid, en or r.Syndrome_name, "tcm_syndrome", "symmap")
        b.al(cid, r.Syndrome_name, "zh", "symmap")
        b.al(cid, r.Syndrome_PinYin, "pinyin", "symmap")
        b.al(cid, en, "en", "symmap")
    skey = _xl("SMSY_key")
    lang = {"Syndrome_name": "zh", "Syndrome_PinYin": "pinyin", "Syndrome_English": "en"}
    for r in skey.itertuples(index=False):
        cid = f"TCMSY:SMSY{int(r.Syndrome_id):05d}"
        if cid in b.cond:
            b.al(cid, r.Field_context, lang.get(r.Field_name, "en"), "symmap")
    # TCM symptom -> modern symptom: SymMap's own mapping is not in the local download (only herb-level scrape
    # relations exist), so no tcm_maps_to edges are invented here.


# ---------------------------------------------------------------------------------------------------------------
def load_herb(b, name_index):
    h = pd.read_csv(data("herb", "HERB_disease_info_v2.txt"), sep="\t", dtype=str, na_values=["NA"],
                    keep_default_na=False)
    for r in h.itertuples(index=False):
        cui = r.DisGeNET_id
        meshes = [m for m in re.split(r"[|;,]\s*", r.MeSH_id) if m] if isinstance(r.MeSH_id, str) else []
        dos = [d.strip() for d in re.split(r"[;|,]", r.DO_id) if d.strip()] if isinstance(r.DO_id, str) else []
        hpos = [x.strip() for x in re.split(r"[;|,]", r.HPO_id) if x.strip()] if isinstance(r.HPO_id, str) else []
        utype = r.UMLS_disease_type if isinstance(r.UMLS_disease_type, str) else ""
        names = [r.Disease_name] + ([a.strip() for a in r.Disease_alias_name.split(";")]
                                    if isinstance(r.Disease_alias_name, str) else [])
        cid = next((b.mesh[m] for m in meshes if m in b.mesh), None)
        how = "mesh"
        if not cid and cui in b.umls:
            cid, how = b.umls[cui], "umls"
        if cid:
            b.stats[f"herb_merged_{how}"] += 1
            # only promote the CUI to the primary column when the names agree (DisGeNET MeSH maps are coarse)
            ckeys = set(k for a in (b.cond[cid]["name"],) for k in cond_keys(a))
            if not b.cond[cid]["umls_cui"] and ckeys & set(cond_keys(r.Disease_name)):
                b.cond[cid]["umls_cui"] = cui
        elif "Sign or Symptom" in utype or meshes or dos:
            typ = ("symptom" if "Sign or Symptom" in utype else
                   "finding" if utype.startswith(("Finding", "Laboratory")) else "disease")
            cid = f"UMLS:{cui}"
            b.add(cid, r.Disease_name, typ, "herb", umls_cui=cui, mesh_id=f"MESH:{meshes[0]}" if meshes else None)
            b.stats["herb_new"] += 1
        else:
            b.stats["herb_skipped"] += 1
            continue
        b.xref(cid, "UMLS", cui, "herb")
        b.xref(cid, "HERB", r.Disease_id, "herb")
        if dos:
            b.fill(cid, "doid", f"DOID:{dos[0]}")
            for d in dos:
                b.xref(cid, "DOID", d, "herb")
        if hpos:
            b.fill(cid, "hpo", hpos[0])
            for x in hpos[1:]:
                b.xref(cid, "HPO", x, "herb")
        if isinstance(r.ICD10_id, str):
            for x in re.split(r"[;|,]\s*", r.ICD10_id):
                b.xref(cid, "ICD10", x, "herb")
        for m in meshes:
            b.xref(cid, "MESH", m, "herb")
        for n in names:
            b.al(cid, n, "en", "herb")


# ---------------------------------------------------------------------------------------------------------------
def build_name_index(b, exclude_prefix=("ICD11:", "ACT:")):
    """norm key -> best condition id among MEDIC/UMLS rows (vocab rank, primary name first)."""
    best = {}
    for (cid, alias, lang), _src in b.alias.items():
        if lang == "xref" or cid.startswith(exclude_prefix):
            continue
        c = b.cond[cid]
        if c["type"] in ("tcm_symptom", "tcm_syndrome", "action"):
            continue
        score = (VOCAB_RANK.get(c["source_vocab"], 9), 0 if alias == c["name"] else 1, cid)
        for k in cond_keys(alias):
            if k not in best or score < best[k]:
                best[k] = score
    return {k: v[2] for k, v in best.items()}


def link_umls_same_as(b):
    """UMLS: rows whose primary name exactly matches a MEDIC name/synonym -> same_as the MEDIC id."""
    medic = {}
    for (cid, alias, lang), _ in b.alias.items():
        if lang == "en" and b.cond[cid]["source_vocab"] == "medic":
            for k in cond_keys(alias):
                medic.setdefault(k, set()).add(cid)
    n = 0
    for cid, c in b.cond.items():
        if cid.startswith("UMLS:"):
            hits = set().union(*[medic.get(k, set()) for k in cond_keys(c["name"])]) if cond_keys(c["name"]) else set()
            if len(hits) == 1:
                b.rel.add((cid, hits.pop(), "same_as"))
                n += 1
    b.stats["umls_same_as_medic"] = n


def load_icd11(b):
    names = {}  # code -> Counter(name)
    cats, srcs = {}, {}
    cm = pd.read_csv(data("cmaup", "CMAUPv2.0_download_Plant_Human_Disease_Associations.txt"), sep="\t", dtype=str,
                     usecols=["ICD-11 Code", "Disease_Category", "Disease"], keep_default_na=False)
    cm = cm.groupby(["ICD-11 Code", "Disease_Category", "Disease"]).size().reset_index(name="n")
    for code, cat, dis, n in cm.itertuples(index=False):
        c = fix_icd11(code)
        if not c or not dis or dis in ("N.A.", "NA"):
            continue
        names.setdefault(c, Counter())[dis] += n
        cats.setdefault(c, cat)
        srcs.setdefault(c, {}).setdefault(dis, "cmaup")
    dd = pd.read_csv(data("ddid", "disease_information.csv"), dtype=str, encoding="utf-8-sig")
    pat = re.compile(r"^(.*?)\s*\[ICD-11:\s*([^\]]+)\]\s*$")
    for ind in dd["Indication"].dropna().unique():
        m = pat.match(ind)
        if not m:
            continue
        dis = m.group(1).strip()
        for code in re.split(r"\s*[,;]\s*", m.group(2)):
            c = fix_icd11(code)
            if not c:
                continue
            names.setdefault(c, Counter())[dis] += 1
            srcs.setdefault(c, {}).setdefault(dis, "ddid")
    for c, cnt in names.items():
        cat = cats.get(c, "")
        if cat.startswith("21.") or re.match(r"^M[A-H]", c):
            typ = "symptom"
        elif cat.startswith(("24.", "25.", "V.")) or re.match(r"^(Q|V)", c):
            typ = "finding"
        else:
            typ = "disease"
        cid = f"ICD11:{c}"
        b.add(cid, cnt.most_common(1)[0][0], typ, "icd11", icd11=c)
        for dis in cnt:
            b.al(cid, dis, "en", srcs[c][dis])
    b.stats["icd11"] = len(names)


def link_icd11_same_as(b, name_index):
    n = 0
    by_cid = {}
    for (a_cid, alias, lang) in b.alias:
        if a_cid.startswith("ICD11:"):
            by_cid.setdefault(a_cid, []).append(alias)
    for cid, c in b.cond.items():
        if not cid.startswith("ICD11:"):
            continue
        # the primary (most frequent) name decides; other names only when they all agree (CMAUP reuses some
        # codes for unrelated names, e.g. DB95.1 = toxic liver disease / biliary atresia)
        hit = next((name_index[k] for k in cond_keys(c["name"]) if k in name_index), None)
        if not hit:
            hits = {name_index[k] for a in by_cid.get(cid, []) for k in cond_keys(a) if k in name_index}
            hit = hits.pop() if len(hits) == 1 else None
        if hit:
            b.rel.add((cid, hit, "same_as"))
            b.fill(hit, "icd11", c["icd11"], "ICD11")
            n += 1
    b.stats["icd11_same_as"] = n


def load_actions(b):
    path = os.path.join(DB_DIR, "maps", "action_map.csv")
    acts = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        tgt = r["condition_id"]
        if tgt not in b.cond:
            raise ValueError(f"action_map.csv: unknown condition {tgt} for {r['action']}")
        aid = "ACT:" + slug(r["action"])
        if aid not in b.cond:
            b.add(aid, r["action"], "action", "action_map")
            b.al(aid, r["action"], "en", "manual")
            for v in ACTION_VARIANTS.get(r["action"], []):
                b.al(aid, v, "en", "manual")
        acts[aid] = 1
        b.rel.add((aid, tgt, "action_targets"))
    b.stats["actions"] = len(acts)
    path = os.path.join(DB_DIR, "maps", "condition_synonyms.csv")
    for r in csv.DictReader(open(path, encoding="utf-8")):
        if r["condition_id"] not in b.cond:
            raise ValueError(f"condition_synonyms.csv: unknown condition {r['condition_id']}")
        b.al(r["condition_id"], r["alias"], r.get("lang") or "en", "manual")


# ---------------------------------------------------------------------------------------------------------------
def build(con):
    b = Builder()
    load_medic(b)
    load_symmap(b)
    load_herb(b, None)
    link_umls_same_as(b)
    load_icd11(b)
    link_icd11_same_as(b, build_name_index(b))
    load_actions(b)
    # drop relations to ids that do not exist (MEDIC parents outside the vocabulary, if any)
    rel = [r for r in b.rel if r[0] in b.cond and r[1] in b.cond]
    b.stats["relations_dropped"] = len(b.rel) - len(rel)

    cols = ["condition_id", "name", "type", "mesh_id", "umls_cui", "icd11", "icd10cm", "doid", "hpo", "mesh_tree",
            "source_vocab"]
    cdf = pd.DataFrame(list(b.cond.values()))[cols]
    adf = pd.DataFrame([(c, a, l, s) for (c, a, l), s in b.alias.items()],
                       columns=["condition_id", "alias", "lang", "source_id"])
    rdf = pd.DataFrame(sorted(rel), columns=["from_id", "to_id", "rel"])
    con.execute("DELETE FROM condition_relation")
    con.execute("DELETE FROM condition_alias")
    con.execute("DELETE FROM condition")
    con.execute("INSERT INTO condition SELECT * FROM cdf")
    con.execute("INSERT INTO condition_alias SELECT * FROM adf")
    con.execute("INSERT INTO condition_relation SELECT * FROM rdf")
    print("[conditions]", dict(b.stats), flush=True)
    print("[conditions] rows:", len(cdf), "aliases:", len(adf), "relations:", len(rdf), flush=True)
