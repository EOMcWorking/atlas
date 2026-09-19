def classify_task(task: str) -> str:
    """
    Fast local classification.

    SIMPLE:
        - short coding requests
        - bug fixes
        - single function

    MEDIUM:
        - feature additions
        - multiple files

    COMPLEX:
        - architecture
        - system design
        - project-wide changes
    """

    task = task.strip().lower()

    words = len(task.split())

    complex_keywords = [
        "architecture",
        "microservice",
        "scalable",
        "system design",
        "database migration",
        "distributed",
        "refactor entire",
        "project-wide",
    ]

    medium_keywords = [
        "feature",
        "endpoint",
        "api",
        "dashboard",
        "integration",
        "workflow",
        "authentication",
    ]

    if any(k in task for k in complex_keywords):
        return "COMPLEX"

    if any(k in task for k in medium_keywords):
        return "MEDIUM"

    if words <= 20:
        return "SIMPLE"

    if words <= 100:
        return "MEDIUM"

    return "COMPLEX"