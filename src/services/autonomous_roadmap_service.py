from src.services.autonomous_goal_service import (
    get_primary_goal
)

from src.services.goal_planning_service import (
    get_goal_plan
)

from src.services.ollama_service import (
    chat
)

from src.services.milestone_tracking_service import (
    add_milestone,
    get_active_milestone
)


def generate_roadmap():

    goal = (
        get_primary_goal()
    )

    if not goal:

        return {
            "success": False,
            "message": "No active goal"
        }

    plan = (
        get_goal_plan()
    )

    prompt = f"""
Primary Goal:

{goal['title']}

Existing Goal Plan:

{plan}

Create:

1. Milestones
2. Success criteria
3. Execution sequence
4. Dependencies
5. Estimated completion path

Return concise roadmap.
"""

    roadmap = chat(
        prompt,
        task_type="planning"
    )

    # Extract milestones from roadmap and populate milestones.json
    _populate_milestones_from_roadmap(roadmap)

    return {

        "success": True,

        "goal":
        goal,

        "roadmap":
        roadmap
    }


def _populate_milestones_from_roadmap(roadmap: str):
    """
    Parse the roadmap for milestone markers and add them
    to the milestone tracker.
    """
    lines = roadmap.splitlines()

    for line in lines:
        line_stripped = line.strip().lower()

        # Match lines like "Milestone 1: ..." or "Milestone: ..."
        if line_stripped.startswith("milestone"):
            # If there's an active milestone already, skip duplicates
            if not get_active_milestone() or line_stripped not in str(get_active_milestone()).lower():
                add_milestone(line.strip())


def get_roadmap():

    result = (
        generate_roadmap()
    )

    return result.get(
        "roadmap",
        ""
    )


def get_roadmap_summary():

    goal = (
        get_primary_goal()
    )

    roadmap = (
        get_roadmap()
    )

    from src.services.milestone_tracking_service import get_milestone_report

    return {

        "goal":
        goal,

        "roadmap":
        roadmap,

        "milestone_report":
        get_milestone_report()
    }