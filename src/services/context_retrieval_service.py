from src.services.project_context_service import (
    build_project_context
)

from src.services.decision_history_service import (
    get_recent_decisions
)


def get_context_for_task(
    task: str,
    max_chars: int = 12000
):

    project_context = (
        build_project_context(
            max_chars=max_chars
        )
    )

    decisions = (
        get_recent_decisions()
    )

    return f"""
TASK:
{task}

RECENT DECISIONS:
{decisions}

PROJECT CONTEXT:
{project_context}
"""