from pathlib import Path
import json


MILESTONES_FILE = Path(
    "MILESTONES.json"
)

def load_milestones():

    if not MILESTONES_FILE.exists():

        return []

    return json.loads(
        MILESTONES_FILE.read_text(
            encoding="utf-8"
        )
    )

def save_milestones(
    milestones
):

    MILESTONES_FILE.write_text(
        json.dumps(
            milestones,
            indent=2
        ),
        encoding="utf-8"
    )

def add_milestone(
    goal: str,
    milestone: str
):

    milestones = (
        load_milestones()
    )

    milestones.append({

        "goal": goal,

        "milestone": milestone,

        "completed": False,

        "progress": 0
    })

    save_milestones(
        milestones
    )

def update_milestone_progress(
    milestone_name: str,
    progress: int
):

    milestones = (
        load_milestones()
    )

    for milestone in milestones:

        if (
            milestone[
                "milestone"
            ]
            == milestone_name
        ):

            milestone[
                "progress"
            ] = progress

            if progress >= 100:

                milestone[
                    "completed"
                ] = True

    save_milestones(
        milestones
    )

def get_active_milestones():

    return [

        milestone

        for milestone

        in load_milestones()

        if not milestone[
            "completed"
        ]
    ]

def get_current_milestone():

    active = (
        get_active_milestones()
    )

    if not active:

        return None

    return active[0]