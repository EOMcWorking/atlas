import os
import shutil
from src.services.project_registry_service import ProjectRegistryService
from src.services.project_paths_service import ProjectPathsService

ROOT_FILES = ["PROJECT.md", "TASKS.md", "DECISIONS.md", "HANDOFF.md", "MEMORY.md", "ROADMAP.md"]

class MigrationService:
    """Migrates single-project root files into projects/atlas/ structure."""

    @staticmethod
    def migrate_single_project_to_multi_project():
        registry = ProjectRegistryService()
        if registry.project_exists("atlas"):
            print("Migration already completed: 'atlas' project exists.")
            return

        # Create the default 'atlas' project
        registry.create_project("atlas")

        for fname in ROOT_FILES:
            if os.path.exists(fname):
                dest = ProjectPathsService.get_project_file("atlas", fname)
                shutil.copy2(fname, dest)
                print(f"Migrated {fname} -> {dest}")
            else:
                print(f"File {fname} not found in root, skipped.")
        print("Migration complete.")
