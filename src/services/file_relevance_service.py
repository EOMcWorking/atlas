from src.services.project_index_service import (
    get_directory_index
)


def rank_relevant_files(
    query: str,
    limit: int = 10
):

    query_words = (
        query.lower()
        .replace("_", " ")
        .split()
    )

    scored = []

    index = get_directory_index()

    for folder, files in index.items():

        # Reward matching the entire folder context
        folder_bonus = 0
        if folder in query_words:
            folder_bonus = 10

        for file in files:

            score = 0

            name = (
                file.lower()
                .replace(".py", "")
            )

            tokens = (
                name.replace(
                    "_",
                    " "
                )
                .split()
            )

            for word in query_words:

                for token in tokens:

                    if word == token:
                        score += 20

                    elif word in token:
                        score += 10

                    elif token in word:
                        score += 5

                if word == folder:
                    score += 15

            # Add folder context bonus
            score += folder_bonus

            if score > 0:

                scored.append(
                    (
                        score,
                        f"src/{folder}/{file}"
                    )
                )

    scored.sort(
        reverse=True
    )

    return [
        item[1]
        for item in scored[:limit]
    ]