from src.services.ollama_service import chat


def review_diff(
    task: str,
    diff: str
):

    prompt = f"""
Task:

{task}

Git Diff:

{diff[:12000]}

Review the changes.

Check:

- Bugs
- Regressions
- Security issues
- Missing logic
- Broken architecture

End with:

VERDICT: APPROVED

or

VERDICT: REJECTED
"""

    return chat(
        prompt,
        task_type="review"
    )