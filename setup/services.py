"""
Service management for the launch system.

This module handles starting, stopping, and managing various services
(Python backend, Node.js frontend, TypeScript backend, etc.).
"""

import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional

from setup.project_config import get_project_config
from setup.utils import process_manager
from src.core.security import validate_path_safety

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent

# Validation constants
VALID_HOST_PATTERN = re.compile(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*$|^localhost$|^127\.0\.0\.1$')
VALID_PORT_RANGE = (1, 65535)


def validate_host(host: str) -> bool:
    """Validate hostname/IP address."""
    return bool(VALID_HOST_PATTERN.match(host))


def validate_port(port: int) -> bool:
    """Validate port number."""
    return VALID_PORT_RANGE[0] <= port <= VALID_PORT_RANGE[1]


def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    try:
        python_exe = get_python_executable()
        if not validate_path_safety(python_exe):
            logger.error(f"Unsafe Python executable path: {python_exe}")
            return False

        result = subprocess.run([python_exe, "-c", "import uvicorn"], capture_output=True, timeout=5)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error checking uvicorn: {e}")
        return False


def check_node_npm_installed() -> bool:
    """Check if Node.js and npm are installed."""
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, timeout=5)
        if result.returncode != 0:
            return False

        result = subprocess.run(["npm", "--version"], capture_output=True, timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def install_nodejs_dependencies(directory: str, update: bool = False) -> bool:
    """Install Node.js dependencies in a directory."""
    dir_path = ROOT_DIR / directory
    
    if not dir_path.exists():
        logger.warning(f"Directory {directory} does not exist, skipping npm install")
        return False

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
        cmd = ["npm", "update" if update else "install"]
        result = subprocess.run(cmd, cwd=dir_path, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            logger.info(f"Node.js dependencies installed successfully in {directory}")
            return True
        else:
            logger.error(f"Failed to install Node.js dependencies in {directory}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"npm install timed out in {directory}")
        return False
    except Exception as e:
        logger.error(f"Error installing Node.js dependencies: {e}")
        return False


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


def setup_node_dependencies(service_path: Path, service_name: str) -> bool:
    """Set up Node.js dependencies for a service. Returns True if successful."""
    if not service_path.exists():
        logger.warning(f"Service path {service_path} does not exist")
        return False

    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return False

    package_json = service_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json found for {service_name}")
        return False

    node_modules = service_path / "node_modules"
    if node_modules.exists():
        logger.info(f"Dependencies already installed for {service_name}")
        return True

    logger.info(f"Installing dependencies for {service_name}...")
    try:
        result = subprocess.run(
            ["npm", "install"],
            cwd=service_path,
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            logger.info(f"Dependencies installed successfully for {service_name}")
            return True
        else:
            logger.error(f"Failed to install dependencies for {service_name}: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        logger.error(f"npm install timed out for {service_name}")
        return False
    except Exception as e:
        logger.error(f"Error installing dependencies for {service_name}: {e}")
        return False


def start_backend(host: str, port: int, debug: bool = False) -> bool:
    """Start the Python backend server. Returns True if process started successfully."""
    python_exe = get_python_executable()

    if not validate_path_safety(python_exe):
        logger.error(f"Unsafe Python executable path: {python_exe}")
        return False

    if not validate_host(host):
        logger.error(f"Invalid host parameter: {host}")
        return False

    if not validate_port(port):
        logger.error(f"Invalid port parameter: {port}")
        return False

    cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "src.main:create_app",
        "--factory",
        "--host",
        host,
        "--port",
        str(port),
    ]

    if debug:
        cmd.extend(["--reload", "--log-level", "debug"])

    logger.info(f"Starting Python backend on {host}:{port}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process_manager.add_process(process)
        logger.info(f"Python backend process started (PID: {process.pid})")
        return True
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
        return False


def start_node_service(
    service_path: Path,
    service_name: str,
    port: int,
    api_url: str
) -> bool:
    """Start a Node.js service. Returns True if process started successfully."""
    logger.info(f"Starting {service_name} on port {port}...")

    if not service_path.exists():
        logger.error(f"Service path {service_path} does not exist")
        return False

    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return False

    if not validate_port(port):
        logger.error(f"Invalid port for {service_name}: {port}")
        return False

    try:
        # Ensure dependencies are installed
        if not setup_node_dependencies(service_path, service_name):
            logger.error(f"Failed to install dependencies for {service_name}")
            return False

        # Determine npm script
        package_json_path = service_path / "package.json"
        if not package_json_path.exists():
            logger.error(f"No package.json found for {service_name}")
            return False

        with open(package_json_path, "r") as f:
            package_data = json.load(f)
            scripts = package_data.get("scripts", {})

            if "dev" in scripts:
                cmd = ["npm", "run", "dev"]
            elif "start" in scripts:
                cmd = ["npm", "start"]
            else:
                logger.warning(f"No suitable npm script found for {service_name}")
                return False

        # Setup environment
        env = os.environ.copy()
        env["PORT"] = str(port)
        env["API_URL"] = api_url  # Assume api_url is already validated

        # Start service
        process = subprocess.Popen(
            cmd,
            cwd=service_path,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process_manager.add_process(process)
        logger.info(f"{service_name} process started (PID: {process.pid})")
        return True

    except json.JSONDecodeError as e:
        logger.error(f"Invalid package.json for {service_name}: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to start {service_name}: {e}")
        return False


def start_gradio_ui(host: str, port: int, share: bool, debug: bool) -> bool:
    """Start the Gradio UI. Returns True if process started successfully."""
    python_exe = get_python_executable()

    if not validate_path_safety(python_exe):
        logger.error(f"Unsafe Python executable path: {python_exe}")
        return False

    if not validate_host(host):
        logger.error(f"Invalid host parameter: {host}")
        return False

    if not validate_port(port):
        logger.error(f"Invalid port parameter: {port}")
        return False

    cmd = [python_exe, "-m", "src.main", "--host", host, "--port", str(port)]

    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")

    logger.info(f"Starting Gradio UI on {host}:{port}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(
            cmd,
            env=env,
            cwd=ROOT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        process_manager.add_process(process)
        logger.info(f"Gradio UI process started (PID: {process.pid})")
        return True
    except Exception as e:
        logger.error(f"Failed to start Gradio UI: {e}")
        return False


def validate_services() -> Dict[str, bool]:
    """Validate which services are available and properly configured."""
    config = get_project_config()
    available_services = {}

    # Check Python backend
    python_backend_config = config.get_service_config("python_backend")
    if python_backend_config:
        backend_path = config.get_service_path("python_backend")
        main_file = backend_path / python_backend_config.get("main_file", "main.py")
        available_services["python_backend"] = backend_path.exists() and main_file.exists()

    # Check TypeScript backend
    ts_backend_config = config.get_service_config("typescript_backend")
    if ts_backend_config:
        ts_path = config.get_service_path("typescript_backend")
        package_json = ts_path / ts_backend_config.get("package_json", "package.json")
        available_services["typescript_backend"] = ts_path.exists() and package_json.exists()

    # Check frontend
    frontend_config = config.get_service_config("frontend")
    if frontend_config:
        frontend_path = config.get_service_path("frontend")
        package_json = frontend_path / frontend_config.get("package_json", "package.json")
        available_services["frontend"] = frontend_path.exists() and package_json.exists()

    return available_services


def start_services(args) -> bool:
    """Start the required services based on arguments. Returns True if all succeeded."""
    if not validate_host(args.host):
        logger.error(f"Invalid host: {args.host}")
        return False

    if not validate_port(args.port):
        logger.error(f"Invalid port: {args.port}")
        return False

    api_url = args.api_url or f"http://{args.host}:{args.port}"

    # Validate available services
    available_services = validate_services()
    logger.info(f"Available services: {available_services}")

    # Get project configuration
    config = get_project_config()
    all_started = True

    if not args.frontend_only:
        if available_services.get("python_backend", False):
            if not start_backend(args.host, args.port, args.debug):
                all_started = False
        else:
            logger.warning("Python backend not available, skipping...")

        # Start TypeScript backend if configured and available
        if available_services.get("typescript_backend", False):
            ts_backend_config = config.get_service_config("typescript_backend")
            ts_backend_path = config.get_service_path("typescript_backend")
            if not start_node_service(
                ts_backend_path,
                "TypeScript Backend",
                ts_backend_config.get("port", 8001),
                api_url
            ):
                all_started = False

    if not args.api_only:
        # Start frontend if configured and available
        if available_services.get("frontend", False):
            frontend_config = config.get_service_config("frontend")
            frontend_path = config.get_service_path("frontend")
            if not start_node_service(
                frontend_path,
                "Frontend Client",
                args.frontend_port,
                api_url
            ):
                all_started = False

    return all_started
