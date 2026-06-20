from src.services.ollama_service import chat


def code(
    task: str
):

    prompt = f"""
Write code for:

{task}

Provide only the code
and necessary explanation.
"""

    return chat(
        prompt,
        task_type="coding"
    )