"""Async Gemini / Gemma client for the LLM tagging experiments: structured output, parallel workers, retries,
a response cache and cost accounting.

  from llm.client import LLM
  llm = LLM("gemini-3.1-flash-lite", workers=16)
  results = asyncio.run(llm.map(SYSTEM, inputs, Schema, version="w1-v1"))   # [Result]

- Structured output: `response_schema` = a pydantic model (all models on the key accept it, Gemma 4 included).
  A response that does not validate is retried once with the validation error appended.
- Cache: .cache/llm/cache.sqlite, key = model + version + thinking + system + input + schema. Re-running an
  experiment costs nothing; change `version` when the prompt changes.
- Cost: from PRICES (USD per 1M tokens, paid tier, checked 2026-10-14 on ai.google.dev/gemini-api/docs/pricing;
  Gemma 4 is free of charge but rate-limited). `LLM.spent` sums the cost of uncached calls; a run stops when
  the process-wide cap `MAX_USD` is reached.
"""
import asyncio, hashlib, json, os, sqlite3, time
from dataclasses import dataclass, field

from google import genai
from google.genai import errors, types
from pydantic import BaseModel, ValidationError
from tenacity import AsyncRetrying, retry_if_exception, stop_after_attempt, wait_random_exponential

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CACHE = os.path.join(ROOT, ".cache", "llm", "cache.sqlite")
# (input, output incl. thinking) USD per 1M tokens; batch mode is half
PRICES = {
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gemini-3.1-flash-lite": (0.25, 1.50),
    "gemini-2.5-flash-lite": (0.10, 0.40),
    "gemma-4-26b-a4b-it": (0.0, 0.0),
    "gemma-4-31b-it": (0.0, 0.0),
}
MAX_USD = float(os.environ.get("LLM_MAX_USD", "45"))
_spent_total = 0.0


def _load_env():
    path = os.path.join(ROOT, ".env")
    if os.path.exists(path):
        for line in open(path):
            k, _, v = line.strip().partition("=")
            if k and not k.startswith("#"):
                os.environ.setdefault(k, v.strip().strip("\"'"))


@dataclass
class Result:
    key: str
    data: dict | None          # validated output, or None
    error: str | None = None
    tokens_in: int = 0
    tokens_out: int = 0        # candidates + thinking
    latency: float = 0.0
    cached: bool = False
    usd: float = 0.0
    raw: str = field(default="", repr=False)


def _retryable(e):
    return isinstance(e, errors.APIError) and getattr(e, "code", None) in (429, 500, 502, 503, 504)


class LLM:
    def __init__(self, model, workers=16, thinking="off"):
        _load_env()
        self.model, self.workers, self.thinking = model, workers, thinking
        self.client = genai.Client()
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        self.db = sqlite3.connect(CACHE)
        self.db.execute("CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, model TEXT, version TEXT, raw TEXT, "
                        "tokens_in INT, tokens_out INT, latency REAL, created REAL)")
        self.spent = 0.0

    def _config(self, system, schema):
        cfg = dict(system_instruction=system, response_mime_type="application/json", response_schema=schema,
                   temperature=0.0)
        if self.model.startswith("gemini"):
            if "2.5" in self.model:
                cfg["thinking_config"] = types.ThinkingConfig(thinking_budget=0 if self.thinking == "off" else 1024)
            else:
                cfg["thinking_config"] = types.ThinkingConfig(
                    thinking_level="minimal" if self.thinking == "off" else self.thinking)
        return types.GenerateContentConfig(**cfg)

    def _key(self, version, system, text, schema):
        h = hashlib.sha256(json.dumps([self.model, version, self.thinking, system, text,
                                       schema.model_json_schema()], ensure_ascii=False).encode()).hexdigest()
        return h

    def _cost(self, tin, tout):
        pin, pout = PRICES.get(self.model, (0.30, 2.50))
        return tin / 1e6 * pin + tout / 1e6 * pout

    async def _call(self, contents, config):
        async for attempt in AsyncRetrying(retry=retry_if_exception(_retryable), stop=stop_after_attempt(8),
                                           wait=wait_random_exponential(multiplier=2, max=90), reraise=True):
            with attempt:
                return await self.client.aio.models.generate_content(model=self.model, contents=contents,
                                                                     config=config)

    async def one(self, system, text, schema: type[BaseModel], version):
        global _spent_total
        key = self._key(version, system, text, schema)
        row = self.db.execute("SELECT raw, tokens_in, tokens_out, latency FROM cache WHERE key=?", (key,)).fetchone()
        if row:
            raw, tin, tout, lat = row
            try:
                return Result(key, schema.model_validate_json(raw).model_dump(), None, tin, tout, lat, True, 0.0, raw)
            except ValidationError as e:
                return Result(key, None, f"cached invalid: {e.errors()[:1]}", tin, tout, lat, True, 0.0, raw)
        if _spent_total >= MAX_USD:
            return Result(key, None, f"spend cap {MAX_USD} USD reached")
        config = self._config(system, schema)
        contents, tin, tout, t0, raw, err = text, 0, 0, time.time(), "", None
        for _ in range(2):  # one repair retry when the JSON does not validate
            try:
                r = await self._call(contents, config)
            except Exception as e:  # noqa: BLE001 - an API error is recorded as the item's error
                err = f"{type(e).__name__}: {str(e)[:300]}"
                break
            u = r.usage_metadata
            tin += u.prompt_token_count or 0
            tout += (u.candidates_token_count or 0) + (u.thoughts_token_count or 0)
            raw = r.text or ""
            try:
                data = schema.model_validate_json(raw).model_dump()
                err = None
                break
            except ValidationError as e:
                err = f"invalid: {e.errors()[:1]}"
                data = None
                contents = f"{text}\n\nYour previous answer was not valid JSON for the schema ({err}). Answer again."
        lat = time.time() - t0
        usd = self._cost(tin, tout)
        self.spent += usd
        _spent_total += usd
        if err is None:
            self.db.execute("INSERT OR REPLACE INTO cache VALUES (?,?,?,?,?,?,?,?)",
                            (key, self.model, version, raw, tin, tout, lat, time.time()))
            self.db.commit()
            return Result(key, data, None, tin, tout, lat, False, usd, raw)
        return Result(key, None, err, tin, tout, lat, False, usd, raw)

    async def map(self, system, texts, schema, version, progress=True):
        sem = asyncio.Semaphore(self.workers)
        done = 0

        async def run(t):
            nonlocal done
            async with sem:
                r = await self.one(system, t, schema, version)
            done += 1
            if progress and (done % 25 == 0 or done == len(texts)):
                print(f"  {self.model}: {done}/{len(texts)}  spent ${self.spent:.4f}", flush=True)
            return r

        return await asyncio.gather(*(run(t) for t in texts))


def summary(results):
    """Totals for a list of Results: n, valid, errors, tokens, mean latency (uncached calls), USD."""
    live = [r for r in results if not r.cached]
    return dict(n=len(results), valid=sum(r.data is not None for r in results),
                errors=sum(r.data is None for r in results), cached=len(results) - len(live),
                tokens_in=sum(r.tokens_in for r in results), tokens_out=sum(r.tokens_out for r in results),
                mean_latency=round(sum(r.latency for r in live) / len(live), 2) if live else None,
                usd=round(sum(r.usd for r in results), 5))
