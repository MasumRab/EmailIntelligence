import unittest
import sys
from subprocess_timer import time_command

class TestSubprocessTimer(unittest.TestCase):
    def test_time_command(self):
        duration = time_command(['sleep', '0.01'])
        self.assertGreater(duration, 0)
        self.assertLess(duration, 500)
        
if __name__ == '__main__':
    unittest.main()
