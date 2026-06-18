from src.services.model_router import get_model
import ollama

from src.core.config import DEFAULT_MODEL, MODELS
from pathlib import Path
MODEL_NAME = DEFAULT_MODEL


def suggest_next_task():
    tasks = Path("TASKS.md").read_text(
        encoding="utf-8"
    )

    decisions = Path(
        "DECISIONS.md"
    ).read_text(
        encoding="utf-8"
    )

    handoff = Path(
        "HANDOFF.md"
    ).read_text(
        encoding="utf-8"
    )

    prompt = f"""
You are Atlas.

Project Tasks:
{tasks}

Decisions:
{decisions}

Handoff:
{handoff}

Suggest the single most important next development task.
"""

    return chat(prompt)

def chat(prompt: str, task_type="general"):
    model = get_model(task_type)

    response = ollama.chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]