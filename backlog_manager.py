#!/usr/bin/env python3
"""
Backlog Management System

This script provides a command-line interface for managing the project's backlog system,
allowing you to list, create, update, and manage tasks stored as markdown files.
"""

import argparse
import os
import glob
import yaml
from pathlib import Path
from datetime import datetime
import re


class BacklogManager:
    def __init__(self, backlog_dir="backlog"):
        self.backlog_dir = Path(backlog_dir)
        self.tasks_dir = self.backlog_dir / "tasks"
        self.deferred_dir = self.backlog_dir / "deferred"
        self.config_file = self.backlog_dir / "config.yml"
        
        # Load config
        self.config = {}
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = yaml.safe_load(f) or {}

    def _parse_task_file(self, file_path):
        """Parse a markdown task file and extract metadata."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract frontmatter if it exists
        frontmatter = {}
        content_without_frontmatter = content
        
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter_content = parts[1]
                content_without_frontmatter = parts[2]
                
                # Parse the frontmatter as YAML
                try:
                    frontmatter = yaml.safe_load(frontmatter_content)
                except yaml.YAMLError:
                    # If YAML parsing fails, just continue with empty frontmatter
                    frontmatter = {}
        
        # If no frontmatter, try to extract from markdown headers
        if not frontmatter.get('title'):
            # Extract title from markdown
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            if title_match:
                frontmatter['title'] = title_match.group(1)
        
        # Extract status from filename if not in frontmatter
        if not frontmatter.get('status'):
            if 'deferred' in str(file_path):
                frontmatter['status'] = 'Deferred'
            else:
                frontmatter['status'] = 'To Do'  # Default status
        
        return {
            'file_path': file_path,
            'frontmatter': frontmatter,
            'content': content_without_frontmatter
        }

    def document_list(self):
        """List all documents/tasks in the backlog."""
        print("=== Backlog Documents/Tasks ===\n")
        
        all_tasks = []
        
        # Get tasks from main tasks directory
        task_files = glob.glob(str(self.tasks_dir / "**/*.md"), recursive=True)
        for file_path in task_files:
            all_tasks.append(self._parse_task_file(file_path))
        
        # Get tasks from deferred directory
        deferred_files = glob.glob(str(self.deferred_dir / "*.md"))
        for file_path in deferred_files:
            all_tasks.append(self._parse_task_file(file_path))
        
        # Sort by status, then by title
        # Ensure all possible statuses are in the list for sorting
        default_statuses = self.config.get('statuses', ['To Do', 'In Progress', 'Done', 'Deferred'])
        all_statuses = list(set(default_statuses + [x['frontmatter'].get('status', 'To Do') for x in all_tasks]))
        
        all_tasks.sort(key=lambda x: (
            all_statuses.index(x['frontmatter'].get('status', 'To Do')),
            x['frontmatter'].get('title', '').lower()
        ))
        
        # Print the tasks
        current_status = None
        for task in all_tasks:
            status = task['frontmatter'].get('status', 'To Do')
            title = task['frontmatter'].get('title', 'Untitled')
            file_path = task['file_path']
            
            # Print status header if different from previous
            if status != current_status:
                print(f"\n--- {status.upper()} ---")
                current_status = status
            
            print(f"  - {title} ({os.path.basename(file_path)})")
        
        print(f"\nTotal: {len(all_tasks)} documents/tasks")

    def task_list(self, status_filter=None):
        """List all tasks, optionally filtered by status."""
        print("=== Task List ===\n")
        
        all_tasks = []
        
        # Get tasks from main tasks directory
        task_files = glob.glob(str(self.tasks_dir / "**/*.md"), recursive=True)
        for file_path in task_files:
            parsed_task = self._parse_task_file(file_path)
            if not status_filter or parsed_task['frontmatter'].get('status') == status_filter:
                all_tasks.append(parsed_task)
        
        # Get tasks from deferred directory
        deferred_files = glob.glob(str(self.deferred_dir / "*.md"))
        for file_path in deferred_files:
            parsed_task = self._parse_task_file(file_path)
            if not status_filter or parsed_task['frontmatter'].get('status') == status_filter:
                all_tasks.append(parsed_task)
        
        # Sort by status, then by title
        all_tasks.sort(key=lambda x: (
            self.config.get('statuses', ['To Do', 'In Progress', 'Done', 'Deferred']).index(x['frontmatter'].get('status', 'To Do')),
            x['frontmatter'].get('title', '').lower()
        ))
        
        # Print the tasks
        current_status = None
        for task in all_tasks:
            status = task['frontmatter'].get('status', 'To Do')
            title = task['frontmatter'].get('title', 'Untitled')
            file_path = task['file_path']
            priority = task['frontmatter'].get('priority', 'None')
            
            # Print status header if different from previous
            if status != current_status:
                if status_filter is None:  # Only show status headers if not filtering
                    print(f"\n--- {status.upper()} ---")
                current_status = status
            
            priority_str = f" [{priority}]" if priority != 'None' else ""
            print(f"  - {title}{priority_str} ({os.path.basename(file_path)})")
        
        print(f"\nTotal: {len(all_tasks)} tasks")

    def create_task(self, title, description="", status="To Do", priority="medium"):
        """Create a new task."""
        # Format title for filename
        formatted_title = re.sub(r'[^\w\s-]', '', title.lower()).strip().replace(' ', '-')
        file_path = self.tasks_dir / f"task-{formatted_title}.md"
        
        # Create content with frontmatter
        content = f"""---
