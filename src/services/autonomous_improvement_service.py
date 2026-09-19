from src.services.project_evolution_service import (
    generate_project_evolution
)

from src.services.task_generation_service import (
    generate_next_task
)

from src.services.task_tracker_service import (
    add_task
)

from src.services.memory_capture_service import (
    save_agent_memory
)


def generate_improvement_task():

    evolution = (
        generate_project_evolution()
    )

    task = generate_next_task()

    if not task:
        return {
            "success": False,
            "message": "No improvement task generated"
        }

    add_task(task)

    save_agent_memory(
        "Autonomous Improvement",
        f"""
Evolution Report:

{evolution}

Generated Task:

{task}
"""
    )

    return {
        "success": True,
        "task": task,
        "evolution": evolution
    }