from src.services.system_capability_service import (
    get_system_capabilities
)

from src.services.project_context_service import (
    get_project_context
)

from src.services.architecture_review_service import (
    review_architecture
)


def build_planner_context():

    capabilities = (
        get_system_capabilities()
    )

    project_context = (
        get_project_context()
    )

    architecture = (
        review_architecture()
    )

    return f"""
SYSTEM CAPABILITIES

{capabilities}

PROJECT CONTEXT

{project_context}

ARCHITECTURE REVIEW

{architecture}
"""