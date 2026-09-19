from src.services.self_improvement_board_service import (
    get_next_improvement,
    complete_improvement
)

from src.services.task_tracker_service import (
    add_task
)

def improvement_to_task(
    improvement
):

    return f"""
SELF IMPROVEMENT:

{improvement['title']}

Reason:

{improvement['reason']}
"""

def schedule_next_improvement():

    improvement = (
        get_next_improvement()
    )

    if not improvement:

        return {

            "success": False,

            "message":
            "No improvements available"
        }

    task = (
        improvement_to_task(
            improvement
        )
    )

    add_task(
        task
    )

    complete_improvement(
        improvement[
            "title"
        ]
    )

    return {

        "success": True,

        "task":
        task,

        "improvement":
        improvement
    }

def schedule_improvements(
    limit: int = 3
):

    results = []

    for _ in range(limit):

        result = (
            schedule_next_improvement()
        )

        if not result["success"]:

            break

        results.append(
            result
        )

    return results
