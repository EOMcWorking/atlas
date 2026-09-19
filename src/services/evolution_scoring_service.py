from src.services.autonomous_benchmark_service import (
    compare_benchmarks
)

def calculate_evolution_score():

    comparison = (
        compare_benchmarks()
    )

    if not comparison:

        return 0

    previous = (
        comparison[
            "previous"
        ]
    )

    current = (
        comparison[
            "current"
        ]
    )

    score = 0

    old_success = previous.get(
        "success_rate",
        0
    )

    new_success = current.get(
        "success_rate",
        0
    )

    score += (
        new_success
        -
        old_success
    )

    old_runtime = previous.get(
        "average_runtime",
        0
    )

    new_runtime = current.get(
        "average_runtime",
        0
    )

    score += (
        old_runtime
        -
        new_runtime
    )

    return round(
        score,
        2
    )

def grade_evolution():

    score = (
        calculate_evolution_score()
    )

    if score > 10:

        return "EXCELLENT"

    if score > 5:

        return "GOOD"

    if score > 0:

        return "MINOR"

    if score == 0:

        return "NEUTRAL"

    return "NEGATIVE"

def get_evolution_report():

    score = (
        calculate_evolution_score()
    )

    return {

        "score":
        score,

        "grade":
        grade_evolution()
    }
