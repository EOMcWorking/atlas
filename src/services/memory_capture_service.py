from pathlib import Path

from src.services.memory_service import (
    append_to_file,
    get_memory_file as get_workspace_memory_file,
)

from src.services.project_paths_service import (
    get_project_file
)


def get_memory_file(
    project_name: str = None
):

    if project_name is None:
        return get_workspace_memory_file()

    return Path(
        get_project_file(
            project_name,
            "MEMORY.md"
        )
    )


def save_agent_memory(
    agent: str,
    content: str,
    project_name: str = None
):

    append_to_file(
        get_memory_file(
            project_name
        ),
        f"[{agent}] {content}"
    )