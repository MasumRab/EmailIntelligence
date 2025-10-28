#!/usr/bin/env python3

import re

def process_tree_line(line):
    # Match lines that contain .md files
    match = re.search(r'^(.*?)(\./.*\.md)$', line)
    if match:
        prefix = match.group(1)
        full_path = match.group(2)
        # Remove leading ./
        path = full_path[2:]
        # Split path into directory and filename
        if '/' in path:
            dir_path, filename = path.rsplit('/', 1)
            link = f"[{filename}]({path})"
        else:
            # Root file
            filename = path
            link = f"[{filename}]({path})"
        return prefix + link
    else:
        return line

def main():
    with open('docs_tree_raw.txt', 'r') as f:
        lines = f.readlines()

    processed_lines = [process_tree_line(line.rstrip()) for line in lines]

    with open('documentation_tree.md', 'w') as f:
        f.write('# Documentation Tree\n\n')
        for line in processed_lines:
            f.write(line + '\n')

if __name__ == '__main__':
    main()
