from src.services.strategy_memory_service import (
    load_strategy_memory,
    remember_strategy
)

from src.services.workflow_metrics_service import (
    get_workflow_metrics
)


def evaluate_strategy(
    strategy: str
):

    metrics = (
        get_workflow_metrics()
    )

    success_rate = metrics.get(
        "success_rate",
        0
    )

    failure_rate = 100 - success_rate

    score = (
        success_rate
        - failure_rate
    )

    return {

        "strategy":
        strategy,

        "score":
        score
    }


def evaluate_all_strategies():

    strategies = (
        load_strategy_memory()
    )

    results = []

    for strategy in strategies:

        result = evaluate_strategy(
            strategy
        )

        # Remember the strategy score
        remember_strategy(
            strategy,
            result["score"]
        )

        results.append(result)

    return results


def get_best_strategy():

    results = (
        evaluate_all_strategies()
    )

    if not results:

        return None

    results.sort(

        key=lambda x:
        x["score"],

        reverse=True
    )

    return results[0]


def get_worst_strategy():

    results = (
        evaluate_all_strategies()
    )

    if not results:

        return None

    results.sort(

        key=lambda x:
        x["score"]
    )

    return results[0]


def get_strategy_report():

    return {

        "best":
        get_best_strategy(),

        "worst":
        get_worst_strategy(),

        "all":
        evaluate_all_strategies()
    }