import time


def retry_provider_call(
    provider,
    prompt,
    model,
    retries: int = 2
):

    last_error = None

    for attempt in range(
        retries + 1
    ):

        try:

            return provider.chat(
                prompt,
                model
            )

        except Exception as e:

            last_error = e

            if attempt < retries:

                time.sleep(
                    2 * (
                        attempt + 1
                    )
                )

    raise last_error