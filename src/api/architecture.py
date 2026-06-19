from fastapi import APIRouter

from src.services.dependency_service import (
    build_dependency_graph
)

router = APIRouter()


@router.get(
    "/atlas/dependencies"
)
def dependencies():

    return build_dependency_graph()