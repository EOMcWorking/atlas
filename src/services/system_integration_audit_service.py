from pathlib import Path
import ast

from src.services.workspace_service import (
    get_project_root
)

from src.services.capability_registry_service import (
    CAPABILITIES
)


def get_src_dir():

    return Path(
        get_project_root()
    ) / "src"


def get_service_dir():

    return get_src_dir() / "services"


def get_api_dir():

    return get_src_dir() / "api"


def get_all_services():

    service_dir = get_service_dir()

    if not service_dir.exists():
        return []

    return sorted(
        [
            file.name
            for file in service_dir.glob(
                "*.py"
            )
            if file.name != "__init__.py"
        ]
    )


def get_all_api_files():

    api_dir = get_api_dir()

    if not api_dir.exists():
        return []

    return sorted(
        [
            file.name
            for file in api_dir.glob(
                "*.py"
            )
            if file.name != "__init__.py"
        ]
    )

def discover_imported_services():

    imported = set()

    src_dir = get_src_dir()

    if not src_dir.exists():
        return imported

    for file in src_dir.rglob("*.py"):

        try:

            tree = ast.parse(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:

            continue

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ImportFrom
            ):

                module = node.module or ""

                if module.startswith(
                    "src.services."
                ):

                    imported.add(
                        module.split(".")[-1]
                        + ".py"
                    )

            elif isinstance(
                node,
                ast.Import
            ):

                for alias in node.names:

                    module = alias.name

                    if module.startswith(
                        "src.services."
                    ):

                        imported.add(
                            module.split(".")[-1]
                            + ".py"
                        )

    return imported

def discover_called_functions():

    called = set()

    src_dir = get_src_dir()

    if not src_dir.exists():
        return called

    for file in src_dir.rglob("*.py"):

        try:

            tree = ast.parse(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            continue

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.Call
            ):

                if isinstance(
                    node.func,
                    ast.Name
                ):

                    called.add(
                        node.func.id
                    )

                elif isinstance(
                    node.func,
                    ast.Attribute
                ):

                    called.add(
                        node.func.attr
                    )

    return called

def find_unreachable_services():

    imported = discover_imported_services()

    service_dir = get_service_dir()

    unreachable = []

    for service_file in imported:

        service_path = (
            service_dir / service_file
        )

        if not service_path.exists():
            continue

        if service_file not in imported:
            unreachable.append(
                service_file
            )

    return sorted(unreachable)

def find_unused_services():

    services = set(
        get_all_services()
    )

    imported = (
        discover_imported_services()
    )

    return sorted(
        services - imported
    )


def find_missing_service_pairs():

    missing = []

    api_dir = get_api_dir()

    for api_file in get_all_api_files():

        api_path = api_dir / api_file

        try:

            text = api_path.read_text(
                encoding="utf-8"
            )

            if not text.strip():
                continue

            tree = ast.parse(text)

        except Exception:
            continue

        wired = False

        for node in ast.walk(tree):

            if isinstance(
                node,
                ast.ImportFrom
            ):

                module = node.module or ""

                if (
                    module.startswith("src.services.")
                    or module.startswith("src.providers.")
                    or module.startswith("src.core.")
                ):
                    wired = True
                    break

            elif isinstance(
                node,
                ast.Import
            ):

                for name in node.names:

                    if (
                        name.name.startswith(
                            "src.services."
                        )
                        or name.name.startswith(
                            "src.providers."
                        )
                        or name.name.startswith(
                            "src.core."
                        )
                    ):
                        wired = True
                        break

                if wired:
                    break

        if not wired:
            missing.append(api_file)

    return sorted(missing)     

