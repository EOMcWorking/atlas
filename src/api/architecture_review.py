from fastapi import APIRouter

from src.services.architecture_review_service import (
    review_architecture
)

router = APIRouter()


@router.get(
    "/atlas/architecture-review"
)
def architecture_review():

    return {
        "review": review_architecture()
    }