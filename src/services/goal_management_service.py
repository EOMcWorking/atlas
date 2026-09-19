from pathlib import Path
import json


GOALS_FILE = Path(
    "GOALS.json"
)

def load_goals():

    if not GOALS_FILE.exists():

        return []

    return json.loads(
        GOALS_FILE.read_text(
            encoding="utf-8"
        )
    )

def save_goals(
    goals
):

    GOALS_FILE.write_text(
        json.dumps(
            goals,
            indent=2
        ),
        encoding="utf-8"
    )

def add_goal(
    goal: str
):

    goals = load_goals()

    goals.append({

        "goal": goal,

        "progress": 0,

        "completed": False
    })

    save_goals(
        goals
    )

def update_goal_progress(
    goal_name: str,
    progress: int
):

    goals = load_goals()

    for goal in goals:

        if (
            goal["goal"]
            == goal_name
        ):

            goal[
                "progress"
            ] = progress

            if progress >= 100:

                goal[
                    "completed"
                ] = True

    save_goals(
        goals
    )

def get_active_goals():

    return [

        goal

        for goal

        in load_goals()

        if not goal[
            "completed"
        ]
    ]

def get_current_goal():

    active = (
        get_active_goals()
    )

    if not active:

        return None

    return active[0]