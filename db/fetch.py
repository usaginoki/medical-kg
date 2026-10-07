"""Download the raw datasets that db/build.py reads into Data/<slug>/ (git-ignored).

Usage:
  uv run db/fetch.py                 # every scripted source
  uv run db/fetch.py ctd foodcom     # selected sources
  uv run db/fetch.py --list

Each source is idempotent: files that already exist are skipped, and curl resumes partial downloads. FooDB and HMDB
sit behind a Cloudflare browser check, so they are downloaded by hand into Data/foodb/raw/ and Data/hmdb/raw/;
`foodb` and `hmdb` here only unpack those files. Scraped and PDF-extracted inputs are not handled here.
"""
import argparse, csv, glob, gzip, json, os, shutil, subprocess, sys, traceback, urllib.parse, urllib.request, zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import DATA  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"
SOURCES = {}


def source(fn):
    SOURCES[fn.__name__] = fn
    return fn


def d(*parts):
    p = os.path.join(DATA, *parts)
    os.makedirs(p, exist_ok=True)
    return p


def curl(url, dest, ua=UA, extra=()):
    """Download url to dest unless dest exists; resumes into dest.part."""
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        print(f"  skip {os.path.relpath(dest, DATA)}")
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    part = dest + ".part"
    print(f"  get  {os.path.relpath(dest, DATA)}", flush=True)
    for attempt in range(4):
        r = subprocess.run(["curl", "-fL", "--retry", "3", "-C", "-", "-sS", "-A", ua, *extra, "-o", part, url])
        if r.returncode == 0:
            os.replace(part, dest)
            return dest
        if r.returncode == 33:  # server does not support resume: restart
            os.remove(part)
    raise RuntimeError(f"curl failed ({r.returncode}): {url}")


def unzip(zpath, dest, members=None, flatten=False):
    with zipfile.ZipFile(zpath) as z:
        for m in z.infolist():
            if m.is_dir() or "__MACOSX" in m.filename or (members and os.path.basename(m.filename) not in members):
                continue
            out = os.path.join(dest, os.path.basename(m.filename) if flatten else m.filename)
            if os.path.exists(out):
                continue
            os.makedirs(os.path.dirname(out), exist_ok=True)
            with z.open(m) as src, open(out, "wb") as dst:
                shutil.copyfileobj(src, dst)


def hf_file(repo, path, dest_dir, repo_type="dataset"):
    from huggingface_hub import hf_hub_download
    out = os.path.join(dest_dir, os.path.basename(path))
    if os.path.exists(out):
        print(f"  skip {os.path.relpath(out, DATA)}")
        return out
    print(f"  get  {os.path.relpath(out, DATA)}", flush=True)
    p = hf_hub_download(repo, path, repo_type=repo_type)
    shutil.copy(p, out)
    return out


# ---- compounds and health effects ---------------------------------------------------------------------------------

