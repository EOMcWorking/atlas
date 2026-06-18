from pathlib import Path

def get_atlas_status():
    return {
        "project": "Atlas",
        "version": "0.5-dev",
        "handoff_exists": Path("HANDOFF.md").exists(),
        "snapshot_exists": Path("atlas_snapshot.json").exists(),
    }