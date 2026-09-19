from pathlib import Path
import re


def find_related_files(
    target_file: str
):

    related = []

    target_name = (
        Path(target_file)
        .stem
    )

    for path in Path(
        "src"
    ).rglob("*.py"):

        if str(path) == target_file:
            continue

        try:

            content = path.read_text(
                encoding="utf-8"
            )

            if (
                target_name in content
            ):
                related.append(
                    str(path)
                )

        except Exception:
            pass

    return related[:20]