@source
def ctd():
    base = d("ctd")
    raw = d("ctd", "raw")
    for f in ["CTD_chemicals.tsv.gz", "CTD_chemicals_diseases.tsv.gz", "CTD_diseases.tsv.gz"]:
        curl(f"https://ctdbase.org/reports/{f}", os.path.join(raw, f))
    if not os.path.exists(f"{base}/CTD_diseases.tsv.gz"):
        shutil.copy(f"{raw}/CTD_diseases.tsv.gz", f"{base}/CTD_diseases.tsv.gz")

    def strip(src, dst, header, keep=lambda cols: True):
        if os.path.exists(dst):
            return
        n = 0
        with gzip.open(src, "rt", encoding="utf-8") as fi, open(dst + ".part", "w", encoding="utf-8") as fo:
            fo.write("\t".join(header) + "\n")
            for line in fi:
                if line.startswith("#"):
                    continue
                cols = line.rstrip("\n").split("\t")
                if keep(cols):
                    fo.write(line)
                    n += 1
        os.replace(dst + ".part", dst)
        print(f"  wrote {os.path.basename(dst)}: {n:,} rows")

    strip(f"{raw}/CTD_chemicals.tsv.gz", f"{base}/CTD_chemicals.tsv",
          ["ChemicalName", "ChemicalID", "CasRN", "PubChemCID", "PubChemSID", "DTXSID", "InChIKey", "Definition",
           "ParentIDs", "TreeNumbers", "ParentTreeNumbers", "MESHSynonyms", "CTDCuratedSynonyms"])
    # curated rows only (DirectEvidence set); the ~9.8 M gene-inferred rows are dropped
    strip(f"{raw}/CTD_chemicals_diseases.tsv.gz", f"{base}/CTD_chemicals_diseases_curated.tsv",
          ["ChemicalName", "ChemicalID", "CasRN", "DiseaseName", "DiseaseID", "DirectEvidence", "InferenceGeneSymbol",
           "InferenceScore", "OmimIDs", "PubMedIDs"],
          keep=lambda c: len(c) > 5 and c[5] != "")


@source
def exposome():
    base = d("exposome-explorer")
    for n in ["biomarkers", "cancer_associations", "concentrations", "correlations", "environmental_pollutants",
              "metabolomic_associations", "microbial_metabolite_identifications", "microbial_metabolites",
              "publications", "reproducibilities"]:
        z = curl(f"http://exposome-explorer.iarc.fr/system/downloads/current/{n}.csv.zip", f"{base}/raw/{n}.csv.zip")
        unzip(z, base, flatten=True)


@source
def phenol():
    base = d("phenol-explorer")
    for n in ["composition-data.xlsx", "foods.csv", "foods-classification.csv", "compounds.csv",
              "compounds-classification.csv", "compounds-structures.csv", "metabolites.csv",
              "metabolites-structures.csv", "publications.csv"]:
        z = curl(f"http://phenol-explorer.eu/system/downloads/current/{n}.zip", f"{base}/raw/{n}.zip")
        unzip(z, base, flatten=True)


@source
def npass():
    base = d("npass")
    for n in ["naturalproducts_generalinfo.txt", "naturalproducts_species_pair.txt", "species_info.txt",
              "naturalproducts_structure.txt", "activities.txt", "target.txt", "toxicity.txt",
              "Coculture.tsv", "Elicitation.tsv", "Engineer.tsv", "Symbiont.tsv"]:
        curl(f"https://bidd.group/NPASS/downloadFiles/NPASS3.0_{n}", f"{base}/NPASS3.0_{n}")


@source
def cmaup():
    base = d("cmaup")
    for n in ["Plants", "Ingredients_All", "Ingredients_onlyActive", "Targets", "Plant_Human_Disease_Associations",
              "Plant_Clinical_Trials_Associations", "Plant_Ingredient_Associations_allIngredients",
              "Plant_Ingredient_Associations_onlyActiveIngredients",
              "Ingredient_Target_Associations_ActivityValues_References",
              "Human_Oral_Bioavailability_information_of_Ingredients_All"]:
        curl(f"https://bidd.group/CMAUP/downloadFiles/CMAUPv2.0_download_{n}.txt", f"{base}/CMAUPv2.0_download_{n}.txt")
    curl("https://bidd.group/CMAUP/downloadFiles/Download_Readme.txt", f"{base}/Download_Readme.txt")
    # the two plant-ingredient files ship without a header line
    for n in ["allIngredients", "onlyActiveIngredients"]:
        p = f"{base}/CMAUPv2.0_download_Plant_Ingredient_Associations_{n}.txt"
        with open(p, encoding="utf-8", newline="") as f:
            first = f.readline()
        if not first.startswith("Plant_ID"):
            tmp = p + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="") as fo, open(p, encoding="utf-8", newline="") as fi:
                fo.write("Plant_ID\tIngredient_ID\n")
                shutil.copyfileobj(fi, fo)
            os.replace(tmp, p)
            print(f"  added header to {os.path.basename(p)}")


