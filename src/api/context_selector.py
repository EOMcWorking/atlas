from fastapi import APIRouter

from src.services.context_selector import (
    find_relevant_files
)

router = APIRouter()


@router.get(
    "/atlas/relevant-files"
)
def relevant_files(
    query: str
):
    files = find_relevant_files(
        query
    )

    return {
        "files": [
            str(file)
            for file in files
        ]
    }