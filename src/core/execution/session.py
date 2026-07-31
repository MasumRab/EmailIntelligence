import json
from pathlib import Path
from typing import Optional, Callable
from src.core.models.orchestration import Session, SessionStatus
from src.core.utils.logger import get_logger

STATE_FILE = Path(".dev_state.json")
logger = get_logger()


class SessionManager:
    """Manages atomic persistence of session state with auto-cleanup on success."""

    def __init__(self):
        self.auto_cleanup = True

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
        session.updated_at = session.model_dump()["updated_at"]
        tmp_file = STATE_FILE.with_suffix(".tmp")
        tmp_file.write_text(session.model_dump_json())
        tmp_file.rename(STATE_FILE)
        logger.debug(f"Session saved: {session.id}")

    def clear(self):
        if STATE_FILE.exists():
            STATE_FILE.unlink()
            logger.debug("Session state cleared")

    def cleanup_on_success(self, session: Session):
        """Auto-cleanup session on successful completion."""
        if not self.auto_cleanup:
            return
        if session.status == SessionStatus.COMPLETED:
            self.clear()
            logger.info("Session auto-cleaned on successful completion")

    def run_with_session(
        self, session: Session, fn: Callable[[Session], None]
    ) -> Session:
        """Execute function within session context with auto-cleanup."""
        try:
            self.save(session)
            fn(session)
            session.status = SessionStatus.COMPLETED
            self.save(session)
            self.cleanup_on_success(session)
            return session
        except Exception as e:
            session.status = SessionStatus.FAILED
            self.save(session)
            logger.error(f"Session failed: {e}")
            raise
