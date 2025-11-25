#!/usr/bin/env python3
"""
Backlog Extraction and Normalization Script
Phase 1 of Backlog Consolidation Plan

This script extracts all backlog files from the remote repository,
parses different file formats, and normalizes the data into a unified structure.
"""

import json
import subprocess
import re
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, date

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles datetime and date objects"""
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, date):
            return o.isoformat()
        return super().default(o)

class BacklogExtractor:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.extracted_tasks = []
        self.errors = []

    def run_git_command(self, cmd: List[str]) -> str:
        """Execute git command and return output"""
        try:
            result = subprocess.run(
                ["git"] + cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            self.errors.append(f"Git command failed: {' '.join(cmd)} - {e}")
            return ""

    def get_backlog_files(self) -> List[str]:
        """Get all backlog files from remote repository"""
        output = self.run_git_command([
            "ls-tree", "-r", "--name-only",
            "origin/align-feature-notmuch-tagging-1"
        ])

        files = [line for line in output.split('\n') if line.startswith('backlog/')]
        print(f"Found {len(files)} backlog files")
        return files

    def extract_file_content(self, file_path: str) -> str:
        """Extract content of a file from remote repository"""
        return self.run_git_command([
            "show", f"origin/align-feature-notmuch-tagging-1:{file_path}"
        ])

    def parse_yaml_frontmatter(self, content: str) -> tuple[Optional[Dict], str]:
        """Parse YAML frontmatter from markdown files"""
        if not content.startswith('---'):
            return None, content

        # Find the end of frontmatter
        end_pos = content.find('---', 3)
        if end_pos == -1:
            return None, content

        frontmatter_text = content[3:end_pos]
        body = content[end_pos + 3:].strip()

        try:
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter, body
        except yaml.YAMLError:
            return None, content

    def parse_markdown_headers(self, content: str) -> Dict[str, Any]:
        """Parse markdown headers and content"""
        task_data = {}
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Parse headers like ## Title: value or ## Description
            if line.startswith('## '):
                header = line[3:].strip()
                content_lines = []

                # Collect content until next header or end
                i += 1
                while i < len(lines) and not lines[i].strip().startswith('## '):
                    if lines[i].strip():
                        content_lines.append(lines[i].rstrip())
                    i += 1

                content = '\n'.join(content_lines).strip()

                # Map common headers to standardized fields
                if 'title' in header.lower():
                    task_data['title'] = content.replace('title: ', '').strip(' "\'')
                elif 'description' in header.lower():
                    task_data['description'] = content
                elif 'priority' in header.lower():
                    task_data['priority'] = content.lower()
                elif 'status' in header.lower():
                    task_data['status'] = content.lower()
                elif 'acceptance criteria' in header.lower():
                    task_data['acceptance_criteria'] = content
                elif 'dependencies' in header.lower():
                    task_data['dependencies'] = content
                else:
                    # Store other headers as-is
                    task_data[header.lower().replace(' ', '_')] = content

                continue

            i += 1

        return task_data

    def normalize_task_data(self, raw_data: Dict, file_path: str) -> Dict[str, Any]:
        """Normalize task data to unified schema"""
        normalized = {
            'id': raw_data.get('id', file_path),
            'title': raw_data.get('title', 'Unknown Title'),
            'description': raw_data.get('description', ''),
            'status': raw_data.get('status', 'todo'),
            'priority': raw_data.get('priority', 'medium'),
            'acceptance_criteria': raw_data.get('acceptance_criteria', ''),
            'dependencies': raw_data.get('dependencies', []),
            'assignees': raw_data.get('assignee', raw_data.get('assignees', [])),
            'labels': raw_data.get('labels', []),
            'created_date': raw_data.get('created_date', raw_data.get('created', '')),
            'updated_date': raw_data.get('updated_date', raw_data.get('updated', '')),
            'source_file': file_path,
            'category': self.extract_category(file_path),
            'extracted_at': datetime.now().isoformat(),
            'raw_data': raw_data  # Keep original for reference
        }

        # Normalize status values
        status_mapping = {
            'to do': 'todo',
            'in progress': 'in-progress',
            'done': 'done',
            'deferred': 'deferred',
            'cancelled': 'cancelled'
        }
        normalized['status'] = status_mapping.get(normalized['status'], normalized['status'])

        # Normalize priority values
        priority_mapping = {
            'high': 'high',
            'medium': 'medium',
            'low': 'low'
        }
        normalized['priority'] = priority_mapping.get(normalized['priority'], 'medium')

        return normalized

    def extract_category(self, file_path: str) -> str:
        """Extract category from file path"""
        parts = file_path.split('/')
        if len(parts) >= 3 and parts[0] == 'backlog' and parts[1] == 'tasks':
            return parts[2]
        elif parts[1] == 'deferred':
            return 'deferred'
        elif parts[1] == 'sessions':
            return 'sessions'
        else:
            return 'other'

    def process_file(self, file_path: str) -> Optional[Dict]:
        """Process a single backlog file"""
        try:
            content = self.extract_file_content(file_path)
            if not content:
                return None

            # Try YAML frontmatter first
            frontmatter, body = self.parse_yaml_frontmatter(content)
            if frontmatter:
                # Combine frontmatter with parsed body
                task_data = dict(frontmatter)
                if body:
                    body_data = self.parse_markdown_headers(body)
                    task_data.update(body_data)
            else:
                # Fallback to markdown header parsing
                task_data = self.parse_markdown_headers(content)

            # Normalize the data
            normalized_task = self.normalize_task_data(task_data, file_path)

            return normalized_task

        except Exception as e:
            self.errors.append(f"Error processing {file_path}: {e}")
            return None

    def extract_all_tasks(self) -> List[Dict]:
        """Extract and normalize all backlog tasks"""
        print("Starting backlog extraction...")

        files = self.get_backlog_files()
        extracted_tasks = []

        for i, file_path in enumerate(files, 1):
            if i % 50 == 0:
                print(f"Processed {i}/{len(files)} files...")

            task = self.process_file(file_path)
            if task:
                extracted_tasks.append(task)

        print(f"✅ Extracted {len(extracted_tasks)} tasks from {len(files)} files")
        if self.errors:
            print(f"⚠️  Encountered {len(self.errors)} errors during extraction")

        return extracted_tasks

    def save_extracted_data(self, tasks: List[Dict]):
        """Save extracted and normalized task data"""
        output_file = Path(self.repo_path) / "backlog" / "extraction" / "extracted_tasks.json"

        data = {
            'metadata': {
                'extraction_date': datetime.now().isoformat(),
                'total_files_processed': len(self.get_backlog_files()),
                'tasks_extracted': len(tasks),
                'errors_encountered': len(self.errors)
            },
            'tasks': tasks,
            'errors': self.errors
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)

        print(f"✅ Saved extracted data to {output_file}")

def main():
    extractor = BacklogExtractor()
    tasks = extractor.extract_all_tasks()
    extractor.save_extracted_data(tasks)

    print("\n📊 EXTRACTION SUMMARY:")
    print(f"  • Total files processed: {len(extractor.get_backlog_files())}")
    print(f"  • Tasks successfully extracted: {len(tasks)}")
    print(f"  • Errors encountered: {len(extractor.errors)}")

    if extractor.errors:
        print(f"  • Error details saved to extraction output")

if __name__ == "__main__":
    main()