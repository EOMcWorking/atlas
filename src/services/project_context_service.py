from pathlib import Path

from src.services.project_paths_service import (
    get_project_root
)

from src.services.workspace_service import (
    get_docs_path,
    get_project_root as get_workspace_project_root
)


PROJECT_EXTENSIONS = [
    ".py",
    ".md"
]


ROOT_DOCS = [
    "PROJECT.md",
    "TASKS.md",
    "DECISIONS.md",
    "MEMORY.md",
    "HANDOFF.md",
    "ROADMAP.md"
]


EXCLUDED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".idea",
    ".vscode",
    "cache",
    "logs",
    "snapshots",
    "atlas_data"
}


def _is_excluded(path: Path):
    return any(
        part in EXCLUDED_DIRECTORIES
        for part in path.parts
    )


def _scan_project_root(project_root: Path):

    files = []

    if not project_root.exists():
        return files

    for extension in PROJECT_EXTENSIONS:

        for path in project_root.rglob(
            f"*{extension}"
        ):

            if _is_excluded(path):
                continue

            files.append(path)

    return files


def get_project_files(
    project_name: str = None
):

    if project_name is None:

        project_root = Path(
            get_workspace_project_root()
        )

        files = _scan_project_root(
            project_root
        )

        docs_path = Path(
            get_docs_path()
        )

        for doc in ROOT_DOCS:

            path = docs_path / doc

            if (
                path.exists()
                and path not in files
            ):
                files.append(path)

        return files

    project_root = Path(
        get_project_root(
            project_name
        )
    )

    return _scan_project_root(
        project_root
    )


def build_project_context(
    max_chars: int = 20000,
    project_name: str = None
):

    context_parts = []

    total_chars = 0

    for file in get_project_files(
        project_name
    ):

        try:

            content = file.read_text(
                encoding="utf-8"
            )

            file_block = (
                f"\n\nFILE: {file}\n"
                f"{content}\n"
            )

            if (
                total_chars
                + len(file_block)
                > max_chars
            ):
                break

            context_parts.append(
                file_block
            )

            total_chars += len(
                file_block
            )

        except Exception:
            continue

    return "".join(
        context_parts
    )


def get_project_stats(
    project_name: str = None
):

    files = get_project_files(
        project_name
    )

    total_chars = 0

    for file in files:

        try:

            total_chars += len(
                file.read_text(
                    encoding="utf-8"
                )
            )

        except Exception:
            pass

    return {
        "files": len(files),
        "characters": total_chars
    }