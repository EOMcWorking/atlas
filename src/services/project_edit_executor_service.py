from src.services.edit_strategy_service import (
    determine_edit_targets
)

from src.services.multi_file_patch_service import (
    patch_project_files
)

from src.services.change_planning_service import (
    create_change_plan
)

from src.services.change_simulation_service import (
    simulate_change
)

from src.services.change_execution_policy_service import (
    determine_execution_policy
)

from src.services.change_plan_parser_service import (
    extract_plan_files
)

from src.services.architecture_guard_service import (
    check_architecture_guard
)

from src.services.approval_service import (
    create_approval
)

from src.services.change_history_service import (
    record_change
)

from src.services.safety_governor_service import (
    evaluate_action
)

from src.services.file_backup_service import (
    backup_file
)

from src.services.patch_validation_service import (
    validate_patch
)

from src.services.auto_rollback_service import (
    auto_rollback
)

from src.services.review_result_service import (
    get_review_verdict
)

from src.services.autonomous_benchmark_service import (
    capture_benchmark
)

from src.services.evolution_scoring_service import (
    get_evolution_report
)

from src.services.capacity_planning_service import (
    get_capacity_status
)

from src.services.file_reader_service import read_file


def execute_project_edit(
    task: str,
    plan: str
):

    # Step 2: Generate a change plan
    change_plan = create_change_plan(
        task
    )

    # Step 3: Simulate the change
    simulation = simulate_change(
        task,
        change_plan
    )

    # Step 4: Determine execution policy
    policy = determine_execution_policy(
        simulation
    )

    # Step 5: Handle HIGH/CRITICAL risk — create approval instead of blocking
    if policy["approval_required"]:

        approval = create_approval(
            task,
            {
                "change_plan": change_plan,
                "simulation": simulation,
                "policy": policy
            }
        )

        record_change(
            task=task,
            files=[],
            risk=simulation["highest_risk"],
            policy=policy["policy"],
            success=False,
            benchmark=None,
            evolution_score=None
        )

        return {
            "success": False,
            "reason": "Approval required",
            "policy": policy,
            "simulation": simulation,
            "change_plan": change_plan,
            "approval": approval
        }

    # Step 6: Use planned files from the change plan
    targets = extract_plan_files(
        change_plan
    )

    # Step 7: Fallback to old logic if no targets found
    if not targets:

        targets = determine_edit_targets(
            task,
            plan
        )

    # Adaptive execution limit based on capacity
    capacity = get_capacity_status()
    if capacity == "OVERLOADED":
        execution_limit = 1
    elif capacity == "HEAVY":
        execution_limit = 2
    else:
        execution_limit = 3

    results = []

    for target in targets[:execution_limit]:

        # Wrap per-file work in try/except for resilience
        try:

            # Architecture guard before patching
            guard = check_architecture_guard(
                target
            )

            if not guard["allowed"]:

                results.append(
                    {
                        "success": False,
                        "file": target,
                        "error": guard["reason"]
                    }
                )

                continue

            # Safety governor check per file
            decision = evaluate_action(
                task,
                target
            )

            if not decision["approved"]:

                results.append({
                    "success": False,
                    "target_file": target,
                    "error": decision["reason"]
                })

                continue

            # Backup → Patch → Validate → Rollback → Review
            original_content = read_file(target)
            backup_file(target)

            result = patch_project_files(
                task,
                target
            )

            # Validate
            if result.get("success"):
                patched_content = read_file(target)
                validation = validate_patch(
                    original_content,
                    patched_content,
                    target
                )

                if not validation.get("success"):
                    auto_rollback(
                        target,
                        validation.get("reason", "Patch validation failed")
                    )
                    result = {
                        "success": False,
                        "file": target,
                        "error": validation.get("reason", "Validation failed"),
                        "rolled_back": True
                    }
                else:
                    # Review with full context
                    review_verdict = get_review_verdict(patched_content)
                    if review_verdict != "APPROVED":
                        auto_rollback(
                            target,
                            f"Review rejected: {review_verdict}"
                        )
                        result = {
                            "success": False,
                            "file": target,
                            "error": f"Review verdict: {review_verdict}",
                            "rolled_back": True
                        }

            results.append(result)

        except Exception as e:
            # Catch any unexpected exception and continue with next file
            results.append({
                "success": False,
                "file": target,
                "error": str(e)
            })

    # Success only if at least one patch succeeded
    success = any(
        result.get("success", False)
        for result in results
    )

    # Benchmark and evolution only after actual success
    benchmark = None
    evolution = None

    if success:
        benchmark = capture_benchmark()
        evolution = get_evolution_report()

    # Record history with final enriched outcome
    record_change(
        task=task,
        files=targets,
        risk=simulation["highest_risk"],
        policy=policy["policy"],
        success=success,
        benchmark=benchmark,
        evolution_score=evolution.get("score") if evolution else None
    )

    # Step 8: Return diagnostics
    return {
        "success": success,
        "change_plan": change_plan,
        "simulation": simulation,
        "policy": policy,
        "results": results,
        "evolution": evolution
    }