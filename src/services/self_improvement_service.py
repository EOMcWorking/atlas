from src.services.project_health_service import (
    calculate_project_health
)

from src.services.root_cause_analysis_service import (
    get_root_cause_summary
)

from src.services.adaptive_learning_service import (
    get_problem_files
)

from src.services.ollama_service import (
    chat
)


def generate_self_improvements():

    health = (
        calculate_project_health()
    )

    root_causes = (
        get_root_cause_summary()
    )

    problem_files = (
        get_problem_files()
    )

    prompt = f"""
You are Atlas Self Improvement Agent.

PROJECT HEALTH:

{health}

ROOT CAUSES:

{root_causes}

PROBLEM FILES:

{problem_files}

Recommend:

1. Internal Atlas improvements
2. Workflow improvements
3. Prompt improvements
4. Architecture improvements

Return only actionable tasks.
"""

    return chat(
        prompt,
        task_type="planning"
    )

def extract_improvement_tasks():

    result = (
        generate_self_improvements()
    )

    tasks = []

    for line in result.splitlines():

        line = line.strip()

        if not line:
            continue

        if len(line) < 10:
            continue

        tasks.append(
            line
        )

    return tasks

from src.services.task_tracker_service import (
    add_task
)


def queue_self_improvements():

    tasks = (
        extract_improvement_tasks()
    )

    for task in tasks:

        add_task(task)

    return len(tasks)