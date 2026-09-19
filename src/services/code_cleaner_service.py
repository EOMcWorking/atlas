import re


def clean_code_response(text: str):

    text = text.replace("```python", "")
    text = text.replace("```", "")

    lines = text.splitlines()

    code_lines = []

    for line in lines:

        if line.strip().startswith("Explanation"):
            break

        code_lines.append(line)

    return "\n".join(code_lines).strip()