from fastapi import APIRouter

from src.models.ai import ChatRequest
from src.services.ollama_service import chat

from src.services.ollama_service import (
    suggest_next_task
)
from src.services.project_review_service import (
    review_project
)
from src.services.task_generation_service import (
    generate_next_task
)

router = APIRouter()

@router.get("/ai/next-task")
def next_task():
    return {
        "task": suggest_next_task()
    }

@router.post("/ai/chat")
def ai_chat(request: ChatRequest):
    return {
        "response": chat(
            request.prompt
        )
    }

@router.post("/ai/project-review")
def project_review():
    return {
        "review": review_project()
    }

@router.post("/ai/next-task")
def next_task():
    return {
        "task": generate_next_task()
    }