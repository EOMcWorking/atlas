from src.services.ollama_service import (
    chat
)


def generate_objective_plan(
    objective: str
):

    prompt = f"""
You are Atlas Strategic Planner.

OBJECTIVE:

{objective}

Generate:

1. Goals
2. Milestones
3. Tasks

Hierarchy:

Objective
 -> Goals
 -> Milestones
 -> Tasks

Return concise output.
"""

    return chat(
        prompt,
        task_type="planning"
    )

def extract_goals(
    plan: str
):

    goals = []

    for line in plan.splitlines():

        line = line.strip()

        if line.lower().startswith(
            "goal"
        ):

            goals.append(
                line
            )

    return goals

def extract_milestones(
    plan: str
):

    milestones = []

    for line in plan.splitlines():

        line = line.strip()

        if line.lower().startswith(
            "milestone"
        ):

            milestones.append(
                line
            )

    return milestones

def extract_tasks(
    plan: str
):

    tasks = []

    for line in plan.splitlines():

        line = line.strip()

        if line.lower().startswith(
            "task"
        ):

            tasks.append(
                line
            )

    return tasks

def build_objective_tree(
    objective: str
):

    plan = (
        generate_objective_plan(
            objective
        )
    )

    return {

        "objective":
        objective,

        "goals":
        extract_goals(
            plan
        ),

        "milestones":
        extract_milestones(
            plan
        ),

        "tasks":
        extract_tasks(
            plan
        ),

        "raw":
        plan
    }

