import pytest
import subprocess
import os
import tempfile
from scripts.conflict_detection import check_conflicts

def test_check_conflicts():
    original_cwd = os.getcwd()
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            
            subprocess.run(["git", "init", "--initial-branch=main"], check=True)
            subprocess.run(["git", "config", "user.name", "Test User"], check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], check=True)
            
            # Create initial commit
            with open("file.txt", "w") as f:
                f.write("line1\n")
            subprocess.run(["git", "add", "file.txt"], check=True)
            subprocess.run(["git", "commit", "-m", "initial"], check=True)
            
            # Create feature branch
            subprocess.run(["git", "branch", "feature"], check=True)
            
            # Make change on main
            with open("file.txt", "w") as f:
                f.write("line2\n")
            subprocess.run(["git", "commit", "-am", "main change"], check=True)
            
            # Check no conflicts with clean branch
            subprocess.run(["git", "checkout", "feature"], check=True)
            subprocess.run(["git", "branch", "clean-feature"], check=True)
            subprocess.run(["git", "checkout", "clean-feature"], check=True)
            with open("clean.txt", "w") as f:
                f.write("clean\n")
            subprocess.run(["git", "add", "clean.txt"], check=True)
            subprocess.run(["git", "commit", "-m", "clean"], check=True)
            
            res = check_conflicts("main", "clean-feature")
            assert res["conflict_detected"] == False
            
            # Check conflicts
            subprocess.run(["git", "checkout", "feature"], check=True)
            with open("file.txt", "w") as f:
                f.write("line3\n")
            subprocess.run(["git", "commit", "-am", "feature change"], check=True)
            
            res2 = check_conflicts("main", "feature")
            assert res2["conflict_detected"] == True
            assert res2["total_conflicts"] == 1
            assert res2["conflict_files"][0]["file_path"] == "file.txt"
            assert res2["conflict_files"][0]["conflict_type"] == "merge"
            assert res2["conflict_files"][0]["severity"] == "high"
            assert res2["manual_resolution_required"] == 1
    finally:
        os.chdir(original_cwd)
