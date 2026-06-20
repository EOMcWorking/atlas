from src.core.config import (
    TASK_PROVIDER_MAP,
    PROVIDER_FALLBACKS
)

from src.services.provider_health_service import (
    get_provider_status
)

from src.services.provider_ranking_service import (
    get_ranked_providers
)

from src.services.provider_cooldown_service import (
    is_on_cooldown
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


def get_ranked_provider_list(
    task_type: str = "general"
):

    ranked = get_ranked_providers(
        task_type
    )

    available = []

    for provider in ranked:

        if not is_on_cooldown(
            provider
        ):
            available.append(
                provider
            )

    if available:
        return available

    return PROVIDER_FALLBACKS