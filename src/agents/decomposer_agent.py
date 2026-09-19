from src.services.ollama_service import chat


def decompose(task: str):

    prompt = f"""
You are a software task decomposer.

Task:
{task}

Rules:
- Return at most 3 subtasks
- Keep each subtask under 15 words
- No explanations
- No documentation tasks
- No testing tasks
- No planning tasks

Format:

1. ...
2. ...
3. ...
"""

    return chat(
        prompt,
        task_type="planning"
    )