from src.services.meta_reasoning_service import (
    get_meta_reasoning_report
)

from src.services.strategy_memory_service import (
    load_strategies,
    save_strategy,
    get_best_strategies
)

from src.services.meta_learning_service import (
    get_meta_learning_report
)


def detect_strategy_changes():

    report = (
        get_meta_reasoning_report()
    )

    text = str(report).lower()

    changes = []

    if "dependency" in text:

        changes.append(
            "USE_DEPENDENCY_ANALYSIS"
        )

    if "context" in text:

        changes.append(
            "REDUCE_CONTEXT_SIZE"
        )

    if "patch" in text:

        changes.append(
            "STRICT_PATCH_VALIDATION"
        )

    if "review" in text:

        changes.append(
            "INCREASE_REVIEW_WEIGHT"
        )

    # Prefer best strategies from memory
    best = get_best_strategies()
    for strategy in best[:3]:
        name = strategy.get("name", "")
        if name and name not in changes:
            changes.append(name)

    # Use meta-learning lessons to influence strategy selection
    learning_report = get_meta_learning_report()
    analysis = learning_report.get("analysis", "").lower()

    if "avoid" in analysis:
        # Remove strategies that meta-learning says to avoid
        for line in analysis.splitlines():
            if "avoid" in line.lower():
                for change in changes[:]:
                    if any(word in change.lower() for word in line.lower().split()):
                        changes.remove(change)

    if "more" in analysis or "best" in analysis:
        # Boost strategies that meta-learning says work well
        for line in analysis.splitlines():
            if "more" in line.lower() or "best" in line.lower():
                words = line.lower().replace("more", "").replace("best", "").replace("do", "").strip()
                if words and words not in changes:
                    changes.insert(0, words.upper().replace(" ", "_"))

    return changes


def apply_strategy_changes():

    changes = (
        detect_strategy_changes()
    )

    applied = []

    for change in changes:

        save_strategy(
            change
        )

        applied.append(
            change
        )

    return applied


def get_active_strategies():

    return load_strategies()


def adapt_strategies():

    applied = (
        apply_strategy_changes()
    )

    return {

        "success": True,

        "applied":
        applied,

        "active":
        get_active_strategies()
    }