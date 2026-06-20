import os

from src.providers.ollama_provider import OllamaProvider
from src.providers.openai_provider import OpenAIProvider
from src.providers.claude_provider import ClaudeProvider
from src.providers.openrouter_provider import OpenRouterProvider
from src.providers.groq_provider import GroqProvider
from src.providers.github_provider import GitHubProvider

from src.core.config import DEFAULT_PROVIDER


providers = {
    "ollama": OllamaProvider()
}


if os.getenv("OPENROUTER_API_KEY"):
    providers["openrouter"] = OpenRouterProvider()

if os.getenv("OPENAI_API_KEY"):
    providers["openai"] = OpenAIProvider()

if os.getenv("ANTHROPIC_API_KEY"):
    providers["claude"] = ClaudeProvider()

if os.getenv("GROQ_API_KEY"):
    providers["groq"] = GroqProvider()

if os.getenv("GITHUB_MODELS_API_KEY"):
    providers["github"] = GitHubProvider()


def get_provider():
    return providers[DEFAULT_PROVIDER]