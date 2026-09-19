from src.services.resource_allocator_service import (
    allocate_next_work
)

from src.services.capacity_planning_service import (
    get_capacity_status
)

from src.services.predictive_risk_service import (
    get_risk_summary
)

from src.services.system_health_dashboard_service import (
    get_health_report
)

from src.services.autonomous_goal_service import (
    get_primary_goal
)

from src.services.goal_progress_service import (
    get_goal_progress_report
)

from src.services.autonomous_roadmap_service import (
    get_roadmap_summary
)

from src.services.milestone_tracking_service import (
    get_milestone_report
)

from src.services.autonomous_benchmark_service import (
    get_benchmark_report
)

from src.services.meta_learning_service import (
    get_meta_learning_report
)

from src.services.system_integration_audit_service import (
    get_system_integration_report
)

from src.services.goal_alignment_service import (
    get_alignment_score
)

from src.services.execution_context_service import (
    set_current_goal,
    set_current_milestone,
    set_current_mode,
    set_current_task,
    set_current_provider,
    set_current_strategy,
    set_current_workflow
)


# Cached values — refreshed periodically, not every cycle
_last_research = None
_last_meta_learning = None
_last_context = None


def build_director_context():
    """
    Build context ONCE per decision cycle.
    All decisions reference this snapshot for consistency.
    """
    global _last_context

    integration = get_system_integration_report()
    health = get_health_report()
    primary_goal = get_primary_goal()
    roadmap = get_roadmap_summary()
    milestones = get_milestone_report()
    capacity = get_capacity_status()
    risk = get_risk_summary()
    benchmarks = get_benchmark_report()

    _last_context = {
        "health": health,
        "capacity": capacity,
        "risk": risk,
        "primary_goal": primary_goal,
        "goal_progress": get_goal_progress_report(),
        "roadmap": roadmap,
        "milestones": milestones,
        "benchmarks": benchmarks,
        "integration_score": integration.get("integration_score", 100),
        "integration": integration,
    }

    return _last_context


def get_cached_research():
    """Return cached research, avoiding LLM call every cycle."""
    global _last_research
    return _last_research


def refresh_research():
    """Explicitly refresh research cache — call periodically, not every cycle."""
    global _last_research
    from src.services.autonomous_research_service import get_research_report
    _last_research = get_research_report()
    return _last_research


def get_cached_meta_learning():
    """Return cached meta-learning, avoiding LLM call every cycle."""
    global _last_meta_learning
    if _last_meta_learning is None:
        _last_meta_learning = get_meta_learning_report()
    return _last_meta_learning


def refresh_meta_learning():
    """Explicitly refresh meta-learning cache."""
    global _last_meta_learning
    _last_meta_learning = get_meta_learning_report()
    return _last_meta_learning


def _update_execution_context(
    mode,
    primary_goal,
    milestone,
    selected_work
):
    """
    Synchronize the Director's decision into the global execution context.
    """

    set_current_mode(mode)

    if primary_goal:
        goal_title = primary_goal if isinstance(primary_goal, str) else primary_goal.get("title")
        set_current_goal(goal_title)

    if milestone:
        milestone_title = milestone if isinstance(milestone, str) else milestone.get("title")
        set_current_milestone(milestone_title)

    if (
        selected_work
        and selected_work.get("type")
        in (
            "TASK",
            "MILESTONE",
            "IMPROVEMENT"
        )
    ):
        set_current_task(
            selected_work.get("item")
        )

    # Set provider and strategy based on mode
    if mode == "INTEGRATION_RECOVERY":
        set_current_provider("openrouter")
        set_current_strategy("repair")
        set_current_workflow("integration_repair")
    elif mode == "RESEARCH_MODE":
        set_current_provider("openrouter")
        set_current_strategy("research")
        set_current_workflow("autonomous_research")
    elif mode == "EXPLORATION_MODE":
        set_current_provider("openrouter")
        set_current_strategy("exploration")
        set_current_workflow("experiment")
    elif mode == "HEALTH_RECOVERY":
        set_current_provider("openrouter")
        set_current_strategy("health_recovery")
        set_current_workflow("health_monitor")
    elif mode == "BACKLOG_REDUCTION":
        set_current_provider("openrouter")
        set_current_strategy("backlog")
        set_current_workflow("task_execution")
    else:
        set_current_provider("openrouter")
        set_current_strategy("default")
        set_current_workflow("task_execution")


