from fastapi import FastAPI
from src.api.memory import router as memory_router
from src.api.ai import router as ai_router
from src.core.database import Base, engine
from src.api.tasks import router as task_router
from src.api.handoff import (
    router as handoff_router
)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas")

app.include_router(task_router)
app.include_router(memory_router)
app.include_router(handoff_router)
app.include_router(ai_router)

@app.get("/")
def root():
    return {
        "project": "Atlas",
        "status": "running"
    }