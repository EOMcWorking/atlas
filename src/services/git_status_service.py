import subprocess


def get_git_status():

    try:

        result = subprocess.run(
            ["git", "status", "--short"],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "success": True,
            "output": result.stdout
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "errors": str(e)
        }