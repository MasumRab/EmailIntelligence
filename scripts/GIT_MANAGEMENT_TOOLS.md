# Git Management Tools

This directory contains a suite of tools for auditing, aligning, and recovering from complex git history divergences (e.g., massive accidental deletions or deep branch divergence).

## 1. analyze_git_history.py
Categorizes git commit history while filtering out "orchestration noise" (bulk deletions, infrastructure-only commits, cleanup tasks).

**Usage:**
```bash
python3 analyze_git_history.py --repo ~/github/EmailIntelligence --range origin/main..HEAD
```
- `--repo`: Path to the repository.
- `--range`: Commit range (standard git range syntax).
- `--verbose`: Shows full commit messages instead of a summary.

## 2. partial_cherry_pick.py
A selective cherry-pick script that automatically imports "safe" changes (newly added files) and attempts cleanly merges of modified files, while automatically skipping any file that results in a structural merge conflict.

**Usage:**
```bash
python3 partial_cherry_pick.py <commit_hash> --repo <path>
```

## 3. inject_markers.py
Injects standard 3-way merge conflict markers into files that were modified in a remote commit but conflict locally. This allows you to use IDE merge tools (like VS Code) to resolve architectural divergences file-by-file.

**Usage:**
```bash
python3 inject_markers.py <commit_hash> --repo <path>
```
