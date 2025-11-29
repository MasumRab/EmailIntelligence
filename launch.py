#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script is a wrapper that forwards to the actual launch.py in the setup subtree.
It maintains backward compatibility for references to launch.py in the root directory.
"""

import subprocess
import sys
<<<<<<< ours
import os
=======
import time
import venv
from pathlib import Path
from typing import List, Optional

from deployment.test_stages import test_stages

try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")


# --- Global state ---
def find_project_root() -> Path:
    """Find the project root directory by looking for key files."""
    current = Path(__file__).resolve().parent
    if (current / "pyproject.toml").exists():
        return current
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    return current


ROOT_DIR = find_project_root()

class ProcessManager:
    """Manages child processes for the application."""
    def __init__(self):
        self.processes = []
    def add_process(self, process):
        self.processes.append(process)
    def cleanup(self):
        logger.info("Performing explicit resource cleanup...")
        for p in self.processes[:]:
            if p.poll() is None:
                logger.info(f"Terminating process {p.pid}...")
                p.terminate()
                try:
                    p.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Process {p.pid} did not terminate gracefully, killing.")
                    p.kill()
        logger.info("Resource cleanup completed.")
    def shutdown(self):
        logger.info("Received shutdown signal, cleaning up processes...")
        self.cleanup()
        sys.exit(0)

process_manager = ProcessManager()
atexit.register(process_manager.cleanup)

# --- Constants ---
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")

# --- Python Version Checking ---
def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(f"Python version {platform.python_version()} is not compatible.")
        sys.exit(1)
    logger.info(f"Python version {platform.python_version()} is compatible.")

# --- Environment Validation ---
def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflict markers in critical files."""
    conflict_markers = ["<<<<<<< ", "======= ", ">>>>>>> "]
    critical_files = [
        "backend/python_backend/main.py",
        "backend/python_nlp/nlp_engine.py",
        "backend/python_backend/database.py",
        "backend/python_backend/email_routes.py",
        "backend/python_backend/category_routes.py",
        "backend/python_backend/gmail_routes.py",
        "backend/python_backend/filter_routes.py",
        "backend/python_backend/action_routes.py",
        "backend/python_backend/dashboard_routes.py",
        "backend/python_backend/workflow_routes.py",
        "backend/python_backend/performance_monitor.py",
        "backend/python_nlp/gmail_integration.py",
        "backend/python_nlp/gmail_service.py",
        "backend/python_nlp/smart_filters.py",
        "backend/python_nlp/smart_retrieval.py",
        "backend/python_nlp/ai_training.py",
        "README.md",
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
    ]

    conflicts_found = False
    for file_path in critical_files:
        full_path = ROOT_DIR / file_path
        if full_path.exists():
            try:
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    for marker in conflict_markers:
                        if marker in content:
                            logger.error(
                                f"Unresolved merge conflict detected in {file_path} with marker: {marker.strip()}"
                            )
                            conflicts_found = True
            except Exception as e:
                logger.warning(f"Could not check {file_path} for conflicts: {e}")

    if conflicts_found:
        logger.error("Please resolve all merge conflicts before proceeding.")
        return False

    logger.info("No unresolved merge conflicts detected in critical files.")
    return True


def check_required_components() -> bool:
    """Check for required components and configurations."""
    issues = []

    # Check Python version
    current_version = sys.version_info[:2]
    if not ((3, 11) <= current_version <= (3, 13)):
        issues.append(f"Python version {current_version} is not compatible. Required: 3.11-3.13")

    # Check key directories
    required_dirs = ["backend", "client", "shared", "tests"]
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    # Check key files
    required_files = ["pyproject.toml", "README.md", "requirements.txt"]
    for file_name in required_files:
        if not (ROOT_DIR / file_name).exists():
            issues.append(f"Required file '{file_name}' is missing.")

    # Check AI models directory
    models_dir = ROOT_DIR / "models"
    if not models_dir.exists():
        logger.warning("AI models directory not found. Creating it...")
        try:
            models_dir.mkdir(parents=True, exist_ok=True)
            logger.info("AI models directory created successfully.")
        except Exception as e:
            logger.error(f"Failed to create models directory: {e}")
            issues.append("Failed to create models directory")

    if issues:
        for issue in issues:
            logger.error(issue)
        return False

    logger.info("All required components are present.")
    return True


def validate_environment() -> bool:
    """Run comprehensive environment validation."""
    logger.info("Running environment validation...")

    if not check_for_merge_conflicts():
        return False

    if not check_required_components():
        return False

    logger.info("Environment validation passed.")
    return True


