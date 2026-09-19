from src.services.architecture_review_service import (
    review_architecture
)

from src.services.technical_debt_service import (
    calculate_technical_debt
)

from src.services.dead_code_service import (
    find_dead_code
)

from src.services.large_file_service import (
    find_large_files
)

from src.services.circular_dependency_service import (
    find_circular_dependencies
)

from src.services.ollama_service import (
    chat
)

from src.services.self_improvement_board_service import (
    add_improvement
)

from src.services.predictive_risk_service import (
    get_risk_summary
)

from src.services.autonomous_benchmark_service import (
    get_benchmark_report
)

from src.services.evolution_scoring_service import (
    get_evolution_report
)


def generate_project_evolution():

    architecture = (
        review_architecture()
    )

    debt = (
        calculate_technical_debt()
    )

    dead_code = (
        find_dead_code()
    )

    large_files = (
        find_large_files()
    )

    circular = (
        find_circular_dependencies()
    )

    risk_summary = get_risk_summary()

    benchmark_report = get_benchmark_report()

    evolution_report = get_evolution_report()

    prompt = f"""
You are Atlas Strategist.

ARCHITECTURE REVIEW:
{architecture}

TECHNICAL DEBT:
{debt}

DEAD CODE:
{dead_code}

LARGE FILES:
{large_files}

CIRCULAR DEPENDENCIES:
{circular}

PREDICTIVE RISK ANALYSIS:
{risk_summary}

BENCHMARK TRENDS:
{benchmark_report}

EVOLUTION SCORE: {evolution_report['score']}
EVOLUTION GRADE: {evolution_report['grade']}

Generate:

1. Top 5 priorities
2. Estimated impact
3. Recommended order
4. Risks if ignored
5. Only use provided evidence.
6. Do not assume tools exist.
7. Do not assume project purpose.
8. If evidence is missing, say: "Insufficient evidence."

Return concise output.
"""

    result = chat(
        prompt,
        task_type="planning"
    )

    # Log technical debt findings to the improvement board
    _log_evolution_improvements(
        debt,
        dead_code,
        large_files,
        circular
    )

    # Log predictive risk findings to the improvement board
    _log_risk_improvements(risk_summary)

    # Log evolution score to improvement board if negative
    _log_evolution_score(evolution_report)

    return result


def _log_evolution_improvements(debt, dead_code, large_files, circular):
    """
    Parse project health findings and log actionable improvements.
    """

    # Technical debt findings
    if debt:
        debt_str = str(debt)
        if "high" in debt_str.lower() or "critical" in debt_str.lower():
            add_improvement(
                title="Address critical technical debt",
                reason=f"Technical debt analysis: {debt_str[:200]}",
                priority=8
            )
        elif "medium" in debt_str.lower():
            add_improvement(
                title="Reduce medium-level technical debt",
                reason=f"Technical debt analysis: {debt_str[:200]}",
                priority=5
            )

    # Dead code findings
    if dead_code:
        dead_str = str(dead_code)
        dead_count = _count_items(dead_code)

        if dead_count > 0:
            add_improvement(
                title=f"Remove {dead_count} dead code files/functions",
                reason=f"Dead code detected: {dead_str[:200]}",
                priority=min(dead_count + 2, 8)
            )

    # Large file findings
    if large_files:
        large_str = str(large_files)
        large_count = _count_items(large_files)

        if large_count > 0:
            priority = 7 if large_count > 5 else 4
            add_improvement(
                title=f"Refactor {large_count} oversized files",
                reason=f"Large files detected: {large_str[:200]}",
                priority=priority
            )

    # Circular dependency findings
    if circular:
        circular_str = str(circular)
        circular_count = _count_items(circular)

        if circular_count > 0:
            add_improvement(
                title=f"Resolve {circular_count} circular dependencies",
                reason=f"Circular dependencies detected: {circular_str[:200]}",
                priority=min(circular_count + 5, 10)
            )


def _log_risk_improvements(risk_summary: str):
    """
    Parse predictive risk analysis and log prevention actions.
    """
    for line in risk_summary.splitlines():
        text = line.strip().lower()

        # Look for prevention/mitigation recommendations
        if any(keyword in text for keyword in ["prevent:", "mitigate:", "action:", "recommend:"]):
            # Extract the action part after the colon
            if ":" in line:
                action = line.split(":", 1)[1].strip()
                add_improvement(
                    title=action[:100],
                    reason=f"Predictive risk analysis: {line.strip()[:200]}",
                    priority=7
                )

        # Catch high-risk predictions
        elif any(keyword in text for keyword in ["high risk", "critical risk", "likely failure"]):
            add_improvement(
                title=f"Mitigate predicted risk: {line.strip()[:100]}",
                reason=f"Predictive risk flagged: {line.strip()[:200]}",
                priority=9
            )


def _log_evolution_score(evolution_report: dict):
    """
    Log improvement if evolution score is negative.
    """
    score = evolution_report.get("score", 0)
    grade = evolution_report.get("grade", "NEUTRAL")

    if grade == "NEGATIVE":
        add_improvement(
            title="Reverse negative evolution trend",
            reason=f"Evolution score is {score}. Success rate or runtime has degraded.",
            priority=9
        )
    elif grade == "NEUTRAL":
        add_improvement(
            title="Boost stagnant evolution",
            reason=f"Evolution score is {score}. No improvement detected between benchmarks.",
            priority=5
        )


def _count_items(data):
    """
    Count items in various data structures.
    """
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        return len(data)
    if isinstance(data, str) and data.strip():
        # Count non-empty lines as a rough estimate
        return len([line for line in data.splitlines() if line.strip()])
    return 0