@source
def ddid():
    base = d("ddid")
    for n in ["Interaction", "Drug", "Food", "Herb", "Target", "Disease", "NP"]:
        url = f"https://bddg.hznu.edu.cn/ddid/static/download/{n}%20Information.csv"
        curl(url, f"{base}/{n.lower()}_information.csv", extra=["--max-time", "1800"])


@source
def usda():
    base = d("usda-fooddata-central")
    for n in ["FoodData_Central_foundation_food_csv_2026-04-30", "FoodData_Central_sr_legacy_food_csv_2018-04"]:
        z = curl(f"https://fdc.nal.usda.gov/fdc-datasets/{n}.zip", f"{base}/raw/{n}.zip")
        unzip(z, base)


@source
def foodb():
    base = d("foodb")
    tars = glob.glob(f"{base}/raw/foodb_*csv*.tar*")
    if not tars:
        print("  MANUAL: download foodb_2020_4_7_csv.tar.gz from https://foodb.ca/downloads into Data/foodb/raw/")
        return
    if os.path.exists(f"{base}/Content.csv"):
        print("  skip (already unpacked)")
        return
    # the .tar.gz is really an uncompressed tar; tar -xf handles both
    subprocess.run(["tar", "-xf", tars[0], "-C", f"{base}/raw"], check=True)
    for p in glob.glob(f"{base}/raw/**/*.csv", recursive=True):
        shutil.move(p, os.path.join(base, os.path.basename(p)))
    print(f"  unpacked {len(glob.glob(base + '/*.csv'))} CSVs")


@source
def hmdb():
    base = d("hmdb")
    if os.path.exists(f"{base}/hmdb_metabolites.csv"):
        print("  skip (already converted)")
        return
    zips = glob.glob(f"{base}/raw/hmdb_metabolites*.zip")
    if not zips:
        print("  MANUAL: download hmdb_metabolites.zip (All Metabolites, XML) from https://hmdb.ca/downloads "
              "into Data/hmdb/raw/")
        return
    hmdb_to_csv(zips[0], base)


