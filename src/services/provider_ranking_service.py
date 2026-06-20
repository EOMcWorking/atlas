from src.services.provider_metrics_service import (
    get_metrics
)

from src.services.provider_cost_service import (
    get_provider_costs
)


def rank_providers():

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

        score = (
            (success * 10)
            - (failures * 5)
            - cost
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