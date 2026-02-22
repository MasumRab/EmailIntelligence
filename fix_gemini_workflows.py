import os

workflows = [
    '.github/workflows/gemini-review.yml',
    '.github/workflows/gemini-triage.yml',
    '.github/workflows/gemini-invoke.yml'
]

# Function to patch a single file content
def patch_content(content):
    lines = content.splitlines()
    new_lines = []

    for i, line in enumerate(lines):
        if "uses: 'google-github-actions/run-gemini-cli@v0'" in line:
            indent = len(line) - len(line.lstrip())

            has_if = False
            # Look backwards for an existing 'if' in the same block
            for j in range(i-1, max(-1, i-10), -1):
                prev_line = lines[j]
                prev_indent = len(prev_line) - len(prev_line.lstrip())
                if prev_indent < indent:
                    break
                if prev_indent == indent and prev_line.strip().startswith("if:"):
                    has_if = True
                    break

            if not has_if:
                # Add the condition.
                condition = f"{' ' * indent}if: |-\n{' ' * (indent + 2)}${{{{ secrets.GEMINI_API_KEY != '' || secrets.GOOGLE_API_KEY != '' || vars.GCP_WIF_PROVIDER != '' }}}}"
                new_lines.append(condition)

        new_lines.append(line)
    return "\n".join(new_lines) + "\n"

for workflow in workflows:
    path = os.path.join(os.getcwd(), workflow)
    if not os.path.exists(path):
        print(f"Workflow {path} not found.")
        continue

    with open(path, 'r') as f:
        content = f.read()

    new_content = patch_content(content)

    with open(path, 'w') as f:
        f.write(new_content)
    print(f"Patched {workflow}")
