import asyncio
import requests
import random
import string

from config import SHORT_URL, SHORT_API, ENABLE_SHORTNER

_cache = {}

def _alias(n=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(n))

def _shorten_sync(long_url: str) -> str:
    alias = _alias()
    api = f"https://{SHORT_URL}/api?api={SHORT_API}&url={long_url}&alias={alias}"
    r = requests.get(api, timeout=10)
    data = r.json()
    if r.status_code == 200 and data.get("status") == "success":
        return data.get("shortenedUrl", long_url)
    return long_url

async def get_short_url(long_url: str) -> str:
    if not ENABLE_SHORTNER:
        return long_url

    if long_url in _cache:
        return _cache[long_url]

    try:
        short = await asyncio.to_thread(_shorten_sync, long_url)
        _cache[long_url] = short
        return short
    except Exception as e:
        print("[Shortener Error]", e)
        return long_url
