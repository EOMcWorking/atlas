import os
from pathlib import Path

from src.services.workspace_service import (
    get_project_root as get_workspace_project_root,
)


class ProjectPathsService:
    """Provides standardized paths for project files."""

    PROJECTS_DIR = "projects"

    @staticmethod
    def get_project_root(
        project_name: str = None
    ) -> str:
        """
        Resolve the project root.

        When no project name is supplied, use the
        currently configured Atlas workspace.

        When a project name is supplied, preserve
        the legacy projects/<name> behavior.
        """
        if project_name is None:
            return get_workspace_project_root()

        return os.path.join(
            ProjectPathsService.PROJECTS_DIR,
            project_name
        )

    @staticmethod
    def get_project_file(
        project_name: str = None,
        filename: str = None
    ) -> str:
        """
        Resolve a file inside the selected project.
        """
        if filename is None:
            raise ValueError(
                "filename is required"
            )

        return os.path.join(
            ProjectPathsService.get_project_root(
                project_name
            ),
            filename
        )


def get_project_root(
    project_name: str = None
):
    return ProjectPathsService.get_project_root(
        project_name
    )


def get_project_file(
    project_name: str = None,
    filename: str = None
):
    return ProjectPathsService.get_project_file(
        project_name,
        filename
    )