def find_orphan_apis():
    orphans = []
    api_dir = get_api_dir()

    for api_file in get_all_api_files():
        api_path = api_dir / api_file

        try:
            text = api_path.read_text(
                encoding="utf-8"
            )

            if not text.strip():
                continue

            tree = ast.parse(text)

        except Exception:
            continue

        wired = False

        for node in ast.walk(tree):

            if isinstance(node, ast.ImportFrom):

                module = node.module or ""

                if (
                    module.startswith("src.services.")
                    or module.startswith("src.providers.")
                    or module.startswith("src.core.")
                ):
                    wired = True
                    break

            elif isinstance(node, ast.Import):

                for alias in node.names:

                    module = alias.name

                    if (
                        module.startswith("src.services.")
                        or module.startswith("src.providers.")
                        or module.startswith("src.core.")
                    ):
                        wired = True
                        break

                if wired:
                    break

        if not wired:
            orphans.append(api_file)

    return sorted(orphans)

def find_duplicate_names():

    names = {}
    duplicates = []

    for service in get_all_services():

        key = service.replace(
            "_service.py",
            ""
        )

        if key in names:
            duplicates.append(service)
        else:
            names[key] = service

    return duplicates


def find_circular_dependencies_integration():

    try:

        from src.services.circular_dependency_service import (
            find_circular_dependencies
        )

        return find_circular_dependencies()

    except Exception:
        return []

def find_dead_services():

    dead = []

    service_dir = get_service_dir()

    if not service_dir.exists():
        return dead

    for service_file in get_all_services():

        path = service_dir / service_file

        try:
            tree = ast.parse(
                path.read_text(
                    encoding="utf-8"
                )
            )
        except Exception:
            continue

        has_implementation = any(
            isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef,
                    ast.ClassDef,
                )
            )
            for node in tree.body
        )

        if not has_implementation:
            dead.append(
                service_file
            )

    return sorted(dead)

def find_missing_director_paths():

    service_dir = get_service_dir()

    try:
        director_file = (
            service_dir / "director_service.py"
        )

        director_tree = ast.parse(
            director_file.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return []

    director_modes = set()

    for node in ast.walk(director_tree):

        if (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
        ):
            value = node.value

            if (
                "MODE" in value
                or "RECOVERY" in value
                or "EXECUTION" in value
            ):
                director_modes.add(value)

    try:
        scheduler_file = (
            service_dir
            / "autonomous_scheduler_service.py"
        )

        scheduler_text = (
            scheduler_file.read_text(
                encoding="utf-8"
            )
        )

    except Exception:
        return sorted(director_modes)

    missing = []

    for mode in director_modes:

        # Direct mode routing.
        if f'mode == "{mode}"' in scheduler_text:
            continue

        # Some Director modes intentionally map
        # to a work type rather than a scheduler mode.
        if mode in {
            "ROADMAP_EXECUTION",
            "HEALTH_RECOVERY",
            "NORMAL_EXECUTION",
        }:
            continue

        missing.append(mode)

    return sorted(missing)

def calculate_integration_score():
    total = len(get_all_services())

    if total == 0:
        return 0

    unused = len(find_unused_services())
    unreachable = len(find_unreachable_services())
    dead = len(find_dead_services())
    orphans = len(find_orphan_apis())
    missing_pairs = len(find_missing_service_pairs())
    circular = len(find_circular_dependencies_integration())
    missing_director = len(find_missing_director_paths())

    service_health = max(
        0,
        100 - (
            (dead / total) * 100
        )
    )

    architecture_penalty = (
        unreachable * 2
        + orphans * 2
        + missing_pairs
        + circular * 5
        + missing_director * 2
    )

    score = service_health - architecture_penalty

    return round(
        max(0, min(100, score)),
        2
    )

def get_system_integration_report():

    return {
        "integration_score":
        calculate_integration_score(),

        "total_services":
        len(get_all_services()),

        "unused_services":
        find_unused_services(),

        "unreachable_services":
        find_unreachable_services(),

        "dead_services":
        find_dead_services(),

        "duplicate_services":
        find_duplicate_names(),

        "apis_missing_services":
        find_missing_service_pairs(),

        "orphan_apis":
        find_orphan_apis(),

        "circular_dependencies":
        find_circular_dependencies_integration(),

        "missing_director_paths":
        find_missing_director_paths()
    }

