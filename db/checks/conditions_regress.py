"""Regression checks for condition and compound matching and the link stage (audit of 2026-10-14): the wrong matches
found then, as inputs with the expected outcome. Needs a built database (stages conditions, compounds, links).
Run: UNIFIED_DB=<path> uv run db/checks/conditions_regress.py"""
import os, sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from common import connect  # noqa: E402
from build.resolve import CompoundResolver, ConditionResolver  # noqa: E402
from build.links_common import CondText  # noqa: E402

# ConditionResolver.by_text: text -> expected condition id (None = must not match)
CONDITIONS = [
    # tie-break: MEDIC's own synonym and MeSH descriptors beat HERB aliases on familial / genetic concepts
    ("Breast cancer", "MESH:D001943"),          # not 'Breast Cancer, Familial'
    ("Prostate cancer", "MESH:D011471"),        # not 'Prostate cancer, familial'
    ("Liver cancer", "MESH:D008113"),           # not 'Hepatoblastoma Caused By Somatic Mutation'
    ("Lung cancer", "MESH:D008175"),            # not 'Adenocarcinoma of Lung'
    ("Pancreatic cancer", "MESH:D010190"),      # not 'Pancreatic carcinoma, familial'
    ("Colorectal cancer", "MESH:D015179"),      # not 'Colonic Neoplasms'
    ("Colon and rectal cancer", "MESH:D015179"),
    ("Gastric cancer", "MESH:D013274"),
    ("Stomach cancer", "MESH:D013274"),
    ("Sore", "MESH:D012883"),                   # not 'Tenderness'
    ("Cirrhosis", "MESH:D008103"),              # not 'Fibrosis'
    ("Kidney stones", "MESH:D007669"),          # not 'Nephrolithiasis, Calcium Oxalate'
    # acronyms: case-sensitive, curated ones first
    ("PTSD", "MESH:D013313"),                   # not 6-pyruvoyl-tetrahydropterin synthase deficiency
    ("IBS", "MESH:D043183"),                    # not Ichthyosis Bullosa of Siemens
    ("HCV", "MESH:D006526"),                    # not Coronaviridae Infections
    ("HIV", "MESH:D015658"),
    ("UTI", "MESH:D014552"),
    ("HTN", "MESH:D006973"),
    ("CKD", "MESH:D051436"),
    ("CAD", "MESH:D003324"),
    ("AD", "MESH:D000544"),                     # Alzheimer Disease, not 'familial, type 3'
    ("face", None),                             # MEDIC 'FACE' = Fanconi anemia group E
    ("Candle", None),                           # MEDIC 'CANDLE' syndrome
    # lay / organ words from HERB and SymMap
    ("tongue", None), ("mouth", None), ("lip", None), ("breast", None), ("brain", None), ("penis", None),
    ("testis", None), ("heat", None), ("wind", None), ("dry", None), ("sleep", None), ("appetite", None),
    ("beauty", None), ("sweat", None),
    ("Liver", "MESH:D008107"),                  # organ word -> the organ's diseases stays
    # fuzzy: numbers and sex must agree
    ("disorder of female genital organs", "MESH:D005831"),   # curated; fuzzy alone gave 'Genital Diseases, Male'
    ("herpesvirus 1, human", None),             # fuzzy gave 'Herpesvirus 3, Human'
    ("herpesvirus 2, human", None),
    # still matched
    ("Cough", "MESH:D003371"),
    ("Ache(Stomach)", "MESH:D015746"),
    ("Osteoarthritis\t Knee", "MESH:D020370"),
]

# CondText: term -> {condition id: direction} that must all be among the hits (empty dict = no hits at all)
LINK_TERMS = [
    ("hits_multi", "Diabetic Nephropathy|Proteinuria", "association",
     {"MESH:D003928": "association", "MESH:D011507": "association"}),
    ("hits_multi", "Gastric and oesophageal cancer", "association",
     {"MESH:D013274": "association", "MESH:D004938": "association"}),
    ("hits_multi", "Head and neck cancer", "association", {"MESH:D006258": "association"}),
    ("hits", "Preventing", "beneficial", {}),
    ("hits", "Poison", "beneficial", {"MESH:D011041": "harmful"}),
    ("hits", "Piscicide", "beneficial", {"MESH:D011041": "harmful"}),
    ("hits", "Narcotic", "beneficial", {"MESH:D011041": "harmful"}),
    ("hits", "ACE-Inhibitor", "association", {"MESH:D006973": "beneficial"}),
    ("hits", "Vasodilator", "association", {"MESH:D006973": "beneficial"}),
    ("hits", "Nervine", "beneficial", {"MESH:D001008": "beneficial"}),
    ("hits", "Hypercholesterolemic", "association", {"MESH:D006937": "harmful"}),
    ("hits", "Hyperthermic", "association", {"MESH:D005334": "harmful"}),   # SymMap alias of Fever loses to the action
    ("hits", "Anorexic", "association", {"MESH:D000855": "harmful"}),
    ("hits", "Emetic", "beneficial", {"MESH:D014839": "harmful"}),
    ("hits", "Tonic", "beneficial", {}),
    ("hits", "Antioxidant", "association", {}),
]

