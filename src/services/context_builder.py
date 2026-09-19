from src.services.project_context_service import (
    build_project_context
)

from src.services.context_selector import (
    build_targeted_context
)

from src.services.memory_service import (
    get_relevant_context
)

from src.services.decision_service import (
    search_decisions
)


def build_context(
    prompt: str,
    project_name: str = None
):

    project_context = (
        build_targeted_context(
            prompt,
            project_name
        )
    )

    decision_context = (
        search_decisions(
            prompt,
            project_name
        )
    )

    memory_context = (
        get_relevant_context(
            prompt,
            project_name=project_name
        )
    )

    return f"""
PROJECT CONTEXT

{project_context}

MEMORY CONTEXT

{memory_context}

DECISION CONTEXT

{decision_context}

USER REQUEST

{prompt}
"""