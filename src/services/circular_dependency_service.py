from src.services.dependency_service import (
    build_dependency_graph
)


def find_circular_dependencies():

    graph = (
        build_dependency_graph()
    )

    cycles = []

    for node in graph:

        visited = set()

        _dfs(
            graph,
            node,
            node,
            visited,
            [],
            cycles
        )

    return {
        "cycles": cycles
    }


def _dfs(
    graph,
    start,
    current,
    visited,
    path,
    cycles
):

    visited.add(current)

    path.append(current)

    for neighbor in graph.get(
        current,
        []
    ):

        if neighbor == start and len(path) > 1:

            cycle = path + [start]

            if cycle not in cycles:
                cycles.append(
                    cycle
                )

        elif neighbor not in visited:

            _dfs(
                graph,
                start,
                neighbor,
                visited.copy(),
                path.copy(),
                cycles
            )