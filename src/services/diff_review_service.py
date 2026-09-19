from src.services.git_diff_service import (
    get_git_diff
)

from src.services.ollama_service import (
    chat
)


def review_diff():

    diff_result = get_git_diff()

    if not diff_result["success"]:

        return {
            "success": False,
            "review": diff_result.get(
                "error",
                "Diff failed"
            )
        }

    diff = diff_result["diff"]

    if not diff.strip():

        return {
            "success": True,
            "approved": True,
            "review": "No changes detected."
        }

    prompt = f"""
You are Atlas Code Reviewer.

Review this git diff.

Check:

- Bugs
- Security issues
- Broken imports
- Dangerous deletions
- Logic mistakes

GIT DIFF:

{diff[:12000]}

Return:

VERDICT: APPROVED

or

VERDICT: REJECTED

Then explain why.
"""

    review = chat(
        prompt,
        task_type="review"
    )

    approved = (
        "VERDICT: APPROVED"
        in review.upper()
    )

    return {
        "success": True,
        "approved": approved,
        "review": review
    }