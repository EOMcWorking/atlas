from src.services.project_graph_service import (
    get_impacted_files
)

from src.services.project_graph_service import (
    get_high_risk_files
)


def analyze_impact(
    target_file: str
):

    impacted = (
        get_impacted_files(
            target_file
        )
    )

    high_risk = {

        file

        for score, file

        in get_high_risk_files()
    }

    risk_score = 0

    for file in impacted:

        if file in high_risk:

            risk_score += 10

        else:

            risk_score += 2

    if risk_score >= 50:

        risk = "HIGH"

    elif risk_score >= 20:

        risk = "MEDIUM"

    else:

        risk = "LOW"

    return {

        "target_file":
        target_file,

        "risk":
        risk,

        "risk_score":
        risk_score,

        "impacted_files":
        impacted,

        "impact_count":
        len(
            impacted
        )
    }

def requires_approval(
    impact_result
):

    return (
        impact_result[
            "risk"
        ]
        == "HIGH"
    )

def impact_summary(
    target_file: str
):

    result = analyze_impact(
        target_file
    )

    return f"""
Target:
{result['target_file']}

Risk:
{result['risk']}

Impacted Files:
{result['impact_count']}
"""