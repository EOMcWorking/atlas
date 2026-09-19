from src.services.ollama_service import chat


def architect(
    plan_result: str,
    research_result: str
):

    prompt = f"""
Review this proposed implementation.

PLAN:

{plan_result}

RESEARCH:

{research_result}

Provide:

- Better alternatives
- Architectural concerns
- Scalability concerns
- Final recommendation
"""

    return chat(
        prompt,
        task_type="general"
    )