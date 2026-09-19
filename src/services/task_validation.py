def validate_task(task):

    task = task.strip()

    if len(task) < 10:
        return False

    banned = [
        "string",
        "test",
        "hello",
        "asdf"
    ]

    if task.lower() in banned:
        return False

    return True