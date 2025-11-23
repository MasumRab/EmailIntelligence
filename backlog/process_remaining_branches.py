#!/usr/bin/env python3
"""
Process All Remaining High-Impact Branches

Automatically processes all remaining high-impact branches in sequence.
"""

import subprocess
import sys
from pathlib import Path


def get_remaining_branches():
    """Get the list of remaining high-impact branches to process."""
    return [
        'pr-179-new',                     # 402 tasks
        'pr-179-patch-clean-1762881335', # 566 tasks
        'align-feature-notmuch-tagging-1',        # 405 tasks
        'align-feature-notmuch-tagging-1-v2'      # 405 tasks
    ]


def process_branch(branch_name):
    """Process a single branch using the single branch processor."""
    print(f"\n{'='*60}")
    print(f"🚀 STARTING BRANCH: {branch_name}")
    print(f"{'='*60}\n")

    # Run the single branch processor
    result = subprocess.run([
        sys.executable, 'process_single_branch.py', branch_name
    ], cwd=Path(__file__).parent, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ SUCCESS: {branch_name} completed")
        print(result.stdout.split('\n')[-3:])  # Show last few lines with summary
    else:
        print(f"❌ FAILED: {branch_name}")
        print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        print("STDERR:", result.stderr[-500:])  # Last 500 chars

    return result.returncode == 0


def main():
    """Process all remaining high-impact branches."""
    remaining_branches = get_remaining_branches()

    print(f"🎯 Processing {len(remaining_branches)} remaining high-impact branches:")
    for i, branch in enumerate(remaining_branches, 1):
        print(f"  {i}. {branch}")
    print()

    successful = 0
    failed = 0

    for branch in remaining_branches:
        if process_branch(branch):
            successful += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print("🎉 BATCH PROCESSING COMPLETE")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total processed: {successful + failed}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()