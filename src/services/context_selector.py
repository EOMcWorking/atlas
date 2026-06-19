from pathlib import Path

from src.services.project_context_service import (
    get_project_files
)


def find_relevant_files(
    query: str,
    limit: int = 10
):
    query_words = (
        query.lower().split()
    )

    matches = []

    for file in get_project_files():

        try:
            content = file.read_text(
                encoding="utf-8"
            )

            score = 0

            file_text = (
                str(file).lower()
                + "\n"
                + content.lower()
            )

            for word in query_words:

                if word in file_text:
                    score += 1

            if score > 0:
                matches.append(
                    (score, file)
                )

        except Exception:
            continue

    matches.sort(
        reverse=True
    )

    return [
        file
        for score, file
        in matches[:limit]
    ]


def build_targeted_context(
    query: str,
    max_chars: int = 15000
):
    files = find_relevant_files(
        query
    )

    context = []
    total_chars = 0

    for file in files:

        try:
            content = file.read_text(
                encoding="utf-8"
            )

            block = (
                f"\nFILE: {file}\n"
                f"{content}\n"
            )

            if (
                total_chars
                + len(block)
                > max_chars
            ):
                break

            context.append(
                block
            )

            total_chars += len(
                block
            )

        except Exception:
            pass

    return "".join(
        context
    )