from pathlib import Path

from src.services.project_paths_service import (
    get_project_file
)
from src.services.workspace_service import (
    get_docs_path
)


def get_docs_file(
    filename: str
):
    return Path(
        get_docs_path()
    ) / filename


def get_decisions_file(
    project_name: str = None
):

    if project_name is None:
        return get_docs_file(
            "DECISIONS.md"
        )

    return Path(
        get_project_file(
            project_name,
            "DECISIONS.md"
        )
    )


def get_memory_file(
    project_name: str = None
):

    if project_name is None:
        return get_docs_file(
            "MEMORY.md"
        )

    return Path(
        get_project_file(
            project_name,
            "MEMORY.md"
        )
    )


def get_handoff_file(
    project_name: str = None
):

    if project_name is None:
        return get_docs_file(
            "HANDOFF.md"
        )

    return Path(
        get_project_file(
            project_name,
            "HANDOFF.md"
        )
    )


def append_to_file(
    file_path: Path,
    text: str
):
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        file_path,
        "a",
        encoding="utf-8"
    ) as f:
        f.write(
            f"\n{text}\n"
        )


def read_file(
    file_path: Path
):

    if not file_path.exists():
        return ""

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:
        return f.read()


def search_decisions(
    query: str,
    project_name: str = None
):
    """
    Exact lookup in DECISIONS.md only.
    """

    content = read_file(
        get_decisions_file(
            project_name
        )
    )

    matches = []

    for line in content.splitlines():

        if query.lower() in line.lower():
            matches.append(line)

    return matches


def get_relevant_context(
    query: str,
    limit: int = 10,
    project_name: str = None
):
    """
    Search across DECISIONS.md, MEMORY.md,
    and HANDOFF.md.
    """

    sources = [
        read_file(
            get_decisions_file(
                project_name
            )
        ),
        read_file(
            get_memory_file(
                project_name
            )
        ),
        read_file(
            get_handoff_file(
                project_name
            )
        ),
    ]

    all_matches = []

    query_words = query.lower().split()

    for source_content in sources:

        for line in source_content.splitlines():

            line_lower = line.lower()

            score = 0

            for word in query_words:

                if word in line_lower:
                    score += 1

            if score > 0:
                all_matches.append(
                    (
                        score,
                        line
                    )
                )

    all_matches.sort(
        reverse=True
    )

    return [
        line
        for score, line
        in all_matches[:limit]
    ]


def save_memory(
    text: str,
    project_name: str = None
):
    """
    Append to MEMORY.md.
    """

    memory_file = get_memory_file(
        project_name
    )

    append_to_file(
        memory_file,
        text
    )


def summarize_decisions(
    project_name: str = None
):

    from src.services.ollama_service import (
        chat
    )

    content = read_file(
        get_decisions_file(
            project_name
        )
    )

    prompt = f"""
You are Atlas memory manager.

Summarize the following project decisions.

Keep:
- Important architectural decisions
- Model choices
- Major project direction

Remove:
- Repetition
- Minor details

DECISIONS:

{content}
"""

    return chat(
        prompt,
        task_type="planning"
    )