from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.ollama_service import (
    chat
)

from src.services.execution_trace_service import (
    get_recent_traces
)


def analyze_root_cause():

    failures = (
        analyze_failures()
    )

    if (
        failures[
            "total_failures"
        ] == 0
    ):

        return {
            "success": True,
            "analysis":
            "No failures found.",
            "priority_fix": None
        }

    # Add execution traces for stronger RCA
    traces = get_recent_traces(100)

    prompt = f"""
You are Atlas RCA Agent.

FAILURE DATA:

{failures}

EXECUTION TRACES:

{traces}

Determine:

1. Most likely causes
2. Repeated patterns
3. Preventative actions
4. Highest priority fix

Return concise output.
"""

    result = chat(
        prompt,
        task_type="planning"
    )

    # Extract highest priority fix from the analysis
    priority_fix = _extract_priority_fix(result)

    return {
        "success": True,
        "analysis": result,
        "priority_fix": priority_fix
    }


def get_root_cause_summary():

    result = (
        analyze_root_cause()
    )

    return result[
        "analysis"
    ]


def extract_prevention_actions(
    analysis: str = None
):
    """
    Extract prevention actions from RCA analysis.
    
    If no analysis is provided, generates one first.
    This avoids duplicate LLM calls when the analysis
    is already available.
    """

    if analysis is None:
        result = analyze_root_cause()
        analysis = result["analysis"]

    actions = []

    for line in analysis.splitlines():

        if (
            "prevent"
            in line.lower()
            or
            "fix"
            in line.lower()
            or
            "action"
            in line.lower()
        ):

            actions.append(
                line.strip()
            )

    return actions


def get_priority_fix(
    analysis: str = None
):
    """
    Extract the highest priority fix from RCA analysis.
    
    Useful for self_improvement_board_service,
    improvement_scheduler_service, and
    project_evolution_service.
    """

    if analysis is None:
        result = analyze_root_cause()
        return result.get("priority_fix")

    return _extract_priority_fix(analysis)


def _extract_priority_fix(analysis: str):
    """
    Parse the analysis text to find the highest priority fix.
    Looks for explicit markers or falls back to heuristics.
    """

    lines = analysis.splitlines()

    # First, look for an explicit "Highest priority fix:" line
    for i, line in enumerate(lines):
        line_lower = line.strip().lower()
        if "highest priority fix" in line_lower:
            # Return this line and the next non-empty line
            if line.strip().startswith(("Highest", "highest")):
                # Try to get the value after the colon
                if ":" in line:
                    return line.split(":", 1)[1].strip()
            # Otherwise return the next line
            if i + 1 < len(lines) and lines[i + 1].strip():
                return lines[i + 1].strip()
            return line.strip()

    # Fallback: look for lines with priority indicators
    for line in lines:
        line_lower = line.strip().lower()
        if (
            ("fix" in line_lower or "action" in line_lower)
            and ("high" in line_lower or "priority" in line_lower or "critical" in line_lower)
        ):
            return line.strip()

    # Last resort: return the first actionable line
    for line in lines:
        line_lower = line.strip().lower()
        if any(
            keyword in line_lower
            for keyword in ["fix:", "action:", "recommend:", "prevent:"]
        ):
            return line.strip()

    return None