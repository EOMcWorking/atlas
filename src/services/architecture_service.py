from src.services.dependency_service import (
    build_dependency_graph
)


def analyze_architecture():

    graph = build_dependency_graph()

    result = {
        "most_connected": [],
        "isolated": []
    }

    connections = []

    for file, imports in graph.items():

        connections.append(
            (
                len(imports),
                file
            )
        )

        if len(imports) == 0:
            result[
                "isolated"
            ].append(file)

    connections.sort(
        reverse=True
    )

    result[
        "most_connected"
    ] = connections[:10]

    return result