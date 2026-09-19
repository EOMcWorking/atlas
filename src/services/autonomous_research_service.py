from src.services.ollama_service import (
    chat
)

from src.services.self_improvement_board_service import (
    add_improvement
)

from src.services.root_cause_analysis_service import (
    get_root_cause_summary
)

from src.services.meta_learning_service import (
    get_meta_learning_report
)


def discover_research_topics():

    root_causes = (
        get_root_cause_summary()
    )

    learning_report = (
        get_meta_learning_report()
    )

    prompt = f"""
Atlas Root Cause Report:

{root_causes}

Learning History:
{learning_report}

Identify:

1. Knowledge gaps
2. Missing capabilities
3. Research opportunities
4. Areas where Atlas has improved
5. Areas needing more exploration

Return concise list.
"""

    result = chat(
        prompt,
        task_type="analysis"
    )

    return result


def perform_research():

    topics = (
        discover_research_topics()
    )

    prompt = f"""
Research Topics:

{topics}

Generate:

1. Findings
2. Recommendations
3. New capabilities Atlas could gain

Return concise output.
"""

    return chat(
        prompt,
        task_type="research"
    )


def create_research_improvements():

    findings = (
        perform_research()
    )

    for line in findings.splitlines():

        text = line.strip()

        if len(text) > 20:

            try:

                add_improvement(

                    title=text[:100],

                    description=text,

                    priority=7
                )

            except Exception:
                pass

    return findings


def get_research_report():

    findings = (
        perform_research()
    )

    return {

        "success": True,

        "findings":
        findings
    }