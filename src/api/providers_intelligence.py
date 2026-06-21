from fastapi import APIRouter

from src.services.provider_metrics_service import (
    get_metrics
)

from src.services.provider_task_metrics_service import (
    load_task_metrics
)

from src.services.provider_cooldown_service import (
    load_cooldowns
)

from src.services.provider_ranking_service import (
    get_ranked_providers
)

router = APIRouter()


@router.get("/providers/metrics")
def provider_metrics():

    return get_metrics()


@router.get("/providers/task-metrics")
def provider_task_metrics():

    return load_task_metrics()


@router.get("/providers/cooldowns")
def provider_cooldowns():

    return load_cooldowns()


@router.get("/providers/rankings")
def provider_rankings():

    return {
        "rankings": get_ranked_providers()
    }