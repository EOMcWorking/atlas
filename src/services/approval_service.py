from pathlib import Path
import json


APPROVAL_FILE = Path(
    "approvals.json"
)


def load_approvals():

    if not APPROVAL_FILE.exists():
        return []

    return json.loads(
        APPROVAL_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_approvals(
    approvals
):

    APPROVAL_FILE.write_text(
        json.dumps(
            approvals,
            indent=2
        ),
        encoding="utf-8"
    )


def create_approval(
    task: str,
    summary: str
):

    approvals = load_approvals()

    approvals.append(
        {
            "task": task,
            "summary": summary,
            "approved": False,
            "rejected": False
        }
    )

    save_approvals(
        approvals
    )


def get_pending_approvals():

    approvals = load_approvals()

    return [
        approval
        for approval in approvals
        if (
            not approval.get(
                "approved",
                False
            )
            and
            not approval.get(
                "rejected",
                False
            )
        )
    ]


def approve_task(
    task: str
):

    approvals = load_approvals()

    for approval in approvals:

        if (
            approval["task"]
            == task
        ):

            approval[
                "approved"
            ] = True

            approval[
                "rejected"
            ] = False

            save_approvals(
                approvals
            )

            return True

    return False


def reject_task(
    task: str
):

    approvals = load_approvals()

    for approval in approvals:

        if (
            approval["task"]
            == task
        ):

            approval[
                "approved"
            ] = False

            approval[
                "rejected"
            ] = True

            save_approvals(
                approvals
            )

            return True

    return False


def approval_exists(
    task: str
):

    approvals = load_approvals()

    return any(
        approval.get(
            "task"
        ) == task
        for approval
        in approvals
    )