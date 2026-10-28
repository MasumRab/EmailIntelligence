#!/usr/bin/env python3
import os
import sys
import ast

def get_script_description(filepath: str) -> str:
    """Extract description from a script."""
    if filepath.endswith('.py'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            module = ast.parse(content)
            docstring = ast.get_docstring(module)
            if docstring:
                return docstring.split('\n')[0].strip()
        except Exception:
            pass
    elif filepath.endswith('.sh'):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            for line in lines:
                if line.startswith('#') and not line.startswith('#!'):
                    return line.lstrip('#').strip()
        except Exception:
            pass
    return "No description available."

def generate_usage_table(scripts_dir: str):
    print("| Script | Description |")
    print("|--------|-------------|")

    try:
        scripts = sorted(os.listdir(scripts_dir))
    except FileNotFoundError:
        print(f"Directory not found: {scripts_dir}")
        return

    for script in scripts:
        if not (script.endswith('.py') or script.endswith('.sh')):
            continue
        filepath = os.path.join(scripts_dir, script)
        if not os.path.isfile(filepath):
            continue

        desc = get_script_description(filepath)
        print(f"| {script} | {desc} |")

if __name__ == '__main__':
    target_dir = sys.argv[1] if len(sys.argv) > 1 else 'scripts'
    generate_usage_table(target_dir)
