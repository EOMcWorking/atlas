from fastapi import APIRouter

from src.services.project_index_service import (
    get_directory_index
)

router = APIRouter()


@router.get(
    "/atlas/project-index"
)
def project_index():
    return get_directory_index()