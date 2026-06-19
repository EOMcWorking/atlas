from src.services.dependency_service import (
    build_dependency_graph
)


def find_dead_code():

    graph = build_dependency_graph()

    imported_modules = set()

    for imports in graph.values():

        for module in imports:
            imported_modules.add(
                module
            )

    dead_files = []

    for file in graph.keys():

        module_name = (
            file.replace("\\", ".")
            .replace("/", ".")
            .replace(".py", "")
        )

        if module_name not in imported_modules:

            if (
                "__init__" not in file
                and "main.py" not in file
            ):
                dead_files.append(
                    file
                )

    return {
        "dead_code_candidates": dead_files
    }