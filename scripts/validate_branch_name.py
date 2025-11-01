#!/usr/bin/env python3
"""
Branch Name Validation Script

Validates branch names against the standardized naming conventions.

Usage:
    python scripts/validate_branch_name.py [branch_name]
    python scripts/validate_branch_name.py --current  # Validate current branch
    python scripts/validate_branch_name.py --ci       # CI/CD mode with exit codes

Exit codes:
    0: Valid branch name
    1: Invalid branch name
    2: Error occurred
"""

import re
import subprocess
import sys
from typing import Optional


class BranchNameValidator:
    """Validates branch names against naming standards."""

    VALID_PATTERNS = [
        r'^feature/[a-z0-9][a-z0-9-]*[a-z0-9]$',  # feature/short-description
        r'^bugfix/[a-z0-9][a-z0-9-]*[a-z0-9]$',  # bugfix/short-description
        r'^hotfix/[a-z0-9][a-z0-9-]*[a-z0-9]$',  # hotfix/short-description
        r'^refactor/[a-z0-9][a-z0-9-]*[a-z0-9]$', # refactor/short-description
        r'^docs/[a-z0-9][a-z0-9-]*[a-z0-9]$',    # docs/short-description
        r'^main$',                                         # main branch
        r'^master$',                                       # master branch (legacy)
        r'^develop$',                                      # develop branch
        r'^scientific$',                                   # scientific branch
        r'^staging$',                                      # staging branch
        r'^production$',                                   # production branch
        r'^release/v\d+\.\d+\.\d+$',                      # release branches
    ]

    EXCLUDED_BRANCHES = [
        'HEAD',
        'origin/HEAD',
        'origin/main',
        'origin/master',
        'origin/develop',
        'origin/scientific',
    ]

    def __init__(self):
        self.patterns = [re.compile(pattern) for pattern in self.VALID_PATTERNS]

    def validate_branch_name(self, branch_name: str) -> tuple[bool, str]:
        """
        Validate a branch name.

        Returns:
            Tuple of (is_valid, message)
        """
        if not branch_name or not branch_name.strip():
            return False, "Branch name cannot be empty"

        branch_name = branch_name.strip()

        if branch_name in self.EXCLUDED_BRANCHES:
            return True, f"Branch '{branch_name}' is excluded from validation"

        # Check against valid patterns
        for pattern in self.patterns:
            if pattern.match(branch_name):
                return True, f"Branch name '{branch_name}' follows naming standards"

        # Provide helpful suggestions
        suggestions = self._get_suggestions(branch_name)
        suggestion_text = f" Consider: {', '.join(suggestions[:3])}" if suggestions else ""

        return False, f"Branch name '{branch_name}' does not follow naming standards.{suggestion_text}"

    def _get_suggestions(self, branch_name: str) -> list[str]:
        """Generate helpful suggestions for invalid branch names."""
        suggestions = []

        # Try to infer the intended category
        lower_name = branch_name.lower()

        if any(word in lower_name for word in ['feat', 'feature', 'new', 'add']):
            suggestions.append(f"feature/{branch_name.replace('feature', '').replace('feat', '').strip('-')}")
        elif any(word in lower_name for word in ['fix', 'bug', 'issue', 'error']):
            suggestions.append(f"bugfix/{branch_name.replace('fix', '').replace('bug', '').strip('-')}")
        elif any(word in lower_name for word in ['refactor', 'restructure', 'cleanup']):
            suggestions.append(f"refactor/{branch_name.replace('refactor', '').strip('-')}")
        elif any(word in lower_name for word in ['doc', 'docs', 'readme', 'guide']):
            suggestions.append(f"docs/{branch_name.replace('doc', '').replace('docs', '').strip('-')}")

        # Convert dash-separated to slash-separated
        if '-' in branch_name and '/' not in branch_name:
            parts = branch_name.split('-', 1)
            if len(parts) == 2 and parts[0] in ['feature', 'fix', 'bug', 'refactor', 'doc']:
                category_map = {'fix': 'bugfix', 'bug': 'bugfix', 'doc': 'docs'}
                category = category_map.get(parts[0], parts[0])
                suggestions.append(f"{category}/{parts[1]}")

        return suggestions[:3]  # Limit to 3 suggestions

    def get_current_branch(self) -> Optional[str]:
        """Get the current branch name."""
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError:
            return None


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate branch names against naming standards")
    parser.add_argument('branch_name', nargs='?', help="Branch name to validate")
    parser.add_argument('--current', action='store_true', help="Validate the current branch")
    parser.add_argument('--ci', action='store_true', help="CI mode: exit with code 1 for invalid names")

    args = parser.parse_args()

    validator = BranchNameValidator()

    if args.current:
        branch_name = validator.get_current_branch()
        if not branch_name:
            print("❌ Error: Could not determine current branch name", file=sys.stderr)
            sys.exit(2)
    elif args.branch_name:
        branch_name = args.branch_name
    else:
        parser.print_help()
        sys.exit(1)

    is_valid, message = validator.validate_branch_name(branch_name)

    if is_valid:
        print(f"✅ {message}")
        if args.ci:
            print(f"::set-output name=branch_valid::{is_valid}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        if args.ci:
            print(f"::set-output name=branch_valid::{is_valid}")
            print(f"::set-output name=validation_message::{message}")
        sys.exit(1 if args.ci else 0)


if __name__ == '__main__':
    main()
