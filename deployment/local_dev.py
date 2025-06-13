#!/usr/bin/env python3
"""
Local Development Server for EmailIntelligence

This script sets up a local development environment for the EmailIntelligence project.
It provides a simple way to run the Python backend with hot-reloading and debugging.

Usage:
    python local_dev.py [--port PORT] [--host HOST] [--debug]
"""

import argparse
import os
import sys
import logging
import subprocess
import time
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("local-dev")

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def setup_environment():
    """Set up the development environment variables."""
    os.environ.setdefault("NODE_ENV", "development")
    os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/emailintelligence")
    os.environ.setdefault("DEBUG", "True")
    
    # Check if .env file exists and load it
    env_file = PROJECT_ROOT / ".env"
    if env_file.exists():
        logger.info("Loading environment variables from .env file")
        from dotenv import load_dotenv
        load_dotenv(env_file)

def check_dependencies():
    """Check if all required dependencies are installed."""
    try:
        import uvicorn
        import fastapi
        import psycopg2
        logger.info("All required Python dependencies are installed")
        return True
    except ImportError as e:
        logger.error(f"Missing dependency: {e}")
        logger.info("Installing required dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(PROJECT_ROOT / "requirements.txt")])
            logger.info("Dependencies installed successfully")
            return True
        except subprocess.CalledProcessError:
            logger.error("Failed to install dependencies")
            return False

def check_database():
    """Check if the database is accessible."""
    try:
        import psycopg2
        conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
        conn.close()
        logger.info("Database connection successful")
        return True
    except psycopg2.Error as e:
        logger.error(f"Database connection failed: {e}")
        logger.info("Make sure PostgreSQL is running and the DATABASE_URL is correct")
        return False

def run_server(host, port, debug):
    """Run the development server."""
    try:
        import uvicorn
        from server.python_backend.main import app
        
        logger.info(f"Starting development server at http://{host}:{port}")
        uvicorn.run(
            "server.python_backend.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="debug" if debug else "info",
            access_log=True
        )
    except ImportError as e:
        logger.error(f"Failed to import required modules: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main entry point for the local development server."""
    parser = argparse.ArgumentParser(description="Local Development Server for EmailIntelligence")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the server on")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    logger.info("Setting up local development environment")
    setup_environment()
    
    if not check_dependencies():
        logger.error("Failed to set up dependencies")
        sys.exit(1)
    
    if not check_database():
        logger.warning("Database connection failed, but continuing anyway")
    
    run_server(args.host, args.port, args.debug)

if __name__ == "__main__":
    main()