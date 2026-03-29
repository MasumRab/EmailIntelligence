import pytest
import subprocess
import json

def test_schema_json_output():
    """Verify dev.py --json schema returns valid JSON."""
    result = subprocess.run(
        ["python3", "dev.py", "--json", "schema"],
        capture_output=True,
        text=True,
        check=True
    )
    
    # Parse output as JSON
    data = json.loads(result.stdout)
    
    assert "ConflictModel" in data
    assert "HistoryPlan" in data
    assert "Session" in data

def test_ide_init_vscode():
    """Verify ide-init creates .vscode/tasks.json."""
    subprocess.run(
        ["python3", "dev.py", "ide", "init", "--target", "vscode"],
        check=True
    )
    
    from pathlib import Path
    assert Path(".vscode/tasks.json").exists()
