"""
<<<<<<< HEAD
Service management for the launch system.

This module handles starting, stopping, and managing various services
(Python backend, Node.js frontend, TypeScript backend, etc.).
=======
Service management utilities for EmailIntelligence launcher
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
"""

import logging
import os
import subprocess
<<<<<<< HEAD
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
    if not re.match(r'^[a-zA-Z0-9.-]+


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

    package_json = service_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json found for {service_name}")
        return

    node_modules = service_path / "node_modules"
    if not node_modules.exists():
        logger.info(f"Installing dependencies for {service_name}...")
        try:
            result = subprocess.run(["npm", "install"], cwd=service_path, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Dependencies installed successfully for {service_name}")
            else:
                logger.error(f"Failed to install dependencies for {service_name}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error installing dependencies for {service_name}: {e}")


def start_gradio_ui(host, port, share, debug):
    """Start the Gradio UI."""
    python_exe = get_python_executable()
    
    # Validate the python executable path to prevent command injection
    if not validate_path_safety(python_exe):
        logger.error(f"Unsafe Python executable path: {python_exe}")
        return
    
    # Sanitize host parameter to prevent command injection
    import re
    if not re.match(r'^[a-zA-Z0-9.-]+$', host):
        logger.error(f"Invalid host parameter: {host}")
        return

    cmd = [python_exe, "-m", "src.main", "--host", host, "--port", str(port)]

    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")

    logger.info(f"Starting Gradio UI on {host}:{port}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(cmd, env=env, cwd=ROOT_DIR)
        from setup.utils import process_manager
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
    api_url = args.api_url or f"http://{args.host}:{args.port}"

    # Validate available services
    available_services = validate_services()
    logger.info(f"Available services: {available_services}")

    # Get project configuration
    config = get_project_config()

    if not args.frontend_only:
        if available_services.get("python_backend", False):
            start_backend(args.host, args.port, args.debug)
        else:
            logger.warning("Python backend not available, skipping...")

        # Start TypeScript backend if configured and available
        if available_services.get("typescript_backend", False):
            ts_backend_config = config.get_service_config("typescript_backend")
            ts_backend_path = config.get_service_path("typescript_backend")
            start_node_service(ts_backend_path, "TypeScript Backend", ts_backend_config.get("port", 8001), api_url)

    if not args.api_only:
        start_gradio_ui(args.host, 7860, args.share, args.debug)

        # Start frontend if configured and available
        if available_services.get("frontend", False):
            frontend_config = config.get_service_config("frontend")
            frontend_path = config.get_service_path("frontend")
            start_node_service(frontend_path, "Frontend Client", args.frontend_port, api_url), host):
        logger.error(f"Invalid host parameter: {host}")
        return
    
=======
from pathlib import Path

logger = logging.getLogger("launcher")

# Get root directory (avoid circular import)
ROOT_DIR = Path(__file__).parent.parent

# Import process manager (will be available at runtime)
try:
    from setup.utils import process_manager
except ImportError:
    # Fallback if utils not available yet
    process_manager = None

# Import helper functions (will be available at runtime)
try:
    from setup.utils import get_python_executable
except ImportError:
    def get_python_executable():
        return "python"

try:
    from setup.launch import run_command
except ImportError:
    def run_command(cmd, description, **kwargs):
        """Fallback run_command implementation"""
        try:
            result = subprocess.run(cmd, **kwargs, capture_output=True, text=True)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Failed to run command {cmd}: {e}")
            return False


def start_services(args):
    """Starts the required services based on arguments."""
    api_url = getattr(args, 'api_url', None) or f"http://{getattr(args, 'host', 'localhost')}:{getattr(args, 'port', 8000)}"

    if not getattr(args, 'frontend_only', False):
        start_backend(getattr(args, 'host', 'localhost'), getattr(args, 'port', 8000), getattr(args, 'debug', False))
        start_node_service(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend", 8001, api_url)

    if not getattr(args, 'api_only', False):
        start_gradio_ui(getattr(args, 'host', 'localhost'), 7860, getattr(args, 'share', False), getattr(args, 'debug', False))
        start_node_service(ROOT_DIR / "client", "Frontend Client", getattr(args, 'frontend_port', 3000), api_url)


def start_backend(host: str, port: int, debug: bool = False):
    """Start the FastAPI backend server."""
    python_exe = get_python_executable()
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
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
<<<<<<< HEAD

    if debug:
        cmd.append("--reload")
        cmd.append("--log-level")
        cmd.append("debug")

    logger.info(f"Starting Python backend on {host}:{port}")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    try:
        process = subprocess.Popen(cmd, env=env, cwd=ROOT_DIR)
        from setup.utils import process_manager
        process_manager.add_process(process)
    except Exception as e:
        logger.error(f"Failed to start backend: {e}")
=======
    if debug:
        cmd.append("--reload")
    logger.info(f"Starting backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    if process_manager:
        process_manager.add_process(process)
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613


def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
    """Start a Node.js service."""
<<<<<<< HEAD
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

    package_json = service_path / "package.json"
    if not package_json.exists():
        logger.warning(f"No package.json found for {service_name}")
        return

    node_modules = service_path / "node_modules"
    if not node_modules.exists():
        logger.info(f"Installing dependencies for {service_name}...")
        try:
            result = subprocess.run(["npm", "install"], cwd=service_path, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"Dependencies installed successfully for {service_name}")
            else:
                logger.error(f"Failed to install dependencies for {service_name}: {result.stderr}")
        except Exception as e:
            logger.error(f"Error installing dependencies for {service_name}: {e}")





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
    api_url = args.api_url or f"http://{args.host}:{args.port}"

    # Validate available services
    available_services = validate_services()
    logger.info(f"Available services: {available_services}")

    # Get project configuration
    config = get_project_config()

    if not args.frontend_only:
        if available_services.get("python_backend", False):
            start_backend(args.host, args.port, args.debug)
        else:
            logger.warning("Python backend not available, skipping...")

        # Start TypeScript backend if configured and available
        if available_services.get("typescript_backend", False):
            ts_backend_config = config.get_service_config("typescript_backend")
            ts_backend_path = config.get_service_path("typescript_backend")
            start_node_service(ts_backend_path, "TypeScript Backend", ts_backend_config.get("port", 8001), api_url)

    if not args.api_only:
        start_gradio_ui(args.host, 7860, args.share, args.debug)

        # Start frontend if configured and available
        if available_services.get("frontend", False):
            frontend_config = config.get_service_config("frontend")
            frontend_path = config.get_service_path("frontend")
            start_node_service(frontend_path, "Frontend Client", args.frontend_port, api_url)
=======
    if not service_path.exists():
        logger.warning(f"{service_name} path not found at {service_path}, skipping.")
        return
    logger.info(f"Starting {service_name} on port {port}...")
    env = os.environ.copy()
    env["PORT"] = str(port)
    env["VITE_API_URL"] = api_url
    process = subprocess.Popen(["npm", "start"], cwd=service_path, env=env)
    if process_manager:
        process_manager.add_process(process)


def start_gradio_ui(host, port, share, debug):
    """Start the Gradio UI."""
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [python_exe, "-m", "src.main"]  # Assuming Gradio is launched from main
    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    process = subprocess.Popen(cmd, cwd=ROOT_DIR, env=env)
    if process_manager:
        process_manager.add_process(process)


def validate_services():
    """Validate that all required services can start."""
    # Basic validation - check if required directories exist
    required_services = [
        ("backend", ROOT_DIR / "src"),
        ("client", ROOT_DIR / "client"),
        ("server-ts", ROOT_DIR / "backend" / "server-ts"),
    ]

    for service_name, service_path in required_services:
        if not service_path.exists():
            logger.warning(f"Service {service_name} directory not found at {service_path}")
        else:
            logger.info(f"Service {service_name} directory found")

    return True
>>>>>>> a7da61cf1f697de3c8c81f536bf579d36d88e613
