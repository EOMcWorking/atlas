from pathlib import Path
import json

PROFILE_FILE = Path(
    "service_profiles.json"
)

def load_profiles():

    if not PROFILE_FILE.exists():

        return {}

    return json.loads(
        PROFILE_FILE.read_text(
            encoding="utf-8"
        )
    )

def save_profiles(
    profiles
):

    PROFILE_FILE.write_text(
        json.dumps(
            profiles,
            indent=2
        ),
        encoding="utf-8"
    )

def record_service_call(
    service_name: str,
    duration: float,
    success: bool
):

    profiles = load_profiles()

    if service_name not in profiles:

        profiles[
            service_name
        ] = {

            "calls": 0,

            "failures": 0,

            "total_runtime": 0
        }

    profile = profiles[
        service_name
    ]

    profile["calls"] += 1

    profile[
        "total_runtime"
    ] += duration

    if not success:

        profile[
            "failures"
        ] += 1

    save_profiles(
        profiles
    )

def get_average_runtime(
    service_name: str
):

    profiles = load_profiles()

    profile = profiles.get(
        service_name
    )

    if not profile:

        return 0

    calls = max(
        profile["calls"],
        1
    )

    return (
        profile[
            "total_runtime"
        ]
        / calls
    )

def get_slowest_services():

    profiles = load_profiles()

    results = []

    for service in profiles:

        results.append({

            "service":
            service,

            "average_runtime":
            get_average_runtime(
                service
            )
        })

    results.sort(

        key=lambda x:
        x["average_runtime"],

        reverse=True
    )

    return results

def get_most_failures():

    profiles = load_profiles()

    results = []

    for service, data in (
        profiles.items()
    ):

        results.append({

            "service":
            service,

            "failures":
            data["failures"]
        })

    results.sort(

        key=lambda x:
        x["failures"],

        reverse=True
    )

    return results