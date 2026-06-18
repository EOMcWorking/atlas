from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str

class Task(BaseModel):
    id: int
    title: str
    completed: bool

    model_config = {
        "from_attributes": True
    }