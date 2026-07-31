import json
import logging
from datetime import datetime
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from typing import Any, Dict, Optional

LOG_DIR = Path(".dev_state/logs")
console = Console()


class StructuredLogger:
    """JSONL-based structured logger for session persistence."""

    def __init__(self, log_file: Optional[Path] = None):
        if log_file is None:
            LOG_DIR.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = LOG_DIR / f"session_{timestamp}.jsonl"
        self.log_file = log_file
        self._setup_logging()

    def _setup_logging(self):
        self.logger = logging.getLogger("dev")
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            handler = RichHandler(console=console, rich_tracebacks=True)
            handler.setFormatter(logging.Formatter("%(message)s"))
            self.logger.addHandler(handler)

    def log(self, level: str, message: str, **kwargs: Any):
        """Log to both JSONL file and standard logging."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            **kwargs,
        }
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

        log_fn = getattr(self.logger, level.lower(), self.logger.info)
        log_fn(message)

    def info(self, message: str, **kwargs: Any):
        self.log("INFO", message, **kwargs)

    def warning(self, message: str, **kwargs: Any):
        self.log("WARNING", message, **kwargs)

    def error(self, message: str, **kwargs: Any):
        self.log("ERROR", message, **kwargs)

    def debug(self, message: str, **kwargs: Any):
        self.log("DEBUG", message, **kwargs)


_global_logger: Optional[StructuredLogger] = None


def get_logger() -> StructuredLogger:
    global _global_logger
    if _global_logger is None:
        _global_logger = StructuredLogger()
    return _global_logger


def set_headless_mode(enabled: bool):
    """Suppress Rich output for JSON/Headless mode."""
    global console
    if enabled:
        console = Console(quiet=True, force_terminal=False, color_system=None)
    else:
        console = Console()


def get_console() -> Console:
    return console
