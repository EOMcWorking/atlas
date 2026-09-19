from src.services.file_reader_service import read_file
from src.services.file_writer_service import write_file
from src.services.rollback_service import create_backup
from src.services.auto_rollback_service import (
    auto_rollback
)
from src.services.dependency_discovery_service import find_related_files
from src.services.context_file_builder import build_file_context
from src.services.patch_validation_service import (
    validate_patch
)
from src.services.safety_governor_service import (
    evaluate_action
)
from src.agents.code_patch_agent import patch_code


def patch_project_files(
    task: str,
    target_file: str
):

    # HIGHEST PRIORITY: Safety governor check before any patching
    decision = evaluate_action(
        task,
        target_file
    )

    if not decision["approved"]:

        return {
            "success": False,
            "target_file": target_file,
            "error": decision["reason"]
        }

    create_backup(
        target_file
    )

    target_content = read_file(
        target_file
    )

    related_files = []

    for path in find_related_files(
        target_file
    ):

        try:

            related_files.append(
                (
                    path,
                    read_file(path)
                )
            )

        except Exception:
            pass

    context = build_file_context(
        target_file,
        target_content,
        related_files
    )

    patched = patch_code(
        task,
        target_file,
        context
    )

    # Validate the patch before writing
    validation = validate_patch(
        target_content,
        patched,
        target_file
    )

    if not validation["success"]:

        # Rollback on validation failure
        auto_rollback(
            target_file,
            validation["reason"]
        )

        return {
            "success": False,
            "target_file": target_file,
            "error": validation["reason"]
        }

    write_file(
        target_file,
        patched
    )

    return {
        "success": True,
        "target_file": target_file,
        "related_files": len(
            related_files
        )
    }