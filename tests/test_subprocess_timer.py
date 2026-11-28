import unittest
import sys
import os
import subprocess

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scripts.subprocess_timer import time_command

class TestSubprocessTimer(unittest.TestCase):
    def test_time_command_success(self):
        command = [sys.executable, "-c", "import time; time.sleep(0.01)"]
        elapsed = time_command(command)
        self.assertGreaterEqual(elapsed, 9.0)

    def test_time_command_failure(self):
        command = [sys.executable, "-c", "import sys; sys.exit(1)"]
        with self.assertRaises(subprocess.CalledProcessError):
            time_command(command)

if __name__ == "__main__":
    unittest.main()
