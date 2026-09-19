from pathlib import Path
import json


RETRY_FILE = Path(
    "retry_state.json"
)


def load_retry_state():

    if not RETRY_FILE.exists():
        return {}

    return json.loads(
        RETRY_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_retry_state(
    state
):

    RETRY_FILE.write_text(
        json.dumps(
            state,
            indent=2
        ),
        encoding="utf-8"
    )


def increment_retry(
    task: str
):

    state = load_retry_state()

    state[task] = (
        state.get(task, 0)
        + 1
    )

    save_retry_state(
        state
    )

    return state[task]


def get_retry_count(
    task: str
):

    state = load_retry_state()

    return state.get(
        task,
        0
    )


def clear_retry(
    task: str
):

    state = load_retry_state()

    if task in state:

        del state[task]

        save_retry_state(
            state
        )