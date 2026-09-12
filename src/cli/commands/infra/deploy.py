"""
Deploy Command Module
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class DeployCommand(Command):
    """
    Command for building and deploying the application.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "deploy"

    @property
    def description(self) -> str:
        return "Deploy the application to production using Docker"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--no-cache", action="store_true", help="Build without cache")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        print("Starting production deployment...")
        return 0
