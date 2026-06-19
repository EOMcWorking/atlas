from pathlib import Path
import re

from src.services.project_context_service import (
    get_project_files
)


IMPORT_PATTERN = re.compile(
    r"^\s*(?:from|import)\s+([a-zA-Z0-9_\.]+)",
    re.MULTILINE
)


def build_dependency_graph():

    graph = {}

    for file in get_project_files():

        if file.suffix != ".py":
            continue

        try:
            content = file.read_text(
                encoding="utf-8"
            )

            imports = (
                IMPORT_PATTERN.findall(
                    content
                )
            )

            graph[
                str(file)
            ] = imports

        except Exception:
            continue

    return graph