id: task-{formatted_title}
title: {title}
status: {status}
assignee: []
labels: []
priority: {priority}
created_date: '{datetime.now().strftime('%Y-%m-%d %H:%M')}'
updated_date: '{datetime.now().strftime('%Y-%m-%d %H:%M')}'
---

## Description
{description}

## Subtasks
- [ ] 

## Acceptance Criteria
- [ ] 

## Implementation Notes

"""
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created new task: {file_path}")
        return file_path

    def update_task(self, task_id, **updates):
        """Update a task with new values."""
        # Find the task file
        task_files = list(glob.glob(str(self.tasks_dir / "**/*.md"), recursive=True))
        task_files.extend(glob.glob(str(self.deferred_dir / "*.md")))
        
        target_file = None
        for file_path in task_files:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if task_id in file_path or f"id: {task_id}" in content:
                    target_file = file_path
                    break
        
        if not target_file:
            print(f"Task with ID '{task_id}' not found.")
            return
        
        # Parse existing task
        task_data = self._parse_task_file(target_file)
        frontmatter = task_data['frontmatter']
        
        # Update the fields
        for key, value in updates.items():
            if value is not None:  # Only update if value was provided
                frontmatter[key] = value
        
        # Update the updated_date
        frontmatter['updated_date'] = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # Reconstruct the file
        content_without_frontmatter = task_data['content']
        new_content = f"---\n{yaml.dump(frontmatter, default_flow_style=False)}---\n{content_without_frontmatter}"
        
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"Updated task: {target_file}")


def main():
    parser = argparse.ArgumentParser(description='Backlog Management System')
    parser.add_argument('--backlog-dir', default='backlog', help='Path to backlog directory')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Document list command
    document_list_parser = subparsers.add_parser('document_list', help='List all backlog documents/tasks')
    
    # Task list command
    task_list_parser = subparsers.add_parser('task_list', help='List all tasks')
    task_list_parser.add_argument('--status', choices=['To Do', 'In Progress', 'Done', 'Deferred'], 
                                 help='Filter tasks by status')
    
    # Create task command
    create_task_parser = subparsers.add_parser('create_task', help='Create a new task')
    create_task_parser.add_argument('--title', required=True, help='Task title')
    create_task_parser.add_argument('--description', default='', help='Task description')
    create_task_parser.add_argument('--status', default='To Do', help='Task status')
    create_task_parser.add_argument('--priority', default='medium', choices=['low', 'medium', 'high'], 
                                   help='Task priority')
    
    # Update task command
    update_task_parser = subparsers.add_parser('update_task', help='Update a task')
    update_task_parser.add_argument('--id', required=True, help='Task ID to update')
    update_task_parser.add_argument('--status', help='New status')
    update_task_parser.add_argument('--priority', choices=['low', 'medium', 'high'], help='New priority')
    update_task_parser.add_argument('--assignee', help='New assignee')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = BacklogManager(args.backlog_dir)
    
    if args.command == 'document_list':
        manager.document_list()
    elif args.command == 'task_list':
        manager.task_list(status_filter=args.status)
    elif args.command == 'create_task':
        manager.create_task(
            title=args.title,
            description=args.description,
            status=args.status,
            priority=args.priority
        )
    elif args.command == 'update_task':
        updates = {}
        if args.status:
            updates['status'] = args.status
        if args.priority:
            updates['priority'] = args.priority
        if args.assignee:
            updates['assignee'] = args.assignee
        manager.update_task(args.id, **updates)


if __name__ == "__main__":
    main()