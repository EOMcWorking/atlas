from fastapi import APIRouter

from src.services.provider_ranking_service import (
    rank_providers
)

router = APIRouter()


@router.get("/providers/ranking")
def provider_ranking():

    return {
        "ranking": rank_providers()
    }