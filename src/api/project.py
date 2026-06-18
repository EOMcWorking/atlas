from fastapi import APIRouter

from src.services.project_service import (
    get_project_state
)

router = APIRouter()

@router.get("/project/state")
def project_state():
    return get_project_state()