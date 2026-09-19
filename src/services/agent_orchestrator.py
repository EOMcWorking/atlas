from src.services.task_classifier import classify_task
from src.services.task_validation import validate_task
from src.services.workflow_estimator import estimate_runtime

from src.agents.decomposer_agent import (
    decompose
)

from src.agents.coder_agent import code
from src.agents.reviewer_agent import review

from src.services.task_parser_service import (
    parse_subtasks
)

from src.services.parallel_executor_service import (
    execute_subtasks_parallel
)

from src.services.review_parser_service import (
    review_passed
)

from src.services.memory_capture_service import (
    save_agent_memory
)

from src.services.knowledge_capture_service import (
    capture_knowledge
)

from src.services.task_generation_service import (
    generate_next_task
)

from src.services.task_tracker_service import (
    add_task
)

from src.services.handoff_service import (
    update_handoff
)

from src.services.workflow_metrics_service import (
    record_workflow
)

from src.services.linter_service import (
    run_linter
)

from src.services.test_runner_service import (
    run_tests
)

from src.services.self_healing_service import (
    self_heal
)

from src.services.approval_service import (
    create_approval
)

from src.services.pull_request_service import (
    generate_pull_request
)

from src.services.task_queue_service import (
    complete_task,
    fail_task
)

from src.services.task_extraction_service import (
    extract_task
)

from src.services.task_failure_service import (
    record_failure
)

from src.services.agent_voting_service import (
    vote_on_solution
)

from src.services.atlas_state_service import (
    mark_task_started,
    mark_task_success,
    mark_task_failure
)

from src.services.execution_context_service import (
    get_context,
    clear_current_task
)

import time


