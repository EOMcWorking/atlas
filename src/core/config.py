DEFAULT_MODEL = "qwen2.5-coder:7b"

MODELS = {
    "coding": "qwen2.5-coder:7b",
    "review": "deepseek-coder:6.7b",
    "planning": "qwen2.5-coder:1.5b",
    "general": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:1.5b",
}

DEFAULT_PROVIDER = "ollama"

PROVIDER_FALLBACKS = [
    "ollama"
]