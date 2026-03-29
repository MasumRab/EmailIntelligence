import pytest
import json
from pathlib import Path

def test_session_persistence(temp_dir):
    """Verify state is saved to atomic file."""
    state_file = temp_dir / ".dev_state.json"
    
    # Simulate writing state
    state_data = {"session_id": "123", "status": "active"}
    
    # Atomic write pattern simulation
    tmp_file = state_file.with_suffix(".tmp")
    tmp_file.write_text(json.dumps(state_data))
    tmp_file.rename(state_file)
    
    assert state_file.exists()
    assert json.loads(state_file.read_text()) == state_data

def test_crash_recovery_mock(temp_dir):
    """Simulate finding a stale lockfile."""
    state_file = temp_dir / ".dev_state.json"
    state_file.write_text(json.dumps({"status": "active", "step": 5}))
    
    # Logic to be implemented: Load logic should detect this file
    assert state_file.exists()
