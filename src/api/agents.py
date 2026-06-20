from fastapi import APIRouter

from src.models.ai import ChatRequest

from src.services.agent_orchestrator import (
    run_task
)

router = APIRouter()


@router.post(
    "/agents/run"
)
def agent_run(
    request: ChatRequest
):

    return run_task(
        request.prompt
    )