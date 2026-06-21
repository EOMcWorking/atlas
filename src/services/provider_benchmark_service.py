import time

from src.providers.provider_registry import (
    providers
)

from src.services.provider_metrics_service import (
    record_success,
    record_failure,
    record_latency
)


BENCHMARK_PROMPT = """
Reply with exactly:
ATLAS_OK
"""


def benchmark_providers():

    results = {}

    for name, provider in providers.items():

        try:

            start = time.time()

            response = provider.chat(
                BENCHMARK_PROMPT,
                "general"
            )

            latency = (
                time.time()
                - start
            )

            record_success(name)

            record_latency(
                name,
                latency
            )

            results[name] = {
                "success": True,
                "latency": latency
            }

        except Exception:

            record_failure(name)

            results[name] = {
                "success": False
            }

    return results