import unittest
import tempfile
import os
from scripts.detect_merge_markers import detect_merge_markers

class TestDetectMergeMarkers(unittest.TestCase):
    def setUp(self):
        # We need to create the temp dir in the current working directory to pass the traversal check
        self.temp_dir = tempfile.TemporaryDirectory(dir=os.getcwd())
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def test_clean_file(self):
        clean_file = os.path.join(self.temp_dir.name, "clean.txt")
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write("This is a clean file\nNo merge markers here\n")
            
        errors = detect_merge_markers([clean_file])
        self.assertEqual(len(errors), 0)
        
    def test_file_with_markers(self):
        conflict_file = os.path.join(self.temp_dir.name, "conflict.txt")
        with open(conflict_file, "w", encoding="utf-8") as f:
            f.write("some text\n")
            f.write("<<<<<<< HEAD\n")
            f.write("my changes\n")
            f.write("=======\n")
            f.write("their changes\n")
            f.write(">>>>>>> branch-name\n")
            f.write("more text\n")
            
        errors = detect_merge_markers([conflict_file])
        self.assertEqual(len(errors), 3)
        self.assertTrue(any("<<<<<<<" in e or "=======" in e or ">>>>>>>" in e for e in errors) or len(errors) == 3)
        self.assertIn(f"MERGE MARKER: {conflict_file}:2", errors)
        self.assertIn(f"MERGE MARKER: {conflict_file}:4", errors)
        self.assertIn(f"MERGE MARKER: {conflict_file}:6", errors)

    def test_file_not_found(self):
        nonexistent_file = os.path.join(self.temp_dir.name, "nonexistent.txt")
        errors = detect_merge_markers([nonexistent_file])
        self.assertEqual(len(errors), 0)

    def test_path_traversal(self):
        traversal_file = "../../etc/passwd"
        errors = detect_merge_markers([traversal_file])
        self.assertEqual(len(errors), 1)
        self.assertIn("PATH TRAVERSAL ERROR: Path must be within current directory: ../../etc/passwd", errors[0])

if __name__ == '__main__':
    unittest.main()
