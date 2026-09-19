import re


def extract_winner(
    vote_result: str
):

    match = re.search(
        r"WINNER\s*:\s*(.*)",
        vote_result,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return "UNKNOWN"