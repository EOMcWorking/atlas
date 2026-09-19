from src.services.ollama_service import chat


def patch_code(
    task: str,
    file_path: str,
    context: str
):

    prompt = f"""
You are modifying an existing file.

TASK:
{task}

FILE:
{file_path}

CONTEXT:

{context}

Requirements:
- Return the COMPLETE updated file
- Preserve existing functionality
- Apply only the requested changes
- No markdown
- No explanations
- No code fences
"""

    return chat(
        prompt,
        task_type="coding"
    )