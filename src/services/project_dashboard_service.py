from src.services.project_health_service import (
    calculate_project_health
)

from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.change_history_service import (
    get_recent_changes
)

from src.services.approval_service import (
    get_pending_approvals
)

from src.services.task_queue_service import (
    get_next_task
)


def build_dashboard():

    health = (
        calculate_project_health()
    )

    failures = (
        analyze_failures()
    )

    approvals = (
        get_pending_approvals()
    )

    recent_changes = (
        get_recent_changes(
            limit=10
        )
    )

    next_task = (
        get_next_task()
    )

    return {

        "health":
        health,

        "failures":
        failures,

        "pending_approvals":
        len(
            approvals
        ),

        "recent_changes":
        recent_changes,

        "next_task":
        next_task
    }

def dashboard_summary():

    dashboard = (
        build_dashboard()
    )

    return f"""
Health:
{dashboard['health']['health']}

Score:
{dashboard['health']['score']}

Pending Approvals:
{dashboard['pending_approvals']}

Next Task:
{dashboard['next_task']}
"""

def dashboard_status():

    health = (
        calculate_project_health()
    )

    if (
        health["health"]
        == "Critical"
    ):
        return "RED"

    if (
        health["health"]
        == "Poor"
    ):
        return "YELLOW"

    return "GREEN"