from fastapi import APIRouter

from src.models.ai import ChatRequest
from src.services.ollama_service import chat

from src.services.ollama_service import (
    suggest_next_task
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