def provider_available(provider):

    try:

        provider.health_check()

        return True

    except Exception:

        return False