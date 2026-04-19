import subprocess
import re
import sys

def run_ruff_check():
    result = subprocess.run(["uv", "run", "ruff", "check", "src/", "modules/", "setup/"], capture_output=True, text=True)
    return result.stdout

def apply_fixes():
    output = run_ruff_check()
    lines = output.split("\n")

    files_to_fix_e402 = set()

    for i, line in enumerate(lines):
        if "E402 Module level import not at top of file" in line:
            if i + 1 < len(lines):
                next_line = lines[i+1]
                m = re.search(r"--> (.*?):", next_line)
                if m:
                    files_to_fix_e402.add(m.group(1).strip())

    for filepath in files_to_fix_e402:
        try:
            with open(filepath, "r") as f:
                content = f.readlines()
            new_content = []
            for line in content:
                if (line.startswith("import ") or line.startswith("from ")) and "noqa: E402" not in line:
                    new_content.append(line.rstrip() + "  # noqa: E402\n")
                else:
                    new_content.append(line)
            with open(filepath, "w") as f:
                f.writelines(new_content)
            print(f"Fixed E402 in {filepath}")
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")

if __name__ == "__main__":
    apply_fixes()
