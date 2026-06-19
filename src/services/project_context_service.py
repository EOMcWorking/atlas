from pathlib import Path

PROJECT_EXTENSIONS = [
    ".py",
    ".md"
]


def get_project_files():
    files = []

    for extension in PROJECT_EXTENSIONS:
        files.extend(
            Path("src").rglob(
                f"*{extension}"
            )
        )

    root_docs = [
        "PROJECT.md",
        "TASKS.md",
        "DECISIONS.md",
        "MEMORY.md",
        "HANDOFF.md",
        "ROADMAP.md"
    ]

    for doc in root_docs:
        path = Path(doc)

        if path.exists():
            files.append(path)

    return files


def build_project_context(
    max_chars: int = 20000
):
    context_parts = []
    total_chars = 0

    for file in get_project_files():

        try:
            content = file.read_text(
                encoding="utf-8"
            )

            file_block = (
                f"\n\nFILE: {file}\n"
                f"{content}\n"
            )

            if (
                total_chars
                + len(file_block)
                > max_chars
            ):
                break

            context_parts.append(
                file_block
            )

            total_chars += len(
                file_block
            )

        except Exception:
            continue

    return "".join(
        context_parts
    )


def get_project_stats():
    files = get_project_files()

    total_chars = 0

    for file in files:

        try:
            total_chars += len(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            pass

    return {
        "files": len(files),
        "characters": total_chars
    }