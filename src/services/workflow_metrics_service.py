from pathlib import Path
import json
import time

from src.services.workspace_service import (
    get_memory_path
)


def get_metrics_file():

    memory_path = Path(
        get_memory_path()
    )

    memory_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return memory_path / "workflow_metrics.json"


def load_metrics():

    metrics_file = get_metrics_file()

    if not metrics_file.exists():
        return []

    try:

        data = json.loads(
            metrics_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, list):
            return []

        return data

    except (
        json.JSONDecodeError,
        OSError
    ):

        return []


def save_metrics(data):

    metrics_file = get_metrics_file()

    metrics_file.write_text(
        json.dumps(data, indent=2),
        encoding="utf-8"
    )


def record_workflow(
    task: str,
    success: bool,
    duration: float,
    goal: str = None,
    mode: str = None,
    provider: str = None,
    strategy: str = None,
    workflow: str = None,
    complexity: str = None
):

    data = load_metrics()

    data.append(
        {
            "task": task,
            "success": success,
            "duration": duration,
            "timestamp": time.time(),
            "goal": goal,
            "mode": mode,
            "provider": provider,
            "strategy": strategy,
            "workflow": workflow,
            "complexity": complexity
        }
    )

    save_metrics(data)


def get_workflow_metrics():

    data = load_metrics()

    total = len(data)

    if total == 0:
        return {
            "total": 0,
            "success_rate": 0,
            "avg_duration": 0,
            "recent": []
        }

    successes = sum(
        1
        for d in data
        if d.get("success", False)
    )

    durations = [
        d.get("duration", 0)
        for d in data
    ]

    return {
        "total": total,
        "success_rate": int(
            (successes / total) * 100
        ),
        "avg_duration": (
            sum(durations) / len(durations)
        ),
        "recent": data[-10:]
    }