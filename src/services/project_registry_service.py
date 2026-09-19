import json
import os
import shutil
from typing import List

REGISTRY_FILE = "data/projects.json"
PROJECTS_DIR = "projects"

class ProjectRegistryService:
    """Manages the list of known projects."""

    def __init__(self):
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "w") as f:
                json.dump([], f)

    def _load_registry(self) -> List[str]:
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)

    def _save_registry(self, projects: List[str]):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(projects, f, indent=2)

    def create_project(self, name: str) -> str:
        """Create a new project directory and register it."""
        if self.project_exists(name):
            raise ValueError(f"Project '{name}' already exists.")

        project_root = os.path.join(PROJECTS_DIR, name)
        os.makedirs(project_root, exist_ok=True)

        # Initialize standard project files
        for filename in ["PROJECT.md", "TASKS.md", "DECISIONS.md", "HANDOFF.md", "MEMORY.md", "ROADMAP.md"]:
            file_path = os.path.join(project_root, filename)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write(f"# {filename.split('.')[0]} for {name}\n")

        projects = self._load_registry()
        if name not in projects:
            projects.append(name)
            self._save_registry(projects)

        return project_root

    def delete_project(self, name: str) -> None:
        """Delete a project directory and unregister it."""
        if not self.project_exists(name):
            raise ValueError(f"Project '{name}' not found.")

        project_root = os.path.join(PROJECTS_DIR, name)
        if os.path.exists(project_root):
            shutil.rmtree(project_root)

        projects = self._load_registry()
        if name in projects:
            projects.remove(name)
            self._save_registry(projects)

    def list_projects(self) -> List[str]:
        """Return list of registered projects."""
        return self._load_registry()

    def project_exists(self, name: str) -> bool:
        """Check if a project is registered and its directory exists."""
        exists_in_registry = name in self._load_registry()
        project_dir = os.path.join(PROJECTS_DIR, name)
        return exists_in_registry and os.path.isdir(project_dir)