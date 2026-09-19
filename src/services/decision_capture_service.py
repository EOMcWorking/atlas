from src.services.ollama_service import chat
from src.services.decision_service import (
    add_decision
)


def capture_decision(
    task: str,
    review: str
):

    prompt = f"""
Extract the most important architectural or implementation decision.

TASK:
{task}

REVIEW:
{review}

Return a single concise decision.
"""

    decision = chat(
        prompt,
        task_type="planning"
    )

    add_decision(
        decision
    )

    return decision