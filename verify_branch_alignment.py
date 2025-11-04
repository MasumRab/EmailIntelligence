#!/usr/bin/env python3
"""
Branch Alignment Verification Script

This script verifies that all three branches (scientific, feature-notmuch-tagging-1, 
and align-feature-notmuch-tagging-1-v2) have consistent TODO comment coverage.
"""

import subprocess
import sys
from typing import Dict, List, Set


def get_todo_comments(branch_name: str, file_path: str) -> List[str]:
    """Extract TODO comments from a file in the specified branch."""
    try:
        result = subprocess.run([
            'git', 'show', f'{branch_name}:{file_path}'
        ], capture_output=True, text=True, check=True)
        
        lines = result.stdout.split('\n')
        todos = []
        for i, line in enumerate(lines, 1):
            if 'TODO' in line.upper():
                # Extract the TODO line and a few surrounding lines for context
                # Include line number for identification
                todos.append(f"{i}:{line.strip()}")
        return todos
    except subprocess.CalledProcessError:
        print(f"File {file_path} does not exist in branch {branch_name}")
        return []


def normalize_todo_content(todo_line: str) -> str:
    """Normalize TODO content by removing line numbers and extra spaces."""
    # Split by the first colon to separate line number from content
    parts = todo_line.split(':', 1)
    if len(parts) > 1:
        content = parts[1]
    else:
        content = todo_line
    
    # Remove extra whitespace and normalize
    normalized = ' '.join(content.split())
    return normalized


def compare_branches_todos(branch1: str, branch2: str, file_path: str) -> bool:
    """Compare TODO comments between two branches for a specific file."""
    todos1 = get_todo_comments(branch1, file_path)
    todos2 = get_todo_comments(branch2, file_path)
    
    normalized_todos1 = {normalize_todo_content(todo) for todo in todos1}
    normalized_todos2 = {normalize_todo_content(todo) for todo in todos2}
    
    missing_in_branch2 = normalized_todos1 - normalized_todos2
    missing_in_branch1 = normalized_todos2 - normalized_todos1
    
    if missing_in_branch2:
        print(f"  Missing in {branch2}:")
        for todo in missing_in_branch2:
            print(f"    - {todo}")
    
    if missing_in_branch1:
        print(f"  Missing in {branch1}:")
        for todo in missing_in_branch1:
            print(f"    - {todo}")
    
    return len(missing_in_branch2) == 0 and len(missing_in_branch1) == 0


def verify_all_branches():
    """Verify TODO comment consistency across all three branches."""
    branches = ['scientific', 'feature-notmuch-tagging-1', 'align-feature-notmuch-tagging-1-v2']
    
    print("Verifying TODO comment consistency across all branches...")
    print("=" * 60)
    
    files_to_check = [
        'backend/node_engine/security_manager.py',
        'backend/node_engine/workflow_engine.py'
    ]
    
    all_consistent = True
    
    for file_path in files_to_check:
        print(f"\nChecking {file_path}:")
        print("-" * 40)
        
        # Compare each pair of branches
        pair_results = []
        pairs = [
            (branches[0], branches[1]),
            (branches[1], branches[2]),
            (branches[0], branches[2])
        ]
        
        for branch1, branch2 in pairs:
            print(f"\nComparing {branch1} vs {branch2}:")
            try:
                result = compare_branches_todos(branch1, branch2, file_path)
                pair_results.append(result)
                if result:
                    print(f"  ✓ Consistent")
                else:
                    print(f"  ✗ Inconsistent")
                    all_consistent = False
            except Exception as e:
                print(f"  Error comparing {branch1} vs {branch2}: {e}")
                all_consistent = False
    
    print("\n" + "=" * 60)
    if all_consistent:
        print("✓ All branches have consistent TODO comment coverage")
        return True
    else:
        print("✗ Inconsistencies found between branches")
        return False


def main():
    """Main verification function."""
    print("Branch Alignment Verification")
    print("=" * 60)
    
    # Verify TODO consistency
    todos_consistent = verify_all_branches()
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY:")
    print(f"  TODO Consistency: {'PASS' if todos_consistent else 'FAIL'}")
    
    overall_success = todos_consistent
    print(f"  Overall: {'PASS' if overall_success else 'FAIL'}")
    
    if overall_success:
        print("\n✓ All verifications passed! Branches are properly aligned.")
        return 0
    else:
        print("\n✗ Some verifications failed. Please address the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())