import subprocess


def run_tests():

    try:

        result = subprocess.run(
            ["pytest"],
            capture_output=True,
            text=True,
            timeout=300
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "errors": result.stderr
        }

    except Exception as e:

        return {
            "success": False,
            "output": "",
            "errors": str(e)
        }