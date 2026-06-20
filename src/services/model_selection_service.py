from src.core.config import MODELS


def get_best_model(
    task_type: str = "general"
):

    return MODELS.get(
        task_type,
        MODELS["general"]
    )