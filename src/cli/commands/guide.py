"""
Guide Command Module

Interactive workflow guide for Email Intelligence CLI.
Provides a unified interface for complex developer context tasks.
"""

from argparse import Namespace
from typing import Any, Dict
import logging

from .interface import Command

logger = logging.getLogger(__name__)

class GuideCommand(Command):
    """
    Command for an interactive developer guide and orchestration.
    """

    def __init__(self):
        self._security_validator = None
        self._nlp = None

    @property
    def name(self) -> str:
        return "guide"

    @property
    def description(self) -> str:
        return "Interactive workflow guide for orchestration tasks"

    def add_arguments(self, parser: Any) -> None:
        """Add command-specific arguments."""
        pass

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator",
            "nlp": "NLPService"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")
        self._nlp = dependencies.get("nlp")

    async def execute(self, args: Namespace) -> int:
        """Execute the guide command."""
        print("💡 Interactive Workflow Guide (Agent-Driven Edition)")
        print("To manage complex workflows, use the agent-anchored commands instead:")
        print("  - speckit.specify.toml")
        print("  - speckit.plan.toml")
        print("  - speckit.tasks.toml")
        print("  - speckit.analyze.toml")
        print("\nNote: For semantic intent and developer feedback analysis, please route")
        print("through LLM-driven agents. Do not use local naive text processing.")
        return 0