def run_task(
    task: str
):

    start_time = time.time()

    # Read execution context once — reuse throughout
    context = get_context()
    current_goal = context.get("goal")
    current_mode = context.get("mode", "NORMAL_EXECUTION")
    current_provider = context.get("provider")
    current_agent = context.get("agent")
    current_strategy = context.get("strategy")
    current_workflow = context.get("workflow")
    current_milestone = context.get("milestone")

    # Mark task as started
    mark_task_started(task)

    # Validate first
    if not validate_task(task):
        mark_task_failure(task)
        clear_current_task()
        return {
            "success": False,
            "message": "Task is too vague. Please provide more detail."
        }

    # Classify
    complexity = classify_task(task)

    estimate = estimate_runtime(
        complexity
    )

    print(
        f"TASK COMPLEXITY: {complexity}"
    )

    print(
        f"ESTIMATED CALLS: {estimate['calls']}"
    )

    print(
        f"ESTIMATED RUNTIME: {estimate['runtime']}"
    )

    print(
        f"EXECUTION MODE: {current_mode}"
    )

    if current_goal:
        print(f"CURRENT GOAL: {current_goal}")
    if current_milestone:
        print(f"CURRENT MILESTONE: {current_milestone}")
    if current_provider:
        print(f"PROVIDER: {current_provider}")
    if current_strategy:
        print(f"STRATEGY: {current_strategy}")
    if current_workflow:
        print(f"WORKFLOW: {current_workflow}")

    # Fast Mode
    if complexity == "SIMPLE":
        print("FAST MODE")

        code_result = code(task)

        duration = time.time() - start_time

        # Capture knowledge even in fast mode
        capture_knowledge(task, "FAST MODE - Review skipped")

        # Record workflow metrics
        record_workflow(
            task=task,
            success=True,
            duration=duration,
            goal=current_goal,
            mode=current_mode,
            provider=current_provider,
            strategy=current_strategy,
            workflow=current_workflow,
            complexity=complexity
        )

        mark_task_success(task)
        clear_current_task()

        return {
            "task": task,
            "success": True,
            "mode": "fast",
            "goal": current_goal,
            "director_mode": current_mode,
            "milestone": current_milestone,
            "provider": current_provider,
            "strategy": current_strategy,
            "workflow": current_workflow,
            "code": code_result,
            "review": "SKIPPED",
            "duration": duration
        }

    # Continue normal workflow below...

    decomposition = decompose(
        task
    )

    print("STEP: DECOMPOSE")

    subtasks = parse_subtasks(
        decomposition
    )

    print("SUBTASK COUNT:", len(subtasks))
    print(subtasks)

    all_results = (
        execute_subtasks_parallel(
            subtasks
        )
    )

    print("STEP: PARALLEL EXECUTION DONE")

    plan_result = "\n\n".join(
        result.get("plan", "")
        for result in all_results
    )

    research_result = "\n\n".join(
        result.get("research", "")
        for result in all_results
    )

    architecture_result = "\n\n".join(
        result.get("architecture", "")
        for result in all_results
    )

    code_result = "\n\n".join(
        result.get("code", "")
        for result in all_results
    )

    review_result = "\n\n".join(
        result.get("review", "")
        for result in all_results
    )

    vote_result = vote_on_solution(
        task,
        research_result,
        architecture_result,
        review_result
    )

    success = review_passed(
        review_result
    )

    print("STEP: REVIEW PASSED CHECK")

    # Handle review failure
    if not success:
        fail_task(task)
        record_failure(
            task,
            review_result
        )

        duration = time.time() - start_time
        record_workflow(
            task=task,
            success=success,
            duration=duration,
            goal=current_goal,
            mode=current_mode,
            provider=current_provider,
            strategy=current_strategy,
            workflow=current_workflow,
            complexity=complexity
        )

        mark_task_failure(task)
        clear_current_task()

        return {
            "task": task,
            "success": False,
            "goal": current_goal,
            "director_mode": current_mode,
            "milestone": current_milestone,
            "provider": current_provider,
            "strategy": current_strategy,
            "workflow": current_workflow,
            "subtasks": subtasks,
            "plan": plan_result,
            "research": research_result,
            "architecture": architecture_result,
            "code": code_result,
            "review": review_result,
            "vote": vote_result,
            "duration": duration,
        }

    if success:

        complete_task(
            task
        )

        print("STEP: LINTER")

        lint_result = (
            run_linter()
        )

        if not lint_result["success"]:

            heal_result = self_heal(
                code_result,
                lint_result["errors"]
            )

            code_result = heal_result["code"]

    print("STEP: TESTS")

    test_result = (
        run_tests()
    )

    if not test_result["success"]:

        heal_result = self_heal(
            code_result,
            test_result["errors"]
        )

        code_result = heal_result["code"]

    next_task = None

    if success:
        create_approval(
            task,
            review_result
        )

        print("STEP: CAPTURE KNOWLEDGE")

        capture_knowledge(
            task,
            review_result
        )

        save_agent_memory(
            "Workflow",
            f"""
Goal: {current_goal}
Milestone: {current_milestone}
Mode: {current_mode}
Provider: {current_provider}
Strategy: {current_strategy}
Workflow: {current_workflow}
Agent: {current_agent}

Task:
{task}

Subtasks:
{subtasks}

Plan:
{plan_result}

Research:
{research_result}

Architecture:
{architecture_result}

Review:
{review_result}
"""
        )

        print("STEP: GENERATE NEXT TASK")

        next_task_result = (
            generate_next_task()
        )

        next_task = (
            extract_task(
                next_task_result
            )
        )

        add_task(
            next_task
        )

        update_handoff(
            f"""
Goal: {current_goal}
Milestone: {current_milestone}
Mode: {current_mode}
Workflow: {current_workflow}

Last Completed Task:

{task}

Next Recommended Task:

{next_task}
"""
        )

    duration = (
        time.time()
        - start_time
    )

    record_workflow(
        task=task,
        success=success,
        duration=duration,
        goal=current_goal,
        mode=current_mode,
        provider=current_provider,
        strategy=current_strategy,
        workflow=current_workflow,
        complexity=complexity
    )

    print("STEP: PULL REQUEST")

    pull_request = (
        generate_pull_request(
            task,
            plan_result,
            review_result
        )
    )

    print("WORKFLOW COMPLETE")

    mark_task_success(task)
    clear_current_task()

    return {
        "task": task,
        "success": success,
        "goal": current_goal,
        "director_mode": current_mode,
        "milestone": current_milestone,
        "provider": current_provider,
        "strategy": current_strategy,
        "workflow": current_workflow,
        "subtasks": subtasks,
        "plan": plan_result,
        "research": research_result,
        "architecture": architecture_result,
        "code": code_result,
        "review": review_result,
        "next_task": next_task,
        "duration": duration,
        "pull_request": pull_request,
    }