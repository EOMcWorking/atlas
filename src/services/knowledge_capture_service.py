from src.services.ollama_service import chat
from src.services.decision_service import (
    add_decision
)


def capture_knowledge(
    task: str,
    review: str,
    project_name: str = None
):

    prompt = f"""
Analyze this completed task.

TASK:
{task}

REVIEW:
{review}

Return:

Decision:
...

Reason:
...

Outcome:
...
"""

    knowledge = chat(
        prompt,
        task_type="planning"
    )

    add_decision(
        knowledge,
        project_name
    )

    return knowledge