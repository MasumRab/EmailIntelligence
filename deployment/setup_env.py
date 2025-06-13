#!/usr/bin/env python3
"""
Environment Setup Script for EmailIntelligence

This script helps set up the development environment for the EmailIntelligence project.
It installs dependencies, configures the database, and sets up environment variables.

Usage:
    python setup_env.py [--dev] [--force]
"""

import argparse
import os
import subprocess
import sys
import logging
from pathlib import Path
import shutil

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("setup-env")

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

def setup_python_environment(dev_mode=False):
    """Set up the Python environment."""
    logger.info("Setting up Python environment...")
    
    # Install Python dependencies
    if dev_mode:
        return run_command(f"{sys.executable} -m pip install -r requirements.txt")
    else:
        return run_command(f"{sys.executable} -m pip install -r requirements.txt --no-dev")

def setup_node_environment(dev_mode=False):
    """Set up the Node.js environment."""
    logger.info("Setting up Node.js environment...")
    
    # Check if Node.js is installed
    if not run_command("node --version"):
        logger.error("Node.js is not installed. Please install Node.js and try again.")
        return False
    
    # Install Node.js dependencies
    if dev_mode:
        return run_command("npm install")
    else:
        return run_command("npm install --production")

def setup_database():
    """Set up the database."""
    logger.info("Setting up database...")
    
    # Check if PostgreSQL is installed
    if not run_command("psql --version"):
        logger.error("PostgreSQL is not installed. Please install PostgreSQL and try again.")
        return False
    
    # Create the database if it doesn't exist
    run_command("createdb -U postgres emailintelligence || true")
    
    # Apply migrations
    return run_command("python deployment/migrate.py apply")

def setup_environment_variables(force=False):
    """Set up environment variables."""
    logger.info("Setting up environment variables...")
    
    # Check if .env file exists
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists() and not force:
        logger.info(".env file already exists. Use --force to overwrite.")
        return True
    
    # Create .env file
    env_content = """# Environment variables for EmailIntelligence
NODE_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/emailintelligence
PORT=8000
DEBUG=True
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        logger.info(f"Created .env file at {env_file}")
        return True
    except Exception as e:
        logger.error(f"Failed to create .env file: {e}")
        return False

def setup_directories():
    """Set up required directories."""
    logger.info("Setting up directories...")
    
    # Create deployment directories if they don't exist
    directories = [
        PROJECT_ROOT / "deployment" / "nginx" / "ssl",
        PROJECT_ROOT / "deployment" / "nginx" / "letsencrypt",
        PROJECT_ROOT / "deployment" / "monitoring" / "grafana" / "provisioning" / "dashboards",
        PROJECT_ROOT / "deployment" / "monitoring" / "grafana" / "provisioning" / "datasources",
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created directory: {directory}")
        except Exception as e:
            logger.error(f"Failed to create directory {directory}: {e}")
            return False
    
    return True

def main():
    """Main entry point for the environment setup script."""
    parser = argparse.ArgumentParser(description="Environment Setup Script for EmailIntelligence")
    parser.add_argument("--dev", action="store_true", help="Set up development environment")
    parser.add_argument("--force", action="store_true", help="Force overwrite of existing files")
    args = parser.parse_args()
    
    logger.info("Setting up EmailIntelligence environment...")
    
    # Set up directories
    if not setup_directories():
        logger.error("Failed to set up directories")
        sys.exit(1)
    
    # Set up environment variables
    if not setup_environment_variables(args.force):
        logger.error("Failed to set up environment variables")
        sys.exit(1)
    
    # Set up Python environment
    if not setup_python_environment(args.dev):
        logger.error("Failed to set up Python environment")
        sys.exit(1)
    
    # Set up Node.js environment
    if not setup_node_environment(args.dev):
        logger.error("Failed to set up Node.js environment")
        sys.exit(1)
    
    # Set up database
    if not setup_database():
        logger.warning("Failed to set up database, but continuing anyway")
    
    logger.info("Environment setup completed successfully!")
    logger.info("You can now run the application using:")
    logger.info("  python deployment/deploy.py local up")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())