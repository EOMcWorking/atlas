from src.services.execution_trace_service import (
    get_recent_traces
)

def count_events(
    event_name: str
):

    traces = (
        get_recent_traces(
            500
        )
    )

    count = 0

    for trace in traces:

        if (
            trace.get(
                "event"
            )
            ==
            event_name
        ):

            count += 1

    return count

def get_failure_trend():

    return {

        "failures":
        count_events(
            "TASK_FAILED"
        )
    }

def get_success_trend():

    return {

        "successes":
        count_events(
            "TASK_COMPLETED"
        )
    }

def get_trend_report():

    failures = (
        get_failure_trend()
    )

    successes = (
        get_success_trend()
    )

    return {

        "failures":
        failures,

        "successes":
        successes
    }
