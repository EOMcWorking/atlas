from src.services.strategy_memory_service import (
    get_strategy_memory_report
)

from src.services.autonomous_benchmark_service import (
    get_benchmark_report
)

from src.services.ollama_service import (
    chat
)

def build_meta_learning_context():

    return {

        "strategies":
        get_strategy_memory_report(),

        "benchmarks":
        get_benchmark_report()
    }

def analyze_learning_patterns():

    context = (
        build_meta_learning_context()
    )

    prompt = f"""
Atlas Meta Learning Analysis

DATA:

{context}

Determine:

1. What learning approaches work best
2. What learning approaches fail
3. What Atlas should do more often
4. What Atlas should avoid

Return concise output.
"""

    return chat(
        prompt,
        task_type="analysis"
    )

def generate_meta_lessons():

    analysis = (
        analyze_learning_patterns()
    )

    lessons = []

    for line in analysis.splitlines():

        text = line.strip()

        if len(text) > 10:

            lessons.append(
                text
            )

    return lessons

def get_meta_learning_report():

    return {

        "analysis":
        analyze_learning_patterns(),

        "lessons":
        generate_meta_lessons()
    }