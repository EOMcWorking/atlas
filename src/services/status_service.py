from pathlib import Path

from src.core.config import (
    PROVIDER_FALLBACKS
)


from pathlib import Path

from src.core.config import PROVIDER_FALLBACKS


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
    return {
        "project": "Atlas",
        "version": "0.6-dev",

        "handoff_exists":
            Path("HANDOFF.md").exists(),

        "snapshot_exists":
            Path("atlas_snapshot.json").exists(),

        "roadmap_exists":
            Path("ROADMAP.md").exists(),

        "tasks_exists":
            Path("TASKS.md").exists(),

        "decisions_exists":
            Path("DECISIONS.md").exists(),

        "task_count":
            count_lines("TASKS.md"),

        "decision_count":
            count_lines("DECISIONS.md"),

        "fallback_count":
            len(PROVIDER_FALLBACKS),

        "providers":
            PROVIDER_FALLBACKS,
    }
    