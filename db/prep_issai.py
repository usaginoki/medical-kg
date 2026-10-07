"""Build tidy CSVs from the ISSAI LLM_for_Dietary_Recommendation_System zips (Datasets/ISSAI Dietary Recommendation
profiles.md): derived/cases_responses.csv (250 rows: 50 profiles x 5 zips) and derived/profiles.csv (50 rows).

Usage: uv run db/prep.py issai   (or: python3 db/prep_issai.py <Data/issai-dietary-recommendation>)

Profile and GPT-4 answer are split heuristically (see the dataset note); spot-check the boundaries.
"""
import csv, io, os, re, sys, zipfile

root = sys.argv[1]
ZIPS = {  # zip -> (language, pipeline)
    'cases_results.zip': ('en', 'direct'),
    'cases_results_1.zip': ('ru', 'direct'),
    'cases_results_1_tr.zip': ('ru', 'translated'),
    'cases_results_2.zip': ('kk', 'direct'),
    'cases_results_2_tr.zip': ('kk', 'translated'),
}
PROMPTS = {
    'en': 'Provide dietary recommendation for this patient profile.',
    'ru': 'Предоставьте рекомендации по питанию для данного пациента.',
    'kk': 'Oсы науқас/пациент профилі үшін тамақтану бойынша кеңес беріңіз.',
}
PLAN = {
    'en': 'Give a specific diet plan for the day based on the patient profile using Central Asian food.',
    'ru': 'Предложите конкретный план питания на день, основанный на профиле пациента с использованием центральноазиатской пищи.',
}
START = re.compile(r'\s(?=(Dietary [Rr]ecommendation|Based on|Given |The following dietary|Рекомендации по питанию|На основе|Основываясь|Судя по|Учитывая|В свете|Дорогая|Ваши рекомендации|Питание играет|Важно помочь|Основные рекомендации)\b)')

def looks_like_response(seg):
    seg = seg.strip()
    if seg[:1].islower():
        return False
    return bool(START.match(' ' + seg) or re.match(r'\d+\.\s', seg) or seg.endswith(':') or len(seg) < 60)

def split_profile(body):
    body = body.lstrip()
    first = body.split('\n', 1)[0]
    m = START.search(first)
    if m and m.start() > len(first) * 0.4:
        return body[:m.start()].strip(), body[m.start():].strip()
    runs = [r for r in re.finditer(r' {2,}', first) if first[r.end():].strip()]
    if runs and looks_like_response(first[runs[-1].end():]):
        cut = runs[-1].start()
        return body[:cut].strip(), body[cut:].strip()
    return first.strip(), body[len(first):].strip()

raw = {}
for zname, (lang, pipe) in ZIPS.items():
    with zipfile.ZipFile(os.path.join(root, 'Cases_and_Responses', zname)) as z:
        for info in z.infolist():
            n = info.filename
            if n.endswith('/') or '__MACOSX' in n:
                continue
            base = os.path.basename(n)
            case_id = int(base.split('_')[0])
            t = z.read(n).decode('utf-8', errors='replace')
            p = PROMPTS[lang]
            body = (t[t.index(p) + len(p):] if p in t else t).lstrip()
            plan_sep = PLAN['en'] if lang == 'en' else PLAN['ru']
            first, plan = body.split(plan_sep, 1) if plan_sep in body else (body, '')
            raw[(case_id, lang, pipe)] = (f'{zname}:{base}', first, plan)

def lcp_split(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    cut = a.rfind(' ', 0, i + 1) if i < len(a) and not a[i - 1].isspace() else i
    return cut

rows = []
for (case_id, lang, pipe), (src, first, plan) in raw.items():
    if lang == 'en':
        profile, rec = split_profile(first)
    else:
        other = raw[(case_id, lang, 'translated' if pipe == 'direct' else 'direct')][1]
        cut = lcp_split(first, other)
        # a shared response opening (>=3-space separator inside the common prefix) belongs to the response
        runs = [r for r in re.finditer(r' {3,}', first[:cut])]
        if runs and cut - runs[-1].end() < 400:
            cut = runs[-1].start()
        # common prefix stopped one or two words early: move them up to the response's '1.' / newline
        m = re.match(r'([^\n]{0,60}?)(?=\s+\d+\.\s|\n)', first[cut:])
        if m and m.group(1).strip() and m.group(1).strip()[0].islower():
            cut += len(m.group(1))
        profile, rec = first[:cut].strip(), first[cut:].strip()
    rows.append(dict(case_id=case_id, language=lang, pipeline=pipe, source=src,
                     profile=profile, gpt4_recommendations=rec, gpt4_meal_plan=plan.strip()))
rows.sort(key=lambda r: (r['case_id'], ['en', 'ru', 'kk'].index(r['language']), r['pipeline']))
os.makedirs(os.path.join(root, 'derived'), exist_ok=True)
with open(os.path.join(root, 'derived', 'cases_responses.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader(); w.writerows(rows)

# one row per case: label + the three profile texts
prof = {}
for r in rows:
    d = prof.setdefault(r['case_id'], {'case_id': r['case_id']})
    if r['pipeline'] == 'direct' or f"profile_{r['language']}" not in d:
        d[f"profile_{r['language']}"] = r['profile']
for d in prof.values():
    en = d.get('profile_en', '')
    m = re.match(r'(.*?)\s*Name:', en)
    d['case_label_en'] = (m.group(1).strip() if m else '')
    dm = re.search(r'Diagnosis:\s*(.*?)(?=\s(?:Date of diagnosis|Diagnosed|Medical History|Symptoms|Current Medication|Medications)\b|$)', en)
    d['diagnosis_en'] = dm.group(1).strip()[:150] if dm else ''
    mm = re.search(r'(?:[Cc]urrent )?[Mm]edications?:\s*(.*?)(?=\s(?:Diet|Anthropometr|Biochemical|Environmental|Clinical|Lifestyle|Family|Allerg|Underlying|Impaired)\b|$)', en)
    d['medications_en'] = mm.group(1).strip()[:200] if mm else ''
cols = ['case_id', 'case_label_en', 'diagnosis_en', 'medications_en', 'profile_en', 'profile_ru', 'profile_kk']
with open(os.path.join(root, 'derived', 'profiles.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader(); w.writerows(sorted(prof.values(), key=lambda d: d['case_id']))
print(len(rows), 'response rows;', len(prof), 'profiles')
