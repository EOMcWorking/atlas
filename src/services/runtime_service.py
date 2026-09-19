from threading import Thread, Lock

from src.services.autonomous_scheduler_service import (
    scheduler_startup,
    scheduler_cycle,
    scheduler_shutdown,
    get_scheduler_interval
)

_runtime_thread = None
_runtime_running = False
_runtime_paused = False

_lock = Lock()


def _runtime_loop():

    global _runtime_running

    scheduler_startup()

    try:

        while _runtime_running:

            if _runtime_paused:
                import time
                time.sleep(1)
                continue

            sleep_seconds = scheduler_cycle()

            import time
            time.sleep(sleep_seconds)

    finally:

        scheduler_shutdown()


def start_runtime():

    global _runtime_thread
    global _runtime_running

    with _lock:

        if _runtime_running:

            return {
                "success": False,
                "message": "Runtime already running"
            }

        _runtime_running = True

        _runtime_thread = Thread(
            target=_runtime_loop,
            daemon=True
        )

        _runtime_thread.start()

        return {
            "success": True,
            "message": "Runtime started"
        }


def stop_runtime():

    global _runtime_running

    with _lock:

        _runtime_running = False

    return {
        "success": True,
        "message": "Runtime stopping"
    }


def restart_runtime():

    stop_runtime()

    import time
    time.sleep(2)

    return start_runtime()


def pause_runtime():

    global _runtime_paused

    _runtime_paused = True

    return {
        "success": True,
        "message": "Runtime paused"
    }


def resume_runtime():

    global _runtime_paused

    _runtime_paused = False

    return {
        "success": True,
        "message": "Runtime resumed"
    }


def runtime_running():

    return _runtime_running


def runtime_paused():

    return _runtime_paused


def get_runtime_status():

    return {

        "running": runtime_running(),

        "paused": runtime_paused(),

        "thread_alive":

        _runtime_thread.is_alive()

        if _runtime_thread

        else False
    }


def get_runtime_snapshot():

    return {

        "status":

        get_runtime_status(),

        "scheduler_interval":

        get_scheduler_interval()
    }