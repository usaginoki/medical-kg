"""One-off polite scrape of SymMap herb relations (NOT run by the build; it needs the network).

    uv run db/build/links_symmap_scrape.py

Same method as the original 8-herb scrape documented in Datasets/SymMap.md: POST
`rrid=<SMHB id>&table_name=<TCM_symptom|MM_symptom|Syndrome|Disease>&filter=0` to
http://www.symmap.org/related_components/ at 1 request/s. Rows are appended to
Data/symmap/scrape/herb_<type>_relations.csv (same columns; `source_herb_id`/`source_herb` added by us).
Herbs already present in a file are skipped, so re-running is a no-op.
"""
import json, os, sys, time, urllib.parse, urllib.request

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import data  # noqa: E402

URL = "http://www.symmap.org/related_components/"
HERBS = {  # SMHB id -> label as in the existing files
    "SMHB00088": "Dasuan (garlic)",
    "SMHB00174": "Huluba (fenugreek)",
    "SMHB00422": "Xihonghua (saffron)",
    "SMHB00671": "Heizhongcaozi (nigella)",
    "SMHB00372": "Shiliupi (pomegranate rind)",
    "SMHB00133": "Gancao (licorice)",
}
TABLES = {"TCM_symptom": "herb_tcm_symptom_relations.csv", "MM_symptom": "herb_mm_symptom_relations.csv",
          "Syndrome": "herb_syndrome_relations.csv", "Disease": "herb_disease_relations.csv"}


def fetch(herb, table):
    body = urllib.parse.urlencode({"rrid": herb, "table_name": table, "filter": 0}).encode()
    req = urllib.request.Request(URL, data=body, headers={"User-Agent": "medical-kg research (polite, 1 req/s)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8")).get("data") or []


def main():
    n_req = 0
    for table, fname in TABLES.items():
        path = data("symmap", "scrape", fname)
        cur = pd.read_csv(path, dtype=str, keep_default_na=False)
        have = set(cur.source_herb_id)
        new = []
        for herb, label in HERBS.items():
            if herb in have:
                continue
            try:
                rows = fetch(herb, table)
            except Exception as e:  # endpoint down / changed: report and continue
                print(f"  {herb} {table}: FAILED {e}")
                rows = None
            n_req += 1
            time.sleep(1.0)
            if rows is None:
                continue
            for r in rows:
                r = {k: ("" if v is None else str(v)) for k, v in r.items()}
                r["source_herb_id"], r["source_herb"] = herb, label
                new.append(r)
            print(f"  {herb} {table}: {len(rows)} rows")
        if new:
            df = pd.DataFrame(new)
            for c in cur.columns:
                if c not in df.columns:
                    df[c] = ""
            pd.concat([cur, df[cur.columns]], ignore_index=True).to_csv(path, index=False)
            print(f"{fname}: +{len(new)} rows")
    print(f"{n_req} requests")


if __name__ == "__main__":
    main()
