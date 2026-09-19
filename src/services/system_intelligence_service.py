from src.services.project_health_service import (
    health_summary
)

from src.services.workflow_optimizer_service import (
    analyze_workflows
)

from src.services.failure_analysis_service import (
    analyze_failures
)

def generate_intelligence_report():

    health = (
        health_summary()
    )

    workflows = (
        analyze_workflows()
    )

    failures = (
        analyze_failures()
    )

    return {

        "health":
        health,

        "workflows":
        workflows,

        "failures":
        failures
    }

def calculate_intelligence_score():

    report = (
        generate_intelligence_report()
    )

    score = 100

    failure_count = len(
        report[
            "failures"
        ]
    )

    score -= (
        failure_count * 2
    )

    health_score = (
        report[
            "health"
        ].get(
            "score",
            100
        )
    )

    score = (
        score + health_score
    ) / 2

    return max(
        int(score),
        0
    )

def identify_weakest_area():

    report = (
        generate_intelligence_report()
    )

    failures = len(
        report[
            "failures"
        ]
    )

    if failures > 20:

        return "FAILURE_HANDLING"

    health = (
        report[
            "health"
        ].get(
            "score",
            100
        )
    )

    if health < 70:

        return "TECHNICAL_DEBT"

    return "STABLE"

def get_system_intelligence():

    return {

        "score":
        calculate_intelligence_score(),

        "weakest_area":
        identify_weakest_area(),

        "report":
        generate_intelligence_report()
    }

