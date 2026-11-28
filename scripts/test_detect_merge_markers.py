import unittest
import tempfile
import os
from scripts.detect_merge_markers import detect_merge_markers

class TestDetectMergeMarkers(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        
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
        self.assertEqual(len(errors), 2)
        self.assertIn(f"MERGE MARKER: {conflict_file}:2", errors)
        self.assertIn(f"MERGE MARKER: {conflict_file}:6", errors)

    def test_latin1_file_with_marker(self):
        conflict_file = os.path.join(self.temp_dir.name, "latin1_conflict.txt")
        with open(conflict_file, "wb") as f:
            f.write(b"caf\xe9\n")
            f.write(b"<<<<<<< HEAD\n")
            f.write(b"latin1 changes\n")
            f.write(b">>>>>>> branch\n")
            
        errors = detect_merge_markers([conflict_file])
        self.assertEqual(len(errors), 2 )
        self.assertIn(f"MERGE MARKER: {conflict_file}:2", errors)
        self.assertIn(f"MERGE MARKER: {conflict_file}:4", errors)
        
    def test_clean_file_with_divider(self):
        clean_file = os.path.join(self.temp_dir.name, "divider.txt")
        with open(clean_file, "w", encoding="utf-8") as f:
            f.write("Section 1\n")
            f.write("=======\n")
            f.write("Section 2\n")
            
        errors = detect_merge_markers([clean_file])
        self.assertEqual(len(errors), 0)

    def test_bom_prefixed_file_with_marker(self):
        bom_file = os.path.join(self.temp_dir.name, "bom.txt")
        with open(bom_file, "w", encoding="utf-8-sig") as f:
            f.write("<<<<<<< HEAD\n")
            f.write("changes\n")
            f.write(">>>>>>> branch\n")
            
        errors = detect_merge_markers([bom_file])
        self.assertEqual(len(errors), 2)
        self.assertIn(f"MERGE MARKER: {bom_file}:1", errors)
        self.assertIn(f"MERGE MARKER: {bom_file}:3", errors)

    def test_file_not_found(self):
        nonexistent_file = os.path.join(self.temp_dir.name, "nonexistent.txt")
        errors = detect_merge_markers([nonexistent_file])
        self.assertEqual(len(errors), 1)
        self.assertIn(f"READ ERROR: {nonexistent_file} - not found", errors)

if __name__ == '__main__':
    unittest.main()