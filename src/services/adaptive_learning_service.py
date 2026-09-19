from collections import defaultdict

from src.services.change_history_service import (
    load_history
)


def build_learning_profile():

    history = load_history()

    file_stats = defaultdict(
        lambda: {
            "success": 0,
            "failure": 0
        }
    )

    for change in history:

        successful = change.get(
            "success",
            False
        )

        for file in change.get(
            "files",
            []
        ):

            if successful:

                file_stats[file][
                    "success"
                ] += 1

            else:

                file_stats[file][
                    "failure"
                ] += 1

    return dict(
        file_stats
    )

def get_file_confidence(
    file_path: str
):

    profile = (
        build_learning_profile()
    )

    stats = profile.get(
        file_path
    )

    if not stats:

        return 50

    success = stats[
        "success"
    ]

    failure = stats[
        "failure"
    ]

    total = (
        success
        + failure
    )

    if total == 0:
        return 50

    return int(
        (success / total)
        * 100
    )

def adjust_risk_level(
    file_path: str,
    current_risk: str
):

    confidence = (
        get_file_confidence(
            file_path
        )
    )

    if (
        confidence >= 90
        and current_risk == "MEDIUM"
    ):
        return "LOW"

    if (
        confidence <= 30
        and current_risk == "LOW"
    ):
        return "MEDIUM"

    return current_risk

def get_problem_files():

    profile = (
        build_learning_profile()
    )

    results = []

    for file, stats in profile.items():

        failures = stats[
            "failure"
        ]

        if failures >= 3:

            results.append(
                (
                    failures,
                    file
                )
            )

    results.sort(
        reverse=True
    )

    return results

def get_safe_files():

    profile = (
        build_learning_profile()
    )

    results = []

    for file, stats in profile.items():

        success = stats[
            "success"
        ]

        failure = stats[
            "failure"
        ]

        if (
            success >= 5
            and failure == 0
        ):

            results.append(
                file
            )

    return results

