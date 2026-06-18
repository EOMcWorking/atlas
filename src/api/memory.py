from fastapi import APIRouter

from src.models.memory import MemoryEntry
from src.services.memory_service import (
    append_to_file,
    read_file,
    DECISIONS_FILE,
)

router = APIRouter()

@router.post("/memory/decision")
def add_decision(entry: MemoryEntry):
    append_to_file(
        DECISIONS_FILE,
        entry.text
    )

    return {
        "status": "saved"
    }

@router.get("/memory/decision")
def get_decisions():
    return {
        "content": read_file(
            DECISIONS_FILE
        )
    }