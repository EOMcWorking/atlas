from src.services.technical_debt_service import (
    calculate_technical_debt
)

from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.change_history_service import (
    load_history
)


def calculate_project_health():

    debt = calculate_technical_debt()

    failures = analyze_failures()

    history = load_history()

    total_changes = len(
        history
    )

    total_failures = failures[
        "total_failures"
    ]

    if total_changes == 0:

        failure_rate = 0

    else:

        failure_rate = (
            total_failures
            / total_changes
        ) * 100

    score = debt[
        "score"
    ]

    score -= int(
        failure_rate
    )

    score = max(
        0,
        min(score, 100)
    )

    if score >= 90:
        health = "Excellent"

    elif score >= 75:
        health = "Good"

    elif score >= 60:
        health = "Fair"

    elif score >= 40:
        health = "Poor"

    else:
        health = "Critical"

    return {

        "health": health,

        "score": score,

        "technical_debt":
        debt["score"],

        "failure_rate":
        round(
            failure_rate,
            2
        ),

        "total_changes":
        total_changes,

        "total_failures":
        total_failures
    }

def health_summary():

    health = (
        calculate_project_health()
    )

    return f"""
Health: {health['health']}

Score: {health['score']}

Technical Debt:
{health['technical_debt']}

Failure Rate:
{health['failure_rate']}%

Changes:
{health['total_changes']}
"""