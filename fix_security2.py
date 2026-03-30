import re

def fix_file(filepath):
    try:
        with open(filepath, "r") as f:
            content = f.read()

        # Remove git conflict markers and keep HEAD version
        fixed_content = re.sub(
            r'<<<<<<< HEAD\n(.*?)\n=======\n.*?\n>>>>>>> [^\n]*\n',
            r'\1\n',
            content,
            flags=re.DOTALL
        )

        with open(filepath, "w") as f:
            f.write(fixed_content)
    except Exception as e:
        print(f"Failed {filepath}: {e}")

fix_file("src/core/security.py")
fix_file("src/core/models.py")
fix_file("src/core/settings.py")
fix_file("src/core/auth.py")
