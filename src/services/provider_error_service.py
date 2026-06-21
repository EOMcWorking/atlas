def get_cooldown_seconds(
    error: Exception
):

    text = str(error).lower()

    if "rate limit" in text:
        return 300

    if "timeout" in text:
        return 60

    if "connection" in text:
        return 120

    if "network" in text:
        return 120

    if "api key" in text:
        return 3600

    if "unauthorized" in text:
        return 3600

    return 300