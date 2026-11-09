#!/usr/bin/env python3
"""
Tests for stale_scripts_monitor.py
"""

import os
import sys
import time
import tempfile
import shutil
import unittest

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from stale_scripts_monitor import check_stale_scripts, get_file_last_modified_time

class TestStaleScriptsMonitor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_check_stale_scripts(self):
        # Create a "new" script
        new_script = os.path.join(self.temp_dir, "new_script.py")
        with open(new_script, "w") as f:
            f.write("# new script")
            
        # Create a "stale" script
        stale_script = os.path.join(self.temp_dir, "stale_script.py")
        with open(stale_script, "w") as f:
            f.write("# stale script")
            
        # Manually set mtime for stale script to 100 days ago
        now = time.time()
        stale_time = now - (100 * 24 * 60 * 60)
        os.utime(stale_script, (stale_time, stale_time))
        
        results = check_stale_scripts(directory=self.temp_dir, days_threshold=90)
        
        self.assertEqual(len(results["all_files"]), 2)
        self.assertEqual(len(results["stale_files"]), 1)
        self.assertEqual(results["stale_files"][0]["filepath"], stale_script)

if __name__ == "__main__":
    unittest.main()
