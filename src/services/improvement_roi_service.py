from src.services.ollama_service import (
    chat
)

def analyze_improvement(
    title: str,
    reason: str
):

    prompt = f"""
You are Atlas ROI Evaluator.

Improvement:

{title}

Reason:

{reason}

Estimate:

1. Impact (1-10)
2. Effort (1-10)
3. Risk (1-10)

Return concise output.
"""

    return chat(
        prompt,
        task_type="analysis"
    )

def extract_score(
    text: str,
    keyword: str
):

    lines = text.splitlines()

    for line in lines:

        if keyword.lower() in (
            line.lower()
        ):

            digits = [

                c

                for c in line

                if c.isdigit()
            ]

            if digits:

                return int(
                    digits[0]
                )

    return 5

def calculate_roi(
    impact,
    effort,
    risk
):

    return (

        impact * 10

        - effort * 5

        - risk * 3
    )

def evaluate_improvement(
    title,
    reason
):

    analysis = (
        analyze_improvement(
            title,
            reason
        )
    )

    impact = (
        extract_score(
            analysis,
            "impact"
        )
    )

    effort = (
        extract_score(
            analysis,
            "effort"
        )
    )

    risk = (
        extract_score(
            analysis,
            "risk"
        )
    )

    roi = (
        calculate_roi(
            impact,
            effort,
            risk
        )
    )

    return {

        "impact":
        impact,

        "effort":
        effort,

        "risk":
        risk,

        "roi":
        roi,

        "analysis":
        analysis
    }