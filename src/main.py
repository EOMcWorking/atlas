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
from src.api.project_index import router as project_index_router
from src.api.architecture import router as architecture_router
from src.api.architecture_analysis import router as architecture_analysis_router
from src.api.dead_code import router as dead_code_router
from src.api.architecture_review import router as architecture_review_router
from src.api.inspection import router as inspection_router
from src.api.recommendations import router as recommendations_router
from src.api.circular_dependencies import router as circular_dependencies_router
from src.api.large_files import router as large_files_router
from src.api.technical_debt import router as technical_debt_router
from src.api.architecture_history import router as history_router
from src.api.providers_test import router as providers_test_router
from src.api.provider_health import router as provider_health_router
from src.api.provider_metrics import router as provider_metrics_router
from src.api.providers_ranking import router as providers_ranking_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Atlas")
app.include_router(status_router)
app.include_router(technical_debt_router)
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
app.include_router(project_index_router)
app.include_router(project_router)
app.include_router(review_router)
app.include_router(context_selector_router)
app.include_router(architecture_router)
app.include_router(architecture_analysis_router)
app.include_router(dead_code_router)
app.include_router(architecture_review_router)
app.include_router(inspection_router)
app.include_router(recommendations_router)
app.include_router(circular_dependencies_router)
app.include_router(large_files_router)
app.include_router(history_router)
app.include_router(architecture_router)
app.include_router(providers_test_router)
app.include_router(provider_health_router)
app.include_router(provider_metrics_router)
app.include_router(providers_ranking_router)


@app.get("/")
def root():
    return {
        "project": "Atlas",
        "status": "running"
    }