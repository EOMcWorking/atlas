from fastapi import APIRouter

from src.services.executive_dashboard_service import (
    build_dashboard,
    get_dashboard_summary,
    get_system_status
)

from src.services.project_health_service import (
    calculate_project_health
)

from src.services.atlas_state_service import (
    get_state
)

from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.project_graph_service import (
    get_high_risk_files
)

from src.services.self_improvement_service import (
    generate_self_improvements
)

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)


# ---------------------------------------------------------------------------
# Executive Dashboard
# ---------------------------------------------------------------------------

@router.get("")
def dashboard() -> dict:
    """
    Complete Atlas executive dashboard.
    """
    return build_dashboard()


@router.get("/summary")
def summary() -> dict:
    """
    Lightweight dashboard summary.
    """
    dashboard = build_dashboard()
    return get_dashboard_summary(dashboard)


@router.get("/status")
def status() -> dict:
    """
    Overall Atlas runtime status.
    """
    dashboard = build_dashboard()
    summary = get_dashboard_summary(dashboard)

    return {
        "status": get_system_status(summary),
        "summary": summary
    }


# ---------------------------------------------------------------------------
# Detailed Diagnostics
# ---------------------------------------------------------------------------

@router.get("/health")
def health() -> dict:
    return calculate_project_health()


@router.get("/state")
def state() -> dict:
    return get_state()


@router.get("/failures")
def failures() -> dict:
    return analyze_failures()


@router.get("/high-risk-files")
def high_risk_files() -> dict:
    return {
        "files": get_high_risk_files()
    }


@router.get("/improvements")
def improvements() -> dict:
    """
    Current self-improvement suggestions.
    """
    return {
        "suggestions": generate_self_improvements()
    }