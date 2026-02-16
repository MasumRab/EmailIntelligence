
import sys
import re

def resolve_file(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    resolved_lines = []
    in_conflict = False
    in_head = False

    for line in lines:
        if line.startswith("<<<<<<< HEAD"):
            in_conflict = True
            in_head = True
            continue
        elif line.startswith("======="):
            if in_conflict:
                in_head = False
                continue
        elif line.startswith(">>>>>>>"):
            if in_conflict:
                in_conflict = False
                in_head = False
                continue

        if in_conflict:
            if in_head:
                resolved_lines.append(line)
        else:
            resolved_lines.append(line)

    with open(filepath, 'w') as f:
        f.writelines(resolved_lines)

if __name__ == "__main__":
    resolve_file("setup/launch.py")
