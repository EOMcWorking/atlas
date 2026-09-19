import subprocess


def auto_commit(
    message: str
):

    subprocess.run(
        ["git", "add", "."]
    )

    subprocess.run(
        [
            "git",
            "commit",
            "-m",
            message
        ]
    )

    return True