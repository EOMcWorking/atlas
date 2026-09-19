import re


def extract_files_from_plan(
    plan: str
):

    files = []

    for line in plan.splitlines():

        line = line.strip()

        if (
            "src/" in line
            and ".py" in line
        ):

            match = re.search(
                r"(src/[a-zA-Z0-9_/\-.]+\.py)",
                line
            )

            if match:
                files.append(
                    match.group(1)
                )

    return list(
        dict.fromkeys(files)
    )