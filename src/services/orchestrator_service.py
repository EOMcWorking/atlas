from src.services.ollama_service import chat


def assign_task(task: str):
    task_lower = task.lower()

    if any(
        word in task_lower
        for word in [
            "review",
            "audit",
            "check",
            "analyze"
        ]
    ):
        return {
            "agent": "reviewer",
            "task_type": "review"
        }

    if any(
        word in task_lower
        for word in [
            "code",
            "bug",
            "python",
            "api",
            "database"
        ]
    ):
        return {
            "agent": "coder",
            "task_type": "coding"
        }

    return {
        "agent": "planner",
        "task_type": "planning"
    }