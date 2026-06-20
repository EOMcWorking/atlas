from src.services.ollama_service import chat


def plan(
    task: str
):

    prompt = f"""
Create a development plan for:

{task}

Return:
1. Goal
2. Steps
3. Risks
4. Success Criteria
"""

    return chat(
        prompt,
        task_type="planning"
    )