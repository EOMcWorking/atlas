from fastapi import APIRouter

from src.services.project_evolution_service import (
    generate_project_evolution
)

router = APIRouter(
    prefix="/project-evolution",
    tags=["Project Evolution"]
)


@router.get("/")
def get_project_evolution():

    result = generate_project_evolution()

    return {
        "success": True,
        "evolution": result
    }