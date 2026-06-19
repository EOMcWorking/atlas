from src.services.ollama_service import chat
from src.services.rule_inspector_service import inspect_architecture
from src.services.architecture_knowledge_service import build_architecture_knowledge


def review_architecture():
    inspection = (
        inspect_architecture()
    )

    knowledge = (
        build_architecture_knowledge()
    )

    prompt = f"""
You are Atlas Architect.

Analyze ONLY the provided data.

IMPORTANT RULES:

- Only make claims supported by evidence.
- Do not assume CI/CD exists.
- Do not assume tests exist.
- Do not assume team structure.
- Do not assume production usage.
- If evidence is missing, say:
  "Insufficient evidence."

Rule Inspection Findings:

{inspection}  

Architecture Knowledge:

{knowledge}

Return EXACTLY:

## Strengths
- item

## Weaknesses
- item

## Refactoring Opportunities
- item

## Dead Code Concerns
- item

## Highest Priority Improvement
- item
"""

    return chat(
        prompt,
        task_type="review"
    )