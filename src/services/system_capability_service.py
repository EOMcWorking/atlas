from src.services.capability_registry_service import (
    get_capabilities
)


def get_system_capabilities():

    capabilities = get_capabilities()

    enabled = [
        name
        for name, status
        in capabilities.items()
        if status
    ]

    return {
        "count": len(enabled),
        "capabilities": enabled
    }