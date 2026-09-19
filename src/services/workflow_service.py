from src.services.agent_orchestrator import (
    run_task
)


def execute_workflow(
    task: str,
    project_name: str = None
):
    return run_task(
        task
    )