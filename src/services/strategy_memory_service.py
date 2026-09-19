import json
from pathlib import Path

from src.services.workspace_service import get_memory_path


def get_strategy_memory_file():
    """
    Return the strategy memory file inside the configured
    Atlas memory directory.
    """
    memory_path = Path(get_memory_path())
    memory_path.mkdir(
        parents=True,
        exist_ok=True
    )

    return memory_path / "strategy_memory.json"


def load_strategy_memory():

    memory_file = get_strategy_memory_file()

    if not memory_file.exists():

        return []

    try:
        data = json.loads(
            memory_file.read_text(
                encoding="utf-8"
            )
        )

        if not isinstance(data, list):
            return []

        return data

    except (json.JSONDecodeError, OSError):
        return []


def save_strategy_memory(data):

    memory_file = get_strategy_memory_file()

    memory_file.write_text(
        json.dumps(
            data,
            indent=2
        ),
        encoding="utf-8"
    )


def remember_strategy(
    name: str,
    score: float,
    notes: str = ""
):

    memory = load_strategy_memory()

    memory.append({
        "name": name,
        "score": score,
        "notes": notes
    })

    save_strategy_memory(memory)


def get_best_strategies():

    memory = load_strategy_memory()

    memory.sort(
        key=lambda x: x.get(
            "score",
            0
        ),
        reverse=True
    )

    return memory[:10]


def get_worst_strategies():

    memory = load_strategy_memory()

    memory.sort(
        key=lambda x: x.get(
            "score",
            0
        )
    )

    return memory[:10]


def get_strategy_memory_report():

    return {
        "best": get_best_strategies(),
        "worst": get_worst_strategies()
    }