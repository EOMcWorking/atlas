from src.services.ollama_service import chat


def review(
    code: str
):

    prompt = f"""
Review the following code:

{code}

Identify:
- Bugs
- Improvements
- Security Issues
- Refactoring Opportunities
"""

    return chat(
        prompt,
        task_type="review"
    )