from src.services.task_classifier import (
    classify_task
)


def choose_strategy(
    task: str
):

    complexity = (
        classify_task(
            task
        )
    )

    task_lower = (
        task.lower()
    )

    if any(
        word in task_lower
        for word in [
            "bug",
            "fix",
            "error",
            "issue"
        ]
    ):

        return "FAST"

    if any(
        word in task_lower
        for word in [
            "refactor",
            "architecture",
            "redesign"
        ]
    ):

        return "SAFE"

    if any(
        word in task_lower
        for word in [
            "research",
            "investigate",
            "analyze"
        ]
    ):

        return "RESEARCH"

    if complexity == "COMPLEX":

        return "PARALLEL"

    return "STANDARD"

def get_strategy_config(
    strategy: str
):

    configs = {

        "FAST": {
            "planner": False,
            "research": False,
            "parallel": False,
            "review": True
        },

        "STANDARD": {
            "planner": True,
            "research": True,
            "parallel": False,
            "review": True
        },

        "PARALLEL": {
            "planner": True,
            "research": True,
            "parallel": True,
            "review": True
        },

        "SAFE": {
            "planner": True,
            "research": True,
            "parallel": False,
            "review": True,
            "approval": True
        },

        "RESEARCH": {
            "planner": True,
            "research": True,
            "parallel": False,
            "review": False
        }
    }

    return configs.get(
        strategy,
        configs[
            "STANDARD"
        ]
    )

def get_task_strategy(
    task: str
):

    strategy = (
        choose_strategy(
            task
        )
    )

    return {

        "strategy":
        strategy,

        "config":
        get_strategy_config(
            strategy
        )
    }