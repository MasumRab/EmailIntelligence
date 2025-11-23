"""
PRD Parser for Task Extraction

Extracts tasks from Product Requirements Documents (PRDs) and converts them
into task format for consolidation.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class PRDParser:
    """Parses PRD files to extract tasks."""

    def __init__(self):
        self.fr_pattern = re.compile(r'\*\*FR-(\d+)\*\*: (.+)')
        self.sc_pattern = re.compile(r'\*\*SC-(\d+)\*\*: (.+)')
        self.user_story_pattern = re.compile(r'### User Story (\d+) - (.+) \(Priority: (P\d+)\)')

    def parse_prd_file(self, file_path: Path) -> List[Dict]:
        """Parse a PRD file and extract tasks."""
        tasks = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract feature branch info
            branch_match = re.search(r'\*\*Feature Branch\*\*: `([^`]+)`', content)
            branch = branch_match.group(1) if branch_match else "unknown"

            # Extract functional requirements as tasks
            fr_matches = self.fr_pattern.findall(content)
            for req_id, description in fr_matches:
                task = {
                    'task_id': f'prd-fr-{req_id}',
                    'title': f'FR-{req_id}: {description[:80]}...',
                    'status': 'pending',
                    'content': f'Functional Requirement {req_id}: {description}',
                    'branch': branch,
                    'file_path': str(file_path),
                    'full_content': f'# FR-{req_id}: {description}\n\n{description}',
                    'frontmatter': {
                        'id': f'prd-fr-{req_id}',
                        'title': f'FR-{req_id}: {description[:80]}...',
                        'status': 'pending',
                        'priority': 'medium'
                    }
                }
                tasks.append(task)

            # Extract success criteria as tasks
            sc_matches = self.sc_pattern.findall(content)
            for req_id, description in sc_matches:
                task = {
                    'task_id': f'prd-sc-{req_id}',
                    'title': f'SC-{req_id}: {description[:80]}...',
                    'status': 'pending',
                    'content': f'Success Criteria {req_id}: {description}',
                    'branch': branch,
                    'file_path': str(file_path),
                    'full_content': f'# SC-{req_id}: {description}\n\n{description}',
                    'frontmatter': {
                        'id': f'prd-sc-{req_id}',
                        'title': f'SC-{req_id}: {description[:80]}...',
                        'status': 'pending',
                        'priority': 'medium'
                    }
                }
                tasks.append(task)

            # Extract user stories as tasks
            story_matches = self.user_story_pattern.findall(content)
            for story_id, title, priority in story_matches:
                task = {
                    'task_id': f'prd-us-{story_id}',
                    'title': f'User Story {story_id}: {title[:80]}...',
                    'status': 'pending',
                    'content': f'User Story {story_id} - {title} (Priority: {priority})',
                    'branch': branch,
                    'file_path': str(file_path),
                    'full_content': f'# User Story {story_id}: {title}\n\n**Priority:** {priority}\n\n{title}',
                    'frontmatter': {
                        'id': f'prd-us-{story_id}',
                        'title': f'User Story {story_id}: {title[:80]}...',
                        'status': 'pending',
                        'priority': priority.lower().replace('p', 'high') if priority == 'P1' else 'medium'
                    }
                }
                tasks.append(task)

        except Exception as e:
            print(f"Error parsing PRD file {file_path}: {e}")

        return tasks

    def parse_all_prd_files(self, docs_dir: Path) -> List[Dict]:
        """Parse all PRD files in the docs directory."""
        all_tasks = []

        prd_files = list(docs_dir.glob("*.txt")) + list(docs_dir.glob("*.md"))

        for prd_file in prd_files:
            if 'prd' in prd_file.name.lower():
                print(f"Parsing PRD file: {prd_file}")
                tasks = self.parse_prd_file(prd_file)
                all_tasks.extend(tasks)
                print(f"  Extracted {len(tasks)} tasks")

        return all_tasks


if __name__ == "__main__":
    parser = PRDParser()
    docs_dir = Path("/home/masum/github/EmailIntelligence/.taskmaster/docs")
    tasks = parser.parse_all_prd_files(docs_dir)

    print(f"\nTotal PRD tasks extracted: {len(tasks)}")
    for task in tasks[:5]:  # Show first 5 tasks
        print(f"- {task['task_id']}: {task['title']}")