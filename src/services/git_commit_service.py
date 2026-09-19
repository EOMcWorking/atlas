import subprocess


def create_commit(
    message: str
):

    try:

        subprocess.run(
            ["git", "add", "."],
            check=True
        )

        result = subprocess.run(
            [
                "git",
                "commit",
                "-m",
                message
            ],
            capture_output=True,
            text=True
        )

        return {
            "success": (
                result.returncode == 0
            ),
            "output": result.stdout,
            "errors": result.stderr
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "errors": str(e)
        }