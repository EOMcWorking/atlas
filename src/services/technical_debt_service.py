from src.services.rule_inspector_service import (
    inspect_architecture
)


def calculate_technical_debt():

    inspection = (
        inspect_architecture()
    )

    score = 100

    score -= (
        len(
            inspection.get(
                "dead_code",
                []
            )
        ) * 5
    )

    score -= (
        len(
            inspection.get(
                "cycles",
                []
            )
        ) * 15
    )

    score -= (
        len(
            inspection.get(
                "large_files",
                []
            )
        ) * 5
    )

    score -= (
        len(
            inspection.get(
                "weaknesses",
                []
            )
        ) * 3
    )

    score = max(
        score,
        0
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
        "score": score,
        "health": health,
        "strengths": len(
            inspection.get(
                "strengths",
                []
            )
        ),
        "weaknesses": len(
            inspection.get(
                "weaknesses",
                []
            )
        ),
        "priorities": inspection.get(
            "priorities",
            []
        )
    }