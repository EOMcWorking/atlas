from src.services.ollama_service import (
    chat
)


def generate_commit_message(
    git_status: str
):

    prompt = f"""
Generate a concise git commit message.

Git Status:

{git_status}

Use conventional commits.

Examples:

feat(auth): add JWT middleware

fix(api): repair provider routing

refactor(memory): simplify context builder
"""

    return chat(
        prompt,
        task_type="planning"
    )