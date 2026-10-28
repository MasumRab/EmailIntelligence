with open("scripts/conflict_detection.py", "r") as f:
    content = f.read()

content = content.replace('["git", "merge-tree", "--write-tree", target_branch, source_branch]', '["git", "merge-tree", "--write-tree", "--", target_branch, source_branch]')

with open("scripts/conflict_detection.py", "w") as f:
    f.write(content)
