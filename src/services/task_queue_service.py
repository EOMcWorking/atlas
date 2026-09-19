from pathlib import Path

from src.services.project_paths_service import (
    get_project_file
)

TASKS_FILE = Path(
    "TASKS.md"
)


def get_tasks_file(
    project_name: str = None
):

    if project_name is None:
        return TASKS_FILE

    return Path(
        get_project_file(
            project_name,
            "TASKS.md"
        )
    )


def get_next_task(
    project_name: str = None
):

    tasks_file = get_tasks_file(
        project_name
    )

    if not tasks_file.exists():
        return None

    lines = tasks_file.read_text(
        encoding="utf-8"
    ).splitlines()

    for line in lines:

        line = line.strip()

        if (
            line
            and not line.startswith("#")
            and not line.startswith("[DONE]")
            and not line.startswith("[FAILED]")
        ):
            return line

    return None


def get_pending_tasks(
    project_name: str = None
):
    """
    Return all pending tasks (not done, not failed, not comments).
    """
    tasks_file = get_tasks_file(
        project_name
    )

    if not tasks_file.exists():
        return []

    lines = tasks_file.read_text(
        encoding="utf-8"
    ).splitlines()

    pending = []

    for line in lines:

        line = line.strip()

        if (
            line
            and not line.startswith("#")
            and not line.startswith("[DONE]")
            and not line.startswith("[FAILED]")
        ):
            pending.append(line)

    return pending


def complete_task(
    task: str,
    project_name: str = None
):

    tasks_file = get_tasks_file(
        project_name
    )

    if not tasks_file.exists():
        return

    lines = tasks_file.read_text(
        encoding="utf-8"
    ).splitlines()

    updated = []

    for line in lines:

        if (
            line.strip()
            == task
        ):

            updated.append(
                f"[DONE] {line}"
            )

        else:

            updated.append(
                line
            )

    tasks_file.write_text(
        "\n".join(updated),
        encoding="utf-8"
    )


def fail_task(
    task: str,
    project_name: str = None
):

    tasks_file = get_tasks_file(
        project_name
    )

    if not tasks_file.exists():
        return

    lines = tasks_file.read_text(
        encoding="utf-8"
    ).splitlines()

    updated = []

    for line in lines:

        if (
            line.strip()
            == task
        ):

            updated.append(
                f"[FAILED] {line}"
            )

        else:

            updated.append(
                line
            )

    tasks_file.write_text(
        "\n".join(updated),
        encoding="utf-8"
    )