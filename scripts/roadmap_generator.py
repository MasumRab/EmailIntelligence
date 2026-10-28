import os
import re
from pathlib import Path
from dataclasses import dataclass
from typing import List

@dataclass
class TaskInfo:
    id: str
    title: str
    status: str
    priority: str

def parse_task_file(file_path: str) -> TaskInfo:
    """Parses a task markdown file and extracts metadata."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return TaskInfo(id="Error", title="Error", status="Error", priority="Error")

    title_match = re.search(r'# Task (\d+): (.*)', content)
    status_match = re.search(r'\*\*Status:\*\*\s*(.*)', content, re.IGNORECASE)
    priority_match = re.search(r'\*\*Priority:\*\*\s*(.*)', content, re.IGNORECASE)

    task_id = title_match.group(1) if title_match else Path(file_path).stem.replace('task_', '')
    title = title_match.group(2).strip() if title_match else "Unknown"
    status = status_match.group(1).strip() if status_match else "Unknown"
    priority = priority_match.group(1).strip() if priority_match else "Unknown"

    return TaskInfo(id=task_id, title=title, status=status, priority=priority)

def generate_roadmap(tasks_dir: str) -> str:
    """Generates a markdown roadmap table from task files in the directory."""
    tasks: List[TaskInfo] = []

    if not os.path.exists(tasks_dir):
        return "# Project Roadmap\n\nNo tasks found."

    for file in os.listdir(tasks_dir):
        if file.startswith('task_') and file.endswith('.md'):
            # Only include main tasks, not subtasks like task_006.3.md
            if re.match(r'^task_\d+\.md$', file):
                task = parse_task_file(os.path.join(tasks_dir, file))
                tasks.append(task)

    # Sort tasks by ID numerically
    tasks.sort(key=lambda t: int(t.id) if t.id.isdigit() else float('inf'))

    # Generate markdown table
    roadmap = "# Project Roadmap\n\n"
    roadmap += "| Task ID | Title | Status | Priority |\n"
    roadmap += "|---------|-------|--------|----------|\n"

    for task in tasks:
        roadmap += f"| {task.id} | {task.title} | {task.status} | {task.priority} |\n"

    return roadmap

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        import unittest
        import tempfile
        import shutil

        class TestRoadmapGenerator(unittest.TestCase):
            def setUp(self):
                self.test_dir = tempfile.mkdtemp()

            def tearDown(self):
                shutil.rmtree(self.test_dir)

            def test_parse_task_file(self):
                task_file = os.path.join(self.test_dir, 'task_123.md')
                with open(task_file, 'w', encoding='utf-8') as f:
                    f.write("# Task 123: Test Task\n")
                    f.write("**Status:** in_progress\n")
                    f.write("**Priority:** High\n")

                task = parse_task_file(task_file)
                self.assertEqual(task.id, "123")
                self.assertEqual(task.title, "Test Task")
                self.assertEqual(task.status, "in_progress")
                self.assertEqual(task.priority, "High")

            def test_generate_roadmap(self):
                # Create some dummy task files
                tasks = [
                    ("task_002.md", "# Task 002: Second Task\n**Status:** pending\n**Priority:** low\n"),
                    ("task_001.md", "# Task 001: First Task\n**Status:** done\n**Priority:** high\n"),
                    ("task_001.1.md", "# Task 001.1: Subtask\n**Status:** done\n**Priority:** high\n"),
                ]

                for name, content in tasks:
                    with open(os.path.join(self.test_dir, name), 'w', encoding='utf-8') as f:
                        f.write(content)

                roadmap = generate_roadmap(self.test_dir)

                self.assertIn("| Task ID | Title | Status | Priority |", roadmap)
                self.assertIn("| 001 | First Task | done | high |", roadmap)
                self.assertIn("| 002 | Second Task | pending | low |", roadmap)
                self.assertNotIn("Subtask", roadmap)

                idx_1 = roadmap.find("First Task")
                idx_2 = roadmap.find("Second Task")
                self.assertTrue(idx_1 < idx_2)

        # Run tests
        # We need to slice sys.argv so unittest doesn't try to parse '--test'
        sys.argv = sys.argv[:1]
        unittest.main()
    else:
        # Normal execution
        tasks_dir = '.taskmaster/tasks'
        roadmap_content = generate_roadmap(tasks_dir)
        output_file = 'ROADMAP.md'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(roadmap_content)
        print(f"Roadmap generated at {output_file}")
