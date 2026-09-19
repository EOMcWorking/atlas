def determine_execution_policy(
    simulation
):

    risk = simulation[
        "highest_risk"
    ]

    if risk == "LOW":

        return {
            "policy": "AUTO_EXECUTE",
            "approval_required": False
        }

    if risk == "MEDIUM":

        return {
            "policy": "AUTO_EXECUTE_WITH_REVIEW",
            "approval_required": False
        }

    if risk == "HIGH":

        return {
            "policy": "REQUIRE_APPROVAL",
            "approval_required": True
        }

    if risk == "CRITICAL":

        return {
            "policy": "ARCHITECTURE_REVIEW_REQUIRED",
            "approval_required": True
        }

    return {
        "policy": "UNKNOWN",
        "approval_required": True
    }

def can_execute(
    policy
):

    return (
        not policy[
            "approval_required"
        ]
    )