from fastapi import APIRouter

from src.services.snapshot_service import (
    generate_snapshot
)

router = APIRouter()

@router.post("/snapshot/generate")
def create_snapshot():
    return generate_snapshot()