from pathlib import Path
import time

from src.providers.provider_router import (
    get_provider_chain
)

from src.services.context_builder import (
    build_context
)

from src.services.model_selection_service import (
    get_model_for_provider
)

from src.services.provider_metrics_service import (
    record_success,
    record_failure,
    record_latency
)

from src.services.provider_cooldown_service import (
    put_on_cooldown
)

from src.services.provider_task_metrics_service import (
    record_task_success,
    record_task_failure
)

from src.services.provider_error_service import (
    get_cooldown_seconds
)

from src.services.provider_retry_service import (
    retry_provider_call
)

def chat(
    prompt: str,
    task_type: str = "general"
):

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

        provider_key = (
            provider_name
            .replace(
                "Provider",
                ""
            )
            .lower()
        )

        model = get_model_for_provider(
            provider_key,
            task_type
        )

        print(
            f"Trying provider: {provider_name}"
        )

        try:

            start = time.time()

            response = retry_provider_call(
                provider,
                enhanced_prompt,
                model
            )

            latency = (
                time.time()
                - start
            )

            record_latency(
                provider_name,
                latency
            )

            record_success(
                provider_name
            )

            record_task_success(
                task_type,
                provider_key
            )

            print(
                f"SUCCESS: {provider_name}"
            )

            return response

        except Exception as e:

            cooldown = get_cooldown_seconds(e)

            put_on_cooldown(
                provider_name,
                cooldown
            )

            put_on_cooldown(
                provider_name,
                cooldown
            )

            record_failure(
                provider_name
            )

            record_task_failure(
                task_type,
                provider_key
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