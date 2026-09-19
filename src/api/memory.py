from fastapi import APIRouter, Query

from src.services.memory_service import (
    summarize_decisions
)
from src.models.memory import MemoryEntry
from src.services.memory_service import (
    append_to_file,
    read_file,
    search_decisions,
    get_decisions_file,
    get_memory_file,
)

router = APIRouter()


@router.post("/memory/decision")
def add_decision(entry: MemoryEntry):
    append_to_file(
        get_decisions_file(),
        entry.text
    )

    return {
        "status": "saved"
    }


@router.get("/memory/decision")
def get_decisions():
    return {
        "content": read_file(
            get_decisions_file()
        )
    }


@router.get("/memory/search")
def memory_search(
    q: str = Query(..., description="Search term")
):
    return {
        "query": q,
        "matches": search_decisions(q)
    }

@router.get("/memory/summary")
def memory_summary():
    return {
        "summary": summarize_decisions()
    }

@router.post("/memory/note")
def add_memory(
    entry: MemoryEntry
):
    append_to_file(
        get_memory_file(),
        entry.text
    )
    read_file(
    get_memory_file()
    )
    return {
        "status": "saved"
    }