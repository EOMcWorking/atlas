from pathlib import Path

from src.services.ollama_service import chat
from src.services.workspace_service import get_docs_path


def review_project():

    docs_path = Path(
        get_docs_path()
    )

    project = (
        docs_path / "PROJECT.md"
    ).read_text(
        encoding="utf-8"
    )

    tasks = (
        docs_path / "TASKS.md"
    ).read_text(
        encoding="utf-8"
    )

    decisions = (
        docs_path / "DECISIONS.md"
    ).read_text(
        encoding="utf-8"
    )

    handoff = (
        docs_path / "HANDOFF.md"
    ).read_text(
        encoding="utf-8"
    )

    prompt = f"""
You are a senior software architect.

Review this project.

PROJECT:
{project}

TASKS:
{tasks}

DECISIONS:
{decisions}

HANDOFF:
{handoff}

Provide:

1. Current project status
2. Biggest risk
3. Missing feature
4. Most important next task
"""

    return chat(
        prompt,
        task_type="review"
    )