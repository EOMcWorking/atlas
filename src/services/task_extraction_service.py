import re


def extract_task(
    task_text: str
):

    lines = [
        line.strip()
        for line in task_text.splitlines()
        if line.strip()
    ]

    for line in lines:

        line = re.sub(
            r"^[0-9\-\*\.\)]*\s*",
            "",
            line
        )

        if len(line) > 10:
            return line

    return None