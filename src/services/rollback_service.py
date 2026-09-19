from pathlib import Path
import shutil


BACKUP_DIR = Path(".atlas_backups")


def create_backup(
    filepath: str
):

    BACKUP_DIR.mkdir(
        exist_ok=True
    )

    source = Path(filepath)

    if not source.exists():
        return

    backup = (
        BACKUP_DIR
        / source.name
    )

    shutil.copy2(
        source,
        backup
    )

def restore_backup(
    filepath: str
):
    return rollback_file(
        filepath
    )

def rollback_file(
    filepath: str
):

    backup = (
        BACKUP_DIR
        / Path(filepath).name
    )

    if not backup.exists():
        return False

    shutil.copy2(
        backup,
        filepath
    )

    return True