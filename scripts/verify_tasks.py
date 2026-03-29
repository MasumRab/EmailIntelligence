#!/usr/bin/env python3
"""
Task Verification Framework

This script verifies completed backlog tasks against their acceptance criteria.
It performs automated checks where possible and generates a verification report.
"""

import os
import re
import glob
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple

class TaskVerifier:
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.tasks_dir = self.repo_root / "backlog" / "tasks"
        self.src_dir = self.repo_root / "src"
        self.tests_dir = self.repo_root / "tests"
        self.docs_dir = self.repo_root / "docs"

    def get_completed_tasks(self) -> List[Path]:
        """Get all completed task files."""
        completed = []
        for task_file in self.tasks_dir.glob("*.md"):
            with open(task_file, 'r') as f:
                content = f.read()
                if re.search(r'status:\s*(Done|Completed)', content, re.IGNORECASE):
                    completed.append(task_file)
        return sorted(completed)

    def parse_task(self, task_file: Path) -> Dict:
        """Parse task file to extract metadata and AC."""
        with open(task_file, 'r') as f:
            content = f.read()

        # Extract frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        frontmatter = {}
        if frontmatter_match:
            for line in frontmatter_match.group(1).split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip()

        # Extract acceptance criteria
        ac_match = re.search(r'<!-- AC:BEGIN -->(.*?)<!-- AC:END -->', content, re.DOTALL)
        ac_items = []
        if ac_match:
            ac_content = ac_match.group(1)
            # Find checked items
            checked_items = re.findall(r'- \[x\]\s*#(\d+)\s*(.+)', ac_content)
            unchecked_items = re.findall(r'- \[ \]\s*#(\d+)\s*(.+)', ac_content)
            ac_items = [(int(num), text.strip(), True) for num, text in checked_items] + \
                      [(int(num), text.strip(), False) for num, text in unchecked_items]
            ac_items.sort(key=lambda x: x[0])

        # Extract implementation notes
        notes_match = re.search(r'<!-- SECTION:NOTES:BEGIN -->(.*?)<!-- SECTION:NOTES:END -->', content, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""

        return {
            'id': frontmatter.get('id', task_file.stem),
            'title': frontmatter.get('title', ''),
            'status': frontmatter.get('status', ''),
            'acceptance_criteria': ac_items,
            'implementation_notes': notes,
            'file': task_file
        }

    def check_file_exists(self, file_path: str) -> bool:
        """Check if a file exists in the repository."""
        return (self.repo_root / file_path).exists()

    def check_test_exists(self, test_name: str) -> bool:
        """Check if test files exist for a given component."""
        # Look for test files matching the component
        test_patterns = [
            f"test_{test_name}.py",
            f"test_{test_name}_*.py",
            f"*{test_name}*test*.py"
        ]
        for pattern in test_patterns:
            if list(self.tests_dir.rglob(pattern)):
                return True
        return False

    def check_code_implementation(self, task_data: Dict) -> Dict:
        """Perform automated checks on task implementation."""
        checks = {
            'files_exist': [],
            'tests_exist': [],
            'docs_updated': False,
            'code_changes': False
        }

        notes = task_data['implementation_notes'].lower()
        title = task_data['title'].lower()

        # Check for file creation mentions
        file_mentions = re.findall(r'created?\s+([^,\n.]+)', notes)
        for mention in file_mentions:
            if '.' in mention:  # Likely a file
                checks['files_exist'].append(self.check_file_exists(mention.strip()))

        # Check for test mentions
        if 'test' in notes or 'testing' in notes:
            checks['tests_exist'].append(self.check_test_exists(title.split()[0]))

        # Check for documentation updates
        if 'doc' in notes or 'readme' in notes or 'guide' in notes:
            # Check if docs were recently modified (simplified check)
            checks['docs_updated'] = bool(list(self.docs_dir.glob("*.md")))

        # Check for code changes
        if any(keyword in notes for keyword in ['implement', 'add', 'create', 'update', 'refactor']):
            checks['code_changes'] = True

        return checks

    def verify_task(self, task_file: Path) -> Dict:
        """Verify a single task."""
        task_data = self.parse_task(task_file)

        verification = {
            'task_id': task_data['id'],
            'title': task_data['title'],
            'status': task_data['status'],
            'ac_count': len(task_data['acceptance_criteria']),
            'ac_checked': sum(1 for _, _, checked in task_data['acceptance_criteria'] if checked),
            'automated_checks': self.check_code_implementation(task_data),
            'manual_verification_needed': True,  # Most tasks need manual review
            'issues': []
        }

        # Basic validation
        if verification['ac_checked'] != verification['ac_count']:
            verification['issues'].append(f"Only {verification['ac_checked']}/{verification['ac_count']} AC checked")

        if not task_data['implementation_notes']:
            verification['issues'].append("Missing implementation notes")

        return verification

    def generate_report(self, verifications: List[Dict]) -> str:
        """Generate a verification report."""
        report = ["# Task Verification Report\n"]
        report.append(f"Total completed tasks: {len(verifications)}\n")

        issues_found = 0
        for v in verifications:
            issues_found += len(v['issues'])

        report.append(f"Tasks with issues: {issues_found}\n")
        report.append("---\n")

        for v in verifications:
            report.append(f"## {v['task_id']}: {v['title']}\n")
            report.append(f"Status: {v['status']}\n")
            report.append(f"AC: {v['ac_checked']}/{v['ac_count']} checked\n")

            if v['automated_checks']['files_exist']:
                report.append(f"Files checked: {sum(v['automated_checks']['files_exist'])}/{len(v['automated_checks']['files_exist'])} exist\n")

            if v['issues']:
                report.append("Issues:\n")
                for issue in v['issues']:
                    report.append(f"- {issue}\n")

            report.append("\n")

        return "".join(report)

    def run_verification(self) -> str:
        """Run verification on all completed tasks."""
        completed_tasks = self.get_completed_tasks()
        verifications = []

        for task_file in completed_tasks:
            try:
                verification = self.verify_task(task_file)
                verifications.append(verification)
            except Exception as e:
                verifications.append({
                    'task_id': task_file.stem,
                    'title': 'Error parsing task',
                    'issues': [str(e)]
                })

        return self.generate_report(verifications)

if __name__ == "__main__":
    verifier = TaskVerifier()
    report = verifier.run_verification()
    print(report)

    # Save report
    with open("task_verification_report.md", "w") as f:
        f.write(report)