import os
import json
import subprocess
from scripts.generate_safety_manifest import get_local_branches_and_shas, write_manifest

def test_get_local_branches_and_shas():
    branches = get_local_branches_and_shas()
    assert isinstance(branches, dict)
    assert 'main' in branches
    # Test that values look like shas (at least 40 chars hex)
    for branch, sha in branches.items():
        assert len(sha) == 40
        # Will raise ValueError if not hex
        int(sha, 16)

def test_write_manifest(tmp_path):
    output_path = tmp_path / "manifest.json"
    branches = {"main": "0bd9b58f9878c8e8e6fdc3996fa3aa2db9501a6c"}
    write_manifest(output_path, branches)
    
    assert output_path.exists()
    
    with open(output_path) as f:
        data = json.load(f)
        
    assert "branches" in data
    assert data["branches"] == branches
