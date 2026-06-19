from fastapi import APIRouter

from src.services.architecture_service import (
    analyze_architecture
)

router = APIRouter()


@router.get(
    "/atlas/architecture-analysis"
)
def architecture_analysis():

    return analyze_architecture()