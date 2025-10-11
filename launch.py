#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

This script provides a single, unified way to set up, manage, and run all
components of the EmailIntelligence application, including the Python backend,
Gradio UI, and Node.js services. It uses 'uv' for Python dependency management
based on pyproject.toml.

Usage:
    python launch.py [arguments]
"""

import argparse
import logging
import os
import platform
import shutil
import signal
import subprocess
import sys
import time
import venv
from pathlib import Path
from typing import List, Optional

# Import dotenv for environment file loading
try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None  # Will be loaded later if needed

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# --- Global state ---
processes = []
ROOT_DIR = Path(__file__).resolve().parent

# --- Constants ---
PYTHON_MIN_VERSION = (3, 11)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"

# Dependency configuration
TORCH_VERSION = "torch>=2.4.0"
TORCH_CPU_URL = "https://download.pytorch.org/whl/cpu"


def run_command(
    cmd: List[str], description: str, cwd: Optional[Path] = None, shell: bool = False
) -> bool:
    """Run a command and log its output.

    SECURITY NOTE: Use shell=False whenever possible to prevent shell injection.
    The shell parameter is maintained for backward compatibility but should be used cautiously.
    """
    if shell:
        logger.warning(
            f"Using shell=True for command: {' '.join(cmd)}. This may be a security risk."
        )

    logger.info(f"{description}...")
    try:
        # Use sys.executable for Python commands to ensure we're using the correct Python
        if cmd[0] == "python":
            cmd[0] = sys.executable

        proc = subprocess.run(
            cmd, cwd=cwd or ROOT_DIR, shell=shell, capture_output=True, text=True, check=True
        )
        # Always log stdout for visibility, especially for debugging setup steps.
        if proc.stdout:
            logger.debug(f"stdout from '{' '.join(cmd)}':\n{proc.stdout}")
        if proc.stderr:
            logger.warning(f"stderr from '{' '.join(cmd)}':\n{proc.stderr}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed: {description}")
        logger.error(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else str(cmd)}")
        logger.error(f"stdout:\n{e.stdout}")
        logger.error(f"stderr:\n{e.stderr}")
        return False
    except FileNotFoundError:
        logger.error(f"Command not found: {cmd[0] if cmd else 'Unknown command'}")
        return False


# --- Python Version Checking ---
def check_python_version():
    """Check if the current Python version is compatible and re-execute if necessary."""
    current_major, current_minor = sys.version_info[:2]
    current_version = (current_major, current_minor)
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.info(
            f"Current Python is {current_major}.{current_minor}. "
            f"Launcher requires Python {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]} to {PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}. Attempting to find and re-execute."
        )

        candidate_interpreters = []
        if platform.system() == "Windows":
            candidate_interpreters = [
                ["py", "-3.12"],  # Python Launcher for Windows
                ["py", "-3.11"],  # Python Launcher for Windows
                ["python3.12"],
                ["python3.11"],
                ["python"],  # General python, check version
            ]
        else:  # Linux/macOS
            candidate_interpreters = [
                ["python3.12"],
                ["python3.11"],
                ["python3"],  # General python3, check version
            ]

        for exe_name in candidate_interpreters:
            try:
                result = subprocess.run(
                    exe_name + ["--version"], capture_output=True, text=True, timeout=10
                )
                # Python version can be in stdout or stderr
                version_output = result.stdout.strip() + result.stderr.strip()

                # Check if version is in supported range
                compatible = False
                for major in range(PYTHON_MIN_VERSION[0], PYTHON_MAX_VERSION[0] + 1):
                    for minor in range(
                        PYTHON_MIN_VERSION[1] if major == PYTHON_MIN_VERSION[0] else 0,
                        PYTHON_MAX_VERSION[1] + 1 if major == PYTHON_MAX_VERSION[0] else 100,
                    ):
                        if f"Python {major}.{minor}" in version_output:
                            logger.info(
                                f"Found compatible Python {major}.{minor} interpreter: {exe_name} (version output: {version_output})"
                            )
                            # Re-execute with the found interpreter
                            os.execv(exe_name[0], exe_name + sys.argv)
                            compatible = True
                            break
                    if compatible:
                        break

                if compatible:
                    break
                else:
                    logger.debug(
                        f"Candidate {exe_name} is not in supported Python version range. Output: {version_output}"
                    )
            except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
                continue

        logger.error("No compatible Python interpreter found. Please install Python 3.12 or 3.11.")
        sys.exit(1)


def _install_pytorch(venv_python: Path):
    """Install PyTorch with CPU support, with fallback options."""
    # SECURITY NOTE: Using hardcoded PyTorch URL - ensure this source is trusted
    logger.info("Installing CPU-only PyTorch...")
    pytorch_cmd = [
        str(venv_python),
        "-m",
        "pip",
        "install",
        TORCH_VERSION,
        "--index-url",
        TORCH_CPU_URL,
    ]
    if not run_command(pytorch_cmd, "Install PyTorch CPU"):
        logger.warning("PyTorch installation failed, attempting fallback...")
        # Try without index URL
        fallback_cmd = [str(venv_python), "-m", "pip", "install", TORCH_VERSION]
        if not run_command(fallback_cmd, "Install PyTorch fallback"):
            logger.error("PyTorch installation completely failed, ML features may not work")


def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    if platform.system() == "Windows":
        return venv_path / "Scripts" / f"{executable}.exe"
    else:
        return venv_path / "bin" / executable


def get_venv_python_path(venv_path: Path = None) -> Path:
    """Get the path to the Python executable in the virtual environment."""
    venv_path = venv_path or (ROOT_DIR / VENV_DIR)
    return get_venv_executable(venv_path, "python")


def create_venv(venv_path: Path, recreate: bool = False):
    """Create or recreate the virtual environment."""
    if venv_path.exists() and recreate:
        logger.info(f"Removing existing virtual environment at {venv_path}")
        shutil.rmtree(venv_path)

    if not venv_path.exists():
        logger.info(f"Creating virtual environment at {venv_path}")
        venv.create(venv_path, with_pip=True)
    else:
        logger.info(f"Virtual environment already exists at {venv_path}")


def _install_package_manager(venv_path: Path, package_manager: str) -> bool:
    """Install a package manager in the virtual environment."""
    venv_python = get_venv_executable(venv_path, "python")
    if not venv_python.exists():
        logger.error(f"Python executable not found at {venv_python}")
        return False

    logger.info(f"Installing {package_manager} package manager...")
    result = subprocess.run(
        [str(venv_python), "-m", "pip", "install", package_manager],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        logger.error(f"Failed to install {package_manager}: {result.stderr}")
        return False
    logger.info(f"{package_manager} installed successfully.")
    return True


def install_uv(venv_path: Path):
    """Install uv package manager in the virtual environment."""
    if not _install_package_manager(venv_path, "uv"):
        sys.exit(1)


def setup_dependencies(venv_path: Path, update: bool = False, use_poetry: bool = False):
    """Install project dependencies using uv or Poetry."""
    venv_python = get_venv_executable(venv_path, "python")

    if use_poetry:
        venv_poetry = get_venv_executable(venv_path, "poetry")

        # Install CPU-only PyTorch first for Poetry
        _install_pytorch(venv_python)

        # Configure Poetry to use the virtual environment
        env_use_cmd = [str(venv_poetry), "env", "use", str(venv_python)]
        logger.info("Configuring Poetry to use the virtual environment...")
        env_use_result = subprocess.run(env_use_cmd, cwd=ROOT_DIR, capture_output=True, text=True)
        if env_use_result.returncode != 0:
            logger.error(f"Failed to configure Poetry venv: {env_use_result.stderr}")
            sys.exit(1)

        cmd = [str(venv_poetry), "install"]
        if not update:
            cmd.extend(["--with", "dev"])

        logger.info("Installing project dependencies with Poetry...")
        result = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Failed to install dependencies with Poetry: {result.stderr}")
            logger.error(f"stdout: {result.stdout}")
            sys.exit(1)
        logger.info("Dependencies installed successfully with Poetry.")

        # Verify critical packages are installed
        logger.info("Verifying critical package installations...")
        critical_packages = [
            "uvicorn",
            "fastapi",
            "numpy",
            "transformers",
            "nltk",
            "psutil",
            "gradio",
        ]
        missing_packages = []
        for package in critical_packages:
            try:
                venv_python = get_venv_python_path()
                check_result = subprocess.run(
                    [str(venv_python), "-c", f"import {package}"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if check_result.returncode != 0:
                    missing_packages.append(package)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_packages.append(package)

        if missing_packages:
            logger.warning(f"Some packages may not be installed: {missing_packages}")
            logger.info("Attempting to install missing packages individually...")
            for package in missing_packages:
                install_cmd = [str(venv_python), "-m", "pip", "install", package]
                if package == "uvicorn":
                    install_cmd = [str(venv_python), "-m", "pip", "install", "uvicorn[standard]"]
                if run_command(install_cmd, f"Install {package}"):
                    logger.info(f"Successfully installed {package}")
                else:
                    logger.error(f"Failed to install {package}")
        else:
            logger.info("All critical packages verified successfully.")
    else:
        # Install CPU-only PyTorch first for uv
        _install_pytorch(venv_python)

        venv_uv = get_venv_executable(venv_path, "uv")

        # Configure uv to use the virtual environment
        os.environ['UV_PROJECT_ENVIRONMENT'] = str(venv_path)

        cmd = [str(venv_uv), "sync"]
        if update:
            cmd.extend(["--upgrade"])

        logger.info("Installing project dependencies with uv...")
        result = subprocess.run(cmd, cwd=ROOT_DIR, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Failed to install dependencies with uv: {result.stderr}")
            logger.error(f"stdout: {result.stdout}")
            sys.exit(1)
        logger.info("Dependencies installed successfully with uv.")

        # Verify critical packages are installed
        logger.info("Verifying critical package installations...")
        critical_packages = [
            "uvicorn",
            "fastapi",
            "numpy",
            "transformers",
            "nltk",
            "psutil",
            "gradio",
        ]
        missing_packages = []
        for package in critical_packages:
            try:
                venv_python = get_venv_python_path()
                check_result = subprocess.run(
                    [str(venv_python), "-c", f"import {package}"],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )
                if check_result.returncode != 0:
                    missing_packages.append(package)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                missing_packages.append(package)

        if missing_packages:
            logger.warning(f"Some packages may not be installed: {missing_packages}")
            logger.info("Attempting to install missing packages individually...")
            for package in missing_packages:
                install_cmd = [str(venv_python), "-m", "pip", "install", package]
                if package == "uvicorn":
                    install_cmd = [str(venv_python), "-m", "pip", "install", "uvicorn[standard]"]
                if run_command(install_cmd, f"Install {package}"):
                    logger.info(f"Successfully installed {package}")
                else:
                    logger.error(f"Failed to install {package}")
        else:
            logger.info("All critical packages verified successfully.")


def download_nltk_data(venv_path: Path):
    """Download required NLTK data."""
    venv_python = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )

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
        [str(venv_python), "-c", nltk_download_script], cwd=ROOT_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to download NLTK data: {result.stderr}")
        # This might fail in some environments but it's not critical for basic operation
        logger.warning("NLTK data download failed, but continuing setup...")
    else:
        logger.info("NLTK data downloaded successfully.")


def start_backend(venv_path: Path, host: str, port: int, debug: bool = False):
    """Start the Python FastAPI backend."""
    venv_python = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )

    # Use uvicorn to run the FastAPI app directly
    cmd = [
        str(venv_python),
        "-m",
        "uvicorn",
        "backend.python_backend.main:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if debug:
        cmd.append("--reload")

    logger.info(f"Starting Python backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def start_gradio_ui(
    venv_path: Path, host: str, port: Optional[int] = None, debug: bool = False, share: bool = False
):
    """Start the Gradio UI."""
    venv_python = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )
    gradio_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"

    cmd = [str(venv_python), str(gradio_path)]
    if share:
        cmd.append("--share")  # Enable public sharing
    if port:
        # Gradio doesn't take port as a command line param directly,
        # we'd need to modify the app to accept it
        logger.info(f"Starting Gradio UI (on default or next available port)")
    else:
        logger.info("Starting Gradio UI on default port")

    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.error("npm is not available in PATH. Please install Node.js.")
        sys.exit(1)

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "client" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing Node.js dependencies...")
        result = subprocess.run(
            ["npm", "install"], cwd=ROOT_DIR / "client", capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to install Node.js dependencies: {result.stderr}")
            sys.exit(1)
        logger.info("Node.js dependencies installed.")

    # Start the React frontend
    process = subprocess.Popen(["npm", "run", "dev"], cwd=ROOT_DIR / "client", shell=True)
    processes.append(process)
    return process


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    # Check if npm is available
    if not shutil.which("npm"):
        logger.error("npm is not available in PATH. Please install Node.js.")
        sys.exit(1)

    # Install Node.js dependencies if node_modules doesn't exist
    node_modules_path = ROOT_DIR / "server" / "node_modules"
    if not node_modules_path.exists():
        logger.info("Installing TypeScript server dependencies...")
        result = subprocess.run(
            ["npm", "install"], cwd=ROOT_DIR / "server", capture_output=True, text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to install TypeScript server dependencies: {result.stderr}")
            sys.exit(1)
        logger.info("TypeScript server dependencies installed.")

    # Start the TypeScript backend
    process = subprocess.Popen(["npm", "run", "dev"], cwd=ROOT_DIR / "server")
    processes.append(process)
    return process


def start_backend(venv_path: Path, host: str, port: int, debug: bool = False):
    """Start the Python FastAPI backend."""
    venv_python = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )

    # Use uvicorn to run the FastAPI app directly
    cmd = [
        str(venv_python),
        "-m",
        "uvicorn",
        "backend.python_backend.main:app",
        "--host",
        host,
        "--port",
        str(port),
    ]
    if debug:
        cmd.append("--reload")

    logger.info(f"Starting Python backend on {host}:{port}")
    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def start_gradio_ui(
    venv_path: Path, host: str, port: Optional[int] = None, debug: bool = False, share: bool = False
):
    """Start the Gradio UI."""
    venv_python = (
        venv_path / "Scripts" / "python.exe"
        if platform.system() == "Windows"
        else venv_path / "bin" / "python"
    )
    gradio_path = ROOT_DIR / "backend" / "python_backend" / "gradio_app.py"

    cmd = [str(venv_python), str(gradio_path)]
    if share:
        cmd.append("--share")  # Enable public sharing
    if port:
        # Gradio doesn't take port as a command line param directly,
        # we'd need to modify the app to accept it
        logger.info(f"Starting Gradio UI (on default or next available port)")
    else:
        logger.info("Starting Gradio UI on default port")

    process = subprocess.Popen(cmd, cwd=ROOT_DIR)
    processes.append(process)
    return process


def wait_for_processes():
    """Wait for all processes to complete."""
    try:
        while True:
            time.sleep(1)
            # Check if any process has terminated unexpectedly
            for i, process in enumerate(processes[:]):
                if process.poll() is not None:
                    logger.warning(
                        f"Process {process.pid} terminated with code {process.returncode}"
                    )
                    processes.remove(process)
    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
        _handle_sigint(None, None)


def main():
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher")

    # Setup arguments
    parser.add_argument("--setup", action="store_true", help="Run environment setup and exit.")
    parser.add_argument("--update-deps", action="store_true", help="Update all dependencies.")
    parser.add_argument(
        "--no-venv", action="store_true", help="Do not create or use a Python venv."
    )
    parser.add_argument(
        "--force-recreate-venv",
        action="store_true",
        help="Delete and recreate the venv before setup.",
    )
    parser.add_argument(
        "--no-download-nltk", action="store_true", help="Skip downloading NLTK data."
    )

    # Service selection
    parser.add_argument(
        "--no-backend", action="store_true", help="Do not start the Python backend."
    )
    parser.add_argument("--no-ui", action="store_true", help="Do not start the Gradio UI.")
    parser.add_argument(
        "--no-client", action="store_true", help="Do not start the Node.js frontend."
    )

    # Configuration
    parser.add_argument(
        "--stage", choices=["dev", "test"], default="dev", help="Application stage."
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for the Python backend.")
    parser.add_argument(
        "--gradio-port", type=int, help="Port for the Gradio UI (defaults to 7860)."
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host address for servers.")
    parser.add_argument(
        "--listen", action="store_true", help="Listen on 0.0.0.0 (overrides --host)."
    )
    parser.add_argument("--share", action="store_true", help="Create a public Gradio sharing link.")
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug/reload mode for services."
    )
    parser.add_argument("--env-file", help="Path to a custom .env file to load.")

    args = parser.parse_args()

    # Use 0.0.0.0 if --listen is specified
    host = "0.0.0.0" if args.listen else args.host

    # Set environment file if specified
    if args.env_file:
        env_path = Path(args.env_file)
        if env_path.exists():
            from dotenv import load_dotenv

            load_dotenv(env_path)
            logger.info(f"Loaded environment variables from {env_path}")
        else:
            logger.error(f"Environment file not found: {env_path}")
            sys.exit(1)

    # Check Python version
    check_python_version()

    # Determine venv path
    venv_path = ROOT_DIR / VENV_DIR

    # Setup mode
    if args.setup or args.update_deps:
        if not args.no_venv:
            create_venv(venv_path, args.force_recreate_venv)
            install_uv(venv_path)
            setup_dependencies(venv_path, args.update_deps)

        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        logger.info("Setup completed successfully.")
        return

    # If not in setup mode, ensure venv exists (unless --no-venv is specified)
    if not args.no_venv and not venv_path.exists():
        logger.error(
            f"Virtual environment does not exist at {venv_path}. Please run with --setup first."
        )
        sys.exit(1)

    # Start services
    if not args.no_backend:
        start_backend(venv_path, host, args.port, args.debug)
        time.sleep(2)  # Brief pause to let backend start

    if not args.no_ui:
        start_gradio_ui(venv_path, host, args.gradio_port, args.debug, args.share)

    if not args.no_client:
        # Note: The client and server-ts might require additional parameters or configuration
        start_client()



    logger.info("All selected services started. Press Ctrl+C to shut down.")
    wait_for_processes()


if __name__ == "__main__":
    main()