# CompoundResolver.by_name (non-strict, as for Duke AGGREGAC / Phenol-Explorer): name -> expected compound
# (None = no match; a string = the compound's name must equal it, case-insensitive)
COMPOUNDS = [
    ("RESIN", "Resin"),                         # the class record, not urea formaldehyde foam
    ("GUM", None),                              # not a trihydroxyflavan
    ("FLAVONOIDS", "Flavonoids"),               # not Rutin
    ("SUGARS", "Sugars"),                       # not Sucrose
    ("LECITHIN", "Lecithins"),                  # not PC(16:0/18:1(9Z))
    ("TANNIN", None),                           # not Tannic acid
    ("PINENE", None),                           # alpha or beta?
    ("CAROTENE", None),
    ("ESSENTIAL-OIL", "Oils, Volatile"),
    ("EPICATECHIN", "Epicatechin"),             # not (+)-Catechin
    ("(-)-EPICATECHIN", "Epicatechin"),
    ("ADENINE", "Adenine"),                     # not Glycine
    ("5-HYDROXYTRYPTAMINE", "Serotonin"),       # synonym-only, one structure dominates
    ("PABA", None),                             # synonym of 4-aminobenzoic and 4-hydroxybenzoic acid
    ("6-gingerol", "gingerol"),                 # the shared InChIKey compound
    ("CURCUMIN", "Curcumin"),
    ("QUERCETIN", "Quercetin"),
]


def main():
    con = connect(read_only=True)
    kr, cr = ConditionResolver(con), CompoundResolver(con)
    ct = CondText(kr)
    name = lambda cid: kr.info[cid][1] if cid in kr.info else cid
    fails = []
    for text, want in CONDITIONS:
        got = kr.by_text(text)
        if got != want:
            fails.append(f"condition {text!r}: got {got} ({name(got)}), want {want} ({name(want)})")
    for fn, text, default, want in LINK_TERMS:
        hits = {h[0]: h[1] for h in getattr(ct, fn)(text, default)}
        if (not want and hits) or any(hits.get(c) != d for c, d in want.items()):
            fails.append(f"{fn} {text!r}: got {hits}, want {want}")
    cname = dict(con.execute("SELECT compound_id, name FROM compound").fetchall())
    for text, want in COMPOUNDS:
        got = cr.by_name(text)
        ok = got is None if want is None else (got is not None and cname.get(got, "").lower() == want.lower())
        if not ok:
            fails.append(f"compound {text!r}: got {got} ({cname.get(got)}), want {want}")
    # link-table invariants (a query on a column the file does not have yet counts as a failure)
    def q(sql):
        try:
            return con.execute(sql).fetchone()[0]
        except Exception:
            return float("nan")
    checks = [
        ("evidence type in_vitro registered", q("SELECT count(*) FROM evidence_type WHERE code = 'in_vitro'") == 1),
        ("Duke activities are in_vitro", q("SELECT count(*) FROM compound_condition WHERE source_id = 'duke' "
                                           "AND evidence_type <> 'in_vitro'") == 0),
        ("FooDB keeps only ChEBI health effects", q("SELECT count(*) FROM compound_condition WHERE source_id = 'foodb' "
                                                    "AND evidence_type <> 'curated_literature'") == 0),
        ("compound_condition notes filled", q("SELECT count(*) FROM compound_condition WHERE note IS NULL") == 0),
        ("animal-model conditions flagged", q("SELECT count(*) FROM condition WHERE animal_model") >= 14),
        ("animal-model links noted", q("SELECT count(*) FROM compound_condition cc JOIN condition c USING (condition_id) "
                                       "WHERE c.animal_model AND cc.note NOT LIKE 'animal model%'") == 0),
        ("Exposome breast cancer -> Breast Neoplasms",
         q("SELECT count(*) FROM compound_condition WHERE source_id = 'exposome' AND condition_id = 'MESH:D001943'") > 0
         and q("SELECT count(*) FROM compound_condition WHERE source_id = 'exposome' AND condition_id = 'MESH:C562840'") == 0),
        ("ICD-11 'Breast cancer' same_as Breast Neoplasms",
         q("SELECT count(*) FROM condition_relation WHERE rel = 'same_as' AND from_id = 'ICD11:2C60-2C65' "
           "AND to_id = 'MESH:D001943'") == 1),
    ]
    fails += [f"invariant failed: {label}" for label, ok in checks if not ok]
    n = len(CONDITIONS) + len(LINK_TERMS) + len(COMPOUNDS) + len(checks)
    for f in fails:
        print("FAIL", f)
    print(f"{n - len(fails)}/{n} checks passed")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
