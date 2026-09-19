import json
from pathlib import Path


ATLAS_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKSPACE_CONFIG = ATLAS_ROOT / "config" / "workspace.json"


def find_project_workspace(start_directory=None):
    """
    Search the current directory and its parents for:
    .atlas/config/workspace.json
    """
    current = Path(
        start_directory or Path.cwd()
    ).resolve()

    for directory in [current, *current.parents]:
        candidate = (
            directory
            / ".atlas"
            / "config"
            / "workspace.json"
        )

        if candidate.exists():
            return candidate

    return None


def get_workspace_config_path():
    """
    Return the project workspace config if available.
    Otherwise fall back to Atlas's own workspace config.
    """
    project_config = find_project_workspace()

    if project_config:
        return project_config

    return DEFAULT_WORKSPACE_CONFIG


def load_workspace():
    """
    Load the active workspace configuration.
    """
    workspace_config = get_workspace_config_path()

    if not workspace_config.exists():
        raise FileNotFoundError(
            f"Workspace configuration not found: "
            f"{workspace_config}"
        )

    with workspace_config.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def _resolve(value):
    """
    Resolve a configured filesystem path.
    """
    if not value:
        return None

    return str(Path(value).resolve())


def get_project_root():
    workspace = load_workspace()
    return _resolve(
        workspace["project"]["root"]
    )


def get_project_name():
    workspace = load_workspace()
    return workspace["project"]["name"]


def get_atlas_root():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["root"]
    )


def get_docs_path():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["docs"]
    )


def get_memory_path():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["memory"]
    )


def get_logs_path():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["logs"]
    )


def get_snapshots_path():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["snapshots"]
    )


def get_cache_path():
    workspace = load_workspace()
    return _resolve(
        workspace["atlas"]["cache"]
    )


def get_atlas_path(name):
    """
    Return a named Atlas path.
    """
    paths = {
        "root": get_atlas_root(),
        "docs": get_docs_path(),
        "memory": get_memory_path(),
        "logs": get_logs_path(),
        "snapshots": get_snapshots_path(),
        "cache": get_cache_path(),
    }

    if name not in paths:
        raise ValueError(
            f"Unknown Atlas path: {name}"
        )

    return paths[name]


def get_workspace():
    workspace = load_workspace()

    return {
        "project": {
            "name": get_project_name(),
            "root": get_project_root(),
        },
        "atlas": {
            "root": get_atlas_root(),
            "docs": get_docs_path(),
            "memory": get_memory_path(),
            "logs": get_logs_path(),
            "snapshots": get_snapshots_path(),
            "cache": get_cache_path(),
        },
    }