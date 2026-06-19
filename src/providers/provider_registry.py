from src.core.config import DEFAULT_PROVIDER
from src.providers.ollama_provider import OllamaProvider

providers = {
    "ollama": OllamaProvider(),
}


def get_provider():
    return providers[
        DEFAULT_PROVIDER
    ]