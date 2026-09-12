"""
Backup Command Module
"""

from argparse import Namespace
from typing import Any, Dict

from ..interface import Command


class BackupCommand(Command):
    """
    Command for creating snapshots of platform data.
    """

    def __init__(self):
        self._security_validator = None

    @property
    def name(self) -> str:
        return "backup"

    @property
    def description(self) -> str:
        return "Create a backup of database and configuration files"

    def add_arguments(self, parser: Any) -> None:
        parser.add_argument("--dir", default="./backups", help="Backup directory")

    def get_dependencies(self) -> Dict[str, Any]:
        return {"security_validator": "SecurityValidator"}

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        print(f"Starting backup to '{args.dir}'...")
        return 0
