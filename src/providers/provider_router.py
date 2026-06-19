from src.core.config import (
    PROVIDER_FALLBACKS
)

from src.providers.provider_registry import (
    providers
)


def get_provider_chain():
    chain = []

    for provider_name in PROVIDER_FALLBACKS:
        provider = providers.get(
            provider_name
        )

        if provider:
            chain.append(provider)

    return chain