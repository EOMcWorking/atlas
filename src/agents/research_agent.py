from src.services.ollama_service import chat


def research(
    task: str
):

    prompt = f"""
Research the following development task.

Task:
{task}

Provide:

- Relevant architecture
- Existing project components
- Risks
- Implementation suggestions
"""

    return chat(
        prompt,
        task_type="general"
    )