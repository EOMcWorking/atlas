from src.services.system_health_dashboard_service import (
    get_health_report
)

from src.services.self_improvement_board_service import (
    add_improvement
)

from src.services.goal_progress_service import (
    refresh_goal_progress
)

from src.services.autonomous_benchmark_service import (
    capture_benchmark
)

MIN_HEALTH_SCORE = 70

MAX_PENDING_TASKS = 50

MAX_OPEN_IMPROVEMENTS = 25

def monitor_health():

    report = (
        get_health_report()
    )

    alerts = []

    if (

        report[
            "health_score"
        ]

        <

        MIN_HEALTH_SCORE

    ):

        alerts.append(
            "LOW_HEALTH_SCORE"
        )

    if (

        report[
            "pending_tasks"
        ]

        >

        MAX_PENDING_TASKS

    ):

        alerts.append(
            "TASK_BACKLOG"
        )

    if (

        report[
            "open_improvements"
        ]

        >

        MAX_OPEN_IMPROVEMENTS

    ):

        alerts.append(
            "IMPROVEMENT_BACKLOG"
        )

    return alerts

def create_corrective_actions():

    alerts = (
        monitor_health()
    )

    actions = []

    for alert in alerts:

        if alert == (
            "LOW_HEALTH_SCORE"
        ):

            add_improvement(

                "Improve System Health",

                "Health score below threshold",

                priority=10
            )

            actions.append(
                alert
            )

        elif alert == (
            "TASK_BACKLOG"
        ):

            add_improvement(

                "Reduce Task Backlog",

                "Too many queued tasks",

                priority=9
            )

            actions.append(
                alert
            )

        elif alert == (
            "IMPROVEMENT_BACKLOG"
        ):

            add_improvement(

                "Process Improvement Backlog",

                "Too many pending improvements",

                priority=8
            )

            actions.append(
                alert
            )

    return actions

def run_health_monitor():

    # Refresh goal progress before running health checks
    refresh_goal_progress()

    # Capture benchmark snapshot
    capture_benchmark()

    actions = (
        create_corrective_actions()
    )

    return {

        "success": True,

        "actions":
        actions
    }