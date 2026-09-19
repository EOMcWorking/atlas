from src.services.git_diff_service import (
    get_git_diff
)

from src.agents.diff_reviewer_agent import (
    review_diff
)

from src.services.review_result_service import (
    get_review_verdict
)

from src.services.git_commit_service import (
    create_commit
)


def commit_if_approved(
    task: str
):

    diff_result = get_git_diff()

    if not diff_result["success"]:
        return diff_result

    # 1. Reject empty diffs
    if not diff_result["diff"].strip():

        return {
            "success": False,
            "review": "No changes detected"
        }

    review_result = review_diff(
        task,
        diff_result["diff"]
    )

    # 2. Use the new verdict service
    verdict = get_review_verdict(
        review_result
    )

    if verdict != "APPROVED":

        return {
            "success": False,
            "review": review_result,
            "verdict": verdict
        }

    commit_result = create_commit(
        task
    )

    return {
        "success": commit_result["success"],
        "review": review_result,
        "commit": commit_result
    }