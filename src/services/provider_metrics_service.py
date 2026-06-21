from pathlib import Path
import json

import time

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

def record_latency(
    provider_name: str,
    latency: float
):

    metrics = load_metrics()

    provider = metrics.setdefault(
        provider_name,
        {
            "success": 0,
            "failures": 0,
            "latency": []
        }
    )

    provider.setdefault(
        "latency",
        []
    )

    provider["latency"].append(
        latency
    )

    provider["latency"] = (
        provider["latency"][-20:]
    )

    save_metrics(metrics)

def get_average_latency(
    provider_name: str
):

    metrics = load_metrics()

    provider = metrics.get(
        provider_name,
        {}
    )

    latencies = provider.get(
        "latencies",
        []
    )

    if not latencies:
        return 999

    return (
        sum(latencies)
        / len(latencies)
    )