"""
Service management for the launch system.

This module handles starting, stopping, and managing various services
(Python backend, Node.js frontend, TypeScript backend, etc.).
"""

import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict

from setup.project_config import get_project_config
from src.core.security import validate_path_safety

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent


def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    try:
        python_exe = get_python_executable()
        # Validate the python executable path to prevent command injection
        if not validate_path_safety(python_exe):
            logger.error(f"Unsafe Python executable path: {python_exe}")
            return False

        result = subprocess.run([python_exe, "-c", "import uvicorn"], capture_output=True)
        return result.returncode == 0
    except Exception:
        return False


def check_node_npm_installed() -> bool:
    """Check if Node.js and npm are installed."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True)
        if result.returncode != 0:
            return False

        result = subprocess.run(["npm", "--version"], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def install_nodejs_dependencies(directory: str, update: bool = False) -> bool:
    """Install Node.js dependencies in a directory."""
    dir_path = ROOT_DIR / directory
    if not dir_path.exists():
        logger.warning(f"Directory {directory} does not exist, skipping npm install")
        return False

    # Validate directory path to prevent directory traversal
    if not validate_path_safety(str(dir_path), str(ROOT_DIR)):
        logger.error(f"Unsafe directory path: {dir_path}")
        return False

    package_json = dir_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json in {directory}, skipping npm install")
        return False

    node_modules = dir_path / "node_modules"
    if node_modules.exists() and not update:
        logger.info(f"Node.js dependencies already installed in {directory}")
        return True

    logger.info(f"Installing Node.js dependencies in {directory}...")
    try:
        if update:
            cmd = ["npm", "update"]
        else:
            cmd = ["npm", "install"]

        result = subprocess.run(cmd, cwd=dir_path, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Node.js dependencies installed successfully in {directory}")
            return True
        else:
            logger.error(f"Failed to install Node.js dependencies in {directory}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing Node.js dependencies: {e}")
        return False


def start_client():
    """Start the Node.js frontend client."""
    logger.info("Starting Node.js frontend client...")
    client_dir = ROOT_DIR / "client"

    if not client_dir.exists():
        logger.error("Client directory not found")
        return

    # Validate directory path to prevent directory traversal
    if not validate_path_safety(str(client_dir), str(ROOT_DIR)):
        logger.error(f"Unsafe client directory path: {client_dir}")
        return

    try:
        # Check if dependencies are installed
        if not install_nodejs_dependencies("client"):
            logger.error("Failed to install client dependencies")
            return

        # Start the development server
        logger.info("Starting client development server...")
        process = subprocess.Popen(["npm", "run", "dev"], cwd=client_dir)
        from setup.utils import process_manager
        process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start client: {e}")


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    server_dir = ROOT_DIR / "backend" / "server-ts"

    if not server_dir.exists():
        logger.error("TypeScript backend directory not found")
        return

    # Validate directory path to prevent directory traversal
    if not validate_path_safety(str(server_dir), str(ROOT_DIR)):
        logger.error(f"Unsafe server directory path: {server_dir}")
        return

    try:
        # Check if dependencies are installed
        if not install_nodejs_dependencies("backend/server-ts"):
            logger.error("Failed to install TypeScript backend dependencies")
            return

        # Start the server
        logger.info("Starting TypeScript backend server...")
        process = subprocess.Popen(["npm", "start"], cwd=server_dir)
        from setup.utils import process_manager
        process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start TypeScript backend: {e}")


def get_python_executable() -> str:
    """Get the Python executable path."""
    venv_path = ROOT_DIR / "venv"
    if sys.platform == "win32":
        python_exe = venv_path / "Scripts" / "python.exe"
    else:
        python_exe = venv_path / "bin" / "python"

    if python_exe.exists():
        return str(python_exe)
    return sys.executable


def start_backend(host: str, port: int, debug: bool = False):
    """Start the Python backend server."""
    python_exe = get_python_executable()

    # Validate the python executable path to prevent command injection
    if not validate_path_safety(python_exe):
        logger.error(f"Unsafe Python executable path: {python_exe}")
        return

    # Sanitize host parameter to prevent command injection
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        logger.error(f"Invalid host format: {host}")
        return

    backend_dir = ROOT_DIR / "src" / "backend" / "python_backend"
    if not backend_dir.exists():
        logger.error("Python backend directory not found")
        return

    # Validate backend directory path
    if not validate_path_safety(str(backend_dir), str(ROOT_DIR)):
        logger.error(f"Unsafe backend directory path: {backend_dir}")
        return

    logger.info(f"Starting Python backend on {host}:{port}...")
    try:
        cmd = [
            python_exe, "-m", "uvicorn", "src.backend.python_backend.main:app",
            "--host", host, "--port", str(port)
        ]
        if debug:
            cmd.append("--reload")

        process = subprocess.Popen(cmd, cwd=ROOT_DIR)
        from setup.utils import process_manager
        process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start Python backend: {e}")


def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
    """Start a Node.js service."""
    logger.info(f"Starting {service_name} on port {port}...")

    if not service_path.exists():
        logger.error(f"Service path {service_path} does not exist")
        return

    # Validate service path to prevent directory traversal
    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return

    try:
        # Ensure dependencies are installed
        setup_node_dependencies(service_path, service_name)

        # Start the service
        env = os.environ.copy()
        env["PORT"] = str(port)
        # Sanitize the API URL to prevent injection
        env["API_URL"] = api_url.replace('"', '').replace("'", "")

        if (service_path / "package.json").exists():
            # Check if it's a dev script or start script
            with open(service_path / "package.json", "r") as f:
                import json
                package_data = json.load(f)
                scripts = package_data.get("scripts", {})

                if "dev" in scripts:
                    cmd = ["npm", "run", "dev"]
                elif "start" in scripts:
                    cmd = ["npm", "start"]
                else:
                    logger.warning(f"No suitable npm script found for {service_name}")
                    return

            process = subprocess.Popen(cmd, cwd=service_path, env=env)
            from setup.utils import process_manager
            process_manager.add_process(process)
        else:
            logger.error(f"No package.json found for {service_name}")
    except Exception as e:
        logger.error(f"Failed to start {service_name}: {e}")


def setup_node_dependencies(service_path: Path, service_name: str):
    """Set up Node.js dependencies for a service."""
    if not service_path.exists():
        logger.warning(f"Service path {service_path} does not exist")
        return

    # Validate service path to prevent directory traversal
    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return

    logger.info(f"Installing Node.js dependencies for {service_name} in {service_path}...")
    try:
        cmd = ["npm", "install"]
        result = subprocess.run(cmd, cwd=service_path, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Node.js dependencies installed successfully for {service_name}")
            return True
        else:
            logger.error(f"Failed to install Node.js dependencies for {service_name}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing Node.js dependencies for {service_name}: {e}")
        return False