from fastapi import APIRouter

from src.services.model_router import MODELS

router = APIRouter()


@router.get("/atlas/models")
def atlas_models():
    return MODELS