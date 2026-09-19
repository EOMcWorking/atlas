from pathlib import Path

from src.services.workspace_service import (
    get_docs_path,
)


def system_health():

    docs_path = Path(
        get_docs_path()
    )

    checks = {
        "project_md": (
            docs_path / "PROJECT.md"
        ).exists(),

        "tasks_md": (
            docs_path / "TASKS.md"
        ).exists(),

        "decisions_md": (
            docs_path / "DECISIONS.md"
        ).exists(),

        "handoff_md": (
            docs_path / "HANDOFF.md"
        ).exists(),

        "memory_md": (
            docs_path / "MEMORY.md"
        ).exists(),

        "atlas_db": Path(
            "atlas.db"
        ).exists()
    }

    healthy = all(
        checks.values()
    )

    return {
        "healthy": healthy,
        "checks": checks
    }