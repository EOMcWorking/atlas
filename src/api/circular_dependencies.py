from fastapi import APIRouter

from src.services.circular_dependency_service import (
    find_circular_dependencies
)

router = APIRouter()


@router.get(
    "/atlas/circular-dependencies"
)
def circular_dependencies():

    return (
        find_circular_dependencies()
    )