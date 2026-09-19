from pathlib import Path
import json
from datetime import datetime

from src.services.project_service import (
    get_project_state
)

from src.services.project_paths_service import (
    get_project_file
)


def generate_snapshot(
    project_name: str = None
):

    if project_name is None:

        snapshot = {
            "timestamp": (
                datetime.now()
                .isoformat()
            ),
            "project": Path(
                "PROJECT.md"
            ).read_text(
                encoding="utf-8"
            ),
            "tasks": Path(
                "TASKS.md"
            ).read_text(
                encoding="utf-8"
            ),
            "decisions": Path(
                "DECISIONS.md"
            ).read_text(
                encoding="utf-8"
            ),
            "handoff": Path(
                "HANDOFF.md"
            ).read_text(
                encoding="utf-8"
            ),
        }

    else:

        snapshot = (
            get_project_state(
                project_name
            )
        )

        snapshot[
            "timestamp"
        ] = (
            datetime.now()
            .isoformat()
        )

    snapshot_file = (
        "atlas_snapshot.json"
        if project_name is None
        else f"{project_name}_snapshot.json"
    )

    with open(
        snapshot_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            snapshot,
            f,
            indent=2,
            ensure_ascii=False
        )

    return snapshot