def hmdb_to_csv(zpath, base):
    """Stream the 6.5 GB All-Metabolites XML (without unpacking it) into the CSVs the build reads."""
    import xml.etree.ElementTree as ET
    ns = "{http://www.hmdb.ca}"
    q = lambda path: "/".join(ns + p for p in path.split("/"))  # 'a/b' -> '{ns}a/{ns}b'
    t = lambda e, path: (e.findtext(q(path)) or "").strip()
    met_cols = ["accession", "name", "status", "chemical_formula", "monisotopic_molecular_weight", "cas_registry_number",
                "inchikey", "smiles", "kingdom", "super_class", "class", "sub_class", "direct_parent",
                "pubchem_compound_id", "chebi_id", "kegg_id", "foodb_id", "drugbank_id", "phenol_explorer_compound_id",
                "biospecimens", "n_diseases", "n_normal_concentrations", "n_abnormal_concentrations", "description"]
    files = {k: open(f"{base}/{k}.csv.part", "w", newline="", encoding="utf-8") for k in
             ["hmdb_metabolites", "hmdb_metabolite_diseases", "hmdb_abnormal_concentrations"]}
    w = {k: csv.writer(f) for k, f in files.items()}
    w["hmdb_metabolites"].writerow(met_cols)
    w["hmdb_metabolite_diseases"].writerow(["accession", "metabolite_name", "disease_name", "omim_id", "n_references",
                                            "pubmed_ids"])
    w["hmdb_abnormal_concentrations"].writerow(["accession", "metabolite_name", "biospecimen", "concentration_value",
                                                "concentration_units", "patient_age", "patient_sex",
                                                "patient_information", "pubmed_ids"])
    pmids = lambda e: "|".join(p.text.strip() for p in e.iter(ns + "pubmed_id") if p.text and p.text.strip())
    n = 0
    with zipfile.ZipFile(zpath) as z:
        xml_name = next(m for m in z.namelist() if m.endswith(".xml"))
        with z.open(xml_name) as fh:
            for _ev, e in ET.iterparse(fh, events=("end",)):
                if e.tag != ns + "metabolite":
                    continue
                acc, name = t(e, "accession"), t(e, "name")
                tax = e.find(ns + "taxonomy")
                dis = e.findall(q("diseases/disease"))
                normal = e.findall(q("normal_concentrations/concentration"))
                abnormal = e.findall(q("abnormal_concentrations/concentration"))
                row = {c: t(e, c) for c in met_cols}
                for c in ["kingdom", "super_class", "class", "sub_class", "direct_parent"]:
                    row[c] = t(tax, c) if tax is not None else ""
                row["biospecimens"] = "|".join(
                    b.text.strip() for b in e.findall(q("biological_properties/biospecimen_locations/biospecimen"))
                    if b.text and b.text.strip())
                row["n_diseases"], row["n_normal_concentrations"] = len(dis), len(normal)
                row["n_abnormal_concentrations"] = len(abnormal)
                row["description"] = row["description"][:400]
                w["hmdb_metabolites"].writerow([row[c] for c in met_cols])
                for dz in dis:
                    refs = dz.findall(f"{ns}references/{ns}reference")
                    w["hmdb_metabolite_diseases"].writerow([acc, name, t(dz, "name"), t(dz, "omim_id"), len(refs),
                                                            pmids(dz)])
                for c in abnormal:
                    w["hmdb_abnormal_concentrations"].writerow(
                        [acc, name] + [t(c, k) for k in ["biospecimen", "concentration_value", "concentration_units",
                                                         "patient_age", "patient_sex", "patient_information"]]
                        + [pmids(c)])
                e.clear()
                n += 1
                if n % 20000 == 0:
                    print(f"  {n:,} metabolites", flush=True)
    for k, f in files.items():
        f.close()
        os.replace(f"{base}/{k}.csv.part", f"{base}/{k}.csv")
    print(f"  wrote hmdb CSVs: {n:,} metabolites")


# ---- ingredients and traditional medicine -------------------------------------------------------------------------

@source
def tmmc():
    base = d("tm-mc")
    for n in ["medicinal_material", "medicinal_compound", "chemical_property", "chemical_protein", "protein_disease",
              "prescription"]:
        curl(f"https://tm-mc.kr/download/{n}.xlsx", f"{base}/{n}.xlsx")
    curl("https://tm-mc.kr/download/README.txt", f"{base}/README.md")


@source
def imppat():
    base = d("imppat")
    for n in ["Chemical_Information_IMPPAT_Phytochemicals", "IMPPAT_Phytochemical_Plant_Association",
              "IMPPAT_TherapeuticUse_Plant_Association", "Plant_Information_IMPPAT", "Bioactivity_IMPPAT_Phytochemicals",
              "Target_IMPPAT_Phytochemicals", "IMPPAT_PolyHerbalFormulations", "IMPPAT_SingleHerbalFormulations"]:
        try:
            curl(f"https://cb.imsc.res.in/imppat/images/Batch_Download1/{n}.tsv", f"{base}/{n}.tsv")
        except RuntimeError:
            curl(f"https://cb.imsc.res.in/imppat/images/Batch_Download/{n}.tsv", f"{base}/{n}.tsv")


@source
def duke():
    base = d("dr-dukes-phytochemical-and-ethnobotanical-databases")
    meta = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://api.figshare.com/v2/articles/24660351", headers={"User-Agent": UA}), timeout=60))
    for f in meta["files"]:
        if f["name"].endswith(".zip") or f["name"].endswith(".csv"):
            p = curl(f["download_url"], f"{base}/raw/{f['name']}", ua="curl/8.0")
            if p.endswith(".zip"):
                unzip(p, base, flatten=True)
            else:
                shutil.copy(p, base)


