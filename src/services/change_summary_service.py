from pathlib import Path


def summarize_changes(
    before: str,
    after: str,
    target_file: str
):

    before_lines = before.splitlines()
    after_lines = after.splitlines()

    added = max(
        0,
        len(after_lines)
        - len(before_lines)
    )

    removed = max(
        0,
        len(before_lines)
        - len(after_lines)
    )

    return {
        "file": target_file,
        "lines_before": len(before_lines),
        "lines_after": len(after_lines),
        "lines_added": added,
        "lines_removed": removed
    }