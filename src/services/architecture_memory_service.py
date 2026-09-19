from pathlib import Path


ARCHITECTURE_MEMORY = Path(
    "ARCHITECTURE_MEMORY.md"
)


def record_architecture_decision(
    title: str,
    reason: str,
    impact: str
):

    with open(
        ARCHITECTURE_MEMORY,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n# {title}\n\n"
            f"REASON:\n{reason}\n\n"
            f"IMPACT:\n{impact}\n\n"
        )


def get_architecture_memory():

    if not ARCHITECTURE_MEMORY.exists():
        return ""

    return ARCHITECTURE_MEMORY.read_text(
        encoding="utf-8"
    )


def search_architecture_memory(
    query: str
):

    if not ARCHITECTURE_MEMORY.exists():
        return []

    content = (
        ARCHITECTURE_MEMORY
        .read_text(
            encoding="utf-8"
        )
    )

    matches = []

    for section in content.split("#"):

        if query.lower() in section.lower():
            matches.append(section)

    return matches[:10]