@source
def symmap():
    base = d("symmap")
    for t in ["SMHB", "SMMS", "SMTS", "SMIT", "SMTT", "SMDE", "SMSY"]:
        for key in ["", " key"]:
            name = urllib.parse.quote(f"SymMap v2.0, {t}{key} file.xlsx")
            curl(f"http://www.symmap.org/static/download/V2.0/{name}",
                 f"{base}/symmap_v2_{t}{'_key' if key else ''}.xlsx")


@source
def herb():
    base = d("herb")
    for n in ["herb_info", "ingredient_info", "formula_info", "target_info", "disease_info", "meta_info",
              "clinical_trials", "reference_info", "experiment_info"]:
        f = f"HERB_{n}_v2.txt"
        path = f"/www/wwwroot/47.92.70.12/HERB_web/static/download_data/V2/{f}"
        curl(f"http://47.92.70.12/download/file/?file_path={urllib.parse.quote(path)}", f"{base}/{f}")


# ---- dishes and recipes -------------------------------------------------------------------------------------------

@source
def culinarydb():
    base = d("culinarydb")
    z = curl("https://cosylab.iiitd.edu.in/culinarydb/static/data/CulinaryDB.zip", f"{base}/raw/CulinaryDB.zip")
    unzip(z, base, flatten=True)


def git_clone(url, dest, marker=None, drop=()):
    """Shallow-clone url into dest, merging with the committed schema.md / samples already there.

    The clone's `.git` is dropped: a nested repository inside Data/ would bypass the vault's .gitignore rules.
    `marker` is a path (relative to dest) whose presence means the clone was already done; `drop` lists repo files to
    delete afterwards (e.g. requirements.txt, which the profiler would read as a table)."""
    if os.path.exists(os.path.join(dest, marker or "README.md")) and (marker or os.path.exists(os.path.join(dest, ".git"))):
        print(f"  skip clone {os.path.relpath(dest, DATA)}")
        return
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".clone"
    shutil.rmtree(tmp, ignore_errors=True)
    subprocess.run(["git", "clone", "--depth", "1", url, tmp], check=True,
                   env={**os.environ, "GIT_LFS_SKIP_SMUDGE": "1"})
    shutil.rmtree(os.path.join(tmp, ".git"), ignore_errors=True)
    for name in os.listdir(tmp):  # merge into dest (it already holds the committed schema.md / samples)
        target = os.path.join(dest, name)
        if not os.path.exists(target):
            shutil.move(os.path.join(tmp, name), target)
    shutil.rmtree(tmp)
    for rel in drop:
        p = os.path.join(dest, rel)
        if os.path.isdir(p):
            shutil.rmtree(p)
        elif os.path.exists(p):
            os.remove(p)


def zip_paths(root, names, zpath):
    """Move files/folders `names` (relative to root) into the zip zpath, so the profiler skips them (no samples)."""
    names = [n for n in names if os.path.exists(os.path.join(root, n))]
    if not names:
        return
    with zipfile.ZipFile(zpath, "a" if os.path.exists(zpath) else "w", zipfile.ZIP_DEFLATED) as z:
        for n in names:
            full = os.path.join(root, n)
            files = [full] if os.path.isfile(full) else [os.path.join(r, f) for r, _, fs in os.walk(full) for f in fs]
            for f in files:
                z.write(f, os.path.relpath(f, root))
    for n in names:
        full = os.path.join(root, n)
        shutil.rmtree(full) if os.path.isdir(full) else os.remove(full)


