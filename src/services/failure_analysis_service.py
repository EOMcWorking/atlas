from collections import Counter

from src.services.change_history_service import (
    load_history
)

from src.services.self_improvement_board_service import (
    add_improvement
)


def analyze_failures():

    history = load_history()

    failures = [

        item

        for item in history

        if not item.get(
            "success",
            False
        )
    ]

    file_counter = Counter()

    risk_counter = Counter()

    policy_counter = Counter()

    for failure in failures:

        for file in failure.get(
            "files",
            []
        ):

            file_counter[
                file
            ] += 1

        risk_counter[
            failure.get(
                "risk",
                "UNKNOWN"
            )
        ] += 1

        policy_counter[
            failure.get(
                "policy",
                "UNKNOWN"
            )
        ] += 1

    analysis = {

        "total_failures":
        len(failures),

        "top_problem_files":
        file_counter.most_common(10),

        "top_problem_risks":
        risk_counter.most_common(),

        "top_problem_policies":
        policy_counter.most_common()
    }

    # When failure patterns appear, log them to the improvement board
    _detect_and_log_failure_patterns(
        analysis,
        failures
    )

    return analysis


def _detect_and_log_failure_patterns(analysis, failures):
    """
    Detect recurring failure patterns and log them as improvements.
    """
    total = analysis["total_failures"]

    # Threshold: only flag if there are at least 2 failures
    if total < 2:
        return

    # 1. Flag problem files that failed more than once
    for file_path, count in analysis["top_problem_files"]:
        if count >= 2:
            add_improvement(
                title=f"Fix recurring failures in {file_path}",
                reason=f"File failed {count}/{total} times in change history",
                priority=min(count + 3, 10)
            )

    # 2. Flag problematic risk levels
    for risk, count in analysis["top_problem_risks"]:
        if count >= 2 and risk != "UNKNOWN":
            add_improvement(
                title=f"Improve handling of {risk} risk changes",
                reason=f"{risk} risk level failed {count}/{total} times",
                priority=min(count + 3, 10)
            )

    # 3. Flag problematic policies
    for policy, count in analysis["top_problem_policies"]:
        if count >= 2 and policy != "UNKNOWN":
            add_improvement(
                title=f"Review {policy} policy effectiveness",
                reason=f"{policy} policy had {count}/{total} failures",
                priority=min(count + 3, 10)
            )

    # 4. Flag same-task repeated failures
    task_counter = Counter()
    for failure in failures:
        task = failure.get("task", "")
        if task:
            task_counter[task] += 1

    for task, count in task_counter.most_common():
        if count >= 3:
            add_improvement(
                title=f"Break down or re-approach: {task[:80]}",
                reason=f"Same task failed {count} times consecutively",
                priority=9
            )


def most_problematic_file():

    analysis = analyze_failures()

    files = analysis[
        "top_problem_files"
    ]

    if not files:
        return None

    return files[0][0]


def most_problematic_risk():

    analysis = analyze_failures()

    risks = analysis[
        "top_problem_risks"
    ]

    if not risks:
        return None

    return risks[0][0]


def failure_summary():

    analysis = analyze_failures()

    return f"""
Failures:
{analysis['total_failures']}

Worst File:
{most_problematic_file()}

Worst Risk:
{most_problematic_risk()}
"""