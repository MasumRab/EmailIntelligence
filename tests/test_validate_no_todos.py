import os
import sys
import pytest
from unittest.mock import patch, mock_open

# Add scripts directory to path to import the script
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from validate_no_todos import check_file_for_todos, get_changed_files, main

def test_check_file_for_todos_no_todos(tmp_path):
    p = tmp_path / "test_file.py"
    p.write_text("def my_func():\n    return 42\n")
    
    assert check_file_for_todos(str(p)) is False

def test_check_file_for_todos_with_todos(tmp_path):
    p = tmp_path / "test_file.py"
    p.write_text("def my_func():\n    # TODO: Implement this\n    pass\n")
    
    assert check_file_for_todos(str(p)) is True

def test_check_file_for_todos_lowercase_todos(tmp_path):
    p = tmp_path / "test_file.py"
    p.write_text("def my_func():\n    # todo: Implement this\n    pass\n")
    
    assert check_file_for_todos(str(p)) is True

def test_check_file_for_todos_file_not_found():
    assert check_file_for_todos("nonexistent_file.py") is False

def test_check_file_for_todos_invalid_utf8(tmp_path):
    p = tmp_path / "binary_file.bin"
    # Write some non-utf8 bytes
    p.write_bytes(b'\xff\xfe\x00\x00')
    
    assert check_file_for_todos(str(p)) is False

@patch('subprocess.run')
def test_get_changed_files(mock_run):
    mock_run.return_value.stdout = "file1.py\nfile2.py\n"
    
    files = get_changed_files()
    assert files == ["file1.py", "file2.py"]
    mock_run.assert_called_once_with(
        ['git', 'diff', '--name-only', 'main...HEAD'],
        capture_output=True,
        text=True,
        check=True
    )

@patch('subprocess.run')
def test_get_changed_files_empty(mock_run):
    mock_run.return_value.stdout = ""
    
    files = get_changed_files()
    assert files == []

@patch('subprocess.run')
def test_get_changed_files_error(mock_run):
    import subprocess
    mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd')
    
    with pytest.raises(SystemExit) as e:
        get_changed_files()
        
    assert e.value.code == 1

@patch('validate_no_todos.get_changed_files')
@patch('validate_no_todos.check_file_for_todos')
def test_main_success(mock_check, mock_get_changed, capsys):
    mock_get_changed.return_value = ["file1.py"]
    mock_check.return_value = False
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "Validation passed" in captured.out

@patch('validate_no_todos.get_changed_files')
@patch('validate_no_todos.check_file_for_todos')
def test_main_failure(mock_check, mock_get_changed, capsys):
    mock_get_changed.return_value = ["file1.py"]
    mock_check.return_value = True
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code == 1
    captured = capsys.readouterr()
    assert "Validation failed" in captured.out

@patch('validate_no_todos.get_changed_files')
def test_main_no_changed_files(mock_get_changed, capsys):
    mock_get_changed.return_value = []
    
    with pytest.raises(SystemExit) as e:
        main()
        
    assert e.value.code == 0
    captured = capsys.readouterr()
    assert "No changed files found" in captured.out
