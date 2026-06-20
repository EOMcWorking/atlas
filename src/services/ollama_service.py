from pathlib import Path

from src.providers.provider_router import (
    get_provider_chain
)

from src.services.context_builder import (
    build_context
)

from src.services.model_router import (
    get_model
)

from src.services.provider_metrics_service import (
    record_success,
    record_failure
)


def chat(
    prompt: str,
    task_type: str = "general"
):

    model = get_model(
        task_type
    )

    enhanced_prompt = prompt

    if task_type in [
        "review",
        "planning"
    ]:

        enhanced_prompt = (
            build_context(
                prompt
            )
        )

    for provider in get_provider_chain(task_type):

        provider_name = (
            provider.__class__.__name__
        )

        print(
            f"Trying provider: {provider_name}"
        )

        try:

            response = provider.chat(
                enhanced_prompt,
                model
            )

            print(
                f"SUCCESS: {provider_name}"
            )

            record_success(
                provider_name
            )

            return response

        except Exception as e:

            print(
                f"FAILED: {provider_name}"
            )

            record_failure(
                provider_name
            )

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