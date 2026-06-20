from src.providers.provider_registry import (
providers
)

from src.services.provider_selection_service import (
get_ranked_providers
)

def get_provider_chain(task_type: str):
    ranked = (
        get_ranked_providers(task_type)
    )

    chain = []

    for provider_name in ranked:
        if provider_name in providers:
            chain.append(
                providers[
                    provider_name
                ]
            )

    return chain