import re


def parse_subtasks(text: str):

    subtasks = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if re.match(r"^\d+\.", line):
            subtasks.append(line)

    return subtasks[:3]