import requests

from src.core.config import (
    OMNIROUTE_API_KEY,
    OMNIROUTE_BASE_URL,
)


def chat(
    model: str,
    messages: list,
    temperature: float = 0.2,
    max_tokens: int = 4096,
):

    headers = {
        "Authorization": f"Bearer {OMNIROUTE_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    response = requests.post(
        f"{OMNIROUTE_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]