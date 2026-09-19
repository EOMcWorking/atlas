from src.services.impact_analysis_service import (
    analyze_impact
)


PROTECTED_FILES = [

    "src/main.py",

    "src/services/agent_orchestrator.py",

    "src/services/autonomous_scheduler_service.py",

    "src/services/approval_service.py",

    "src/services/commit_workflow_service.py",
]


def check_architecture_guard(
    file_path: str
):

    impact = analyze_impact(
        file_path
    )

    if file_path in PROTECTED_FILES:

        return {
            "allowed": False,
            "reason": "Protected file",
            "impact": impact
        }

    if (
        impact["impact_level"]
        == "CRITICAL"
    ):

        return {
            "allowed": False,
            "reason": "Critical impact",
            "impact": impact
        }

    return {
        "allowed": True,
        "impact": impact
    }

def is_protected(
    file_path: str
):

    return (
        file_path
        in PROTECTED_FILES
    )