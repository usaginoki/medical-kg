"""links stage, part 3: `ingredient_condition` (direct food/herb -> condition links).

Sources: SymMap scraped herb relations (TCM symptom, MM symptom, syndrome, inferred disease), SpiceRx, CMAUP
plant–disease, IMPPAT therapeutic uses, Dr. Duke's ETHNOBOT, UNaProd monographs, HERB clinical trials, KNApSAcK Jamu.

Traditional-use claims ('used for cough') are stored as direction 'beneficial' (the tradition's claim); when a term
is an action ('antiemetic'), the action's target conditions are used with the action map's direction.
"""
import re

import pandas as pd

from common import data
from build.links_common import log, df_to_temp, xref_alias_map, s, pmids as parse_pmids

COLS = ["ingredient_id", "condition_id", "direction", "evidence_type", "tradition", "plant_part", "n_pos", "n_neg",
        "pmids", "source_id", "note"]


def _row(ing, cond, direction, ev, src, tradition=None, part=None, n_pos=None, n_neg=None, pm=None, note=None):
    return (ing, cond, direction, ev, tradition, part, n_pos, n_neg, pm, src, note)


def _insert(con, rows, label):
    df = pd.DataFrame(rows, columns=COLS).astype({"n_pos": "Int64", "n_neg": "Int64"})
    df_to_temp(con, "ic_rows", df)
    con.execute("INSERT INTO stg_ic2 SELECT * FROM ic_rows")
    log(f"{label}: {len(rows):,} staged")


POS = re.compile(r"\b(effective|efficacious|improv\w*|significant(ly)? (reduc|decreas|lower|attenuat|alleviat)\w*|"
                 r"beneficial|ameliorat\w*|alleviat\w*|relie\w*)\b", re.I)
NEG = re.compile(r"\b(no (significant )?(effect|difference|benefit|improvement)|not (effective|significant)|did not|"
                 r"failed|no evidence|insufficient|inconclusive|unclear|warrant\w*)\b", re.I)


