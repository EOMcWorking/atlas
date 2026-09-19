def is_safe_patch(
    old_content: str,
    new_content: str
):

    if not new_content.strip():
        return False

    if len(new_content) < 20:
        return False

    if len(new_content) < (
        len(old_content) * 0.2
    ):
        return False

    return True