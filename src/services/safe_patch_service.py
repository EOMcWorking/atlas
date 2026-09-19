from src.services.multi_file_patch_service import (
    patch_project_files
)

from src.services.test_runner_service import (
    run_tests
)

from src.services.rollback_service import (
    rollback_file
)


def safe_patch(
    task: str,
    target_file: str
):

    result = patch_project_files(
        task,
        target_file
    )

    tests = run_tests()

    if tests["success"]:

        result["tests"] = tests

        return result

    rollback_file(
        target_file
    )

    return {
        "success": False,
        "message": "Tests failed",
        "tests": tests
    }