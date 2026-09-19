from src.services.autonomous_goal_service import (
    get_primary_goal
)

from src.services.ollama_service import (
    chat
)

from src.services.goal_planning_service import (
    get_goal_plan
)


def analyze_alignment(
    work_item: str
):

    goal = (
        get_primary_goal()
    )

    if not goal:

        return {

            "score": 50,

            "reason":
            "No active goal"
        }

    goal_plan = get_goal_plan()

    prompt = f"""
Primary Goal:

{goal['title']}

Goal Plan:

{goal_plan}

Work Item:

{work_item}

Rate alignment from 0-100.

Return:

Score:
Reason:
"""

    result = chat(
        prompt,
        task_type="analysis"
    )

    return {

        "score":
        extract_alignment_score(
            result
        ),

        "reason":
        result
    }


def extract_alignment_score(
    text: str
):

    digits = []

    for c in text:

        if c.isdigit():

            digits.append(c)

    if not digits:

        return 50

    value = int(
        "".join(digits[:3])
    )

    return min(
        value,
        100
    )


def get_alignment_score(
    work_item: str
):

    result = (
        analyze_alignment(
            work_item
        )
    )

    return result[
        "score"
    ]