def determine_priority_mode():
    """
    Decision hierarchy:
    Health → Integration → Capacity → Goal → Roadmap → Milestone → Alignment
    """

    ctx = _last_context if _last_context else build_director_context()

    health = ctx["health"]
    integration_score = ctx["integration_score"]
    capacity = ctx["capacity"]
    milestones = ctx["milestones"]
    roadmap = ctx["roadmap"]

    # 1. Health — always highest priority
    if health.get("health_score", 0) < 60:
        return "HEALTH_RECOVERY"

    # 2. Integration — structural problems
    if integration_score < 80:
        return "INTEGRATION_RECOVERY"

    # 3. Capacity — don't start new work when overloaded
    if capacity == "OVERLOADED":
        return "BACKLOG_REDUCTION"

    # 4. Milestones — if active milestone exists, work toward it
    active_milestone = milestones.get("active")
    if active_milestone:
        return "MILESTONE_EXECUTION"

    # 5. Roadmap — if roadmap has milestones defined
    if roadmap and roadmap.get("roadmap"):
        return "ROADMAP_EXECUTION"

    # 6. Research — only if cached research exists and health is stable
    research = get_cached_research()
    if research and health.get("health_score", 0) >= 70:
        return "RESEARCH_MODE"

    # 7. Exploration — only if meta-learning suggests it
    meta = get_cached_meta_learning()
    analysis = meta.get("analysis", "").lower()
    if "exploration" in analysis and health.get("health_score", 0) >= 80:
        return "EXPLORATION_MODE"

    return "NORMAL_EXECUTION"


def decide_next_action():
    """
    Use the snapshot context to decide the single next action.
    All decisions made from one consistent context.
    """

    ctx = _last_context if _last_context else build_director_context()

    mode = determine_priority_mode()
    primary_goal = ctx["primary_goal"]
    milestones = ctx["milestones"]
    roadmap = ctx["roadmap"]

    # --- INTEGRATION_RECOVERY ---
    if mode == "INTEGRATION_RECOVERY":
        from src.services.integration_repair_service import get_integration_repair_report
        repair = get_integration_repair_report()
        repair_plan = repair.get("repair", {})
        issues = repair_plan.get("issues", [])

        selected_work = {
            "type": "INTEGRATION_REPAIR",
            "item": issues[0] if issues else "Repair integration issues",
            "score": 90,
            "reason": f"Integration score is {ctx['integration_score']} — repair required"
        }

        _update_execution_context(
            mode,
            primary_goal,
            None,
            selected_work
        )

        return {
            "mode": mode,
            "selected_work": selected_work,
            "primary_goal": primary_goal,
            "repair": repair
        }

    # --- MILESTONE_EXECUTION ---
    if mode == "MILESTONE_EXECUTION":
        active = milestones.get("active", {})
        milestone_title = active.get("title", "Complete active milestone")

        selected_work = {
            "type": "MILESTONE",
            "item": milestone_title,
            "score": 85,
            "reason": "Active milestone in progress"
        }

        _update_execution_context(
            mode,
            primary_goal,
            active,
            selected_work
        )

        return {
            "mode": mode,
            "selected_work": selected_work,
            "primary_goal": primary_goal,
            "milestone": active
        }

    # --- ROADMAP_EXECUTION ---
    if mode == "ROADMAP_EXECUTION":
        milestone_report = roadmap.get("milestone_report", {})
        active_rm = milestone_report.get("active")
        milestone_title = active_rm.get("title", "Next roadmap milestone") if active_rm else "Next roadmap milestone"

        selected_work = {
            "type": "MILESTONE",
            "item": milestone_title,
            "score": 80,
            "reason": "Roadmap-driven milestone"
        }

        _update_execution_context(
            mode,
            primary_goal,
            active_rm,
            selected_work
        )

        return {
            "mode": mode,
            "selected_work": selected_work,
            "primary_goal": primary_goal
        }

    # --- RESEARCH_MODE ---
    if mode == "RESEARCH_MODE":
        research = get_cached_research()

        selected_work = {
            "type": "RESEARCH",
            "item": "Autonomous research findings",
            "score": 75,
            "reason": "Research Mode — exploring new capabilities"
        }

        _update_execution_context(
            mode,
            primary_goal,
            None,
            None
        )

        return {
            "mode": mode,
            "selected_work": selected_work,
            "primary_goal": primary_goal,
            "research": research
        }

    # --- EXPLORATION_MODE ---
    if mode == "EXPLORATION_MODE":
        meta = get_cached_meta_learning()
        lessons = meta.get("lessons", [])

        selected_work = {
            "type": "EXPLORATION",
            "item": lessons[0] if lessons else "Explore new learning approach",
            "score": 80,
            "reason": "Exploration Mode — Atlas learning optimization"
        }

        _update_execution_context(
            mode,
            primary_goal,
            None,
            None
        )

        return {
            "mode": mode,
            "selected_work": selected_work,
            "primary_goal": primary_goal,
            "meta_learning": meta
        }

    # --- NORMAL_EXECUTION ---
    work = allocate_next_work()

    if primary_goal and work:
        # Use goal_alignment_service instead of fragile substring match
        work_item = str(work.get("item", ""))
        alignment = get_alignment_score(work_item)

        if alignment < 70:
            work = {
                "type": "TASK",
                "item": primary_goal["title"],
                "score": primary_goal["priority"] * 10,
                "reason": f"Goal alignment score {alignment} — prioritizing primary goal"
            }

    _update_execution_context(
        mode,
        primary_goal,
        None,
        work
    )

    return {
        "mode": mode,
        "selected_work": work,
        "primary_goal": primary_goal
    }


def get_director_report():
    ctx = build_director_context()
    decision = decide_next_action()

    return {
        "context": ctx,
        "decision": decision
    }