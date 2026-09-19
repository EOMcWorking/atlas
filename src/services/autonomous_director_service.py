from src.services.goal_management_service import (
    get_active_goals
)

from src.services.milestone_service import (
    get_active_milestones
)

from src.services.project_health_service import (
    health_summary
)

from src.services.ollama_service import (
    chat
)

def build_director_report():

    goals = (
        get_active_goals()
    )

    milestones = (
        get_active_milestones()
    )

    health = (
        health_summary()
    )

    return {

        "goals": goals,

        "milestones": milestones,

        "health": health
    }

def choose_priority():

    report = (
        build_director_report()
    )

    prompt = f"""
You are Atlas Director.

STATE:

{report}

Choose:

1. Highest priority goal
2. Highest priority milestone
3. Reason

Return concise output.
"""

    return chat(
        prompt,
        task_type="planning"
    )

def choose_focus():

    report = (
        build_director_report()
    )

    health = report.get(
        "health",
        {}
    )

    score = health.get(
        "score",
        100
    )

    if score < 60:

        return "SELF_IMPROVEMENT"

    return "PROJECT_WORK"

def get_directive():

    return {

        "focus":
        choose_focus(),

        "priority":
        choose_priority()
    }

