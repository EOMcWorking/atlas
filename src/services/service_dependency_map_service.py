from pathlib import Path
import re


IMPORT_PATTERN = re.compile(
    r"from\s+([a-zA-Z0-9_.]+)\s+import"
)


def build_service_map():

    graph = {}

    for file in Path(
        "src"
    ).rglob("*.py"):

        try:

            content = file.read_text(
                encoding="utf-8"
            )

        except Exception:

            continue

        imports = []

        for match in IMPORT_PATTERN.findall(
            content
        ):

            if (
                "src.services"
                in match
            ):

                imports.append(
                    match
                )

        graph[
            str(file)
        ] = imports

    return graph

def get_core_services():

    graph = (
        build_service_map()
    )

    counts = {}

    for imports in graph.values():

        for service in imports:

            counts[
                service
            ] = (
                counts.get(
                    service,
                    0
                )
                + 1
            )

    return sorted(
        counts.items(),
        key=lambda x: x[1],
        reverse=True
    )

def get_orphan_services():

    graph = (
        build_service_map()
    )

    used = set()

    for imports in graph.values():

        used.update(
            imports
        )

    orphans = []

    for file in graph:

        if (
            "services"
            not in file
        ):
            continue

        module = (
            file
            .replace(
                "\\",
                "."
            )
            .replace(
                "/",
                "."
            )
            .replace(
                ".py",
                ""
            )
        )

        if module not in used:

            orphans.append(
                file
            )

    return orphans