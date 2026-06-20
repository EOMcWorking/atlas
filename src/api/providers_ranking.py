from fastapi import APIRouter

from src.services.provider_ranking_service import (
    get_ranked_providers
)

router = APIRouter()


@router.get("/providers/ranking")
def provider_ranking():

    return {
        "ranking": get_ranked_providers()
    }