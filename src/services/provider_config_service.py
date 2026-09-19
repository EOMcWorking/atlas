import json
from pathlib import Path

from src.services.workspace_service import (
    get_atlas_path,
)


def get_provider_config_file():
    path = Path(get_atlas_path("root")) / "config" / "providers.json"
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )
    return path


def load_provider_config():
    path = get_provider_config_file()

    if not path.exists():
        return {}

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_provider_config(config):
    path = get_provider_config_file()

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            config,
            file,
            indent=4,
        )

    return config