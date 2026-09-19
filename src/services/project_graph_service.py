from collections import defaultdict

from src.services.dependency_graph_service import (
    build_dependency_graph
)

from src.services.change_history_service import (
    load_history
)

from src.services.adaptive_learning_service import (
    get_file_confidence
)


def build_project_graph():

    dependency_graph = (
        build_dependency_graph()
    )

    history = load_history()

    graph = defaultdict(
        lambda: {
            "dependencies": [],
            "changes": 0,
            "confidence": 50
        }
    )

    for file, deps in (
        dependency_graph.items()
    ):

        graph[file][
            "dependencies"
        ] = deps

        graph[file][
            "confidence"
        ] = get_file_confidence(
            file
        )

    for change in history:

        for file in change.get(
            "files",
            []
        ):

            graph[file][
                "changes"
            ] += 1

    return dict(graph)

def get_impacted_files(
    target_file: str,
    depth: int = 2
):

    graph = (
        build_project_graph()
    )

    visited = set()

    queue = [
        (
            target_file,
            0
        )
    ]

    impacted = []

    while queue:

        current, level = (
            queue.pop(0)
        )

        if current in visited:
            continue

        visited.add(
            current
        )

        impacted.append(
            current
        )

        if level >= depth:
            continue

        for dependency in graph.get(
            current,
            {}
        ).get(
            "dependencies",
            []
        ):

            queue.append(
                (
                    dependency,
                    level + 1
                )
            )

    return impacted

def get_high_risk_files():

    graph = (
        build_project_graph()
    )

    results = []

    for file, data in (
        graph.items()
    ):

        score = (
            len(
                data[
                    "dependencies"
                ]
            ) * 5
            +
            data[
                "changes"
            ]
        )

        if (
            data[
                "confidence"
            ] < 50
        ):
            score += 20

        results.append(
            (
                score,
                file
            )
        )

    results.sort(
        reverse=True
    )

    return results[:20]

def get_safe_files():

    graph = (
        build_project_graph()
    )

    safe = []

    for file, data in (
        graph.items()
    ):

        if (
            data[
                "confidence"
            ] >= 90
            and
            len(
                data[
                    "dependencies"
                ]
            ) <= 2
        ):

            safe.append(
                file
            )

    return safe