from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies import get_db
from src.models.task import TaskCreate
from src.services.task_service import get_tasks, create_task

router = APIRouter()

@router.get("/tasks")
def list_tasks(db: Session = Depends(get_db)):
    return get_tasks(db)

@router.post("/tasks")
def add_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    return create_task(db, task.title)