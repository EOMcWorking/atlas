from pathlib import Path

from src.core.config import PROVIDER_FALLBACKS
from src.services.workspace_service import (
    get_atlas_path,
    get_docs_path,
    get_project_name,
)


def count_lines(filepath: str):
    path = Path(filepath)

    if not path.exists():
        return 0

    return len(
        path.read_text(
            encoding="utf-8"
        ).splitlines()
    )


def get_atlas_status():
    docs_path = Path(get_docs_path())

    handoff = docs_path / "HANDOFF.md"
    snapshot = Path(
        get_atlas_path("snapshots")
    ) / "atlas_snapshot.json"
    roadmap = docs_path / "ROADMAP.md"
    tasks = docs_path / "TASKS.md"
    decisions = docs_path / "DECISIONS.md"

    return {
        "project": get_project_name(),
        "version": "0.6-dev",

        "handoff_exists":
            handoff.exists(),

        "snapshot_exists":
            snapshot.exists(),

        "roadmap_exists":
            roadmap.exists(),

        "tasks_exists":
            tasks.exists(),

        "decisions_exists":
            decisions.exists(),

        "task_count":
            count_lines(str(tasks)),

        "decision_count":
            count_lines(str(decisions)),

        "fallback_count":
            len(PROVIDER_FALLBACKS),

        "providers":
            PROVIDER_FALLBACKS,
    }