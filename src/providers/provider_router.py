from src.providers.provider_registry import (
    providers
)

from src.services.provider_selection_service import (
    get_ranked_provider_list
)

from src.services.provider_cooldown_service import (
    is_on_cooldown
)


def get_provider_chain(
    task_type: str = "general"
):

    ranked = get_ranked_provider_list(
        task_type
    )

    chain = []

    for provider_name in ranked:

        provider = providers.get(
            provider_name
        )

        if not provider:
            continue

        provider_class_name = (
            provider.__class__.__name__
        )

        if is_on_cooldown(
            provider_class_name
        ):
            continue

        chain.append(
            provider
        )

    return chain