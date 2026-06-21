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

from src.services.provider_task_metrics_service import (
    get_task_winner
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

    ranked = get_ranked_providers(task_type)

    winner = get_task_winner(
        task_type
    )

    if (
        winner
        and winner in ranked
    ):

        ranked.remove(
            winner
        )

        ranked.insert(
            0,
            winner
        )

    return ranked
