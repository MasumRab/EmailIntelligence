"""
Service management for the launch system.

This module handles starting, stopping, and managing various services
(Python backend, Node.js frontend, TypeScript backend, etc.).
"""

import logging
import os
import subprocess
import sys
import re
from pathlib import Path
from typing import Dict, List, Optional

from setup.project_config import get_project_config
from src.core.security import validate_path_safety

logger = logging.getLogger(__name__)

# Global paths
ROOT_DIR = Path(__file__).resolve().parent.parent

def get_python_executable() -> str:
    """Get the appropriate Python executable."""
    from setup.environment import get_python_executable as env_get_python
    return env_get_python()

def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    try:
        python_exe = get_python_executable()
        if not validate_path_safety(python_exe):
            logger.error(f"Unsafe Python executable path: {python_exe}")
            return False

        result = subprocess.run([python_exe, "-m", "uvicorn", "--version"], capture_output=True)
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

    if not validate_path_safety(str(dir_path), str(ROOT_DIR)):
        logger.error(f"Unsafe directory path: {dir_path}")
        return False

    package_json = dir_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json in {directory}, skipping npm install")
        return False

    logger.info(f"Installing Node.js dependencies in {directory}...")
    try:
        cmd = ["npm", "update" if update else "install"]
        # Use shell=True on Windows for npm
        use_shell = platform.system() == "Windows"
        result = subprocess.run(cmd, cwd=dir_path, capture_output=True, text=True, shell=use_shell)
        if result.returncode == 0:
            logger.info(f"Node.js dependencies installed successfully in {directory}")
            return True
        else:
            logger.error(f"Failed to install Node.js dependencies in {directory}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error installing Node.js dependencies: {e}")
        return False

import platform

def start_backend(host: str, port: int, debug: bool = False):
    """Start the Python backend server."""
    python_exe = get_python_executable()

    if not validate_path_safety(python_exe):
        logger.error(f"Unsafe Python executable path: {python_exe}")
        return

    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        logger.error(f"Invalid host parameter: {host}")
        return

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
        cmd.append("--reload")

    logger.info(f"Starting Python backend on {host}:{port}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(cmd, env=env, cwd=ROOT_DIR)
        from setup.utils import process_manager
        if process_manager:
            process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")

def setup_node_dependencies(service_path: Path, service_name: str):
    """Set up Node.js dependencies for a service."""
    if not service_path.exists():
        logger.warning(f"Service path {service_path} does not exist")
        return
    
    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return
        
    package_json = service_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json found for {service_name}")
        return
        
    node_modules = service_path / "node_modules"
    if not node_modules.exists():
        logger.info(f"Installing dependencies for {service_name}...")
        try:
            use_shell = platform.system() == "Windows"
            result = subprocess.run(["npm", "install"], cwd=service_path, capture_output=True, text=True, shell=use_shell)
            if result.returncode == 0:
                logger.info(f"Dependencies installed successfully for {service_name}")
            else:
                logger.error(f"Failed to install dependencies for {service_name}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error installing dependencies for {service_name}: {e}")

def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
    """Start a Node.js service."""
    logger.info(f"Starting {service_name} on port {port}...")

    if not service_path.exists():
        logger.error(f"Service path {service_path} does not exist")
        return

    if not validate_path_safety(str(service_path), str(ROOT_DIR)):
        logger.error(f"Unsafe service path: {service_path}")
        return

    try:
        setup_node_dependencies(service_path, service_name)

        env = os.environ.copy()
        env["PORT"] = str(port)
        env["VITE_API_URL"] = api_url

        # Check if it's a dev script or start script
        cmd = ["npm", "start"]
        package_json_path = service_path / "package.json"
        if package_json_path.exists():
            import json
            with open(package_json_path, "r") as f:
                package_data = json.load(f)
                if "dev" in package_data.get("scripts", {}):
                    cmd = ["npm", "run", "dev"]

        use_shell = platform.system() == "Windows"
        process = subprocess.Popen(cmd, cwd=service_path, env=env, shell=use_shell)
        from setup.utils import process_manager
        if process_manager:
            process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start {service_name}: {e}")

def start_gradio_ui(host: str, port: int, share: bool = False, debug: bool = False):
    """Start the Gradio UI."""
    logger.info(f"Starting Gradio UI on {host}:{port}...")
    python_exe = get_python_executable()
    
    cmd = [python_exe, "-m", "src.main"]
    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")
        
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    
    try:
        process = subprocess.Popen(cmd, cwd=ROOT_DIR, env=env)
        from setup.utils import process_manager
        if process_manager:
            process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start Gradio UI: {e}")

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

def start_services(args):
    """Start the required services based on arguments."""
    api_url = getattr(args, "api_url", None) or f"http://{args.host}:{args.port}"

    available_services = validate_services()
    logger.info(f"Available services: {available_services}")

    config = get_project_config()

    if not getattr(args, "frontend_only", False):
        if available_services.get("python_backend", False):
            start_backend(args.host, args.port, args.debug)
        else:
            logger.warning("Python backend not available, skipping...")

        if available_services.get("typescript_backend", False):
            ts_backend_config = config.get_service_config("typescript_backend")
            ts_backend_path = config.get_service_path("typescript_backend")
            start_node_service(ts_backend_path, "TypeScript Backend", ts_backend_config.get("port", 8001), api_url)

    if not getattr(args, "api_only", False):
        start_gradio_ui(args.host, 7860, getattr(args, "share", False), args.debug)

        if available_services.get("frontend", False):
            frontend_path = config.get_service_path("frontend")
            start_node_service(frontend_path, "Frontend Client", getattr(args, "frontend_port", 5173), api_url)
