from pathlib import Path
import hashlib
import json


CACHE_FILE = Path(
    "llm_cache.json"
)

def load_cache():

    if not CACHE_FILE.exists():

        return {}

    return json.loads(
        CACHE_FILE.read_text(
            encoding="utf-8"
        )
    )

def save_cache(
    cache
):

    CACHE_FILE.write_text(
        json.dumps(
            cache,
            indent=2
        ),
        encoding="utf-8"
    )

def build_cache_key(
    prompt: str,
    task_type: str
):

    content = (
        task_type
        + "::"
        + prompt
    )

    return hashlib.sha256(
        content.encode(
            "utf-8"
        )
    ).hexdigest()

def get_cached_response(
    prompt: str,
    task_type: str
):

    cache = load_cache()

    key = build_cache_key(
        prompt,
        task_type
    )

    return cache.get(
        key
    )

def cache_response(
    prompt: str,
    task_type: str,
    response: str
):

    cache = load_cache()

    key = build_cache_key(
        prompt,
        task_type
    )

    cache[key] = response

    save_cache(
        cache
    )

def get_or_cache(
    prompt: str,
    task_type: str,
    generator
):

    cached = (
        get_cached_response(
            prompt,
            task_type
        )
    )

    if cached:

        return cached

    response = generator()

    cache_response(
        prompt,
        task_type,
        response
    )

    return response
