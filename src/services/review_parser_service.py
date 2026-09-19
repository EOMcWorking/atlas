import re


def review_passed(
    review_result: str
):

    text = review_result.upper()

    approved = re.search(
        r"VERDICT\s*:\s*APPROVED",
        text
    )

    rejected = re.search(
        r"VERDICT\s*:\s*REJECTED",
        text
    )

    if approved:
        return True

    if rejected:
        return False

    return False