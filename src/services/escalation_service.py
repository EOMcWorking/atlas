from pathlib import Path


ESCALATION_FILE = Path(
    "HUMAN_REVIEW.md"
)


def escalate_task(
    task: str,
    reason: str
):

    with open(
        ESCALATION_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            f"\n# TASK\n{task}\n\n"
            f"## REASON\n{reason}\n\n"
            f"{'-'*50}\n"
        )