from fastapi import APIRouter

from src.services.dead_code_service import (
    find_dead_code
)

router = APIRouter()


@router.get(
    "/atlas/dead-code"
)
def dead_code():

    return find_dead_code()