from pathlib import Path
import json

GOAL_FILE = Path(
    "autonomous_goals.json"
)

def load_goals():

    if not GOAL_FILE.exists():

        return []

    return json.loads(
        GOAL_FILE.read_text(
            encoding="utf-8"
        )
    )

def save_goals(
    goals
):

    GOAL_FILE.write_text(
        json.dumps(
            goals,
            indent=2
        ),
        encoding="utf-8"
    )

def add_goal(
    title: str,
    priority: int = 5
):

    goals = load_goals()

    goals.append({

        "title":
        title,

        "priority":
        priority,

        "progress":
        0,

        "status":
        "ACTIVE"
    })

    save_goals(
        goals
    )

def get_active_goals():

    return [

        goal

        for goal in load_goals()

        if goal[
            "status"
        ] == "ACTIVE"
    ]

def get_primary_goal():

    goals = (
        get_active_goals()
    )

    if not goals:

        return None

    goals.sort(

        key=lambda g:
        g["priority"],

        reverse=True
    )

    return goals[0]

def update_goal_progress(
    title,
    progress
):

    goals = load_goals()

    for goal in goals:

        if goal[
            "title"
        ] == title:

            goal[
                "progress"
            ] = progress

            if progress >= 100:

                goal[
                    "status"
                ] = "COMPLETED"

    save_goals(
        goals
    )

def get_goal_report():

    return {

        "primary":
        get_primary_goal(),

        "active":
        get_active_goals()
    }