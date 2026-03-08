#!/usr/bin/env python3
import subprocess
import collections
import re
import argparse
import os
import sys

def analyze_git_history(commit_range, verbose=False):
    # Detect EmailIntelligence repo root
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "EmailIntelligence"))
    if not os.path.exists(repo_path):
        # Fallback to finding it in ~/github
        repo_path = os.path.expanduser("~/github/EmailIntelligence")
    
    if not os.path.exists(os.path.join(repo_path, ".git")):
        print(f"Error: Could not find EmailIntelligence repository at {repo_path}")
        return

    cmd = ["git", "-C", repo_path, "log", "--no-merges", "--format=%s", commit_range]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running git log: {result.stderr}")
        return

    commits = result.stdout.strip().split('\n')
    categories = collections.defaultdict(list)

    # Keywords to ignore (orchestration, deletions, exact sync commits)
    ignore_patterns = [
        r'(?i)remove\b', r'(?i)delete\b', r'(?i)clean up', r'(?i)clean orchestration',
        r'(?i)minimize docs', r'(?i)trim docs', r'(?i)setup directory', r'(?i)orchestration-tools',
        r'(?i)sync', r'(?i)merge pull request', r'^Update.*\.md$'
    ]

    for commit in commits:
        if not commit.strip(): continue
        
        # Skip orchestration/deletion noise
        if any(re.search(p, commit) for p in ignore_patterns):
            continue
            
        lower_commit = commit.lower()
        
        # Categorize
        if any(keyword in lower_commit for keyword in ['frontend', 'ui', 'react', 'dashboard', 'component', 'tailwind']):
            categories['Frontend / UI'].append(commit)
        elif any(keyword in lower_commit for keyword in ['database', 'sqlite', 'db', 'migration', 'repository']):
            categories['Database / Data Layer'].append(commit)
        elif any(keyword in lower_commit for keyword in ['ai', 'nlp', 'model', 'smart filter', 'llm', 'gemini', 'qwen', 'sentiment', 'topic']):
            categories['AI Engine / NLP'].append(commit)
        elif any(keyword in lower_commit for keyword in ['api', 'route', 'backend', 'fastapi', 'endpoint']):
            categories['Backend API / Core'].append(commit)
        elif any(keyword in lower_commit for keyword in ['test', 'pytest', 'coverage', 'mock']):
            categories['Testing'].append(commit)
        elif any(keyword in lower_commit for keyword in ['security', 'auth', 'mfa', 'audit', 'login']):
            categories['Security / Auth'].append(commit)
        elif any(keyword in lower_commit for keyword in ['refactor', 'solid', 'architecture']):
            categories['Refactoring / Architecture'].append(commit)
        elif any(keyword in lower_commit for keyword in ['docs', 'readme', 'documentation', 'guide']):
            categories['Documentation'].append(commit)
        else:
            # Keep interesting miscellaneous items if they look like features
            if 'feat:' in lower_commit or 'fix:' in lower_commit or 'implement' in lower_commit:
                categories['Other Features & Fixes'].append(commit)

    print(f"=== Substantive Code Changes in EmailIntelligence ({commit_range}) ===\n")

    for cat, items in sorted(categories.items()):
        print(f"## {cat} ({len(items)} commits)")
        for i, item in enumerate(items):
            if i < (100 if verbose else 8):
                print(f"  - {item}")
        if not verbose and len(items) > 8:
            print(f"  - ... and {len(items)-8} more")
        print()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Categorize EmailIntelligence git history and filter orchestration noise.")
    parser.add_argument("--range", default="origin/main..HEAD", help="Commit range (default: origin/main..HEAD)")
    parser.add_argument("--verbose", action="store_true", help="Show all commits in each category")
    
    args = parser.parse_args()
    analyze_git_history(args.range, args.verbose)
