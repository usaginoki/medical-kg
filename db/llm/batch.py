"""Gemini Batch API runner: submit many structured-output requests as JSONL files, poll, and collect the results into
the same SQLite cache the standard client uses (db/llm/client.py), so the scorers and db/llm/store.py read them alike.

Batch requests cost half the standard price. A ledger in .cache/llm/batch/jobs.json keeps every job, its estimated
cost before submission and its actual cost from the usage metadata after collection; a submission is refused when
estimated + already spent would pass the cap ($LLM_BATCH_MAX_USD, default 40).

Used by db/llm/full_pass.py:
  submit(task, items)   task = dict(name, model, version, system, schema, est_in_per_char, est_out)
  poll()                refresh job states
  collect()             download finished jobs into the cache; returns the items that failed validation
"""
import json, os, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from client import LLM, PRICES  # noqa: E402
from w1_run import BASE  # noqa: E402

DIR = f"{BASE}/batch"
LEDGER = f"{DIR}/jobs.json"
MAX_USD = float(os.environ.get("LLM_BATCH_MAX_USD", "40"))
MAX_LINES = 20000          # requests per job file
DONE = {"JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED", "JOB_STATE_EXPIRED"}


def batch_cost(model, tin, tout):
    pin, pout = PRICES[model]
    return (tin * pin + tout * pout) / 1e6 / 2


def load_ledger():
    return json.load(open(LEDGER)) if os.path.exists(LEDGER) else {"jobs": []}


def save_ledger(led):
    os.makedirs(DIR, exist_ok=True)
    json.dump(led, open(LEDGER, "w"), indent=1)


def committed(led):
    """USD spent (collected jobs) plus estimated (jobs not collected yet)."""
    return sum(j["actual_usd"] if j.get("collected") else j["est_usd"] for j in led["jobs"])


def submit(task, items):
    """items: [(item_id, text)]. Skips items already in the cache. Returns the job names submitted."""
    llm = LLM(task["model"])
    gen = llm.generation_config(task["schema"])
    todo = []
    for item_id, text in items:
        key = llm.key(task["version"], task["system"], text, task["schema"])
        if llm.get(key) is None:
            todo.append((item_id, key, text))
    if not todo:
        print(f"{task['name']}: all {len(items):,} items cached")
        return []
    pin, pout = PRICES[task["model"]]
    est_in = sum((len(task["system"]) + len(t)) * task["est_in_per_char"] for _, _, t in todo)
    est = (est_in * pin + len(todo) * task["est_out"] * pout) / 1e6 / 2
    led = load_ledger()
    if committed(led) + est > MAX_USD:
        raise SystemExit(f"{task['name']}: estimated ${est:.2f} + committed ${committed(led):.2f} would pass the "
                         f"${MAX_USD:.0f} cap; not submitted")
    os.makedirs(DIR, exist_ok=True)
    names = []
    for start in range(0, len(todo), MAX_LINES):
        chunk = todo[start:start + MAX_LINES]
        stem = f"{task['name']}_{int(time.time())}_{start // MAX_LINES}"
        req_path, items_path = f"{DIR}/{stem}.requests.jsonl", f"{DIR}/{stem}.items.jsonl"
        with open(req_path, "w", encoding="utf-8") as f, open(items_path, "w", encoding="utf-8") as g:
            for item_id, key, text in chunk:
                f.write(json.dumps({"key": key, "request": {
                    "contents": [{"role": "user", "parts": [{"text": text}]}],
                    "system_instruction": {"parts": [{"text": task["system"]}]},
                    "generation_config": gen}}, ensure_ascii=False) + "\n")
                g.write(json.dumps({"item_id": item_id, "key": key, "text": text}, ensure_ascii=False) + "\n")
        up = llm.client.files.upload(file=req_path, config={"mime_type": "jsonl", "display_name": stem})
        job = llm.client.batches.create(model=task["model"], src=up.name, config={"display_name": stem})
        part_est = est * len(chunk) / len(todo)
        led["jobs"].append({"name": job.name, "task": task["name"], "model": task["model"], "version": task["version"],
                            "items": items_path, "n": len(chunk), "est_usd": round(part_est, 4), "state": str(job.state),
                            "submitted": time.strftime("%Y-%m-%d %H:%M:%S"), "collected": False})
        save_ledger(led)
        names.append(job.name)
        print(f"{task['name']}: submitted {job.name} ({len(chunk):,} requests, est ${part_est:.2f})")
    return names


def poll():
    led = load_ledger()
    llm = None
    for j in led["jobs"]:
        if j["state"].split(".")[-1] in DONE:
            continue
        llm = llm or LLM(j["model"])
        job = llm.client.batches.get(name=j["name"])
        j["state"] = str(job.state)
        j["dest"] = job.dest.file_name if job.dest else None
    save_ledger(led)
    for j in led["jobs"]:
        print(f"  {j['task']:4} {j['name'].split('/')[-1][:12]} n={j['n']:>6,} {j['state'].split('.')[-1]:22} "
              f"{'collected' if j.get('collected') else ''} est ${j['est_usd']:.2f}"
              + (f" actual ${j['actual_usd']:.2f}" if j.get("collected") else ""))
    return led


def collect(schemas):
    """Download every finished, uncollected job into the cache. schemas: {task name: pydantic model}.
    Returns {task name: [item dicts that failed]} for repair with the standard client."""
    led = poll()
    failed = {}
    for j in led["jobs"]:
        if j.get("collected") or not j["state"].endswith("JOB_STATE_SUCCEEDED"):
            continue
        llm = LLM(j["model"])
        items = {x["key"]: x for x in map(json.loads, open(j["items"], encoding="utf-8"))}
        raw = llm.client.files.download(file=j["dest"]).decode("utf-8")
        tin = tout = ok = 0
        seen = set()
        schema = schemas[j["task"]]
        for line in raw.splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            key = r.get("key")
            seen.add(key)
            resp = r.get("response") or {}
            u = resp.get("usageMetadata", {})
            a, b = u.get("promptTokenCount", 0), u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0)
            tin, tout = tin + a, tout + b
            try:
                text = resp["candidates"][0]["content"]["parts"][0]["text"]
                schema.model_validate_json(text)
                llm.put(key, j["version"], text, a, b)
                ok += 1
            except Exception:  # noqa: BLE001 - missing candidate or invalid JSON: repaired later
                failed.setdefault(j["task"], []).append(items[key])
        failed.setdefault(j["task"], []).extend(x for k, x in items.items() if k not in seen)
        llm.db.commit()
        j.update(collected=True, ok=ok, tokens_in=tin, tokens_out=tout,
                 actual_usd=round(batch_cost(j["model"], tin, tout), 4))
        save_ledger(led)
        print(f"{j['task']}: collected {ok:,}/{j['n']:,} valid, ${j['actual_usd']:.2f}")
    return failed
