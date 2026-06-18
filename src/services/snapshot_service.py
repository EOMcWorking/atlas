from pathlib import Path
import json
from datetime import datetime

from src.services.project_service import get_project_state

snapshot = get_project_state()
snapshot["timestamp"] = datetime.now().isoformat()

def generate_snapshot():
    snapshot = {
        "timestamp": datetime.now().isoformat(),
        "project": Path("PROJECT.md").read_text(encoding="utf-8"),
        "tasks": Path("TASKS.md").read_text(encoding="utf-8"),
        "decisions": Path("DECISIONS.md").read_text(encoding="utf-8"),
        "handoff": Path("HANDOFF.md").read_text(encoding="utf-8"),
    }

    with open(
        "atlas_snapshot.json",
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