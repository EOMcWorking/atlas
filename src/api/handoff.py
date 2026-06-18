from fastapi import APIRouter

from src.services.handoff_service import (
    generate_handoff
)

router = APIRouter()

@router.post("/handoff/generate")
def create_handoff():
    return {
        "handoff": generate_handoff()
    }