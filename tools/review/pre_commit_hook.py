#!/usr/bin/env python3
"""
Pre-commit hook for Multi-Agent Code Review System

This script runs automatically before each commit to check for code issues.
"""

import subprocess
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from tools.review import MultiAgentCodeReview


def get_staged_files():
    """Get list of staged files for commit."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            capture_output=True, text=True, cwd=ROOT_DIR
        )
        if result.returncode == 0:
            return result.stdout.strip().split('\n')
        else:
            print("Error getting staged files:", result.stderr)
            return []
    except Exception as e:
        print("Error getting staged files:", e)
        return []


def main():
    """Main function to run pre-commit code review."""
    print("Running pre-commit code review...")
    
    # Get staged files
    staged_files = get_staged_files()
    
    if not staged_files:
        print("No staged files to review.")
        return 0
    
    # Filter to only include Python and TypeScript files
    relevant_files = [
        str(ROOT_DIR / f) for f in staged_files 
        if f.endswith(('.py', '.ts', '.tsx')) and (ROOT_DIR / f).exists()
    ]
    
    if not relevant_files:
        print("No relevant files to review.")
        return 0
    
    print(f"Reviewing {len(relevant_files)} files...")
    
    # Initialize the review system
    review_system = MultiAgentCodeReview()
    
    # Run the review
    results = review_system.run_review(relevant_files)
    
    # Check for critical or high priority issues
    critical_issues = 0
    high_issues = 0
    
    for agent_name, agent_results in results.items():
        for issue in agent_results.get("issues", []):
            if issue.get("priority") == "critical":
                critical_issues += 1
            elif issue.get("priority") == "high":
                high_issues += 1
    
    # Generate report
    report = review_system.generate_report(results, format="console")
    
    if critical_issues > 0:
        print("\nCRITICAL ISSUES FOUND:")
        print(report)
        print(f"\nFound {critical_issues} critical issues that must be fixed before committing.")
        return 1
    elif high_issues > 0:
        print("\nHIGH PRIORITY ISSUES FOUND:")
        print(report)
        print(f"\nFound {high_issues} high priority issues.")
        response = input("Do you want to continue with the commit? (y/N): ")
        if response.lower() != 'y':
            return 1
    
    print("Code review completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())