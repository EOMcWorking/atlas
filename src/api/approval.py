from fastapi import (
    APIRouter
)

from src.services.approval_service import (
    approve_task,
    get_pending_approvals,
    load_approvals,
    reject_task
)

router = APIRouter(
    prefix="/approval",
    tags=["approval"]
)


@router.get("/")
def get_approvals():

    return load_approvals()

@router.get("/pending")
def pending():

    return get_pending_approvals()

@router.post("/approve/{task}")
def approve(
    task: str
):

    return {
        "success":
        approve_task(task)
    }

@router.post("/reject/{task}")
def reject(
    task: str
):

    return {
        "success":
        reject_task(task)
    }