from src.services.ollama_service import chat
from src.services.code_cleaner_service import clean_code_response


def code(task: str):

    prompt = f"""
You are a senior software engineer.

TASK:
{task}

Rules:
- Return ONLY code
- No explanations
- No markdown
- No code fences
- No example usage
- No comments unless required
- Output must be directly usable
"""

    response = chat(
        prompt,
        task_type="coding"
    )

    return clean_code_response(
        response
    )