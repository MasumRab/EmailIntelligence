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


def generate_migration():
    """Generate a new migration."""
    cmd = ["npx", "drizzle-kit", "generate:sqlite"]
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            check=True,
            text=True,
            capture_output=True,
            cwd=str(PROJECT_ROOT),
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False


def apply_migrations():
    """Apply pending migrations."""
    cmd = ["npx", "drizzle-kit", "migrate:sqlite"]
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            check=True,
            text=True,
            capture_output=True,
            cwd=str(PROJECT_ROOT),
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False


def check_migration_status():
    """Check migration status."""
    cmd = ["npx", "drizzle-kit", "status:sqlite"]
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            check=True,
            text=True,
            capture_output=True,
            cwd=str(PROJECT_ROOT),
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False


def rollback_migration():
    """Rollback the last migration."""
    cmd = ["npx", "drizzle-kit", "rollback:sqlite"]
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        result = subprocess.run(
            cmd,
            shell=False,
            check=True,
            text=True,
            capture_output=True,
            cwd=str(PROJECT_ROOT),
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False


def main():
    """Main entry point for the migration script."""
    parser = argparse.ArgumentParser(description="Database Migration Script for EmailIntelligence")
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
