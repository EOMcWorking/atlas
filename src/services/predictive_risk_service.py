from src.services.execution_trace_service import (
    get_recent_traces
)

from src.services.failure_analysis_service import (
    analyze_failures
)

from src.services.ollama_service import (
    chat
)

def build_risk_context():

    traces = (
        get_recent_traces(
            100
        )
    )

    failures = (
        analyze_failures()
    )

    return {

        "traces":
        traces,

        "failures":
        failures
    }

def predict_risks():

    context = (
        build_risk_context()
    )

    prompt = f"""
You are Atlas Predictive Risk Analyzer.

SYSTEM DATA:

{context}

Predict:

1. Likely future failures
2. Architectural risks
3. Workflow risks
4. Strategy risks
5. Recommended prevention actions

Return concise output.
"""

    result = chat(
        prompt,
        task_type="analysis"
    )

    return {

        "success": True,

        "prediction":
        result
    }

def get_risk_summary():

    result = (
        predict_risks()
    )

    return result[
        "prediction"
    ]

def extract_prevention_actions():

    summary = (
        get_risk_summary()
    )

    actions = []

    for line in summary.splitlines():

        text = line.lower()

        if (

            "prevent"
            in text

            or

            "mitigate"
            in text

            or

            "reduce"
            in text

        ):

            actions.append(
                line.strip()
            )

    return actions
