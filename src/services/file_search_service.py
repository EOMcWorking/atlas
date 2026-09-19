from src.services.project_index_service import (
    build_project_index
)


def find_candidate_files(
    keyword: str
):

    files = build_project_index()

    matches = []

    keyword = keyword.lower()

    for file in files:

        if keyword in file.lower():

            matches.append(file)

    return matches[:10]