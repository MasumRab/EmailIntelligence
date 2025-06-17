#!/usr/bin/env python3
"""
Deployment Script for EmailIntelligence

This script helps manage the deployment of the EmailIntelligence application
across different environments (local, development, staging, production).

Usage:
    python deploy.py [environment] [command]

Environments:
    local       - Local development environment
    dev         - Docker-based development environment
    staging     - Staging environment
    prod        - Production environment

Commands:
    up          - Start the environment
    down        - Stop the environment
    build       - Build the environment
    logs        - View logs
    status      - Check status
    test        - Run tests
    migrate     - Run database migrations
    backup      - Backup the database
    restore     - Restore the database
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
logger = logging.getLogger("deploy")

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


# Removed local_environment function

# Define Docker Compose filenames
BASE_COMPOSE_FILE = "docker-compose.yml"
DEV_COMPOSE_FILE = "docker-compose.dev.yml"
STAG_COMPOSE_FILE = "docker-compose.stag.yml"
PROD_COMPOSE_FILE = "docker-compose.prod.yml"


def docker_environment(
    command, base_compose_file, env_compose_file, remaining_args=None
):
    """Manage a Docker-based environment."""
    if remaining_args is None:
        remaining_args = []
    compose_files_str = f"-f {base_compose_file} -f {env_compose_file}"

    if command == "up":
        return run_command(f"docker-compose {compose_files_str} up -d")
    elif command == "down":
        return run_command(f"docker-compose {compose_files_str} down")
    elif command == "build":
        return run_command(f"docker-compose {compose_files_str} build")
    elif command == "logs":
        return run_command(f"docker-compose {compose_files_str} logs -f")
    elif command == "status":
        return run_command(f"docker-compose {compose_files_str} ps")
    elif command == "test":
        # Execute tests using the run_tests.py script within the backend service
        # The run_tests.py script is expected to be in the /app/deployment directory in the container
        test_script_path = "deployment/run_tests.py"
        additional_test_args = " ".join(remaining_args)
        return run_command(
            f"docker-compose {compose_files_str} exec backend python {test_script_path} {additional_test_args}".strip()
        )
    elif command == "migrate":
        logger.info(
            "Database migrations are handled by the application on startup or via dedicated migration scripts if available."
        )
        # Example: return run_command(f"docker-compose {compose_files_str} exec backend python manage.py migrate")
        return True
    elif command == "backup":
        # Ensure backup.sql is saved outside the container, perhaps in PROJECT_ROOT/deployment
        backup_file_path = PROJECT_ROOT / "deployment" / "backup.sql"
        return run_command(
            f"docker-compose {compose_files_str} exec postgres pg_dump -U postgres -d emailintelligence > {backup_file_path}"
        )
    elif command == "restore":
        backup_file_path = PROJECT_ROOT / "deployment" / "backup.sql"
        if not backup_file_path.exists():
            logger.error(f"Backup file not found: {backup_file_path}")
            return False
        return run_command(
            f"docker-compose {compose_files_str} exec -T postgres psql -U postgres -d emailintelligence < {backup_file_path}"
        )
    else:
        logger.error(f"Unknown command: {command}")
        return False


def main():
    """Main entry point for the deployment script."""
    parser = argparse.ArgumentParser(
        description="Deployment Script for EmailIntelligence"
    )
    parser.add_argument(
        "environment", choices=["dev", "staging", "prod"], help="Deployment environment"
    )
    parser.add_argument(
        "command",
        help="Command to execute: up, down, build, logs, status, test, migrate, backup, restore. For 'test', pass script arguments after the command, e.g., 'test -- --unit'.",
    )
    # For the 'test' command, we might have additional arguments for run_tests.py
    # We parse known args first to separate deploy.py args from script args
    args, remaining_args = parser.parse_known_args()

    # Validate command choices manually now
    valid_commands = [
        "up",
        "down",
        "build",
        "logs",
        "status",
        "test",
        "migrate",
        "backup",
        "restore",
    ]
    if args.command not in valid_commands:
        logger.error(f"Invalid command: {args.command}. Choose from {valid_commands}")
        sys.exit(1)

    # Set up environment variables
    os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

    deployment_dir = PROJECT_ROOT / "deployment"
    base_file = deployment_dir / BASE_COMPOSE_FILE

    env_specific_file = None
    if args.environment == "dev":
        env_specific_file = deployment_dir / DEV_COMPOSE_FILE
    elif args.environment == "staging":
        env_specific_file = deployment_dir / STAG_COMPOSE_FILE
    elif args.environment == "prod":
        env_specific_file = deployment_dir / PROD_COMPOSE_FILE

    if not base_file.exists():
        logger.error(f"Base Docker Compose file not found: {base_file}")
        sys.exit(1)
    if not env_specific_file or not env_specific_file.exists():
        logger.error(
            f"Environment-specific Docker Compose file not found: {env_specific_file}"
        )
        sys.exit(1)
    else:
        logger.error(f"Unknown environment: {args.environment}")
        success = False

    # Pass remaining_args to docker_environment only if command is 'test'
    success = docker_environment(
        args.command,
        str(base_file),
        str(env_specific_file),
        remaining_args=(remaining_args if args.command == "test" else []),
    )
    # Exit with appropriate status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
