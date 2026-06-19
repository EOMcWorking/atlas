from src.core.config import DEFAULT_PROVIDER
from src.providers.ollama_provider import OllamaProvider
from src.providers.openai_provider import OpenAIProvider
from src.providers.claude_provider import ClaudeProvider


providers = {
    "ollama": OllamaProvider(),
    "openai": OpenAIProvider(),
    "claude": ClaudeProvider(),
}


def get_provider():
    return providers[
        DEFAULT_PROVIDER
    ]