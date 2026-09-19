from pathlib import Path

from src.services.project_paths_service import (
    get_project_file
)

from src.services.workspace_service import (
    get_docs_path
)


def get_project_state_file(
    filename: str,
    project_name: str = None
):

    if project_name is None:

        return Path(
            get_docs_path()
        ) / filename

    return Path(
        get_project_file(
            project_name,
            filename
        )
    )


def update_handoff(
    content: str,
    project_name: str = None
):

    handoff_file = get_project_state_file(
        "HANDOFF.md",
        project_name
    )

    handoff_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    handoff_file.write_text(
        content,
        encoding="utf-8"
    )


def generate_handoff(
    project_name: str = None
):

    project = (
        get_project_state_file(
            "PROJECT.md",
            project_name
        )
        .read_text(
            encoding="utf-8"
        )
    )

    tasks = (
        get_project_state_file(
            "TASKS.md",
            project_name
        )
        .read_text(
            encoding="utf-8"
        )
    )

    decisions = (
        get_project_state_file(
            "DECISIONS.md",
            project_name
        )
        .read_text(
            encoding="utf-8"
        )
    )

    handoff = f"""
# Atlas Handoff

## Project

{project}

## Tasks

{tasks}

## Decisions

{decisions}
"""

    update_handoff(
        handoff,
        project_name
    )

    return handoff