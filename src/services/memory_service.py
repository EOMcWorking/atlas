from pathlib import Path
from src.services.ollama_service import chat

PROJECT_FILE = Path("PROJECT.md")
TASKS_FILE = Path("TASKS.md")
DECISIONS_FILE = Path("DECISIONS.md")
HANDOFF_FILE = Path("HANDOFF.md")
MEMORY_FILE = Path("MEMORY.md")

def search_decisions(query: str):
    content = read_file(
        DECISIONS_FILE
    )

    matches = []

    for line in content.splitlines():
        if query.lower() in line.lower():
            matches.append(line)

    return matches

def append_to_file(file_path: Path, text: str):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"\n{text}\n")


def read_file(file_path: Path):
    if not file_path.exists():
        return ""

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
    
def summarize_decisions():
    content = read_file(
        DECISIONS_FILE
    )

    prompt = f"""
You are Atlas memory manager.

Summarize the following project decisions.

Keep:
- Important architectural decisions
- Model choices
- Major project direction

Remove:
- Repetition
- Minor details

DECISIONS:

{content}
"""
def get_relevant_context(
    query: str,
    limit: int = 10
):
    content = read_file(
        DECISIONS_FILE
    )

    matches = []

    query_words = query.lower().split()

    for line in content.splitlines():

        line_lower = line.lower()

        score = 0

        for word in query_words:
            if word in line_lower:
                score += 1

        if score > 0:
            matches.append(
                (score, line)
    )
    matches.sort(
            reverse=True
    )

    return [
        line
        for score, line
        in matches[:limit]
    ]

    return chat(
        prompt,
        task_type="planning"
    )