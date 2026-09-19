from src.services.system_integration_audit_service import (
    get_system_integration_report
)

from src.services.ollama_service import (
    chat
)

def collect_integration_issues():

    report = (
        get_system_integration_report()
    )

    issues = []

    for service in report["unused_services"]:

        issues.append(
            f"Unused service: {service}"
        )

    for api in report["apis_missing_services"]:

        issues.append(
            f"API missing service: {api}"
        )

    for duplicate in report["duplicate_services"]:

        issues.append(
            f"Duplicate service: {duplicate}"
        )

    return issues

def generate_repair_plan():

    issues = (
        collect_integration_issues()
    )

    if not issues:

        return {

            "success": True,

            "message":
            "No integration issues found."
        }

    prompt = f"""
You are Atlas Integration Repair Planner.

Detected Issues:

{issues}

Generate:

1. Safe repair actions

2. Recommended order

3. Risk level

Do NOT generate code.

Only produce a repair plan.
"""

    plan = chat(
        prompt,
        task_type="planning"
    )

    return {

        "success": True,

        "issues": issues,

        "repair_plan": plan
    }

def extract_repair_actions():

    result = (
        generate_repair_plan()
    )

    if not result["success"]:

        return []

    actions = []

    for line in result[
        "repair_plan"
    ].splitlines():

        text = line.strip()

        if len(text) > 5:

            actions.append(
                text
            )

    return actions

def get_integration_repair_report():

    return {

        "audit":

        get_system_integration_report(),

        "repair":

        generate_repair_plan()
    }
