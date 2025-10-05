#!/usr/bin/env python3
"""
EmailIntelligence Launcher (v3)

This script automates the environment setup for the Email Intelligence Platform
and then hands off control to the main application entry point.

Key Features:
-   **Environment Setup**: Manages the Python virtual environment and installs
    dependencies from `requirements.txt`.
-   **NLTK Data Download**: Ensures necessary NLTK data models are available.
-   **Application Handoff**: Executes the core application located at `src/main.py`.
"""

import argparse
import logging
import os
import shutil
import subprocess
import sys
import venv
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent
VENV_DIR = "venv"

def get_python_executable() -> str:
    """Gets the path to the virtual environment's Python executable."""
    if os.name == "nt":
        return str(ROOT_DIR / VENV_DIR / "Scripts" / "python.exe")
    else:
        return str(ROOT_DIR / VENV_DIR / "bin" / "python")

def prepare_environment():
    """
    Sets up the Python virtual environment and installs dependencies.
    """
    venv_path = ROOT_DIR / VENV_DIR
    if not venv_path.exists():
        logger.info(f"Creating virtual environment at {venv_path}...")
        venv.create(venv_path, with_pip=True)

    python_executable = get_python_executable()

    # Install dependencies
    requirements_path = ROOT_DIR / "requirements.txt"
    if requirements_path.exists():
        logger.info(f"Installing dependencies from {requirements_path}...")
        subprocess.check_call(
            [python_executable, "-m", "pip", "install", "-r", str(requirements_path)]
        )
    else:
        logger.warning(f"'{requirements_path}' not found. Skipping dependency installation.")

    # Download NLTK data
    logger.info("Downloading NLTK data...")
    subprocess.check_call(
        [
            python_executable,
            "-c",
            "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True);",
        ]
    )

def main():
    """
    Main entry point for the launcher script.
    """
    parser = argparse.ArgumentParser(
        description="Launch the Email Intelligence Platform."
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Host to run the server on."
    )
    parser.add_argument(
        "--port", type=int, default=7860, help="Port to run the server on."
    )
    parser.add_argument("--reload", action="store_true", help="Enable auto-reloading.")
    args, unknown_args = parser.parse_known_args()

    # Prepare the environment
    prepare_environment()

    # Run the main application
    python_executable = get_python_executable()
    main_app_path = ROOT_DIR / "src" / "main.py"

    cmd = [
        python_executable,
        str(main_app_path),
        f"--host={args.host}",
        f"--port={args.port}",
    ]
    if args.reload:
        cmd.append("--reload")

    # Pass any unknown arguments to the main application
    cmd.extend(unknown_args)

    logger.info(f"Starting application: {' '.join(cmd)}")

    # Set PYTHONPATH to include the project root
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as e:
        logger.error(f"Application failed to run: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Launcher shutting down.")
        sys.exit(0)

if __name__ == "__main__":
    main()