from fastapi import APIRouter

from src.services.runtime_service import (
    start_runtime,
    stop_runtime,
    restart_runtime,
    pause_runtime,
    resume_runtime,
    get_runtime_status,
    get_runtime_snapshot
)

router = APIRouter(
    prefix="/runtime",
    tags=["runtime"]
)


@router.post("/start")
def start():
    return start_runtime()


@router.post("/stop")
def stop():
    return stop_runtime()


@router.post("/restart")
def restart():
    return restart_runtime()


@router.post("/pause")
def pause():
    return pause_runtime()


@router.post("/resume")
def resume():
    return resume_runtime()


@router.get("/status")
def status():
    return get_runtime_status()


@router.get("/snapshot")
def snapshot():
    return get_runtime_snapshot()