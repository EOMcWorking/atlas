from fastapi import APIRouter

from src.services.status_service import (
    get_atlas_status
)

router = APIRouter()

@router.get("/atlas/status")
def atlas_status():
    return get_atlas_status()