from src.services.autonomous_goal_service import (
    get_primary_goal
)

from src.services.ollama_service import (
    chat
)

def generate_goal_plan():

    goal = (
        get_primary_goal()
    )

    if not goal:

        return {
            "success": False,
            "message": "No active goal"
        }

    prompt = f"""
Primary Goal:

{goal['title']}

Create:

1. Milestones
2. Improvements
3. Recommended execution order

Return concise output.
"""

    result = chat(
        prompt,
        task_type="planning"
    )

    return {
        "success": True,
        "goal": goal,
        "plan": result
    }

def get_goal_plan():

    result = (
        generate_goal_plan()
    )

    return result.get(
        "plan",
        ""
    )