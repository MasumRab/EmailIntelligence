import pytest
import tempfile
import json
import subprocess
from pathlib import Path

def test_manifest_processing():
    manifest_data = {
        "branches": [
            {"name": "main", "target": "main"},
            {"name": "non-existent-branch", "target": "main"}
        ]
    }
    
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(manifest_data, f)
        manifest_path = f.name
        
    try:
        result = subprocess.run(
            ["python", "scripts/orchestration/check_alignment_status.py", manifest_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        output = json.loads(result.stdout)
        
        assert "summary" in output
        assert output["summary"]["total_branches"] == 2
        assert output["summary"]["missing_branches"] == 1
        
        assert len(output["results"]) == 2
        
        main_result = next(r for r in output["results"] if r["branch"] == "main")
        assert main_result["alignment_status"]["status"] == "exists"
        
        missing_result = next(r for r in output["results"] if r["branch"] == "non-existent-branch")
        assert missing_result["alignment_status"]["status"] == "missing"
    finally:
        Path(manifest_path).unlink(missing_ok=True)
