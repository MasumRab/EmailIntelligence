import re
with open('emailintelligence_cli.py') as f:
    content = f.read()

# Fix 1: ["git", "checkout", "-b", resolution_branch] -> ["git", "checkout", "-b", resolution_branch, "--"]
content = content.replace(
    '["git", "checkout", "-b", resolution_branch]',
    '["git", "checkout", "-b", resolution_branch, "--"]'
)

# Fix 2: ["git", "worktree", "add", str(worktree_a_path), source_branch] -> ["git", "worktree", "add", str(worktree_a_path), source_branch, "--"]
content = content.replace(
    '["git", "worktree", "add", str(worktree_a_path), source_branch]',
    '["git", "worktree", "add", str(worktree_a_path), source_branch, "--"]'
)

# Fix 3: ["git", "worktree", "add", str(worktree_b_path), target_branch]
content = content.replace(
    '["git", "worktree", "add", str(worktree_b_path), target_branch]',
    '["git", "worktree", "add", str(worktree_b_path), target_branch, "--"]'
)

with open('emailintelligence_cli.py', 'w') as f:
    f.write(content)

