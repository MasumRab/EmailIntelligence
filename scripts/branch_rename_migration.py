#!/usr/bin/env python3
"""
Branch Rename Migration Script

This script helps migrate existing branches to follow the new standardized naming conventions.

Usage:
    python scripts/branch_rename_migration.py --dry-run  # Show what would be renamed
    python scripts/branch_rename_migration.py --execute # Actually rename branches

Naming Standards:
- feature/* -> feature/* (keep as-is)
- feat/* -> feature/* (rename)
- fix/* -> bugfix/* (rename)
- refactor/* -> refactor/* (keep as-is)
- docs/* -> docs/* (keep as-is)
- Other patterns -> review manually
"""

import subprocess
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class BranchRenameMigrator:
    """Handles branch renaming migration to standardized naming conventions."""

    def __init__(self):
        self.rename_mappings = {
            r'^feat/': 'feature/',
            r'^fix/': 'bugfix/',
            # Add more mappings as needed
        }

    def get_all_branches(self) -> List[str]:
        """Get all local branches."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--format=%(refname:short)'],
                capture_output=True,
                text=True,
                check=True
            )
            branches = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            # Exclude main branches that shouldn't be renamed
            exclude_patterns = ['main', 'master', 'develop', 'scientific', 'staging', 'production']
            return [b for b in branches if not any(b.startswith(excl) for excl in exclude_patterns)]
        except subprocess.CalledProcessError as e:
            print(f"Error getting branches: {e}")
            return []

    def suggest_rename(self, branch_name: str) -> Tuple[str, str]:
        """
        Suggest a rename for a branch based on naming standards.

        Returns:
            Tuple of (original_name, suggested_name)
            If no rename needed, suggested_name will be the same as original_name
        """
        for pattern, replacement in self.rename_mappings.items():
            if re.match(pattern, branch_name):
                new_name = re.sub(pattern, replacement, branch_name, count=1)
                return branch_name, new_name

        # Check for other inconsistent patterns
        if branch_name.startswith(('feature-', 'fix-', 'bug-', 'refactor-', 'doc-')):
            # Convert dash to slash
            parts = branch_name.split('-', 1)
            if len(parts) == 2:
                category = parts[0]
                description = parts[1]
                # Map categories
                category_mapping = {
                    'feature': 'feature',
                    'fix': 'bugfix',
                    'bug': 'bugfix',
                    'refactor': 'refactor',
                    'doc': 'docs'
                }
                if category in category_mapping:
                    new_name = f"{category_mapping[category]}/{description}"
                    return branch_name, new_name

        return branch_name, branch_name

    def rename_branch(self, old_name: str, new_name: str, dry_run: bool = True) -> bool:
        """Rename a branch."""
        if old_name == new_name:
            print(f"ℹ️  Skipping {old_name} (no rename needed)")
            return True

        if dry_run:
            print(f"🔄 Would rename: {old_name} → {new_name}")
            return True

        try:
            # Rename the branch
            subprocess.run(['git', 'branch', '-m', old_name, new_name], check=True)
            print(f"✅ Renamed: {old_name} → {new_name}")

            # If this was the current branch, we need to update the remote tracking
            try:
                # Check if remote branch exists
                subprocess.run(
                    ['git', 'ls-remote', '--heads', 'origin', old_name],
                    capture_output=True,
                    check=True
                )

                # Delete old remote branch and push new one
                print(f"🔄 Updating remote branch...")
                subprocess.run(['git', 'push', 'origin', '--delete', old_name], check=False)
                subprocess.run(['git', 'push', '-u', 'origin', new_name], check=True)
                print(f"✅ Updated remote: {old_name} → {new_name}")

            except subprocess.CalledProcessError:
                print(f"ℹ️  No remote branch to update for {old_name}")

            return True

        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to rename {old_name}: {e}")
            return False

    def analyze_branches(self) -> Dict[str, List[Tuple[str, str]]]:
        """Analyze all branches and categorize them."""
        branches = self.get_all_branches()
        analysis = {
            'needs_rename': [],
            'already_correct': [],
            'manual_review': []
        }

        for branch in branches:
            original, suggested = self.suggest_rename(branch)

            if original != suggested:
                analysis['needs_rename'].append((original, suggested))
            elif self._is_standard_branch(branch):
                analysis['already_correct'].append(branch)
            else:
                analysis['manual_review'].append(branch)

        return analysis

    def _is_standard_branch(self, branch_name: str) -> bool:
        """Check if a branch follows the standard naming conventions."""
        standard_patterns = [
            r'^feature/',
            r'^bugfix/',
            r'^hotfix/',
            r'^refactor/',
            r'^docs/',
            r'^main$',
            r'^master$',
            r'^develop$',
            r'^scientific$'
        ]

        return any(re.match(pattern, branch_name) for pattern in standard_patterns)

    def execute_migration(self, dry_run: bool = True) -> bool:
        """Execute the branch migration."""
        print("🔍 Analyzing branches...")
        analysis = self.analyze_branches()

        print("
📊 Analysis Results:")
        print(f"   🔄 Branches needing rename: {len(analysis['needs_rename'])}")
        print(f"   ✅ Branches already correct: {len(analysis['already_correct'])}")
        print(f"   🤔 Branches needing manual review: {len(analysis['manual_review'])}")

        if analysis['needs_rename']:
            print("
🔄 Branches to rename:"            for old, new in analysis['needs_rename']:
                print(f"   {old} → {new}")

        if analysis['manual_review']:
            print("
🤔 Branches needing manual review:"            for branch in analysis['manual_review']:
                print(f"   {branch}")

        if not analysis['needs_rename']:
            print("\n✅ No branches need renaming!")
            return True

        if dry_run:
            print("
🔍 DRY RUN - No changes made. Use --execute to perform actual renaming."            return True

        print("
⚠️  EXECUTING BRANCH RENAMES..."        success_count = 0

        for old_name, new_name in analysis['needs_rename']:
            if self.rename_branch(old_name, new_name, dry_run=False):
                success_count += 1

        print(f"\n✅ Migration complete: {success_count}/{len(analysis['needs_rename'])} branches renamed")
        return success_count == len(analysis['needs_rename'])


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Branch naming standardization migration")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help="Show what would be renamed without making changes")
    parser.add_argument('--execute', action='store_true',
                       help="Actually perform the branch renaming")

    args = parser.parse_args()

    if args.execute:
        args.dry_run = False

    migrator = BranchRenameMigrator()
    success = migrator.execute_migration(dry_run=args.dry_run)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
