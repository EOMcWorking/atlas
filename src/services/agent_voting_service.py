from src.services.ollama_service import chat


def vote_on_solution(
    task: str,
    research_result: str,
    architecture_result: str,
    review_result: str
):

    prompt = f"""
Task:

{task}

Research Agent:

{research_result}

Architect Agent:

{architecture_result}

Reviewer Agent:

{review_result}

Choose the best approach.

Return:

Winner:
Reason:
Final Recommendation:
"""

    return chat(
        prompt,
        task_type="planning"
    )