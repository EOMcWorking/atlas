from pathlib import Path

from src.services.ollama_service import chat


def generate_next_task():
    roadmap = Path(
        "ROADMAP.md"
    ).read_text(
        encoding="utf-8"
    )

    tasks = Path(
        "TASKS.md"
    ).read_text(
        encoding="utf-8"
    )

    decisions = Path(
        "DECISIONS.md"
    ).read_text(
        encoding="utf-8"
    )

    handoff = Path(
        "HANDOFF.md"
    ).read_text(
        encoding="utf-8"
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
        task_type="general"
    )