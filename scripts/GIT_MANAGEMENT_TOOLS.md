# Git Management Tools

This directory contains a suite of tools for auditing, aligning, and recovering from complex git history divergences (e.g., massive accidental deletions or deep branch divergence).

## 1. analyze_git_history.py
Categorizes EmailIntelligence git commit history while filtering out "orchestration noise". **Run this from within any EmailIntelligence git repository.**

**Usage:**
```bash
python3 /path/to/analyze_git_history.py --range origin/main..HEAD
```
- `--range`: Commit range (standard git range syntax).
- `--verbose`: Shows full commit messages instead of a summary.

## 2. partial_cherry_pick.py
A selective cherry-pick script for EmailIntelligence that automatically imports "safe" changes. **Run this from within the target EmailIntelligence repository.**

**Usage:**
```bash
python3 /path/to/partial_cherry_pick.py <commit_hash>
```

## 3. inject_markers.py
Injects standard 3-way merge conflict markers for EmailIntelligence. **Run this from within the target repository.**

**Usage:**
```bash
python3 /path/to/inject_markers.py <commit_hash>
```
