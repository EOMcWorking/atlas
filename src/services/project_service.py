from pathlib import Path


def get_project_state():
    return {
        "project": Path("PROJECT.md").read_text(
            encoding="utf-8"
        ),
        "tasks": Path("TASKS.md").read_text(
            encoding="utf-8"
        ),
        "decisions": Path("DECISIONS.md").read_text(
            encoding="utf-8"
        ),
        "handoff": Path("HANDOFF.md").read_text(
            encoding="utf-8"
        ),
    }