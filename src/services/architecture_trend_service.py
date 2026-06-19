import json
from pathlib import Path
from datetime import datetime

from src.services.technical_debt_service import (
    calculate_technical_debt
)


TREND_FILE = Path(
    "ARCHITECTURE_HISTORY.json"
)


def save_architecture_snapshot():

    snapshot = {
        "timestamp":
            datetime.now().isoformat(),

        "debt":
            calculate_technical_debt()
    }

    history = []

    if TREND_FILE.exists():

        history = json.loads(
            TREND_FILE.read_text(
                encoding="utf-8"
            )
        )

    history.append(snapshot)

    TREND_FILE.write_text(
        json.dumps(
            history,
            indent=2
        ),
        encoding="utf-8"
    )

    return snapshot


def get_architecture_history():

    if not TREND_FILE.exists():

        return []

    return json.loads(
        TREND_FILE.read_text(
            encoding="utf-8"
        )
    )