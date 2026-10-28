import unittest
import os
import tempfile
import sys
from io import StringIO
from contextlib import redirect_stdout

# Add the scripts directory to sys.path to allow importing doc_generator
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from doc_generator import generate_usage_table, get_script_description

class TestDocGenerator(unittest.TestCase):
    def test_get_script_description_py(self):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
            f.write('"""Test Python Script"""\ndef foo(): pass')
            temp_name = f.name
        try:
            self.assertEqual(get_script_description(temp_name), "Test Python Script")
        finally:
            os.unlink(temp_name)

    def test_get_script_description_sh(self):
        with tempfile.NamedTemporaryFile(suffix=".sh", mode="w", delete=False) as f:
            f.write('#!/bin/bash\n# Test Bash Script\necho "test"')
            temp_name = f.name
        try:
            self.assertEqual(get_script_description(temp_name), "Test Bash Script")
        finally:
            os.unlink(temp_name)

    def test_generate_usage_table(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "a.py"), "w") as f:
                f.write('"""Doc A"""')
            with open(os.path.join(d, "b.sh"), "w") as f:
                f.write('#!/bin/bash\n# Doc B')

            f_out = StringIO()
            with redirect_stdout(f_out):
                generate_usage_table(d)

            output = f_out.getvalue()
            self.assertIn("a.py", output)
            self.assertIn("Doc A", output)
            self.assertIn("b.sh", output)
            self.assertIn("Doc B", output)

if __name__ == '__main__':
    unittest.main()
