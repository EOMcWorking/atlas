from fastapi import APIRouter

from src.services.provider_benchmark_service import (
    benchmark_providers
)

router = APIRouter()


@router.post(
    "/providers/benchmark"
)
def benchmark():

    return benchmark_providers()