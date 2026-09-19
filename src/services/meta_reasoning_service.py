from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.workflow_metrics_service import (
    get_workflow_metrics
)

from src.services.ollama_service import (
    chat
)

from src.services.self_improvement_board_service import (
    add_improvement
)


def build_meta_context():

    failures = (
        analyze_failures()
    )

    metrics = (
        get_workflow_metrics()
    )

    return {

        "failures":
        failures,

        "metrics":
        metrics
    }


def analyze_reasoning():

    context = (
        build_meta_context()
    )

    prompt = f"""
You are Atlas Meta Reasoner.

SYSTEM DATA:

{context}

Analyze:

1. Recurring mistakes
2. Weak strategies
3. Repeated failures
4. Recommended improvements

Return concise output.
"""

    return chat(
        prompt,
        task_type="analysis"
    )


def generate_lessons():

    analysis = (
        analyze_reasoning()
    )

    # When recurring issues are discovered, log them to the improvement board
    _extract_and_log_improvements(analysis)

    return {

        "analysis":
        analysis
    }


def get_meta_reasoning_report():

    return {

        "report":
        generate_lessons()
    }


def _extract_and_log_improvements(analysis: str):
    """
    Parse the meta-analysis output for recurring issues
    and log each as an improvement on the board.
    """
    lines = analysis.strip().splitlines()

    current_title = None
    current_reason = None

    for line in lines:
        line = line.strip()

        # Look for lines that suggest an improvement
        # Matches patterns like:
        #   "Improvement: Add retry logic"
        #   "Recommended: Better error handling"
        #   "Fix: Review false positives"
        if line.lower().startswith("improvement:"):
            current_title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("recommended:"):
            current_title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("fix:"):
            current_title = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reason:") and current_title:
            current_reason = line.split(":", 1)[1].strip()
        elif line.lower().startswith("priority:") and current_title:
            try:
                priority = int(line.split(":", 1)[1].strip())
            except ValueError:
                priority = 5

            add_improvement(
                title=current_title,
                reason=current_reason or "Recurring issue detected by meta-analysis",
                priority=priority
            )

            # Reset for next improvement
            current_title = None
            current_reason = None

    # If we reached the end with a pending title but no priority line,
    # still log it with default priority
    if current_title:
        add_improvement(
            title=current_title,
            reason=current_reason or "Recurring issue detected by meta-analysis",
            priority=5
        )