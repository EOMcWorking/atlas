from src.core.config import (MODELS, TASK_MODELS)


def get_best_model(
    task_type: str = "general"
):

    return MODELS.get(
        task_type,
        MODELS["general"]
    )


def get_model_for_provider(
    provider_name: str,
    task_type: str
):

    task_models = (
        TASK_MODELS.get(
            task_type,
            TASK_MODELS["general"]
        )
    )

    return task_models.get(
        provider_name
    )