from threading import Lock
import time

_lock = Lock()

_context = {
    "task": None,
    "goal": None,
    "milestone": None,
    "mode": "NORMAL_EXECUTION",
    "provider": None,
    "agent": None,
    "workflow": None,
    "strategy": None,
    "budget": None,
    "started_at": None,
    "updated_at": time.time()
}


def get_context():

    with _lock:
        return dict(_context)


def update_context(**kwargs):

    with _lock:

        _context.update(kwargs)

        _context["updated_at"] = time.time()

        return dict(_context)


def reset_context():

    with _lock:

        _context.update({
            "task": None,
            "goal": None,
            "milestone": None,
            "mode": "NORMAL_EXECUTION",
            "provider": None,
            "agent": None,
            "workflow": None,
            "strategy": None,
            "budget": None,
            "started_at": None,
            "updated_at": time.time()
        })


def set_current_task(task):

    return update_context(
        task=task,
        started_at=time.time()
    )


def clear_current_task():

    return update_context(
        task=None,
        started_at=None
    )


def set_current_provider(provider):

    return update_context(
        provider=provider
    )


def set_current_agent(agent):

    return update_context(
        agent=agent
    )


def set_current_strategy(strategy):

    return update_context(
        strategy=strategy
    )


def set_current_workflow(workflow):

    return update_context(
        workflow=workflow
    )


def set_current_goal(goal: str):
    """Update only the current goal."""
    return update_context(goal=goal)


def set_current_milestone(milestone: str):
    """Update only the current milestone."""
    return update_context(milestone=milestone)


def set_current_mode(mode: str):
    """Update only the current mode."""
    return update_context(mode=mode)


def get_current_goal():
    """Get the current goal."""
    return get_context().get("goal")


def get_current_milestone():
    """Get the current milestone."""
    return get_context().get("milestone")


def get_current_task():
    """Get the current task."""
    return get_context().get("task")


def get_current_mode():
    """Get the current mode."""
    return get_context().get("mode", "NORMAL_EXECUTION")


def get_current_provider():
    """Get the current provider."""
    return get_context().get("provider")


def get_current_strategy():
    """Get the current strategy."""
    return get_context().get("strategy")


def get_current_workflow():
    """Get the current workflow."""
    return get_context().get("workflow")


def get_context_summary():
    """Lightweight summary for dashboards."""
    ctx = get_context()
    return {
        "goal": ctx["goal"],
        "milestone": ctx["milestone"],
        "task": ctx["task"],
        "mode": ctx["mode"],
        "provider": ctx["provider"],
        "strategy": ctx["strategy"],
        "workflow": ctx["workflow"],
        "uptime_seconds": round(time.time() - ctx["started_at"], 2) if ctx["started_at"] else 0
    }