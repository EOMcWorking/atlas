from src.services.workflow_metrics_service import (
    get_workflow_metrics
)

from src.services.strategy_evaluation_service import (
    get_strategy_report
)

from src.services.self_improvement_board_service import (
    get_open_improvements
)

from src.services.task_queue_service import (
    get_pending_tasks
)

def build_dashboard():

    metrics = (
        get_workflow_metrics()
    )

    strategies = (
        get_strategy_report()
    )

    improvements = (
        get_open_improvements()
    )

    tasks = (
        get_pending_tasks()
    )

    return {

        "metrics":
        metrics,

        "strategies":
        strategies,

        "open_improvements":
        len(improvements),

        "pending_tasks":
        len(tasks)
    }

def calculate_health_score():

    dashboard = (
        build_dashboard()
    )

    score = 100

    score -= min(
        dashboard[
            "open_improvements"
        ],
        20
    )

    score -= min(
        dashboard[
            "pending_tasks"
        ],
        20
    )

    return max(
        score,
        0
    )

def get_health_report():

    dashboard = (
        build_dashboard()
    )

    dashboard[
        "health_score"
    ] = (
        calculate_health_score()
    )

    return dashboard
