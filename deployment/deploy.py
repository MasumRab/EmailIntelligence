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
import os
import subprocess
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
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
            cwd=cwd or str(PROJECT_ROOT)
        )
        logger.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(e.stderr)
        return False

# Removed local_environment function

def docker_environment(command, compose_file):
    """Manage a Docker-based environment."""
    if command == "up":
        return run_command(f"docker-compose -f {compose_file} up -d")
    elif command == "down":
        return run_command(f"docker-compose -f {compose_file} down")
    elif command == "build":
        return run_command(f"docker-compose -f {compose_file} build")
    elif command == "logs":
        return run_command(f"docker-compose -f {compose_file} logs -f")
    elif command == "status":
        return run_command(f"docker-compose -f {compose_file} ps")
    elif command == "test":
        return run_command(f"docker-compose -f {compose_file} exec backend python -m pytest tests/")
    elif command == "migrate":
        logger.info("Database migrations are handled by the application on startup")
        return True
    elif command == "backup":
        return run_command(f"docker-compose -f {compose_file} exec postgres pg_dump -U postgres -d emailintelligence > backup.sql")
    elif command == "restore":
        return run_command(f"docker-compose -f {compose_file} exec -T postgres psql -U postgres -d emailintelligence < backup.sql")
    else:
        logger.error(f"Unknown command: {command}")
        return False

def main():
    """Main entry point for the deployment script."""
    parser = argparse.ArgumentParser(description="Deployment Script for EmailIntelligence")
    parser.add_argument("environment", choices=["dev", "staging", "prod"], help="Deployment environment") # Removed "local"
    parser.add_argument("command", choices=["up", "down", "build", "logs", "status", "test", "migrate", "backup", "restore"], help="Command to execute")
    args = parser.parse_args()

    # Set up environment variables
    os.environ["PROJECT_ROOT"] = str(PROJECT_ROOT)

    # Execute the command for the specified environment
    # Removed local environment block
    if args.environment == "dev":
        compose_file = str(PROJECT_ROOT / "deployment" / "docker-compose.dev.yml")
        success = docker_environment(args.command, compose_file)
    elif args.environment == "staging":
        compose_file = str(PROJECT_ROOT / "deployment" / "docker-compose.staging.yml")
        success = docker_environment(args.command, compose_file)
    elif args.environment == "prod":
        compose_file = str(PROJECT_ROOT / "deployment" / "docker-compose.production.yml")
        success = docker_environment(args.command, compose_file)
    else:
        logger.error(f"Unknown environment: {args.environment}")
        success = False

    # Exit with appropriate status code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()