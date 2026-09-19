def estimate_runtime(complexity):

    if complexity == "SIMPLE":
        return {
            "calls": 2,
            "runtime": "10-30 sec"
        }

    if complexity == "MEDIUM":
        return {
            "calls": 6,
            "runtime": "1-3 min"
        }

    return {
        "calls": 12,
        "runtime": "5-15 min"
    }