def build_ingredient_condition(con, ir, kr, ct, icd11):
    con.execute("CREATE OR REPLACE TEMP TABLE stg_ic2 (" + ", ".join(
        f"{c} {'INTEGER' if c in ('n_pos', 'n_neg') else 'VARCHAR'}" for c in COLS) + ")")
    symmap_alias = xref_alias_map(con, "SYMMAP")
    sm_ing = lambda h: (ir.by_xref("symmap", h) or (None,))[0]

    # ---- SymMap scraped relations -------------------------------------------------------------------------
    sc = lambda f: pd.read_csv(data("symmap", "scrape", f), dtype=str, keep_default_na=False)
    rows = []
    for r in sc("herb_tcm_symptom_relations.csv").itertuples(index=False):
        ing = sm_ing(r.source_herb_id)
        if ing:
            rows.append(_row(ing, "TCM:" + r.TCM_symptom_id, "beneficial", "traditional", "symmap", "tcm",
                             note=f"{r.TCM_symptom_name} {r.Symptom_pinyin}".strip()))
    for r in sc("herb_mm_symptom_relations.csv").itertuples(index=False):
        ing = sm_ing(r.source_herb_id)
        cond = kr.by_umls(r.UMLS_id) or symmap_alias.get(r.MM_symptom_id)
        if ing and cond:
            rows.append(_row(ing, cond, "beneficial", "traditional", "symmap", "tcm",
                             note=f"{r.MM_symptom_name} (via TCM symptom)"))
    for r in sc("herb_syndrome_relations.csv").itertuples(index=False):
        ing = sm_ing(r.source_herb_id)
        if ing:
            rows.append(_row(ing, "TCMSY:" + r.Syndrome_id, "beneficial", "traditional", "symmap", "tcm",
                             note=f"{r.Syndrome_name} {r.Syndrome_English}".strip()))
    n_trad = len(rows)
    dis = sc("herb_disease_relations.csv")
    fdr = pd.to_numeric(dis["FDR(BH)"], errors="coerce")
    dis_kept = dis[fdr <= 0.05]
    for r in dis_kept.to_dict("records"):
        ing = sm_ing(r["source_herb_id"])
        cond = symmap_alias.get(r["Disease_id"])
        if ing and cond:
            rows.append(_row(ing, cond, "association", "predicted", "symmap",
                             note=f"{r['Disease_name']}; {r['Relationship']}; FDR(BH) {r['FDR(BH)']}"))
    _insert(con, rows, f"SymMap: traditional {n_trad}; inferred diseases kept {len(dis_kept):,}/{len(dis):,} (FDR<=0.05)")

    # ---- SpiceRx ------------------------------------------------------------------------------------------
    sa = pd.read_csv(data("spicerx", "spice_disease_associations.csv"), dtype=str, keep_default_na=False)
    sr = pd.read_csv(data("spicerx", "spice_disease_references.csv"), dtype=str, keep_default_na=False)
    refs = sr.groupby(["tax_id", "mesh_id"]).pmid.apply(lambda x: "|".join(dict.fromkeys(x))).to_dict()
    rows = []
    for r in sa.itertuples(index=False):
        ing = ir.by_xref("spicerx", r.tax_id) or ir.by_taxon(r.tax_id)
        cond = kr.by_mesh(r.mesh_id)
        if not ing or not cond:
            continue
        p, n = int(r.n_positive), int(r.n_negative)
        direction = "beneficial" if p > n else "harmful" if n > p else "association"
        rows.append(_row(ing[0], cond, direction, "text_mined", "spicerx", n_pos=p, n_neg=n,
                         pm=refs.get((r.tax_id, r.mesh_id)), note=r.disease))
    _insert(con, rows, f"SpiceRx ({len(sa)} associations)")

    # ---- CMAUP plant–disease ------------------------------------------------------------------------------
    con.execute("""CREATE OR REPLACE TEMP TABLE cmd AS SELECT Plant_ID AS p, "ICD-11 Code" AS code, Disease_Category AS cat,
                          Disease AS disease, Association_by_Therapeutic_Target AS tgt,
                          Association_by_Disease_Transcriptiome_Reversion AS trx,
                          Association_by_Clinical_Trials_of_Plant AS nct
                   FROM read_csv(?, delim='\t', all_varchar=true, quote='')""",
                [data("cmaup", "CMAUPv2.0_download_Plant_Human_Disease_Associations.txt")])
    total = con.execute("SELECT count(*) FROM cmd").fetchone()[0]
    rows, n_pred_all, n_unres = [], 0, 0
    plant = {}
    for r in con.execute("SELECT * FROM cmd").fetchall():
        p, code, cat, disease, tgt, trx, nct = r
        if p not in plant:
            hit = ir.by_xref("cmaup", p) or ir.by_xref("npass", p)
            plant[p] = hit[0] if hit else None
        ing = plant[p]
        if not ing:
            continue
        has_trial = s(nct) is not None
        predicted = (s(tgt) or s(trx)) is not None
        if not has_trial:
            if not predicted:
                continue
            n_pred_all += 1
            # keep volume sane: symptoms (chapter 21) plus category-level diseases (codes without a subcode)
            if not ((cat or "").startswith("21.") or (code and "." not in code)):
                continue
        cond = icd11(code)
        if not cond:
            n_unres += 1
            continue
        if has_trial:
            rows.append(_row(ing, cond, "association", "clinical", "cmaup", note=f"{disease}; {nct}"))
        else:
            rows.append(_row(ing, cond, "association", "predicted", "cmaup",
                             note=f"{disease}; by " + "+".join(x for x, v in (("target", tgt), ("transcriptome", trx)) if s(v))))
    con.execute("DROP TABLE cmd")
    _insert(con, rows, f"CMAUP ({total:,} rows; dictionary plants predicted {n_pred_all:,} before the chapter-21/"
                       f"category filter; {n_unres:,} unresolved codes; clinical "
                       f"{sum(1 for r in rows if r[3] == 'clinical')}, predicted {sum(1 for r in rows if r[3] == 'predicted'):,})")

    # ---- IMPPAT therapeutic uses --------------------------------------------------------------------------
    tu = pd.read_csv(data("imppat", "IMPPAT_TherapeuticUse_Plant_Association.tsv"), sep="\t", dtype=str,
                     keep_default_na=False, quoting=3)
    pinfo = pd.read_csv(data("imppat", "Plant_Information_IMPPAT.tsv"), sep="\t", dtype=str, keep_default_na=False,
                        quoting=3, usecols=["Plant_identifier", "System_of_Medicine"])
    systems = {}
    for pid_, sysm in zip(pinfo.Plant_identifier, pinfo.System_of_Medicine):
        ss = [x.strip().lower() for x in sysm.split(",") if x.strip()]
        systems[pid_] = "ayurveda" if (not ss or "ayurveda" in ss) else ss[0]
    rows, hit_terms = [], set()
    for r in tu.itertuples(index=False):
        ing = ir.by_xref("imppat", r.IMPPAT_Plant_identifier)
        if not ing:
            continue
        for cond, direction, _m, _sc in ct.hits(r.Therapeutic_use, "beneficial"):
            hit_terms.add(r.Therapeutic_use)
            rows.append(_row(ing[0], cond, direction, "traditional", "imppat", systems.get(r.IMPPAT_Plant_identifier, "ayurveda"),
                             part=s(r.Plant_part), note=r.Therapeutic_use))
    _insert(con, rows, f"IMPPAT therapeutic uses (terms mapped {len(hit_terms)}/{tu.Therapeutic_use.nunique()})")

    # ---- Dr. Duke's ETHNOBOT ------------------------------------------------------------------------------
    eb = pd.read_csv(data("dr-dukes-phytochemical-and-ethnobotanical-databases", "ETHNOBOT.csv"), dtype=str,
                     keep_default_na=False, usecols=["ACTIVITY", "TAXON", "COUNTRY"])
    rows, hit_terms = [], set()
    taxa = {t: ir.by_xref("duke", t) for t in eb.TAXON.unique()}
    for act, taxon, country in zip(eb.ACTIVITY, eb.TAXON, eb.COUNTRY):
        ing = taxa.get(taxon)
        if not ing:
            continue
        for cond, direction, _m, _sc in ct.hits(act, "beneficial"):
            hit_terms.add(act)
            rows.append(_row(ing[0], cond, direction, "traditional", "duke", "folk",
                             note=act + (f" ({country})" if s(country) else "")))
    _insert(con, rows, f"Duke ETHNOBOT ({len(eb):,} rows; taxa matched {sum(1 for v in taxa.values() if v)}/{len(taxa)}; "
                       f"activities mapped {len(hit_terms)}/{eb.ACTIVITY.nunique()})")

    # ---- UNaProd monographs -------------------------------------------------------------------------------
    un = pd.read_csv(data("unaprod", "unaprod_monographs_sample.csv"), dtype=str, keep_default_na=False)
    rows, n_terms, hit_terms = [], 0, set()
    for r in un.itertuples(index=False):
        ing = ir.by_xref("unaprod", r.ID) or (ir.by_scientific(r.SciName1) if s(r.SciName1) else None)
        if not ing:
            continue
        for t in dict.fromkeys(x.strip() for x in r.DiseaseType.split(";") if x.strip()):
            n_terms += 1
            for cond, direction, _m, _sc in ct.hits(t, "beneficial"):
                hit_terms.add(t)
                rows.append(_row(ing[0], cond, direction, "traditional", "unaprod", "persian", note=t))
        # actions (IrGO ActionType) only through the action map: 'Diuretic', 'Emmenagogue', 'Nauseating'…
        for t in dict.fromkeys(x.strip() for x in r.ActionType.split(";") if x.strip()):
            for cond, direction, _m, _sc in ct.hits(t, "beneficial", actions_only=True):
                hit_terms.add(t)
                rows.append(_row(ing[0], cond, direction, "traditional", "unaprod", "persian", note=f"action: {t}"))
    _insert(con, rows, f"UNaProd ({len(un)} monographs; disease/action terms mapped {len(hit_terms)}; "
                       f"AdverseEffect is Persian free text -> skipped)")

    # ---- HERB clinical trials -----------------------------------------------------------------------------
    ch = pd.read_csv(data("herb", "scrape", "clinical_herb.csv"), dtype=str, keep_default_na=False)
    rows = []
    for r in ch.to_dict("records"):
        ing = ir.by_xref("herb", r["source_herb_id"])
        if not ing:
            continue
        # beneficial only when the curated conclusion says the intervention worked
        direction = "beneficial" if (POS.search(r["Conclusion"]) and not NEG.search(r["Conclusion"])) else "association"
        for cond, _d, _m, _sc in ct.hits(r["Study condition"], "association"):
            rows.append(_row(ing[0], cond, direction, "clinical", "herb", pm=parse_pmids(r["PubMed id"]),
                             note=" ".join(f"{r['NCT id']} {r['Study condition']}".split())))
    _insert(con, rows, f"HERB clinical trials ({len(ch)} trials)")

    # ---- KNApSAcK Jamu ------------------------------------------------------------------------------------
    jf = pd.read_csv(data("knapsack-family", "jamu_formula_herbs.csv"), dtype=str, keep_default_na=False)
    je = pd.read_csv(data("knapsack-family", "jamu_herb_effect_examples.csv"), dtype=str, keep_default_na=False)

    def jamu_terms(effect):
        e = re.sub(r"^(cure|curing|treat|treating|relieve|relieving|overcome|prevent|reduce|for)\s+", "", effect.strip(), flags=re.I)
        e = re.sub(r"\s+(medicine|drug|salve)$", "", e, flags=re.I)
        e = re.sub(r"^(drug|medicine)\s+", "", e, flags=re.I)
        return [x.strip() for x in re.split(r",|\band\b", e) if x.strip()]

    def jamu_ing(sci, name=None):
        return (ir.by_scientific(sci) if s(sci) else None) or (ir.by_xref("knapsack", sci) if s(sci) else None)
    rows = []
    for r in je.itertuples(index=False):
        ing = jamu_ing(r.scientific_name)
        m = re.search(r"Effect\s+(.*?)\s+Comment", r.text)
        if not ing or not m:
            continue
        eff = re.sub(r"^[A-Za-z ]+:\s*", "", m.group(1))
        for t in re.split(r",", eff):
            for cond, direction, _m, _sc in ct.hits(re.sub(r"^(drug|medicine)\s+|\s+(medicine|salve)$", "", t.strip().rstrip(".")), "beneficial"):
                rows.append(_row(ing[0], cond, direction, "traditional", "knapsack", "jamu", note=t.strip()))
    for r in jf.itertuples(index=False):
        ing = jamu_ing(r.scientific_name)
        if not ing:
            continue
        for t in jamu_terms(r.jamu_effect):
            for cond, direction, _m, _sc in ct.hits(t, "beneficial"):
                rows.append(_row(ing[0], cond, direction, "traditional", "knapsack", "jamu", part=s(r.plant_part),
                                 note=f"jamu formula '{r.jamu_name}': {r.jamu_effect}"))
    _insert(con, rows, "KNApSAcK Jamu")

    # ---- dedupe on (ingredient, condition, direction, evidence, source, tradition) ------------------------
    con.execute("DELETE FROM ingredient_condition")
    con.execute("""
        INSERT INTO ingredient_condition
        SELECT ingredient_id, condition_id, direction, evidence_type, tradition,
               left(string_agg(DISTINCT plant_part, '|'), 200), max(n_pos), max(n_neg),
               left(string_agg(DISTINCT pmids, '|'), 2000), source_id,
               left(string_agg(DISTINCT note, '; '), 500)
        FROM stg_ic2
        WHERE ingredient_id IN (SELECT ingredient_id FROM ingredient) AND condition_id IN (SELECT condition_id FROM condition)
        GROUP BY ingredient_id, condition_id, direction, evidence_type, tradition, source_id""")
    dropped = con.execute("""SELECT count(*) FROM stg_ic2 WHERE condition_id NOT IN (SELECT condition_id FROM condition)""").fetchone()[0]
    log(f"ingredient_condition: {con.execute('SELECT count(*) FROM ingredient_condition').fetchone()[0]:,} rows "
        f"({dropped} staged rows had an unknown condition id)")
    con.execute("DROP TABLE stg_ic2")
