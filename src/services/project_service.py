from src.services.handoff_service import (
    get_project_state_file
)


def get_project_state(
    project_name: str = None
):

    return {
        "project": get_project_state_file(
            "PROJECT.md",
            project_name
        ).read_text(
            encoding="utf-8"
        ),

        "tasks": get_project_state_file(
            "TASKS.md",
            project_name
        ).read_text(
            encoding="utf-8"
        ),

        "decisions": get_project_state_file(
            "DECISIONS.md",
            project_name
        ).read_text(
            encoding="utf-8"
        ),

        "handoff": get_project_state_file(
            "HANDOFF.md",
            project_name
        ).read_text(
            encoding="utf-8"
        )
    }