#!/usr/bin/env python3
"""
Database Migration Script for EmailIntelligence

This script helps manage database migrations for the EmailIntelligence project.
It uses the Drizzle ORM migration system.

Usage:
    python migrate.py [command]

Commands:
    generate    - Generate a new migration
    apply       - Apply pending migrations
    status      - Check migration status
    rollback    - Rollback the last migration
"""

import argparse
import logging
import os
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("migrate")

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent


def run_command(command, cwd=None):
    """Run a shell command and log the output."""
    logger.info(f"Running command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            text=True,
            capture_output=True,
            cwd=cwd or str(PROJECT_ROOT),
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False


def generate_migration():
    """Generate a new migration."""
    return run_command("npx drizzle-kit generate:pg")


def apply_migrations():
    """Apply pending migrations."""
    return run_command("npx drizzle-kit migrate:pg")


def check_migration_status():
    """Check migration status."""
    return run_command("npx drizzle-kit status:pg")


def rollback_migration():
    """Rollback the last migration."""
    return run_command("npx drizzle-kit rollback:pg")


def main():
    """Main entry point for the migration script."""
    parser = argparse.ArgumentParser(
        description="Database Migration Script for EmailIntelligence"
    )
    parser.add_argument(
        "command",
        choices=["generate", "apply", "status", "rollback"],
        help="Migration command to execute",
    )
    args = parser.parse_args()

    # Set up environment variables
    os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

    # Load environment variables from .env file if it exists
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        logger.info("Loading environment variables from .env file")
        from dotenv import load_dotenv

        load_dotenv(env_file)

    # Execute the command
    if args.command == "generate":
        success = generate_migration()
    elif args.command == "apply":
        success = apply_migrations()
    elif args.command == "status":
        success = check_migration_status()
    elif args.command == "rollback":
        success = rollback_migration()
    else:
        logger.error(f"Unknown command: {args.command}")
        success = False

    # Exit with appropriate status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
