from rich.console import Console
from rich.logging import RichHandler
import logging

# Global console instance
console = Console()

def set_headless_mode(enabled: bool):
    """Suppress Rich output for JSON/Headless mode."""
    global console
    if enabled:
        console = Console(quiet=True, force_terminal=False, color_system=None)
    else:
        # Default interactive mode
        console = Console()

def get_console() -> Console:
    return console
