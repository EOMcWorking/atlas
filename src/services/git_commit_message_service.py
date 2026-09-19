from src.services.ollama_service import chat


def generate_commit_message(
    task: str
):

    prompt = f"""
Generate a concise git commit message.

TASK:
{task}

Return only the commit message.
"""

    return chat(
        prompt,
        task_type="planning"
    )