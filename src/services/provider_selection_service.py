from src.core.config import (
TASK_PROVIDER_MAP,
PROVIDER_FALLBACKS
)

from src.services.provider_health_service import (
get_provider_status
)

from src.services.provider_ranking_service import (
rank_providers
)

def get_best_provider():
    return select_provider(
        "general"
    )

def select_provider(
    task_type: str
):

    status = get_provider_status()

    preferred = (
        TASK_PROVIDER_MAP.get(
            task_type,
            "openrouter"
        )
    )

    if status.get(preferred):
        return preferred

    for provider in PROVIDER_FALLBACKS:
        if status.get(provider):
            return provider

    return "ollama"

def get_ranked_providers():
    ranked = rank_providers()

    if ranked:
        return ranked

    return PROVIDER_FALLBACKS