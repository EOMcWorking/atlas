from fastapi import APIRouter

from src.providers.provider_registry import (
    providers
)

router = APIRouter()


@router.get("/atlas/providers")
def atlas_providers():
    return {
        "providers": list(
            providers.keys()
        )
    }