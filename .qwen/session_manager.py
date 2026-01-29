#!/usr/bin/env python3
"""
Session Manager for Taskmaster Project

This module handles session initialization and state management
for the Taskmaster project following the specified requirements.
"""

import json
import uuid
import os
from datetime import datetime
from pathlib import Path


class SessionManager:
    def __init__(self, project_root):
        """
        Initialize the SessionManager with the project root path.
        
        Args:
            project_root (str): The absolute path to the project root
        """
        self.project_root = Path(project_root).resolve()
        self.qwen_dir = self.project_root / ".qwen"
        
        # Ensure .qwen directory exists
        self.qwen_dir.mkdir(exist_ok=True)
        
        # Define state file paths
        self.state_file = self.qwen_dir / "state.json"
        self.session_file = self.qwen_dir / "session.json"
        self.handoff_file = self.qwen_dir / "handoff.json"
        
        # Initialize state files if they don't exist
        self._initialize_state_files()
    
    def _initialize_state_files(self):
        """Initialize state files with default values if they don't exist."""
        # Initialize state.json
        if not self.state_file.exists():
            state_data = {
                "current_session": None,
                "command_history": []
            }
            self._write_json_file(self.state_file, state_data)
        
        # Initialize session.json
        if not self.session_file.exists():
            session_data = {
                "session_id": None,
                "start_time": None,
                "project_path": str(self.project_root),
                "goals": [],
                "status": "inactive"
            }
            self._write_json_file(self.session_file, session_data)
        
        # Initialize handoff.json
        if not self.handoff_file.exists():
            handoff_data = {
                "pending_handoffs": []
            }
            self._write_json_file(self.handoff_file, handoff_data)
    
    def _write_json_file(self, filepath, data):
        """Write data to a JSON file with proper formatting."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def _read_json_file(self, filepath):
        """Read data from a JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _backup_state_file(self):
        """Create a backup of the current state.json file."""
        if self.state_file.exists():
            backup_path = self.state_file.with_suffix('.json.backup')
            state_data = self._read_json_file(self.state_file)
            self._write_json_file(backup_path, state_data)
    
    def start_session(self, goals=None, session_id=None):
        """
        Start a new session with the specified goals.
        
        Args:
            goals (list): List of session goals
            session_id (str): Optional session ID (will be generated if not provided)
        
        Returns:
            dict: Session information
        """
        if goals is None:
            goals = []
        
        # Generate session ID if not provided
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        # Create timestamp
        start_time = datetime.utcnow().isoformat() + "Z"
        
        # Load current state
        state_data = self._read_json_file(self.state_file)
        
        # Backup state before making changes
        self._backup_state_file()
        
        # Update state with new session info
        state_data["current_session"] = session_id
        state_data["command_history"].append({
            "command": "session-start",
            "timestamp": start_time,
            "session_id": session_id
        })
        
        # Write updated state
        self._write_json_file(self.state_file, state_data)
        
        # Update session file
        session_data = {
            "session_id": session_id,
            "start_time": start_time,
            "project_path": str(self.project_root),
            "goals": goals,
            "status": "active"
        }
        self._write_json_file(self.session_file, session_data)
        
        return session_data
    
    def end_session(self):
        """End the current active session."""
        # Load current state
        state_data = self._read_json_file(self.state_file)
        
        # Backup state before making changes
        self._backup_state_file()
        
        # Update state to remove current session
        session_id = state_data.get("current_session")
        if session_id:
            state_data["current_session"] = None
            state_data["command_history"].append({
                "command": "session-end",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "session_id": session_id
            })
            
            # Write updated state
            self._write_json_file(self.state_file, state_data)
        
        # Update session file to inactive
        session_data = self._read_json_file(self.session_file)
        session_data["status"] = "inactive"
        self._write_json_file(self.session_file, session_data)
        
        return session_id
    
    def get_current_session(self):
        """Get information about the current session."""
        try:
            return self._read_json_file(self.session_file)
        except FileNotFoundError:
            return None
    
    def get_project_context(self):
        """Capture initial project context."""
        context = {}
        
        # Read QWEN.md if it exists
        qwem_md_path = self.project_root / "QWEN.md"
        if qwem_md_path.exists():
            with open(qwem_md_path, 'r', encoding='utf-8') as f:
                context['qwem_md_content'] = f.read()
        
        # Check for pending handoffs
        try:
            handoff_data = self._read_json_file(self.handoff_file)
            context['pending_handoffs'] = handoff_data.get('pending_handoffs', [])
        except FileNotFoundError:
            context['pending_handoffs'] = []
        
        # Get command history
        try:
            state_data = self._read_json_file(self.state_file)
            context['command_history'] = state_data.get('command_history', [])
        except FileNotFoundError:
            context['command_history'] = []
        
        return context


def initialize_session_manager():
    """Initialize the session manager for the current project."""
    project_root = Path.cwd()
    
    # If we're inside a .taskmaster directory, adjust the project root
    if '.taskmaster' in str(project_root):
        # Find the actual .taskmaster project root
        parts = project_root.parts
        for i, part in enumerate(parts):
            if part == '.taskmaster':
                # The parent of .taskmaster is the project root
                project_root = Path(*parts[:i+1])
                break
    
    session_manager = SessionManager(project_root)
    return session_manager


if __name__ == "__main__":
    # Example usage
    print("Initializing session manager...")
    sm = initialize_session_manager()
    
    print(f"Project root: {sm.project_root}")
    print(f"Qwen directory: {sm.qwen_dir}")
    
    # Get initial context
    context = sm.get_project_context()
    print(f"Found QWEN.md: {'qwem_md_content' in context}")
    print(f"Pending handoffs: {len(context.get('pending_handoffs', []))}")
    print(f"Command history entries: {len(context.get('command_history', []))}")
    
    # Start a sample session
    goals = [
        "Implement session management system",
        "Document development process",
        "Ensure state persistence"
    ]
    
    session_info = sm.start_session(goals=goals)
    print(f"Started session: {session_info['session_id']}")
    print(f"Session goals: {session_info['goals']}")
    
    # End the session
    ended_session_id = sm.end_session()
    print(f"Ended session: {ended_session_id}")