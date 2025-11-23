#!/usr/bin/env python3
"""
Backlog Organization and Deduplication Script

Organizes tasks into categories and handles deduplication based on analysis results.
"""

import os
import shutil
import yaml
from pathlib import Path
from typing import Dict, List, Set


class BacklogOrganizer:
    """Organizes and deduplicates backlog tasks."""

    def __init__(self, backlog_root: Path):
        self.backlog_root = backlog_root
        self.tasks_dir = backlog_root / "tasks"
        self.organized_dir = backlog_root / "organized"
        self.duplicates_dir = self.organized_dir / "duplicates_archived"

        # Category mappings based on task analysis
        self.categories = {
            'consolidation_migration': {
                'name': 'Consolidation & Migration',
                'keywords': ['consolidat', 'migrat', 'centraliz', 'distribut', 'worktree', 'orchestrat'],
                'tasks': []
            },
            'branch_management': {
                'name': 'Branch Management & Alignment',
                'keywords': ['branch', 'align', 'pr ', 'merge', 'extract', 'split'],
                'tasks': []
            },
            'validation_testing': {
                'name': 'Validation & Testing',
                'keywords': ['validat', 'test', 'verif', 'cleanup', 'post-merge'],
                'tasks': []
            },
            'documentation_research': {
                'name': 'Documentation & Research',
                'keywords': ['research', 'document', 'summary', 'expansion'],
                'tasks': []
            }
        }

        # Known duplicates from analysis
        self.known_duplicates = {
            'task-115.1': 'duplicate_of_task_116_hierarchy',
            'task-115.2': 'duplicate_of_task_116_hierarchy',
            'task-115.3': 'duplicate_of_task_116_hierarchy',
            'task-115.4': 'duplicate_of_task_116_hierarchy',
            'task-116': 'preferred_version_keep',  # Keep task-116 as it has 5 phases vs 115's 4
        }

    def read_task_content(self, task_file: Path) -> Dict:
        """Read and parse task file content."""
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract frontmatter
            frontmatter = {}
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    try:
                        frontmatter = yaml.safe_load(parts[1]) or {}
                        content_body = parts[2].strip()
                    except yaml.YAMLError:
                        content_body = content
                else:
                    content_body = content
            else:
                content_body = content

            return {
                'file_path': task_file,
                'filename': task_file.name,
                'frontmatter': frontmatter,
                'content': content_body,
                'full_content': content
            }
        except Exception as e:
            print(f"Error reading {task_file}: {e}")
            return {}

    def categorize_task(self, task_data: Dict) -> str:
        """Categorize a task based on its content and metadata."""
        content = task_data.get('content', '').lower()
        filename = task_data.get('filename', '').lower()
        title = task_data.get('frontmatter', {}).get('title', '').lower()

        # Combine all text for keyword matching
        search_text = f"{content} {filename} {title}"

        # Check each category
        for category, info in self.categories.items():
            for keyword in info['keywords']:
                if keyword.lower() in search_text:
                    return category

        # Default category
        return 'documentation_research'

    def is_duplicate(self, task_data: Dict) -> bool:
        """Check if task is a known duplicate."""
        task_id = task_data.get('frontmatter', {}).get('id', '')
        filename = task_data.get('filename', '')

        # Check known duplicates
        if task_id in self.known_duplicates:
            return self.known_duplicates[task_id] != 'preferred_version_keep'

        # Check filename patterns for duplicates
        if filename.startswith(('task-115.', 'task-116.')):
            return True

        return False

    def organize_tasks(self):
        """Main organization function."""
        print("🔄 Starting backlog organization...")

        if not self.tasks_dir.exists():
            print(f"❌ Tasks directory not found: {self.tasks_dir}")
            return

        # Ensure organized directories exist
        for category in self.categories.keys():
            category_dir = self.organized_dir / category
            category_dir.mkdir(parents=True, exist_ok=True)

        self.duplicates_dir.mkdir(parents=True, exist_ok=True)

        # Process all task files
        task_files = list(self.tasks_dir.glob("*.md"))
        print(f"📁 Found {len(task_files)} task files to organize")

        organized_count = 0
        duplicate_count = 0

        for task_file in task_files:
            task_data = self.read_task_content(task_file)
            if not task_data:
                continue

            if self.is_duplicate(task_data):
                # Move to duplicates archive
                dest_path = self.duplicates_dir / task_file.name
                shutil.copy2(task_file, dest_path)
                print(f"📋 Archived duplicate: {task_file.name} -> duplicates_archived/")
                duplicate_count += 1
            else:
                # Categorize and move
                category = self.categorize_task(task_data)
                category_dir = self.organized_dir / category
                dest_path = category_dir / task_file.name

                shutil.copy2(task_file, dest_path)
                self.categories[category]['tasks'].append(task_data)
                print(f"📂 Categorized: {task_file.name} -> {category}/")
                organized_count += 1

        # Create category summaries
        self.create_category_summaries()

        print("\n✅ Organization complete!")
        print(f"📂 Organized: {organized_count} tasks")
        print(f"📋 Archived: {duplicate_count} duplicates")
        print(f"📁 Categories created: {len(self.categories)}")

    def create_category_summaries(self):
        """Create summary files for each category."""
        for category, info in self.categories.items():
            category_dir = self.organized_dir / category
            summary_file = category_dir / "README.md"

            tasks = info['tasks']
            summary_content = f"""# {info['name']}

## Overview
This category contains tasks related to {info['name'].lower()}.

## Tasks ({len(tasks)} total)

"""

            for task in tasks:
                task_id = task.get('frontmatter', {}).get('id', 'unknown')
                title = task.get('frontmatter', {}).get('title', task['filename'])
                status = task.get('frontmatter', {}).get('status', 'Unknown')

                summary_content += f"""### {task_id}: {title}
- **Status:** {status}
- **File:** {task['filename']}

"""

            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)

            print(f"📝 Created summary: {category}/README.md")

    def create_master_summary(self):
        """Create a master summary of the organization."""
        summary_file = self.organized_dir / "ORGANIZATION_SUMMARY.md"

        total_tasks = sum(len(info['tasks']) for info in self.categories.values())

        summary_content = f"""# Backlog Organization Summary

## Overview
Backlog has been organized into categories with deduplication applied.

## Statistics
- **Total tasks processed:** {len(list(self.tasks_dir.glob('*.md')))}
- **Tasks organized:** {total_tasks}
- **Duplicates archived:** {len(list(self.duplicates_dir.glob('*.md')))}
- **Categories created:** {len(self.categories)}

## Categories

"""

        for category, info in self.categories.items():
            task_count = len(info['tasks'])
            summary_content += f"""### {info['name']}
- **Tasks:** {task_count}
- **Keywords:** {', '.join(info['keywords'])}
- **Location:** `organized/{category}/`

"""

        summary_content += """
## Duplicate Resolution

### Archived Duplicates
The following tasks were identified as duplicates and archived:
- All task-115.* subtasks (superseded by task-116.* hierarchy)
- Tasks with identical content and acceptance criteria

### Preferred Versions
- **Task 116**: Retained as it includes Phase 5 (Validation & Go-Live)
- **Task 115**: Archived (4 phases, missing Phase 5)

## Directory Structure
```
organized/
├── consolidation_migration/     # Script and system consolidation tasks
├── branch_management/          # Branch alignment and PR management
├── validation_testing/         # Post-merge validation and testing
├── documentation_research/     # Research summaries and documentation
└── duplicates_archived/        # Archived duplicate tasks
```

## Next Steps
1. Review organized tasks in each category
2. Update task dependencies and references
3. Implement the consolidated task plans
4. Monitor progress using the organized structure
"""

        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)

        print(f"📊 Created master summary: ORGANIZATION_SUMMARY.md")


def main():
    """Main execution function."""
    backlog_root = Path("/home/masum/github/backlog")

    organizer = BacklogOrganizer(backlog_root)
    organizer.organize_tasks()
    organizer.create_master_summary()

    print("\n🎉 Backlog organization complete!")
    print(f"📂 Organized tasks available in: {backlog_root}/organized/")
    print(f"📋 Archived duplicates in: {backlog_root}/organized/duplicates_archived/")


if __name__ == "__main__":
    main()