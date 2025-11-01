#!/usr/bin/env python3
"""
Branch Name Validator

This script validates branch names against the standardized naming conventions.

Usage:
    python scripts/validate_branch_name.py  # Validate current branch
    python scripts/validate_branch_name.py branch-name  # Validate specific branch name

Exit codes:
    0 - Branch name is valid
    1 - Branch name is invalid
    2 - Git error
"""

import subprocess
import re
import sys
from typing import Optional


class BranchNameValidator:
    """Validates branch names against standardized naming conventions."""

    def __init__(self):
        # Standard branch name patterns
        self.valid_patterns = [
            r'^feature/[a-z0-9-]+$',
            r'^bugfix/[a-z0-9-]+$',
            r'^hotfix/[a-z0-9-]+$',
            r'^refactor/[a-z0-9-]+$',
            r'^docs/[a-z0-9-]+$',
            r'^main$',
            r'^master$',
            r'^develop$',
            r'^scientific$',
            r'^staging$',
            r'^production$',
            r'^release/v\d+\.\d+\.\d+$',  # Release branches
        ]

    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting current branch: {e}", file=sys.stderr)
            return None

    def validate_branch_name(self, branch_name: str) -> bool:
        """
        Validate a branch name against naming standards.

        Args:
            branch_name: The branch name to validate

        Returns:
            True if valid, False otherwise
        """
        # Check if branch name matches any valid pattern
        for pattern in self.valid_patterns:
            if re.match(pattern, branch_name):
                return True

        return False

    def validate(self, branch_name: Optional[str] = None) -> bool:
        """
        Validate a branch name.

        Args:
            branch_name: Branch name to validate, or None to validate current branch

        Returns:
            True if valid, False otherwise
        """
        if branch_name is None:
            branch_name = self.get_current_branch()
            if branch_name is None:
                print("Error: Could not determine current branch", file=sys.stderr)
                return False

        if not branch_name:
            print("Error: Empty branch name", file=sys.stderr)
            return False

        is_valid = self.validate_branch_name(branch_name)

        if is_valid:
            print(f"✅ Branch name '{branch_name}' is valid")
        else:
            print(f"❌ Branch name '{branch_name}' is invalid")
            print("Valid patterns include:")
            print("  feature/description")
            print("  bugfix/description")
            print("  hotfix/description")
            print("  refactor/description")
            print("  docs/description")
            print("  release/vX.Y.Z")
            print("Where description contains only lowercase letters, numbers, and hyphens")

        return is_valid


def main():
    """Main entry point."""
    validator = BranchNameValidator()

    # If branch name provided as argument, validate that
    if len(sys.argv) > 1:
        branch_name = sys.argv[1]
        is_valid = validator.validate(branch_name)
        sys.exit(0 if is_valid else 1)

    # Otherwise validate current branch
    is_valid = validator.validate()
    sys.exit(0 if is_valid else 1)


if __name__ == '__main__':
    main()