import subprocess
import sys
import unittest

class TestCliContracts(unittest.TestCase):

    def run_command(self, command):
        """
        Runs a CLI command.
        """
        process = subprocess.Popen(
            [sys.executable, "-m", "src.cli.main"] + command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        return stdout.decode("utf-8"), stderr.decode("utf-8"), process.returncode

    def test_analyze_contract(self):
        # Act
        stdout, stderr, returncode = self.run_command("analyze")

        # Assert
        self.assertNotEqual(returncode, 0)
        self.assertIn("usage: main.py analyze [-h] branch_name", stderr)
        self.assertIn("main.py analyze: error: the following arguments are required: branch_name", stderr)

    def test_verify_contract(self):
        # Act
        stdout, stderr, returncode = self.run_command("verify")

        # Assert
        self.assertNotEqual(returncode, 0)
        self.assertIn("usage: main.py verify [-h] merged_branch_name", stderr)
        self.assertIn("main.py verify: error: the following arguments are required: merged_branch_name", stderr)

    def test_ci_check_contract(self):
        # Act
        stdout, stderr, returncode = self.run_command("ci-check")

        # Assert
        self.assertNotEqual(returncode, 0)
        self.assertIn("usage: main.py ci-check [-h] branch_name", stderr)
        self.assertIn("main.py ci-check: error: the following arguments are required: branch_name", stderr)

if __name__ == '__main__':
    unittest.main()
