import os
import tempfile
import unittest
from marker_scanner import scan_directory

class TestMarkerScanner(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        
        # Create some dummy files with markers
        with open(os.path.join(self.test_dir.name, "file1.py"), "w") as f:
            f.write("# TO" + "DO: Implement this feature\n")
            f.write("def foo():\n    pass\n")
            
        with open(os.path.join(self.test_dir.name, "file2.py"), "w") as f:
            f.write("def bar():\n")
            f.write("    # FIX" + "ME: Broken logic\n")
            f.write("    pass\n")
            
        with open(os.path.join(self.test_dir.name, "file3.py"), "w") as f:
            f.write("# just a regular comment\n")
            f.write("# todo without colon works too\n")

    def tearDown(self):
        self.test_dir.cleanup()

    def test_scan_directory(self):
        markers = scan_directory(self.test_dir.name)
        
        self.assertEqual(len(markers), 3)
        
        # FIX" + "ME should be prioritized over TO" + "DO
        self.assertEqual(markers[0].marker_type, "FIX" + "ME")
        self.assertEqual(markers[0].content, "Broken logic")
        
        # Then the TO" + "DOs
        self.assertEqual(markers[1].marker_type, "TO" + "DO")
        self.assertTrue(markers[2].marker_type == "TO" + "DO")

if __name__ == "__main__":
    unittest.main()
