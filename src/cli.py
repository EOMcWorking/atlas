import argparse
import json
import uvicorn
import webbrowser
import threading
import time

from pathlib import Path

from src.services.workspace_service import get_workspace


def get_cli_workspace():
    return get_workspace()

def initialize_project():
    project_root = Path.cwd().resolve()

    atlas_directory = project_root / ".atlas"

    directories = {
        "config": atlas_directory / "config",
        "docs": atlas_directory / "atlas_md",
        "memory": atlas_directory / "memory",
        "logs": atlas_directory / "logs",
        "snapshots": atlas_directory / "snapshots",
        "cache": atlas_directory / "cache",
    }

    for directory in directories.values():
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    workspace_file = (
        directories["config"]
        / "workspace.json"
    )

    workspace = {
        "project": {
            "name": project_root.name,
            "root": str(project_root),
        },
        "atlas": {
            "root": str(atlas_directory),
            "docs": str(directories["docs"]),
            "memory": str(directories["memory"]),
            "logs": str(directories["logs"]),
            "snapshots": str(directories["snapshots"]),
            "cache": str(directories["cache"]),
        },
    }

    workspace_file.write_text(
        json.dumps(workspace, indent=4),
        encoding="utf-8",
    )

    providers_file = directories["config"] / "providers.json"

    if not providers_file.exists():
        providers_file.write_text(
            json.dumps({}, indent=4),
            encoding="utf-8",
        )

    default_documents = {
        "PROJECT.md": (
            f"# {project_root.name}\n\n"
            "Project initialized with Atlas.\n"
        ),
        "TASKS.md": "# Tasks\n",
        "DECISIONS.md": "# Decisions\n",
        "MEMORY.md": "# Memory\n",
        "HANDOFF.md": "# Atlas Handoff\n",
        "ROADMAP.md": "# Roadmap\n",
    }

    for filename, content in default_documents.items():
        document = directories["docs"] / filename

        if not document.exists():
            document.write_text(
                content,
                encoding="utf-8"
            )
    print("Atlas project initialized")
    print("-------------------------")
    print(f"Project : {workspace['project']['name']}")
    print(f"Root    : {workspace['project']['root']}")
    print(f"Atlas   : {workspace['atlas']['root']}")
    print(f"Config  : {workspace_file}")

def main():
    parser = argparse.ArgumentParser(
        prog="atlas",
        description="Atlas AI Software Engineering System",
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="status",
        help="Atlas command to execute",
    )

    args = parser.parse_args()

    if args.command in ("server", "start"):
        url = "http://127.0.0.1:8000/docs"

        def open_browser():
            time.sleep(1)
            webbrowser.open(url)

        threading.Thread(
            target=open_browser,
            daemon=True,
        ).start()

        uvicorn.run(
            "src.main:app",
            host="127.0.0.1",
            port=8000,
            reload=False,
        )
        return

    if args.command == "status":
        workspace = get_cli_workspace()

        print("Atlas")
        print("-----")
        print(f"Project : {workspace['project']['name']}")
        print(f"Root    : {workspace['project']['root']}")
        print(f"Atlas   : {workspace['atlas']['root']}")
        print("Status  : ready")
        return

    if args.command == "init":
        initialize_project()
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()