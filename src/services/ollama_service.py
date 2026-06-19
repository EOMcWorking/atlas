from pathlib import Path

from src.providers.provider_router import get_provider_chain

from src.services.model_router import get_model



def chat(
    prompt: str,
    task_type: str = "general"
):
    from src.services.memory_service import (
        get_relevant_context
    )

    model = get_model(task_type)

    context = get_relevant_context(
        prompt
    )

    enhanced_prompt = f"""
Atlas Memory:

{chr(10).join(context)}

User Request:

{prompt}
"""

    for provider in get_provider_chain():

        try:
            return provider.chat(
                enhanced_prompt,
                model
            )

        except Exception as e:
            print(
                f"Provider failed: {e}"
            )

            continue

    raise Exception(
        "No provider available"
    )


def suggest_next_task():
    tasks = Path(
        "TASKS.md"
    ).read_text(
        encoding="utf-8"
    )

    decisions = Path(
        "DECISIONS.md"
    ).read_text(
        encoding="utf-8"
    )

    handoff = Path(
        "HANDOFF.md"
    ).read_text(
        encoding="utf-8"
    )

    prompt = f"""
You are Atlas.

Project Tasks:
{tasks}

Decisions:
{decisions}

Handoff:
{handoff}

Suggest the single most important next development task.
"""

    return chat(
        prompt,
        task_type="planning"
    )