from src.services.service_dependency_map_service import (
    get_orphan_services
)

from src.services.large_file_service import (
    find_large_files
)

from src.services.ollama_service import (
    chat
)


def generate_self_refactor_plan():

    orphan_services = (
        get_orphan_services()
    )

    large_files = (
        find_large_files()
    )

    prompt = f"""
You are Atlas Self Refactor Agent.

ORPHAN SERVICES:

{orphan_services}

LARGE FILES:

{large_files}

Generate:

1. Services that could be removed
2. Services that should be merged
3. Files that should be split
4. Risks
5. Recommended order

Do NOT assume code.
Use only evidence provided.
"""

    return chat(
        prompt,
        task_type="planning"
    )

def extract_refactor_tasks():

    plan = (
        generate_self_refactor_plan()
    )

    tasks = []

    for line in plan.splitlines():

        line = line.strip()

        if len(line) < 10:
            continue

        tasks.append(
            line
        )

    return tasks

def requires_human_review():

    return True