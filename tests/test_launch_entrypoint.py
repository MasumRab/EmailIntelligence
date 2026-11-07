import os
import subprocess
import sys
import tempfile
import unittest

class TestLaunchEntrypoint(unittest.TestCase):
    """
    Test the behavior of the python3 launch.py entrypoint script to ensure it correctly
    forwards arguments and runs the setup.launch module via subprocess instead of direct file path execution.
    This suite checks various scenarios such as running from inside the repo, outside the repo,
    and handling of invalid flags.
    """

    def setUp(self):
        # We need the path to the real repository root to set the pythonpath / cwd.
        self.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.launch_script = os.path.join(self.repo_root, "launch.py")

    def test_launch_help_output(self):
        """Test running python3 launch.py --help from a temporary directory with cwd=repo_root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # We execute python3 launch.py --help from tmpdir, but setting cwd=self.repo_root
            # Actually, if we set cwd=self.repo_root, we can just run python3 launch.py

            # Run using the python executable that runs the test
            cmd = [sys.executable, self.launch_script, "--help"]

            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            # Check exit code is 0
            self.assertEqual(
                result.returncode,
                0,
                f"Expected 0, got {result.returncode}. Stderr: {result.stderr}"
            )

            # Check stdout is not empty and contains expected help text
            self.assertTrue(len(result.stdout) > 0, "Stdout should not be empty")
            self.assertIn("usage:", result.stdout.lower())
            self.assertIn("--system-info", result.stdout)
            self.assertIn("options:", result.stdout.lower())

    def test_launch_system_info(self):
        """Test running python3 launch.py --system-info from a temporary directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [sys.executable, self.launch_script, "--system-info"]

            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            # Check exit code is 0
            self.assertEqual(
                result.returncode,
                0,
                f"Expected 0, got {result.returncode}. Stderr: {result.stderr}"
            )

            # Check stdout is not empty and contains system info headers
            self.assertTrue(len(result.stdout) > 0, "Stdout should not be empty")
            self.assertIn("System Information", result.stdout)
            self.assertIn("Project Root", result.stdout)
            self.assertIn("Python Version", result.stdout)

    def test_launch_invalid_subcommand(self):
        """Test that an invalid subcommand correctly propagates a non-zero exit code."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [sys.executable, self.launch_script, "--non-existent-flag-for-testing"]

            result = subprocess.run(
                cmd,
                cwd=self.repo_root,
                capture_output=True,
                text=True
            )

            # Check exit code is non-zero
            self.assertNotEqual(result.returncode, 0, "Expected non-zero exit code for invalid flag.")

            # Ensure the wrapper propagated the child's error
            output_combined = result.stderr + result.stdout
            self.assertTrue("unrecognized arguments" in output_combined)

    def test_launch_from_outside_repo(self):
        """Test that running the script with an absolute path from an external cwd works correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            cmd = [sys.executable, self.launch_script, "--help"]

            # We run the command from the tmpdir, so cwd is tmpdir, not repo_root.
            # The script should be able to resolve setup_launch_path and run properly
            # because we pass cwd=script_dir in subprocess.run inside launch.py.
            result = subprocess.run(
                cmd,
                cwd=tmpdir,
                capture_output=True,
                text=True
            )

            # Check exit code is 0
            self.assertEqual(
                result.returncode,
                0,
                f"Expected 0, got {result.returncode}. Stderr: {result.stderr}"
            )
            self.assertIn("--system-info", result.stdout)
            self.assertIn("usage:", result.stdout.lower())

if __name__ == "__main__":
    unittest.main()
