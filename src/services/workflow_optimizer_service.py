from src.services.workflow_metrics_service import (
    load_metrics
)

def analyze_workflows():

    metrics = load_metrics()

    strategies = {}

    for item in metrics:

        strategy = item.get(
            "strategy",
            "UNKNOWN"
        )

        if strategy not in strategies:

            strategies[
                strategy
            ] = {

                "runs": 0,
                "successes": 0,
                "runtime": 0
            }

        strategies[
            strategy
        ]["runs"] += 1

        if item.get(
            "success",
            False
        ):
            strategies[
                strategy
            ]["successes"] += 1

        strategies[
            strategy
        ]["runtime"] += item.get(
            "duration",
            0
        )

    return strategies

def get_best_strategy():

    data = (
        analyze_workflows()
    )

    winner = None

    best_score = -1

    for strategy, stats in data.items():

        runs = max(
            stats["runs"],
            1
        )

        success_rate = (
            stats["successes"]
            / runs
        )

        score = success_rate

        if score > best_score:

            best_score = score

            winner = strategy

    return winner

def recommend_strategy():

    best = (
        get_best_strategy()
    )

    return {

        "recommended":
        best
    }