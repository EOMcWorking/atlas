from src.providers.provider_registry import (
    providers
)

from src.services.provider_selection_service import (
    get_ranked_provider_list
)


def get_provider_chain(
    task_type: str = "general"
):

    ranked = (
        get_ranked_provider_list(
            task_type
        )
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