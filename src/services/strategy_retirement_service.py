from src.services.strategy_memory_service import (
    load_strategies,
    save_strategies,
    get_worst_strategies
)

from src.services.strategy_evaluation_service import (
    evaluate_all_strategies
)

RETIREMENT_THRESHOLD = 40


def find_retirement_candidates():

    evaluations = (
        evaluate_all_strategies()
    )

    candidates = []

    for item in evaluations:

        if (
            item["score"]
            < RETIREMENT_THRESHOLD
        ):

            candidates.append(
                item["strategy"]
            )

    # Also add worst strategies from memory
    worst = get_worst_strategies()
    for strategy in worst[:3]:
        name = strategy.get("name", "")
        if name and name not in candidates:
            candidates.append(name)

    return candidates


def retire_strategies():

    strategies = (
        load_strategies()
    )

    candidates = (
        find_retirement_candidates()
    )

    remaining = [

        s

        for s in strategies

        if s not in candidates
    ]

    save_strategies(
        remaining
    )

    return {

        "retired":
        candidates,

        "remaining":
        remaining
    }


def get_retirement_report():

    return {

        "candidates":
        find_retirement_candidates()
    }