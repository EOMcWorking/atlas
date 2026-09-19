from pathlib import Path

from src.services.ollama_service import chat

from src.services.project_paths_service import (
    get_project_file
)


def get_project_state_file(
    filename: str,
    project_name: str = None
):

    if project_name is None:
        return Path(
            filename
        )

    return Path(
        get_project_file(
            project_name,
            filename
        )
    )


def generate_next_task(
    project_name: str = None
):

    roadmap = (
        get_project_state_file(
            "ROADMAP.md",
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

    handoff = (
        get_project_state_file(
            "HANDOFF.md",
            project_name
        )
        .read_text(
            encoding="utf-8"
        )
    )

    prompt = f"""
You are the Atlas project manager.

ROADMAP:
{roadmap}

TASKS:
{tasks}

DECISIONS:
{decisions}

HANDOFF:
{handoff}

Recommend:

1. One next task
2. Why it matters
3. Estimated difficulty (1-10)

Return concise output.
"""

    return chat(
        prompt,
        task_type="planning"
    )


def generate_actionable_task(
    context: str
):

    prompt = f"""
You are Atlas Project Manager.

CONTEXT:

{context}

Generate exactly ONE task.

Rules:

- Concrete
- File-specific
- Actionable
- Engineering task
- One sentence only

Good:

Split src/main.py into router modules

Bad:

Improve architecture

Return only the task.
"""

    return chat(
        prompt,
        task_type="planning"
    )