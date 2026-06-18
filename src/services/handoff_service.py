from pathlib import Path

PROJECT_FILE = Path("PROJECT.md")
TASKS_FILE = Path("TASKS.md")
DECISIONS_FILE = Path("DECISIONS.md")
HANDOFF_FILE = Path("HANDOFF.md")


def generate_handoff():
    project = PROJECT_FILE.read_text(encoding="utf-8")
    tasks = TASKS_FILE.read_text(encoding="utf-8")
    decisions = DECISIONS_FILE.read_text(encoding="utf-8")

    handoff = f"""
# Atlas Handoff

## Project

{project}

## Tasks

{tasks}

## Decisions

{decisions}
"""

    HANDOFF_FILE.write_text(
        handoff,
        encoding="utf-8"
    )

    return handoff