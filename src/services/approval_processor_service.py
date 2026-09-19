from src.services.approval_service import (
    load_approvals,
    save_approvals
)

from src.services.git_commit_service import (
    create_commit
)

from src.services.pull_request_service import (
    generate_pull_request
)

from src.services.handoff_service import (
    update_handoff
)


def process_approved_tasks():

    approvals = load_approvals()

    processed = []

    for approval in approvals:

        if not approval.get(
            "approved",
            False
        ):
            continue

        if approval.get(
            "processed",
            False
        ):
            continue

        task = approval[
            "task"
        ]

        # Attempt commit — check result before continuing
        commit_result = create_commit(
            f"Atlas: {task}"
        )

        if not commit_result.get("success", False):
            print(f"Commit failed for: {task}")
            continue

        # Only generate PR after successful commit
        pr_text = (
            generate_pull_request(
                task,
                approval.get(
                    "summary",
                    ""
                ),
                approval.get(
                    "summary",
                    ""
                )
            )
        )

        update_handoff(
            f"""
Approved Task:

{task}

Pull Request Draft:

{pr_text}
"""
        )

        approval[
            "processed"
        ] = True

        processed.append(
            task
        )

    # Fix 1: Persist processed flag back to disk
    save_approvals(approvals)

    return processed