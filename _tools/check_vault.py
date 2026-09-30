"""Integrity check: required properties, questions<->q/ tag agreement, candidate notes,
dataset notes (enums, country/region links, schema profile when accessed), duplicate arXiv ids,
and that wikilinks and embeds resolve.

Usage: python3 _tools/check_vault.py
"""
import collections, glob, os, re

VAULT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(VAULT)
notes = {os.path.basename(p)[:-3] for p in glob.glob("**/*.md", recursive=True) if not p.startswith((".", "_tools"))}
files = {os.path.basename(p) for p in glob.glob("**/*", recursive=True) if os.path.isfile(p)}
PAPER_REQ = ["title", "authors", "year", "published", "venue", "peer_reviewed", "url", "pdf", "pdf_url",
             "topics", "questions", "relevance", "tags"]
CAND_REQ = ["title", "topics", "status", "tags"]
STATUSES = {"candidate", "processing", "processed", "rejected"}
DATASET_REQ = ["title", "slug", "kind", "availability", "access_link", "accessed", "access_method",
               "countries", "regions", "topics", "questions", "tags"]
DATASET_ENUMS = {
    "availability": {"open-download", "open-api", "open-web", "registration", "on-request", "contact-authors",
                     "commercial", "unavailable"},
    "accessed": {"true", "false", "partial"},
    "has_amounts": {"yes", "partial", "no", ""},
    "has_cooking_method": {"steps", "tags", "no", ""},
    "body_effect": {"direct", "linkable", "no", ""},
}
KINDS = {"food", "ingredient", "compound"}
problems = []
arxiv_ids = collections.defaultdict(list)


def frontmatter(s):
    return s[4:].split("\n---\n", 1)[0] if s.startswith("---\n") else ""


def prop(fm, key):
    m = re.search(rf"^{key}:\s*['\"]?([^'\"\n]*)", fm, re.M)
    return m.group(1).strip() if m else None


def prop_list(fm, key):
    """Values of an inline `[a, b]` or block `- a` YAML list (quotes and [[ ]] stripped)."""
    m = re.search(rf"^{key}:[ \t]*(\[.*\])?[ \t]*\n((?:[ \t]+-.*\n?)*)", fm + "\n", re.M)
    if not m:
        return []
    raw = re.findall(r"\[\[[^\]]+\]\]|[^,\[\]]+", m.group(1)[1:-1]) if m.group(1) else []
    raw += re.findall(r"^[ \t]+-[ \t]*(.+)$", m.group(2), re.M)
    vals = (v.strip().strip("'\"").strip("[]").split("|")[0].strip() for v in raw)
    return [v for v in vals if v]


scan = [p for d in ("Papers", "Questions", "Sessions", "Backlog", "Datasets", "Countries", "Regions", "Database")
        for p in glob.glob(f"{d}/*.md")] + ["Backlog.md"]
