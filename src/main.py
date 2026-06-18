from fastapi import FastAPI

from src.core.database import Base, engine
from src.api.tasks import router as task_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas")

app.include_router(task_router)

@app.get("/")
def root():
    return {
        "project": "Atlas",
        "status": "running"
    }