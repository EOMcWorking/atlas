def score_context(
    query: str,
    content: str
):

    score = 0

    query_words = (
        query.lower()
        .split()
    )

    text = content.lower()

    for word in query_words:

        if word in text:

            score += 10

    return score

def rank_context(
    query: str,
    entries: list
):

    scored = []

    for item in entries:

        score = score_context(
            query,
            item
        )

        scored.append(

            (
                score,
                item
            )
        )

    scored.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return [

        item[1]

        for item

        in scored
    ]

def get_top_context(
    query: str,
    entries: list,
    limit: int = 20
):

    ranked = rank_context(
        query,
        entries
    )

    return ranked[:limit]
