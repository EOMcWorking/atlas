from pathlib import Path
import json
import time

from src.services.workspace_service import get_memory_path


def get_state_file():
    """
    Return the Atlas state file inside the configured
    Atlas memory directory.
    """
    memory_path = Path(get_memory_path())
    memory_path.mkdir(parents=True, exist_ok=True)
    return memory_path / "atlas_state.json"


def get_default_state():
    return {
        "status": "idle",
        "current_task": None,
        "last_task": None,
        "last_success": None,
        "last_failure": None,
        "tasks_completed": 0,
        "tasks_failed": 0,
        "uptime_start": time.time(),
        "last_checkpoint": None,
        "last_shutdown": None,
        "runtime_cycles": 0,
        "benchmark_runs": 0,
        "director_mode": "NORMAL_EXECUTION",
    }


def load_state():
    state_file = get_state_file()

    if not state_file.exists():
        state = get_default_state()
        save_state(state)
        return state

    try:
        return json.loads(
            state_file.read_text(
                encoding="utf-8"
            )
        )
    except (json.JSONDecodeError, OSError):
        # Corrupted JSON recovery
        state = get_default_state()
        save_state(state)
        return state


def save_state(state):
    """
    Atomic write — writes to .tmp first, then replaces.
    Prevents corruption if Atlas crashes mid-write.
    """
    state_file = get_state_file()
    tmp = state_file.with_suffix(".tmp")

    tmp.write_text(
        json.dumps(
            state,
            indent=2
        ),
        encoding="utf-8"
    )

    tmp.replace(state_file)


def update_state(**kwargs):
    state = load_state()

    state.update(kwargs)

    save_state(state)

    return state


def increment_counter(name: str):
    """
    Safely increment a counter in state.
    """
    state = load_state()
    state[name] = state.get(name, 0) + 1
    save_state(state)
    return state[name]


def flush_state():
    """
    Persist the latest Atlas state.

    Currently state is written immediately on every update,
    so flushing simply reloads and rewrites the latest state.
    """
    state = load_state()
    state["last_checkpoint"] = time.time()
    save_state(state)
    return state


def mark_task_started(task: str):
    return update_state(
        status="running",
        current_task=task
    )


def mark_task_success(task: str):
    state = load_state()

    state["status"] = "idle"
    state["current_task"] = None
    state["last_task"] = task
    state["last_success"] = task
    state["tasks_completed"] = (
        state.get("tasks_completed", 0) + 1
    )

    save_state(state)

    return state


def mark_task_failure(task: str):
    state = load_state()

    state["status"] = "idle"
    state["current_task"] = None
    state["last_task"] = task
    state["last_failure"] = task
    state["tasks_failed"] = (
        state.get("tasks_failed", 0) + 1
    )

    save_state(state)

    return state


def record_shutdown():
    """
    Record a clean shutdown in state.
    """
    state = load_state()
    state["last_shutdown"] = time.time()
    state["status"] = "shutdown"

    save_state(state)

    return state


def record_cycle():
    """
    Increment the runtime cycle counter.
    """
    return increment_counter("runtime_cycles")


def record_benchmark():
    """
    Increment the benchmark runs counter.
    """
    return increment_counter("benchmark_runs")


def set_director_mode(mode: str):
    """
    Update the current director mode in state.
    """
    return update_state(
        director_mode=mode
    )


def get_state():
    return load_state()