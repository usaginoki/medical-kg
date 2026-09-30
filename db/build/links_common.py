"""Helpers shared by the `links` stage modules (db/build/links*.py).

Resolvers are applied to the *distinct* source keys only; the resulting (key -> id) tables are loaded as DuckDB
temp tables and joined in SQL, so large sources (FooDB Content, 5M rows) never go through Python row by row.
"""
import re, time

import pandas as pd

T0 = time.time()


def log(msg):
    print(f"  [links {time.time() - T0:6.1f}s] {msg}", flush=True)


def s(x):
    """Clean scalar: None for NaN / '' / 'NA' / 'n.a.'."""
    if x is None:
        return None
    if isinstance(x, float) and x != x:
        return None
    t = str(x).strip()
    return None if t in ("", "NA", "N/A", "n.a.", "nan", "NaN", "None", "-") else t


def lookup_table(con, name, keys, fn):
    """Create TEMP TABLE name(k VARCHAR, v VARCHAR) with v = fn(k) for each distinct non-null key (hits only).

    fn may return an id, a resolver tuple (id, method, score) or None."""
    out = []
    for k in set(keys):
        if k is None:
            continue
        v = fn(k)
        if isinstance(v, tuple):
            v = v[0]
        if v:
            out.append((str(k), v))
    df = pd.DataFrame(out, columns=["k", "v"])
    con.register("_lk_df", df)
    con.execute(f"CREATE OR REPLACE TEMP TABLE {name} AS SELECT k, v FROM _lk_df")
    con.unregister("_lk_df")
    return len(df)


def df_to_temp(con, name, df):
    con.register("_tmp_df", df)
    con.execute(f"CREATE OR REPLACE TEMP TABLE {name} AS SELECT * FROM _tmp_df")
    con.unregister("_tmp_df")


class CondText:
    """Free text -> list of (condition_id, direction, method, score).

    A hit on an action (ACT:…, e.g. 'antiemetic') is replaced by the action's target conditions with the direction
    from db/maps/action_map.csv; a plain condition hit gets `default_direction`. Results are cached per term.
    """

    def __init__(self, cr):
        self.cr = cr
        self.cache = {}

    def hits(self, term, default_direction, actions_only=False):
        term = s(term)
        if not term:
            return []
        key = (term, default_direction, actions_only)
        if key in self.cache:
            return self.cache[key]
        r = self.cr.by_text_scored(term)
        out = []
        if r:
            cid, method, score = r
            if cid.startswith("ACT:"):
                out = [(t, self.cr.action_direction(cid, t) or "beneficial", f"action:{cid}", score)
                       for t in self.cr.action_targets(cid)]
            elif not actions_only:
                out = [(cid, default_direction, method, score)]
        self.cache[key] = out
        return out


def icd11_resolver(con, cr):
    """ICD-11 code -> condition id, following same_as to the MEDIC (preferred) or UMLS twin when present."""
    twin = {}
    for f, t in con.execute("""SELECT from_id, to_id FROM condition_relation WHERE rel = 'same_as'
                               AND from_id LIKE 'ICD11:%' ORDER BY (to_id LIKE 'MESH:%') DESC, to_id""").fetchall():
        twin.setdefault(f, t)

    def f(code):
        c = cr.by_icd11(code)
        return twin.get(c, c) if c else None
    return f


def xref_alias_map(con, prefix):
    """condition_alias xref aliases '<PREFIX>:<id>' -> condition_id (e.g. OMIM, SYMMAP)."""
    d = {}
    for cid, a in con.execute("""SELECT a.condition_id, a.alias FROM condition_alias a JOIN condition c USING (condition_id)
                                 WHERE a.lang = 'xref' AND a.alias LIKE ? ORDER BY c.source_vocab = 'medic' DESC, a.condition_id""",
                              [prefix + ":%"]).fetchall():
        d.setdefault(a.split(":", 1)[1], cid)
    return d


PMID_RE = re.compile(r"\d{5,9}")


def pmids(text):
    """'PMID[123] 456; 789' -> '123|456|789' (None if no ids)."""
    if text is None:
        return None
    ids = list(dict.fromkeys(PMID_RE.findall(str(text))))
    return "|".join(ids) if ids else None
