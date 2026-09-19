from src.services.file_relevance_service import (
    rank_relevant_files
)

from src.services.impact_analysis_service import (
    analyze_impact
)

from src.services.ollama_service import (
    chat
)


def create_change_plan(
    task: str
):

    files = rank_relevant_files(
        task,
        limit=10
    )

    impact = []

    for file in files[:5]:

        impact.append(
            analyze_impact(
                file
            )
        )

    prompt = f"""
Task:

{task}

Candidate Files:

{files}

Impact Analysis:

{impact}

Create:

1. Files to modify
2. Reason for each file
3. Estimated risk
4. Recommended order

Keep concise.
"""

    return chat(
        prompt,
        task_type="planning"
    )