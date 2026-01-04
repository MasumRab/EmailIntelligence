#!/usr/bin/env python3
"""
Validate markdown documentation using linting rules.

Usage:
    python markdownlint_check.py --fix
    python markdownlint_check.py --validate-only
    python markdownlint_check.py --check-links
"""

import re
import json
import sys
import subprocess
from pathlib import Path
from datetime import datetime


class MarkdownValidator:
    def __init__(self, docs_dir="docs"):
        self.docs_dir = Path(docs_dir)
        self.errors = []
        self.warnings = []
        self.fixes = 0

    def validate_task_file(self, file_path):
        """Validate a single task file for consistency."""
        errors = []
        warnings = []

        try:
            content = file_path.read_text()
            lines = content.split("\n")

            # Check for basic markdown structure
            if not lines or not lines[0].strip().startswith("# "):
                errors.append("Missing or empty task title")

            # Check for consistent heading levels
            heading_level = None
            for i, line in enumerate(lines, 1):
                if line.startswith("# "):
                    level = line.count(" ")
                    if heading_level is None:
                        heading_level = level
                    elif abs(level - heading_level) > 1:
                        errors.append(
                            f"Line {i + 1}: Heading level jumped (from {heading_level} to {level})"
                        )

            # Check for proper task ID format
            task_ids = set()
            for line in lines:
                match = re.match(r"^# Task (\d+)", line)
                if match:
                    task_id = match.group(1)
                    if task_id in task_ids:
                        errors.append(f"Line {i + 1}: Duplicate task ID {task_id}")
                    else:
                        task_ids.add(task_id)

            # Check for consistent formatting
            success_criteria_section = False
            subtasks_section = False
            for line in lines:
                if "## Success Criteria" in line:
                    success_criteria_section = True
                elif "## Subtasks" in line:
                    subtasks_section = True

            if success_criteria_section and not subtasks_section:
                warnings.append("Success Criteria section found but no Subtasks section")

            if subtasks_section and not success_criteria_section:
                warnings.append("Subtasks section found but no Success Criteria section")

            # Check for proper field ordering (Purpose before Success Criteria before Subtasks)
            purpose_idx = None
            success_idx = None
            subtasks_idx = None
            for i, line in enumerate(lines, 1):
                line_stripped = line.strip().lower()
                if "## Purpose" in line_stripped:
                    purpose_idx = i
                elif "## Success Criteria" in line_stripped:
                    success_idx = i
                elif "## Subtasks" in line_stripped:
                    subtasks_idx = i

            if all([purpose_idx, success_idx, subtasks_idx]):
                errors.append("Missing or improperly ordered sections")
            elif purpose_idx < success_idx and success_idx < subtasks_idx:
                errors.append(
                    "Sections out of order: Purpose before Success Criteria before Subtasks"
                )

        except Exception as e:
            errors.append(f"Error reading file: {e}")

        return errors, warnings, self.apply_fixes(file_path, errors, warnings)

    def check_internal_links(self, file_path):
        """Check for broken internal links in task file."""
        try:
            content = file_path.read_text()

            # Check for common broken patterns
            broken_patterns = [
                r"\[backlog/tasks/[^\]]*\]",  # Backlog references
                r"\[outdated\]",  # Outdated references
                r"Task_data/[^\]]*\]",  # Legacy data dir references
                r"tasks\.json",  # Deprecated JSON references
            ]

            for pattern in broken_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    warnings.append(f"Found {len(matches)} broken references: {pattern}")

        except Exception as e:
            errors.append(f"Error checking links: {e}")

        return errors, warnings, []

    def check_relative_paths(self, file_path):
        """Check for relative path references."""
        try:
            content = file_path.read_text()
            rel_paths = re.findall(r"\.\.\/.*\.(md|txt|json)", content)
            if rel_paths:
                warnings.append(f"Found {len(rel_paths)} relative path references")

        except Exception as e:
            errors.append(f"Error checking paths: {e}")

        return [], warnings

    def apply_fixes(self, file_path, errors, warnings):
        """Apply simple fixes for common issues."""
        try:
            content = file_path.read_text()
            fixed_content = content

            # Fix missing task title
            fixed_content = re.sub(r"^# Task\s*$", "# Task XXX - MISSING TITLE", fixed_content)

            # Fix broken internal links (comment out for now)
            fixed_content = re.sub(
                r"\[backlog/[^\]]*\]", "[BROKEN LINK: backlog/...]", fixed_content
            )
            fixed_content = re.sub(r"\[outdated\]", "[OUTDATED REFERENCE]", fixed_content)
            fixed_content = re.sub(
                r"\[task_data/[^\]]*\]", "[LEGACY DATA REFERENCE]", fixed_content
            )
            fixed_content = re.sub(r"tasks\.json", "[DEPRECATED REFERENCE]", fixed_content)

            if content != fixed_content:
                file_path.write_text(fixed_content)
                self.fixes += 1
                print(f"Fixed {file_path.name}")
            else:
                print(f"No fixes needed for {file_path.name}")

        except Exception as e:
            print(f"Error fixing {file_path.name}: {e}")

    def validate_all(self):
        """Validate all documentation files."""
        all_errors = []
        all_warnings = []

        task_files = list(self.docs_dir.glob("task-*.md"))

        for task_file in task_files:
            errors, warnings = self.validate_task_file(task_file)
            all_errors.extend(errors)
            all_warnings.extend(warnings)
            errors, warnings = self.check_internal_links(task_file)
            all_errors.extend(errors)
            all_warnings.extend(warnings)
            errors, warnings = self.check_relative_paths(task_file)
            all_errors.extend(errors)
            all_warnings.extend(warnings)

        if all_errors or all_warnings:
            print(
                f"Found {len(all_errors)} errors and {len(all_warnings)} warnings across {len(task_files)} files"
            )
        else:
            print(f"All {len(task_files)} files validated successfully")

        return all_errors, all_warnings


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Validate markdown documentation and fix issues")
    parser.add_argument("--fix", action="store_true", help="Apply fixes automatically")
    parser.add_argument("--validate-only", action="store_true", help="Only validate without fixing")
    parser.add_argument(
        "--check-links", action="store_true", help="Check for broken internal/external links"
    )
    parser.add_argument("docs_dir", default="docs", help="Documentation directory")

    args = parser.parse_args()

    validator = MarkdownValidator(args.docs_dir)

    if args.validate_only:
        validator.validate_all()
    elif args.fix:
        task_files = list(validator.docs_dir.glob("task-*.md"))
        for task_file in task_files:
            errors, warnings = validator.validate_task_file(task_file)
            validator.apply_fixes(task_file, errors, warnings)

    print(f"\nValidation complete. Total fixes applied: {validator.fixes}")


if __name__ == "__main__":
    main()
