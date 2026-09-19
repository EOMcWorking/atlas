from pathlib import Path


def write_file(
    filepath: str,
    content: str
):

    Path(filepath).write_text(
        content,
        encoding="utf-8"
    )