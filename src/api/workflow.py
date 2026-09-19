from fastapi import APIRouter
from pydantic import BaseModel

from src.services.workflow_service import (
    execute_workflow
)

router = APIRouter()


class WorkflowRequest(
    BaseModel
):
    task: str


@router.post(
    "/workflow/run"
)
def run_workflow(
    request: WorkflowRequest
):
    return execute_workflow(
        request.task
    )