from src.services.file_target_service import (
    find_target_file
)

from src.services.multi_file_patch_service import (
    patch_project_files
)


def smart_edit(
    task: str
):

    targets = find_target_file(
        task
    )

    if not targets:

        return {
            "success": False,
            "message": "No target files found"
        }

    results = []

    for target in targets[:3]:

        try:

            result = patch_project_files(
                task,
                target
            )

            results.append(
                result
            )

        except Exception as e:

            results.append(
                {
                    "success": False,
                    "file": target,
                    "error": str(e)
                }
            )

    return {
        "success": True,
        "edited_files": len(
            results
        ),
        "results": results
    }