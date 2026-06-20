from pathlib import Path
import json

METRICS_FILE = Path(
    "provider_metrics.json"
)


def load_metrics():

    if not METRICS_FILE.exists():

        return {}

    return json.loads(
        METRICS_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_metrics(metrics):

    METRICS_FILE.write_text(
        json.dumps(
            metrics,
            indent=2
        ),
        encoding="utf-8"
    )


def record_success(
    provider_name: str
):

    metrics = load_metrics()

    provider = metrics.setdefault(
        provider_name,
        {
            "success": 0,
            "failures": 0
        }
    )

    provider["success"] += 1

    save_metrics(metrics)

def get_metrics():

    return load_metrics()


def record_failure(
    provider_name: str
):

    metrics = load_metrics()

    provider = metrics.setdefault(
        provider_name,
        {
            "success": 0,
            "failures": 0
        }
    )

    provider["failures"] += 1

    save_metrics(metrics)