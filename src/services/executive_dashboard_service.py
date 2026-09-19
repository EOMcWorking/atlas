import time

from src.services.project_health_service import (
    health_summary
)

from src.services.goal_management_service import (
    get_active_goals
)

from src.services.milestone_service import (
    get_active_milestones
)

from src.services.task_queue_service import (
    get_pending_tasks
)

from src.services.system_intelligence_service import (
    get_system_intelligence
)

from src.services.autonomous_director_service import (
    get_directive
)

from src.services.system_integration_audit_service import (
    get_system_integration_report
)

from src.services.integration_repair_service import (
    get_integration_repair_report
)

from src.services.autonomous_benchmark_service import (
    get_benchmark_report
)

from src.services.evolution_scoring_service import (
    get_evolution_report
)


def _safe_call(func):
    """Call a function safely, returning empty dict on failure."""
    try:
        return func()
    except Exception:
        return {}


def _clamp(value, minimum=0, maximum=100):
    """Clamp a value between min and max."""
    return max(minimum, min(maximum, value))


def build_dashboard():

    generated_at = time.time()

    # Core services (must succeed)
    integration = _safe_call(get_system_integration_report)
    integration_score = _clamp(integration.get("integration_score", 0))

    if integration_score >= 95:
        integration_status = "EXCELLENT"
    elif integration_score >= 85:
        integration_status = "GOOD"
    elif integration_score >= 70:
        integration_status = "NEEDS_ATTENTION"
    else:
        integration_status = "CRITICAL"

    # Optional services (fail individually without killing dashboard)
    repair = _safe_call(get_integration_repair_report)
    benchmark = _safe_call(get_benchmark_report)
    evolution = _safe_call(get_evolution_report)
    intelligence = _safe_call(get_system_intelligence)
    director = _safe_call(get_directive)
    health = _safe_call(health_summary)
    goals = _safe_call(get_active_goals)
    milestones = _safe_call(get_active_milestones)
    tasks = _safe_call(get_pending_tasks)

    return {

        "health":
        health,

        "goals":
        goals,

        "milestones":
        milestones,

        "pending_tasks":
        tasks,

        "intelligence":
        intelligence,

        "director":
        director,

        "integration": {
            "report": integration,
            "status": integration_status,
            "score": integration_score
        },

        "repair":
        repair,

        "benchmark":
        benchmark,

        "evolution":
        evolution,

        "generated_at":
        generated_at
    }


def get_dashboard_summary(
    dashboard: dict = None
):
    """
    Accept an optional pre-built dashboard to avoid duplicate work.
    If not provided, builds one internally.
    """

    if dashboard is None:
        dashboard = build_dashboard()

    health_score = _clamp(dashboard["health"].get("score", 0))
    intelligence_score = _clamp(dashboard["intelligence"].get("score", 0))
    integration_score = _clamp(dashboard["integration"]["score"])

    goals = dashboard["goals"]
    if isinstance(goals, list) and len(goals) > 0:
        goal_progress = sum(g.get("progress", 0) for g in goals) / len(goals)
    else:
        goal_progress = 0

    evolution = dashboard.get("evolution", {})
    benchmark = dashboard.get("benchmark", {})

    generated_at = dashboard.get("generated_at")
    if generated_at is None:
        generated_at = time.time()

    return {

        "health_score":
        health_score,

        "integration_score":
        integration_score,

        "integration_status":
        dashboard["integration"]["status"],

        "goal_progress":
        int(goal_progress),

        "goal_count":
        len(goals) if isinstance(goals, list) else 0,

        "milestone_count":
        len(dashboard["milestones"]) if isinstance(dashboard["milestones"], list) else 0,

        "task_count":
        len(dashboard["pending_tasks"]) if isinstance(dashboard["pending_tasks"], list) else 0,

        "intelligence_score":
        intelligence_score,

        "evolution_score":
        evolution.get("score", 0),

        "evolution_grade":
        evolution.get("grade", "NEUTRAL"),

        "benchmark_latest":
        benchmark.get("latest"),

        "generated_at":
        generated_at
    }


def get_system_status(
    summary: dict = None
):
    """
    Accept an optional pre-built summary to avoid duplicate work.
    Weighted scoring: Health 40%, Integration 35%, Intelligence 25%
    Returns dict with status and overall_score.
    """

    if summary is None:
        summary = get_dashboard_summary()

    health = _clamp(summary["health_score"])
    intelligence = _clamp(summary["intelligence_score"])
    integration = _clamp(summary["integration_score"])

    overall = (
        health * 0.4
        + integration * 0.35
        + intelligence * 0.25
    )

    if overall >= 90:
        status = "EXCELLENT"
    elif overall >= 75:
        status = "GOOD"
    elif overall >= 60:
        status = "FAIR"
    elif overall >= 40:
        status = "POOR"
    else:
        status = "CRITICAL"

    return {
        "status": status,
        "overall_score": round(overall, 2)
    }