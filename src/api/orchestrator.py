from fastapi import APIRouter
from pydantic import BaseModel

from src.services.orchestrator_service import (
    assign_task
)

from src.services.ollama_service import (
    chat
)

router = APIRouter()


class TaskRequest(BaseModel):
    task: str


@router.post("/atlas/assign")
def atlas_assign(
    request: TaskRequest
):
    assignment = assign_task(
        request.task
    )

    response = chat(
        request.task,
        task_type=assignment[
            "task_type"
        ]
    )

    return {
        "agent":
            assignment["agent"],
        "task_type":
            assignment["task_type"],
        "response":
            response
    }