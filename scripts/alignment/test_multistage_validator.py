#!/usr/bin/env python3
import unittest
from unittest.mock import patch
import sys

# Add parent directory to path so we can import the script
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alignment.multistage_validator import run_validation, main

class TestMultistageValidator(unittest.TestCase):
    
    @patch('subprocess.run')
    def test_run_validation_success(self, mock_run):
        mock_run.return_value.returncode = 0
        self.assertTrue(run_validation("dummy_script.py"))
        
    @patch('subprocess.run')
    def test_run_validation_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "Failed"
        mock_run.return_value.stderr = "Error"
        self.assertFalse(run_validation("dummy_script.py"))

    @patch('subprocess.run')
    def test_run_validation_exception(self, mock_run):
        mock_run.side_effect = Exception("File not found")
        self.assertFalse(run_validation("dummy_script.py"))
        
    @patch('alignment.multistage_validator.run_validation')
    def test_main_success(self, mock_run_validation):
        mock_run_validation.return_value = True
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 0)
        
    @patch('alignment.multistage_validator.run_validation')
    def test_main_failure(self, mock_run_validation):
        # First script succeeds, second fails
        mock_run_validation.side_effect = [True, False]
        with self.assertRaises(SystemExit) as cm:
            main()
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
