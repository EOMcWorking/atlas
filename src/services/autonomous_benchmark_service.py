import json
from pathlib import Path

from src.services.workflow_metrics_service import (
    get_workflow_metrics
)
from src.services.workspace_service import (
    get_memory_path
)


def get_benchmark_file():
    """
    Return the benchmark file inside the configured
    Atlas memory directory.
    """
    memory_path = Path(get_memory_path())
    memory_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return memory_path / "benchmarks.json"


def load_benchmarks():

    benchmark_file = get_benchmark_file()

    if not benchmark_file.exists():

        return []

    try:
        data = json.loads(
            benchmark_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError):
        return []


def save_benchmarks(data):

    benchmark_file = get_benchmark_file()

    benchmark_file.write_text(

        json.dumps(
            data,
            indent=2
        ),

        encoding="utf-8"
    )


def capture_benchmark():

    metrics = (
        get_workflow_metrics()
    )

    history = (
        load_benchmarks()
    )

    history.append(
        metrics
    )

    save_benchmarks(
        history
    )

    return metrics


def get_latest_benchmark():

    history = (
        load_benchmarks()
    )

    if not history:

        return None

    return history[-1]


def compare_benchmarks():

    history = (
        load_benchmarks()
    )

    if len(history) < 2:

        return None

    previous = history[-2]

    current = history[-1]

    return {

        "previous":
        previous,

        "current":
        current
    }


def get_benchmark_report():

    return {

        "latest":
        get_latest_benchmark(),

        "comparison":
        compare_benchmarks()
    }