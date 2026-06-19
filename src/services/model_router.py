from src.core.config import MODELS

MODELS = {
    "coding": "qwen2.5-coder:7b",
    "review": "deepseek-coder:6.7b",
    "planning": "qwen2.5-coder:1.5b",
    "general": "qwen2.5-coder:7b",
    "fast": "qwen2.5-coder:1.5b",
}


def get_model(task_type: str):
    return MODELS.get(
        task_type,
        MODELS["general"]
    )