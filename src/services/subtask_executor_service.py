from src.agents.planner_agent import plan
from src.agents.research_agent import research
from src.agents.architect_agent import architect
from src.agents.reviewer_agent import review

from src.services.project_edit_executor_service import (
    execute_project_edit
)


def execute_subtask(
    subtask: str
):
    print(
        "STARTING SUBTASK:",
        subtask
    )

    plan_result = plan(
        subtask
    )

    research_result = research(
        plan_result
    )

    architecture_result = architect(
        plan_result,
        research_result
    )

    edit_result = execute_project_edit(
        subtask,
        plan_result
    )

    review_result = review(
        str(edit_result)
    )

    return {
        "subtask": subtask,
        "plan": plan_result,
        "research": research_result,
        "architecture": architecture_result,
        "code": str(edit_result),
        "review": review_result
    }