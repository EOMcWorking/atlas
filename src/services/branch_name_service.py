from src.services.ollama_service import (
    chat
)


def generate_branch_name(
    task: str
):

    prompt = f"""
Generate a git branch name.

Task:

{task}

Examples:

feature/provider-learning

feature/task-decomposition

fix/reviewer-loop

refactor/context-builder

Return only the branch name.
"""

    return chat(
        prompt,
        task_type="planning"
    ).strip()