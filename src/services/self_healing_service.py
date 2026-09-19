from src.agents.coder_agent import (
    code
)

from src.agents.reviewer_agent import (
    review
)


def self_heal(
    code_result: str,
    errors: str,
    max_attempts: int = 3
):

    current_code = code_result
    best_code = code_result  # Fix 3: Preserve best version

    attempts = 0

    while attempts < max_attempts:

        prompt = f"""
Fix the following code.

CODE:

{current_code}

ERRORS:

{errors}

Requirements:

- Fix all reported issues
- Do not remove existing functionality
- Return only corrected code
"""

        fixed_code = code(
            prompt
        )

        # Fix 2: Protect against empty output
        if not fixed_code.strip():
            attempts += 1
            continue

        review_result = review(
            fixed_code
        )

        text = review_result.lower()

        # Fix 1: Safer review check
        if "verdict: approved" in text:
            best_code = fixed_code  # Fix 3: update best on approval

            return {
                "success": True,
                "code": fixed_code,
                "review": review_result,
                "attempts": attempts + 1
            }

        current_code = fixed_code

        attempts += 1

    # Fix 3: Return best_code instead of potentially degraded current_code
    return {
        "success": False,
        "code": best_code,
        "review": review_result if attempts > 0 else "",
        "attempts": attempts
    }