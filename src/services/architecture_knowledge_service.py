from src.services.architecture_service import (
    analyze_architecture
)

from src.services.dead_code_service import (
    find_dead_code
)

from src.services.dependency_service import (
    build_dependency_graph
)

from src.services.project_context_service import (
    get_project_stats,
    get_project_files
)


def build_architecture_knowledge():

    return {
        "architecture": (
            analyze_architecture()
        ),

        "dead_code": (
            find_dead_code()
        ),

        "project_stats": (
            get_project_stats()
        ),

        "project_files": [
            str(file)
            for file in get_project_files()
        ],

        "dependency_graph": list(
            build_dependency_graph().items()
        )[:20]
    }