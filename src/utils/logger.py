"""
Structured logging configuration for EmailIntelligence CLI

This module configures structlog for structured logging, supporting both
JSON output (for production/parsing) and pretty console output (for development).
"""

import sys
import logging
import structlog
from typing import Any, Dict, Optional
from ..core.config import settings


def configure_logging(
    log_level: str = None,
    json_format: bool = None,
    log_file: Optional[str] = None
) -> None:
    """
    Configure structured logging based on settings.
    
    Args:
        log_level: Override log level from settings
        json_format: Override log format from settings
        log_file: Override log file path from settings
    """
    level_name = log_level or settings.log_level
    use_json = json_format if json_format is not None else (settings.log_format.lower() == "json")
    
    # Map string level to logging constant
    level = getattr(logging, level_name.upper(), logging.INFO)
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )
    
    # Processors common to both formats
    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Add format-specific processor
    if use_json:
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer(colors=True))
    
    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure file logging if requested
    file_path = log_file or settings.log_file
    if file_path:
        file_handler = logging.FileHandler(file_path)
        file_handler.setLevel(level)
        # Always use JSON for file logs for easier parsing
        formatter = structlog.stdlib.ProcessorFormatter(
            processor=structlog.processors.JSONRenderer(),
        )
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)


def get_logger(name: str = None) -> Any:
    """
    Get a structured logger instance.
    
    Args:
        name: Optional logger name (defaults to module name)
        
    Returns:
        Structured logger instance
    """
    return structlog.get_logger(name)


# Initialize logging with default settings
configure_logging()
