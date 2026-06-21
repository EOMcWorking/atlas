from src.services.provider_metrics_service import (
    get_metrics,
    get_average_latency
)

from src.services.provider_cost_service import (
    get_provider_costs
)

from src.services.provider_task_metrics_service import (
    get_task_score
)


def get_ranked_providers(
    task_type: str = "general"
):

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

        latency = get_average_latency(
            provider
        )

        task_score = get_task_score(
            task_type,
            provider
        )

        score = (
            (success * 10)
            - (failures * 8)
            - (latency * 2)
            - (cost * 5)
            + task_score
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