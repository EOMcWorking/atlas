def build_file_context(
    target_file: str,
    target_content: str,
    related_files: list
):

    sections = []

    sections.append(
        f"TARGET FILE:\n{target_file}\n\n{target_content}"
    )

    for file_name, content in related_files:

        sections.append(
            f"""
RELATED FILE:
{file_name}

{content[:4000]}
"""
        )

    return "\n\n".join(
        sections
    )