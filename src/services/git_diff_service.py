
import subprocess


def get_git_diff():

    try:

        result = subprocess.run(
            ["git", "diff"],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "success": True,
            "diff": result.stdout
        }

    except Exception as e:

        return {
            "success": False,
            "diff": "",
            "error": str(e)
        }