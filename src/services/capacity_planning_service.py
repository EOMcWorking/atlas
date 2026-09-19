from src.services.task_queue_service import (
    get_pending_tasks
)

from src.services.workflow_metrics_service import (
    get_workflow_metrics
)

def get_current_capacity():

    metrics = (
        get_workflow_metrics()
    )

    return {

        "average_runtime":
        metrics.get(
            "average_runtime",
            0
        ),

        "success_rate":
        metrics.get(
            "success_rate",
            0
        )
    }

def get_queue_pressure():

    tasks = (
        get_pending_tasks()
    )

    return len(
        tasks
    )

def get_capacity_status():

    queue_size = (
        get_queue_pressure()
    )

    if queue_size < 20:

        return "NORMAL"

    if queue_size < 50:

        return "HIGH"

    return "OVERLOADED"

def get_capacity_recommendations():

    status = (
        get_capacity_status()
    )

    recommendations = []

    if status == "HIGH":

        recommendations.append(
            "Reduce low-priority work"
        )

    elif status == "OVERLOADED":

        recommendations.append(
            "Pause self-improvement tasks"
        )

        recommendations.append(
            "Process backlog first"
        )

    return recommendations

def get_capacity_report():

    return {

        "status":
        get_capacity_status(),

        "queue_size":
        get_queue_pressure(),

        "capacity":
        get_current_capacity(),

        "recommendations":
        get_capacity_recommendations()
    }
