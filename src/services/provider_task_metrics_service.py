from pathlib import Path
import json

TASK_METRICS_FILE = Path(
    "provider_task_metrics.json"
)


def load_task_metrics():

    if not TASK_METRICS_FILE.exists():
        return {}

    return json.loads(
        TASK_METRICS_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_task_metrics(
    metrics
):

    TASK_METRICS_FILE.write_text(
        json.dumps(
            metrics,
            indent=2
        ),
        encoding="utf-8"
    )


def record_task_success(
    task_type: str,
    provider_name: str
):

    metrics = load_task_metrics()

    task_data = metrics.setdefault(
        task_type,
        {}
    )

    provider = task_data.setdefault(
        provider_name,
        {
            "success": 0,
            "failure": 0
        }
    )

    provider["success"] += 1

    save_task_metrics(
        metrics
    )

def get_task_winner(
    task_type: str
):

    metrics = load_task_metrics()

    task_data = metrics.get(
        task_type,
        {}
    )

    if not task_data:
        return None

    best_provider = None
    best_score = -999999

    for provider, stats in task_data.items():

        score = (
            stats.get(
                "success",
                0
            ) * 10
            -
            stats.get(
                "failure",
                0
            ) * 5
        )

        if score > best_score:

            best_score = score
            best_provider = provider

    return best_provider

def record_task_failure(
    task_type: str,
    provider_name: str
):

    metrics = load_task_metrics()

    task_data = metrics.setdefault(
        task_type,
        {}
    )

    provider = task_data.setdefault(
        provider_name,
        {
            "success": 0,
            "failure": 0
        }
    )

    provider["failure"] += 1

    save_task_metrics(
        metrics
    )

def get_task_score(
    task_type: str,
    provider_name: str
):

    metrics = load_task_metrics()

    task_data = metrics.get(
        task_type,
        {}
    )

    provider = task_data.get(
        provider_name,
        {}
    )

    success = provider.get(
        "success",
        0
    )

    failure = provider.get(
        "failure",
        0
    )

    return (
        success * 5
        - failure * 3
    )