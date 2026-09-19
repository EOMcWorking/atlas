from fastapi import APIRouter
import threading

from src.services.autonomous_scheduler_service import (
    run_scheduler
)

router = APIRouter(
    prefix="/scheduler",
    tags=["scheduler"]
)


@router.post("/start")
def start_scheduler():

    thread = threading.Thread(
        target=run_scheduler,
        daemon=True
    )

    thread.start()

    return {
        "status": "started"
    }