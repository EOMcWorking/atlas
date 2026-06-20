from src.agents.planner_agent import plan
from src.agents.coder_agent import code
from src.agents.reviewer_agent import review


def run_task(
    task: str
):

    plan_result = plan(task)

    code_result = code(
        plan_result
    )

    review_result = review(
        code_result
    )

    return {
        "plan": plan_result,
        "code": code_result,
        "review": review_result
    }