from pathlib import Path
import json
from datetime import datetime


HISTORY_FILE = Path(
    "change_history.json"
)


def load_history():

    if not HISTORY_FILE.exists():
        return []

    return json.loads(
        HISTORY_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_history(
    history
):

    HISTORY_FILE.write_text(
        json.dumps(
            history,
            indent=2
        ),
        encoding="utf-8"
    )


def record_change(
    task: str,
    files: list,
    risk: str,
    policy: str,
    success: bool
):

    history = load_history()

    history.append(
        {
            "timestamp":
            datetime.utcnow().isoformat(),

            "task": task,

            "files": files,

            "risk": risk,

            "policy": policy,

            "success": success
        }
    )

    save_history(
        history
    )

    return True

def get_recent_changes(
    limit: int = 20
):

    history = load_history()

    return history[-limit:]

def get_failed_changes():

    return [
        item
        for item
        in load_history()
        if not item.get(
            "success",
            False
        )
    ]

def get_changes_for_file(
    file_path: str
):

    return [
        item
        for item
        in load_history()
        if file_path in item.get(
            "files",
            []
        )
    ]