# --- Input Validation ---
def validate_port(port: int) -> int:
    """Validate port number is within valid range."""
    if not 1 <= port <= 65535:
        raise ValueError(f"Invalid port: {port}. Port must be between 1 and 65535.")
    return port


def validate_host(host: str) -> str:
    """Validate host name/address format."""
    import re

    if not re.match(r"^[a-zA-Z0-9.-]+$", host):
        raise ValueError(f"Invalid host: {host}")
    return host


# --- Conda Environment Support ---
def is_conda_available() -> bool:
    """Check if conda is available on the system."""
    try:
        result = subprocess.run(
            ["conda", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_conda_env_info():
    """Get information about the current conda environment."""
    env_vars = os.environ
    conda_default_env = env_vars.get("CONDA_DEFAULT_ENV")
    conda_prefix = env_vars.get("CONDA_PREFIX")

    return {
        "is_active": conda_default_env is not None,
        "env_name": conda_default_env,
        "prefix": conda_prefix,
        "python_exe": env_vars.get("CONDA_PREFIX", "") + "/python" if conda_prefix else None
    }


def activate_conda_env(env_name: str = None) -> bool:
    """Activate a conda environment."""
    env_name = env_name or CONDA_ENV_NAME

    # Validate environment name to prevent command injection
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', env_name):
        logger.error(f"Invalid conda environment name: {env_name}. Only alphanumeric characters, hyphens, and underscores are allowed.")
        return False

    if not is_conda_available():
        logger.debug("Conda not available, skipping environment activation.")
        return False

    conda_info = get_conda_env_info()
    if conda_info["is_active"]:
        logger.info(f"Already in conda environment: {conda_info['env_name']}")
        return True

    try:
        # Try to activate the specified environment
        logger.info(f"Activating conda environment: {env_name}")
        result = subprocess.run(
            ["conda", "activate", env_name],
            shell=True,  # shell=True is needed for conda activate
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Successfully activated conda environment: {env_name}")
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"Failed to activate conda environment {env_name}: {e}")
        return False


def get_python_executable() -> str:
    """Get the appropriate Python executable (conda > venv > system)."""
    # Check if we're in a conda environment
    conda_info = get_conda_env_info()
    if conda_info["is_active"] and conda_info["python_exe"]:
        python_exe = conda_info["python_exe"]
        if platform.system() == "Windows":
            python_exe += ".exe"
        if os.path.exists(python_exe):
            logger.info(f"Using conda Python: {python_exe}")
            return python_exe

    # Check for venv
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            logger.info(f"Using venv Python: {python_exe}")
            return str(python_exe)

    # Fall back to system Python
    logger.info("Using system Python")
    return sys.executable

# --- Helper Functions ---
def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    scripts_dir = "Scripts" if platform.system() == "Windows" else "bin"
    return venv_path / scripts_dir / (f"{executable}.exe" if platform.system() == "Windows" else executable)

def run_command(cmd: List[str], description: str, **kwargs) -> bool:
    """Run a command and log its output."""
    logger.info(f"{description}...")
    try:
        proc = subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)
        if proc.stdout:
            logger.debug(proc.stdout)
        if proc.stderr:
            logger.warning(proc.stderr)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logger.error(f"Failed: {description}")
        if isinstance(e, subprocess.CalledProcessError):
            logger.error(f"Stderr: {e.stderr}")
        return False

# --- Setup Functions ---
def create_venv(venv_path: Path, recreate: bool = False):
    if venv_path.exists() and recreate:
        logger.info("Removing existing virtual environment.")
        shutil.rmtree(venv_path)
    if not venv_path.exists():
        logger.info("Creating virtual environment.")
        venv.create(venv_path, with_pip=True, upgrade_deps=True)

def install_package_manager(venv_path: Path, manager: str):
    python_exe = get_venv_executable(venv_path, "python")
    run_command([str(python_exe), "-m", "pip", "install", manager], f"Installing {manager}")

def setup_dependencies(venv_path: Path, use_poetry: bool = False):
    python_exe = get_python_executable()

    if use_poetry:
        # For poetry, we need to install it first if not available
        try:
            subprocess.run([python_exe, "-c", "import poetry"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "poetry"], "Installing Poetry")

        run_command([python_exe, "-m", "poetry", "install", "--with", "dev"], "Installing dependencies with Poetry", cwd=ROOT_DIR)
    else:
        # For uv, install if not available
        try:
            subprocess.run([python_exe, "-c", "import uv"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([python_exe, "-m", "pip", "install", "uv"], "Installing uv")

        run_command([python_exe, "-m", "uv", "pip", "install", "-e", ".[dev]"], "Installing dependencies with uv", cwd=ROOT_DIR)

def download_nltk_data(venv_path=None):
    python_exe = get_python_executable()

    nltk_download_script = """
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('omw-1.4')
print("NLTK data download completed.")
"""

    logger.info("Downloading NLTK data...")
    result = subprocess.run(
        [python_exe, "-c", nltk_download_script], cwd=ROOT_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to download NLTK data: {result.stderr}")
        # This might fail in some environments but it's not critical for basic operation
        logger.warning("NLTK data download failed, but continuing setup...")
    else:
        logger.info("NLTK data downloaded successfully.")

    # Download TextBlob corpora
    run_command([python_exe, "-m", "textblob.download_corpora"], "Downloading TextBlob corpora")


def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    python_exe = get_python_executable()
    try:
        result = subprocess.run(
            [python_exe, "-c", "import uvicorn"], capture_output=True, text=True
        )
        if result.returncode == 0:
            logger.info("uvicorn is available.")
            return True
        else:
            logger.error("uvicorn is not installed.")
            return False
    except FileNotFoundError:
        logger.error("Python executable not found.")
        return False


def check_node_npm_installed() -> bool:
    """Check if Node.js and npm are installed and available."""
    if not shutil.which("node"):
        logger.error("Node.js is not installed. Please install it to continue.")
        return False
    if not shutil.which("npm"):
        logger.error("npm is not installed. Please install it to continue.")
        return False
    return True


def install_nodejs_dependencies(directory: str, update: bool = False) -> bool:
    """Install Node.js dependencies in a given directory."""
    pkg_json_path = ROOT_DIR / directory / "package.json"
    if not pkg_json_path.exists():
        logger.debug(f"No package.json in '{directory}/', skipping npm install.")
        return True

    if not check_node_npm_installed():
        return False

    cmd = ["npm", "update" if update else "install"]
    desc = f"{'Updating' if update else 'Installing'} Node.js dependencies for '{directory}/'"
    return run_command(cmd, desc, cwd=ROOT_DIR / directory, shell=(os.name == "nt"))


def start_backend(host: str, port: int, debug: bool = False):
    """Start the Python FastAPI backend."""
    if not check_uvicorn_installed():
        logger.error(
            "Cannot start backend without uvicorn. Please run 'python launch.py --setup' first."
        )
        return None

    python_exe = get_python_executable()

    # Use uvicorn to run the FastAPI app directly
    cmd = [
        python_exe,
        "-m",
        "uvicorn",
        "backend.python_backend.main:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if debug:
        cmd.append("--reload")  # Enable auto-reload in debug mode

    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)

    logger.info(f"Starting Python backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR, env=env)
    process_manager.add_process(process)
    return process


def start_gradio_ui(
    venv_path: Path, host: str, port: Optional[int] = None, debug: bool = False, share: bool = False
):
    """Start the Gradio UI."""
    gradio_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"

    cmd = [str(venv_python), str(gradio_path), "--host", host]
    if port:
        cmd.extend(["--port", str(port)])
        logger.info(f"Starting Gradio UI on {host}:{port}")
    else:
        logger.info(f"Starting Gradio UI on {host}:7860 (default port)")

    if share:
        cmd.append("--share")  # Enable public sharing
    if port:
        # Gradio doesn't take port as a command line param directly,
        # we'd need to modify the app to accept it
        logger.info(f"Starting Gradio UI (on default or next available port)")
    else:
        logger.info("Starting Gradio UI on default port")

    logger.info("Starting Gradio UI...")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    process_manager.add_process(process)
    return process


def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    if not install_nodejs_dependencies("client"):
        return None

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "client" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing Node.js dependencies...")


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.warning("npm not found. Skipping TypeScript backend server startup.")
        return None

    # Check if package.json exists
    pkg_json_path = ROOT_DIR / "server" / "package.json"
    if not pkg_json_path.exists():
        logger.debug("No package.json in 'server/', skipping TypeScript backend server startup.")
        return None
>>>>>>> theirs

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the actual launch.py in the setup subtree
setup_launch_path = os.path.join(script_dir, 'setup', 'launch.py')

if __name__ == "__main__":
    # Forward all arguments to the actual launch.py in the setup directory
    # Add the script directory to Python path so imports work
    env = os.environ.copy()
    python_path = env.get('PYTHONPATH', '')
    if python_path:
        env['PYTHONPATH'] = f"{script_dir}:{python_path}"
    else:
        env['PYTHONPATH'] = script_dir

    cmd = [sys.executable, setup_launch_path] + sys.argv[1:]
    result = subprocess.run(cmd, env=env)
    sys.exit(result.returncode)