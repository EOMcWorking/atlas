from src.services.project_context_service import build_project_context
from src.services.context_selector import build_targeted_context
from src.services.memory_service import get_relevant_context


def build_context(
    prompt: str
):
    project_context = (
        build_targeted_context(
            prompt
        )
    )

    memory_context = (
        get_relevant_context(
            prompt
        )
    )

    return f"""
PROJECT CONTEXT

{project_context}

MEMORY CONTEXT

{memory_context}

USER REQUEST

{prompt}
"""