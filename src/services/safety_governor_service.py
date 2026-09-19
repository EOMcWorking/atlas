PROTECTED_PATHS = [

    "src/services/safety_governor_service.py",

    "src/services/approval_service.py",

    "src/services/rollback_service.py",

    "src/services/auto_rollback_service.py",

    ".env"
]

PROTECTED_KEYWORDS = [

    "delete all",

    "remove safety",

    "disable approval",

    "disable rollback",

    "disable validation",

    "wipe memory",

    "erase backups"
]

def is_file_safe(
    filepath: str
):

    for protected in PROTECTED_PATHS:

        if protected in filepath:

            return False

    return True

def is_task_safe(
    task: str
):

    text = task.lower()

    for keyword in PROTECTED_KEYWORDS:

        if keyword in text:

            return False

    return True

def is_experiment_safe(
    strategy_name: str
):

    dangerous = [

        "DISABLE_VALIDATION",

        "DISABLE_REVIEW",

        "SKIP_TESTS",

        "NO_APPROVAL"
    ]

    return strategy_name not in dangerous

def approve_edit(
    task: str,
    target_file: str
):

    if not is_task_safe(
        task
    ):

        return {

            "approved": False,

            "reason":
            "Unsafe task"
        }

    if not is_file_safe(
        target_file
    ):

        return {

            "approved": False,

            "reason":
            "Protected file"
        }

    return {

        "approved": True
    }

def evaluate_action(
    task: str,
    target_file: str
):

    return approve_edit(
        task,
        target_file
    )
