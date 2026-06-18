from sqlalchemy.orm import Session
from src.models.task_db import TaskDB

def get_tasks(db: Session):
    return db.query(TaskDB).all()

def create_task(db: Session, title: str):
    task = TaskDB(
        title=title,
        completed=False
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task