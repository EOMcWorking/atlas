from pathlib import Path


def get_recent_decisions(
    limit: int = 10
):

    path = Path(
        "DECISIONS.md"
    )

    if not path.exists():
        return ""

    text = path.read_text(
        encoding="utf-8"
    )

    lines = [
        line
        for line in text.splitlines()
        if line.strip()
    ]

    return "\n".join(
        lines[-limit:]
    )