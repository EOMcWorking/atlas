from src.services.task_classifier import (
    classify_task
)


def assign_task(
    task: str
):

    complexity = classify_task(
        task
    )

    return {
        "complexity": complexity
    }