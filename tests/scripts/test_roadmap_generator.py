import unittest
import os
import tempfile
import shutil
import importlib.util
from pathlib import Path

# Load roadmap_generator by path since scripts is not a package
script_path = Path(__file__).resolve().parents[2] / "scripts" / "roadmap_generator.py"
spec = importlib.util.spec_from_file_location("roadmap_generator", script_path)
roadmap_generator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(roadmap_generator)

generate_roadmap = roadmap_generator.generate_roadmap
parse_task_file = roadmap_generator.parse_task_file

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
        self.assertIsNotNone(task)
        self.assertEqual(task.id, "123")
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, "in_progress")
        self.assertEqual(task.priority, "High")

    def test_generate_roadmap(self):
        # Create some dummy task files
        tasks = [
            ("task_002.md", "# Task 002: Second Task\n**Status:** pending\n**Priority:** low\n"),
            ("task_001.md", "# Task 001: First Task | with pipe\n**Status:** done\n**Priority:** high\n"),
            ("task_001.1.md", "# Task 001.1: Subtask\n**Status:** done\n**Priority:** high\n"),
        ]

        for name, content in tasks:
            with open(os.path.join(self.test_dir, name), 'w', encoding='utf-8') as f:
                f.write(content)

        # Create a directory named task_006.md to test error skipping
        os.makedirs(os.path.join(self.test_dir, 'task_006.md'))

        roadmap = generate_roadmap(self.test_dir)

        self.assertIn("| Task ID | Title | Status | Priority |", roadmap)
        self.assertIn(r"| 001 | First Task \| with pipe | done | high |", roadmap)
        self.assertIn("| 002 | Second Task | pending | low |", roadmap)
        self.assertNotIn("Subtask", roadmap)
        
        # Verify that task_006 was skipped and didn't result in an "Error" row
        self.assertNotIn("Error", roadmap)
        
        idx_1 = roadmap.find("First Task")
        idx_2 = roadmap.find("Second Task")
        self.assertTrue(idx_1 < idx_2)

if __name__ == '__main__':
    unittest.main()