@source
def indicrecipenutri():
    base = d("indicrecipenutri")
    git_clone("https://github.com/Poshaka-Research-Lab/IndicRecipeNutri-dataset.git", base, marker="data/corpus")
    # `git lfs pull` fails ("repository exceeded its LFS budget"); the media URLs still serve the objects
    wanted = ["data/corpus/recipes_structured.parquet", "data/corpus/recipes.parquet", "data/corpus/labels.parquet",
              "data/corpus/nutrition.parquet", "data/corpus/allergens.parquet",
              "data/enrichment/ingredients_weights.parquet"]
    wanted += [os.path.relpath(p, base) for sub in ["kg", "kg_flavor"]
               for p in glob.glob(f"{base}/data/{sub}/*.parquet")]
    for rel in wanted:
        p = os.path.join(base, rel)
        with open(p, "rb") as f:
            if not f.read(40).startswith(b"version https://git-lfs"):
                print(f"  skip {rel}")
                continue
        os.remove(p)  # replace the LFS pointer with the object
        curl("https://media.githubusercontent.com/media/Poshaka-Research-Lab/IndicRecipeNutri-dataset/main/" + rel, p)


@source
def indb():
    git_clone("https://github.com/lindsayjaacks/Indian-Nutrient-Databank-INDB-.git",
              d("indian-nutrient-databank-indb"), marker="INDB.xlsx")


@source
def maff():
    base = d("our-regional-cuisines-japan-maff")
    for lang in ["jpn", "eng"]:
        hf_file("JunichiroMorita/Our-Regional-Cuisines", f"our_regional_cuisines_{lang}.csv", base)
    if not os.path.exists(f"{base}/parsed_jpn.csv"):
        print("  TODO: parse the Markdown into parsed_jpn.csv / parsed_eng.csv (parser was not committed)")


@source
def xiachufang():
    base = d("xiachufang-recipe-corpus")
    out = f"{base}/recipe_corpus_full_first80MB.jsonl"
    if os.path.exists(out):
        print("  skip")
        return
    url = "https://huggingface.co/datasets/xzm1999/XiaChuFang_Recipe_Corpus/resolve/main/recipe_corpus_full.json"
    raw = f"{base}/raw/first80MB.part.json"
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    subprocess.run(["curl", "-fL", "-sS", "-r", "0-83886079", "-o", raw, url], check=True)
    with open(raw, "rb") as f:
        data = f.read()
    with open(out, "wb") as f:
        f.write(data[:data.rfind(b"\n") + 1])  # drop the cut-off last line
    print(f"  wrote {out.rsplit('/', 1)[1]}: {data[:data.rfind(b'\n') + 1].count(b'\n'):,} recipes")


@source
def foodcom():
    base = d("food-com-recipes-and-interactions")
    names = ["RAW_recipes.csv", "interactions_train.csv", "interactions_validation.csv", "interactions_test.csv"]
    if all(os.path.exists(f"{base}/{n}") for n in names):
        print("  skip")
        return
    import kagglehub
    src = kagglehub.dataset_download("shuyangli94/food-com-recipes-and-user-interactions")
    for n in names:
        shutil.copy(os.path.join(src, n), base)
        print(f"  copied {n}")


@source
def world_wide_dishes():
    from huggingface_hub import snapshot_download
    base = d("world-wide-dishes")
    if os.path.exists(f"{base}/data"):
        print("  skip")
        return
    snapshot_download("WorldWideDishes/worldwidedishes-v1", repo_type="dataset", local_dir=base)


@source
def worldcuisines():
    hf_file("worldcuisines/food-kb-v1.1", "worldcuisines.csv", d("worldcuisines", "food-kb-v1.1"))
    hf_file("worldcuisines/location-cuisine-kb", "location_and_cuisines.csv", d("worldcuisines", "location-cuisine-kb"))


@source
def fmlama():
    base = d("fmlama")
    for p in ["data/Dishes.csv", "data/Dish_Count.json", "data/country_info.json", "data/ingredient_info_English.json",
              "data/data_filter/en/en_count.jsonl", "data/data_filter/en/en_dishes.jsonl",
              "data/templates/en_templates.jsonl", "README.md"]:
        curl(f"https://raw.githubusercontent.com/lizhou21/FmLAMA-master/main/{p}", os.path.join(base, p))


