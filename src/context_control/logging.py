"""Logging infrastructure for Agent Context Control library."""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    format_string: Optional[str] = None,
) -> logging.Logger:
    """Setup logging configuration for the context control library.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path to write logs to
        format_string: Optional custom format string

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger("context_control")
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Default format
    if format_string is None:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - " "[%(context_id)s] %(message)s"
        )

    formatter = logging.Formatter(format_string)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "context_control") -> logging.Logger:
    """Get a logger instance for the specified name.

    Args:
        name: Logger name (will be prefixed with context_control)

    Returns:
        Logger instance
    """
    if name.startswith("context_control"):
        return logging.getLogger(name)
    else:
        return logging.getLogger(f"context_control.{name}")


class ContextAdapter(logging.LoggerAdapter):
    """Logger adapter that adds context_id to log records."""

    def __init__(self, logger: logging.Logger, context_id: Optional[str] = None):
        super().__init__(logger, {"context_id": context_id or "unknown"})

    def process(self, msg, kwargs):
        """Process the logging record to include context_id."""
        # Merge our context extra with any existing extra
        extra = kwargs.get("extra", {})
        extra.update(self.extra)
        kwargs["extra"] = extra
        return msg, kwargs


def get_context_logger(
    context_id: Optional[str] = None, name: str = "context_control"
) -> ContextAdapter:
    """Get a context-aware logger that includes context_id in all log messages.

    Args:
        context_id: Optional context identifier to include in logs
        name: Logger name

    Returns:
        ContextAdapter instance
    """
    logger = get_logger(name)
    return ContextAdapter(logger, context_id)
