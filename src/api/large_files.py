from fastapi import APIRouter

from src.services.large_file_service import (
    find_large_files
)

router = APIRouter()


@router.get(
    "/atlas/large-files"
)
def large_files():

    return find_large_files()