# ---- patient case datasets (topic kg-medical-eval, Questions/Q4; read by db/cases.py) -------------------------------

@source
def medicationqa():
    git_clone("https://github.com/abachaa/Medication_QA_MedInfo2019.git", d("medicationqa"),
              marker="MedInfo2019-QA-Medications.xlsx")


@source
def ngqa():
    """Benchmark CSV from the README's Google Drive link (no login) + the code repo, zipped. fndds_ingredients.csv
    (Data/ngqa/data/) came from the raw-data Drive folder by hand and is not needed by db/cases.py:
    https://drive.google.com/drive/folders/1bR_ZGGxet19GC7rbqB5y7oor4WsaGylJ"""
    base = d("ngqa")
    out = os.path.join(d("ngqa", "processed_data"), "NGQA_benchmark.csv")
    if not os.path.exists(out):
        subprocess.run(["uv", "run", "--with", "gdown", "gdown", "1CpFbd5WWjZhu20utl0X5Tsoemc1pSmgF", "-O", out],
                       check=True)
    git_clone("https://github.com/Yiyang-Ian-Li/NGQA.git", base, marker="code.zip", drop=(".gitignore",))
    zip_paths(base, ["benchmark_pipeline", "experiments", "requirements.txt"], os.path.join(base, "code.zip"))


@source
def tcm_best4sdt():
    """Data JSONs, READMEs and prompt templates of the figshare record (CC BY 4.0). The evaluation scripts and figures
    of the record (code.zip, images/ in our copy) are not needed by db/cases.py and are skipped."""
    base = d("tcm-best4sdt")
    meta = json.load(urllib.request.urlopen(urllib.request.Request(
        "https://api.figshare.com/v2/articles/30615956", headers={"User-Agent": UA}), timeout=60))
    for f in meta["files"]:
        if f["name"].endswith((".json", ".md")) and f["name"] != "config_example.json":  # that one is code config
            curl(f["download_url"], os.path.join(base, f["name"]), ua="curl/8.0")


@source
def mtcmb():
    base = d("mtcmb")
    git_clone("https://github.com/Wayyuanyuan/MTCMB.git", base, marker="data/TCM-MSDD.jsonl",
              drop=("requirements.txt", ".gitignore"))
    if os.path.exists(os.path.join(base, "LICENSE.txt")):
        os.replace(os.path.join(base, "LICENSE.txt"), os.path.join(base, "LICENSE"))


@source
def medcasereasoning():
    """Only the three split parquets (medcasereasoning_core.csv/.pqt are their union, so they are skipped)."""
    from huggingface_hub import snapshot_download
    base = d("medcasereasoning")
    if os.path.exists(os.path.join(base, "data", "test-00000-of-00001.parquet")):
        print("  skip")
        return
    snapshot_download("zou-lab/MedCaseReasoning", repo_type="dataset", local_dir=base,
                      allow_patterns=["data/*.parquet", "README.md"])


@source
def rumedbench():
    """sb-ai-lab/MedBench (continuation of pavel-blinov/RuMedBench) + RuMedPrime from Zenodo. RuMedNLI (PhysioNet
    licence, MIMIC-derived) and RuMedNER are zipped so that no samples of them are ever committed."""
    base = d("rumedbench", "medbench")
    git_clone("https://github.com/sb-ai-lab/MedBench.git", base, marker="data/RuMedTop3")
    data = os.path.join(base, "data")
    zip_paths(data, ["RuMedNLI"], os.path.join(data, "RuMedNLI.zip"))
    zip_paths(data, ["RuMedNER", "raw/RuDReC.csv"], os.path.join(data, "RuMedNER_RuDReC.zip"))
    zip_paths(base, ["code", "lb_submissions"], os.path.join(base, "code_and_lb_submissions.zip"))
    curl("https://zenodo.org/api/records/5765873/files/RuMedPrimeData.zip/content",
         os.path.join(d("rumedbench", "zenodo"), "RuMedPrimeData.zip"))


