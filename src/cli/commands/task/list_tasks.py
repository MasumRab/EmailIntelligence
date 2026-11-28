"""
List Tasks Command Module
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class ListTasksCommand(Command):
    """
    Command for listing and filtering project tasks.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "task-list"

    @property
    def description(self) -> str:
        return "List and filter project tasks"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--status", help="Filter by status")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        print("Listing tasks...")
        return 0
