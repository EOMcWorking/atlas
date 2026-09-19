from src.services.file_relevance_service import (
    rank_relevant_files
)


def find_target_file(
    task: str
):
    return rank_relevant_files(
        task,
        limit=5
    )