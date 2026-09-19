from src.services.change_plan_parser_service import (
    extract_plan_files
)

from src.services.impact_analysis_service import (
    analyze_impact
)


def simulate_change(
    task: str,
    change_plan: str
):

    files = extract_plan_files(
        change_plan
    )

    analysis = []

    highest_risk = "LOW"

    risk_order = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    for file in files:

        result = analyze_impact(
            file
        )

        analysis.append(
            result
        )

        if (
            risk_order[
                result["impact_level"]
            ]
            >
            risk_order[
                highest_risk
            ]
        ):
            highest_risk = (
                result[
                    "impact_level"
                ]
            )

    return {
        "task": task,
        "files": files,
        "highest_risk": highest_risk,
        "analysis": analysis
    }

def requires_manual_review(
    simulation
):

    return (
        simulation[
            "highest_risk"
        ]
        in [
            "HIGH",
            "CRITICAL"
        ]
    )