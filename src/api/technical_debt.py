from fastapi import APIRouter

from src.services.technical_debt_service import (
    calculate_technical_debt
)

router = APIRouter()


@router.get(
    "/atlas/technical-debt"
)
def technical_debt():

    return (
        calculate_technical_debt()
    )