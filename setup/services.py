"""
Service management utilities for EmailIntelligence launcher
"""

import logging
import os
import subprocess
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
    logger.info(f"Starting backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    if process_manager:
        process_manager.add_process(process)


def start_node_service(service_path: Path, service_name: str, port: int, api_url: str):
    """Start a Node.js service."""
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