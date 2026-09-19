from src.services.planner_file_extractor_service import (
    extract_planner_files
)

from src.services.file_target_service import (
    find_target_file
)


def determine_edit_targets(
    task: str,
    plan: str
):

    # First try to extract files from the planner output
    targets = extract_planner_files(
        plan
    )

    if targets:
        return targets

    # Fall back to finding target file from the task
    return find_target_file(
        task
    )