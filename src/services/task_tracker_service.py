from pathlib import Path

from src.services.memory_service import (
    read_file,
    append_to_file
)

from src.services.project_paths_service import (
    get_project_file
)


from src.services.workspace_service import (
    get_docs_path
)


def get_tasks_file(
    project_name: str = None
):

    if project_name is None:
        return Path(
            get_docs_path()
        ) / "TASKS.md"

    return Path(
        get_project_file(
            project_name,
            "TASKS.md"
        )
    )

def task_exists(
    task: str,
    project_name: str = None
):
    """
    Check if a task already exists in TASKS.md.
    """
    tasks_file = get_tasks_file(project_name)

    if not tasks_file.exists():
        return False

    content = read_file(tasks_file)
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        # Strip off checkbox markers like "- [ ]" or "- [x]"
        if line.startswith("- [ ]"):
            existing_task = line[5:].strip()
        elif line.startswith("- [x]"):
            existing_task = line[4:].strip()
        else:
            continue

        if existing_task == task:
            return True

    return False


def add_task(
    task: str,
    project_name: str = None
):
    """
    Add a task to TASKS.md, but only if it doesn't already exist.
    Returns True if added, False if duplicate.
    """
    if task_exists(task, project_name):
        return False

    append_to_file(
        get_tasks_file(project_name),
        f"- [ ] {task}"
    )
    return True


def complete_task(
    task: str,
    project_name: str = None
):

    tasks_file = get_tasks_file(
        project_name
    )

    content = read_file(
        tasks_file
    )

    content = content.replace(
        f"- [ ] {task}",
        f"- [x] {task}"
    )

    tasks_file.write_text(
        content,
        encoding="utf-8"
    )