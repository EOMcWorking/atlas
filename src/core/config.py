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

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY",
    ""
)

DEFAULT_MODEL = "qwen2.5-coder:7b"

MODELS = {
    "coding": "deepseek/deepseek-chat",
    "review": "anthropic/claude-sonnet-4",
    "planning": "google/gemini-2.5-flash",
    "general": "openai/gpt-5",
    "fast": "llama-3.3-70b-versatile"
}

DEFAULT_PROVIDER = "ollama"

PROVIDER_FALLBACKS = [
    "openrouter",
    "groq",
    "github",
    "gemini",
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

TASK_MODELS = {

    "general": {
        "openrouter": "openai/gpt-5",
        "openai": "gpt-5",
        "ollama": "qwen2.5-coder:7b"
    },

    "planning": {
        "openrouter": "google/gemini-2.5-flash",
        "openai": "gpt-5-mini",
        "ollama": "qwen2.5:3b"
    },

    "coding": {
        "openrouter": "deepseek/deepseek-chat",
        "openai": "gpt-5",
        "ollama": "qwen2.5-coder:7b"
    },

    "review": {
        "openrouter": "anthropic/claude-sonnet-4",
        "openai": "gpt-5",
        "ollama": "deepseek-coder:6.7b"
    }
}