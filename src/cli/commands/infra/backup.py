"""
Backup Command Module

Implements automated backup of database and configuration files.
Ported from scripts/shell/ops/backup.sh.
"""

import shutil
import datetime
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict

from ..interface import Command


class BackupCommand(Command):
    """
    Command for creating snapshots of platform data and secrets.

    Backs up the SQLite database and configuration files into a timestamped
    directory, ensuring data persistence before risky operations.
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
        """Add command-specific arguments."""
        parser.add_argument(
            "--dir",
            default="./backups",
            help="Directory to store backups"
        )
        parser.add_argument(
            "--db-only",
            action="store_true",
            help="Only backup the database"
        )

    def get_dependencies(self) -> Dict[str, Any]:
        """Get required dependencies."""
        return {
            "security_validator": "SecurityValidator"
        }

    def set_dependencies(self, dependencies: Dict[str, Any]) -> None:
        """Set command dependencies."""
        self._security_validator = dependencies.get("security_validator")

    async def execute(self, args: Namespace) -> int:
        """Execute the backup command."""
        backup_root = Path(args.dir)
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target_dir = backup_root / f"backup_{timestamp}"

        # Security validation
        if self._security_validator:
            is_safe, error = self._security_validator.validate_path_security(str(backup_root.absolute()))
            if not is_safe:
                print(f"Error: Security violation for backup dir: {error}")
                return 1

        print(f"📦 Starting backup to '{target_dir}'...")

        try:
            target_dir.mkdir(parents=True, exist_ok=True)

            # 1. Database backup
            db_path = Path("./data/production.db")
            if db_path.exists():
                shutil.copy2(db_path, target_dir / "production.db")
                print("  - Database backup created.")
            else:
                print("  - Warning: Database file not found.")

            # 2. Config backup (if not db-only)
            if not args.db_only:
                config_dir = Path("./config")
                if config_dir.exists():
                    shutil.copytree(config_dir, target_dir / "config", dirs_exist_ok=True)
                    print("  - Configuration backup created.")

            print(f"\n✅ Backup successfully created at: {target_dir}")
            return 0

        except Exception as e:
            print(f"Error during backup: {e}")
            return 1
