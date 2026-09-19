from src.services.strategy_evaluation_service import (
    evaluate_strategy
)

from src.services.strategy_memory_service import (
    save_strategy
)

from src.services.safety_governor_service import (
    is_experiment_safe
)


def run_experiment(
    strategy_a: str,
    strategy_b: str
):

    result_a = (
        evaluate_strategy(
            strategy_a
        )
    )

    result_b = (
        evaluate_strategy(
            strategy_b
        )
    )

    return {

        "strategy_a":
        result_a,

        "strategy_b":
        result_b
    }


def determine_winner(
    experiment
):

    score_a = (
        experiment[
            "strategy_a"
        ][
            "score"
        ]
    )

    score_b = (
        experiment[
            "strategy_b"
        ][
            "score"
        ]
    )

    if score_a >= score_b:

        return experiment[
            "strategy_a"
        ][
            "strategy"
        ]

    return experiment[
        "strategy_b"
    ][
        "strategy"
    ]


def promote_winner(
    experiment
):

    winner = (
        determine_winner(
            experiment
        )
    )

    save_strategy(
        winner
    )

    return winner


def execute_experiment(
    strategy_a: str,
    strategy_b: str
):

    # Safety check before running any experiment
    if not is_experiment_safe(
        strategy_a
    ):

        return {
            "success": False,
            "reason": f"Unsafe strategy: {strategy_a}"
        }

    if not is_experiment_safe(
        strategy_b
    ):

        return {
            "success": False,
            "reason": f"Unsafe strategy: {strategy_b}"
        }

    experiment = (
        run_experiment(
            strategy_a,
            strategy_b
        )
    )

    winner = (
        promote_winner(
            experiment
        )
    )

    return {

        "winner":
        winner,

        "experiment":
        experiment
    }