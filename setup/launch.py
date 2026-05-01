#!/usr/bin/env python3
"""
EmailIntelligence Unified Launcher

Legacy Component
This module is being phased out in favor of the new launcher in launch.py.
The new launcher provides better modularity and cross-platform support.
"""

import logging
import os
import platform
import shutil
import subprocess
import sys
import time
import venv
from pathlib import Path
from typing import List

try:
    from dotenv import load_dotenv

    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    load_dotenv = None

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("launcher")

# --- Global state ---
ROOT_DIR = Path(__file__).parent.parent.resolve()
process_manager = None  # Placeholder for process manager

# --- Constants ---
PYTHON_MIN_VERSION = (3, 12)
PYTHON_MAX_VERSION = (3, 13)
VENV_DIR = "venv"
CONDA_ENV_NAME = os.getenv("CONDA_ENV_NAME", "base")


# --- Helper Functions ---
def is_wsl() -> bool:
    """Check if running in WSL."""
    return (
        "microsoft" in platform.release().lower()
        if platform.system() == "Linux"
        else False
    )


def is_conda_available() -> bool:
    """Check if Conda is available on the system."""
    return shutil.which("conda") is not None


def get_conda_env_info() -> dict:
    """Get information about the current Conda environment."""
    conda_env = os.environ.get("CONDA_DEFAULT_ENV", None)
    is_active = conda_env is not None
    return {"is_active": is_active, "name": conda_env}


def activate_conda_env(env_name: str = None) -> bool:
    """Attempt to activate a Conda environment."""
    if env_name is None:
        env_name = CONDA_ENV_NAME
    try:
        result = subprocess.run(
            ["conda", "activate", env_name],
            capture_output=True,
            text=True,
            shell=True if os.name == "nt" else False
        )
        return result.returncode == 0
    except Exception:
        return False


def get_python_executable() -> Path:
    """Get the Python executable to use."""
    # Try to use venv Python first
    venv_python = get_venv_executable(ROOT_DIR / VENV_DIR, "python")
    if venv_python.exists():
        return venv_python
    
    # Fall back to current Python
    return Path(sys.executable)


def validate_port(port: int) -> int:
    """Validate port number."""
    if port < 1 or port > 65535:
        raise ValueError(f"Port must be between 1 and 65535, got {port}")
    return port


def validate_host(host: str) -> str:
    """Validate host address."""
    if not host:
        raise ValueError("Host cannot be empty")
    return host


def check_for_merge_conflicts() -> bool:
    """Check for unresolved merge conflicts in the codebase."""
    conflict_markers = ["<<<<<<<", "=======", ">>>>>>>"]
    conflict_found = False
    
    # Check common source directories for merge conflicts
    check_dirs = ["scripts/", "src/", "setup/"]
    for check_dir in check_dirs:
        check_path = ROOT_DIR / check_dir
        if check_path.exists():
            for py_file in check_path.rglob("*.py"):
                try:
                    content = py_file.read_text()
                    for marker in conflict_markers:
                        if marker in content:
                            logger.error(f"Merge conflict detected in: {py_file}")
                            conflict_found = True
                except Exception:
                    pass
    
    if conflict_found:
        logger.error("Unresolved merge conflicts found. Please resolve before proceeding.")
        return False
    
    logger.info("No merge conflicts detected.")
    return True


def setup_wsl_environment():
    """Setup WSL-specific environment variables if in WSL"""
    if not is_wsl():
        return

    if "DISPLAY" not in os.environ:
        os.environ["DISPLAY"] = ":0"

    os.environ["MPLBACKEND"] = "Agg"
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    os.environ["PYTHONUNBUFFERED"] = "1"
    os.environ["LIBGL_ALWAYS_INDIRECT"] = "1"

    logger.info("WSL environment detected - applied optimizations")


def check_wsl_requirements():
    """Check WSL-specific requirements and warn if needed"""
    if not is_wsl():
        return

    try:
        result = subprocess.run(["xset", "-q"], capture_output=True, timeout=2)
        if result.returncode != 0:
            logger.warning("X11 server not accessible - GUI applications may not work")
            logger.info("Install VcXsrv, MobaXterm, or similar X11 server on Windows")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


