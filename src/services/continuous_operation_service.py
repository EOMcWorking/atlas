import time

from src.services.atlas_state_service import (
    get_state,
    update_state
)

from src.services.task_queue_service import (
    get_next_task
)

from src.services.agent_orchestrator import (
    run_task
)

from src.services.approval_processor_service import (
    process_approved_tasks
)


def run_continuously():

    failure_count = 0

    while True:

        try:

            process_approved_tasks()

        except Exception as e:

            print(
                f"Approval error: {e}"
            )

        task = get_next_task()

        if not task:

            update_state(
                status="idle"
            )

            time.sleep(
                300
            )

            continue

        update_state(
            status="running",
            current_task=task
        )

        result = run_task(
            task
        )

        if result.get(
            "success",
            False
        ):

            failure_count = 0

        else:

            failure_count += 1

        sleep_time = min(
            300 * max(
                failure_count,
                1
            ),
            3600
        )

        time.sleep(
            sleep_time
        )