#!/usr/bin/env python3
"""
Backlog Consolidated Files Generation Script
Phase 5 of Backlog Consolidation Plan

This script generates the final consolidated backlog files in searchable,
organized formats including markdown files, JSON indexes, and search databases.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

class ConsolidatedFilesGenerator:
    def __init__(self, reorganized_tasks_file: str, relationships_file: str):
        self.reorganized_tasks_file = reorganized_tasks_file
        self.relationships_file = relationships_file
        self.tasks = []
        self.relationships = {}
        self.categories = {}

    def load_data(self):
        """Load reorganized tasks and relationships"""
        # Load reorganized tasks
        with open(self.reorganized_tasks_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.categories = data['categories']

            # Flatten tasks with category information
            for category_key, category_data in self.categories.items():
                for task in category_data['tasks']:
                    task['category_key'] = category_key
                    task['category_name'] = category_data['name']
                    self.tasks.append(task)

        # Load relationships
        with open(self.relationships_file, 'r', encoding='utf-8') as f:
            rel_data = json.load(f)
            self.relationships = rel_data['relationships']

        print(f"Loaded {len(self.tasks)} tasks and relationship data")

    def normalize_status(self, status: str) -> str:
        """Normalize status values to standard format"""
        if not status:
            return 'todo'

        status_lower = status.lower().strip()

        # Map various status formats to standard ones
        status_mapping = {
            'to do': 'todo',
            'in progress': 'in-progress',
            'in-progress': 'in-progress',
            'pending': 'pending',
            'done': 'done',
            'completed': 'done',
            'deferred': 'deferred',
            'cancelled': 'cancelled',
            'not started': 'pending',
            'todo': 'todo'
        }

        return status_mapping.get(status_lower, 'todo')

    def generate_category_markdown_files(self):
        """Generate individual markdown files for each category"""
        output_dir = Path("backlog/consolidated/categories")
        output_dir.mkdir(parents=True, exist_ok=True)

        for category_key, category_data in self.categories.items():
            tasks = category_data['tasks']

            # Sort tasks by priority and status
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            status_order = {'in-progress': 0, 'pending': 1, 'todo': 2, 'done': 3, 'deferred': 4, 'cancelled': 5}

            tasks.sort(key=lambda t: (
                priority_order.get(t.get('priority', 'medium'), 1),
                status_order.get(t.get('status', 'todo'), 2),
                t.get('title', '')
            ))

            # Generate markdown content
            content = f"# {category_data['name']}\n\n"
            content += f"{category_data['description']}\n\n"
            content += f"**Total Tasks:** {len(tasks)}\n\n"

            # Group tasks by status (normalize status values)
            status_groups = {}
            for task in tasks:
                raw_status = task.get('status', 'todo')
                # Normalize status values
                status = self.normalize_status(raw_status)
                if status not in status_groups:
                    status_groups[status] = []
                status_groups[status].append(task)

            for status in ['in-progress', 'pending', 'todo', 'done', 'deferred', 'cancelled']:
                if status in status_groups:
                    status_tasks = status_groups[status]
                    content += f"## {status.replace('-', ' ').title()} ({len(status_tasks)} tasks)\n\n"

                    for task in status_tasks:
                        content += self.format_task_as_markdown(task)
                        content += "\n---\n\n"

            # Save category file
            filename = f"{category_key}.md"
            with open(output_dir / filename, 'w', encoding='utf-8') as f:
                f.write(content)

        print(f"✅ Generated {len(self.categories)} category markdown files")

    def format_task_as_markdown(self, task: Dict) -> str:
        """Format a single task as markdown"""
        content = ""

        # Title
        title = task.get('title', 'Unknown Title')
        if title == 'Unknown Title' or not title.strip():
            # Try to extract a better title from source file
            source_file = task.get('source_file', '')
            if source_file:
                # Extract filename without extension and path
                filename = source_file.split('/')[-1]
                if filename.endswith('.md'):
                    filename = filename[:-3]
                # Remove task- prefix and numbers
                filename = re.sub(r'^task-\d+\s*-\s*', '', filename)
                filename = re.sub(r'^task-\d+', '', filename)
                # Replace dashes with spaces and capitalize
                title = filename.replace('-', ' ').strip()
                title = ' '.join(word.capitalize() for word in title.split())
            else:
                title = f"Task {task.get('id', 'unknown')}"

        content += f"### {title}\n\n"

        # Metadata
        content += f"**ID:** {task.get('id', 'unknown')}\n"
        content += f"**Status:** {task.get('status', 'todo').replace('-', ' ').title()}\n"
        content += f"**Priority:** {task.get('priority', 'medium').title()}\n"

        if task.get('assignees'):
            assignees = task['assignees']
            if isinstance(assignees, list):
                content += f"**Assignees:** {', '.join(assignees)}\n"
            else:
                content += f"**Assignees:** {assignees}\n"

        if task.get('labels'):
            labels = task['labels']
            if isinstance(labels, list):
                content += f"**Labels:** {', '.join(labels)}\n"
            else:
                content += f"**Labels:** {labels}\n"

        content += "\n"

        # Description
        if task.get('description'):
            desc = self.clean_markdown_content(task['description'])
            content += f"**Description:**\n{desc}\n\n"

        # Acceptance Criteria
        if task.get('acceptance_criteria'):
            ac = self.clean_markdown_content(task['acceptance_criteria'])
            content += f"**Acceptance Criteria:**\n{ac}\n\n"

        # Dependencies
        if task.get('dependencies'):
            deps = task['dependencies']
            if isinstance(deps, list) and deps:
                content += f"**Dependencies:** {', '.join(deps)}\n\n"

        # Relationships
        task_id = task.get('id')
        if task_id and task_id in self.relationships.get('depends_on', {}):
            deps = self.relationships['depends_on'][task_id]
            if deps:
                content += f"**Depends On:** {', '.join(deps)}\n\n"

        if task_id and task_id in self.relationships.get('blocks', {}):
            blocks = self.relationships['blocks'][task_id]
            if blocks:
                content += f"**Blocks:** {', '.join(blocks)}\n\n"

        if task_id and task_id in self.relationships.get('parent_of', {}):
            children = self.relationships['parent_of'][task_id]
            if children:
                content += f"**Subtasks:** {', '.join(children)}\n\n"

        # Source
        if task.get('source_file'):
            content += f"**Source:** {task['source_file']}\n\n"

        return content

    def clean_markdown_content(self, content: str) -> str:
        """Clean and format markdown content"""
        if not content:
            return ""

        # Remove HTML comments
        content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

        # Ensure proper line breaks
        content = content.strip()
        if not content.startswith('\n'):
            content = '\n' + content

        return content

    def generate_search_index(self):
        """Generate a searchable JSON index of all tasks"""
        search_index = {
            'metadata': {
                'generated_date': datetime.now().isoformat(),
                'total_tasks': len(self.tasks),
                'categories': list(self.categories.keys())
            },
            'tasks': []
        }

        for task in self.tasks:
            # Create searchable content
            searchable_content = self.create_searchable_content(task)

            index_entry = {
                'id': task.get('id'),
                'title': task.get('title', ''),
                'status': task.get('status', 'todo'),
                'priority': task.get('priority', 'medium'),
                'category': task.get('category_name', ''),
                'category_key': task.get('category_key', ''),
                'assignees': task.get('assignees', []),
                'labels': task.get('labels', []),
                'searchable_content': searchable_content,
                'relationships': self.get_task_relationships(task.get('id')),
                'source_file': task.get('source_file', '')
            }

            search_index['tasks'].append(index_entry)

        # Save search index
        output_dir = Path("backlog/consolidated")
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / "search_index.json", 'w', encoding='utf-8') as f:
            json.dump(search_index, f, indent=2, ensure_ascii=False)

        print("✅ Generated searchable JSON index")

    def create_searchable_content(self, task: Dict) -> str:
        """Create searchable content from task data"""
        content_parts = [
            task.get('title', ''),
            task.get('description', ''),
            task.get('acceptance_criteria', ''),
            task.get('category_name', ''),
            task.get('source_file', '')
        ]

        if task.get('assignees'):
            assignees = task['assignees']
            if isinstance(assignees, list):
                content_parts.extend(assignees)
            else:
                content_parts.append(str(assignees))

        if task.get('labels'):
            labels = task['labels']
            if isinstance(labels, list):
                content_parts.extend(labels)
            else:
                content_parts.append(str(labels))

        # Normalize and join
        content = ' '.join(content_parts)
        content = re.sub(r'[^\w\s]', ' ', content)
        content = re.sub(r'\s+', ' ', content)
        return content.lower().strip()

    def get_task_relationships(self, task_id: str) -> Dict[str, List[str]]:
        """Get all relationships for a task"""
        if not task_id:
            return {}

        relationships = {}
        for rel_type, rel_data in self.relationships.items():
            if task_id in rel_data:
                relationships[rel_type] = rel_data[task_id]

        return relationships

    def generate_master_backlog_file(self):
        """Generate a master backlog file with all tasks organized by category"""
        output_dir = Path("backlog/consolidated")
        output_dir.mkdir(parents=True, exist_ok=True)

        content = "# EmailIntelligenceQwen Backlog\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"**Total Tasks:** {len(self.tasks)}\n\n"

        # Add category overview
        content += "## Category Overview\n\n"
        for category_key, category_data in self.categories.items():
            task_count = category_data['task_count']
            content += f"- **{category_data['name']}:** {task_count} tasks\n"
        content += "\n"

        # Add tasks by category
        for category_key, category_data in self.categories.items():
            content += f"## {category_data['name']}\n\n"
            content += f"{category_data['description']}\n\n"

            tasks = category_data['tasks']
            # Sort by priority and status
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            status_order = {'in-progress': 0, 'pending': 1, 'todo': 2, 'done': 3}

            tasks.sort(key=lambda t: (
                priority_order.get(t.get('priority', 'medium'), 1),
                status_order.get(t.get('status', 'todo'), 2)
            ))

            for task in tasks:
                title = task.get('title', f"Task {task.get('id', 'unknown')}")
                status = task.get('status', 'todo')
                priority = task.get('priority', 'medium')

                content += f"### {title}\n\n"
                content += f"**Status:** {status.replace('-', ' ').title()} | "
                content += f"**Priority:** {priority.title()} | "
                content += f"**ID:** {task.get('id', 'unknown')}\n\n"

                if task.get('description'):
                    desc = self.clean_markdown_content(task['description'])
                    content += f"**Description:**{desc}\n\n"

                content += "---\n\n"

        # Save master file
        with open(output_dir / "master_backlog.md", 'w', encoding='utf-8') as f:
            f.write(content)

        print("✅ Generated master backlog markdown file")

    def generate_statistics_report(self):
        """Generate a statistics report of the consolidated backlog"""
        output_dir = Path("backlog/consolidated")
        output_dir.mkdir(parents=True, exist_ok=True)

        # Calculate statistics
        stats = {
            'total_tasks': len(self.tasks),
            'categories': {},
            'status_distribution': {},
            'priority_distribution': {},
            'relationships': {}
        }

        # Category stats
        for category_key, category_data in self.categories.items():
            stats['categories'][category_key] = {
                'name': category_data['name'],
                'count': category_data['task_count'],
                'percentage': round(category_data['task_count'] / len(self.tasks) * 100, 1)
            }

        # Status distribution
        status_counts = {}
        for task in self.tasks:
            status = task.get('status', 'todo')
            status_counts[status] = status_counts.get(status, 0) + 1
        stats['status_distribution'] = status_counts

        # Priority distribution
        priority_counts = {}
        for task in self.tasks:
            priority = task.get('priority', 'medium')
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        stats['priority_distribution'] = priority_counts

        # Relationship stats
        for rel_type, rel_data in self.relationships.items():
            if rel_type == 'part_of':
                stats['relationships'][rel_type] = len(rel_data)
            else:
                stats['relationships'][rel_type] = sum(len(rel_list) for rel_list in rel_data.values())

        # Generate markdown report
        content = "# Backlog Consolidation Statistics Report\n\n"
        content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"**Total Tasks:** {stats['total_tasks']}\n\n"

        content += "## Category Distribution\n\n"
        for cat_key, cat_stats in stats['categories'].items():
            content += f"- **{cat_stats['name']}:** {cat_stats['count']} tasks ({cat_stats['percentage']}%)\n"
        content += "\n"

        content += "## Status Distribution\n\n"
        for status, count in stats['status_distribution'].items():
            percentage = round(count / stats['total_tasks'] * 100, 1)
            content += f"- **{status.replace('-', ' ').title()}:** {count} tasks ({percentage}%)\n"
        content += "\n"

        content += "## Priority Distribution\n\n"
        for priority, count in stats['priority_distribution'].items():
            percentage = round(count / stats['total_tasks'] * 100, 1)
            content += f"- **{priority.title()}:** {count} tasks ({percentage}%)\n"
        content += "\n"

        content += "## Relationship Summary\n\n"
        for rel_type, count in stats['relationships'].items():
            content += f"- **{rel_type.replace('_', ' ').title()}:** {count} relationships\n"
        content += "\n"

        # Save report
        with open(output_dir / "statistics_report.md", 'w', encoding='utf-8') as f:
            f.write(content)

        # Save JSON stats
        with open(output_dir / "statistics.json", 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)

        print("✅ Generated statistics report")

    def generate_all_files(self):
        """Generate all consolidated files"""
        print("Generating consolidated backlog files...")

        self.generate_category_markdown_files()
        self.generate_search_index()
        self.generate_master_backlog_file()
        self.generate_statistics_report()

        print("✅ All consolidated files generated successfully")

def main():
    generator = ConsolidatedFilesGenerator(
        "backlog/reorganization/reorganized_tasks.json",
        "backlog/relationships/task_relationships.json"
    )
    generator.load_data()
    generator.generate_all_files()

    print("\n📊 CONSOLIDATION COMPLETE:")
    print("  • Category-specific markdown files")
    print("  • Searchable JSON index")
    print("  • Master backlog file")
    print("  • Statistics report")
    print("  • All files saved to backlog/consolidated/")

if __name__ == "__main__":
    main()