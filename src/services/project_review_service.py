from pathlib import Path

from src.services.ollama_service import chat


def review_project():
    project = Path("PROJECT.md").read_text(
        encoding="utf-8"
    )

    tasks = Path("TASKS.md").read_text(
        encoding="utf-8"
    )

    decisions = Path("DECISIONS.md").read_text(
        encoding="utf-8"
    )

    handoff = Path("HANDOFF.md").read_text(
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