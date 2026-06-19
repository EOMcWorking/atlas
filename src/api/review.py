from fastapi import APIRouter

from src.services.ollama_service import (
    chat
)

router = APIRouter()


@router.get(
    "/ai/project-review"
)
def project_review():

    response = chat(
        "Review the Atlas project architecture. "
        "Identify weaknesses, risks and improvements.",
        task_type="review"
    )

    return {
        "review": response
    }