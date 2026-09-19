from src.services.task_queue_service import (
    get_pending_tasks
)

from src.services.self_improvement_board_service import (
    get_open_improvements
)

from src.services.capacity_planning_service import (
    get_capacity_status
)

from src.services.predictive_risk_service import (
    get_risk_summary
)

from src.services.improvement_roi_service import (
    evaluate_improvement
)

from src.services.goal_alignment_service import (
    get_alignment_score
)


def score_task(
    task
):

    score = 50

    text = str(
        task
    ).lower()

    if (
        "critical"
        in text
    ):
        score += 50

    if (
        "security"
        in text
    ):
        score += 40

    if (
        "bug"
        in text
    ):
        score += 30

    # Goal alignment bonus
    alignment = get_alignment_score(task)
    score += alignment

    return score


def score_improvement(
    improvement
):
    """
    Score an improvement using ROI evaluation instead of simple priority * 10.
    """

    title = improvement.get("title", "")
    reason = improvement.get("reason", "")

    try:
        roi_result = evaluate_improvement(title, reason)
        roi_score = roi_result["roi"]

        # Map ROI to a score range comparable with tasks
        # ROI from evaluate_improvement uses: impact*10 - effort*5 - risk*3
        # Typical range: -15 to 75+
        # Normalize to 0-100 range for fair comparison with tasks
        normalized = max(0, min(roi_score + 15, 100))

    except Exception:
        # Fallback to simple priority scoring if ROI evaluation fails
        normalized = improvement.get("priority", 5) * 10

    # Goal alignment bonus for improvements too
    alignment = get_alignment_score(title)
    normalized += alignment

    return normalized


def collect_work_items():

    work = []

    for task in (
        get_pending_tasks()
    ):

        work.append({

            "type":
            "TASK",

            "item":
            task,

            "score":
            score_task(
                task
            )
        })

    for improvement in (
        get_open_improvements()
    ):

        work.append({

            "type":
            "IMPROVEMENT",

            "item":
            improvement,

            "score":
            score_improvement(
                improvement
            )
        })

    return work


def rank_work_items():

    work = (
        collect_work_items()
    )

    work.sort(

        key=lambda x:
        x["score"],

        reverse=True
    )

    return work


def allocate_next_work():

    capacity = (
        get_capacity_status()
    )

    ranked = (
        rank_work_items()
    )

    if not ranked:

        return None

    if capacity == (
        "OVERLOADED"
    ):

        ranked = [

            item

            for item in ranked

            if item[
                "type"
            ] == "TASK"
        ]

        if not ranked:

            return None

    return ranked[0]


def get_allocation_report():

    return {

        "capacity":
        get_capacity_status(),

        "selected":
        allocate_next_work(),

        "top_10":
        rank_work_items()[:10]
    }