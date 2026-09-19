from pathlib import Path

from src.services.project_paths_service import (
    get_project_file
)

DECISIONS_FILE = Path(
    "DECISIONS.md"
)


def get_decisions_file(
    project_name: str = None
):

    if project_name is None:
        return DECISIONS_FILE

    return Path(
        get_project_file(
            project_name,
            "DECISIONS.md"
        )
    )


def read_decisions(
    project_name: str = None
):

    decisions_file = (
        get_decisions_file(
            project_name
        )
    )

    if not decisions_file.exists():
        return ""

    return decisions_file.read_text(
        encoding="utf-8"
    )


def add_decision(
    decision: str,
    project_name: str = None
):

    decisions_file = (
        get_decisions_file(
            project_name
        )
    )

    with open(
        decisions_file,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n{decision}\n"
        )


def search_decisions(
    query: str,
    project_name: str = None
):

    content = read_decisions(
        project_name
    )

    matches = []

    for line in content.splitlines():

        if query.lower() in (
            line.lower()
        ):
            matches.append(
                line
            )

    return matches