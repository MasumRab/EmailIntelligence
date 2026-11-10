import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime


class CLIState:
    """Manages CLI state persistence for command chaining."""

    STATE_FILE = Path.home() / ".cli_state.json"

    def __init__(self):
        self._state = self._load_defaults()
        self.load()

    def _load_defaults(self) -> Dict[str, Any]:
        return {
            "last_branch": None,
            "last_command": None,
            "last_health_score": None,
            "last_conflicts_count": 0,
            "command_chain": [],
            "last_run": None,
        }

    def load(self) -> None:
        """Load state from file."""
        if self.STATE_FILE.exists():
            try:
                with open(self.STATE_FILE) as f:
                    self._state.update(json.load(f))
            except Exception:
                pass

    def save(self) -> None:
        """Save state to file."""
        self._state["last_run"] = datetime.now().isoformat()
        self.STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.STATE_FILE, "w") as f:
            json.dump(self._state, f, indent=2)

    def update(self, key: str, value: Any) -> None:
        """Update a state value."""
        self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a state value."""
        return self._state.get(key, default)

    def append_chain(self, command: str) -> None:
        """Append command to chain history."""
        self._state.setdefault("command_chain", [])
        self._state["command_chain"].append(
            {"command": command, "timestamp": datetime.now().isoformat()}
        )
        self._state["command_chain"] = self._state["command_chain"][-50:]

    def get_chain(self) -> List[Dict]:
        """Get command chain history."""
        return self._state.get("command_chain", [])
