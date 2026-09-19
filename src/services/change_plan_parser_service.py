import re


def extract_plan_files(
    plan: str
):

    matches = re.findall(
        r"src/[a-zA-Z0-9_/\-.]+\.py",
        plan
    )

    return list(
        dict.fromkeys(
            matches
        )
    )