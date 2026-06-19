from pathlib import Path

from src.services.project_context_service import (
    get_project_files
)


LARGE_FILE_LINES = 200


def find_large_files():

    large_files = []

    for file in get_project_files():

        try:

            content = file.read_text(
                encoding="utf-8"
            )

            line_count = len(
                content.splitlines()
            )

            if (
                line_count
                >= LARGE_FILE_LINES
            ):

                large_files.append(
                    {
                        "file": str(file),
                        "lines": line_count
                    }
                )

        except Exception:
            continue

    large_files.sort(
        key=lambda x: x["lines"],
        reverse=True
    )

    return {
        "threshold": LARGE_FILE_LINES,
        "large_files": large_files
    }