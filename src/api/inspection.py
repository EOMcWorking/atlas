from fastapi import APIRouter

from src.services.rule_inspector_service import (
    inspect_architecture
)

router = APIRouter()


@router.get(
    "/atlas/inspection"
)
def inspection():

    return inspect_architecture()