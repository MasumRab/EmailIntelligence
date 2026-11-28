import pytest
from unittest.mock import patch, MagicMock
import subprocess
from deploy_plan import get_deploy_plan

def test_get_deploy_plan_with_staged_files():
    mock_run = MagicMock()
    mock_run.stdout = "file1.txt\nfile2.py\n"
    
    with patch("subprocess.run", return_value=mock_run):
        plan = get_deploy_plan("v1.0.0")
        
    assert plan == {
        "target_ref": "v1.0.0",
        "staged_files": ["file1.txt", "file2.py"]
    }

def test_get_deploy_plan_empty_staged():
    mock_run = MagicMock()
    mock_run.stdout = ""
    
    with patch("subprocess.run", return_value=mock_run):
        plan = get_deploy_plan("main")
        
    assert plan == {
        "target_ref": "main",
        "staged_files": []
    }

def test_get_deploy_plan_git_error():
    with patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")):
        plan = get_deploy_plan("main")
        
    assert plan == {
        "target_ref": "main",
        "staged_files": []
    }
