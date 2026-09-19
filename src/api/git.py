from fastapi import APIRouter

from src.services.git_status_service import (
    get_git_status
)

router = APIRouter(
    prefix="/git",
    tags=["git"]
)


@router.get("/status")
def git_status():

    return {
        "status": get_git_status()
    }