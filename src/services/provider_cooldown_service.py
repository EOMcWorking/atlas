import json
import time
from pathlib import Path

COOLDOWN_FILE = Path(
    "provider_cooldowns.json"
)


def load_cooldowns():

    if not COOLDOWN_FILE.exists():
        return {}

    return json.loads(
        COOLDOWN_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_cooldowns(
    cooldowns
):

    COOLDOWN_FILE.write_text(
        json.dumps(
            cooldowns,
            indent=2
        ),
        encoding="utf-8"
    )


def put_on_cooldown(
    provider_name: str,
    seconds: int = 1800
):

    cooldowns = load_cooldowns()

    cooldowns[
        provider_name
    ] = (
        time.time()
        + seconds
    )

    save_cooldowns(
        cooldowns
    )


def is_on_cooldown(
    provider_name: str
):

    cooldowns = load_cooldowns()

    expires = cooldowns.get(
        provider_name,
        0
    )

    return (
        time.time()
        < expires
    )