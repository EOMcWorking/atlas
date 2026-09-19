from src.services.ollama_service import chat


def review(code: str):

    prompt = f"""
Review this code.

Return ONLY:

VERDICT: APPROVED

or

VERDICT: REJECTED
Reason: <one sentence>

CODE:
{code}
"""

    return chat(
        prompt,
        task_type="review"
    )