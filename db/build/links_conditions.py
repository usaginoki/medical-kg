"""links stage, part 2: `compound_condition`.

Sources: CTD curated chemical–disease (attached to the CTD-owning compound, fanned out to same-MeSH variants that
occur in ingredient_compound), HMDB metabolite diseases, Exposome-Explorer cancer associations, FooDB
CompoundsHealthEffect and Dr. Duke's AGGREGAC (chemical activities).
"""
import os, pandas as pd

from common import data
from build.links_common import log, lookup_table, df_to_temp, xref_alias_map, s, CondText

STG = """CREATE OR REPLACE TEMP TABLE stg_cc (compound_id VARCHAR, condition_id VARCHAR, direction VARCHAR,
         evidence_type VARCHAR, source_id VARCHAR, pmids VARCHAR, score DOUBLE)"""
CTD_SCORE = {"self": 1.0, "own": 1.0, "inchikey": 1.0, "cid": 1.0, "xref": 1.0,
             "inchikey_skeleton": 0.7, "name": 0.7, "cas": 0.7}


def build_compound_condition(con, cr, kr, ct):
    con.execute(STG)
    omim = xref_alias_map(con, "OMIM")

    def disease(did):
        did = s(did)
        if not did:
            return None
        if did.upper().startswith("OMIM:"):
            return omim.get(did.split(":", 1)[1])
        return kr.by_mesh(did)

    # ---- CTD ----------------------------------------------------------------------------------------------
    con.execute("""CREATE OR REPLACE TEMP TABLE ctd AS SELECT 'MESH:' || ChemicalID AS mesh, DiseaseID AS did,
                          DirectEvidence AS de, PubMedIDs AS pm
                   FROM read_csv(?, delim='\t', all_varchar=true, quote='') WHERE DirectEvidence IS NOT NULL""",
                [data("ctd", "CTD_chemicals_diseases_curated.tsv")])
    lookup_table(con, "lk_ctd_d", [r[0] for r in con.execute("SELECT DISTINCT did FROM ctd").fetchall()], disease)
    # mesh -> compounds: the owner, plus same-mesh variants that occur in ingredient_compound (food paths)
    in_ic = {r[0] for r in con.execute("SELECT DISTINCT compound_id FROM ingredient_compound").fetchall()}
    match = dict(con.execute("SELECT compound_id, xref_id FROM compound_xref WHERE db = 'ctd_match'").fetchall())
    rows = []
    for (m,) in con.execute("SELECT DISTINCT mesh FROM ctd").fetchall():
        own = cr.by_mesh(m)
        if own:
            rows.append((m, own, CTD_SCORE.get(match.get(own, "own"), 0.7)))
        for c in cr.all_by_mesh(m):
            if c != own and c in in_ic:
                rows.append((m, c, CTD_SCORE.get(match.get(c, "own"), 0.7)))
    df_to_temp(con, "lk_ctd_c", pd.DataFrame(rows, columns=["mesh", "compound_id", "score"]))
    con.execute("""INSERT INTO stg_cc
        SELECT c.compound_id, d.v, CASE WHEN ctd.de = 'therapeutic' THEN 'beneficial' ELSE 'marker' END,
               'curated_literature', 'ctd', ctd.pm, c.score
        FROM ctd JOIN lk_ctd_c c USING (mesh) JOIN lk_ctd_d d ON d.k = ctd.did""")
    n_ctd = con.execute("SELECT count(*) FROM ctd").fetchone()[0]
    log(f"CTD: {n_ctd:,} curated rows; {len(rows):,} mesh->compound links "
        f"({sum(1 for r in rows if r[2] < 1):,} weak); diseases resolved "
        f"{con.execute('SELECT count(*) FROM lk_ctd_d').fetchone()[0]:,}/"
        f"{con.execute('SELECT count(DISTINCT did) FROM ctd').fetchone()[0]:,} -> "
        f"{con.execute('SELECT count(*) FROM stg_cc').fetchone()[0]:,} staged")
    con.execute("DROP TABLE ctd")

    # ---- HMDB metabolite diseases (biomarker associations) ------------------------------------------------
    if not os.path.exists(data("hmdb", "hmdb_metabolite_diseases.csv")):
        log("HMDB: files missing (Data/hmdb/), skipped")
    else:
        hm = pd.read_csv(data("hmdb", "hmdb_metabolite_diseases.csv"), dtype=str, keep_default_na=False)
        # 20k templated cardiolipin -> Barth syndrome (3-methylglutaconic aciduria type II, OMIM 302060) rows
        barth = (hm.omim_id == "302060") & hm.metabolite_name.str.startswith("CL(")
        hm = hm[~barth]
        rows, n_unres = [], 0
        dcache = {}
        for r in hm.itertuples(index=False):
            c = cr.by_xref("hmdb", r.accession)
            if not c:
                continue
            key = (r.omim_id, r.disease_name)
            if key not in dcache:
                dcache[key] = omim.get(r.omim_id) if s(r.omim_id) else None
                dcache[key] = dcache[key] or kr.by_text(r.disease_name)
            d = dcache[key]
            if not d:
                n_unres += 1
                continue
            if d.startswith("ACT:"):
                continue
            rows.append((c, d, "marker", "epidemiological", "hmdb", s(r.pubmed_ids), None))
        df_to_temp(con, "hm", pd.DataFrame(rows, columns=list("abcdefg")))
        con.execute("INSERT INTO stg_cc SELECT * FROM hm")
        log(f"HMDB: {len(hm):,} rows after dropping {int(barth.sum()):,} templated cardiolipin/Barth rows -> "
            f"{len(rows):,} staged ({n_unres:,} rows with unresolved disease)")

    # ---- Exposome-Explorer cancer associations ------------------------------------------------------------
    bm = pd.read_csv(data("exposome-explorer", "biomarkers.csv"), dtype=str, keep_default_na=False)

    def bm_compound(r):
        return (cr.by_inchikey(s(r["InChIKey"])) or cr.by_xref("hmdb", s(r["HMDB ID"]))
                or cr.by_cid(s(r["PubChem ID"])) or cr.by_xref("foodb", s(r["FooDB ID"]))
                or cr.by_cas(s(r["CAS Number"])) or cr.by_name(r["Name"], strict=True))
    bmap = {}
    for _, r in bm.iterrows():
        c = bm_compound(r)
        if c:
            bmap.setdefault(r["Name"], c)
    ca = pd.read_csv(data("exposome-explorer", "cancer_associations.csv"), dtype=str, keep_default_na=False)
    rows = []
    for b, cancer in zip(ca.Biomarker, ca.Cancer):
        c = bmap.get(b)
        for d, direction, _m, _sc in ct.hits(cancer, "association"):
            if c:
                rows.append((c, d, "association", "epidemiological", "exposome", None, None))
    df_to_temp(con, "ex", pd.DataFrame(rows, columns=list("abcdefg")))
    con.execute("INSERT INTO stg_cc SELECT * FROM ex")
    log(f"Exposome-Explorer: {len(ca):,} cancer associations -> {len(rows):,} staged "
        f"(biomarkers resolved {sum(1 for b in ca.Biomarker.unique() if b in bmap)}/{ca.Biomarker.nunique()}; "
        f"cancers resolved {sum(1 for x in ca.Cancer.unique() if ct.hits(x, 'association'))}/{ca.Cancer.nunique()})")

    # ---- FooDB CompoundsHealthEffect ----------------------------------------------------------------------
    he = pd.read_csv(data("foodb", "HealthEffect.csv"), dtype=str, keep_default_na=False, usecols=["id", "name"])
    hname = dict(zip(he.id, he.name))
    ch = pd.read_csv(data("foodb", "CompoundsHealthEffect.csv"), dtype=str, keep_default_na=False,
                     usecols=["compound_id", "health_effect_id", "citation"])
    rows, terms_hit = [], set()
    for c_id, h_id, cit in zip(ch.compound_id, ch.health_effect_id, ch.citation):
        c = cr.by_xref("foodb", c_id)
        name = hname.get(h_id)
        if not c or not name:
            continue
        ev = "curated_literature" if cit.upper() == "CHEBI" else "traditional"
        for d, direction, _m, _sc in ct.hits(name, "association"):
            terms_hit.add(name)
            rows.append((c, d, direction, ev, "foodb", None, None))
    df_to_temp(con, "fh", pd.DataFrame(rows, columns=list("abcdefg")))
    con.execute("INSERT INTO stg_cc SELECT * FROM fh")
    log(f"FooDB health effects: {len(ch):,} rows -> {len(rows):,} staged "
        f"(terms mapped {len(terms_hit)}/{ch.health_effect_id.nunique()})")

    # ---- Dr. Duke's AGGREGAC (chemical activities) --------------------------------------------------------
    ag = pd.read_csv(data("dr-dukes-phytochemical-and-ethnobotanical-databases", "AGGREGAC.csv"), dtype=str,
                     keep_default_na=False, usecols=["CHEM", "ACTIVITY"]).drop_duplicates()
    cmap = {n: cr.by_name(n) for n in ag.CHEM.unique()}
    rows, terms_hit = [], set()
    for chem, act in zip(ag.CHEM, ag.ACTIVITY):
        c = cmap.get(chem)
        if not c:
            continue
        for d, direction, _m, _sc in ct.hits(act, "association"):
            terms_hit.add(act)
            rows.append((c, d, direction, "traditional", "duke", None, None))
    df_to_temp(con, "dk", pd.DataFrame(rows, columns=list("abcdefg")))
    con.execute("INSERT INTO stg_cc SELECT * FROM dk")
    log(f"Duke AGGREGAC: {len(ag):,} rows, chemicals resolved {sum(1 for v in cmap.values() if v)}/{len(cmap)}, "
        f"activities mapped {len(terms_hit)}/{ag.ACTIVITY.nunique()} -> {len(rows):,} staged")

    # ---- dedupe --------------------------------------------------------------------------------------------
    con.execute("DELETE FROM compound_condition")
    con.execute("""
        INSERT INTO compound_condition
        SELECT compound_id, condition_id, direction, evidence_type, source_id,
               nullif(left(array_to_string(list_distinct(flatten(list(string_split(coalesce(pmids, ''), '|')))), '|'), 2000), ''),
               max(score)
        FROM stg_cc
        WHERE compound_id IN (SELECT compound_id FROM compound) AND condition_id IN (SELECT condition_id FROM condition)
        GROUP BY compound_id, condition_id, direction, evidence_type, source_id""")
    con.execute("UPDATE compound_condition SET pmids = trim(replace('|' || pmids || '|', '||', '|'), '|') WHERE pmids IS NOT NULL")
    log("compound_condition: " + ", ".join(f"{a} {b:,}" for a, b in con.execute(
        "SELECT source_id, count(*) FROM compound_condition GROUP BY 1 ORDER BY 2 DESC").fetchall()))
    con.execute("DROP TABLE stg_cc")
