from src.services.rollback_service import (
    restore_backup
)


def auto_rollback(
    file_path: str,
    reason: str
):

    try:

        restore_backup(
            file_path
        )

        return {
            "success": True,
            "rolled_back": True,
            "reason": reason
        }

    except Exception as e:

        return {
            "success": False,
            "rolled_back": False,
            "reason": str(e)
        }