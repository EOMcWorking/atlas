import random

from src.services.provider_selection_service import (
    get_ranked_provider_list
)


def choose_provider(
    task_type: str = "general"
):

    ranked = get_ranked_provider_list(
        task_type
    )

    if not ranked:
        return None

    if len(ranked) == 1:
        return ranked[0]

    roll = random.randint(
        1,
        100
    )

    if roll <= 90:
        return ranked[0]

    return random.choice(
        ranked[1:]
    )