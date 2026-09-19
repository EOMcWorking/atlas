from pathlib import Path
import ast

from src.services.workspace_service import (
    get_project_root
)


def build_dependency_graph():

    graph = {}

    project_root = Path(
        get_project_root()
    )

    if not project_root.exists():
        return graph

    for file in project_root.rglob(
        "*.py"
    ):

        if any(
            part in {
                ".git",
                ".venv",
                "venv",
                "env",
                "node_modules",
                "__pycache__",
                ".pytest_cache",
                ".mypy_cache",
                ".ruff_cache",
                ".idea",
                ".vscode",
                "cache",
                "logs",
                "snapshots",
                "atlas_data"
            }
            for part in file.parts
        ):
            continue

        file_key = str(file)

        graph[file_key] = []

        try:

            content = file.read_text(
                encoding="utf-8"
            )

            tree = ast.parse(
                content
            )

            for node in ast.walk(tree):

                if isinstance(
                    node,
                    ast.Import
                ):

                    for name in node.names:

                        graph[
                            file_key
                        ].append(
                            name.name
                        )

                elif isinstance(
                    node,
                    ast.ImportFrom
                ):

                    if node.module:

                        graph[
                            file_key
                        ].append(
                            node.module
                        )

        except Exception:
            pass

    return graph


def get_dependencies(
    file_path: str
):

    graph = build_dependency_graph()

    return graph.get(
        file_path,
        []
    )


def get_dependents(
    file_path: str
):

    graph = build_dependency_graph()

    dependents = []

    target = (
        file_path
        .replace("/", ".")
        .replace("\\", ".")
        .replace(".py", "")
    )

    for source, imports in graph.items():

        for imported in imports:

            if target.endswith(
                imported
            ):

                dependents.append(
                    source
                )

    return dependents