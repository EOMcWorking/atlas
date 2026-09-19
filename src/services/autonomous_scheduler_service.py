import time
from pathlib import Path

from src.services.task_queue_service import (
    fail_task
)

from src.services.agent_orchestrator import (
    run_task
)

from src.services.approval_processor_service import (
    process_approved_tasks
)

from src.services.memory_capture_service import (
    save_agent_memory
)

from src.services.system_health_monitor_service import (
    run_health_monitor
)

from src.services.director_service import (
    decide_next_action,
    refresh_research,
    refresh_meta_learning
)

from src.services.autonomous_benchmark_service import (
    capture_benchmark
)

from src.services.atlas_state_service import (
    flush_state
)

# Configurable sleep interval
SCHEDULER_INTERVAL_SECONDS = 300
QUICK_INTERVAL_SECONDS = 60
LONG_INTERVAL_SECONDS = 600

# Cache refresh interval (every 10 cycles or 30 minutes, whichever comes first)
CACHE_REFRESH_CYCLES = 10


def get_scheduler_interval(mode: str = "NORMAL_EXECUTION") -> int:
    """
    Return sleep interval based on Director mode.
    Fast modes get shorter intervals, calm modes get longer.
    """
    fast_modes = ["HEALTH_RECOVERY", "INTEGRATION_RECOVERY", "BACKLOG_REDUCTION"]
    slow_modes = ["RESEARCH_MODE", "EXPLORATION_MODE"]

    if mode in fast_modes:
        return QUICK_INTERVAL_SECONDS
    if mode in slow_modes:
        return LONG_INTERVAL_SECONDS
    return SCHEDULER_INTERVAL_SECONDS


def stop_requested() -> bool:
    """
    Check if STOP_ATLAS file exists.
    """
    return Path("STOP_ATLAS").exists()


# ---------------------------------------------------------------------------
# Lifecycle functions
# ---------------------------------------------------------------------------

def scheduler_startup():
    """
    Runs once when Atlas starts.
    Initialize caches, database, memory, provider router, runtime state.
    """
    print("Atlas starting up...")

    try:
        refresh_research()
        refresh_meta_learning()
        print("Caches initialized.")
    except Exception as e:
        print(f"Cache init warning: {e}")

    # Future: initialize database, memory, provider router, runtime state here

    print("Atlas startup complete.")


def scheduler_cycle(cycle_count: int = 0):
    """
    Executes ONE autonomous cycle:
    approvals → health → caches → director → execute → benchmark
    Returns (sleep_seconds, work_executed).
    """

    # --- Approvals ---
    try:
        process_approved_tasks()
    except Exception as e:
        print(f"Approval processor error: {e}")

    # --- Health monitor ---
    try:
        health_result = run_health_monitor()
        if health_result.get("actions"):
            print(f"Health alerts triggered: {health_result['actions']}")
    except Exception as e:
        print(f"Health monitor error: {e}")

    # --- Refresh caches periodically (not every cycle) ---
    if cycle_count % CACHE_REFRESH_CYCLES == 0:
        try:
            refresh_research()
            refresh_meta_learning()
            print("Caches refreshed.")
        except Exception as e:
            print(f"Cache refresh error: {e}")

    # --- Director decides ---
    try:
        decision = decide_next_action()
        mode = decision.get("mode", "NORMAL_EXECUTION")
        print(f"Director mode: {mode}")
    except Exception as e:
        print(f"Director decision error: {e}")
        return SCHEDULER_INTERVAL_SECONDS, False

    selected_work = decision.get("selected_work")

    if not selected_work:
        print("No work available.")
        return get_scheduler_interval(mode), False

    work_type = selected_work.get("type")
    work_item = selected_work.get("item")

    # --- Execute work based on mode ---
    executed = False

    if mode == "INTEGRATION_RECOVERY":
        executed = _execute_integration_repair()

    elif mode == "RESEARCH_MODE":
        executed = _execute_research()

    elif mode == "EXPLORATION_MODE":
        executed = _execute_exploration(work_item)

    elif mode == "MILESTONE_EXECUTION":
        task = work_item if isinstance(work_item, str) else str(work_item)
        executed = _execute_task(task)

    elif work_type == "MILESTONE":
        task = work_item if isinstance(work_item, str) else str(work_item)
        executed = _execute_task(task)

    elif work_type == "TASK":
        executed = _execute_task(work_item)

    elif work_type == "IMPROVEMENT":
        title = work_item.get("title", "Unknown improvement") if isinstance(work_item, dict) else str(work_item)
        executed = _execute_task(title)

    elif work_type == "INTEGRATION_REPAIR":
        executed = _execute_integration_repair()

    elif work_type == "RESEARCH":
        executed = _execute_research()

    elif work_type == "EXPLORATION":
        executed = _execute_exploration(work_item)

    else:
        print(f"Unknown work type: {work_type}")

    # --- Benchmark only if work was actually executed ---
    if executed:
        try:
            capture_benchmark()
        except Exception as e:
            print(f"Benchmark error: {e}")

    return get_scheduler_interval(mode), executed


def scheduler_shutdown():
    """
    Runs once before Atlas exits.
    Flush state, save memories, save runtime metrics, create snapshots.
    """
    print("Shutting down Atlas...")

    try:
        flush_state()
        print("State flushed successfully.")
    except Exception as e:
        print(f"Error flushing state: {e}")

    # Future: save memories, save runtime metrics, create snapshots here

    print("Atlas stopped.")


# ---------------------------------------------------------------------------
# Work execution helpers (return True if work was executed)
# ---------------------------------------------------------------------------

def _execute_task(task: str) -> bool:
    """Execute a single task through the orchestrator. Returns True if executed."""
    try:
        print(f"Running task: {task}")
        result = run_task(task)
        success = result.get("success", False)
        if not success:
            print("Task failed")
        save_agent_memory("Scheduler", str(result))
        return True
    except Exception as e:
        print(f"Task error: {e}")
        fail_task(task)
        return False


def _execute_integration_repair() -> bool:
    """Run integration repair workflow. Returns True if executed."""
    try:
        from src.services.integration_repair_service import get_integration_repair_report
        print("Running integration repair...")
        repair = get_integration_repair_report()
        save_agent_memory("Scheduler", str(repair))
        print("Integration repair completed.")
        return True
    except Exception as e:
        print(f"Integration repair error: {e}")
        return False


def _execute_research() -> bool:
    """Run autonomous research workflow. Returns True if executed."""
    try:
        from src.services.autonomous_research_service import get_research_report
        print("Running autonomous research...")
        research = get_research_report()
        save_agent_memory("Scheduler", str(research))
        print("Research completed.")
        return True
    except Exception as e:
        print(f"Research error: {e}")
        return False


def _execute_exploration(work_item) -> bool:
    """Run exploration experiment. Returns True if executed."""
    try:
        from src.services.experiment_manager_service import execute_experiment
        print("Running exploration experiment...")
        strategy_b = work_item if isinstance(work_item, str) else "alternative"
        experiment = execute_experiment(
            strategy_a="current_best",
            strategy_b=strategy_b
        )
        save_agent_memory("Scheduler", str(experiment))
        print("Exploration completed.")
        return True
    except Exception as e:
        print(f"Exploration error: {e}")
        return False


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_scheduler():
    """
    Atlas autonomous scheduler.
    startup → loop(cycle) → shutdown
    """

    scheduler_startup()

    cycle_count = 0

    while True:

        if stop_requested():
            break

        sleep_seconds, _ = scheduler_cycle(cycle_count)

        cycle_count += 1

        time.sleep(sleep_seconds)

    scheduler_shutdown()