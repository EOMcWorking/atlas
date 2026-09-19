from pathlib import Path


FAILED_FILE = Path("FAILED_TASKS.md")


def record_failure(
    task: str,
    error: str
):

    with open(
        FAILED_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\nTASK: {task}\n"
            f"ERROR: {error}\n"
            f"{'-'*40}\n"
        )