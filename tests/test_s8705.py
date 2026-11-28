import pytest
from unittest.mock import patch, MagicMock
from emailintelligence_cli import CommandDispatcher

def test_analyze_invalid_branch_injection():
    dispatcher = CommandDispatcher()
    # Mock to prevent actual execution, just want to see if ValueError is raised
    with pytest.raises(ValueError, match="Invalid branch name: -b"):
        # We need to simulate the execution of the analyze command with an invalid branch
        # But analyze takes args. We can just test the validation logic if we can mock it
        pass

def test_run_injections():
    dispatcher = CommandDispatcher()
    # Let's mock subprocess.run and call analyze
    args = MagicMock()
    args.source_branch = "main"
    args.target_branch = "-b"
    
    with patch('subprocess.run') as mock_run:
        with pytest.raises(ValueError, match="Invalid branch name: -b"):
            dispatcher.analyze(args)

def test_s8707_path_traversal():
    from src.cli.state import secure_open
    import os
    with pytest.raises(ValueError, match="Path traversal detected"):
        secure_open("../test", "r", base_dir="/app/src/cli")
