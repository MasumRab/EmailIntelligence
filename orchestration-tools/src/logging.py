"""Structured logging configuration."""

import logging
import json
import uuid
from datetime import datetime
from typing import Any, Optional
from pythonjsonlogger import jsonlogger

from src.config import settings


class CorrelationIDFilter(logging.Filter):
    """Filter to add correlation ID to log records."""

    def __init__(self, prefix: str = "ORCH"):
        """Initialize filter with correlation ID prefix."""
        super().__init__()
        self.prefix = prefix
        self.correlation_id = self._generate_correlation_id()

    def _generate_correlation_id(self) -> str:
        """Generate a correlation ID."""
        unique_id = str(uuid.uuid4())[:8].upper()
        return f"{self.prefix}-{unique_id}"

    def filter(self, record: logging.LogRecord) -> bool:
        """Add correlation ID to log record."""
        if not hasattr(record, "correlation_id"):
            record.correlation_id = self.correlation_id
        return True


def setup_logging(
    name: str,
    level: str = "INFO",
    log_format: str = "json",
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Setup structured logging for a module."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Add correlation ID filter
    correlation_filter = CorrelationIDFilter(settings.correlation_id_prefix)
    logger.addFilter(correlation_filter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, level.upper()))

    if log_format == "json":
        formatter = jsonlogger.JsonFormatter(
            fmt="%(timestamp)s %(level)s %(name)s %(message)s %(correlation_id)s",
            timestamp=True,
        )
    else:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(name)s - %(levelname)s - [%(correlation_id)s] - %(message)s"
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, level.upper()))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """Get or create logger with standard configuration."""
    return setup_logging(
        name,
        level=settings.log_level,
        log_format=settings.log_format,
        log_file=settings.log_file_path if settings.structured_logging else None,
    )


class StructuredLogger:
    """Wrapper for structured logging with additional context."""

    def __init__(self, logger: logging.Logger):
        """Initialize with a logger instance."""
        self.logger = logger
        self.context: dict[str, Any] = {}

    def set_context(self, **kwargs: Any) -> None:
        """Set context variables for all subsequent logs."""
        self.context.update(kwargs)

    def clear_context(self) -> None:
        """Clear context variables."""
        self.context.clear()

    def _log(
        self,
        level: int,
        message: str,
        **kwargs: Any,
    ) -> None:
        """Internal logging method with context."""
        extra = {"context": {**self.context, **kwargs}}
        self.logger.log(level, message, extra=extra)

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message."""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message."""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message."""
        self._log(logging.CRITICAL, message, **kwargs)
