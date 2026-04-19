#!/usr/bin/env python3
"""
CLI State Persistence Module

Provides state management for command chaining and context preservation
during CLI tool execution.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime
import threading


@dataclass
class CLIState:
    """Represents the current CLI execution state."""
    session_id: str
    command_chain: List[str]
    working_directory: str
    branch: Optional[str]
    start_time: str
    end_time: Optional[str]
    status: str  # pending, running, completed, failed
    results: Dict[str, Any]
    metadata: Dict[str, Any]


class CLIStateManager:
    """
    Manages CLI tool state across multiple invocations.
    
    Features:
    - Session persistence
    - Command chaining
    - Result sharing between tools
    - Error tracking
    """

    STATE_DIR = ".cli_state"
    MAX_SESSIONS = 100

    def __init__(self, state_dir: Optional[str] = None, persist: bool = True):
        self.persist = persist
        self.state_dir = Path(state_dir or self.STATE_DIR)
        self._current_state: Optional[CLIState] = None
        self._lock = threading.Lock()
        
        if self.persist:
            self.state_dir.mkdir(parents=True, exist_ok=True)
            self._cleanup_old_sessions()

    def _cleanup_old_sessions(self) -> None:
        """Remove old session files to prevent disk buildup."""
        import glob
        session_files = glob.glob(str(self.state_dir / "*.json"))
        if len(session_files) > self.MAX_SESSIONS:
            # Keep the most recent sessions
            session_files.sort()
            for old_file in session_files[:-self.MAX_SESSIONS]:
                try:
                    os.remove(old_file)
                except OSError:
                    pass

    def start_session(self, command_chain: List[str], **metadata) -> CLIState:
        """
        Start a new CLI session.
        
        Args:
            command_chain: List of commands to execute
            **metadata: Additional metadata to store
            
        Returns:
            CLIState object for this session
        """
        with self._lock:
            self._current_state = CLIState(
                session_id=datetime.now().strftime("%Y%m%d%H%M%S%f"),
                command_chain=command_chain,
                working_directory=str(Path.cwd()),
                branch=self._get_current_branch(),
                start_time=datetime.now().isoformat(),
                end_time=None,
                status="running",
                results={},
                metadata=metadata
            )
            
            if self.persist:
                self._save_state()
            
            return self._current_state

    def _get_current_branch(self) -> Optional[str]:
        """Get current Git branch."""
        try:
            import subprocess
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.stdout.strip() or None
        except Exception:
            return None

    def update_status(self, status: str) -> None:
        """Update the current session status."""
        with self._lock:
            if self._current_state:
                self._current_state.status = status
                self._current_state.end_time = datetime.now().isoformat()
                if self.persist:
                    self._save_state()

    def add_result(self, key: str, value: Any) -> None:
        """Add a result to the current session."""
        with self._lock:
            if self._current_state:
                self._current_state.results[key] = value
                if self.persist:
                    self._save_state()

    def add_metadata(self, **kwargs) -> None:
        """Add metadata to current session."""
        with self._lock:
            if self._current_state:
                self._current_state.metadata.update(kwargs)
                if self.persist:
                    self._save_state()

    def end_session(self, status: str = "completed") -> Optional[str]:
        """
        End the current session.
        
        Args:
            status: Final status (completed, failed, etc.)
            
        Returns:
            Session ID if persisted
        """
        with self._lock:
            if not self._current_state:
                return None
            
            self._current_state.status = status
            self._current_state.end_time = datetime.now().isoformat()
            session_id = self._current_state.session_id
            
            if self.persist:
                self._save_state()
            
            self._current_state = None
            return session_id

    def _save_state(self) -> None:
        """Save current state to file."""
        if not self._current_state:
            return
        
        state_file = self.state_dir / f"{self._current_state.session_id}.json"
        with open(state_file, 'w') as f:
            json.dump(asdict(self._current_state), f, indent=2, default=str)

    def load_session(self, session_id: str) -> Optional[CLIState]:
        """Load a previous session by ID."""
        state_file = self.state_dir / f"{session_id}.json"
        if state_file.exists():
            with open(state_file, 'r') as f:
                data = json.load(f)
                state = CLIState(**data)
                self._current_state = state
                return state
        return None

    def list_sessions(self, limit: int = 20) -> List[str]:
        """List recent session IDs."""
        if not self.persist:
            return []
        
        import glob
        session_files = sorted(
            glob.glob(str(self.state_dir / "*.json")),
            reverse=True
        )
        return [Path(f).stem for f in session_files[:limit]]

    def get_current_state(self) -> Optional[CLIState]:
        """Get the current active state."""
        return self._current_state

    @property
    def session_id(self) -> Optional[str]:
        """Get the current session ID."""
        return self._current_state.session_id if self._current_state else None


# Global state manager instance
_state_manager: Optional[CLIStateManager] = None
_lock = threading.Lock()


def get_state_manager(persist: bool = True) -> CLIStateManager:
    """
    Get the global state manager instance.
    
    Args:
        persist: Whether to persist state to disk
        
    Returns:
        CLIStateManager instance
    """
    global _state_manager
    with _lock:
        if _state_manager is None:
            _state_manager = CLIStateManager(persist=persist)
        return _state_manager


def reset_state_manager() -> None:
    """Reset the global state manager."""
    global _state_manager
    with _lock:
        _state_manager = None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="CLI State Manager")
    parser.add_argument("--list", action="store_true", help="List recent sessions")
    parser.add_argument("--load", help="Load session by ID")
    
    args = parser.parse_args()
    
    manager = get_state_manager()
    
    if args.list:
        sessions = manager.list_sessions()
        print("Recent Sessions:")
        for session_id in sessions[:20]:
            print(f"  - {session_id}")
    elif args.load:
        state = manager.load_session(args.load)
        if state:
            print(f"Loaded session {state.session_id}")
            print(f"Status: {state.status}")
            print(f"Commands: {state.command_chain}")
        else:
            print(f"Session {args.load} not found")
    else:
        print("CLI State Manager")
        print("--list: List recent sessions")
        print("--load <id>: Load session by ID")