@source
def medarabiq():
    """Custom NYU licence: internal research only, no redistribution. .gitignore keeps its samples out of git."""
    git_clone("https://github.com/nyuad-cai/MedArabiQ.git", d("medarabiq"), marker="datasets/patient-doctor-qa.csv")


@source
def fam_bench():
    """Anonymous review repository: it may move after review; our snapshot is commit abfaf02 (2026-06-08)."""
    git_clone("https://github.com/anonymous-research-artifact123/Food-as-medicine.git", d("fam-bench"),
              marker="dataset/task1_dish_suitability.json")


@source
def issai_diet():
    """50 mock Kazakh patient profiles (EN/RU/KK) with GPT-4 answers; `uv run db/prep.py issai` parses the zips."""
    from huggingface_hub import snapshot_download
    base = d("issai-dietary-recommendation")
    if os.path.exists(os.path.join(base, "Cases_and_Responses")):
        print("  skip")
        return
    snapshot_download("issai/LLM_for_Dietary_Recommendation_System", repo_type="dataset", local_dir=base)


@source
def permedcqa():
    """Real Iranian patient questions with physician answers (CC BY-NC-SA 4.0); db/cases.py takes a small sample."""
    from huggingface_hub import snapshot_download
    base = d("permedcqa")
    if os.path.exists(os.path.join(base, "Data", "train.json")):
        print("  skip")
        return
    snapshot_download("NaghmehAI/PerMedCQA", repo_type="dataset", local_dir=base)


@source
def rezaei2026():
    """MedQA items with LLM-injected cultural cues (Rezaei & Shakeri 2026). The repository has no licence: local use
    only."""
    curl("https://raw.githubusercontent.com/HIVE-UofT/Evaluating-Cultural-Cues-Medical-LLMs/main/Data/"
         "final_augment_test_questions.json", f"{d('rezaei2026')}/final_augment_test_questions.json")


# ---- PDFs (extraction to CSV is a separate step) ------------------------------------------------------------------

@source
def pdfs():
    curl("https://www.sfda.gov.sa/sites/default/files/2026-04/SFCT-E.pdf",
         f"{d('saudi-food-composition-tables')}/SFCT-E.pdf")
    curl("https://www.moh.gov.bh/Content/Upload/File/638916394661198002-FCT-book-final-2025_ar.pdf",
         f"{d('bahrain-food-composition-tables')}/FCT-book-final-2025_ar.pdf")
    curl("https://ndownloader.figshare.com/files/36169554",
         f"{d('kyrgyzstan-food-composition-table')}/Kyrgyzstan_FCT_06072022.pdf", ua="curl/8.0")
    curl("https://media.githubusercontent.com/media/Central-Asian-Food-Innovation-Lab/"
         "Central-Asian-Digital-Visual-Food-Atlas/0ab8965/Atlas.pdf",
         f"{d('central-asian-digital-visual-food-atlas')}/Atlas.pdf")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sources", nargs="*")
    ap.add_argument("--list", action="store_true")
    a = ap.parse_args()
    if a.list:
        print("\n".join(SOURCES))
        return
    bad = [s for s in a.sources if s not in SOURCES]
    if bad:
        sys.exit(f"unknown sources: {bad}; see --list")
    failed = []
    for name in a.sources or SOURCES:
        print(f"[{name}]", flush=True)
        try:
            SOURCES[name]()
        except Exception as e:  # keep going; report at the end
            traceback.print_exc()
            failed.append(f"{name}: {e}")
    print("\nFAILED:\n  " + "\n  ".join(failed) if failed else "\nall done")


if __name__ == "__main__":
    main()
