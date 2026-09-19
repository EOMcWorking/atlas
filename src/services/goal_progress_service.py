from src.services.autonomous_goal_service import (
    get_primary_goal,
    update_goal_progress
)

from src.services.system_health_dashboard_service import (
    get_health_report
)

from src.services.milestone_tracking_service import (
    get_milestone_report
)


def estimate_goal_progress():

    goal = (
        get_primary_goal()
    )

    if not goal:

        return 0

    health = (
        get_health_report()
    )

    milestones = (
        get_milestone_report()
    )

    health_score = health.get(
        "health_score",
        0
    )

    milestone_progress = milestones.get(
        "progress",
        0
    )

    # Weighted average: 40% health, 60% milestone completion
    progress = int(
        health_score * 0.4
        + milestone_progress * 0.6
    )

    return min(
        progress,
        100
    )


def refresh_goal_progress():

    goal = (
        get_primary_goal()
    )

    if not goal:

        return {
            "success": False
        }

    progress = (
        estimate_goal_progress()
    )

    update_goal_progress(
        goal["title"],
        progress
    )

    return {
        "success": True,
        "goal": goal["title"],
        "progress": progress
    }


def get_goal_progress_report():

    goal = (
        get_primary_goal()
    )

    if not goal:

        return None

    return {
        "goal":
        goal["title"],

        "progress":
        goal.get(
            "progress",
            0
        )
    }