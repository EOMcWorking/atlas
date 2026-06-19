from fastapi import APIRouter

from src.services.project_context_service import (
    get_project_stats
)

router = APIRouter()


@router.get(
    "/atlas/project-context"
)
def project_context():
    return get_project_stats()