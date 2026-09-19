from pathlib import Path
import json


BOARD_FILE = Path(
    "self_improvement_board.json"
)


def load_board():

    if not BOARD_FILE.exists():

        return []

    return json.loads(
        BOARD_FILE.read_text(
            encoding="utf-8"
        )
    )


def save_board(
    board
):

    BOARD_FILE.write_text(
        json.dumps(
            board,
            indent=2
        ),
        encoding="utf-8"
    )


def add_improvement(
    title: str,
    reason: str,
    priority: int = None
):
    """
    Add an improvement to the board.
    
    If priority is None, it will be calculated via evaluate_improvement().
    Otherwise, the caller can still pass a priority directly.
    """

    if priority is None:
        roi = evaluate_improvement(
            title,
            reason
        )
        priority = roi["roi"]

    # Clamp priority to 1-10 range
    priority = max(1, min(priority, 10))

    board = load_board()

    board.append({

        "title":
        title,

        "reason":
        reason,

        "priority":
        priority,

        "status":
        "OPEN"
    })

    save_board(
        board
    )


def evaluate_improvement(
    title: str,
    reason: str
):
    """
    Heuristic ROI evaluation for improvement ideas.
    
    Returns a dict with 'roi' (1-10) and 'rationale'.
    This can be upgraded to an LLM call later.
    """

    title_lower = title.lower()
    reason_lower = reason.lower()

    score = 5  # default neutral

    # High-impact indicators
    high_impact_keywords = [
        "critical", "security", "crash", "bug", "fix",
        "circular", "dependency", "deadlock", "memory",
        "performance", "slow", "broken", "failure",
        "failing", "recurring", "repeated"
    ]
    for keyword in high_impact_keywords:
        if keyword in title_lower or keyword in reason_lower:
            score += 2
            break  # only boost once for high impact

    # Medium-impact indicators
    medium_impact_keywords = [
        "refactor", "improve", "technical", "debt",
        "large", "oversized", "dead code", "clean",
        "organize", "split", "modularize"
    ]
    for keyword in medium_impact_keywords:
        if keyword in title_lower or keyword in reason_lower:
            score += 1
            break

    # Low-impact indicators (reduce priority)
    low_impact_keywords = [
        "minor", "cosmetic", "rename", "format",
        "whitespace", "comment", "docstring",
        "optional", "nice to have"
    ]
    for keyword in low_impact_keywords:
        if keyword in title_lower or keyword in reason_lower:
            score -= 2
            break

    # Frequency/severity boost from reason
    # Look for numbers indicating repeated issues
    import re
    numbers = re.findall(r'\d+', reason)
    if numbers:
        count = int(numbers[0])
        if count >= 10:
            score += 3
        elif count >= 5:
            score += 2
        elif count >= 3:
            score += 1

    # Clamp final score
    score = max(1, min(score, 10))

    return {
        "roi": score,
        "rationale": f"Heuristic evaluation based on title and reason keywords"
    }


def get_open_improvements():

    board = load_board()

    return [

        item

        for item in board

        if item["status"]
        == "OPEN"
    ]


def get_prioritized_improvements():

    items = (
        get_open_improvements()
    )

    items.sort(

        key=lambda x:
        x["priority"],

        reverse=True
    )

    return items


def get_next_improvement():

    items = (
        get_prioritized_improvements()
    )

    if not items:

        return None

    return items[0]


def complete_improvement(
    title: str
):

    board = load_board()

    for item in board:

        if (
            item["title"]
            == title
        ):

            item["status"] = (
                "COMPLETED"
            )

    save_board(
        board
    )