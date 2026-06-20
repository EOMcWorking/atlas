from src.providers.provider_registry import (
    providers
)


def get_provider_status():

    status = {}

    for name, provider in providers.items():

        try:

            if hasattr(
                provider,
                "health_check"
            ):

                status[name] = (
                    provider.health_check()
                )

            else:

                status[name] = False

        except Exception:

            status[name] = False

    return status