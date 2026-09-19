from pathlib import Path
import ast


def validate_patch(
    original_content: str,
    patched_content: str,
    file_path: str
):

    if not patched_content.strip():

        return {
            "success": False,
            "reason": "Empty patch"
        }

    if (
        patched_content.strip()
        == original_content.strip()
    ):

        return {
            "success": False,
            "reason": "No changes made"
        }

    if file_path.endswith(".py"):

        try:

            ast.parse(
                patched_content
            )

        except Exception as e:

            return {
                "success": False,
                "reason": f"Syntax error: {e}"
            }

    return {
        "success": True
    }