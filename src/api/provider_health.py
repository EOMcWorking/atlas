from fastapi import APIRouter

from src.services.provider_health_service import (
    get_provider_status
)

router = APIRouter(
    prefix="/atlas/providers",
    tags=["providers"]
)


@router.get("/status")
def provider_status():

    return get_provider_status()