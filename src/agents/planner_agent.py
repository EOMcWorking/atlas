from src.services.ollama_service import chat

from src.services.context_builder import (
    build_context
)


def plan(
    task: str
):

    context = build_context(task)

    prompt = f"""
You are Atlas Planner.

{context}

TASK:

{task}

Return:

1. Goal
2. Implementation Steps
3. Files Likely Involved
4. Risks
5. Success Criteria

Keep concise.
"""

    return chat(
        prompt,
        task_type="planning"
    )