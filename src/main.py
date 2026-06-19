from fastapi import FastAPI

from src.core.database import Base, engine
from src.api.models import router as models_router
from src.api.tasks import router as task_router
from src.api.memory import router as memory_router
from src.api.handoff import router as handoff_router
from src.api.ai import router as ai_router
from src.api.snapshot import router as snapshot_router
from src.api.project import router as project_router
from src.api.status import router as status_router
from src.api.providers import router as providers_router
from src.api.orchestrator import router as orchestrator_router
from src.api.project_context import router as project_context_router
from src.api.context import router as context_router
from src.api.review import router as review_router
from src.api.context_selector import router as context_selector_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas")
app.include_router(status_router)
app.include_router(project_context_router)
app.include_router(context_router)
app.include_router(models_router)
app.include_router(providers_router)
app.include_router(orchestrator_router)
app.include_router(task_router)
app.include_router(memory_router)
app.include_router(handoff_router)
app.include_router(ai_router)
app.include_router(snapshot_router)
app.include_router(project_router)
app.include_router(review_router)
app.include_router(context_selector_router)

@app.get("/")
def root():
    return {
        "project": "Atlas",
        "status": "running"
    }