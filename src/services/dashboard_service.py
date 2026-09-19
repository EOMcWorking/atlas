from src.services.database_service import (
    get_connection
)


def get_workflow_stats():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM workflow_metrics
        """
    )

    total_tasks = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM workflow_metrics
        WHERE success = 1
        """
    )

    successful_tasks = (
        cursor.fetchone()[0]
    )

    cursor.execute(
        """
        SELECT AVG(duration)
        FROM workflow_metrics
        """
    )

    avg_duration = (
        cursor.fetchone()[0]
    )

    conn.close()

    return {
        "total_tasks": total_tasks,
        "successful_tasks": successful_tasks,
        "success_rate":
            (
                successful_tasks
                / total_tasks
            )
            if total_tasks
            else 0,
        "average_duration":
            avg_duration or 0
    }