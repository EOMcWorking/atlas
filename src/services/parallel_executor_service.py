from concurrent.futures import (
    ThreadPoolExecutor
)

from src.services.subtask_executor_service import (
    execute_subtask
)


def execute_subtasks_parallel(
    subtasks
):

    with ThreadPoolExecutor(
        max_workers=3
    ) as executor:

        results = list(
            executor.map(
                execute_subtask,
                subtasks
            )
        )

    return results