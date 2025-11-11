import subprocess
import sys
import unittest

class TestCli(unittest.TestCase):

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

    def test_install_command(self):
        # Act
        stdout, stderr, returncode = self.run_command("install")

        # Assert
        self.assertEqual(returncode, 0)
        self.assertIn("Setting up the tool...", stdout)
        self.assertIn("Tool setup complete.", stdout)

    def test_identify_rebased_branches_command(self):
        # Act
        stdout, stderr, returncode = self.run_command("identify-rebased-branches")

        # Assert
        self.assertEqual(returncode, 0)
        self.assertIn("Rebased branches:", stdout)
        self.assertIn("- feature/branch-a", stdout)
        self.assertIn("- feature/branch-b", stdout)

    def test_analyze_command(self):
        # Act
        stdout, stderr, returncode = self.run_command("analyze feature/branch-a")

        # Assert
        self.assertEqual(returncode, 0)
        self.assertIn("Analysis complete:", stdout)
        self.assertIn("- Implement user authentication feature.", stdout)

    def test_verify_command(self):
        # Act
        stdout, stderr, returncode = self.run_command("verify main")

        # Assert
        self.assertEqual(returncode, 0)
        self.assertIn("Verification complete:", stdout)
        self.assertIn("All intentions have been fulfilled.", stdout)

    def test_ci_check_command(self):
        # Act
        stdout, stderr, returncode = self.run_command("ci-check feature/branch-a")

        # Assert
        self.assertEqual(returncode, 0)
        self.assertIn("Running CI checks for branch: feature/branch-a...", stdout)
        self.assertIn("CI checks passed.", stdout)

if __name__ == '__main__':
    unittest.main()
