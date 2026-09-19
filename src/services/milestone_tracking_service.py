import json
from pathlib import Path

from src.services.workspace_service import get_memory_path


def get_milestone_file():
    """
    Return the milestone file inside the configured
    Atlas memory directory.
    """
    memory_path = Path(get_memory_path())
    memory_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return memory_path / "milestones.json"


def load_milestones():

    milestone_file = get_milestone_file()

    if not milestone_file.exists():

        return []

    try:
        data = json.loads(
            milestone_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError):
        return []


def save_milestones(milestones):

    milestone_file = get_milestone_file()

    milestone_file.write_text(
        json.dumps(
            milestones,
            indent=2
        ),
        encoding="utf-8"
    )


def add_milestone(title):

    milestones = load_milestones()

    milestones.append({
        "title": title,
        "status": "ACTIVE"
    })

    save_milestones(milestones)


def get_active_milestone():

    milestones = load_milestones()

    for milestone in milestones:

        if milestone.get("status") == "ACTIVE":
            return milestone

    return None


def complete_milestone(title):

    milestones = load_milestones()

    for milestone in milestones:

        if milestone.get("title") == title:
            milestone["status"] = "COMPLETED"

    save_milestones(milestones)


def get_milestone_report():

    milestones = load_milestones()

    completed = len([
        milestone
        for milestone in milestones
        if milestone.get("status") == "COMPLETED"
    ])

    total = len(milestones)

    progress = 0

    if total:
        progress = int(
            completed * 100 / total
        )

    return {
        "active": get_active_milestone(),
        "completed": completed,
        "total": total,
        "progress": progress
    }