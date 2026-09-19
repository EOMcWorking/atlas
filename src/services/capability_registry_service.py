CAPABILITIES = {

    "planning": [
        "planner_agent",
        "task_generation_service"
    ],

    "editing": [
        "smart_edit_service",
        "multi_file_patch_service"
    ],

    "review": [
        "reviewer_agent",
        "diff_reviewer_agent"
    ],

    "rollback": [
        "rollback_service",
        "auto_rollback_service"
    ],

    "learning": [
        "adaptive_learning_service",
        "root_cause_analysis_service"
    ],

    "health": [
        "project_health_service",
        "technical_debt_service"
    ],

    "graph_analysis": [
        "dependency_graph_service",
        "project_graph_service",
        "impact_analysis_service"
    ]
}

def get_capabilities():

    return CAPABILITIES

def find_capability(
    capability_name: str
):

    return CAPABILITIES.get(
        capability_name,
        []
    )

def find_service_capabilities(
    service_name: str
):

    results = []

    for capability, services in (
        CAPABILITIES.items()
    ):

        if service_name in services:

            results.append(
                capability
            )

    return results

def find_missing_capabilities():

    expected = [

        "planning",
        "editing",
        "review",
        "learning",
        "health",
        "graph_analysis",
        "testing",
        "deployment",
        "monitoring"
    ]

    missing = []

    for capability in expected:

        if capability not in CAPABILITIES:

            missing.append(
                capability
            )

    return missing