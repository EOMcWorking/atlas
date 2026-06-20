from src.services.ollama_service import chat


def analyze(
    context: str
):

    prompt = f"""
Analyze the architecture:

{context}

Provide:
- Strengths
- Weaknesses
- Risks
- Recommendations
"""

    return chat(
        prompt,
        task_type="planning"
    )