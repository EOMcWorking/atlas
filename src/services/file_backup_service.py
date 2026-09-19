from pathlib import Path
import shutil


def backup_file(path: str):

    source = Path(path)

    backup = Path(
        str(source) + ".bak"
    )

    shutil.copy2(
        source,
        backup
    )

    return str(backup)