import os

from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv(
    "OPENAI_API_KEY",
    ""
)
OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY",
    ""
)
GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY",
    ""
)

GITHUB_MODELS_API_KEY = os.getenv(
    "GITHUB_MODELS_API_KEY",
    ""
)

GOOGLE_API_KEY = os.getenv(
    "GOOGLE_API_KEY",
    ""
)
DEFAULT_MODEL = "qwen2.5-coder:7b"

MODELS = {
    "coding": "qwen2.5-coder:7b",
    "review": "deepseek-coder:6.7b",
    "planning": "qwen2.5-coder:1.5b",
    "general": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:1.5b",
    "gpt_fast": "gpt-4.1-mini",
    "gpt_smart": "gpt-5"
}

DEFAULT_PROVIDER = "ollama"

PROVIDER_FALLBACKS = [
    "openrouter",
    "groq",
    "github",
    "openai",
    "claude",
    "ollama"
]

TASK_PROVIDER_MAP = {
    "coding": "openrouter",
    "review": "openrouter",
    "planning": "openrouter",
    "general": "openrouter",
    "fast": "ollama"
}