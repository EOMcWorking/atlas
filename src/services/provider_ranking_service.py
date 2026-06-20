from src.services.provider_metrics_service import (
    get_metrics
)

from src.services.provider_cost_service import (
    get_provider_costs
)


def get_ranked_providers():

    metrics = get_metrics()

    costs = get_provider_costs()

    scores = []

    for provider, cost in costs.items():

        stats = metrics.get(
            provider,
            {}
        )

        success = stats.get(
            "success",
            0
        )

        failures = stats.get(
            "failures",
            0
        )

        latencies = stats.get(
            "latency",
            []
        )

        avg_latency = (
            sum(latencies) / len(latencies)
            if latencies
            else 1
        )

        score = (
            (success * 10)
            - (failures * 5)
            - cost
            - avg_latency
        )

        scores.append(
            (
                score,
                provider
            )
        )

    scores.sort(
        reverse=True
    )

    return [
        provider
        for score, provider
        in scores
    ]