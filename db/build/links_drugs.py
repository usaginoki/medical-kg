"""links stage, part 4: `drug`, `drug_condition`, `ingredient_drug` (DDID + DrugBank sample rows)."""
import re

import pandas as pd

from common import data, slug
from build.links_common import log, df_to_temp, s


def build_drugs(con, ir, icd11):
    rd = lambda f: pd.read_csv(data("ddid", f), dtype=str, keep_default_na=False, encoding="utf-8-sig")
    di = rd("drug_information.csv")
    drugs, fhdi = {}, {}
    for r in di.to_dict("records"):
        db = s(r["DrugBank_ID"])
        did = f"DB:{db}" if db else f"DRUGNAME:{slug(r['Drug_Name'])}"
        fhdi[r["FHDI_Drug_ID"]] = did
        drugs.setdefault(did, (did, r["Drug_Name"], db, s(r["InChIKey"])))

    # DrugBank sample rows (food interactions scraped via DDID) + public drug cards
    dbi = pd.read_csv(data("drugbank", "food_interactions_via_ddid.csv"), dtype=str, keep_default_na=False)
    cards = pd.read_csv(data("drugbank", "public_drug_cards.csv"), dtype=str, keep_default_na=False)
    card_ik = dict(zip(cards.drugbank_id, cards.InChIKey))
    for dbid, name in zip(dbi.drugbank_id, dbi.Drug_Name):
        drugs.setdefault(f"DB:{dbid}", (f"DB:{dbid}", name, dbid, s(card_ik.get(dbid))))
    for dbid, name, ik in zip(cards.drugbank_id, cards.name, cards.InChIKey):
        drugs.setdefault(f"DB:{dbid}", (f"DB:{dbid}", name, dbid, s(ik)))
    con.execute("DELETE FROM drug")
    df_to_temp(con, "dr", pd.DataFrame(list(drugs.values()), columns=["a", "b", "c", "d"]))
    con.execute("INSERT INTO drug SELECT * FROM dr")

    # indications: 'Constipation [ICD-11: DD91.1]'
    dis = rd("disease_information.csv")
    rows, n_unres = [], 0
    for ind, fid in zip(dis.Indication, dis.FHDI_Drug_ID):
        m = re.search(r"\[ICD-11:\s*([^\]]+)\]", ind)
        cond = icd11(m.group(1).strip()) if m else None
        if cond and fid in fhdi:
            rows.append((fhdi[fid], cond, "ddid"))
        else:
            n_unres += 1
    con.execute("DELETE FROM drug_condition")
    df_to_temp(con, "dc", pd.DataFrame(rows, columns=["a", "b", "c"]).drop_duplicates())
    con.execute("INSERT INTO drug_condition SELECT * FROM dc WHERE b IN (SELECT condition_id FROM condition)")

    # interactions
    ii = rd("interaction_information.csv")
    rows, n_unres_i = [], 0
    for r in ii.to_dict("records"):
        fh = r["Food_Herb_ID"]
        ing = ir.by_xref("ddid_food" if fh.startswith("F") else "ddid_herb", fh)
        drug = fhdi.get(r["Drug_ID"])
        if not ing or not drug:
            n_unres_i += 1
            continue
        eff = s(r["Effect"])
        eff = eff[0].upper() + eff[1:] if eff else None
        pm = s(r["PMID"])
        ev = "curated_literature" if pm else ("predicted" if eff == "Possible" else "curated_literature")
        note = s(r["Conclusion"]) or s(r["Result"])
        comp = s(r["Component"])
        if comp:
            note = f"[{comp}] {note or ''}".strip()
        rows.append((ing[0], drug, eff, s(r["Potential_Target"]), ev, pm, "ddid", note[:500] if note else None))
    seen = {(a, b) for a, b, *_ in rows}
    n_db = 0
    for r in dbi.to_dict("records"):
        ing = ir.by_text(r["Food_Herb_Name"], "en", fuzzy=False)
        drug = f"DB:{r['drugbank_id']}"
        if not ing or (ing[0], drug) in seen:
            continue
        eff = s(r["Effect"])
        eff = eff[0].upper() + eff[1:] if eff else None
        note = s(r["Conclusion"]) or s(r["Result"])
        if s(r["Component"]):
            note = f"[{r['Component']}] {note or ''}".strip()
        rows.append((ing[0], drug, eff, None, "predicted" if eff == "Possible" else "curated_literature", None,
                     "drugbank", note[:500] if note else None))
        seen.add((ing[0], drug))
        n_db += 1
    con.execute("DELETE FROM ingredient_drug")
    df_to_temp(con, "idr", pd.DataFrame(rows, columns=list("abcdefgh")))
    con.execute("""INSERT INTO ingredient_drug SELECT * FROM idr
                   WHERE a IN (SELECT ingredient_id FROM ingredient) AND b IN (SELECT drug_id FROM drug)""")
    q = lambda t: con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
    log(f"drugs: drug {q('drug'):,}; drug_condition {q('drug_condition'):,} ({n_unres} indications unresolved); "
        f"ingredient_drug {q('ingredient_drug'):,} (DDID {len(ii):,} interactions, {n_unres_i:,} with unmatched "
        f"food/herb; DrugBank sample added {n_db})")