def check_python_version():
    """Check if the current Python version is compatible."""
    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        logger.error(
            f"Python version {current_version} not supported. "
            f"Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )
        sys.exit(1)
    logger.info(f"Python version {platform.python_version()} is compatible.")


def check_required_components() -> bool:
    """Check for required components and configurations."""
    issues = []

    current_version = sys.version_info[:2]
    if not (PYTHON_MIN_VERSION <= current_version <= PYTHON_MAX_VERSION):
        issues.append(
            f"Python version {current_version} is not compatible. "
            f"Required: {PYTHON_MIN_VERSION[0]}.{PYTHON_MIN_VERSION[1]}-{PYTHON_MAX_VERSION[0]}.{PYTHON_MAX_VERSION[1]}"
        )

    required_dirs = ["backend", "client", "shared", "tests"]
    for dir_name in required_dirs:
        if not (ROOT_DIR / dir_name).exists():
            issues.append(f"Required directory '{dir_name}' is missing.")

    required_files = ["pyproject.toml", "README.md", "requirements.txt"]
    for file_name in required_files:
        if not (ROOT_DIR / file_name).exists():
            issues.append(f"Required file '{file_name}' is missing.")

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


def get_venv_executable(venv_path: Path, executable: str) -> Path:
    """Get the path to a specific executable in the virtual environment."""
    scripts_dir = "Scripts" if platform.system() == "Windows" else "bin"
    return (
        venv_path
        / scripts_dir
        / (f"{executable}.exe" if platform.system() == "Windows" else executable)
    )


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
        try:
            subprocess.run([str(python_exe), "-c", "import poetry"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([str(python_exe), "-m", "pip", "install", "poetry"], "Installing Poetry")

        run_command(
            [str(python_exe), "-m", "poetry", "install", "--with", "dev"],
            "Installing dependencies with Poetry",
            cwd=ROOT_DIR,
        )
    else:
        try:
            subprocess.run([str(python_exe), "-c", "import uv"], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            run_command([str(python_exe), "-m", "pip", "install", "uv"], "Installing uv")

        install_notmuch_matching_system()


def install_notmuch_matching_system():
    try:
        result = subprocess.run(
            ["notmuch", "--version"], capture_output=True, text=True, check=True
        )
        version_line = result.stdout.strip()
        version = version_line.split()[1]
        major_minor = ".".join(version.split(".")[:2])
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("notmuch not found on system, skipping version-specific install")


def download_nltk_data(venv_path=None):
    python_exe = get_python_executable()

    nltk_download_script = """
try:
    import nltk
    packages = ['punkt', 'punkt_tab', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'vader_lexicon', 'omw-1.4']
    for package in packages:
        try:
            nltk.download(package, quiet=True)
            print(f"Downloaded NLTK package: {package}")
        except Exception as e:
            print(f"Failed to download {package}: {e}")
    print("NLTK data download completed.")
except ImportError:
    print("NLTK not available, skipping download.")
except Exception as e:
    print(f"NLTK download failed: {e}")
"""

    logger.info("Downloading NLTK data...")
    result = subprocess.run(
        [str(python_exe), "-c", nltk_download_script], cwd=ROOT_DIR, capture_output=True, text=True
    )
    if result.returncode != 0:
        logger.error(f"Failed to download NLTK data: {result.stderr}")
        logger.warning("NLTK data download failed, but continuing setup...")
    else:
        logger.info("NLTK data downloaded successfully.")

    textblob_download_script = """
try:
    from textblob import download_corpora
    download_corpora()
    print("TextBlob corpora download completed.")
except ImportError:
    print("TextBlob not available, skipping corpora download.")
except Exception as e:
    print(f"TextBlob corpora download failed: {e}")
"""

    logger.info("Downloading TextBlob corpora...")
    result = subprocess.run(
        [str(python_exe), "-c", textblob_download_script],
        cwd=ROOT_DIR,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if result.returncode != 0:
        logger.warning(f"TextBlob corpora download failed: {result.stderr}")
        logger.warning("Continuing setup without TextBlob corpora...")
    else:
        logger.info("TextBlob corpora downloaded successfully.")


def check_uvicorn_installed() -> bool:
    """Check if uvicorn is installed."""
    python_exe = get_python_executable()
    try:
        result = subprocess.run(
            [str(python_exe), "-c", "import uvicorn"], capture_output=True, text=True
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
    return run_command(cmd, desc, cwd=ROOT_DIR / directory)


def setup_node_dependencies(service_path: Path, service_name: str):
    """Install npm dependencies for a Node.js service."""
    if not (service_path / "package.json").exists():
        logger.warning(
            f"package.json not found for {service_name}, skipping dependency installation."
        )
        return
    logger.info(f"Installing npm dependencies for {service_name}...")
    run_command(["npm", "install"], f"Installing {service_name} dependencies", cwd=service_path)


def start_client():
    """Start the Node.js frontend."""
    logger.info("Starting Node.js frontend...")
    if not install_nodejs_dependencies("client"):
        return None


def start_server_ts():
    """Start the TypeScript backend server."""
    logger.info("Starting TypeScript backend server...")
    if not shutil.which("npm"):
        logger.warning("npm not found. Skipping TypeScript backend server startup.")
        return None

    pkg_json_path = ROOT_DIR / "backend" / "server-ts" / "package.json"
    if not pkg_json_path.exists():
        logger.debug(
            "No package.json in 'backend/server-ts/', skipping TypeScript backend server startup."
        )
        return None


def start_backend(host: str, port: int, debug: bool = False):
    python_exe = get_python_executable()
    cmd = [
        str(python_exe),
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
    process_manager.add_process(process)


def start_gradio_ui(host, port, share, debug):
    logger.info("Starting Gradio UI...")
    python_exe = get_python_executable()
    cmd = [str(python_exe), "-m", "src.main"]
    if share:
        cmd.append("--share")
    if debug:
        cmd.append("--debug")
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT_DIR)
    process = subprocess.Popen(cmd, cwd=ROOT_DIR, env=env)
    process_manager.add_process(process)


def handle_setup(args, venv_path):
    """Handles the complete setup process."""
    logger.info("Starting environment setup...")

    if args.use_conda:
        logger.info("Using Conda environment - assuming dependencies are already installed")
    else:
        create_venv(venv_path, args.force_recreate_venv)
        install_package_manager(venv_path, "uv")
        setup_dependencies(venv_path, False)
        if not args.no_download_nltk:
            download_nltk_data(venv_path)

        setup_node_dependencies(ROOT_DIR / "client", "Frontend Client")
        setup_node_dependencies(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend")
    logger.info("Setup complete.")


def prepare_environment(args):
    """Prepares the environment for running the application."""
    if not args.no_venv:
        if not activate_conda_env():
            venv_path = ROOT_DIR / VENV_DIR
            create_venv(venv_path)
        if args.update_deps:
            setup_dependencies(ROOT_DIR / VENV_DIR, False)
    if not args.no_download_nltk:
        download_nltk_data()


def start_services(args):
    """Starts the required services based on arguments."""
    api_url = args.api_url or f"http://{args.host}:{args.port}"

    if not args.frontend_only:
        start_backend(args.host, args.port, args.debug)
        start_node_service(ROOT_DIR / "backend" / "server-ts", "TypeScript Backend", 8001, api_url)

    if not args.api_only:
        start_gradio_ui(args.host, 7860, args.share, args.debug)
        start_node_service(ROOT_DIR / "client", "Frontend Client", args.frontend_port, api_url)


def print_system_info():
    """Print detailed system, Python, and project configuration information."""
    print("=== System Information ===")
    print(f"OS: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")

    print("\n=== Project Information ===")
    print(f"Project Root: {ROOT_DIR}")
    print(f"Python Path: {os.environ.get('PYTHONPATH', 'Not set')}")

    print("\n=== Environment Status ===")
    venv_path = ROOT_DIR / VENV_DIR
    if venv_path.exists():
        print(f"Virtual Environment: {venv_path} (exists)")
        python_exe = get_venv_executable(venv_path, "python")
        if python_exe.exists():
            print(f"Venv Python: {python_exe}")
        else:
            print("Venv Python: Not found")
    else:
        print(f"Virtual Environment: {venv_path} (not created)")

    conda_available = is_conda_available()
    print(f"Conda Available: {conda_available}")
    if conda_available:
        conda_env = os.environ.get("CONDA_DEFAULT_ENV", "None")
        print(f"Current Conda Env: {conda_env}")

    node_available = check_node_npm_installed()
    print(f"Node.js/npm Available: {node_available}")

    print("\n=== Configuration Files ===")
    config_files = [
        "pyproject.toml",
        "requirements.txt",
        "requirements-dev.txt",
        "package.json",
        "launch-user.env",
        ".env",
    ]
    for cf in config_files:
        exists = (ROOT_DIR / cf).exists()
        print(f"{cf}: {'Found' if exists else 'Not found'}")


def main():
    """Legacy Component - This launcher is being phased out in favor of launch.py"""
    import argparse
    parser = argparse.ArgumentParser(description="EmailIntelligence Unified Launcher (Legacy)")

    parser.add_argument("--setup", action="store_true", help="Set up the environment")
    parser.add_argument("--stage", choices=["dev", "test"], default="dev", help="Application mode")

    parser.add_argument("--force-recreate-venv", action="store_true", help="Force recreation of the venv.")
    parser.add_argument("--use-conda", action="store_true", help="Use Conda environment instead of venv.")
    parser.add_argument("--conda-env", type=str, default="base", help="Conda environment name")
    parser.add_argument("--no-venv", action="store_true", help="Don't create or use a virtual environment.")
    parser.add_argument("--update-deps", action="store_true", help="Update dependencies before launching.")
    parser.add_argument("--skip-python-version-check", action="store_true", help="Skip Python version check.")
    parser.add_argument("--no-download-nltk", action="store_true", help="Skip downloading NLTK data.")
    parser.add_argument("--skip-prepare", action="store_true", help="Skip all environment preparation steps.")
    parser.add_argument("--loglevel", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO")

    parser.add_argument("--port", type=int, default=8000, help="Specify the port to run on.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Specify the host to run on.")
    parser.add_argument("--frontend-port", type=int, default=5173, help="Specify the frontend port.")
    parser.add_argument("--api-url", type=str, help="Specify the API URL for the frontend.")
    parser.add_argument("--api-only", action="store_true", help="Run only the API server.")
    parser.add_argument("--frontend-only", action="store_true", help="Run only the frontend.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("--system-info", action="store_true", help="Print system information.")
    parser.add_argument("--share", action="store_true", help="Create a public URL.")

    args = parser.parse_args()

    # Setup logging
    logging.getLogger().setLevel(getattr(logging, args.loglevel))

    # Legacy argument handling
    setup_wsl_environment()
    check_wsl_requirements()

    if not args.skip_python_version_check:
        check_python_version()

    if DOTENV_AVAILABLE:
        user_env_file = ROOT_DIR / "launch-user.env"
        if user_env_file.exists():
            load_dotenv(user_env_file)
            logger.info(f"Loaded user environment variables from {user_env_file}")

        env_file = ".env"
        if os.path.exists(env_file):
            load_dotenv(env_file)

    global CONDA_ENV_NAME
    if args.conda_env and args.conda_env != "base":
        CONDA_ENV_NAME = args.conda_env
        args.use_conda = True

    if not args.skip_prepare and not validate_environment():
        return 1

    if args.setup:
        venv_path = ROOT_DIR / VENV_DIR
        handle_setup(args, venv_path)
        return 0

    if args.use_conda:
        if not is_conda_available():
            logger.error("Conda is not available. Please install Conda or use venv.")
            return 1

    if not args.skip_prepare and not args.use_conda:
        prepare_environment(args)

    if args.system_info:
        print_system_info()
        return 0

    start_services(args)

    logger.info("All services started. Press Ctrl+C to shut down.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutdown signal received.")
    finally:
        process_manager.cleanup()

    return 0


if __name__ == "__main__":
    sys.exit(main())