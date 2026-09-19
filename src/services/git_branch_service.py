import subprocess


def create_branch(
    branch_name: str
):

    try:

        result = subprocess.run(
            [
                "git",
                "checkout",
                "-b",
                branch_name
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