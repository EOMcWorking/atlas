from fastapi import APIRouter

from src.services.architecture_trend_service import (
    save_architecture_snapshot,
    get_architecture_history
)

router = APIRouter()


@router.post(
    "/atlas/history/save"
)
def save_history():

    return (
        save_architecture_snapshot()
    )


@router.get(
    "/atlas/history"
)
def history():

    return {
        "history":
            get_architecture_history()
    }