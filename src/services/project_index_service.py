from pathlib import Path


def get_directory_index():

    structure = {}

    folders = [
        "api",
        "services",
        "providers",
        "models",
        "core"
    ]

    for folder in folders:

        path = Path(
            "src"
        ) / folder

        if not path.exists():
            continue

        structure[
            folder
        ] = []

        for file in path.glob(
            "*.py"
        ):
            structure[
                folder
            ].append(
                file.name
            )

    return structure