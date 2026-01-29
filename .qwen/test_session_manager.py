#!/usr/bin/env python3
"""
Test suite for the Session Management System
"""

import json
import tempfile
import shutil
from pathlib import Path
from session_manager import SessionManager


def test_session_lifecycle():
    """Test the complete session lifecycle."""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        test_dir = project_root / ".qwen"
        test_dir.mkdir()
        
        # Initialize session manager
        sm = SessionManager(project_root)
        
        # Verify initial state files were created
        assert sm.state_file.exists(), "state.json should be created"
        assert sm.session_file.exists(), "session.json should be created"
        assert sm.handoff_file.exists(), "handoff.json should be created"
        
        # Verify initial content
        with open(sm.state_file, 'r') as f:
            state_data = json.load(f)
            assert state_data["current_session"] is None
            assert len(state_data["command_history"]) == 0
        
        with open(sm.session_file, 'r') as f:
            session_data = json.load(f)
            assert session_data["status"] == "inactive"
            assert session_data["project_path"] == str(project_root)
        
        # Start a session
        goals = ["Test goal 1", "Test goal 2"]
        session_info = sm.start_session(goals=goals)
        
        # Verify session was started
        assert session_info["session_id"] is not None
        assert session_info["status"] == "active"
        assert session_info["goals"] == goals
        assert session_info["project_path"] == str(project_root)
        
        # Verify state was updated
        with open(sm.state_file, 'r') as f:
            state_data = json.load(f)
            assert state_data["current_session"] == session_info["session_id"]
            assert len(state_data["command_history"]) == 1
            assert state_data["command_history"][0]["command"] == "session-start"
        
        # End the session
        ended_session_id = sm.end_session()
        
        # Verify session was ended
        assert ended_session_id == session_info["session_id"]
        
        # Verify state was updated
        with open(sm.state_file, 'r') as f:
            state_data = json.load(f)
            assert state_data["current_session"] is None
            assert len(state_data["command_history"]) == 2
            assert state_data["command_history"][1]["command"] == "session-end"
        
        # Verify session file was updated
        with open(sm.session_file, 'r') as f:
            session_data = json.load(f)
            assert session_data["status"] == "inactive"
        
        print("✓ Session lifecycle test passed")


def test_project_context():
    """Test project context retrieval."""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        test_dir = project_root / ".qwen"
        test_dir.mkdir()
        
        # Create a sample QWEN.md file
        qwem_file = project_root / "QWEN.md"
        with open(qwem_file, 'w') as f:
            f.write("# Test QWEN.md\nThis is a test file.")
        
        # Initialize session manager
        sm = SessionManager(project_root)
        
        # Get project context
        context = sm.get_project_context()
        
        # Verify context contains expected elements
        assert "qwem_md_content" in context
        assert context["qwem_md_content"] == "# Test QWEN.md\nThis is a test file."
        assert "pending_handoffs" in context
        assert "command_history" in context
        
        print("✓ Project context test passed")


def test_backup_functionality():
    """Test state backup functionality."""
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        project_root = Path(tmpdir)
        test_dir = project_root / ".qwen"
        test_dir.mkdir()
        
        # Initialize session manager
        sm = SessionManager(project_root)
        
        # Modify state while preserving required structure but adding a custom field
        test_data = {
            "current_session": None,
            "command_history": [{"test_entry": "test_value"}],
            "custom_field": "test_value"
        }
        with open(sm.state_file, 'w') as f:
            json.dump(test_data, f)

        # Call backup function by starting a session (which triggers backup)
        sm.start_session(goals=["test"])

        # Verify backup was created
        backup_file = sm.state_file.with_suffix('.json.backup')
        assert backup_file.exists(), "Backup file should be created"

        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
            assert backup_data["custom_field"] == "test_value"
        
        print("✓ Backup functionality test passed")


if __name__ == "__main__":
    print("Running session management tests...")
    
    test_session_lifecycle()
    test_project_context()
    test_backup_functionality()
    
    print("\n✅ All tests passed!")