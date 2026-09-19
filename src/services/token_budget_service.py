def estimate_tokens(
    text: str
):

    return max(
        1,
        len(text) // 4
    )

def trim_to_budget(
    text: str,
    max_tokens: int
):

    max_chars = (
        max_tokens * 4
    )

    if len(text) <= max_chars:

        return text

    return text[
        :max_chars
    ]

def allocate_budget():

    return {

        "task": 500,

        "memory": 1500,

        "context": 2500,

        "failures": 500,

        "handoff": 500,

        "roadmap": 1000
    }

def budget_context(
    sections: dict
):

    budgets = (
        allocate_budget()
    )

    result = {}

    for section, content in (
        sections.items()
    ):

        limit = budgets.get(
            section,
            500
        )

        result[
            section
        ] = trim_to_budget(
            content,
            limit
        )

    return result

def get_budget_report(
    sections: dict
):

    report = {}

    for name, text in (
        sections.items()
    ):

        report[
            name
        ] = estimate_tokens(
            text
        )

    return report
