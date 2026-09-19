import re


def extract_planner_files(
    planner_output: str
):

    files = []

    matches = re.findall(
        r"(src/[A-Za-z0-9_/\-\.]+\.py)",
        planner_output
    )

    for match in matches:

        if match not in files:
            files.append(match)

    return files