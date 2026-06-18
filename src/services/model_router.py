from src.core.config import MODELS

def get_model(task_type: str) -> str:
    return MODELS.get(
        task_type,
        MODELS["general"]
    )