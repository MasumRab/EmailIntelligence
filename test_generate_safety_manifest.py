import os
import json
import subprocess
from scripts.generate_safety_manifest import get_local_branches_and_shas, write_manifest
import pytest

def test_get_local_branches_and_shas():
    branches = get_local_branches_and_shas()
    assert isinstance(branches, dict)
    for branch, sha in branches.items():
        assert len(sha) == 40
        int(sha, 16)

def test_write_manifest(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    output_path = tmp_path / "manifest.json"
    branches = {"main": "0bd9b58f9878c8e8e6fdc3996fa3aa2db9501a6c"}
    write_manifest(output_path, branches)

    assert output_path.exists()

    with open(output_path) as f:
        data = json.load(f)

    assert "branches" in data
    assert data["branches"] == branches

def test_write_manifest_refuses_traversal(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(ValueError):
        write_manifest(os.path.join('..', 'escaped.json'), {'main': 'deadbeef'})

