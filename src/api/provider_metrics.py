from fastapi import APIRouter

from src.services.provider_metrics_service import (
    load_metrics
)

router = APIRouter(
    prefix="/providers",
    tags=["providers"]
)


@router.get("/metrics")
def provider_metrics():

    return load_metrics()