countries = {os.path.basename(p)[:-3] for p in glob.glob("Countries/*.md")}
regions = {os.path.basename(p)[:-3] for p in glob.glob("Regions/*.md")}
for p in sorted(scan):
    if not os.path.exists(p):
        continue
    s = open(p).read()
    fm = frontmatter(s)
    if p.startswith("Papers/"):
        for k in PAPER_REQ:
            if prop(fm, k) is None:
                problems.append(f"{p}: missing property {k}")
        qs = re.search(r"^questions:\s*\[(.*)\]", fm, re.M)
        qs = {q.strip() for q in qs.group(1).split(",")} if qs else set()
        tags = {t.replace("-", ".").upper() for t in re.findall(r"q/([\d-]+)", fm)}
        if {q.upper() for q in qs} != {"Q" + t for t in tags}:
            problems.append(f"{p}: questions {sorted(qs)} vs q/ tags {sorted(tags)}")
    if p.startswith("Backlog/"):
        for k in CAND_REQ:
            if prop(fm, k) is None:
                problems.append(f"{p}: missing property {k}")
        st = prop(fm, "status")
        if st not in STATUSES:
            problems.append(f"{p}: status {st!r} not in {sorted(STATUSES)} (processed papers belong in Papers/)")
        if st == "candidate" and prop(fm, "priority") not in {"1", "2", "3"}:
            problems.append(f"{p}: candidate needs priority 1-3")
        if st == "processed" and not prop(fm, "dataset"):
            problems.append(f"{p}: processed candidate needs dataset: \"[[<dataset note>]]\"")
        if st == "rejected" and not prop(fm, "reason"):
            problems.append(f"{p}: rejected candidate needs a reason")
    if p.startswith("Datasets/"):
        for k in DATASET_REQ:
            if prop(fm, k) is None:
                problems.append(f"{p}: missing property {k}")
        for k, allowed in DATASET_ENUMS.items():
            v = prop(fm, k)
            if v is not None and v not in allowed:
                problems.append(f"{p}: {k} {v!r} not in {sorted(allowed - {''})}")
        kinds = set(prop_list(fm, "kind"))
        if not kinds or kinds - KINDS:
            problems.append(f"{p}: kind {sorted(kinds)} must be a non-empty subset of {sorted(KINDS)}")
        if "food" in kinds and prop(fm, "has_ingredients") in (None, ""):
            problems.append(f"{p}: food dataset needs has_ingredients / has_amounts / has_cooking_method")
        if kinds & {"ingredient", "compound"} and prop(fm, "body_effect") in (None, ""):
            problems.append(f"{p}: ingredient/compound dataset needs body_effect + body_effect_how")
        for c in prop_list(fm, "countries"):
            if c not in countries:
                problems.append(f"{p}: country [[{c}]] has no note in Countries/")
        for r in prop_list(fm, "regions"):
            if r not in regions:
                problems.append(f"{p}: region [[{r}]] has no note in Regions/")
        slug = prop(fm, "slug")
        if prop(fm, "accessed") in ("true", "partial") and not os.path.exists(f"Data/{slug}/schema.md"):
            problems.append(f"{p}: accessed but Data/{slug}/schema.md missing (run _tools/profile_dataset.py)")
    if p.startswith("Papers/") or (p.startswith("Backlog/") and prop(fm, "status") != "processed"):
        a = prop(fm, "arxiv")  # processed dataset candidates share the arXiv id of their paper note
        if a and re.fullmatch(r"\d{4}\.\d{4,5}", a):
            arxiv_ids[a].append(p)
    s = re.sub(r"`[^`\n]*`", "", s)  # links inside inline code are not links
    for emb, tgt in re.findall(r"(!?)\[\[([^\]|#]+)", s):
        tgt = tgt.strip().rstrip("\\").strip()  # "\|" is an escaped alias pipe inside tables
        ok = tgt in notes or tgt in files or os.path.basename(tgt) in files or tgt + ".md" in files
        if not ok:
            problems.append(f"{p}: unresolved {'embed' if emb else 'link'} [[{tgt}]]")

# Obsidian resolves [[Name]] by file name, so the same name in two folders makes links ambiguous
by_name = collections.defaultdict(list)
for p in glob.glob("**/*.md", recursive=True):
    if not p.startswith((".", "_tools", "Templates", "Access-help", "Data/", "db/")):
        by_name[os.path.basename(p)].append(p)
for n, ps in by_name.items():
    if len(ps) > 1:
        problems.append(f"duplicate note name {n!r} (links are ambiguous): " + " | ".join(sorted(ps)))

for a, ps in arxiv_ids.items():
    if len(ps) > 1:
        problems.append(f"duplicate arXiv {a}: " + " | ".join(ps))

print("\n".join(problems) or "OK: no problems")
print(f"{len(glob.glob('Papers/*.md'))} paper, {len(glob.glob('Datasets/*.md'))} dataset, "
      f"{len(countries)} country, {len(regions)} region, {len(glob.glob('Backlog/*.md'))} candidate notes checked")
