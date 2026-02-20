import json
from pathlib import Path
from typing import Optional
from src.core.models.orchestration import Session

STATE_FILE = Path(".dev_state.json")

class SessionManager:
    """Manages atomic persistence of session state."""
    
    def load(self) -> Optional[Session]:
        if not STATE_FILE.exists():
            return None
        try:
            data = json.loads(STATE_FILE.read_text())
            return Session(**data)
        except Exception:
            return None

    def save(self, session: Session):
        """Atomic write."""
        tmp_file = STATE_FILE.with_suffix(".tmp")
        tmp_file.write_text(session.model_dump_json())
        tmp_file.rename(STATE_FILE)

    def clear(self):
        if STATE_FILE.exists():
            STATE_FILE.unlink()
