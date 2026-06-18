from pathlib import Path

PROJECT_FILE = Path("PROJECT.md")
TASKS_FILE = Path("TASKS.md")
DECISIONS_FILE = Path("DECISIONS.md")
HANDOFF_FILE = Path("HANDOFF.md")


def append_to_file(file_path: Path, text: str):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n{text}\n")


def read_file(file_path: Path):
    if not file_path.exists():
        return ""

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()