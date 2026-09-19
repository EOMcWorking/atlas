from pathlib import Path
import json
from datetime import datetime


TRACE_FILE = Path(
    "execution_trace.jsonl"
)

def record_trace(
    event_type: str,
    data: dict
):

    record = {

        "timestamp":
        datetime.utcnow().isoformat(),

        "event":
        event_type,

        "data":
        data
    }

    with open(
        TRACE_FILE,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            json.dumps(record)
            + "\n"
        )

def load_traces():

    if not TRACE_FILE.exists():

        return []

    results = []

    with open(
        TRACE_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        for line in f:

            try:

                results.append(
                    json.loads(line)
                )

            except Exception:
                pass

    return results

def get_recent_traces(
    limit: int = 100
):

    return load_traces()[
        -limit:
    ]
