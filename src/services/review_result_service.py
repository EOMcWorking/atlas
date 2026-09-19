import re


def get_review_verdict(
    review_result: str
):

    text = review_result.upper()

    if re.search(
        r"VERDICT\s*:\s*APPROVED",
        text
    ):
        return "APPROVED"

    if re.search(
        r"VERDICT\s*:\s*REJECTED",
        text
    ):
        return "REJECTED"

    return "UNKNOWN"